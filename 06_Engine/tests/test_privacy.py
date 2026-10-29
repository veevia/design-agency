"""Privacy gate and publish check: detectors, binary metadata, denylists, history and remote refs."""

from __future__ import annotations

import base64
import gzip
import io
import json
import os
import struct
import subprocess
import tarfile
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path
from unittest import mock

from helpers import GIT_ENV, git, load_harness, make_host, run_cli, write

PRIVACY = load_harness("check-privacy.py")

# Synthetic values are assembled at runtime so this file never carries what the gate blocks.
AT = "@"
CORP = "client-corp" + ".com"
PERSONAL = "personal-mail" + ".net"
SAMPLE_GUID = "3f2504e0" + "-4f89-11d3-9a0c-" + "0305e82c3301"
MEETING = "https://teams." + "microsoft.com/l/" + "meetup-join/abc"
DESIGN_FILE = "https://www.figma.com/" + "design/" + "AbCdEfGhIjKlMnOpQrStUv/Name"
VALUE = "Q9w8E7r6" + "T5y4U3i2"
JPEG_EXIF = b"\xff\xd8\xff\xe1\x00\x20" + b"Exif\x00\x00" + b"\x00" * 20 + b"\xff\xd9"


def terms(*words: str):
    return [(word, PRIVACY.term_pattern(word)) for word in words]


def zipped(members: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, body in members.items():
            archive.writestr(name, body)
    return buffer.getvalue()


def png(text_chunks: dict[str, str] | None = None) -> bytes:
    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)
    out = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    for key, value in (text_chunks or {}).items():
        out += chunk(b"tEXt", key.encode() + b"\0" + value.encode())
    return out + chunk(b"IDAT", zlib.compress(b"\0\0\0\0")) + chunk(b"IEND", b"")


def docx(creator: str = "", body: str = "Hello") -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("docProps/core.xml", f"<cp:coreProperties><dc:creator>{creator}</dc:creator></cp:coreProperties>")
        archive.writestr("word/document.xml", f"<w:document><w:t>{body}</w:t></w:document>")
    return buffer.getvalue()


class DetectorTests(unittest.TestCase):
    def test_text_detectors_and_allow_rules(self):
        token = "ghp_" + "a" * 36
        lines = [
            f"contact jane.doe{AT}{CORP}",
            "bot 123+bot@users.noreply.github.com and you@example.com and ci@build.invalid",
            f"tenant {SAMPLE_GUID}",
            "placeholder 00000000-0000-0000-0000-000000000000",
            f"join {MEETING}",
            f"file {DESIGN_FILE}",
            "public https://www.figma.com/community/file/123456",
            f"token {token}",
            f"sample jane{AT}{CORP}  " + "privacy: allow — fictional address in a test fixture",
        ]
        findings = PRIVACY.scan_text("\n".join(lines), "f.md", [])
        self.assertEqual(sorted((f.kind, f.where) for f in findings), [
            ("credential", "f.md:8"), ("email", "f.md:1"), ("identifier", "f.md:3"), ("link", "f.md:5"), ("link", "f.md:6"),
        ])
        self.assertFalse(any(token[8:] in f.detail or "jane.doe" in f.detail for f in findings), "values are masked")
        allowed = PRIVACY.scan_text(f"contact ops{AT}{CORP}", "g.md", [], extra_domains=(CORP,))
        self.assertEqual(allowed, [])

    def test_lockfiles_skip_emails_and_ids_but_not_credentials_or_denylisted_terms(self):
        lock = '{"integrity": "sha512-' + SAMPLE_GUID + '", "author": "x' + AT + CORP + '"}'
        self.assertEqual(PRIVACY.scan_blob("web/package-lock.json", lock.encode(), []), [])
        feed = b'{"resolved": "https://pkgs.dev.azure.com/clientco/_packaging/feed/x.tgz"}'
        self.assertEqual([f.kind for f in PRIVACY.scan_blob("web/package-lock.json", feed, terms("Clientco"))], ["denylist"])

    def test_more_credential_formats_without_flagging_code_or_placeholders(self):
        flagged = {
            "jwt": "eyJ" + "hbGciOiJIUzI1NiJ9" + "." + "eyJ" + "zdWIiOiIxMjMifQ" + "." + "c2lnbmF0dXJlXzEy",
            "slack": "https://hooks.slack." + "com/services/" + "T0000/B0000/" + "x" * 24,
            "office": "https://client.webhook.office." + "com/webhookb2/" + "abc",
            "sas": "https://acct.blob.core.windows.net/c?sv=2022-11-02&" + "sig=" + "A" * 30,
            "npm": "_authToken=" + "npm_" + "a1B2c3D4e5" * 3 + "a1B2c3",
            "url": "https://bot:" + VALUE + AT + "git.corp-host.net/r.git",
            "env": "DB_PASSWORD=" + VALUE,
            "quoted": "const apiKey = '" + VALUE + "';",
        }
        for label, line in flagged.items():
            findings = PRIVACY.scan_text(line, "f.md", [])
            self.assertEqual([f.kind for f in findings], ["credential"], label)
            self.assertNotIn(VALUE, findings[0].detail, "values are masked")
        clean = [
            "  account = x, readSecret = readFrom1Password }) {",
            "DB_PASSWORD=${DB_PASSWORD_2}",
            "API_KEY=your-api-key-here-123",
            "https://user:" + "pass" + AT + "host.example.com/x",
            "https://x-access-token:${{ secrets.T }}" + AT + "github.com/o/r",
        ]
        for line in clean:
            self.assertEqual(PRIVACY.scan_text(line, "f.md", []), [], line)

    def test_denylist_ignores_accents_and_spans_line_breaks_hyphens_and_underscores(self):
        listed = terms("Clientco", "Partnerco Labs")
        text = "Review with Cli\u00ebntco\nSigned with Partnerco\nLabs\npartnerco_labs and PARTNERCO-LABS\nPartnercoLabs ok"
        self.assertEqual([f.where for f in PRIVACY.scan_text(text, "n.md", listed)], ["n.md:1", "n.md:2", "n.md:4", "n.md:4"])
        self.assertEqual([f.kind for f in PRIVACY.scan_blob("hubs/partnerco-labs/notes.md", b"clean", listed)], ["denylist"])
        allowed = PRIVACY.scan_text("Clientco  privacy: allow - fictional client in a fixture", "a.md", listed)
        self.assertEqual(allowed, [])

    def test_denylist_sources_regex_and_word_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            listing = write(root / "list.txt", "# client terms\nClientco\nre:\\bPRJ-\\d{4}\\b\n")
            write(root / ".agency" / "denylist.txt", "Partnerco\n")
            with mock.patch.dict(os.environ, {"AGENCY_DENYLIST": str(listing)}):
                terms = PRIVACY.load_denylist(root)
            self.assertEqual([term for term, _ in terms], ["Clientco", "re:\\bPRJ-\\d{4}\\b", "Partnerco"])
            findings = PRIVACY.scan_text("clientco notes\nClientcoian ok\nsee PRJ-2041\nPARTNERCO", "n.md", terms)
            self.assertEqual([f.where for f in findings], ["n.md:1", "n.md:3", "n.md:4"])
            path_hit = PRIVACY.scan_blob("hubs/clientco-launch/README.md", b"clean", terms)
            self.assertEqual([f.kind for f in path_hit], ["denylist"], "file paths are checked too")

    def test_binary_metadata(self):
        terms = [("Clientco", PRIVACY.re.compile(r"(?<![A-Za-z0-9])Clientco(?![A-Za-z0-9])", PRIVACY.re.I))]
        self.assertEqual(PRIVACY.scan_blob("clean.png", png(), terms), [])
        tagged = PRIVACY.scan_blob("shot.png", png({"Author": "Jane Doe"}), terms)
        self.assertEqual([f.kind for f in tagged], ["metadata"])
        office = PRIVACY.scan_blob("brief.docx", docx("Jane Doe", "Clientco launch plan"), terms)
        self.assertEqual(sorted(f.kind for f in office), ["denylist", "metadata"])
        pdf = PRIVACY.scan_blob("brief.pdf", b"%PDF-1.7\n1 0 obj << /Author (Jane Doe) >> endobj\n", [])
        self.assertEqual([f.kind for f in pdf], ["metadata"])
        svg = PRIVACY.scan_blob("icon.svg", b'<svg xmlns="http://www.w3.org/2000/svg" sodipodi:docname="x.svg"/>', [])
        self.assertEqual([f.kind for f in svg], ["metadata"])
        self.assertEqual(PRIVACY.scan_blob("plain.svg", b'<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0"/></svg>', []), [])

    def test_text_hidden_in_encodings_archives_and_embedded_payloads(self):
        listed = terms("Clientco")
        found = lambda name, data: sorted((f.kind, f.where) for f in PRIVACY.scan_blob(name, data, listed))  # noqa: E731
        self.assertEqual(found("notes.txt", ("\ufeff" + "Kick-off with Clientco").encode("utf-16-le")), [("denylist", "notes.txt:1")])
        self.assertEqual(found("cache.bin", b"\x00\x01" * 8 + b"meeting with Clientco" + b"\x00" * 8), [("denylist", "cache.bin")])
        self.assertEqual(found("bundle.zip", zipped({"notes.txt": ("contact jane.doe" + AT + PERSONAL).encode()})),
                         [("email", "bundle.zip!notes.txt:1")])
        self.assertEqual(found("notes.txt.gz", gzip.compress(b"Clientco rollout")), [("denylist", "notes.txt.gz!(decompressed):1")])
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w") as archive:
            body = b"Clientco plan"
            info = tarfile.TarInfo("notes/plan.txt")
            info.size = len(body)
            archive.addfile(info, io.BytesIO(body))
        self.assertEqual(found("bundle.tar", buffer.getvalue()), [("denylist", "bundle.tar!notes/plan.txt:1")])
        page = '<img src="data:image/jpeg;base64,' + base64.b64encode(JPEG_EXIF).decode() + '">'
        self.assertEqual(found("page.html", page.encode()), [("metadata", "page.html!data-uri-1.jpg")])
        notebook = {"cells": [{"cell_type": "code", "outputs": [{"output_type": "display_data",
                               "data": {"image/png": base64.b64encode(png({"Author": "Jane Doe"})).decode()}}]}]}
        self.assertEqual(found("nb.ipynb", json.dumps(notebook).encode()), [("metadata", "nb.ipynb!cell-1-output-1.png")])
        hex_author = PRIVACY.scan_blob("a.pdf", b"%PDF-1.4\n1 0 obj << /Author <FEFF004A0061006E0065> >> endobj\n", [])
        self.assertEqual([f.detail.split(" (")[0] for f in hex_author], ["embedded metadata: PDF author Jan…"])
        xmp = zlib.compress(b"<x:xmpmeta><dc:creator><rdf:li>Jane Doe</rdf:li></dc:creator></x:xmpmeta>")
        packed = b"%PDF-1.4\n2 0 obj << /Filter /FlateDecode >> stream\n" + xmp + b"\nendstream endobj\n"
        self.assertEqual([f.kind for f in PRIVACY.scan_blob("b.pdf", packed, [])], ["metadata"])
        office = PRIVACY.scan_blob("deck.pptx", zipped({"ppt/media/image1.jpg": JPEG_EXIF}), [])
        self.assertEqual([(f.kind, f.where) for f in office], [("metadata", "deck.pptx!ppt/media/image1.jpg")])

    def test_what_cannot_be_read_is_reported_not_skipped(self):
        broken = PRIVACY.scan_blob("bundle.zip", b"PK\x03\x04" + b"damaged" * 10, [])
        self.assertEqual([f.kind for f in broken], ["unscanned"])
        nested = zipped({"inner.zip": zipped({"deeper.zip": zipped({"notes.txt": b"hi"})})})
        self.assertEqual([(f.kind, f.where) for f in PRIVACY.scan_blob("outer.zip", nested, [])],
                         [("unscanned", "outer.zip!inner.zip!deeper.zip")])
        with mock.patch.object(PRIVACY, "MAX_BYTES", 100):
            self.assertEqual([f.kind for f in PRIVACY.scan_blob("big.txt", b"x" * 200, [])], ["unscanned"])


class TreeAndHistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "repo"
        self.root.mkdir()
        git(self.root, "init", "-q")
        self.denylist = [("Clientco", PRIVACY.re.compile(r"(?<![A-Za-z0-9])Clientco(?![A-Za-z0-9])", PRIVACY.re.I))]

    def tearDown(self):
        self.tmp.cleanup()

    def commit(self, message: str, email: str = "test@example.invalid") -> None:
        git(self.root, "add", "-A")
        git(self.root, "-c", f"user.email={email}", "-c", "user.name=Someone", "commit", "-q", "-m", message,
            "--author", f"Someone <{email}>")

    def test_history_finds_what_the_tree_no_longer_shows(self):
        write(self.root / "notes.md", "Kick-off with Clientco\n")
        write(self.root / "README.md", "# Project\n")
        self.commit("add kick-off notes", email=f"someone{AT}{PERSONAL}")
        (self.root / "notes.md").unlink()
        self.commit("drop the Clientco notes")
        self.assertEqual(PRIVACY.scan_tree(self.root, self.denylist), [])
        findings, commits = PRIVACY.scan_history(self.root, "HEAD", self.denylist)
        self.assertEqual(commits, 2)
        kinds = sorted({(f.kind, f.where.split(" ")[0]) for f in findings})
        self.assertIn(("denylist", "notes.md:1"), kinds)
        self.assertIn(("denylist", "commit"), kinds, "commit messages are scanned")
        self.assertEqual(sum(f.kind == "commit-identity" for f in findings), 1,
                         "the first commit's author (the test helper pins a placeholder committer)")

    def test_symlinks_are_not_content(self):
        write(self.root / "real.md", "clean\n")
        os.symlink("real.md", self.root / "link.md")
        self.commit("init")
        self.assertEqual(PRIVACY.tracked_files(self.root), ["real.md"])

    def test_symlink_targets_are_scanned_in_the_tree(self):
        write(self.root / "real.md", "clean\n")
        os.symlink("../Clientco-share/notes.md", self.root / "link.md")
        self.commit("init")
        findings = PRIVACY.scan_tree(self.root, self.denylist)
        self.assertEqual([(f.kind, f.where) for f in findings], [("denylist", "link.md (link target)")])

    def test_history_covers_every_path_tags_ref_names_and_identity_names(self):
        listed = terms("Clientco", "Partnerco")
        write(self.root / "a" / "readme.md", "same\n")
        write(self.root / "clientco-notes" / "readme.md", "same\n")
        self.commit("init")
        (self.root / "clientco-notes" / "readme.md").unlink()
        self.commit("tidy")
        git(self.root, "branch", "pilot/clientco")
        git(self.root, "commit", "-q", "--allow-empty", "-m", "plain", "--author", "Partnerco Bot <bot@example.invalid>")
        tagger = {**os.environ, **GIT_ENV, "GIT_COMMITTER_EMAIL": f"me{AT}{PERSONAL}"}
        subprocess.run(["git", "tag", "-a", "v1", "-m", "release for Partnerco"], cwd=self.root, env=tagger, check=True)
        findings, _ = PRIVACY.scan_history(self.root, "HEAD", listed)
        seen = {(f.kind, f.where, f.detail.split(" (")[0]) for f in findings}
        self.assertIn(("denylist", "clientco-notes/readme.md @history", "denylisted term 'Clientco' in the file path"), seen)
        self.assertIn(("denylist", "refs/heads/pilot/clientco", "denylisted term 'Clientco' in the ref name"), seen)
        self.assertIn(("denylist", "tag v1 message", "denylisted term 'Partnerco'"), seen)
        self.assertTrue(any(k == "commit-identity" and w == "tag v1" and "tagger email" in d for k, w, d in seen))
        self.assertTrue(any("author name matches denylisted term 'Partnerco'" in f.detail for f in findings))
        git(self.root, "config", "user.name", "Partnerco Bot")
        findings, _ = PRIVACY.scan_history(self.root, "HEAD", listed)
        self.assertFalse(any("author name" in f.detail for f in findings), "your own git user.name is who you publish as")


class PublishCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = make_host(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args: str, expect: int = 0) -> str:
        result = run_cli(self.root, *args)
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        return result.stdout

    def test_clean_template_is_ready_and_a_personal_identity_is_not(self):
        self.assertIn("publish check: READY", self.cli("publish-check"))
        write(self.root / "02_Workflows" / "notes.md", "Owner: ops\n")
        git(self.root, "add", "-A")
        git(self.root, "-c", f"user.email=me{AT}{PERSONAL}", "commit", "-q", "-m", "notes", "--author", f"Me <me{AT}{PERSONAL}>")
        out = self.cli("publish-check", expect=1)
        self.assertIn("NOT READY", out)
        self.assertIn("commit-identity", out)

    def test_remote_refs_outside_the_published_history_fail(self):
        remote = Path(self.tmp.name) / "remote.git"
        git(Path(self.tmp.name), "init", "-q", "--bare", str(remote))
        git(self.root, "remote", "add", "origin", str(remote))
        git(self.root, "push", "-q", "origin", "HEAD:refs/heads/main")
        self.assertIn("PASS  remote origin", self.cli("publish-check", "--remote", "origin"))
        git(self.root, "checkout", "-q", "--orphan", "old")
        write(self.root / "old.md", "old history\n")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-q", "-m", "old")
        git(self.root, "push", "-q", "origin", "old")
        git(self.root, "checkout", "-q", "main")
        out = self.cli("publish-check", "--ref", "main", "--remote", "origin", expect=1)
        self.assertIn("refs/heads/old", out)
        self.assertIn("local refs with history outside main", out)

    def test_the_checked_out_tree_must_be_the_ref(self):
        skill_file = self.root / "03_Agents-and-Skills" / "Skills" / "demo-skill" / "SKILL.md"
        skill_file.write_text(skill_file.read_text() + "\nedited\n")
        self.assertIn("not a clean checkout of HEAD", self.cli("publish-check", expect=1))
        git(self.root, "checkout", "-q", "--", ".")
        git(self.root, "branch", "other")
        git(self.root, "checkout", "-q", "other")
        git(self.root, "commit", "-q", "--allow-empty", "-m", "other")
        git(self.root, "checkout", "-q", "main")
        self.assertIn("not a clean checkout of other", self.cli("publish-check", "--ref", "other", expect=1))
        self.assertIn("publish check: READY", self.cli("publish-check"))

    def test_remote_pull_refs_and_denylisted_ref_names_fail(self):
        remote = Path(self.tmp.name) / "remote.git"
        git(Path(self.tmp.name), "init", "-q", "--bare", str(remote))
        git(self.root, "remote", "add", "origin", str(remote))
        git(self.root, "push", "-q", "origin", "HEAD:refs/heads/main", "HEAD:refs/heads/clientco-pilot")
        git(self.root, "checkout", "-q", "--orphan", "pr")
        write(self.root / "pr.md", "a contribution\n")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-q", "-m", "pr")
        git(self.root, "push", "-q", "origin", "HEAD:refs/pull/1/head")
        git(self.root, "checkout", "-q", "main")
        listing = write(Path(self.tmp.name) / "deny.txt", "Clientco\n")
        with mock.patch.dict(os.environ, {"AGENCY_DENYLIST": str(listing)}):
            out = self.cli("publish-check", "--ref", "main", "--remote", "origin", expect=1)
        self.assertIn("refs/pull/1/head", out)
        self.assertIn("pull request refs cannot be deleted by the owner", out)
        self.assertIn("refs/heads/clientco-pilot (denylisted term 'Clientco')", out)


if __name__ == "__main__":
    unittest.main()
