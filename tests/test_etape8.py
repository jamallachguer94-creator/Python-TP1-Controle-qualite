"""Étape 8 (à la maison) : l'histogramme."""
from qualite import histogramme


def test_histogramme_simple():
    texte = histogramme([25.0, 25.01, 25.03], debut=25.0, pas=0.02, nb_classes=2)
    assert texte == "[25.000 ; 25.020[ **\n[25.020 ; 25.040[ *"


def test_borne_haute_exclue():
    assert histogramme([25.02], debut=25.0, pas=0.02, nb_classes=1) == "[25.000 ; 25.020[ "


def test_hors_classes_ignorees():
    assert histogramme([20.0, 30.0], debut=25.0, pas=0.1, nb_classes=1) == "[25.000 ; 25.100[ "
