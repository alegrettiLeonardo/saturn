from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
import csv
import math


def _bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass"}


def _float(value: Any) -> float | None:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def _read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh)]


@dataclass(frozen=True)
class ResultSelection:
    population: list[dict[str, Any]]
    selected_rows: list[dict[str, Any]]
    baseline: dict[str, Any] | None
    selected: dict[str, Any] | None
    population_path: Path | None
    selected_path: Path | None


class ResultsRepository:
    """Small read-only adapter over SATURN's generated robust-search artifacts.

    The desktop UI consumes the same CSVs written by ``search_artifacts.py``.  It
    never recomputes objectives or invents design results when artifacts are absent.
    """

    def __init__(self, project: Any):
        self.project = project

    def _first_file(self, paths: Iterable[Path]) -> Path | None:
        return next((p for p in paths if p.is_file()), None)

    def population_path(self) -> Path | None:
        if hasattr(self.project, "existing_result_population"):
            p = self.project.existing_result_population()
            if p is not None:
                return p
        root = self.project.result_plot_dir()
        return self._first_file(
            [
                root / "plot_population.csv",
                self.project.report_dir() / "pareto_population.csv",
            ]
        )

    def selected_path(self) -> Path | None:
        root = self.project.result_plot_dir()
        rdir = self.project.report_dir()
        return self._first_file(
            [
                root / "plot_selected_solutions.csv",
                rdir / "00_decision_summary_comparison.csv",
                root / "00_decision_summary_comparison.csv",
            ]
        )

    def load(self) -> ResultSelection:
        pp = self.population_path()
        sp = self.selected_path()
        population = _read_csv(pp) if pp else []
        selected_rows = _read_csv(sp) if sp else []
        baseline = self._find_baseline(selected_rows)
        selected = self._find_preferred(selected_rows, population)
        return ResultSelection(population, selected_rows, baseline, selected, pp, sp)

    @staticmethod
    def _find_baseline(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
        for row in rows:
            tag = str(row.get("solution") or row.get("solution_tag") or "").strip().upper()
            if tag == "BASELINE":
                return row
        return None

    @staticmethod
    def _find_preferred(
        rows: list[dict[str, Any]], population: list[dict[str, Any]]
    ) -> dict[str, Any] | None:
        preferred_names = {"PREFERRED", "PREFERRED_FINAL", "COMPROMISE"}
        for row in rows:
            tag = str(row.get("solution") or row.get("solution_tag") or "").strip().upper()
            if tag in preferred_names:
                return row
        for row in population:
            tag = str(row.get("solution_tag") or "").strip().upper()
            if tag in preferred_names:
                return row
        # Do not manufacture an "optimal" solution.  When a robust search has not
        # emitted a semantic preferred candidate, show the first Pareto candidate as
        # a selected candidate only.
        for row in population:
            if _bool(row.get("is_pareto")):
                return row
        return population[0] if population else None

    @staticmethod
    def status(row: dict[str, Any]) -> str:
        tag = str(row.get("solution_tag") or row.get("solution") or "").strip().upper()
        if tag in {"PREFERRED", "PREFERRED_FINAL", "COMPROMISE"}:
            return "Preferred"
        if not _bool(row.get("robust_feasible", True)):
            return "Infeasible"
        if _bool(row.get("is_pareto")):
            return "Pareto"
        return "Feasible"

    @staticmethod
    def candidate_id(row: dict[str, Any], fallback: str = "—") -> str:
        return str(row.get("individual_id") or row.get("solution") or row.get("solution_tag") or fallback)

    @staticmethod
    def numeric(row: dict[str, Any] | None, key: str) -> float | None:
        if row is None:
            return None
        return _float(row.get(key))

    @staticmethod
    def critical_rpm(row: dict[str, Any] | None) -> float | None:
        hz = ResultsRepository.numeric(row, "critical_1_hz")
        return None if hz is None else 60.0 * hz

    @staticmethod
    def selected_metrics(row: dict[str, Any] | None) -> dict[str, tuple[float | None, str]]:
        return {
            "F1": (ResultsRepository.numeric(row, "F1_um"), "µm"),
            "CRIT": (ResultsRepository.critical_rpm(row), "rpm"),
            "F2": (
                None
                if ResultsRepository.numeric(row, "F2_N") is None
                else ResultsRepository.numeric(row, "F2_N") / 1000.0,
                "kN",
            ),
            "F3": (ResultsRepository.numeric(row, "F3"), "—"),
        }

    @staticmethod
    def percent_delta(current: float | None, baseline: float | None) -> float | None:
        if current is None or baseline is None or baseline == 0:
            return None
        return 100.0 * (current - baseline) / abs(baseline)

    @staticmethod
    def design_numeric_columns(rows: list[dict[str, Any]]) -> list[str]:
        if not rows:
            return []
        reserved = {
            "individual_id", "bearing_DE", "bearing_NDE", "F1_um", "F2_N", "F3",
            "rotor_mass_kg", "critical_1_hz", "is_pareto", "robust_feasible",
            "solution", "solution_tag", "governing_scenario", "max_utilization_pct",
        }
        out: list[str] = []
        for key in rows[0].keys():
            if key in reserved:
                continue
            vals = [_float(r.get(key)) for r in rows[:25]]
            if any(v is not None for v in vals):
                out.append(key)
        return out


__all__ = ["ResultSelection", "ResultsRepository"]
