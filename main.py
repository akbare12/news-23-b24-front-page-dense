#!/usr/bin/env python3
"""news-23 b24 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import os
import struct
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("bad PNG signature")
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (1024, 1024):
        sys.exit(f"bad size {w}x{h}, want 1024x1024")
    if len(data) > 1024 * 1024:
        sys.exit("entry.png over 1 MiB")
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        sys.exit("bad PNG trailer: missing well-formed IEND chunk")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    # Guard: never write next to this script (the grader runs from a read-only copy).
    if os.path.abspath(outdir) == here:
        sys.exit("refusing to write output next to main.py")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        if f.read() != data:
            sys.exit("output differs from source entry.png")
    print(f"wrote {dst} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
