# Releasing — publish the template without customer or personal data

**TL;DR:** Publish only from a commit that passes `python3 06_Engine/scripts/agency.py publish-check --ref <ref> --remote <remote>`; if the repository ever held customer material, publish its cleaned tree as fresh history instead of rewriting and re-exposing the old one.

## What the release gate checks

| Step | Proves | Command (run by `publish-check`) |
|---|---|---|
| Mode | The repository is the blank template (`mode: template` in `agency.yaml`) | — |
| Checkout | The working tree is a clean checkout of the ref, so the tree checks test what you publish | `git status` |
| Tree | No emails outside example and no-reply domains, tenant or conversation IDs, meeting and document links, credentials (tokens, JWTs, webhooks, signed URLs, credentials in URLs, secret assignments), file metadata (image text/EXIF/XMP/C2PA, office and PDF authors, SVG editor data) or denylisted terms — also inside archives, office files, UTF-16 text, binaries' readable strings, data URIs, notebook outputs and symlink targets; files it cannot read are reported, never skipped | `06_Engine/harness/check-privacy.py` |
| History | The same for every blob reachable from the ref, every file path that ever existed, commit and annotated tag messages, the names of local branches and tags that point into it, and commit and tag identities: no-reply emails, and names that match no denylisted term (your own `git config user.name` excepted) | `06_Engine/harness/check-privacy.py --history <ref>` |
| Hygiene | Template-mode rules: no hubs beyond the template, no mounted plug-ins, no `_TENANT` files, no personal paths | `06_Engine/harness/check-template.py` |
| Remote | Every ref the remote advertises (branches, tags, pull-request refs) is the ref or part of its history, and no ref name holds a denylisted term | `git ls-remote` |

Terms the gate cannot guess — customer names, people, codenames, project IDs, file keys — go in the local denylist
`.agency/denylist.txt` (ignored by git; one term per line, `re:` for a pattern). Matching ignores case and accents,
and a space in a term also matches hyphens, underscores and line breaks, so `Client Corp` finds `client-corp` slugs.
Keep the list current while you work, not only at release time. A line that must keep a flagged value says why
with `privacy: allow`.

## Publish

1. Work in `mode: workspace` with real projects; keep customer material in `*_TENANT.md` files and out of
   examples. Before release, return the repository to the blank template (`mode: template`, only
   `_template-project` in `01_Project-Hubs`, no plug-ins mounted).
2. Run the full review and the gate:
   ```sh
   python3 00_Agentic-OS/agentic-os-review.py
   python3 06_Engine/scripts/agency.py publish-check --ref main --remote origin
   ```
3. If the history fails (it ever contained customer material), publish fresh history instead of rewriting.
   `git checkout --orphan` keeps the working tree and index (`git switch --orphan` would empty them):
   ```sh
   git checkout --orphan release && git add -A && git commit -m "feat: initial public release"
   python3 06_Engine/scripts/agency.py publish-check --ref release
   ```
   Push it to a new, empty repository (recommended), or replace every branch on the existing remote and delete
   the rest. Commit with a no-reply address (`git config user.email <id>+<user>@users.noreply.github.com`).
4. Before changing visibility to public on an existing repository, close the gaps a push cannot:
   - forks keep the old history — ask their owners to delete them;
   - the host may keep unreachable commits, cached views and workflow logs — delete old workflow runs and ask
     the host's support to purge cached objects, or publish from a new repository;
   - collaborators' clones still hold the old history — ask them to re-clone, never to push old branches.
5. Re-clone the published repository and run the review and `publish-check` again on that clone.

## Never

- Never put customer names, people, screenshots, transcripts, survey answers or datasets in examples — use roles and
  placeholders that name no person, organization or real use case (see the sprint method skills).
- Never commit a document or image without stripping its metadata (authors, company, EXIF, C2PA).
- Never push a branch that `publish-check` reports as holding history outside the release.
