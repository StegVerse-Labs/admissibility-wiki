#!/usr/bin/env python3
"""Canonical compatibility entrypoint for the public-anchor reconstruction invitation.

The implementation remains in
`scripts/check_stegverse_public_anchor_reconstruction_invitation.py`.
This wrapper preserves the generic canonical checker name used by the
multi-docket aggregate without duplicating logic or changing authority.
"""
from __future__ import annotations

import runpy
from pathlib import Path

TARGET = Path(__file__).with_name("check_stegverse_public_anchor_reconstruction_invitation.py")

if __name__ == "__main__":
    runpy.run_path(str(TARGET), run_name="__main__")
