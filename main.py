#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The grader runs this program in a read-only /bot, so the program must
never write next to itself: the only output is
os.environ["MAKEFUN_OUTPUT_DIR"]/entry.png
"""
import hashlib
import os
import shutil
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, dst)
    w, h = png_size(dst)
    size = os.path.getsize(dst)
    digest = sha256(dst)
    assert (w, h) == (1024, 1024), "unexpected size %dx%d" % (w, h)
    assert size <= 1048576, "entry.png over 1 MiB: %d bytes" % size
    assert digest == sha256(SRC), "copy differs from source"
    print("OK entry.png %dx%d %d bytes sha256 %s" % (w, h, size, digest))
    print("OK wrote %s (source %s, %d bytes)" % (dst, SRC, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
