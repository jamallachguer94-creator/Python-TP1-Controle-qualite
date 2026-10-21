"""Étape 4 : analyser un lot sans s'arrêter à la première erreur."""
from donnees import LOT_A
from qualite import analyser_lot, compter_verdicts

PETIT_LOT = [
    "# commentaire",
    "AXE-0001 ; 25,02",
    "",
    "AXE-0002 ; abc",
    "AXE-0003 ; 25,09",
    "AXE-04 ; 25,00",
]


def test_resultats_valides():
    resultats, _ = analyser_lot(PETIT_LOT)
    assert resultats == [("AXE-0001", 25.02, "conforme"), ("AXE-0003", 25.09, "à reprendre")]


def test_erreurs_numerotees():
    _, erreurs = analyser_lot(PETIT_LOT)
    assert erreurs == ["ligne 4 : mesure invalide : 'abc'", "ligne 6 : code invalide : 'AXE-04'"]


def test_reglages_transmis():
    resultats, _ = analyser_lot(["AXE-0003 ; 25,09"], tolerance=0.1)
    assert resultats == [("AXE-0003", 25.09, "conforme")]


def test_lot_vide():
    assert analyser_lot([]) == ([], [])


def test_lot_a():
    resultats, erreurs = analyser_lot(LOT_A)
    assert len(resultats) == 10
    assert len(erreurs) == 3


def test_la_liste_recue_n_est_pas_modifiee():
    copie = list(PETIT_LOT)
    analyser_lot(PETIT_LOT)
    assert PETIT_LOT == copie


def test_compter_verdicts():
    resultats, _ = analyser_lot(LOT_A)
    assert compter_verdicts(resultats) == (8, 1, 1)
    assert compter_verdicts([]) == (0, 0, 0)
