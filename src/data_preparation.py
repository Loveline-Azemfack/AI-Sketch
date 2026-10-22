from pathlib import Path
import numpy as np


# Chemin vers le dossier principal du projet
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dossier contenant les données originales
RAW_DIR = PROJECT_DIR / "dataset" / "raw"

# Catégories de dessins utilisées dans AI Sketch
CATEGORIES = [
    "maison",
    "arbre",
    "voiture",
    "chat",
    "soleil",
    "fish",
    "flower",
    "airplane",
]

def valider_donnees(donnees):
    """Vérifie que les dessins possèdent un format compatible."""

    if donnees.ndim == 2 and donnees.shape[1] == 784:
        return True

    if donnees.ndim == 3 and donnees.shape[1:] == (28, 28):
        return True

    if donnees.ndim == 4 and donnees.shape[1:] == (28, 28, 1):
        return True

    return False

def verifier_dataset():
    """Vérifie la présence et la structure des fichiers du dataset."""

    print("=== Vérification du dataset AI Sketch ===")
    print(f"Dossier des données : {RAW_DIR}\n")

    if not RAW_DIR.is_dir():
        print("ERREUR : le dossier dataset/raw est introuvable.")
        return

    total_dessins = 0

    for categorie in CATEGORIES:
        chemin = RAW_DIR / categorie / f"{categorie}.npy"

        if not chemin.is_file():
            print(f"[ERREUR] Fichier introuvable : {chemin}")
            continue

        try:
            donnees = np.load(chemin, mmap_mode="r")

            nombre_dessins = donnees.shape[0]

            print(f"[OK] Catégorie : {categorie}")
            print(f"     Nombre de dessins : {nombre_dessins}")
            print(f"     Dimensions du tableau : {donnees.shape}")
            print(f"     Type des données : {donnees.dtype}")

            total_dessins += nombre_dessins

        except (OSError, ValueError) as erreur:
            print(f"[ERREUR] Impossible de lire {chemin.name} : {erreur}")

    print("\n=== Bilan ===")
    print(f"Nombre total de dessins trouvés : {total_dessins}")


if __name__ == "__main__":
    verifier_dataset()