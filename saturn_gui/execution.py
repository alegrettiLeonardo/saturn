from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import os
import re


@dataclass(frozen=True)
class ExecutionConfig:
    mode: str = "full"
    workers: str = "4"
    heartbeat: int = 15
    audit: bool = True
    serial: bool = False


MODE_TARGETS = {
    "baseline": "robust-3obj-baseline",
    "smoke": "robust-3obj-smoke",
    "search": "robust-3obj-search",
    "full": "robust-3obj",
}


def build_make_command(cfg: ExecutionConfig) -> list[str]:
    target = MODE_TARGETS.get(cfg.mode)
    if target is None:
        raise ValueError(f"modo de execução desconhecido: {cfg.mode}")
    if cfg.serial and cfg.mode in {"smoke", "search", "full"}:
        serial_target = {
            "smoke": "robust-3obj-smoke-serial",
            "search": "robust-3obj-search-serial",
            "full": "robust-3obj-serial",
        }
        target = serial_target[cfg.mode]
    cmd = ["make", target]
    if not cfg.serial and cfg.mode != "baseline":
        cmd.append(f"ROBUST3_WORKERS={cfg.workers}")
        cmd.append(f"ROBUST3_HEARTBEAT={int(cfg.heartbeat)}")
    if cfg.mode in {"search", "full"}:
        cmd.append(f"ROBUST3_AUDIT={1 if cfg.audit else 0}")
    return cmd


# High-level stages mirror the real robust three-objective workflow.  They are
# intentionally coarser than the internal P4/P5/P6 optimizer tags so the desktop
# progress panel stays readable while still being driven only by real solver output.
STAGES = [
    "Baseline",
    "Commercial Screening",
    "Dynamic Screening",
    "Nominal Optimization",
    "Robust Audit",
    "Robust Search",
    "Final Verification",
    "Report",
]


def stage_from_log(line: str, current: str = "Baseline") -> str:
    """Map native SATURN/shaftOpt console text to one UI progress stage.

    The parser recognizes the headings emitted by ``popa_3obj_console`` and the
    lower-level P4/P5/P6 tags.  It never advances the scientific workflow itself;
    it only reflects what the backend has already printed.
    """
    u = line.upper()

    if (
        "POPA FINAL REPORT" in u
        or "REPORT DIRECTORY" in u
        or "WRITING SHAFTOPT_FINAL_REPORT" in u
        or "END OF SHAFTOPT POPA-STYLE FINAL REPORT" in u
    ):
        return "Report"
    if (
        "FINAL VERIFICATION" in u
        or "FINAL_VERIFICATION" in u
        or "FINALISTS" in u
        or "FINE ROTORDYNAMIC" in u
        or "FINE ROBUST SCENARIO" in u
        or re.search(r"\bPHASE\s+11(?:/15)?\b", u)
    ):
        return "Final Verification"
    if (
        "ROBUST MULTIOBJECTIVE CONTINUOUS SEARCH" in u
        or "ROBUST MULTIOBJECTIVE SCENARIO EVALUATION" in u
        or "FINAL ROBUST SCENARIO HARMONIZATION" in u
        or re.search(r"\bPHASE\s+(?:9-10|10H)\b", u)
        or re.search(r"\bP10[-_ ]?COBYQA", u)
    ):
        return "Robust Search"
    if (
        "INITIAL ROBUST SCENARIO AUDIT" in u
        or "ROBUST SCENARIO ENRICHMENT" in u
        or "PROMOTED ROBUST SCENARIO RE-EVALUATION" in u
        or re.search(r"\bPHASE\s+[78]\b", u)
    ):
        return "Robust Audit"
    if (
        "NOMINAL MULTIOBJECTIVE OPTIMIZATION" in u
        or re.search(r"\bPHASE\s+4-6\b", u)
        or re.search(r"\bP[456][-_ ]?(?:SOBOL|DE|COBYQA)", u)
        or "DE-SOBOL" in u
        or "DIFFERENTIAL EVOLUTION" in u
        or "COBYQA" in u
    ):
        return "Nominal Optimization"
    if (
        "MULTIOBJECTIVE DYNAMIC SCREENING" in u
        or re.search(r"\bPHASE\s+3\b", u)
        or "DYNAMIC SCREENING" in u
    ):
        return "Dynamic Screening"
    if (
        "COMMERCIAL SCREENING" in u
        or re.search(r"\bPHASE\s+2\b", u)
        or "ROLLBEAR SCREENING" in u
        or "LUBRICATION SCREENING" in u
        or "BEARING PAIRS KEPT AFTER SCREENING" in u
    ):
        return "Commercial Screening"
    if (
        "USER INPUT DATA / BASELINE VALIDATION" in u
        or "BASELINE VALIDATION" in u
        or "PHASE 0/1" in u
        or re.search(r"\bPHASE\s+0-1\b", u)
    ):
        return "Baseline"
    return current


def completed_stages(current: str) -> list[str]:
    try:
        idx = STAGES.index(current)
    except ValueError:
        return []
    return STAGES[:idx]


def shell_display(cmd: Iterable[str]) -> str:
    def q(s: str) -> str:
        if re.search(r"[\s'\"]", s):
            return "'" + s.replace("'", "'\\''") + "'"
        return s
    return " ".join(q(str(x)) for x in cmd)


def child_environment() -> dict[str, str]:
    env = dict(os.environ)
    env.setdefault("PYTHONUNBUFFERED", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    return env
