"""Étape 2 : l'écart et le verdict."""
import pytest

from qualite import ecart, verdict


def test_ecart_arrondi():
    assert ecart(25.05) == 0.05            # et non 0.05000000000000071
    assert ecart(24.93) == -0.07


def test_ecart_autre_nominal():
    assert ecart(12.04, nominal=12.0) == 0.04


def test_conforme():
    assert verdict(25.02) == "conforme"
    assert verdict(24.98) == "conforme"
    assert verdict(25.0) == "conforme"


def test_limites_incluses():
    # le piège des flottants : sans arrondi, 25.05 serait refusé
    assert verdict(25.05) == "conforme"
    assert verdict(24.95) == "conforme"


def test_trop_gros_a_reprendre():
    assert verdict(25.07) == "à reprendre"


def test_trop_petit_rebut():
    assert verdict(24.93) == "rebut"


def test_autres_reglages():
    assert verdict(12.04, 12.0, 0.1) == "conforme"
    assert verdict(12.04, nominal=12.0, tolerance=0.01) == "à reprendre"


@pytest.mark.parametrize("tolerance", [0, -0.05])
def test_tolerance_invalide(tolerance):
    with pytest.raises(ValueError):
        verdict(25.0, 25.0, tolerance)
