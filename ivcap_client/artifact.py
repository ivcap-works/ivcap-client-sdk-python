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
import json
import logging
import mimetypes
import os
import shutil
import tempfile
import uuid
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime, timezone
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
from ivcap_client.exception import MissingParameterValue, ResourceNotFound
from ivcap_client.models.artifact_list_item import ArtifactListItem
from ivcap_client.models.artifact_list_rt import ArtifactListRT
from ivcap_client.models.artifact_status_rt import ArtifactStatusRT
from ivcap_client.models.artifact_status_rt_status import ArtifactStatusRTStatus
from ivcap_client.utils import BaseIter, Links, _set_fields, process_error


@dataclass
class Artifact:
    """Represents an artifact stored in an IVCAP deployment.

    An artifact is any binary or structured data blob produced or consumed by a job —
    an image, a CSV file, a NetCDF dataset, a trained model checkpoint, etc.

    Each artifact has two complementary parts:

    1. **Blob** — the raw bytes, stored in object storage (GCS/S3-compatible).
    2. **Aspects** — typed metadata records in the Datafabric describing the artifact's
       MIME type, size, provenance, and any domain annotations.

    Key properties:

    * ``id`` / ``urn`` — canonical ``urn:ivcap:artifact:<uuid>`` identifier
    * ``name`` — human-readable name
    * ``mime_type`` — MIME content type (e.g. ``"image/jpeg"``)
    * ``size`` — size in bytes
    * ``status`` — current :class:`~ivcap_client.models.ArtifactStatusRTStatus` value

    Reading artifact content:

    * :meth:`as_local_file` — **recommended** download method; saves to a temp file
      (auto-deleted on context exit) or to an explicit path.
    * :meth:`open` — returns a file-like object with all bytes loaded into memory
      (convenient for small files).
    * :meth:`as_stream` — yields raw ``bytes`` chunks for memory-efficient streaming
      or custom chunk processing.

    Example::

        artifact = ivcap.get_artifact("urn:ivcap:artifact:<uuid>")

        # Download to a temp file (auto-deleted when the 'with' block exits)
        with artifact.as_local_file() as path:
            data = path.read_bytes()

        # Download to a specific path (file is kept)
        path = artifact.as_local_file("/tmp/output.jpg")

        # Load entirely into memory
        with artifact.open() as f:
            data = f.read()
    """

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
        """Return a file-like object with the full artifact content loaded into memory.

        The entire artifact blob is fetched in a single HTTP request and wrapped in a
        :class:`ProxyFile` backed by an in-memory :class:`io.BytesIO` buffer.  This
        is convenient for small artifacts where memory is not a concern.

        .. warning::
            The full content is loaded into memory.  For large artifacts (hundreds of
            MB or more) prefer :meth:`as_stream` (chunked iteration) or
            :meth:`as_local_file` (stream-to-disk), both of which avoid holding the
            entire blob in RAM.

        Returns:
            ProxyFile: A readable, seekable, context-manager-compatible file-like
            object.  Call :meth:`~ProxyFile.read` or iterate over lines.

        Example::

            with artifact.open() as f:
                data = f.read()           # bytes
                text = data.decode("utf-8")
        """
        client = self._ivcap._client.get_httpx_client()
        response = client.get(self._data_href)
        response.raise_for_status()
        b = io.BytesIO(response.content)
        return ProxyFile(b)

    def as_stream(self, chunk_size: int = -1) -> Iterator[bytes]:
        """Stream the artifact content as a sequence of raw byte chunks.

        Uses an HTTP streaming GET so that only ``chunk_size`` bytes are buffered
        in memory at a time.  This is the lowest-level download method and is
        suitable when you need to:

        * Implement custom progress reporting.
        * Pipe artifact bytes into a third-party streaming API.
        * Process data incrementally without writing a local file.

        For simply saving the artifact to disk, :meth:`as_local_file` is more
        ergonomic.  For loading everything into memory at once, use :meth:`open`.

        Args:
            chunk_size (int): Number of bytes to read per chunk.  Pass ``-1``
                (the default) to let the SDK choose a chunk size automatically:
                ``max(8 KiB, min(artifact_size / 10, 10 MiB))``.  The artifact
                ``size`` attribute is used when available; if it is unknown the
                fallback is 8 KiB.

        Yields:
            bytes: The next chunk of raw artifact bytes.

        Example::

            # Stream to a file with progress reporting
            total = 0
            with open("/tmp/output.dat", "wb") as f:
                for chunk in artifact.as_stream():
                    f.write(chunk)
                    total += len(chunk)
            print(f"Downloaded {total} bytes")
        """
        chunk_size = _resolve_chunk_size(chunk_size, self.size)
        client = self._ivcap._client.get_httpx_client()
        with client.stream("GET", self._data_href) as response:
            response.raise_for_status()
            for chunk in response.iter_bytes(chunk_size=chunk_size):
                yield chunk

    def as_local_file(
        self,
        path: Path | None = None,
        *,
        chunk_size: int = -1,
        progress_callback: Callable[[int, int | None], None] | None = None,
    ) -> Path:
        """Download the artifact to a local file and return the path.

        This is the **recommended** method for saving artifact content to disk.
        It supports two usage patterns depending on whether ``path`` is supplied:

        **Temporary file (path omitted)** — a new temp file is created and a
        :class:`CMPath` is returned.  :class:`CMPath` is a context-manager-aware
        :class:`~pathlib.Path` subclass: when used in a ``with`` statement the
        file is **automatically deleted** when the block exits.  Use this pattern
        when you only need the file transiently::

            with artifact.as_local_file() as path:
                data = path.read_bytes()
            # temp file has been deleted here

        **Explicit path (path provided)** — the content is streamed to the given
        path (parent directories are created automatically).  A plain
        :class:`~pathlib.Path` is returned; the file is **not** deleted
        automatically.  Use this pattern when you want to keep the file::

            path = artifact.as_local_file("/tmp/output.jpg")
            # file remains at /tmp/output.jpg

        Args:
            path: Destination file path.  If ``None`` (default), a temporary file
                is created and wrapped in a self-deleting :class:`CMPath`.
                If a path is provided, the file is written there and a plain
                :class:`~pathlib.Path` is returned.
            chunk_size (int): Number of bytes to read per chunk.  Pass ``-1``
                (the default) to let the SDK choose automatically based on the
                artifact size (see :meth:`as_stream` for the formula).
            progress_callback: Optional callable invoked after each chunk is
                written.  Receives two arguments:

                * ``bytes_downloaded`` (int) — cumulative bytes written so far.
                * ``total_bytes`` (int | None) — total expected size in bytes,
                  or ``None`` if the artifact size is unknown.

                Example::

                    def on_progress(downloaded: int, total: int | None) -> None:
                        if total:
                            pct = downloaded / total * 100
                            print(f"\\r{pct:.1f}%", end="", flush=True)
                        else:
                            print(f"\\r{downloaded} bytes", end="", flush=True)

                    path = artifact.as_local_file(progress_callback=on_progress)

        Returns:
            :class:`CMPath` when ``path`` is ``None`` (context-manager, auto-delete).
            Plain :class:`~pathlib.Path` when ``path`` is provided (persists).

        Note:
            Both :class:`CMPath` and :class:`~pathlib.Path` are
            :class:`~pathlib.Path` subclasses and support all normal path
            operations (``read_bytes()``, ``open()``, etc.).
        """
        total_bytes = self.size if self.size and self.size > 0 else None

        def _stream_to(f):
            downloaded = 0
            for chunk in self.as_stream(chunk_size=chunk_size):
                f.write(chunk)
                if progress_callback is not None:
                    downloaded += len(chunk)
                    progress_callback(downloaded, total_bytes)

        if path is not None:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "wb") as f:
                _stream_to(f)
            return path
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        with temp_file as f:
            _stream_to(f)
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
    """A local filesystem file presented with the same interface as :class:`Artifact`.

    Returned by :meth:`~ivcap_client.ivcap.LocalIVCAP.get_artifact` and
    :meth:`~ivcap_client.ivcap.LocalIVCAP.upload_artifact` when running in local
    mode.  No network calls are made — the underlying file already exists on disk.

    The artifact ``id`` is a ``urn:file://<absolute-path>`` URN.  Key methods:

    * :meth:`open` — open the file for reading (text mode, UTF-8).
    * :meth:`as_local_file` — return the file's :class:`SafePath`; supports
      ``with`` statements but the file is **never deleted** on exit (it is a
      pre-existing local file, not a temp file).
    * :meth:`as_stream` — not implemented; raises :class:`NotImplementedError`.
      Use :meth:`open` or :meth:`as_local_file` instead.
    """

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
        """Open the local file for reading and return a file-like object.

        The file is opened in **text mode with UTF-8 encoding**.  If the
        artifact is a binary file (e.g. an image or model checkpoint) use
        :meth:`as_local_file` to get the :class:`~pathlib.Path` and open it
        yourself in binary mode::

            path = artifact.as_local_file()
            with open(path, "rb") as f:
                data = f.read()

        Returns:
            A text-mode file object for the local file.
        """
        return open(self._fp, encoding="utf-8")

    def as_local_file(self) -> Path:
        """Return a :class:`SafePath` to the existing local file.

        Unlike :meth:`Artifact.as_local_file`, no download is performed — the
        file already exists on disk.  The returned :class:`SafePath` supports
        use in a ``with`` statement, but **the file is never deleted on exit**
        (it is a pre-existing local source file, not a temporary download).

        Example::

            with artifact.as_local_file() as path:
                data = path.read_bytes()
            # file still exists — it was not a temp file

            # Or without the context manager:
            path = artifact.as_local_file()
            data = path.read_bytes()

        Returns:
            SafePath: A :class:`~pathlib.Path` subclass pointing to the local
            file.  ``unlink()`` is disabled to prevent accidental deletion.
        """
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


class LocalAspect:
    """A filesystem-backed aspect record returned by :class:`LocalIVCAP`.

    Provides the same key properties as :class:`~ivcap_client.aspect.Aspect`
    so that callers do not need to branch between local and platform mode.

    Instances are created by :meth:`LocalIVCAP.add_aspect` /
    :meth:`LocalIVCAP.update_aspect` and retrieved by
    :meth:`LocalIVCAP.get_aspect`.  On disk each aspect is a single JSON
    file stored under ``<base_dir>/aspects/<uuid>.json``.
    """

    def __init__(
        self,
        id: str,
        entity: str,
        schema: str,
        content: dict,
        *,
        valid_from: datetime | None = None,
    ):
        self.id = id
        self.entity = entity
        self.schema = schema
        self._content = content
        self.valid_from = valid_from
        self.valid_to = None

    @property
    def urn(self) -> str:
        """URN of this aspect record (``urn:ivcap:aspect:<uuid>``)."""
        return self.id

    @property
    def aspect(self) -> dict:
        """The JSON content body of the aspect."""
        return self._content

    @property
    def content(self) -> dict:
        """Alias for :attr:`aspect`."""
        return self._content

    def __repr__(self) -> str:
        return f"<LocalAspect id={self.id}, entity={self.entity}, schema={self.schema}>"


# ---------------------------------------------------------------------------
# Backward-compatibility re-export: LocalIVCAP has been moved to ivcap.py
# so that it can properly subclass IVCAP.  Imports such as
#   from ivcap_client.artifact import LocalIVCAP
# continue to work transparently via module __getattr__.
# ---------------------------------------------------------------------------


def __getattr__(name: str):
    if name == "LocalIVCAP":
        from ivcap_client.ivcap import LocalIVCAP  # noqa: PLC0415

        return LocalIVCAP
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


#### HELPER FUNCTIONS ####

_CHUNK_MIN = 8 * 1024  # 8 KiB
_CHUNK_MAX = 10 * 1024 * 1024  # 10 MiB


def _resolve_chunk_size(chunk_size: int, artifact_size: int | None) -> int:
    """Return an effective chunk size for streaming downloads.

    If *chunk_size* is ``-1`` (the sentinel "choose for me" value) the chunk
    size is derived from *artifact_size* using the formula::

        max(8 KiB, min(artifact_size / 10, 10 MiB))

    This keeps small artifacts in a small number of chunks while capping
    memory usage for large ones.  When *artifact_size* is ``None`` or
    non-positive the minimum (8 KiB) is used as a safe fallback.

    Any explicit positive *chunk_size* is returned unchanged.

    Args:
        chunk_size: Requested chunk size, or ``-1`` to auto-calculate.
        artifact_size: Known artifact size in bytes, or ``None`` if unknown.

    Returns:
        Resolved chunk size in bytes (always a positive integer).
    """
    if chunk_size != -1:
        return chunk_size
    if artifact_size and artifact_size > 0:
        return max(_CHUNK_MIN, min(artifact_size // 10, _CHUNK_MAX))
    return _CHUNK_MIN


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
    """Upload a file or byte stream to IVCAP as a new artifact.

    Either ``file_path`` or ``io_stream`` must be provided (not both).  When
    using ``io_stream``, ``content_type`` must be supplied explicitly.

    **Deduplication:** When ``file_path`` is given, the SDK stores a hidden
    ``.ivcap-<filename>.txt`` sidecar file next to the source file containing
    an MD5 hash.  On subsequent calls for the same unchanged file the existing
    artifact is returned immediately without re-uploading.  Override with
    ``force_upload=True``.

    Args:
        name (Optional[str]): Human-readable display name for the artifact.
        file_path (Optional[str]): Path to the local file to upload.
            The MIME type is auto-detected from the file extension if
            ``content_type`` is not given.
        io_stream (Optional[IO]): In-memory byte stream to upload.
            ``content_type`` must be provided when using this argument.
        content_type (Optional[str]): MIME type of the content.  Required
            when using ``io_stream``; auto-detected from ``file_path`` otherwise.
        content_size (Optional[int]): Size of the content in bytes.  Defaults
            to -1 (unknown); auto-determined from ``file_path`` when possible.
        collection (Optional[URN]): Add the artifact to a named collection
            (``urn:ivcap:collection:<uuid>``).
        policy (Optional[URN]): Access policy URN
            (``urn:ivcap:policy:<name>``).
        chunk_size (Optional[int]): TUS upload chunk size in bytes.
            Defaults to ``sys.maxsize`` (single-chunk upload).
        retries (Optional[int]): Number of retry attempts on upload failure.
            Defaults to 0 (no retries).
        retry_delay (Optional[int]): Seconds to wait between retries.
            Defaults to 30.
        force_upload (Optional[bool]): Re-upload even if a sidecar file
            indicates the file was already uploaded.  Defaults to False.

    Returns:
        Artifact: The newly created (or previously uploaded) artifact.

    Raises:
        ValueError: If neither ``file_path`` nor ``io_stream`` is provided,
            if the file does not exist or is not readable, or if
            ``content_type`` cannot be determined.
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
    """A :class:`~pathlib.Path` subclass that protects local source files.

    Returned by :meth:`LocalFileArtifact.as_local_file`.  Behaves like a
    normal :class:`~pathlib.Path` except:

    * ``unlink()`` is a no-op — prevents accidental deletion of the source
      file when caller code reuses the ``with artifact.as_local_file() as path:``
      pattern (which calls ``unlink()`` on a :class:`CMPath` for temp files).
    * Supports the context manager protocol (``with`` statement) — the
      ``__exit__`` is a no-op, so no cleanup is performed on exit.

    This means code written to work with :class:`CMPath` (platform artifacts)
    also works with :class:`SafePath` (local artifacts) without modification.
    """

    def unlink(self, missing_ok: bool = False):
        """No-op — prevents accidental deletion of the local source file."""
        return

    def __enter__(self) -> SafePath:
        """Return self for use in ``with`` statements."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """No-op — local source files are never deleted on context exit."""


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
