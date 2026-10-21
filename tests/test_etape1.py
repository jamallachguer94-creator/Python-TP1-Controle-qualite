"""Étape 1 : lire une mesure et valider un code pièce."""
import pytest

from qualite import lire_mesure, valider_code


def test_virgule_et_unite():
    assert lire_mesure("25,03 mm") == 25.03


def test_espaces_autour():
    assert lire_mesure("   24,98 mm  ") == 24.98


def test_point_et_unite_collee():
    assert lire_mesure("25.1mm") == 25.1
    assert lire_mesure("25.1") == 25.1


def test_majuscules_dans_l_unite():
    assert lire_mesure("25,00 MM") == 25.0


@pytest.mark.parametrize("texte", ["abc", "", "mm", "ERREUR CAPTEUR", "-3", "0", "nan", "inf"])
def test_mesure_invalide(texte):
    with pytest.raises(ValueError):
        lire_mesure(texte)


def test_message_clair():
    with pytest.raises(ValueError, match="mesure invalide : 'abc'"):
        lire_mesure(" abc ")


@pytest.mark.parametrize("code", ["AXE-0001", "ABC-9999", "ZZZ-0000"])
def test_code_valide(code):
    assert valider_code(code) is True


@pytest.mark.parametrize("code", ["AXE-010", "AXE-00011", "axe-0001", "AX1-0001", "AXE_0001", "AXE-00A1", "",
                                  "ÉTÉ-0001"])
def test_code_invalide(code):
    assert valider_code(code) is False
