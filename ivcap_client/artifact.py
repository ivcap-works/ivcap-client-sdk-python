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
import queue
import re
import tarfile
import tempfile
import threading
import time
import uuid
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from sys import maxsize as MAXSIZE
from typing import IO, TYPE_CHECKING, BinaryIO
from urllib.parse import unquote_to_bytes, urlparse

import httpx
from tusclient.client import TusClient

from ivcap_client.api.artifact import artifact_list, artifact_read, artifact_upload
from ivcap_client.aspect import (  # noqa: F401 – re-exported for backward compat
    Aspect,
    LocalAspect,
)
from ivcap_client.exception import ArtifactTooLargeForDataUrlError, IvcapApiError
from ivcap_client.models.artifact_list_item import ArtifactListItem
from ivcap_client.models.artifact_list_rt import ArtifactListRT
from ivcap_client.models.artifact_status_rt import ArtifactStatusRT
from ivcap_client.models.artifact_status_rt_status import ArtifactStatusRTStatus
from ivcap_client.utils import BaseIter, Links, _set_fields, process_error

if TYPE_CHECKING:
    from typing import Self

    from ivcap_client.ivcap import IVCAP, URN


_CHUNK_MIN = 8 * 1024  # 8 KiB
_CHUNK_MAX = 16 * 1024 * 1024  # 16 MiB

# MIME types and filename suffixes that indicate a tar-based archive.
_TAR_MIME_TYPES: frozenset[str] = frozenset(
    {
        "application/x-tar",
        "application/gzip",
        "application/x-gzip",
        "application/x-bzip2",
        "application/x-xz",
        "application/x-compressed-tar",
        "application/x-gtar",
    }
)
_TAR_SUFFIXES: tuple[str, ...] = (
    ".tar",
    ".tgz",
    ".tar.gz",
    ".tar.bz2",
    ".tbz2",
    ".tar.xz",
)

logger = logging.getLogger(__name__)


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

    def as_data_url(self, max_length: int = 512) -> str:
        """Return this artifact's content as an RFC 2397 ``data:`` URL.

        The full artifact content is downloaded and base64-encoded into a
        ``data:<mime_type>;base64,<data>`` string — the inverse of
        :meth:`~ivcap_client.ivcap.IVCAP.get_artifact` accepting a ``data:``
        URL. This is convenient for embedding small artifacts inline (e.g. in
        a JSON payload or a service request) instead of passing an artifact
        URN.

        Because base64 encoding adds roughly 33% overhead on top of the raw
        content size (plus the ``data:<mime_type>;base64,`` header), this
        method is only intended for **small** artifacts. To avoid silently
        producing huge strings, the encoded URL's length is checked against
        ``max_length`` and a :class:`~ivcap_client.exception.ArtifactTooLargeForDataUrlError`
        is raised if it would be exceeded — no partial/truncated URL is ever
        returned.

        Args:
            max_length: Maximum allowed length, in characters, of the
                resulting ``data:`` URL. Defaults to 512.

        Returns:
            str: The ``data:<mime_type>;base64,<data>`` URL.

        Raises:
            ArtifactTooLargeForDataUrlError: If the artifact's known size (or,
                failing that, its actual encoded content) would produce a
                ``data:`` URL longer than ``max_length``.

        Example::

            artifact = ivcap.get_artifact("urn:ivcap:artifact:<uuid>")
            url = artifact.as_data_url(max_length=2048)
            # "data:image/png;base64,iVBORw0KGgo..."
        """
        # Fail fast without downloading if the known size already guarantees
        # the encoded URL will exceed max_length.
        if self.size and self.size > 0:
            header_len = len(f"data:{self.mime_type or 'application/octet-stream'};base64,")
            estimated_len = header_len + (-(-self.size * 4 // 3))  # ceil(size * 4/3)
            if estimated_len > max_length:
                raise ArtifactTooLargeForDataUrlError(
                    artifact_id=self.id,
                    content_size=self.size,
                    data_url_length=estimated_len,
                    max_length=max_length,
                )

        with self.open() as f:
            content = f.read()
        return _build_data_url(content, self.mime_type, self.id, max_length)

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
                ``max(8 KiB, min(artifact_size / 10, 16 MiB))``.  The artifact
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
        reuse_if_exists: bool = False,
        verify_if_exists: bool = True,
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
            reuse_if_exists: If ``True`` and ``path`` already exists, return it
                without downloading the artifact again.  Defaults to ``False``,
                which overwrites the existing file.
            verify_if_exists: Only used with ``reuse_if_exists``.  If ``True``
                (default), an existing file is reused only when its size matches
                the artifact size; otherwise it is downloaded again.  If the size
                is unknown, the file is downloaded again.  Set to ``False`` to
                reuse the file without any check.
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
            if reuse_if_exists and path.exists():
                if not verify_if_exists or path.stat().st_size == self.size:
                    return KeepFilePath(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "wb") as f:
                _stream_to(f)
            return KeepFilePath(path)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        with temp_file as f:
            _stream_to(f)
        return CMPath(temp_file.name)

    @property
    def is_tar_file(self) -> bool:
        """Return ``True`` if this artifact appears to be a tar archive.

        The check consults two sources of evidence in order:

        1. **MIME type** — if :attr:`mime_type` is one of the known tar-related
           types (``application/x-tar``, ``application/gzip``,
           ``application/x-bzip2``, etc.) the result is ``True``.
        2. **File name suffix** — if :attr:`name` ends with a recognised tar
           extension (``.tar``, ``.tgz``, ``.tar.gz``, ``.tar.bz2``,
           ``.tbz2``, ``.tar.xz``) the result is ``True``.

        If neither attribute is set, ``False`` is returned.

        Use this property to branch between :meth:`untar` and
        :meth:`as_local_file` without having to inspect MIME types yourself::

            if artifact.is_tar_file:
                artifact.untar("/tmp/results")
            else:
                artifact.as_local_file("/tmp/result.bin")
        """
        if self.mime_type and self.mime_type.lower() in _TAR_MIME_TYPES:
            return True
        if self.name:
            name_lower = self.name.lower()
            return any(name_lower.endswith(s) for s in _TAR_SUFFIXES)
        return False

    def untar(
        self,
        dest_dir: Path | str,
        *,
        chunk_size: int = -1,
        progress_callback: Callable[[int, int | None], None] | None = None,
    ) -> Path:
        """Stream a tar artifact and extract its files into a destination directory.

        The artifact must be a tar archive (``tar``, ``tar.gz``, ``tar.bz2``, etc.).
        Each file contained in the archive is written under ``dest_dir``,
        preserving the relative directory structure stored in the archive.
        Absolute paths in the archive (e.g. ``/etc/passwd``) are made relative
        to ``dest_dir`` by stripping the leading ``/``, so all extracted files
        always land inside ``dest_dir`` regardless of how the archive was created.

        The artifact is streamed directly through :meth:`as_stream` — neither the
        compressed archive nor its contents are ever fully buffered in memory.

        The resolved ``chunk_size`` is used as the buffer size at two independent
        layers:

        * **HTTP layer** — compressed bytes fetched per network read.
        * **Disk write layer** — decompressed bytes written per ``f_in.read()``
          call inside the tar loop.

        For compressed archives (``.tar.gz``, ``.tar.bz2``) these two layers are
        **decoupled** by tarfile's decompression stage, so a ``chunk_size``-byte
        compressed network chunk does not correspond to ``chunk_size`` bytes of
        decompressed output.  Both layers still benefit independently from a
        larger buffer (fewer syscalls).  An additional 8 KiB ``io.BufferedReader``
        sits between the network iterator and tarfile, further smoothing any
        size mismatch.

        The compression format is detected automatically from the stream header
        (``tarfile`` mode ``"r|*"``), so ``.tar``, ``.tar.gz``, and ``.tar.bz2``
        artifacts all work without any extra configuration.

        Args:
            dest_dir: Destination directory.  Created (including any missing
                parent directories) if it does not already exist.
            chunk_size (int): Buffer size in bytes used for both HTTP download
                chunks and per-member disk writes.  Pass ``-1`` (the default) to
                let the SDK choose automatically (see :meth:`as_stream` for the
                formula).  For compressed archives the two layers operate on
                different data domains (compressed vs decompressed bytes) and
                are therefore independent even when the same value is used.
            progress_callback: Optional callable invoked after each disk-write
                chunk is written.  Receives two arguments:

                * ``bytes_written`` (int) — cumulative uncompressed bytes written
                  so far across all extracted files.
                * ``total_bytes`` (int | None) — compressed artifact size in bytes,
                  or ``None`` if unknown.  This is a rough upper-bound indicator
                  only; actual extracted bytes will differ for compressed archives.

                Example::

                    def on_progress(written: int, total: int | None) -> None:
                        print(f"\\r{written:,} bytes extracted", end="", flush=True)

                    artifact.untar("/tmp/results", progress_callback=on_progress)

        Returns:
            :class:`~pathlib.Path`: The resolved ``dest_dir`` path.

        Raises:
            tarfile.TarError: If the artifact is not a valid tar archive.

        Example::

            dest = artifact.untar("/tmp/results")
            for p in sorted(dest.rglob("*")):
                print(p)
        """
        if not self.is_tar_file:
            raise ValueError(
                f"artifact {self.id!r} does not appear to be a tar archive "
                f"(mime_type={self.mime_type!r}, name={self.name!r}). "
                "Use as_local_file() to download it as a plain file, or "
                "check artifact.is_tar_file before calling untar()."
            )
        dest = Path(dest_dir)
        dest.mkdir(parents=True, exist_ok=True)
        total_bytes = self.size if self.size and self.size > 0 else None
        copy_size = _resolve_chunk_size(chunk_size, self.size)

        raw = _IterStream(self.as_stream(chunk_size=copy_size))
        buf = io.BufferedReader(raw)
        with tarfile.open(fileobj=buf, mode="r|*") as tar:
            return _untar_from_tarfile(
                tar, dest, copy_size, total_bytes, progress_callback
            )

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

    def __init__(self, id: str, *, mime_type: str | None = None):
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
        # When resolved from a platform artifact URN (see
        # LocalIVCAP.register_artifact / the `.ivcap-*.txt` sidecar scan) the
        # real, platform-recorded mime type may be known and should take
        # precedence over guessing from the filename extension.
        self._mime_type_override = mime_type

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

    def as_data_url(self, max_length: int = 512) -> str:
        """Return this local file's content as an RFC 2397 ``data:`` URL.

        See :meth:`Artifact.as_data_url` for full semantics. The file is read
        in binary mode (regardless of :meth:`open`'s text-mode behaviour) and
        base64-encoded into a ``data:<mime_type>;base64,<data>`` string.

        Args:
            max_length: Maximum allowed length, in characters, of the
                resulting ``data:`` URL. Defaults to 512.

        Returns:
            str: The ``data:<mime_type>;base64,<data>`` URL.

        Raises:
            ArtifactTooLargeForDataUrlError: If the resulting ``data:`` URL
                would be longer than ``max_length``.
        """
        header_len = len(f"data:{self.mime_type or 'application/octet-stream'};base64,")
        estimated_len = header_len + (-(-self.size * 4 // 3))  # ceil(size * 4/3)
        if estimated_len > max_length:
            raise ArtifactTooLargeForDataUrlError(
                artifact_id=self.id,
                content_size=self.size,
                data_url_length=estimated_len,
                max_length=max_length,
            )
        content = self._fp.read_bytes()
        return _build_data_url(content, self.mime_type, self.id, max_length)

    def as_local_file(
        self,
        path: Path | None = None,
        *,
        chunk_size: int = -1,
        progress_callback: Callable[[int, int | None], None] | None = None,
        reuse_if_exists: bool = False,
        verify_if_exists: bool = True,
    ) -> Path:
        """Return a :class:`SafePath` to the existing local file.

        Unlike :meth:`Artifact.as_local_file`, no download is performed — the
        file already exists on disk.  The ``path``, ``chunk_size``,
        ``progress_callback``, ``reuse_if_exists`` and ``verify_if_exists``
        arguments are accepted for interface compatibility and ignored, so the
        existing file is always returned as is.  The returned :class:`SafePath` supports
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
        return ArtifactStatusRT(
            id=self.id, links=[], status=ArtifactStatusRTStatus.READY
        )

    @property
    def etag(self) -> str:
        return md5sum(f"{self.name}-{self.last_modified_at.timestamp()}")

    @property
    def mime_type(self) -> str:
        if self._mime_type_override:
            return self._mime_type_override
        mime_type, _ = mimetypes.guess_type(self._fp.name)
        # Fallback if mimetypes can't guess from the extension
        if not mime_type:
            mime_type = "application/octet-stream"
        return mime_type

    @property
    def is_tar_file(self) -> bool:
        """Return ``True`` if this local file appears to be a tar archive.

        Uses the same MIME-type and suffix detection as :attr:`Artifact.is_tar_file`.
        Because the file is local, the MIME type is inferred from the filename
        extension via :func:`mimetypes.guess_type`.
        """
        if self.mime_type and self.mime_type.lower() in _TAR_MIME_TYPES:
            return True
        name_lower = self._fp.name.lower()
        return any(name_lower.endswith(s) for s in _TAR_SUFFIXES)

    def untar(
        self,
        dest_dir: Path | str,
        *,
        chunk_size: int = -1,
        progress_callback: Callable[[int, int | None], None] | None = None,
    ) -> Path:
        """Extract the files inside this local tar archive into a destination directory.

        The archive file already exists on the local filesystem — no download is
        performed.  The extraction logic is identical to :meth:`Artifact.untar`:
        files are written under ``dest_dir`` preserving relative directory
        structure, and absolute archive paths are made relative to ``dest_dir``
        by stripping the leading ``/``.

        Args:
            dest_dir: Destination directory.  Created (including any missing
                parent directories) if it does not already exist.
            chunk_size (int): Bytes read per ``f_in.read()`` call when copying
                each member to disk.  Pass ``-1`` (the default) to let the SDK
                choose automatically based on the archive file size.
            progress_callback: Optional ``(bytes_written, total_bytes)`` callable
                invoked after each chunk is written.  ``total_bytes`` is the
                compressed archive file size and serves as a rough progress indicator
                only.

        Returns:
            :class:`~pathlib.Path`: The resolved ``dest_dir`` path.

        Raises:
            ValueError: If :attr:`is_tar_file` is ``False``.
            tarfile.TarError: If the file is not a valid tar archive.

        Example::

            artifact = ivcap.get_artifact("file:///data/results.tar.gz")
            dest = artifact.untar("/tmp/results")
        """
        if not self.is_tar_file:
            raise ValueError(
                f"local file {str(self._fp)!r} does not appear to be a tar archive "
                f"(mime_type={self.mime_type!r}). "
                "Check artifact.is_tar_file before calling untar()."
            )
        dest = Path(dest_dir)
        dest.mkdir(parents=True, exist_ok=True)
        total_bytes = self.size if self.size and self.size > 0 else None
        copy_size = _resolve_chunk_size(chunk_size, self.size)

        with tarfile.open(self._fp, mode="r:*") as tar:
            return _untar_from_tarfile(
                tar, dest, copy_size, total_bytes, progress_callback
            )

    def __repr__(self) -> str:
        return f"<LocalFileArtifact id={self.id}>"


# Matches the RFC 2397 'data:' URL scheme:
#   data:[<mediatype>][;base64],<data>
_DATA_URL_RE = re.compile(r"^data:([^,]*),(.*)$", re.DOTALL)


def is_data_url(id: str) -> bool:
    """Return ``True`` if *id* looks like an RFC 2397 ``data:`` URL.

    In addition to the plain ``data:`` form, the ``urn:data:`` form is also
    recognised for consistency with other IVCAP URN schemes (e.g.
    ``urn:file://...``), allowing a ``data:`` payload to be embedded as a
    proper URN where required.

    Args:
        id: Candidate artifact identifier/URN.

    Returns:
        ``True`` if *id* starts with ``"data:"`` or ``"urn:data:"``, ``False``
        otherwise.
    """
    return isinstance(id, str) and (
        id.startswith("data:") or id.startswith("urn:data:")
    )


def _strip_urn_prefix(data_url: str) -> str:
    """Normalise a ``urn:data:...`` identifier to a plain ``data:...`` URL."""
    if data_url.startswith("urn:data:"):
        return data_url[len("urn:") :]
    return data_url


def _parse_data_url(data_url: str) -> tuple[str, str | None, bytes]:
    """Parse an RFC 2397 ``data:`` URL (optionally ``urn:data:``-prefixed)
    into ``(mime_type, charset, content)``.

    Args:
        data_url: A string of the form ``data:[<mediatype>][;base64],<data>``,
            optionally prefixed with ``urn:`` (i.e. ``urn:data:...``).

    Returns:
        A tuple of ``mime_type`` (defaulting to ``"text/plain"`` if omitted),
        ``charset`` (or ``None``), and the decoded payload ``content`` bytes.

    Raises:
        ValueError: If *data_url* is not a well-formed ``data:`` URL.
    """
    m = _DATA_URL_RE.match(_strip_urn_prefix(data_url))
    if not m:
        raise ValueError(f"'{data_url[:40]}...' is not a well-formed data URL")
    header, payload = m.group(1), m.group(2)

    parts = [p for p in header.split(";")] if header else []
    is_base64 = any(p.strip() == "base64" for p in parts)
    non_flag_parts = [p for p in parts if p.strip() != "base64"]

    mime_type = "text/plain"
    charset: str | None = None
    if non_flag_parts and "/" in non_flag_parts[0]:
        mime_type = non_flag_parts[0].strip()
        param_parts = non_flag_parts[1:]
    else:
        param_parts = non_flag_parts

    for p in param_parts:
        if "=" in p:
            k, v = p.split("=", 1)
            if k.strip().lower() == "charset":
                charset = v.strip()

    if is_base64:
        # Data URLs are sometimes percent-encoded even in base64 form
        # (e.g. embedded newlines encoded as '%0A'); normalise first.
        cleaned = unquote_to_bytes(payload).decode("ascii")
        cleaned += "=" * (-len(cleaned) % 4)  # tolerate missing padding
        content = base64.b64decode(cleaned)
    else:
        content = unquote_to_bytes(payload)

    return mime_type, charset, content


class DataUrlArtifact:
    """An in-memory artifact backed by an RFC 2397 ``data:`` URL.

    Returned by :meth:`~ivcap_client.ivcap.IVCAP.get_artifact` (and
    :meth:`~ivcap_client.ivcap.LocalIVCAP.get_artifact`) when the supplied
    ``id`` is a ``data:`` URL (e.g. ``"data:image/png;base64,iVBORw0KGgo..."``)
    rather than an ``urn:ivcap:artifact:<uuid>`` or ``file://`` URN. The
    ``urn:data:...`` form (e.g. ``"urn:data:image/png;base64,iVBORw0KGgo..."``)
    is also accepted, for consistency with other IVCAP URN schemes — both
    forms are handled identically and ``.id``/``.urn`` preserve whichever
    form was originally passed in.

    The URL is parsed once at construction time into an internal in-memory
    byte buffer, after which :meth:`open`, :meth:`as_stream`,
    :meth:`as_local_file`, and :meth:`untar` all behave exactly as if the
    content had been downloaded from the platform — no network calls are
    ever made.

    Example::

        artifact = ivcap.get_artifact("data:text/plain;base64,SGVsbG8h")
        with artifact.open() as f:
            print(f.read())  # b"Hello!"

        with artifact.as_local_file() as path:
            data = path.read_bytes()
    """

    def __init__(self, data_url: str):
        mime_type, charset, content = _parse_data_url(data_url)
        self.id = data_url
        self._content = content
        self.mime_type = mime_type
        self._charset = charset
        self.size = len(content)
        now = datetime.now()
        self.created_at = now
        self.last_modified_at = now

        ext = mimetypes.guess_extension(mime_type) or ""
        self.name = f"{uuid.uuid4()}{ext}"

    @property
    def urn(self) -> str:
        return self.id

    def refresh(self) -> DataUrlArtifact:
        return self

    @property
    def status(self, refresh=True) -> ArtifactStatusRT:
        return ArtifactStatusRT(
            id=self.id, links=[], status=ArtifactStatusRTStatus.READY
        )

    def as_data_url(self, max_length: int = 512) -> str:
        """Return this artifact's content as an RFC 2397 ``data:`` URL.

        Since a :class:`DataUrlArtifact` is already backed by an in-memory
        ``data:``/``urn:data:`` URL, this simply re-validates and re-encodes
        the already-decoded content against ``max_length`` — no download is
        performed. The returned URL always uses the canonical ``data:`` form
        (without the ``urn:`` prefix), regardless of which form was used to
        construct this artifact.

        Args:
            max_length: Maximum allowed length, in characters, of the
                resulting ``data:`` URL. Defaults to 512.

        Returns:
            str: The ``data:<mime_type>;base64,<data>`` URL.

        Raises:
            ArtifactTooLargeForDataUrlError: If the resulting ``data:`` URL
                would be longer than ``max_length``.
        """
        return _build_data_url(self._content, self.mime_type, self.id, max_length)

    @property
    def etag(self) -> str:
        return hashlib.md5(self._content).hexdigest()

    @property
    def is_tar_file(self) -> bool:
        """Return ``True`` if this data URL's content appears to be a tar archive."""
        if self.mime_type and self.mime_type.lower() in _TAR_MIME_TYPES:
            return True
        name_lower = self.name.lower()
        return any(name_lower.endswith(s) for s in _TAR_SUFFIXES)

    def open(self) -> io.IOBase:
        """Return a file-like object over the decoded in-memory content.

        Returns:
            ProxyFile: A readable, seekable, context-manager-compatible
            file-like object wrapping the decoded bytes.
        """
        return ProxyFile(io.BytesIO(self._content))

    def as_stream(self, chunk_size: int = -1) -> Iterator[bytes]:
        """Yield the decoded content as a sequence of ``bytes`` chunks.

        Args:
            chunk_size: Number of bytes per chunk.  Pass ``-1`` (the default)
                to let the SDK choose automatically based on content size.

        Yields:
            bytes: The next chunk of decoded content.
        """
        copy_size = _resolve_chunk_size(chunk_size, self.size)
        buf = self._content
        if not buf:
            yield b""
            return
        for i in range(0, len(buf), copy_size):
            yield buf[i : i + copy_size]

    def as_local_file(
        self,
        path: Path | None = None,
        *,
        chunk_size: int = -1,
        progress_callback: Callable[[int, int | None], None] | None = None,
        reuse_if_exists: bool = False,
        verify_if_exists: bool = True,
    ) -> Path:
        """Write the decoded content to a local file and return the path.

        Mirrors :meth:`Artifact.as_local_file` — if ``path`` is omitted a
        self-deleting temporary file (:class:`CMPath`) is returned; otherwise
        the content is written to the given path (parent directories are
        created automatically) and a plain :class:`~pathlib.Path` is returned.

        Args:
            path: Destination file path, or ``None`` for a temp file.
            chunk_size: Bytes written per call.  ``-1`` auto-selects.
            progress_callback: Optional ``(bytes_written, total_bytes)``
                callable invoked after each chunk is written.
            reuse_if_exists: If ``True`` and ``path`` already exists, return it
                without rewriting the content.  Defaults to ``False``.
            verify_if_exists: Only used with ``reuse_if_exists``.  If ``True``
                (default), an existing file is reused only when its size matches
                the content size; otherwise it is rewritten.  Set to ``False`` to
                reuse the file without any check.

        Returns:
            :class:`CMPath` (temp file) or plain :class:`~pathlib.Path`.
        """
        total_bytes = self.size

        def _stream_to(f):
            written = 0
            for chunk in self.as_stream(chunk_size=chunk_size):
                f.write(chunk)
                if progress_callback is not None:
                    written += len(chunk)
                    progress_callback(written, total_bytes)

        if path is not None:
            path = Path(path)
            if reuse_if_exists and path.exists():
                if not verify_if_exists or path.stat().st_size == self.size:
                    return KeepFilePath(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "wb") as f:
                _stream_to(f)
            return KeepFilePath(path)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        with temp_file as f:
            _stream_to(f)
        return CMPath(temp_file.name)

    def untar(
        self,
        dest_dir: Path | str,
        *,
        chunk_size: int = -1,
        progress_callback: Callable[[int, int | None], None] | None = None,
    ) -> Path:
        """Extract the files inside this data URL's tar content into *dest_dir*.

        Args:
            dest_dir: Destination directory (created if missing).
            chunk_size: Bytes read per disk-write call. ``-1`` auto-selects.
            progress_callback: Optional ``(bytes_written, total_bytes)``
                callable invoked after each chunk is written.

        Returns:
            :class:`~pathlib.Path`: The resolved ``dest_dir`` path.

        Raises:
            ValueError: If :attr:`is_tar_file` is ``False``.
            tarfile.TarError: If the content is not a valid tar archive.
        """
        if not self.is_tar_file:
            raise ValueError(
                f"data URL artifact (mime_type={self.mime_type!r}) does not "
                "appear to be a tar archive. "
                "Check artifact.is_tar_file before calling untar()."
            )
        dest = Path(dest_dir)
        dest.mkdir(parents=True, exist_ok=True)
        total_bytes = self.size if self.size > 0 else None
        copy_size = _resolve_chunk_size(chunk_size, self.size)

        with tarfile.open(fileobj=io.BytesIO(self._content), mode="r:*") as tar:
            return _untar_from_tarfile(
                tar, dest, copy_size, total_bytes, progress_callback
            )

    def __repr__(self) -> str:
        return f"<DataUrlArtifact mime_type={self.mime_type}, size={self.size}>"


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


class _IterStream(io.RawIOBase):
    """Wrap a ``bytes`` iterator as a readable :class:`io.RawIOBase` stream.

    Used by :meth:`Artifact.untar` to feed :func:`tarfile.open` directly from
    :meth:`Artifact.as_stream` without buffering the entire download in memory.
    """

    def __init__(self, iterator: Iterator[bytes]):
        self._iter = iterator
        self._leftover = b""

    def readable(self) -> bool:
        return True

    def readinto(self, b: bytearray) -> int:
        try:
            while not self._leftover:
                self._leftover = next(self._iter)
        except StopIteration:
            return 0
        n = min(len(self._leftover), len(b))
        b[:n] = self._leftover[:n]
        self._leftover = self._leftover[n:]
        return n


def _untar_from_tarfile(
    tar: tarfile.TarFile,
    dest: Path,
    copy_size: int,
    total_bytes: int | None,
    progress_callback: Callable[[int, int | None], None] | None,
) -> Path:
    """Extract all file members from an open :class:`tarfile.TarFile` into *dest*.

    Shared implementation used by both :meth:`Artifact.untar` (HTTP streaming
    source) and :meth:`LocalFileArtifact.untar` (local file source).  The caller
    is responsible for opening/closing *tar* and creating *dest*.

    Absolute member paths are made safe by stripping the leading ``/`` before
    joining with *dest* (prevents path traversal outside the destination).

    Args:
        tar: An already-open :class:`tarfile.TarFile` in any read mode.
        dest: Destination directory (must already exist).
        copy_size: Bytes to read per ``f_in.read()`` call.
        total_bytes: Value forwarded as the second argument of *progress_callback*
            (may be ``None`` if the size is unknown).
        progress_callback: Optional ``(bytes_written, total_bytes)`` callable
            invoked after each chunk is written to disk.

    Returns:
        *dest* (unchanged).
    """
    written = 0
    for member in tar:
        if not member.isfile():
            continue
        f_in = tar.extractfile(member)
        if f_in is None:
            continue
        # Strip leading "/" so absolute archive paths are always
        # relative to dest (prevents path traversal outside dest).
        safe_name = member.name.lstrip("/")
        out_path = dest / safe_name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f_out:
            while True:
                chunk = f_in.read(copy_size)
                if not chunk:
                    break
                f_out.write(chunk)
                if progress_callback is not None:
                    written += len(chunk)
                    progress_callback(written, total_bytes)
    return dest


def _resolve_chunk_size(chunk_size: int, artifact_size: int | None) -> int:
    """Return an effective chunk size for streaming downloads.

    If *chunk_size* is ``-1`` (the sentinel "choose for me" value) the chunk
    size is derived from *artifact_size* using the formula::

        max(8 KiB, min(artifact_size / 10, 16 MiB))

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


def _build_data_url(
    content: bytes,
    mime_type: str | None,
    artifact_id: str,
    max_length: int,
) -> str:
    """Encode *content* as an RFC 2397 ``data:`` URL, enforcing *max_length*.

    Args:
        content: Raw artifact bytes to encode.
        mime_type: MIME type to embed in the URL header (falls back to
            ``"application/octet-stream"`` if ``None``/empty).
        artifact_id: Identifier used in the raised exception's message.
        max_length: Maximum allowed length (in characters) of the resulting
            ``data:`` URL.

    Returns:
        The ``data:<mime_type>;base64,<data>`` URL string.

    Raises:
        ArtifactTooLargeForDataUrlError: If the resulting URL would be longer
            than *max_length*.
    """
    mt = mime_type or "application/octet-stream"
    encoded = base64.b64encode(content).decode("ascii")
    data_url = f"data:{mt};base64,{encoded}"
    if len(data_url) > max_length:
        raise ArtifactTooLargeForDataUrlError(
            artifact_id=artifact_id,
            content_size=len(content),
            data_url_length=len(data_url),
            max_length=max_length,
        )
    return data_url


# ---------------------------------------------------------------------------
# Streaming tar-archive creation with chunked TUS upload
#
# Builds a gzip-compressed tar archive on the fly from local files and/or
# in-memory byte buffers, and streams it to the server as a single resumable
# TUS upload — without ever materializing the full archive on disk or in
# memory.  See the module-level design notes in the class/function
# docstrings below for the producer/consumer architecture.
# ---------------------------------------------------------------------------

_DEFAULT_TAR_UPLOAD_CHUNK_SIZE = 4 * 1024 * 1024  # 4 MiB
_DEFAULT_TAR_QUEUE_MAXSIZE = 4  # bounded queue items for backpressure


@dataclass
class TarMember:
    """A single entry to add to a streamed tar archive.

    Exactly one of ``file_path`` or ``data`` must be provided:

    * ``file_path`` — a local file read and streamed straight from disk.
    * ``data`` — an in-memory ``bytes`` buffer (e.g. a dynamically generated
      report, a serialized object, …), never written to disk.

    Use the :meth:`from_file` / :meth:`from_bytes` convenience constructors
    rather than calling the constructor directly.
    """

    arcname: str
    file_path: str | None = None
    data: bytes | None = None
    mtime: float | None = None
    mode: int | None = None

    def __post_init__(self):
        if (self.file_path is None) == (self.data is None):
            raise ValueError(
                "TarMember requires exactly one of 'file_path' or 'data'"
            )

    @classmethod
    def from_file(cls, file_path: str, arcname: str | None = None) -> TarMember:
        """Create a member backed by a local file on disk.

        Args:
            file_path: Path to the local file to include.
            arcname: Name of the entry inside the archive. Defaults to the
                file's basename.

        Returns:
            TarMember: A file-backed tar member.
        """
        return cls(arcname=arcname or os.path.basename(file_path), file_path=file_path)

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
        arcname: str,
        *,
        mtime: float | None = None,
        mode: int | None = None,
    ) -> TarMember:
        """Create a member backed by an in-memory byte buffer.

        Args:
            data: Raw bytes to embed as the entry's content.
            arcname: Name of the entry inside the archive.
            mtime: Optional modification time (seconds since epoch) recorded
                in the tar header. Defaults to the time the entry is written.
            mode: Optional Unix file mode recorded in the tar header.

        Returns:
            TarMember: An in-memory tar member.
        """
        return cls(arcname=arcname, data=data, mtime=mtime, mode=mode)


class _TarUploadCancelled(Exception):
    """Internal signal used to abort the tar-producer thread early when the
    upload consumer has given up (e.g. retries exhausted)."""


class _QueueWriter(io.RawIOBase):
    """A write-only file-like object that pushes written bytes onto a queue.

    Used as the ``fileobj`` for ``tarfile.open(mode="w|gz", fileobj=...)`` so
    that the tar+gzip stream is produced incrementally, one small ``write()``
    call at a time, without ever being buffered in full.

    :meth:`close` enqueues a ``None`` sentinel so the consumer thread knows no
    more data is coming.  If ``cancel_event`` is set, :meth:`write` raises
    :class:`_TarUploadCancelled` to unwind ``tarfile``'s write loop promptly.
    """

    def __init__(self, q: queue.Queue, cancel_event: threading.Event):
        super().__init__()
        self._q = q
        self._cancel_event = cancel_event

    def writable(self) -> bool:
        return True

    def write(self, data) -> int:
        b = bytes(data)
        if b:
            # Loop with a timeout (rather than a plain blocking put) so a
            # cancellation can be observed even while the queue is full and
            # the consumer has stopped pulling from it.
            while True:
                if self._cancel_event.is_set():
                    raise _TarUploadCancelled("tar upload was cancelled")
                try:
                    self._q.put(b, timeout=0.5)
                    break
                except queue.Full:
                    continue
        return len(b)

    def close(self):
        if not self.closed:
            self._q.put(None)  # sentinel: no more data
        super().close()


def _tar_stream_producer(
    members: Iterable[TarMember],
    q: queue.Queue,
    cancel_event: threading.Event,
    error_box: list,
) -> None:
    """Archive producer (runs in a background thread).

    Streams a gzip-compressed tar archive built from *members* into *q*, one
    chunk at a time, via :class:`_QueueWriter`.  Never materializes the full
    archive on disk or in memory — each member is read/streamed individually.

    Any exception raised while building the archive (missing file, I/O
    error, …) is captured into ``error_box[0]`` (a 1-element list used as a
    simple thread-safe box) rather than raised here, so the consumer thread
    can observe and re-raise it after fully draining the queue.
    """
    writer = _QueueWriter(q, cancel_event)
    try:
        with tarfile.open(fileobj=writer, mode="w|gz") as tar:
            for member in members:
                if cancel_event.is_set():
                    raise _TarUploadCancelled("tar upload was cancelled")
                if member.file_path is not None:
                    tar.add(member.file_path, arcname=member.arcname)
                else:
                    info = tarfile.TarInfo(name=member.arcname)
                    info.size = len(member.data)
                    info.mtime = (
                        member.mtime if member.mtime is not None else time.time()
                    )
                    if member.mode is not None:
                        info.mode = member.mode
                    tar.addfile(info, io.BytesIO(member.data))
    except _TarUploadCancelled:
        pass  # consumer already failed/cancelled; nothing further to report
    except BaseException as e:  # noqa: BLE001 – surfaced to the consumer thread
        error_box.append(e)
    finally:
        writer.close()


def _tus_create_deferred_upload(
    client: httpx.Client,
    creation_url: str,
    headers: dict[str, str],
) -> str:
    """POST to the TUS creation endpoint with ``Upload-Defer-Length: 1``.

    The final (compressed) size is not known upfront, so the standard
    ``Upload-Length`` header is replaced with the TUS creation-defer-length
    extension. Returns the absolute upload URL from the ``Location`` header.

    Raises:
        IvcapApiError: If the server does not return a ``Location`` header.
    """
    h = dict(headers)
    h["Upload-Defer-Length"] = "1"
    h["Tus-Resumable"] = "1.0.0"
    r = client.post(creation_url, headers=h)
    if r.status_code >= 300:
        raise IvcapApiError(
            "upload_tar_artifact.create",
            r.status_code,
            content=r.content,
            url=str(r.request.url) if r.request else None,
        )
    location = r.headers.get("location")
    if not location:
        raise IvcapApiError(
            "upload_tar_artifact.create",
            r.status_code,
            content="TUS creation response missing 'Location' header",
            url=str(r.request.url) if r.request else None,
        )
    if location.startswith("http"):
        return location
    base = urlparse(creation_url)
    return base._replace(path=urlparse(location).path).geturl()


def _tus_head_offset(client: httpx.Client, upload_url: str) -> int:
    """Return the server's authoritative ``Upload-Offset`` via ``HEAD``."""
    r = client.head(upload_url, headers={"Tus-Resumable": "1.0.0"})
    if r.status_code >= 300:
        raise IvcapApiError(
            "upload_tar_artifact.head",
            r.status_code,
            content=r.content,
            url=str(r.request.url) if r.request else None,
        )
    offset = r.headers.get("upload-offset")
    if offset is None:
        raise IvcapApiError(
            "upload_tar_artifact.head",
            r.status_code,
            content="TUS HEAD response missing 'Upload-Offset' header",
            url=str(r.request.url) if r.request else None,
        )
    return int(offset)


def _tus_patch_chunk(
    client: httpx.Client,
    upload_url: str,
    chunk: bytes,
    offset: int,
    *,
    final: bool,
    total_length: int | None,
) -> int:
    """PATCH a single chunk at *offset*; return the server's new offset.

    Args:
        final: Whether this is the last chunk of the upload.
        total_length: Total upload size — included as ``Upload-Length`` only
            when ``final`` is True (completes the deferred-length upload).
    """
    headers = {
        "Content-Type": "application/offset+octet-stream",
        "Upload-Offset": str(offset),
        "Tus-Resumable": "1.0.0",
    }
    if final and total_length is not None:
        headers["Upload-Length"] = str(total_length)
    r = client.patch(upload_url, content=chunk, headers=headers)
    if r.status_code >= 300:
        raise IvcapApiError(
            "upload_tar_artifact.patch",
            r.status_code,
            content=r.content,
            url=str(r.request.url) if r.request else None,
        )
    new_offset = r.headers.get("upload-offset")
    return int(new_offset) if new_offset is not None else offset + len(chunk)


def _tus_patch_with_retry(
    client: httpx.Client,
    upload_url: str,
    chunk: bytes,
    offset: int,
    *,
    final: bool,
    total_length: int | None,
    retries: int,
    retry_delay: float,
) -> int:
    """PATCH *chunk* at *offset*, retrying with exponential backoff.

    On failure, re-synchronises with the server's authoritative offset via
    ``HEAD`` before each retry (the server may have received part or all of
    the previous attempt even though the client saw an error), and re-slices
    the pending chunk accordingly rather than assuming full success/failure.
    """
    attempt = 0
    pending = chunk
    pending_offset = offset
    while True:
        try:
            return _tus_patch_chunk(
                client,
                upload_url,
                pending,
                pending_offset,
                final=final,
                total_length=total_length,
            )
        except (IvcapApiError, httpx.HTTPError) as e:
            if attempt >= retries:
                raise
            attempt += 1
            time.sleep(retry_delay * (2 ** (attempt - 1)))
            try:
                server_offset = _tus_head_offset(client, upload_url)
            except (IvcapApiError, httpx.HTTPError):
                continue  # try the PATCH again with our last-known offset
            advanced = server_offset - offset
            if advanced < 0 or advanced > len(chunk):
                # Server offset is inconsistent with what we sent; give up
                # rather than silently corrupting the upload.
                raise e
            pending = chunk[advanced:]
            pending_offset = server_offset


def _drain_queue_into_buffer(
    q: queue.Queue, buffer: bytearray, target_size: int
) -> bool:
    """Pull items from *q* into *buffer* until either *target_size* bytes have
    accumulated or the sentinel (``None``) is reached.

    Returns:
        bool: ``True`` if the sentinel was consumed (no more data is coming),
        ``False`` if the buffer simply reached ``target_size``.
    """
    while len(buffer) < target_size:
        item = q.get()
        if item is None:
            return True
        buffer.extend(item)
    return False


def _stream_tar_members_to_tus(
    client: httpx.Client,
    upload_url: str,
    members: Iterable[TarMember],
    *,
    chunk_size: int,
    queue_maxsize: int,
    retries: int,
    retry_delay: float,
) -> None:
    """Drive the producer thread + chunked-upload consumer loop.

    Starts :func:`_tar_stream_producer` in a background thread, then drains
    its output queue in this (the calling) thread, PATCHing upload-sized
    chunks to *upload_url* until the producer's sentinel is reached and the
    final chunk (with ``Upload-Length`` set) has been sent.

    If the chunk loop raises, the producer thread is signalled to cancel via
    a shared :class:`threading.Event` and joined before re-raising, so no
    background thread is ever left running past this function's return.
    """
    q: queue.Queue = queue.Queue(maxsize=queue_maxsize)
    cancel_event = threading.Event()
    error_box: list = []
    producer = threading.Thread(
        target=_tar_stream_producer,
        args=(members, q, cancel_event, error_box),
        daemon=True,
    )
    producer.start()

    offset = 0
    buffer = bytearray()
    try:
        while True:
            finished = _drain_queue_into_buffer(q, buffer, chunk_size)
            if not finished:
                to_send = bytes(buffer[:chunk_size])
                del buffer[:chunk_size]
                offset = _tus_patch_with_retry(
                    client,
                    upload_url,
                    to_send,
                    offset,
                    final=False,
                    total_length=None,
                    retries=retries,
                    retry_delay=retry_delay,
                )
            else:
                # Sentinel reached: send the remainder (possibly empty) as
                # the final chunk, completing the deferred-length upload.
                to_send = bytes(buffer)
                total_length = offset + len(to_send)
                offset = _tus_patch_with_retry(
                    client,
                    upload_url,
                    to_send,
                    offset,
                    final=True,
                    total_length=total_length,
                    retries=retries,
                    retry_delay=retry_delay,
                )
                break
    except BaseException:
        cancel_event.set()
        raise
    finally:
        producer.join()

    if error_box:
        raise error_box[0]


def upload_tar_artifact(
    ivcap: IVCAP,
    members: Iterable[TarMember],
    *,
    content_type: str = "application/gzip",
    name: str | None = None,
    collection: URN | None = None,
    policy: URN | None = None,
    chunk_size: int = _DEFAULT_TAR_UPLOAD_CHUNK_SIZE,
    queue_maxsize: int = _DEFAULT_TAR_QUEUE_MAXSIZE,
    retries: int = 3,
    retry_delay: float = 2.0,
) -> Artifact:
    """Build a gzip-compressed tar archive from *members* and upload it via a
    single chunked, resumable TUS upload — without ever materializing the
    full archive on disk or in memory.

    See the module design notes above :class:`TarMember` for the full
    producer/consumer architecture. In short:

    1. A background thread streams ``tarfile`` (``mode="w|gz"``) output into
       a bounded :class:`queue.Queue`, one small ``write()`` at a time
       (:func:`_tar_stream_producer`). The bounded queue provides
       backpressure so archive generation cannot run arbitrarily far ahead
       of the network.
    2. This thread (the upload consumer) drains the queue, accumulates
       upload-sized chunks, and ``PATCH``es them to a TUS endpoint created
       with the creation-defer-length extension (final size unknown
       upfront). Each chunk is retried with exponential backoff, re-
       synchronising via ``HEAD`` on failure.
    3. Once the tar producer's sentinel is reached, the final chunk is sent
       together with the now-known ``Upload-Length``, completing the upload.

    Args:
        ivcap: The owning :class:`IVCAP` instance.
        members: Iterable of :class:`TarMember` entries to add to the
            archive, in order. Each is either a local file (streamed
            straight from disk) or an in-memory ``bytes`` buffer.
        content_type: MIME type recorded for the resulting artifact.
            Defaults to ``"application/gzip"``.
        name: Optional human-readable artifact name.
        collection: Optional collection URN to add the artifact to.
        policy: Optional access policy URN.
        chunk_size: Upload chunk size in bytes. Defaults to 4 MiB.
        queue_maxsize: Max number of pending chunks buffered between the
            producer and consumer threads (backpressure bound).
        retries: Number of retry attempts per chunk on failure.
        retry_delay: Base delay (seconds) between retries; doubles after
            each attempt (exponential backoff).

    Returns:
        Artifact: The newly created artifact.

    Raises:
        ValueError: If ``collection``/``policy`` are not well-formed URNs.
        IvcapApiError: If artifact creation or any upload request fails
            after exhausting retries.
        Exception: Any exception raised while reading a member's content
            (e.g. a missing local file) is re-raised here, after the queue
            has been fully drained and the producer thread has stopped.

    Example::

        from ivcap_client.artifact import TarMember

        members = [
            TarMember.from_file("/data/image1.jpg"),
            TarMember.from_file("/data/image2.jpg", arcname="renamed.jpg"),
            TarMember.from_bytes(b"{...}", arcname="metadata.json"),
        ]
        artifact = ivcap.upload_tar_artifact(members, name="dataset.tar.gz")
    """
    if collection and not collection.startswith("urn:"):
        raise ValueError(f"collection '{collection}' is not a URN.")
    if policy and not policy.startswith("urn:ivcap:policy:"):
        raise ValueError(f"policy '{policy}' is not a policy URN.")

    # Step 1: create the (initially empty) artifact record with a deferred
    # content length — the compressed size is not known upfront.
    kwargs = {
        "x_content_type": content_type,
        "x_content_length": -1,
        "tus_resumable": "1.0.0",
    }
    if name:
        kwargs["x_name"] = base64.b64encode(bytes(name, "utf-8"))
    if collection:
        kwargs["x_collection"] = collection
    if policy:
        kwargs["x_policy"] = policy

    r = artifact_upload.sync_detailed(client=ivcap._client, **kwargs)
    if r.status_code >= 300:
        return process_error("upload_tar_artifact", r)
    res: ArtifactStatusRT = r.parsed

    headers = {}
    if ivcap._token:
        headers["Authorization"] = f"Bearer {ivcap._token}"
    data_url = ivcap._url + fix_data_ref(res.data_href)

    # Reuse the IVCAP instance's own httpx.Client (same base_url, auth
    # headers, and — in tests — the same mock transport) rather than
    # spinning up a brand-new one that would try to hit the real network.
    client = ivcap._client.get_httpx_client()
    upload_url = _tus_create_deferred_upload(client, data_url, headers)
    _stream_tar_members_to_tus(
        client,
        upload_url,
        members,
        chunk_size=chunk_size,
        queue_maxsize=queue_maxsize,
        retries=retries,
        retry_delay=retry_delay,
    )

    kwargs = res.to_dict()
    kwargs["status"] = None
    a = Artifact(ivcap, **kwargs)
    a.status  # force status update as it will have changed
    return a


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
        mark_file_already_uploaded(res.id, file_path, mime_type=content_type)
    kwargs["status"] = None
    a = Artifact(ivcap, **kwargs)
    a.status  # force status update as it will have change
    return a


def check_file_already_uploaded(file_path: str) -> str | None:
    aid, _mime_type = _read_upload_marker(file_path)
    return aid


def _read_upload_marker(file_path: str) -> tuple[str | None, str | None]:
    """Read the ``.ivcap-<filename>.txt`` sidecar for ``file_path``, if any.

    The sidecar format is ``<md5>|<artifact-urn>[|<mime-type>]`` — the
    trailing mime-type field is optional so that older, pre-existing sidecar
    files (written with only ``<md5>|<artifact-urn>``) continue to work.

    Returns:
        A ``(artifact_urn, mime_type)`` tuple. Either or both may be
        ``None`` if the sidecar is missing, unreadable, stale (md5
        mismatch), or doesn't record a mime-type.
    """
    df = _upload_marker(file_path)

    if os.path.isfile(df) and os.access(df, os.R_OK):
        with open(df) as f:
            lines = f.readlines()
        if lines:
            parts = lines[0].strip().split("|")
            oh5 = parts[0] if len(parts) > 0 else None
            aid = parts[1] if len(parts) > 1 else None
            mime_type = parts[2] if len(parts) > 2 else None
            if oh5 and aid:
                h5 = md5sum(file_path)
                if oh5 == h5:
                    return aid.strip(), (mime_type.strip() if mime_type else None)
    return None, None


def mark_file_already_uploaded(id: str, file_path: str, *, mime_type: str | None = None):
    df = _upload_marker(file_path)
    h5 = md5sum(file_path)
    line = f"{h5}|{id}"
    if mime_type:
        line += f"|{mime_type}"
    with open(df, "w") as f:
        f.write(f"{line}\n")


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


class KeepFilePath(_CONCRETE_PATH):
    """
    A pathlib.Path subclass for a file the caller chose to keep.

    Returned by :meth:`Artifact.as_local_file` and :meth:`DataUrlArtifact.as_local_file`
    when an explicit ``path`` is given.  Supports the context manager protocol so that
    ``with artifact.as_local_file(path=...) as p:`` works, but never deletes the file
    on exit.
    """

    def __new__(cls, *pathsegments) -> Self:
        # Path subclasses must implement __new__; delegate to the concrete path type.
        return super().__new__(cls, *pathsegments)

    def __enter__(self) -> Self:
        """Return self for use in ``with`` statements."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """No-op — the file is kept after the ``with`` block."""


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
