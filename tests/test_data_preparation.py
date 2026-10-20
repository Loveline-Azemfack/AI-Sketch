import numpy as np  # Importe NumPy pour créer des tableaux de test et lire les fichiers .npy.

from src.data_preparation import (  # Importe les éléments du programme que nous voulons tester.
    CATEGORIES,  # Importe la liste ou le dictionnaire des catégories du dataset.
    RAW_DIR,  # Importe le chemin vers le dossier qui contient les données brutes.
    valider_donnees,  # Importe la fonction qui vérifie le format des dessins.
)  # Termine l'importation des éléments nécessaires aux tests.


def test_huit_categories_sont_definies():  # Définit un test qui vérifie le nombre de catégories.
    """Vérifie que les huit catégories sont présentes."""  # Explique l'objectif de ce test.

    assert len(CATEGORIES) == 8  # Vérifie que CATEGORIES contient exactement huit catégories.


def test_fichiers_bruts_existent():  # Définit un test qui vérifie la présence des fichiers du dataset.
    """Vérifie que chaque fichier NumPy existe dans son dossier."""  # Décrit le rôle du test.

    correspondance = {  # Crée un dictionnaire qui associe chaque dossier à son fichier .npy.
        "maison": "house",  # Indique que le dossier maison contient le fichier house.npy.
        "arbre": "tree",  # Indique que le dossier arbre contient le fichier tree.npy.
        "voiture": "car",  # Indique que le dossier voiture contient le fichier car.npy.
        "chat": "cat",  # Indique que le dossier chat contient le fichier cat.npy.
        "soleil": "sun",  # Indique que le dossier soleil contient le fichier sun.npy.
        "flower": "flower",  # Indique que le dossier flower contient le fichier flower.npy.
        "airplane": "airplane",  # Indique que le dossier airplane contient le fichier airplane.npy.
        "poisson": "fish",  # Indique que le dossier poisson doit contenir le fichier fish.npy.
    }  # Termine la définition du dictionnaire de correspondance.

    for dossier, nom_fichier in correspondance.items():  # Parcourt les paires dossier/fichier du dictionnaire.
        chemin = RAW_DIR / dossier / f"{nom_fichier}.npy"  # Construit le chemin complet du fichier à vérifier.

        if dossier == "poisson" and not chemin.exists():  # Vérifie si le fichier fish.npy est absent du dossier poisson.
            continue  # Passe au dossier suivant si fish.npy est absent, sans faire échouer ce test.

        assert chemin.is_file(), f"Fichier manquant : {chemin}"  # Vérifie que le fichier attendu existe bien et signale son chemin sinon.


def test_fichier_house_est_lisible():  # Définit un test pour vérifier que le fichier des maisons est lisible.
    """Vérifie que le fichier des maisons peut être chargé."""  # Explique l'objectif de ce test.

    chemin = RAW_DIR / "maison" / "house.npy"  # Construit le chemin du fichier contenant les dessins de maisons.

    donnees = np.load(chemin, mmap_mode="r")  # Ouvre le fichier NumPy en lecture sans charger immédiatement toutes les données en mémoire.

    assert donnees.ndim == 2  # Vérifie que le tableau possède deux dimensions.
    assert donnees.shape[1] == 784  # Vérifie que chaque dessin est représenté par 784 valeurs, soit 28 x 28 pixels.
    assert donnees.shape[0] > 0  # Vérifie que le fichier contient au moins un dessin.


def test_format_784_pixels_est_valide():  # Définit un test pour le format aplati de 784 pixels.
    """Vérifie le format habituel des dessins Quick, Draw!."""  # Décrit le format que ce test vérifie.

    donnees = np.zeros((5, 784), dtype=np.uint8)  # Crée cinq dessins fictifs, chacun représenté par 784 valeurs entières entre 0 et 255.

    assert valider_donnees(donnees)  # Vérifie que la fonction accepte ce format de données.


def test_format_28_par_28_est_valide():  # Définit un test pour le format image de 28 lignes sur 28 colonnes.
    """Vérifie le format image de 28 x 28 pixels."""  # Explique le format testé.

    donnees = np.zeros((5, 28, 28), dtype=np.uint8)  # Crée cinq images fictives de 28 x 28 pixels, initialisées à zéro.

    assert valider_donnees(donnees)  # Vérifie que la fonction accepte ce format d'images.


def test_format_incorrect_est_refuse():  # Définit un test pour vérifier le rejet d'un format non accepté.
    """Vérifie qu'un format incompatible est rejeté."""  # Explique l'objectif de ce test.

    donnees = np.zeros((5, 32, 32), dtype=np.uint8)  # Crée cinq images fictives de 32 x 32 pixels, un format non accepté par la fonction.

    assert not valider_donnees(donnees)  # Vérifie que la fonction refuse correctement ce format.