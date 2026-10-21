"""Étape 5 : statistiques et capabilité du procédé."""
import statistics

import pytest

from qualite import capabilite, ecart_type, moyenne


def test_moyenne():
    assert moyenne(1, 2, 3, 4) == 2.5
    assert moyenne(7) == 7


def test_moyenne_avec_deballage():
    valeurs = [24.98, 25.02, 25.0]
    assert moyenne(*valeurs) == pytest.approx(25.0)


def test_moyenne_vide():
    with pytest.raises(ValueError):
        moyenne()


def test_ecart_type_comme_statistics():
    valeurs = [25.02, 24.98, 25.05, 25.01, 25.07]
    assert ecart_type(*valeurs) == pytest.approx(statistics.stdev(valeurs))


def test_ecart_type_trop_peu_de_valeurs():
    with pytest.raises(ValueError):
        ecart_type(25.0)


def test_capabilite_procede_capable():
    mesures = [25.00, 25.01, 24.99, 25.00, 25.01, 24.99]
    assert capabilite(mesures) == (1.86, 1.86)


def test_capabilite_procede_decentre():
    mesures = [25.03, 25.04, 25.02, 25.03, 25.04, 25.02]
    cp, cpk = capabilite(mesures)
    assert cp == 1.86
    assert cpk == 0.75        # même précision, mais mal centré : Cpk chute


def test_capabilite_reglages_nommes():
    assert capabilite([12.0, 12.1, 11.9], nominal=12.0, tolerance=0.3) == (1.0, 1.0)


def test_capabilite_ecart_type_nul():
    with pytest.raises(ValueError):
        capabilite([25.0, 25.0, 25.0])
