#!/usr/bin/env python3
"""Validate the SG-001 drawing asset and its canonical documentation reference."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ASSET = ROOT / "static/img/formalisms/original-drawing-reference.jpg"
PAGE = ROOT / "docs/formalisms/original-drawing-reference.md"
PUBLIC_PATH = "/img/formalisms/original-drawing-reference.jpg"
JPEG_SOI = b"\xff\xd8\xff"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MIN_SIZE_BYTES = 1024


def fail(message: str) -> None:
    raise SystemExit(f"ORIGINAL DRAWING PUBLICATION: FAIL - {message}")


def main() -> None:
    if not SOURCE_ASSET.is_file():
        fail(f"missing static asset: {SOURCE_ASSET.relative_to(ROOT)}")

    payload = SOURCE_ASSET.read_bytes()
    if len(payload) < MIN_SIZE_BYTES:
        fail(f"asset is unexpectedly small ({len(payload)} bytes)")

    if payload.startswith(JPEG_SOI):
        detected_format = "JPEG"
    elif payload.startswith(PNG_SIGNATURE):
        detected_format = "PNG_LEGACY_JPG_PATH"
    else:
        fail("asset binary signature is neither JPEG nor PNG")

    if not PAGE.is_file():
        fail(f"missing canonical page: {PAGE.relative_to(ROOT)}")

    page_text = PAGE.read_text(encoding="utf-8")
    if PUBLIC_PATH not in page_text:
        fail(f"canonical page does not reference {PUBLIC_PATH}")
    if "docs/docs/formalisms/original-drawing-reference" in page_text:
        fail("canonical page contains the removed nested docs/docs route")

    print(
        "ORIGINAL DRAWING PUBLICATION: PASS - "
        f"asset validated ({len(payload)} bytes, detected={detected_format}) and canonical page reference confirmed"
    )


if __name__ == "__main__":
    main()
