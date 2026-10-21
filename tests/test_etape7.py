"""Étape 7 : le programme principal et ses commandes."""
from main import executer


def test_mesure_valide(capsys):
    saisies = []
    assert executer("mesure AXE-0100 25,04", saisies) is True
    assert capsys.readouterr().out == "AXE-0100 : 25.040 mm -> conforme\n"
    assert len(saisies) == 1


def test_mesure_refusee(capsys):
    saisies = []
    executer("mesure AXE-01 25", saisies)
    assert capsys.readouterr().out == "Refusé : code invalide : 'AXE-01'\n"
    assert saisies == []


def test_lot(capsys):
    executer("lot", [])
    assert capsys.readouterr().out.startswith("Contrôle des axes")


def test_aide(capsys):
    executer("aide", [])
    assert "quitter" in capsys.readouterr().out


def test_commande_inconnue(capsys):
    assert executer("bonjour", []) is True
    assert "Commande inconnue" in capsys.readouterr().out


def test_mesure_sans_valeur(capsys):
    executer("mesure AXE-0100", [])
    assert "Commande inconnue" in capsys.readouterr().out


def test_quitter(capsys):
    assert executer("quitter", ["a", "b"]) is False
    assert capsys.readouterr().out == "2 pièce(s) contrôlée(s) à la main. Au revoir.\n"
