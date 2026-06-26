"""Tests for council.py module (38 geniuses, 5 guardians, 7 questions)."""
import council


def test_total_geniuses_is_38():
    assert len(council.get_all_geniuses()) == 38


def test_geniuses_have_required_fields():
    for g in council.get_all_geniuses():
        assert "id" in g
        assert "name" in g
        assert "expertise" in g
        assert "domain" in g
        assert g["id"].startswith("AG")


def test_eight_domains():
    domains = council.list_domains()
    assert len(domains) == 8
    assert sum(domains.values()) == 38


def test_guardians_count():
    assert len(council.GUARDIANS) == 5
    guardian_ids = {g["id"] for g in council.GUARDIANS}
    assert guardian_ids == {"Architecture", "Simplicity", "Security", "Quality", "Documentation"}


def test_security_guardian_has_veto():
    security = next(g for g in council.GUARDIANS if g["id"] == "Security")
    assert any("VETO" in check for check in security["checks"])


def test_devils_advocate_has_7_questions():
    assert len(council.DEVILS_ADVOCATE_QUESTIONS) == 7


def test_get_relevant_security():
    results = council.get_relevant_geniuses("security")
    assert len(results) > 0
    domains = {d for _, d in results}
    assert "seguranca_privacidade" in domains


def test_get_relevant_ux():
    results = council.get_relevant_geniuses("ux design")
    assert len(results) > 0
    domains = {d for _, d in results}
    assert "ux_ui_design" in domains


def test_get_relevant_unknown_topic_returns_software():
    results = council.get_relevant_geniuses("foobar random")
    assert len(results) > 0
    domains = {d for _, d in results}
    assert "engenharia_software" in domains


def test_get_relevant_returns_at_most_7():
    results = council.get_relevant_geniuses("react api security")
    assert len(results) <= 7
    assert len(results) > 0


def test_get_geniuses_by_domain_valid():
    g = council.get_geniuses_by_domain("ux_ui_design")
    assert len(g) == 8


def test_get_geniuses_by_domain_invalid_returns_empty():
    assert council.get_geniuses_by_domain("invalid") == []
