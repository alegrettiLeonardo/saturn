# SATURN — solver/UI audit for desktop interface

Date: 2026-11-23

## Scope

Review of the supplied `SATURN(1).zip` before applying the approved desktop UI reference screens.
The objective is explicitly **not** to move or duplicate the validated mechanics in the GUI.

## Scientific architecture found

The package is self-contained and already has the correct separation for a desktop UI:

- Fortran shaft optimizer in `src/` and `bin/shaftopt`;
- coupled Python orchestration in `shaftopt_coupled/`;
- vendored native solvers under `external/` (RotorDin, RollBear, Flextor and Keyway2);
- canonical W60F case/configuration under `cases/`;
- engineering data under `data/`;
- campaign/report scripts under `scripts/`;
- desktop presentation package under `saturn_gui/`.

The current GUI model constructs the same scientific evaluator used by the coupled workflow:

`SaturnProject -> BaselineCase -> CoupledEvaluator.from_files(...) -> base_case/design_variable_spec()`

Execution is also correctly delegated to the existing validated workflow:

`GUI -> ExecutionConfig -> make robust-3obj-* -> existing scripts/native solvers -> result artifacts`

Therefore the interface can be refactored without changing the solver equations.

## W60F topology actually loaded

`python scripts/run_saturn_gui.py --check` reports:

- project: `W60F_450_2000kW_2P`;
- 11 computational shaft sections;
- 10 disks;
- 2 bearings;
- 5 active continuous design variables;
- required paths/executables: valid in the supplied package.

The five current design variables are:

1. rotor-stack axial position;
2. free transition diameter A;
3. free transition diameter B;
4. DE fan-hub seat length;
5. NDE fan-hub seat length.

The protected bearing shoulders are not design variables. This must remain visible in the GUI.

## UI-specific findings

### F-UI-01 — current scientific separation is correct

The GUI does not need to reproduce stress, deflection, critical-speed, bearing or optimization calculations.
Keep `CoupledEvaluator` and native executables authoritative.

### F-UI-02 — current desktop shell does not match the approved SATURN visual identity

The supplied Tk/ttk application is functional but its shell, sidebar, hierarchy, cards and result/run pages differ substantially from the approved screens. Refactoring is presentation-level and is safe if the existing model/execution adapters remain intact.

### F-UI-03 — project model is currently tied to one default W60F manifest

`SaturnProject` uses fixed defaults for the W60F case TOML, optimization JSON and bearing catalogue. The scientific evaluator is more general than this desktop project loader. The visual refactor must not introduce additional W60F assumptions; a later project-loader refactor should expose those paths through a project manifest/open-project workflow.

### F-UI-04 — missing results must remain missing

The supplied package does not contain a completed `results/robust_3obj/reports/plots` campaign. The production desktop application must show `— / not calculated` until real solver artifacts exist. The HTML result screen is therefore a visual mockup only.

### F-UI-05 — zero damping in the loaded rolling-bearing baseline is visible in the model

The baseline bearing records loaded by the desktop model contain zero damping. The GUI must not manufacture damping values or imply certified absolute resonance amplitudes from placeholder values.

## Implementation rule

The desktop interface is an orchestration/presentation layer only. The refactor may:

- restyle and reorganize the screens;
- draw the rotor from `base_case`;
- display project/configuration data;
- launch the existing make targets asynchronously;
- stream actual stdout/stderr;
- read the existing result CSV/HTML/PNG/report artifacts.

It must not:

- duplicate the mechanics in Python widgets;
- overwrite native input decks silently;
- substitute mock result values in normal operation;
- reinterpret protected shaft topology as optimizable geometry.
