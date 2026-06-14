#
# Copyright (c) 2023-2026 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations  # postpone evaluation of annotations

import base64
import datetime
import hashlib
import io
import logging
import mimetypes
import os
import shutil
import tempfile
import uuid
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from sys import maxsize as MAXSIZE
from typing import IO, TYPE_CHECKING, BinaryIO
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from typing import Self

    from ivcap_client.ivcap import IVCAP, URN

from tusclient.client import TusClient

from ivcap_client.api.artifact import artifact_list, artifact_read, artifact_upload
from ivcap_client.aspect import Aspect
from ivcap_client.models.artifact_list_item import ArtifactListItem
from ivcap_client.models.artifact_list_rt import ArtifactListRT
from ivcap_client.models.artifact_status_rt import ArtifactStatusRT
from ivcap_client.models.artifact_status_rt_status import ArtifactStatusRTStatus
from ivcap_client.utils import BaseIter, Links, _set_fields, process_error


@dataclass
class Artifact:
    """This class represents an artifact record
    stored at a particular IVCAP deployment"""

    id: str
    status: ArtifactStatusRTStatus
    name: str | None = None
    size: int | None = None
    mime_type: str | None = None
    created_at: datetime.datetime | None = None
    last_modified_at: datetime.datetime | None = None

    etag: str | None = None

    policy: URN | None = None
    account: URN | None = None

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
        p = [
            "id",
            "name",
            "size",
            "mime-type",
            "last-modified-at",
            "created-at",
            "policy",
            "etag",
            "account",
        ]
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
            return process_error("place_order", r)
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
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        with temp_file as f:
            for chunk in self.as_stream():
                f.write(chunk)
        return CMPath(temp_file.name)

    @property
    def metadata(self) -> Iterator[Aspect]:
        return self._ivcap.list_aspects(entity=self.id)

    def add_metadata(
        self,
        aspect: dict[str, any],
        *,
        schema: str | None = None,
        policy: URN | None = None,
    ) -> Artifact:
        """Add a metadata 'aspect' to this artifact. The 'schema' of the aspect, if not defined
        is expected to found in the 'aspect' under the '$schema' key.

        Args:
            aspect (dict): The aspect to be attached
            schema (Optional[str], optional): Schema of the aspect. Defaults to 'aspect["$schema"]'.
            policy: Optional[URN]: Set specific policy controlling access ('urn:ivcap:policy:...').

        Returns:
            self: To enable chaining
        """
        self._ivcap.add_aspect(
            entity=self.id, aspect=aspect, schema=schema, policy=policy
        )
        return self

    def __repr__(self):
        return (
            f"<Artifact id={self.id}, status={self._status if self._status else '???'}>"
        )


class ArtifactIter(BaseIter[Artifact, ArtifactListItem]):
    def __init__(self, ivcap: IVCAP, **kwargs):
        super().__init__(ivcap, **kwargs)

    def _next_el(self, el) -> Artifact:
        return Artifact._from_list_item(el, self._ivcap)

    def _get_list(self) -> list[ArtifactListItem]:
        r = artifact_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300:
            return process_error("artifact_list", r)
        l: ArtifactListRT = r.parsed
        self._links = Links(l.links)
        return l.items


class LocalFileArtifact:
    """This class represents a loca file masquerading as an artifact"""

    def __init__(self, id: str):
        if id.startswith("file://"):
            id = f"urn:${id}"
        self.id = id
        fn = id[len("urn:file://") :]
        fp = Path(fn)
        self._fp = fp
        if not (fp.exists() and fp.is_file()):
            raise ValueError(f"file '{fn}' does not exist")
        self.name = fp.name

        stats = fp.stat()
        self.size = stats.st_size
        self.last_modified_at = datetime.fromtimestamp(stats.st_mtime)
        self.created_at = self.last_modified_at  # keep it simple

    def open(self) -> io.IOBase:
        """Return a file-like object for the artifact data"""
        return open(self._fp, encoding="utf-8")

    def as_local_file(self) -> Path:
        # Return the Path to the local file but ensure it won't be deleted
        return SafePath(self._fp)

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

    def __repr__(self) -> str:
        return f"<LocalFileArtifact id={self.id}>"


class LocalIVCAP:
    """A filesystem-backed implementation of the IVCAP client interface for use
    in local development and testing.  All artifacts are written under ``base_dir``.
    No network calls are made.

    This is the drop-in replacement for :class:`~ivcap_client.ivcap.IVCAP` when no
    IVCAP platform URL is available — for example when running a service locally with
    a test JSON file.

    Use the factory method :meth:`~ivcap_client.ivcap.IVCAP.local` to obtain an
    instance, or construct one directly:

    .. code-block:: python

        from ivcap_client import LocalIVCAP

        ivcap = LocalIVCAP(base_dir="./my-artifacts")
        artifact = ivcap.upload_artifact(name="report.txt", file_path="/tmp/report.txt")
        print(artifact.id)  # urn:file:///abs/path/to/my-artifacts/report.txt

    The root directory for local artifact storage can also be configured via the
    ``IVCAP_LOCAL_DIR`` environment variable (default: ``./ivcap-artifacts``).
    """

    def __init__(self, base_dir: str | Path = "./ivcap-artifacts"):
        """Create a new LocalIVCAP instance.

        Args:
            base_dir: Root directory under which all artifacts are stored.
                Relative paths are resolved relative to the current working
                directory at the time of the first upload.  The directory is
                created on demand.  Defaults to ``./ivcap-artifacts``.
        """
        self._base_dir = Path(base_dir)

    @property
    def base_dir(self) -> Path:
        """The root directory for local artifact storage."""
        return self._base_dir

    def upload_artifact(
        self,
        *,
        name: str | None = None,
        file_path: str | None = None,
        io_stream: IO | None = None,
        content_type: str | None = None,
        content_size: int | None = -1,
        collection: URN | None = None,
        policy: URN | None = None,
        **kwargs,
    ) -> LocalFileArtifact:
        """Write content to the local filesystem and return a :class:`LocalFileArtifact`.

        The content is written to ``base_dir / name``.  Parent directories are
        created automatically (``mkdir -p`` semantics).

        Args:
            name: Relative path under ``base_dir`` for the saved artifact.
                May contain subdirectory components (e.g. ``"results/output.csv"``).
                If ``None``, a UUID-based filename is generated (preserving the
                source file extension when ``file_path`` is given).
            file_path: Local source file to copy into ``base_dir``.
            io_stream: Byte-stream (or text-stream) to write into ``base_dir``.
                Provide either ``file_path`` or ``io_stream`` — not both.
            content_type: Accepted for interface compatibility; ignored locally.
            content_size: Accepted for interface compatibility; ignored locally.
            collection: Accepted for interface compatibility; silently ignored.
            policy: Accepted for interface compatibility; silently ignored.
            **kwargs: Any additional keyword arguments are silently ignored so
                that callers can pass platform-specific options without branching.

        Returns:
            LocalFileArtifact: A local-file artifact whose ``.id`` is
            ``urn:file://<absolute_path>``.

        Raises:
            ValueError: If neither ``file_path`` nor ``io_stream`` is provided.
        """
        if not (file_path or io_stream):
            raise ValueError("require either 'file_path' or 'io_stream'")

        if name is None:
            suffix = Path(file_path).suffix if file_path else ""
            name = f"{uuid.uuid4()}{suffix}"

        dest = self._base_dir / name
        dest.parent.mkdir(parents=True, exist_ok=True)

        if file_path:
            shutil.copy2(file_path, dest)
        else:
            raw = io_stream.read()
            if isinstance(raw, str):
                dest.write_text(raw)
            else:
                dest.write_bytes(raw)

        urn = f"urn:file://{dest.resolve()}"
        logger.info("LocalIVCAP: written artifact '%s' → %s", name, dest)
        return LocalFileArtifact(urn)

    def get_artifact(self, id: str) -> LocalFileArtifact:
        """Return a :class:`LocalFileArtifact` for the given local-file URN.

        Args:
            id: A ``file://`` or ``urn:file://`` URN pointing to a local file.

        Returns:
            LocalFileArtifact: The local file artifact.
        """
        return LocalFileArtifact(id)

    def __repr__(self) -> str:
        return f"<LocalIVCAP base_dir={self._base_dir}>"


#### HELPER FUNCTIONS ####


def upload_artifact(
    ivcap: IVCAP,
    *,
    name: str | None = None,
    file_path: str | None = None,
    io_stream: IO | None = None,
    content_type: str | None = None,
    content_size: int | None = -1,
    collection: URN | None = None,
    policy: URN | None = None,
    chunk_size: int | None = MAXSIZE,
    retries: int | None = 0,
    retry_delay: int | None = 30,
    force_upload: bool | None = False,
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
        "x_content_type": content_type,
        "x_content_length": content_size,
        "tus_resumable": "1.0.0",
    }
    if name:
        n = base64.b64encode(bytes(name, "utf-8"))
        kwargs["x_name"] = n
    if collection:
        if not collection.startswith("urn:"):
            raise ValueError(f"collection '{collection} is not a URN.")
        kwargs["x_collection"] = collection
    if policy:
        if not policy.startswith("urn:ivcap:policy:"):
            raise ValueError(f"policy '{collection} is not a policy URN.")
        kwargs["x_policy"] = policy

    r = artifact_upload.sync_detailed(client=ivcap._client, **kwargs)
    if r.status_code >= 300:
        return process_error("upload_artifact", r)
    res: ArtifactStatusRT = r.parsed

    h = {}
    if ivcap._token:
        h["Authorization"] = f"Bearer {ivcap._token}"
    # NOTE: See coment on fix_data_ref
    data_url = ivcap._url + fix_data_ref(res.data_href)
    # print(f"... res.data_href: '{res.data_href}' data_url: '{data_url}")
    c = TusClient(data_url, headers=h)
    kwargs = {
        "file_path": file_path,
        "file_stream": io_stream,
        "chunk_size": chunk_size,
        "retries": retries,
        "retry_delay": retry_delay,
    }
    uploader = c.uploader(**kwargs)
    uploader.set_url(data_url)  # not sure why I need to set it here again
    uploader.upload()

    kwargs = res.to_dict()
    if file_path:
        mark_file_already_uploaded(res.id, file_path)
    kwargs["status"] = None
    a = Artifact(ivcap, **kwargs)
    a.status  # force status update as it will have change
    return a


def check_file_already_uploaded(file_path: str) -> str | None:
    df = _upload_marker(file_path)

    if os.path.isfile(df) and os.access(df, os.R_OK):
        with open(df) as f:
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
_CONCRETE_PATH = type(Path())


class SafePath(_CONCRETE_PATH):
    """
    A Path object that disables the destructive 'unlink' (delete) method.
    """

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

    def __init__(self, buffer: BinaryIO):
        self._buffer: BinaryIO = buffer
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


class CMPath(_CONCRETE_PATH):
    """
    A pathlib.Path subclass that acts as a context manager
    for a file and ensuring its cleanup on exit.
    """

    def __new__(cls, *pathsegments) -> Self:
        # Path subclasses must implement __new__; delegate to the concrete path type.
        return super().__new__(cls, *pathsegments)

    # --- Context Manager Protocol ---

    def __enter__(self) -> Self:
        """Returns the fully initialized CMPath instance."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Cleans up the file."""
        try:
            if self.exists():
                self.unlink()  # Path.unlink() is the correct deletion method
        except Exception as e:
            print(f"ERROR: Could not remove file {self}: {e}")
