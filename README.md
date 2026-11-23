# SATURN

Shaft Analysis, Tuning & Unified Rotordynamics Navigator.

This repository is being initialized from the reviewed SATURN solver package and desktop-interface implementation.


## SATURN Desktop

A desktop engineering interface is available in `saturn_gui/`. It is intentionally an orchestration/presentation layer over the existing SATURN/shaftOpt scientific workflow: it reads the same canonical case/configuration, launches the existing solver targets, consumes real generated artifacts, and does not replace the validated numerical kernel.

### Quick check

```bash
python scripts/run_saturn_gui.py --project-root . --check
```

### Launch the desktop interface

```bash
python scripts/run_saturn_gui.py --project-root .
```

The interface contains the approved project-oriented workspaces:

- Project Setup and longitudinal rotor configuration;
- Rotor Model, Bearings and native Loads;
- Optimization objectives, constraints and design variables;
- Optimization Results with Pareto/candidate comparison;
- Run Analysis with asynchronous execution, live stdout/stderr, progress and report/output actions.

### Native solver executables

Runtime execution expects the native tools referenced by the active case (RotorDin, RollBear, Flextor and Keyway2). Local native build outputs are deliberately ignored by Git. Build or place the validated executables under the paths defined by the case configuration before starting a real coupled run.

### Engineering traceability

The GUI does not synthesize scientific results. Missing/not-yet-calculated responses are displayed as unavailable, while computed KPIs and plots are loaded from SATURN result artifacts. The supplied W60F baseline currently contains zero bearing damping; critical-speed/Campbell studies remain meaningful, but absolute resonance-response certification requires physically justified damping or a bounded uncertainty model.

## Approved SATURN visual refresh — 2026-11-23

The desktop shell has been aligned with the approved SATURN Project Setup, Optimization Results and Run Analysis references while preserving the existing scientific adapters and native solver ownership.

HTML reference mockups are available at:

- `mockups/index.html`
- `mockups/project_setup.html`
- `mockups/optimization_results.html`
- `mockups/run_analysis.html`

The implementation audit and engineering constraints are documented in `docs/SATURN_UI_SOLVER_AUDIT_20261123.md`.
