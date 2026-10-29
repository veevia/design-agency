#!/usr/bin/env python3
"""check-privacy.py — personal data, client terms and file metadata that must not ship.

Scans the tracked files (default) or every blob and commit reachable from a ref (`--history REF`) for:
  * email addresses outside example, placeholder and no-reply domains;
  * GUIDs (tenant, subscription, conversation IDs) other than the all-zero placeholder;
  * meeting and document links that carry IDs (Teams, Zoom, Meet, Webex, SharePoint, OneDrive,
    Google Docs/Drive, Figma files, Miro boards, Loom);
  * credentials: private keys, common token formats, JWTs, webhook URLs, signed-URL signatures,
    credentials inside URLs and secret-looking assignments; values are never printed;
  * metadata inside binaries: image text, EXIF, XMP and C2PA chunks; office document authors,
    company and comments; PDF authors (literal, hex or compressed); SVG editor metadata;
  * terms from local denylists that are never committed (client names, people, project codenames):
    $AGENCY_DENYLIST (paths separated by the OS path separator), <repo>/.agency/denylist.txt and
    ~/.config/agency/denylist.txt — one term per line, `re:<regex>` for a pattern, `#` for comments.
    Matching ignores case and accents, and a space in a term also matches line breaks, hyphens and
    underscores ("Client Corp" finds "client-corp" and a term broken across two lines).
It also looks inside archives (zip, tar, gzip), office files, UTF-16 text, the readable strings of
other binaries, base64 data URIs, notebook outputs and symlink targets. Files over 20 MB, unreadable
archive members and nesting deeper than two archives are reported as unscanned, never skipped silently.
With --history it also checks every file path that ever existed, commit messages, commit and tag
identities (no-reply or allowed email domains; names against the denylists except your own git
user.name), annotated tag messages and the names of local branches and tags that point into the history.

A text line containing `privacy: allow` is exempt; say why on the same line.

    python3 06_Engine/harness/check-privacy.py [--json]
    python3 06_Engine/harness/check-privacy.py --history HEAD [--allow-email-domain example.org]
"""

from __future__ import annotations

import argparse
import base64
import binascii
import bisect
import codecs
import gzip
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import unicodedata
import zipfile
import zlib
from dataclasses import asdict, dataclass
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parents[1]

ALLOWED_EMAIL_DOMAINS = ("example.com", "example.org", "example.net", "users.noreply.github.com", "noreply.github.com")
ALLOWED_EMAIL_SUFFIXES = (".example", ".invalid", ".test", ".localhost")
EMAIL = re.compile(r"(?<![\w.+%-])[A-Za-z0-9._%+-]+@((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})(?![\w-])")
GUID = re.compile(r"(?<![0-9A-Fa-f-])[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}(?![0-9A-Fa-f-])")
LINKS = re.compile(
    r"teams\.microsoft\.com/l/|teams\.live\.com/|\bzoom\.us/(?:j|my|w)/|meet\.google\.com/[a-z]|\.webex\.com/(?:meet|join)"
    r"|[A-Za-z0-9-]+\.sharepoint\.com/|\b1drv\.ms/|onedrive\.live\.com/"
    r"|docs\.google\.com/(?:document|spreadsheets|presentation|forms)/d/|drive\.google\.com/(?:file|drive)/"
    r"|figma\.com/(?:file|design|proto|board|slides)/[A-Za-z0-9]{10,}|miro\.com/app/board/|loom\.com/share/",
    re.I,
)
SECRETS = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|(?:ghp|gho|ghu|ghs|ghr|github_pat)_[A-Za-z0-9_]{20,}|\bsk-[A-Za-z0-9_-]{20,}"
    r"|\b[sr]k_live_[A-Za-z0-9]{20,}|xox[abprs]-[A-Za-z0-9-]{10,}|\bxapp-[A-Za-z0-9-]{20,}|AKIA[0-9A-Z]{16}"
    r"|AIza[0-9A-Za-z_-]{35}|\bfigd_[A-Za-z0-9_-]{20,}|\bnpm_[A-Za-z0-9]{36}\b|\bpypi-AgEIcHlwaS5vcmc[A-Za-z0-9_-]{20,}"
    r"|\bglpat-[A-Za-z0-9_-]{20,}|\bhf_[A-Za-z0-9]{30,}|AccountKey=[A-Za-z0-9+/=]{20,}|SharedAccessSignature=[^\s;\"']{20,}"
    r"|[?&]sig=[A-Za-z0-9%+/=]{20,}|\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"
    r"|hooks\.slack\.com/(?:services|workflows|triggers)/[A-Za-z0-9/_-]{16,}|\.webhook\.office\.com/webhookb2/"
    r"|discord(?:app)?\.com/api/webhooks/\d+/"
)
URL_CREDENTIALS = re.compile(r"\b[a-z][a-z0-9+.-]*://([^\s/:@<>{}\[\]$%\"'`]+):([^\s/@<>\"'`]+)@[A-Za-z0-9.-]+", re.I)
# A quoted value anywhere, or an unquoted one when the key starts the line (.env, YAML, ini); never code identifiers.
ASSIGNED_SECRET = re.compile(
    r"(^\s*(?:export\s+)?[\"']?)?\b[A-Za-z0-9_.-]*(?:password|passwd|pwd|secret|api_?key|access_?key|auth_?token|access_?token"
    r"|private_?key)[A-Za-z0-9_.-]*[\"']?\s*[:=]\s*([\"']?)([^\s\"'`#;,]{12,})", re.I)
PLACEHOLDER = re.compile(r"[<>{}()\[\]$%/\\*]|\.\.\.|example|placeholder|changeme|change_me|your|redacted|dummy|sample|xxxx", re.I)
DOTTED_NAME = re.compile(r"^[A-Za-z_][\w-]*(?:\.[A-Za-z_][\w-]*)+$")
DATA_URI = re.compile(r"data:([a-z]+/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=]{40,})", re.I)
MIME_EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg", "image/gif": ".gif", "image/webp": ".webp",
            "image/tiff": ".tiff", "image/heic": ".heic", "image/avif": ".avif", "image/svg+xml": ".svg", "application/pdf": ".pdf"}
ALLOW_MARKER = "privacy: allow"
LOCKFILES = ("package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "uv.lock", "Cargo.lock")
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff", ".heic", ".avif"}
OFFICE_EXT = {".docx", ".xlsx", ".pptx", ".docm", ".xlsm", ".pptm"}
SVG_META = re.compile(r"<metadata\b|sodipodi:docname=|inkscape:export-filename=|<dc:creator\b|<rdf:RDF\b", re.I)
MAX_BYTES = 20_000_000
MAX_MEMBERS = 5_000
MAX_DEPTH = 2
SELF = Path(__file__).resolve()

ALL = frozenset({"credential", "email", "identifier", "link", "denylist"})
LOCKFILE = frozenset({"credential", "denylist"})
STRINGS = frozenset({"credential", "denylist"})
OFFICE_TEXT = frozenset({"credential", "email", "link", "denylist"})
LINK_TARGET = frozenset({"credential", "email", "link", "denylist"})


@dataclass(frozen=True)
class Finding:
    kind: str
    where: str
    detail: str


# --------------------------------------------------------------------------- denylist


def fold(text: str) -> str:
    """Accent- and width-insensitive form used for denylist matching; keeps line breaks where they are."""
    if text.isascii():
        return text
    return "".join(ch for ch in unicodedata.normalize("NFKD", text) if not unicodedata.combining(ch))


def denylist_paths(root: Path) -> list[Path]:
    paths = [Path(p) for p in os.environ.get("AGENCY_DENYLIST", "").split(os.pathsep) if p]
    paths += [root / ".agency" / "denylist.txt", Path.home() / ".config" / "agency" / "denylist.txt"]
    seen, out = set(), []
    for path in paths:
        resolved = path.expanduser().resolve()
        if resolved not in seen and resolved.is_file():
            seen.add(resolved)
            out.append(resolved)
    return out


def term_pattern(term: str) -> re.Pattern:
    words = [re.escape(word) for word in re.split(r"[\s_-]+", fold(term)) if word]
    return re.compile(r"(?<![A-Za-z0-9])" + r"[\s_-]+".join(words) + r"(?![A-Za-z0-9])", re.I)


def load_denylist(root: Path) -> list[tuple[str, re.Pattern]]:
    terms: list[tuple[str, re.Pattern]] = []
    for path in denylist_paths(root):
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            terms.append((line, re.compile(line[3:], re.I) if line.startswith("re:") else term_pattern(line)))
    return terms


def denylist_hits(text: str, denylist) -> list[str]:
    folded = fold(text)
    return [term for term, pattern in denylist if pattern.search(folded)]


# --------------------------------------------------------------------------- detectors


def email_allowed(domain: str, extra: tuple[str, ...]) -> bool:
    domain = domain.lower()
    allowed = ALLOWED_EMAIL_DOMAINS + tuple(d.lower() for d in extra)
    return domain in allowed or domain.endswith(ALLOWED_EMAIL_SUFFIXES) or any(domain.endswith("." + d) for d in allowed)


def mask(value: str) -> str:
    return value[:3] + "…" if len(value) > 3 else "…"


def _assigned_secret(value: str) -> bool:
    return (len(value) >= 12 and re.search(r"\d", value) is not None and re.search(r"[A-Za-z]", value) is not None
            and not PLACEHOLDER.search(value) and not DOTTED_NAME.match(value) and not re.fullmatch(r"[A-Z0-9_]+", value))


def _credentials(line: str) -> tuple[list[str], str]:
    """(masked credential descriptions, the line with URL credentials blanked for the other detectors)."""
    found = [f"looks like a credential ({mask(m.group(0))}); remove and rotate it" for m in SECRETS.finditer(line)]
    for match in URL_CREDENTIALS.finditer(line):
        if not PLACEHOLDER.search(match.group(2)) and match.group(2).lower() not in {"pass", "password", "passwd", "secret", "token", "pat"}:
            found.append(f"credentials inside a URL ({match.group(1)[:3]}…:…@); remove and rotate them")
    line = URL_CREDENTIALS.sub("<url-with-credentials>", line)
    if not found:
        for match in ASSIGNED_SECRET.finditer(line):
            if (match.group(1) is not None or match.group(2)) and _assigned_secret(match.group(3)):
                found.append(f"secret-looking assignment ({mask(match.group(0))}); move it to a secret store and rotate it")
                break
    return found, line


def scan_text(text: str, where: str, denylist, *, lockfile: bool = False, extra_domains: tuple[str, ...] = (),
              detectors: frozenset[str] | None = None) -> list[Finding]:
    active = detectors if detectors is not None else (LOCKFILE if lockfile else ALL)
    findings: list[Finding] = []
    lines = text.split("\n")
    for number, raw in enumerate(lines, 1):
        line = raw.rstrip("\r")
        if ALLOW_MARKER in line:
            continue
        at = f"{where}:{number}"
        credentials, line = _credentials(line)
        if "credential" in active:
            findings += [Finding("credential", at, detail) for detail in credentials]
        if "email" in active:
            for match in EMAIL.finditer(line):
                if not email_allowed(match.group(1), extra_domains):
                    findings.append(Finding("email", at, f"email address {mask(match.group(0))}@{match.group(1)}"))
        if "identifier" in active:
            for match in GUID.finditer(line):
                if set(match.group(0).replace("-", "")) != {"0"}:
                    findings.append(Finding("identifier", at, f"GUID {match.group(0)[:8]}… (tenant, subscription or conversation ID?)"))
        if "link" in active:
            for match in LINKS.finditer(line):
                findings.append(Finding("link", at, f"meeting or document link ({match.group(0)}…)"))
    if "denylist" in active and denylist:
        folded = fold(text)
        starts = [0] + [i + 1 for i, ch in enumerate(folded) if ch == "\n"]
        for term, pattern in denylist:
            for match in pattern.finditer(folded):
                number = bisect.bisect_right(starts, match.start())
                if number <= len(lines) and ALLOW_MARKER in lines[number - 1]:
                    continue
                findings.append(Finding("denylist", f"{where}:{number}", f"denylisted term {term!r}"))
    return findings


def _png_chunks(data: bytes) -> list[str]:
    found, offset = [], 8
    while offset + 8 <= len(data):
        length = int.from_bytes(data[offset:offset + 4], "big")
        kind = data[offset + 4:offset + 8].decode("latin-1")
        body = data[offset + 8:offset + 8 + length]
        if kind in ("tEXt", "zTXt", "iTXt"):
            key = body.split(b"\0", 1)[0].decode("latin-1")[:40]
            found.append(f"{kind}:{key}")
        elif kind in ("eXIf", "caBX"):
            found.append(kind)
        offset += 12 + length
        if kind == "IEND":
            break
    return found


def _inflate(data: bytes) -> bytes:
    try:
        return zlib.decompressobj().decompress(data, MAX_BYTES)
    except zlib.error:
        return b""


def _pdf_string(raw: bytes) -> str:
    if raw.startswith(b"<"):
        try:
            raw = bytes.fromhex(re.sub(rb"[^0-9A-Fa-f]", b"", raw[1:-1]).decode())
        except ValueError:
            return ""
    else:
        raw = raw[1:-1]
    if raw.startswith(codecs.BOM_UTF16_BE):
        return raw[2:].decode("utf-16-be", "ignore").strip()
    return raw.decode("latin-1").strip()


def binary_strings(data: bytes) -> str:
    """Readable ASCII and UTF-16LE runs, as `strings` would show them."""
    runs = [m.decode("latin-1") for m in re.findall(rb"[\x20-\x7e]{4,}", data)]
    runs += [m.decode("utf-16-le") for m in re.findall(rb"(?:[\x20-\x7e]\x00){4,}", data)]
    return "\n".join(runs)


def binary_metadata(name: str, data: bytes) -> tuple[list[str], str]:
    """(metadata descriptions, extra text for denylist matching beyond the readable strings)."""
    ext = Path(name).suffix.lower()
    notes: list[str] = []
    text = ""
    if ext == ".png" and data.startswith(b"\x89PNG\r\n\x1a\n"):
        notes = [f"PNG chunk {chunk}" for chunk in _png_chunks(data)]
    elif ext in IMAGE_EXT:
        for marker, label in ((b"Exif\x00\x00", "EXIF"), (b"http://ns.adobe.com/xap/1.0/", "XMP"), (b"jumb", "C2PA/JUMBF")):
            if marker in data:
                notes.append(label)
    elif ext == ".pdf" or data.startswith(b"%PDF"):
        streams = [_inflate(s) for s in re.findall(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S)[:500]]
        for chunk in [data, *streams]:
            for raw in re.findall(rb"/Author\s*(\((?:\\.|[^\\)])*\)|<[0-9A-Fa-f\s]*>)", chunk):
                author = _pdf_string(raw)
                if author:
                    notes.append(f"PDF author {mask(author)}")
            if b"<dc:creator" in chunk and "PDF XMP creator" not in notes:
                notes.append("PDF XMP creator")
        text = "\n".join(binary_strings(s) for s in streams if s)
    return notes, text


def _office(name: str, data: bytes, denylist, extra_domains, depth: int) -> list[Finding]:
    findings: list[Finding] = []
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            names = archive.namelist()
            for part, fields in (("docProps/core.xml", ("creator", "lastModifiedBy")), ("docProps/app.xml", ("Company", "Manager"))):
                if part in names:
                    xml = archive.read(part).decode("utf-8", "ignore")
                    for field in fields:
                        value = re.search(rf"<(?:\w+:)?{field}>([^<]+)<", xml)
                        if value and value.group(1).strip():
                            findings.append(Finding("metadata", name, f"embedded metadata: {field} {mask(value.group(1).strip())} (strip it before publishing)"))
            if any(n.endswith(("commentAuthors.xml", "people.xml")) or "/comments" in n for n in names):
                findings.append(Finding("metadata", name, "embedded metadata: comments or comment authors (strip it before publishing)"))
            for info in archive.infolist()[:MAX_MEMBERS]:
                if info.is_dir() or info.file_size > MAX_BYTES:
                    continue
                body = archive.read(info)
                if info.filename.endswith((".xml", ".rels")):
                    text = re.sub(r"<[^>]+>", " ", body.decode("utf-8", "ignore"))
                    findings += [Finding(f.kind, f"{name}!{info.filename}", f.detail)
                                 for f in scan_text(text, info.filename, denylist, extra_domains=extra_domains, detectors=OFFICE_TEXT)]
                else:
                    findings += scan_blob(f"{name}!{info.filename}", body, denylist, extra_domains=extra_domains, depth=depth + 1)
    except (zipfile.BadZipFile, OSError, RuntimeError, EOFError, zlib.error):
        findings.append(Finding("unscanned", name, "office file could not be read (damaged or encrypted): review it by hand"))
    return findings


def _tar_members(data: bytes) -> list[tuple[str, bytes | None]] | None:
    if len(data) < 262 or data[257:262] != b"ustar":
        return None
    members: list[tuple[str, bytes | None]] = []
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for member in archive.getmembers()[:MAX_MEMBERS]:
            if member.issym() or member.islnk():
                members.append((member.name + " (link target)", member.linkname.encode()))
            elif member.isfile():
                handle = archive.extractfile(member) if member.size <= MAX_BYTES else None
                members.append((member.name, handle.read() if handle else None))
    return members


def is_archive(data: bytes) -> bool:
    return data[:4] == b"PK\x03\x04" or data[:2] == b"\x1f\x8b" or (len(data) >= 262 and data[257:262] == b"ustar")


def archive_members(data: bytes) -> list[tuple[str, bytes | None]]:
    """Members of a zip, tar or gzip payload; a None body marks one that could not be read."""
    try:
        if data[:4] == b"PK\x03\x04":
            members: list[tuple[str, bytes | None]] = []
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for info in archive.infolist()[:MAX_MEMBERS]:
                    if info.is_dir():
                        continue
                    if info.flag_bits & 0x1 or info.file_size > MAX_BYTES:
                        members.append((info.filename, None))
                        continue
                    with archive.open(info) as handle:
                        members.append((info.filename, handle.read(MAX_BYTES + 1)))
            return members
        if data[:2] == b"\x1f\x8b":
            body = gzip.GzipFile(fileobj=io.BytesIO(data)).read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                return [("(decompressed)", None)]
            return _tar_members(body) or [("(decompressed)", body)]
        return _tar_members(data) or []
    except (zipfile.BadZipFile, tarfile.TarError, OSError, EOFError, RuntimeError, zlib.error, ValueError):
        return [("(archive)", None)]


def decode_text(data: bytes) -> str | None:
    if data.startswith(codecs.BOM_UTF8):
        return data[3:].decode("utf-8", "replace")
    if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return data.decode("utf-16", "replace")
    if b"\0" in data[:8000]:
        return None
    return data.decode("utf-8", "replace")


def _embedded(name: str, text: str) -> list[tuple[str, bytes]]:
    """Base64 payloads inside text: data URIs and notebook outputs."""
    payloads: list[tuple[str, str]] = [(f"data-uri-{i}{MIME_EXT.get(m.group(1).lower(), '.bin')}", m.group(2))
                                      for i, m in enumerate(DATA_URI.finditer(text), 1)]
    if name.lower().endswith(".ipynb"):
        try:
            cells = json.loads(text).get("cells", [])
        except (ValueError, AttributeError):
            cells = []
        for c, cell in enumerate(cells if isinstance(cells, list) else [], 1):
            for o, output in enumerate(cell.get("outputs", []) if isinstance(cell, dict) else [], 1):
                data = output.get("data", {}) if isinstance(output, dict) else {}
                for mime, value in (data.items() if isinstance(data, dict) else []):
                    if mime in MIME_EXT and mime != "image/svg+xml":
                        payloads.append((f"cell-{c}-output-{o}{MIME_EXT[mime]}", "".join(value) if isinstance(value, list) else str(value)))
    decoded = []
    for label, payload in payloads:
        try:
            decoded.append((label, base64.b64decode(payload, validate=False)))
        except (binascii.Error, ValueError):
            continue
    return decoded


def scan_blob(name: str, data: bytes, denylist, *, extra_domains: tuple[str, ...] = (), depth: int = 0) -> list[Finding]:
    findings: list[Finding] = []
    own_path = name.rsplit("!", 1)[-1] if depth else name
    findings += [Finding("denylist", name, f"denylisted term {term!r} in the file path") for term in denylist_hits(own_path, denylist)]
    if len(data) > MAX_BYTES:
        return findings + [Finding("unscanned", name, "larger than 20 MB, not scanned: review it by hand or keep it out of the repository")]
    ext = Path(own_path).suffix.lower()
    if ext in OFFICE_EXT and data[:4] == b"PK\x03\x04":
        return findings + _office(name, data, denylist, extra_domains, depth)
    if is_archive(data):
        if depth >= MAX_DEPTH:
            return findings + [Finding("unscanned", name, f"archive nested more than {MAX_DEPTH} deep, not scanned: review it by hand")]
        for member, body in archive_members(data):
            where = f"{name}!{member}"
            if body is None:
                findings.append(Finding("unscanned", where, "archive member could not be read (encrypted, damaged or over 20 MB)"))
            else:
                findings += scan_blob(where, body, denylist, extra_domains=extra_domains, depth=depth + 1)
        return findings
    text = None if ext in IMAGE_EXT or ext == ".pdf" else decode_text(data)
    if text is None:
        notes, extra_text = binary_metadata(own_path, data)
        findings += [Finding("metadata", name, f"embedded metadata: {note} (strip it before publishing)") for note in notes]
        strings = binary_strings(data) + ("\n" + extra_text if extra_text else "")
        findings += [Finding(f.kind, name, f.detail) for f in scan_text(strings, name, denylist, detectors=STRINGS)]
        return findings
    if ext == ".svg" and SVG_META.search(text):
        findings.append(Finding("metadata", name, "SVG editor metadata (<metadata>, sodipodi/inkscape or dc:creator)"))
    findings += scan_text(text, name, denylist, lockfile=Path(own_path).name in LOCKFILES, extra_domains=extra_domains)
    if depth < MAX_DEPTH:
        for label, payload in _embedded(own_path, text):
            findings += scan_blob(f"{name}!{label}", payload, denylist, extra_domains=extra_domains, depth=depth + 1)
    return findings


# --------------------------------------------------------------------------- sources


def git(root: Path, *args: str, binary: bool = False):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout if binary else result.stdout.decode("utf-8", "replace")


def _index_entries(root: Path) -> list[tuple[str, str]]:
    out = git(root, "ls-files", "-s", "-z")
    return [(entry.split(" ", 1)[0], entry.split("\t", 1)[1]) for entry in out.split("\0") if entry]


def tracked_files(root: Path) -> list[str]:
    try:
        entries = _index_entries(root)
    except RuntimeError:
        return [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    return [name for mode, name in entries if mode not in ("120000", "160000")]  # links and plug-in gitlinks are not content


def tracked_symlinks(root: Path) -> list[str]:
    try:
        return [name for mode, name in _index_entries(root) if mode == "120000"]
    except RuntimeError:
        return []


def scan_tree(root: Path, denylist, extra_domains: tuple[str, ...] = ()) -> list[Finding]:
    findings: list[Finding] = []
    for name in tracked_files(root):
        path = root / name
        if path.resolve() == SELF or not path.is_file() or path.is_symlink():
            continue
        if path.stat().st_size > MAX_BYTES:
            findings.append(Finding("unscanned", name, "larger than 20 MB, not scanned: review it by hand or keep it out of the repository"))
            continue
        findings += scan_blob(name, path.read_bytes(), denylist, extra_domains=extra_domains)
    for name in tracked_symlinks(root):
        path = root / name
        if path.is_symlink():
            target = os.readlink(path)
            findings += [Finding(f.kind, f"{name} (link target)", f.detail)
                         for f in scan_text(target, name, denylist, extra_domains=extra_domains, detectors=LINK_TARGET)]
            findings += [Finding("denylist", name, f"denylisted term {term!r} in the file path") for term in denylist_hits(name, denylist)]
    return findings


def _identity(where: str, role: str, name: str, email: str, denylist, extra_domains, own_name: str) -> list[Finding]:
    findings = []
    domain = email.rsplit("@", 1)[-1] if "@" in email else ""
    if not email_allowed(domain, extra_domains):
        findings.append(Finding("commit-identity", where, f"{role} email {mask(email.rsplit('@', 1)[0])}@{domain} (use a no-reply address)"))
    if name.strip() and fold(name).casefold() != fold(own_name).casefold():
        findings += [Finding("commit-identity", where, f"{role} name matches denylisted term {term!r}") for term in denylist_hits(name, denylist)]
    return findings


def scan_history(root: Path, ref: str, denylist, extra_domains: tuple[str, ...] = ()) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    try:
        own_name = git(root, "config", "user.name").strip()
    except RuntimeError:
        own_name = ""
    commits = git(root, "rev-list", ref).split()
    for line in git(root, "log", "--format=%H%x00%an%x00%ae%x00%cn%x00%ce", ref).splitlines():
        sha, an, ae, cn, ce = line.split("\0")
        findings += _identity(sha[:8], "author", an, ae, denylist, extra_domains, own_name)
        findings += _identity(sha[:8], "committer", cn, ce, denylist, extra_domains, own_name)
    for sha in commits:
        message = git(root, "log", "-1", "--format=%B", sha)
        findings += [Finding(f.kind, f"commit {sha[:8]} message", f.detail) for f in scan_text(message, "msg", denylist, extra_domains=extra_domains)]
    # Every path that ever existed: a blob is read once, but the same content can sit under other names.
    for path in set(git(root, "log", "--format=", "--name-only", "-z", "-m", "--root", "--no-renames", ref).replace("\n", "\0").split("\0")):
        if path:
            findings += [Finding("denylist", f"{path} @history", f"denylisted term {term!r} in the file path") for term in denylist_hits(path, denylist)]
    commit_set = set(commits)
    for line in git(root, "for-each-ref", "--format=%(refname)%00%(objecttype)%00%(objectname)%00%(*objectname)", "refs/heads", "refs/tags").splitlines():
        refname, kind, oid, peeled = line.split("\0")
        if (peeled or oid) not in commit_set:
            continue
        short = refname.split("/", 2)[-1]
        findings += [Finding("denylist", refname, f"denylisted term {term!r} in the ref name") for term in denylist_hits(short, denylist)]
        if kind == "tag":
            header, _, message = git(root, "cat-file", "tag", oid).partition("\n\n")
            tagger = re.search(r"^tagger (.*) <([^>]*)>", header, re.M)
            if tagger:
                findings += _identity(f"tag {short}", "tagger", tagger.group(1), tagger.group(2), denylist, extra_domains, own_name)
            findings += [Finding(f.kind, f"tag {short} message", f.detail) for f in scan_text(message, "msg", denylist, extra_domains=extra_domains)]
    objects: dict[str, str] = {}
    for line in git(root, "rev-list", "--objects", ref).splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            objects.setdefault(parts[0], parts[1])
    proc = subprocess.Popen(["git", "-C", str(root), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert proc.stdin and proc.stdout
    for sha, name in objects.items():
        proc.stdin.write(f"{sha}\n".encode())
        proc.stdin.flush()
        header = proc.stdout.readline().decode().split()
        size = int(header[2]) if len(header) == 3 else 0
        data = proc.stdout.read(size)
        proc.stdout.read(1)
        if len(header) == 3 and header[1] == "blob":
            findings += [Finding(f.kind, f"{f.where} @history", f.detail) for f in scan_blob(name, data, denylist, extra_domains=extra_domains)]
    proc.stdin.close()
    proc.stdout.close()
    proc.wait()
    return findings, len(commits)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ENGINE_DIR.parent)
    parser.add_argument("--history", metavar="REF", help="scan every commit, message and blob reachable from REF")
    parser.add_argument("--allow-email-domain", action="append", default=[], help="additional allowed email domain")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    denylist = load_denylist(root)
    extra = tuple(args.allow_email_domain)
    if args.history:
        findings, commits = scan_history(root, args.history, denylist, extra)
        scope = f"history of {args.history} ({commits} commits)"
    else:
        findings = scan_tree(root, denylist, extra)
        scope = "tracked files"
    unique = list(dict.fromkeys(findings))
    if args.json:
        print(json.dumps({"scope": scope, "denylists": [str(p) for p in denylist_paths(root)], "denylist_terms": len(denylist),
                          "findings": [asdict(f) for f in unique]}, indent=2))
    else:
        for finding in unique:
            print(f"FAIL [{finding.kind}] {finding.where}: {finding.detail}")
        print(f"privacy ({scope}; {len(denylist)} denylist terms): "
              + ("clean" if not unique else f"{len(unique)} finding(s)"))
    return 1 if unique else 0


if __name__ == "__main__":
    sys.exit(main())
