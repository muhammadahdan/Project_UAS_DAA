from rute.cli import main


def test_TC21_cli_skenario_valid(capsys):
    assert main(["--scenario", "S1", "--method", "held_karp"]) == 0
    out = capsys.readouterr().out
    assert "Total jarak" in out and "Depo Kemayoran" in out


def test_TC22_cli_skenario_tidak_ada(capsys):
    assert main(["--scenario", "S99"]) == 2


def test_TC23_cli_stops_tidak_valid_kode_keluar_2(capsys):
    assert main(["--stops", "3,999", "--method", "nn2opt"]) == 2
    assert "Input tidak valid" in capsys.readouterr().err
