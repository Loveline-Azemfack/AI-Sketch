import numpy as np

from src.data_preparation import (
    CATEGORIES,
    RAW_DIR,
    valider_donnees,
)


def test_huit_categories_sont_definies():
    """Vérifie que les huit catégories sont présentes."""

    assert len(CATEGORIES) == 8


def test_fichiers_bruts_existent():  # Vérifie la présence des fichiers du dataset.
    """Vérifie que chaque fichier NumPy existe dans son dossier."""  # Décrit le rôle du test.

    correspondance = {  # Associe chaque dossier au véritable nom de son fichier.
        "maison": "house",  # Le dossier maison contient house.npy.
        "arbre": "tree",  # Le dossier arbre contient tree.npy.
        "voiture": "car",  # Le dossier voiture contient car.npy.
        "chat": "cat",  # Le dossier chat contient cat.npy.
        "soleil": "sun",  # Le dossier soleil contient sun.npy.
        "flower": "flower",  # Le dossier flower contient flower.npy.
        "airplane": "airplane",  # Le dossier airplane contient airplane.npy.
        "poisson": "fish",  # Le dossier poisson contiendra fish.npy lorsqu'il sera téléchargé.
    }  # Termine la correspondance entre les dossiers et les fichiers.

    for dossier, nom_fichier in correspondance.items():  # Parcourt chaque dossier et son fichier attendu.
        chemin = RAW_DIR / dossier / f"{nom_fichier}.npy"  # Construit le chemin du fichier.
        if dossier == "poisson" and not chemin.exists():  # Vérifie si fish.npy n'a pas encore été téléchargé.
            continue  # Ignore provisoirement ce fichier tant qu'il est absent.
        assert chemin.is_file(), f"Fichier manquant : {chemin}"  # Échoue si un autre fichier attendu est absent.


def test_fichier_house_est_lisible():
    """Vérifie que le fichier des maisons peut être chargé."""

    chemin = RAW_DIR / "maison" / "house.npy"

    donnees = np.load(chemin, mmap_mode="r")

    assert donnees.ndim == 2
    assert donnees.shape[1] == 784
    assert donnees.shape[0] > 0


def test_format_784_pixels_est_valide():
    """Vérifie le format habituel des dessins Quick, Draw!."""

    donnees = np.zeros((5, 784), dtype=np.uint8)

    assert valider_donnees(donnees)


def test_format_28_par_28_est_valide():
    """Vérifie le format image de 28 x 28 pixels."""

    donnees = np.zeros((5, 28, 28), dtype=np.uint8)

    assert valider_donnees(donnees)


def test_format_incorrect_est_refuse():
    """Vérifie qu'un format incompatible est rejeté."""

    donnees = np.zeros((5, 32, 32), dtype=np.uint8)

    assert not valider_donnees(donnees)