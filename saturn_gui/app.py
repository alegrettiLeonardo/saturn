"""SATURN desktop application loader.

The desktop source is stored as deterministic gzip+base64 chunks under
``saturn_gui/_app_source_v21``.  Keeping the presentation payload separate
preserves the compact bootstrap layout used by this repository while still
shipping the reviewed Python source exactly.
"""
from __future__ import annotations

import base64
import gzip
from pathlib import Path

_SOURCE_DIR = Path(__file__).with_name("_app_source_v21")
_PARTS = sorted(_SOURCE_DIR.glob("*.b64"))
if not _PARTS:
    raise ImportError(f"SATURN GUI source payload not found in {_SOURCE_DIR}")

_payload = "".join(p.read_text(encoding="ascii").strip() for p in _PARTS)
_source = gzip.decompress(base64.b64decode(_payload, validate=True)).decode("utf-8")
exec(compile(_source, __file__, "exec"), globals(), globals())

# Install the approved reference-derived artwork after loading the presentation.
from .visual_assets import install as _install_visual_assets
_install_visual_assets(SaturnApp)
