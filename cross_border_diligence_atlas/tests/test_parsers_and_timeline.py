from crossborder_dd.argentina_rns_parser import normalize_cuit
from crossborder_dd.brazil_cnpj_parser import normalize_cnpj
from crossborder_dd.brazil_sanctions_screen import screen_sanctions
from crossborder_dd.gazette_timeline_builder import build_timeline


def test_identifier_normalizers():
    assert normalize_cnpj("11.222.333/0001-81") == "11222333000181"
    assert normalize_cuit("20-12345678-6") == "20123456786"


def test_sanctions_screen_exact_identifier_lead():
    subjects = [{"cnpj": "11.222.333/0001-81", "name": "Empresa Sintetica Brasil Ltda"}]
    sanctions = [{"cnpj": "11222333000181", "name": "Other", "sanction_type": "synthetic"}]
    leads = screen_sanctions(subjects, sanctions)
    assert leads[0]["match_type"] == "exact_identifier"
    assert "Lead only" in leads[0]["limitation"]


def test_build_timeline_sorts_dates():
    rows = [
        {"event_date": "2026-02-10", "entity_name": "Sociedad Sintetica Argentina SA"},
        {"event_date": "2026-01-15", "entity_name": "Sociedad Sintetica Argentina SA"},
    ]
    timeline = build_timeline(rows, "Sociedad Sintetica Argentina SA")
    assert [event["event_date"] for event in timeline] == ["2026-01-15", "2026-02-10"]
