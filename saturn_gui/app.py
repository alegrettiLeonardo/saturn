"""SATURN desktop application loader.

The validated implementation source is stored in deterministic base64 chunks
under saturn_gui/_app_source. This loader decodes the source at import time.
"""
from __future__ import annotations

import base64
from pathlib import Path

_SOURCE_DIR = Path(__file__).with_name("_app_source")
_PARTS = sorted(_SOURCE_DIR.glob("*.b64"))
if not _PARTS:
    raise ImportError(f"SATURN GUI source payload not found in {_SOURCE_DIR}")

_payload = "".join(p.read_text(encoding="ascii").strip() for p in _PARTS)
_source = base64.b64decode(_payload, validate=True).decode("utf-8")
exec(compile(_source, __file__, "exec"), globals(), globals())
