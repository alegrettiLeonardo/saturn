from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOCKUPS = ROOT / "mockups"


def test_saturn_html_mockups_are_self_contained_and_present():
    names = ["index.html", "project_setup.html", "optimization_results.html", "run_analysis.html", "saturn.css", "shared.js"]
    for name in names:
        path = MOCKUPS / name
        assert path.is_file(), name
        text = path.read_text(encoding="utf-8")
        assert "https://" not in text
        assert "http://" not in text


def test_project_mockup_is_bound_to_reviewed_w60f_topology():
    text = (MOCKUPS / "project_setup.html").read_text(encoding="utf-8")
    assert "W60F_450_2000kW_2P" in text
    assert "2175.5" in text
    assert "FREE_TRANSITION A" in text
    assert "294.13 MN/m" in text


def test_results_mockup_declares_illustrative_result_values():
    text = (MOCKUPS / "optimization_results.html").read_text(encoding="utf-8")
    assert "values are illustrative" in text
