from crossborder_dd.normalize_names import normalize_identifier, normalize_name


def test_normalize_name_removes_accents_and_punctuation():
    assert normalize_name("Companhia Sao Joao, S.A.") == "companhia sao joao s a"


def test_normalize_identifier_keeps_digits_only():
    assert normalize_identifier("11.222.333/0001-81") == "11222333000181"
