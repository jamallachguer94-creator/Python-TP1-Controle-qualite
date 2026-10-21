"""Étape 3 : analyser une ligne complète."""
import pytest

from qualite import analyser_ligne


def test_ligne_normale():
    assert analyser_ligne("AXE-0042 ; 25,03 mm") == ("AXE-0042", 25.03, "conforme")


def test_code_remis_en_majuscules():
    assert analyser_ligne("axe-0004;25,01mm") == ("AXE-0004", 25.01, "conforme")


def test_verdicts():
    assert analyser_ligne("AXE-0005 ; 25,07 mm")[2] == "à reprendre"
    assert analyser_ligne("AXE-0008 ; 24,93 mm")[2] == "rebut"


def test_reglages_nommes():
    assert analyser_ligne("ARB-0001 ; 12,04", nominal=12.0, tolerance=0.1) == ("ARB-0001", 12.04, "conforme")


def test_reglages_obligatoirement_nommes():
    with pytest.raises(TypeError):
        analyser_ligne("ARB-0001 ; 12,04", 12.0, 0.1)


@pytest.mark.parametrize("ligne, morceau", [
    ("AXE-0042 25,03", "2 champs attendus, 1 trouvé"),
    ("AXE-0042 ; 25,03 ; mm", "2 champs attendus, 3 trouvé"),
    ("AXE-042 ; 25,03", "code invalide : 'AXE-042'"),
    ("AXE-0042 ; abc", "mesure invalide : 'abc'"),
])
def test_lignes_invalides(ligne, morceau):
    with pytest.raises(ValueError, match=morceau):
        analyser_ligne(ligne)
