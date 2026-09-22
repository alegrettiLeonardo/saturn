from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import tomllib

try:
    import yaml
except Exception:  # pragma: no cover - optional at GUI model import time
    yaml = None

from shaftopt_coupled.baseline_case import BaselineCase
from shaftopt_coupled.coupled_evaluator import CoupledEvaluator


DEFAULT_CASE_TOML = Path("cases/w60f_user_baseline/shaftopt_case.toml")
DEFAULT_OPT_CONFIG = Path("cases/w60f_450_2mw_3obj.json")
DEFAULT_BEARING_CATALOG = Path("data/bearings/w60_multisupplier_catalog.json")


@dataclass(frozen=True)
class ProjectSummary:
    project_id: str
    case_id: str
    description: str
    machine: str
    power_kw: float | None
    rated_rpm: float
    rotor_length_m: float
    section_count: int
    disk_count: int
    bearing_count: int
    objective: str
    strategy: str
    version: str


class SaturnProject:
    """Read-only view of the active shaftOpt project used by the desktop UI.

    The class does not alter native decks.  It materializes the same computational
    topology used by the coupled evaluator so that the desktop geometry view and
    design-variable table stay synchronized with the optimizer.
    """

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self.case_toml = (self.root / DEFAULT_CASE_TOML).resolve()
        self.config_json = (self.root / DEFAULT_OPT_CONFIG).resolve()
        self.catalog_json = (self.root / DEFAULT_BEARING_CATALOG).resolve()
        self.baseline = BaselineCase.from_toml(self.case_toml)
        self.config: dict[str, Any] = json.loads(self.config_json.read_text(encoding="utf-8"))
        self.evaluator = CoupledEvaluator.from_files(
            self.baseline.rotordin.path,
            self.config_json,
            rotordin_executable=self.baseline.executables.rotordin,
            bearing_catalog_path=self.catalog_json,
            rollbear_executable=self.baseline.executables.rollbear,
            flextor_executable=self.baseline.executables.flextor,
            keyway2_executable=self.baseline.executables.keyway2,
        )
        self.config = self.evaluator.config
        self.case = self.evaluator.base_case

    @property
    def summary(self) -> ProjectSummary:
        cid = self.baseline.case_id
        project_id = cid.removesuffix("_user_baseline")
        power_kw = self._power_from_project_id(project_id)
        machine = self._machine_from_project_id(project_id)
        objective = "Otimização robusta 3 objetivos"
        strategy = "SOBOL → DE → COBYQA → ROBUST → FINE"
        return ProjectSummary(
            project_id=project_id,
            case_id="user_baseline",
            description=self.baseline.description,
            machine=machine,
            power_kw=power_kw,
            rated_rpm=float(self.case.rated_rpm),
            rotor_length_m=float(self.case.length),
            section_count=len(self.case.sections),
            disk_count=len(self.case.disks),
            bearing_count=len(self.case.bearings),
            objective=objective,
            strategy=strategy,
            version="V22",
        )

    @staticmethod
    def _power_from_project_id(project_id: str) -> float | None:
        for token in project_id.split("_"):
            low = token.lower()
            if low.endswith("kw"):
                try:
                    return float(token[:-2])
                except ValueError:
                    return None
        return None

    @staticmethod
    def _machine_from_project_id(project_id: str) -> str:
        if project_id.upper().startswith("W60F"):
            return "Motor W60F"
        return project_id.split("_")[0]

    @property
    def module_rows(self) -> list[tuple[str, str, Path, str]]:
        roll = self.baseline.rollbear[0].path if self.baseline.rollbear else Path("")
        rows = [
            ("RotorDin", self.baseline.rotordin.path.name, self.baseline.rotordin.path, "Válido"),
            ("RollBear", roll.name, roll, "Válido"),
            ("Flextor", self.baseline.flextor.path.name, self.baseline.flextor.path, "Válido"),
            ("Keyway2", self.baseline.keyway2.path.name, self.baseline.keyway2.path, "Válido"),
            ("Configuração", self.case_toml.name, self.case_toml, "Válido"),
        ]
        return rows

    @property
    def design_variables(self) -> list[dict[str, Any]]:
        base = self.evaluator.base_design()
        out: list[dict[str, Any]] = []
        for spec in self.evaluator.design_variable_spec():
            row = dict(spec)
            row["current"] = base.get(spec["name"], spec.get("initial"))
            out.append(row)
        return out

    @property
    def objective_rows(self) -> list[dict[str, str]]:
        return [
            {"name": "F1", "description": "Resposta dinâmica normalizada ao desbalanceamento", "unit": "µm", "sense": "Minimizar"},
            {"name": "F2", "description": "Força dinâmica transmitida aos mancais/suportes", "unit": "N", "sense": "Minimizar"},
            {"name": "F3", "description": "Sensibilidade às incertezas (robustez)", "unit": "-", "sense": "Minimizar"},
        ]

    @property
    def constraint_rows(self) -> list[dict[str, str]]:
        c = self.config.get("constraints", {}) or {}
        rows: list[dict[str, str]] = []
        mapping = [
            ("max_deflection_airgap_ratio", "Deflexão lateral / entreferro", "≤", "0.05", "ratio"),
            ("minimum_static_safety_factor", "Fator de segurança estático", "≥", None, "-"),
            ("minimum_fatigue_safety_factor", "Fator de segurança à fadiga", "≥", None, "-"),
            ("required_l10m_h", "Vida L10m dos rolamentos", "≥", None, "h"),
            ("max_bearing_temperature_c", "Temperatura máxima do rolamento", "≤", None, "°C"),
            ("allowable_stress_pa", "Tensão admissível", "≤", None, "Pa"),
            ("allowable_slope_rad", "Inclinação admissível", "≤", None, "rad"),
            ("allowable_twist_rad", "Torção admissível", "≤", None, "rad"),
        ]
        for key, label, op, fallback, unit in mapping:
            val = c.get(key)
            if val is None:
                if fallback is None:
                    continue
                val = fallback
            rows.append({"name": key, "description": label, "operator": op, "limit": str(val), "unit": unit})
        shoulder = self.config.get("bearing_shoulder_validation", {}) or {}
        if shoulder.get("enabled"):
            mm = 1000.0 * float(shoulder.get("minimum_axial_clearance_m", 0.03))
            rows.append({
                "name": "bearing_shoulder_axial",
                "description": "Folga axial mínima do encosto do mancal",
                "operator": "≥",
                "limit": f"{mm:.1f}",
                "unit": "mm",
            })
        return rows

    @property
    def uncertainty_rows(self) -> list[dict[str, Any]]:
        model = self.config.get("uncertainty_model", {}) or {}
        if not model.get("enabled"):
            return []
        path = model.get("definition")
        if not path or yaml is None:
            return []
        p = (self.root / str(path)).resolve()
        if not p.is_file():
            return []
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        rows: list[dict[str, Any]] = []
        candidates = []
        for key in ("uncertainties", "parameters", "variables"):
            if isinstance(data.get(key), list):
                candidates = data[key]
                break
        for item in candidates:
            if isinstance(item, dict):
                rows.append(dict(item))
        return rows

    @property
    def workflow(self) -> dict[str, Any]:
        return dict((self.config.get("optimization", {}) or {}).get("workflow", {}) or {})

    @property
    def machine_data(self) -> dict[str, Any]:
        """Engineering metadata used by the desktop project summary.

        Values are read from the authoritative W60F configuration/deck.  The GUI
        intentionally does not invent missing project data.
        """
        iface = self.config.get("rotordin_interface", {}) or {}
        dyn = self.config.get("dynamic_criteria", {}) or {}
        summary = self.summary
        return {
            "machine_type": summary.machine,
            "rated_power_kw": summary.power_kw,
            "rated_speed_rpm": float(iface.get("NWT_RTD_RATED_SPEED_rpm", self.case.rated_rpm)),
            "number_of_poles": iface.get("NWT_RTD_POLES"),
            "grid_frequency_hz": iface.get("NWT_RTD_FN_Hz", dyn.get("grid_frequency_hz")),
            "airgap_mm": iface.get("NWT_RTD_AIRGAP_mm"),
            "rotor_length_mm": 1000.0 * float(self.case.length),
            "critical_speed_min_rpm": dyn.get("minimum_critical_speed_rpm"),
            "critical_frequency_min_hz": dyn.get("minimum_critical_frequency_hz"),
        }

    def section_role(self, index_1based: int) -> str:
        protected = {
            int(x.get("shoulder_section")): f"{x.get('support', '')} bearing shoulder"
            for x in (self.config.get("protected_bearing_shoulders", []) or [])
            if x.get("shoulder_section") is not None
        }
        transitions = {
            int(x.get("transition_section")): f"{x.get('support', '')} free transition"
            for x in (self.config.get("bearing_shoulder_transition_generation", {}) or {}).get("generated_transitions", []) or []
            if x.get("transition_section") is not None
        }
        fan_sections: dict[int, str] = {}
        for spec in self.evaluator.design_variable_spec():
            if spec.get("component_role") == "fan_hub_seat_length" and spec.get("section") is not None:
                fan_sections[int(spec["section"])] = str(spec.get("component_label") or "Fan hub seat")
        bearing_seats = {int(x) for x in (self.config.get("bearing_seat_sections", []) or [])}
        if index_1based in protected:
            return protected[index_1based]
        if index_1based in transitions:
            return transitions[index_1based]
        if index_1based in fan_sections:
            return fan_sections[index_1based]
        if index_1based in bearing_seats:
            return "Bearing seat"
        sec = self.case.sections[index_1based - 1]
        start = self.case.section_start(index_1based - 1)
        stack_specs = [x for x in self.evaluator.design_variable_spec() if x.get("component_role") == "rotor_stack_axial_position"]
        if stack_specs:
            st = float(stack_specs[0].get("package_start_m", -1.0))
            en = float(stack_specs[0].get("package_end_m", -1.0))
            if start <= st and float(sec.end) >= en:
                return "Rotor active region"
        return "Shaft section"

    @property
    def section_rows(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        variable_sections: set[int] = set()
        variable_lengths: set[int] = set()
        for spec in self.evaluator.design_variable_spec():
            if spec.get("variable_kind") == "section_diameter":
                variable_sections.update(int(x) for x in spec.get("sections", []) or [])
            if spec.get("variable_kind") == "section_length" and spec.get("section") is not None:
                variable_lengths.add(int(spec["section"]))
        for i, sec in enumerate(self.case.sections, 1):
            start = float(self.case.section_start(i - 1))
            end = float(sec.end)
            rows.append({
                "index": i,
                "label": self.section_role(i),
                "start_mm": 1000.0 * start,
                "end_mm": 1000.0 * end,
                "length_mm": 1000.0 * (end - start),
                "outer_diameter_mm": 1000.0 * float(sec.outer_diameter),
                "inner_diameter_mm": 1000.0 * float(getattr(sec, "inner_diameter", 0.0)),
                "young_pa": float(getattr(sec, "young", 0.0)),
                "density_kg_m3": float(getattr(sec, "density", 0.0)),
                "diameter_variable": i in variable_sections,
                "length_variable": i in variable_lengths,
            })
        return rows

    @property
    def bearing_rows(self) -> list[dict[str, Any]]:
        cfg = self.config.get("baseline_bearings", []) or []
        rows: list[dict[str, Any]] = []
        for i, b in enumerate(self.case.bearings, 1):
            meta = cfg[i - 1] if i - 1 < len(cfg) and isinstance(cfg[i - 1], dict) else {}
            designation = meta.get("commercial_designation") or meta.get("id") or "—"
            rows.append({
                "support": "DE" if i == 1 else "NDE" if i == 2 else f"B{i}",
                "position_mm": 1000.0 * float(b.position),
                "type": "Deep groove ball" if designation != "—" else "Bearing",
                "model": str(designation),
                "kxx_n_m": float(b.kxx),
                "kzz_n_m": float(b.kzz),
                "cxx_n_s_m": float(b.cxx),
                "czz_n_s_m": float(b.czz),
                "width_mm": None if meta.get("width_m") is None else 1000.0 * float(meta["width_m"]),
            })
        return rows

    @property
    def results_candidates(self) -> list[Path]:
        """Known robust-search population files, newest naming first."""
        r = self.report_dir()
        p = self.result_plot_dir()
        return [
            p / "plot_population.csv",
            r / "pareto_population.csv",
            r / "optimization_population.csv",
            self.root / "results/robust_3obj/robust_pareto_population.csv",
        ]

    def existing_result_population(self) -> Path | None:
        return next((p for p in self.results_candidates if p.is_file()), None)

    def result_plot_dir(self, smoke: bool = False) -> Path:
        base = self.root / ("results/robust_3obj_smoke" if smoke else "results/robust_3obj")
        return base / "reports/plots"

    def report_dir(self, smoke: bool = False) -> Path:
        base = self.root / ("results/robust_3obj_smoke" if smoke else "results/robust_3obj")
        return base / "reports"

    def validate_paths(self) -> list[str]:
        problems: list[str] = []
        for _, _, path, _ in self.module_rows:
            if not path.is_file():
                problems.append(f"Arquivo ausente: {path}")
        for name, exe in self.baseline.executables.as_dict().items():
            p = Path(exe)
            if not p.is_file():
                problems.append(f"Executável {name} ausente: {p}")
        return problems


def read_project_toml(path: str | Path) -> dict[str, Any]:
    return tomllib.loads(Path(path).read_text(encoding="utf-8"))
