#
# Copyright (c) 2023-2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations
import mimetypes
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Iterator, List, Optional, BinaryIO
from urllib.parse import urlparse

if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN
    from typing import Self

import datetime
from dataclasses import dataclass
from datetime import datetime
from tusclient.client import TusClient
import mimetypes
import base64
import os
import io
from sys import maxsize as MAXSIZE

from ivcap_client.api.artifact import artifact_list, artifact_read, artifact_upload
from ivcap_client.models.artifact_list_rt import ArtifactListRT
from ivcap_client.models.artifact_status_rt import ArtifactStatusRT
from ivcap_client.models.artifact_list_item import ArtifactListItem
from ivcap_client.models.artifact_status_rt_status import ArtifactStatusRTStatus

from ivcap_client.utils import BaseIter, Links, _set_fields, process_error
from ivcap_client.aspect import Aspect

@dataclass
class Artifact:
    """This class represents an artifact record
    stored at a particular IVCAP deployment"""

    id: str
    status: ArtifactStatusRTStatus
    name: Optional[str] = None
    size: Optional[int] = None
    mime_type: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_at: Optional[datetime.datetime] = None

    etag: Optional[str] = None

    policy: Optional[URN] = None
    account: Optional[URN] = None

    @classmethod
    def _from_list_item(cls, item: ArtifactListItem, ivcap: IVCAP):
        kwargs = item.to_dict()
        return cls(ivcap, **kwargs)

    def __init__(self, ivcap: IVCAP, **kwargs):
        if not ivcap:
            raise ValueError("missing 'ivcap' argument")
        self._ivcap = ivcap
        self.__update__(**kwargs)

    def __update__(self, **kwargs):
        p = ["id", "name", "size", "mime-type", "last-modified-at",
             "created-at", "policy", "etag", "account"]
        hp = ["status", "cache_of", "data-href"]
        _set_fields(self, p, hp, kwargs)

        if self._data_href:
            self._data_href = fix_data_ref(self._data_href)
        if not self.id:
            raise ValueError("missing 'id' for Artifact")

    @property
    def urn(self) -> str:
        return self.id

    @property
    def status(self, refresh=True) -> ArtifactStatusRT:
        if refresh or not self._status:
            self.refresh()
        return self._status

    def refresh(self) -> Artifact:
        r = artifact_read.sync_detailed(client=self._ivcap._client, id=self.id)
        if r.status_code >= 300:
            return process_error('place_order', r)
        kwargs = r.parsed.to_dict()
        self.__update__(**kwargs)
        return self

    def open(self) -> io.IOBase:
        """Return a file-like object for the artifact data"""
        client = self._ivcap._client.get_httpx_client()
        response = client.get(self._data_href)
        response.raise_for_status()
        b = io.BytesIO(response.content)
        return ProxyFile(b)

    def as_stream(self, chunk_size: int = 8192) -> Iterator[bytes]:
        """
        Stream the artifact data in chunks.

        Args:
            chunk_size (int): Number of bytes to read per chunk. Default is 8192.

        Yields:
            bytes: Next chunk of artifact data.
        """
        client = self._ivcap._client.get_httpx_client()
        with client.stream("GET", self._data_href) as response:
            response.raise_for_status()
            for chunk in response.iter_bytes(chunk_size=chunk_size):
                yield chunk

    def as_local_file(self) -> Path:
        """Download the artifact data to a local temporary file and return the Path"""
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        with temp_file as f:
            for chunk in self.as_stream():
                f.write(chunk)
        return CMPath(temp_file.name)

    @property
    def metadata(self) -> Iterator[Aspect]:
        return self._ivcap.list_aspects(entity=self.id)

    def add_metadata(self,
                     aspect: Dict[str,any],
                     *,
                     schema: Optional[str]=None,
                     policy: Optional[URN]=None,
    ) -> 'Artifact':
        """Add a metadata 'aspect' to this artifact. The 'schema' of the aspect, if not defined
        is expected to found in the 'aspect' under the '$schema' key.

        Args:
            aspect (dict): The aspect to be attached
            schema (Optional[str], optional): Schema of the aspect. Defaults to 'aspect["$schema"]'.
            policy: Optional[URN]: Set specific policy controlling access ('urn:ivcap:policy:...').

        Returns:
            self: To enable chaining
        """
        self._ivcap.add_aspect(entity=self.id, aspect=aspect, schema=schema, policy=policy)
        return self

    def __repr__(self):
        return f"<Artifact id={self.id}, status={self._status if self._status else '???'}>"

class ArtifactIter(BaseIter[Artifact, ArtifactListItem]):
    def __init__(self, ivcap: 'IVCAP', **kwargs):
        super().__init__(ivcap, **kwargs)

    def _next_el(self, el) -> Artifact:
        return Artifact._from_list_item(el, self._ivcap)

    def _get_list(self) -> List[ArtifactListItem]:
        r = artifact_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('artifact_list', r)
        l: ArtifactListRT = r.parsed
        self._links = Links(l.links)
        return l.items

class LocalFileArtifact:
    """This class represents a loca file masquerading as an artifact"""
    def __init__(self, id: str):
        if id.startswith("file://"):
            id = f"urn:${id}"
        self.id = id
        fn = id[len("urn:file://"):]
        fp = Path(fn)
        self._fp = fp
        if not(fp.exists() and fp.is_file()):
            raise ValueError(f"file '{fn}' does not exist")
        self.name = fp.name

        stats = fp.stat()
        self.size = stats.st_size
        self.last_modified_at = datetime.fromtimestamp(stats.st_mtime)
        self.created_at = self.last_modified_at # keep it simple

    def open(self) -> io.IOBase:
        """Return a file-like object for the artifact data"""
        return open(self._fp, 'r', encoding='utf-8')

    def as_local_file(self) -> Path:
        # Return the Path to the local file but ensure it won't be deleted
        return CMPath(SafePath(self._fp))

    def refresh(self) -> Artifact:
        return self

    @property
    def status(self, refresh=True) -> ArtifactStatusRT:
        return ArtifactStatusRT(status=ArtifactStatusRTStatus.READY)

    @property
    def etag(self) -> str:
        return md5sum(f"{self.name}-{self.last_modified_at.timestamp()}")

    @property
    def mime_type(self) -> str:
        mime_type, _ = mimetypes.guess_type(self._fp.name)
        # Fallback if mimetypes can't guess from the extension
        if not mime_type:
            mime_type = "application/octet-stream"
        return mime_type

#### HELPER FUNCTIONS ####

def upload_artifact(ivcap: IVCAP,
                    *,
                    name: Optional[str] = None,
                    file_path: Optional[str] = None,
                    io_stream: Optional[IO] = None,
                    content_type:  Optional[str] = None,
                    content_size: Optional[int] = -1,
                    collection: Optional[URN] = None,
                    policy: Optional[URN] = None,
                    chunk_size: Optional[int] = MAXSIZE,
                    retries: Optional[int] = 0,
                    retry_delay: Optional[int] = 30,
                    force_upload: Optional[bool] = False,
    ) -> Artifact:
    """Uploads content which is either identified as a `file_path` or `io_stream`. In the
    latter case, content type need to be provided.

    Args:
        file_path (Optional[str]): File to upload
        io_stream (Optional[IO]): Content as IO stream.
        content_type (Optional[str]): Content type - needs to be declared for `io_stream`.
        content_size (Optional[int]): Overall size of content to be uploaded. Defaults to -1 (don't know).
        collection: Optional[URN]: Additionally adds artifact to named collection ('urn:...').
        policy: Optional[URN]: Set specific policy controlling access ('urn:ivcap:policy:...').
        chunk_size (Optional[int]): Chunk size to use for each individual upload. Defaults to MAXSIZE.
        retries (Optional[int]): The number of attempts should be made in the case of a failed upload. Defaults to 0.
        retry_delay (Optional[int], optional): How long (in seconds) should we wait before retrying a failed upload attempt. Defaults to 30.
        force_upload (Optional[bool], optional): Upload file even if it has been uploaded before.
    """

    if not (file_path or io_stream):
        raise ValueError("require either 'file_path' or 'io_stream'")
    if file_path:
        if not (os.path.isfile(file_path) and os.access(file_path, os.R_OK)):
            raise ValueError(f"file '{file_path}' doesn't exist or is not readable.")

    if not force_upload and file_path:
        aurn = check_file_already_uploaded(file_path)
        if aurn is not None:
            return ivcap.get_artifact(aurn)

    if not content_type and file_path:
        content_type, _ = mimetypes.guess_type(file_path)

    if not content_type:
        raise ValueError("missing 'content-type'")

    if content_size < 0 and file_path:
        # generate size of file from file_path
        content_size = os.path.getsize(file_path)

    kwargs = {
        'x_content_type': content_type,
        'x_content_length': content_size,
        'tus_resumable': "1.0.0",
    }
    if name:
        n = base64.b64encode(bytes(name, 'utf-8'))
        kwargs['x_name'] = n
    if collection:
        if not collection.startswith("urn:"):
            raise ValueError(f"collection '{collection} is not a URN.")
        kwargs['x_collection'] = collection
    if policy:
        if not policy.startswith("urn:ivcap:policy:"):
            raise ValueError(f"policy '{collection} is not a policy URN.")
        kwargs['x_policy'] = policy

    r = artifact_upload.sync_detailed(client=ivcap._client, **kwargs)
    if r.status_code >= 300 :
        return process_error('upload_artifact', r)
    res:ArtifactStatusRT = r.parsed

    h = {}
    if ivcap._token:
        h['Authorization'] = f"Bearer {ivcap._token}"
    # NOTE: See coment on fix_data_ref
    data_url = ivcap._url + fix_data_ref(res.data_href)
    # print(f"... res.data_href: '{res.data_href}' data_url: '{data_url}")
    c = TusClient(data_url, headers=h)
    kwargs = {
        'file_path': file_path,
        'file_stream': io_stream,
        'chunk_size': chunk_size,
        'retries': retries,
        'retry_delay': retry_delay,
    }
    uploader = c.uploader(**kwargs)
    uploader.set_url(data_url) # not sure why I need to set it here again
    uploader.upload()

    kwargs = res.to_dict()
    if file_path:
        mark_file_already_uploaded(res.id, file_path)
    kwargs["status"] = None
    a = Artifact(ivcap, **kwargs)
    a.status # force status update as it will have change
    return a

def check_file_already_uploaded(file_path: str) -> Optional[str]:
    df = _upload_marker(file_path)

    if os.path.isfile(df) and os.access(df, os.R_OK):
        with open(df, "r") as f:
            l = f.readlines()
            oh5, aid = l[0].split("|") if len(l) > 0 else [None, None]
            if oh5 and aid:
                h5 = md5sum(file_path)
                if oh5 == h5:
                    return aid.strip()
    return None

def mark_file_already_uploaded(id: str, file_path: str):
    df = _upload_marker(file_path)
    h5 = md5sum(file_path)
    with open(df, "w") as f:
        f.write(f"{h5}|{id}\n")

def _upload_marker(file_path: str):
    fn = os.path.basename(file_path)
    dn = os.path.dirname(file_path)
    df = os.path.join(dn, ".ivcap-" + fn + ".txt")
    return df

import hashlib
def md5sum(filename, blocksize=65536):
    h = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            h.update(block)
    return h.hexdigest()

def fix_data_ref(data_href):
    """NOTE: the artifact API still provides the full 'external' data url
    which causes problems internally. So we strip off the host and let it
    default to self._ivcap's base_url. May fail in the future!
    """
    durl = urlparse(data_href)
    return durl.path


### PROTECT FILES WHEN RUNNING LOCALLY ####
class SafePath(Path):
    """
    A Path object that disables the destructive 'unlink' (delete) method.
    """
    _flavour = Path()._flavour

    def unlink(self, missing_ok: bool = False):
        """
        Overrides the standard unlink method to prevent file deletion.
        Instead, just return.
        """
        return

class ProxyFile:
    """
    A custom class that acts as a Read-Only (Input) File-Like Object,
    proxying data from an internal io.BytesIO instance.
    Implements the Context Manager protocol for use with 'with' statements.
    """

    def __init__(self, buffer: io.BinaryIO):
        self._buffer:BinaryIO = buffer
        self._closed = False

    def __enter__(self) -> Self:
        """Sets up the context. Ensures the resource is open."""
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Cleans up the context. Closes the resource."""
        self.close()

    def read(self, size: int = -1) -> bytes:
        """Reads data from the internal buffer."""
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        return self._buffer.read(size)

    def readline(self, size: int = -1) -> bytes:
        """Reads a single line from the internal buffer."""
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        return self._buffer.readline(size)

    def readlines(self) -> list[bytes]:
        """Reads all lines into a list."""
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        return self._buffer.readlines()

    def seek(self, offset: int, whence: int = 0) -> int:
        """Changes the stream position."""
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        return self._buffer.seek(offset, whence)

    def tell(self) -> int:
        """Returns the current stream position."""
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        return self._buffer.tell()

    def close(self) -> None:
        """Closes the underlying buffer and marks this object as closed."""
        if not self.closed:
            self._buffer.close()
            self._closed = True

    @property
    def closed(self) -> bool:
        """Check if the file is closed."""
        return self._closed

    # The object should be iterable (yield lines)
    def __iter__(self):
        return self._buffer.__iter__()

# --- FIX for Path Subclassing ---
# Dynamically get the platform-specific flavour object from an instance of Path.
CONCRETE_PATH_FLAVOUR = Path()._flavour

class CMPath(Path):
    """
    A pathlib.Path subclass that acts as a context manager
    for a file and ensuring its cleanup on exit.
    """

    # 1. CRITICAL: Inherit the platform-specific flavour
    _flavour = CONCRETE_PATH_FLAVOUR

    def __new__(cls, filename: str) -> Self:
        instance = super().__new__(cls, filename)
        return instance

    # --- Context Manager Protocol ---

    def __enter__(self) -> Self:
        """Returns the fully initialized CMPath instance."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Cleans up the file."""
        try:
            if self.exists():
                self.unlink() # Path.unlink() is the correct deletion method
        except Exception as e:
            print(f"ERROR: Could not remove file {self._file_path}: {e}")
