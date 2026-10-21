"""Étape 6 : le rapport de contrôle."""
from donnees import LOT_A
from qualite import rapport


def test_entete():
    lignes = rapport(LOT_A).splitlines()
    assert lignes[0] == "Contrôle des axes : 25.00 ± 0.05 mm"
    assert lignes[1] == "Code        Mesure    Écart   Verdict"


def test_ligne_piece_alignee():
    lignes = rapport(LOT_A).splitlines()
    assert lignes[2] == "AXE-0001    25.020   +0.020   conforme"
    assert "AXE-0008    24.930   -0.070   rebut" in lignes


def test_bilan():
    texte = rapport(LOT_A)
    assert "Pièces : 10 | conformes : 8 (80.0%) | à reprendre : 1 | rebuts : 1" in texte
    assert "Cp = 0.42 | Cpk = 0.32 -> procédé NON capable" in texte


def test_rejets_listes_a_la_fin():
    lignes = rapport(LOT_A).splitlines()
    assert lignes[-4] == "Lignes rejetées : 3"
    assert lignes[-1] == "  ligne 15 : 2 champs attendus, 3 trouvé(s)"


def test_lot_sans_erreur_ni_capabilite():
    texte = rapport(["AXE-0001 ; 25,00"])
    assert "Pièces : 1 | conformes : 1 (100.0%)" in texte
    assert "Cp" not in texte
    assert "rejetées" not in texte


def test_autres_reglages():
    assert rapport(["ARB-0001 ; 12,04"], nominal=12.0, tolerance=0.1).startswith(
        "Contrôle des axes : 12.00 ± 0.10 mm")
