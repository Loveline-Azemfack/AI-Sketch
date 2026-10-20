"""
Tests d'intégration du programme principal AI-Sketch.
"""

import numpy as np
import pytest

from src import main as application


def test_reconnaissance_maison(monkeypatch):
    """
    Vérifie que le programme principal transmet correctement
    le dessin au module de reconnaissance.
    """

    # Création d'un dessin de test.
    image = np.zeros((64, 64, 3), dtype=np.uint8)

    # Résultat simulé du modèle.
    resultat_attendu = {
        "classe": "maison",
        "confiance": 0.95,
        "inconnu": False
    }

    # Fonction simulant le module de reconnaissance.
    def fausse_reconnaissance(image_recue):
        assert image_recue is image
        return resultat_attendu

    # Remplacement de la vraie fonction par la fonction simulée.
    monkeypatch.setattr(
        application,
        "recognize_drawing",
        fausse_reconnaissance
    )

    # Appel du programme principal.
    resultat = application.traiter_dessin(image)

    # Vérification du résultat.
    assert resultat["classe"] == "maison"
    assert resultat["confiance"] == 0.95
    assert resultat["inconnu"] is False


def test_image_absente():
    """
    Vérifie que le programme gère l'absence de dessin.
    """

    resultat = application.traiter_dessin(None)

    assert resultat["classe"] == "Aucun dessin"
    assert resultat["inconnu"] is True
    assert "erreur" in resultat


def test_erreur_du_module_de_reconnaissance(monkeypatch):
    """
    Vérifie que le programme principal gère une exception
    provenant du module de reconnaissance.
    """

    image = np.zeros((64, 64, 3), dtype=np.uint8)

    def fausse_reconnaissance(image_recue):
        raise RuntimeError("Erreur simulée du modèle")

    monkeypatch.setattr(
        application,
        "recognize_drawing",
        fausse_reconnaissance
    )

    resultat = application.traiter_dessin(image)

    assert resultat["classe"] == "Erreur"
    assert resultat["inconnu"] is True
    assert "erreur" in resultat


@pytest.mark.parametrize(
    "resultat_invalide",
    [
        None,
        "maison",
        {},
        {
            "classe": "maison",
            "confiance": 0.95
        },
        {
            "classe": "maison",
            "confiance": 1.5,
            "inconnu": False
        },
        {
            "classe": "maison",
            "confiance": 0.95,
            "inconnu": "non"
        }
    ]
)
def test_resultat_de_reconnaissance_invalide(
    monkeypatch,
    resultat_invalide
):
    """
    Vérifie que les résultats incorrects sont détectés.
    """

    image = np.zeros((64, 64, 3), dtype=np.uint8)

    def fausse_reconnaissance(image_recue):
        return resultat_invalide

    monkeypatch.setattr(
        application,
        "recognize_drawing",
        fausse_reconnaissance
    )

    resultat = application.traiter_dessin(image)

    assert resultat["classe"] == "Erreur"
    assert resultat["inconnu"] is True
    assert "erreur" in resultat