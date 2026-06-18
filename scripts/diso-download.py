#!/usr/bin/env python3
"""Download DISO member ontologies from their source links.

Self-contained: the Python standard library only, with `metadata/links.json` as its sole
input. For each ontology it tries the preferred source first (the authoritative `upstream`),
then each `mirror` in recorded order, and saves the first that downloads successfully.

By default it downloads only the ontologies that are NOT shipped in the DISO release — those
flagged `"withheld": true` in links.json (their redistribution rights could not be
established, so the release omits them and a user must obtain them from upstream). Pass
`--all` to download every member ontology instead.

Each ontology is saved under its own sub-directory of the output folder, so files that share
an upstream name never collide. Downloads are written atomically (temp file + rename), so an
interrupted run never leaves a truncated file at the final path.

Usage:
  python3 scripts/diso-download.py                 # only ontologies not in the release (withheld)
  python3 scripts/diso-download.py --all           # every member ontology
  python3 scripts/diso-download.py --list          # show what would be downloaded; no network
  python3 scripts/diso-download.py --dest ./onts   # choose the output directory
  python3 scripts/diso-download.py --links path/to/links.json

Exit status: 0 if every selected source was obtained or listed (entries with no recorded
source are reported but do not fail the run); non-zero if any download was attempted and all
of its sources were unreachable, or links.json could not be read.
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit, unquote

DEFAULT_LINKS = Path(__file__).resolve().parent.parent / "metadata" / "links.json"
CHUNK = 65536


def sources(entry: dict) -> list:
    """Candidate URLs, preferred first: upstream, then mirrors; empties dropped, de-duplicated."""
    urls = []
    if entry.get("upstream"):
        urls.append(entry["upstream"])
    for m in entry.get("mirrors", []) or []:
        if m:
            urls.append(m)
    out = []
    for u in urls:
        if u not in out:
            out.append(u)
    return out


def safe_name(s: str) -> str:
    """Filesystem-safe segment: keep word chars, dot, plus, hyphen; never '.' or '..' alone."""
    s = re.sub(r"[^\w.+-]", "_", s)
    return s if s.strip(".") else "ontology"


def target_path(dest: Path, label: str, url: str) -> Path:
    # URL-decode the path so percent-encoded stems (e.g. Brick%2Bimports.ttl) round-trip to
    # the registry stem (Brick+imports.ttl) that DISO-mappings keys on.
    name = Path(unquote(urlsplit(url).path)).name
    return dest / safe_name(label) / safe_name(name or label)


def download_to(url: str, out: Path, timeout: int) -> int:
    """Stream url to out atomically (write to .part, then rename). Returns bytes written."""
    req = urllib.request.Request(url, headers={"User-Agent": "diso-download/1.0"})
    tmp = out.with_name(out.name + ".part")
    total = 0
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp, open(tmp, "wb") as f:
            while True:
                chunk = resp.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)
                total += len(chunk)
        os.replace(tmp, out)
        return total
    finally:
        if tmp.exists():
            tmp.unlink()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true",
                    help="download every member ontology (default: only those not in the DISO release)")
    ap.add_argument("--dest", default="diso-ontologies", help="output directory (default: ./diso-ontologies)")
    ap.add_argument("--links", default=str(DEFAULT_LINKS), help="path to links.json")
    ap.add_argument("--list", action="store_true", help="list what would be downloaded; make no network requests")
    ap.add_argument("--timeout", type=int, default=60, help="per-request timeout in seconds (default: 60)")
    args = ap.parse_args()

    links_path = Path(args.links)
    if not links_path.is_file():
        print(f"ERROR: links.json not found: {links_path}", file=sys.stderr)
        return 2
    try:
        links = json.loads(links_path.read_text())
    except (OSError, ValueError) as exc:
        print(f"ERROR: could not read {links_path}: {exc}", file=sys.stderr)
        return 2
    if not isinstance(links, dict) or not all(isinstance(v, dict) for v in links.values()):
        print(f"ERROR: {links_path} is not a JSON object of per-ontology objects", file=sys.stderr)
        return 2

    selected = {k: v for k, v in links.items() if args.all or v.get("withheld")}
    scope = "all member ontologies" if args.all else "ontologies not in the DISO release (withheld)"
    if not selected:
        print(f"Nothing to download for: {scope}. (Use --all to fetch every ontology.)")
        return 0

    dest = Path(args.dest)
    print(f"diso-download: {len(selected)} {scope}" + ("" if args.list else f" -> {dest}") + "\n")

    ok = fail = nosrc = 0
    for label in selected:
        srcs = [u for u in sources(selected[label]) if urlsplit(u).scheme in ("http", "https")]
        if not srcs:
            print(f"  [no-source] {label}: no http(s) upstream or mirror URL recorded in links.json")
            nosrc += 1
            continue
        if args.list:
            extra = f"  (+{len(srcs) - 1} fallback)" if len(srcs) > 1 else ""
            print(f"  [would-get] {label:16} <- {srcs[0]}{extra}")
            continue
        got = False
        for url in srcs:
            out = target_path(dest, label, url)
            out.parent.mkdir(parents=True, exist_ok=True)
            try:
                n = download_to(url, out, args.timeout)
            except Exception as exc:  # noqa: BLE001 - any network/HTTP/IO error -> try next source
                print(f"  [retry    ] {label}: {url} failed ({type(exc).__name__})")
                continue
            print(f"  [ok       ] {label:16} <- {url}  ({n} bytes) -> {out}")
            ok += 1
            got = True
            break
        if not got:
            print(f"  [FAIL     ] {label}: all {len(srcs)} source(s) unreachable")
            fail += 1

    if args.list:
        return 0
    print(f"\n{ok} downloaded, {fail} failed, {nosrc} with no recorded source")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
