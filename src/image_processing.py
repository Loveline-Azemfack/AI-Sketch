
import cv2
import numpy as np


IMAGE_SIZE = (28, 28)


def load_image(image_source):
    """
    Charge une image depuis un chemin de fichier
    ou accepte directement une image NumPy.
    """
    if isinstance(image_source, str):
        image = cv2.imread(image_source)

        if image is None:
            raise ValueError(
                f"Impossible de charger l'image : {image_source}"
            )

        return image

    if isinstance(image_source, np.ndarray):
        if image_source.size == 0:
            raise ValueError("L'image est vide.")

        return image_source.copy()

    raise TypeError(
        "La source doit être un chemin de fichier "
        "ou un tableau NumPy."
    )


def is_blank_image(image, threshold=10):
    """
    Vérifie si une image contient suffisamment de traces
    pour être considérée comme un dessin.

    Cette fonction suppose un fond blanc et des traits sombres,
    comme dans une zone de dessin classique.
    """
    image = load_image(image)

    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return cv2.countNonZero(
        cv2.threshold(
            image, threshold, 255, cv2.THRESH_BINARY_INV
        )[1]
    ) == 0


def preprocess_image(image_source):
    """
    Prépare une image pour le modèle :
    - chargement ;
    - conversion en niveaux de gris ;
    - redimensionnement ;
    - normalisation des pixels entre 0 et 1.

    Retourne un tableau NumPy de forme (28, 28, 1).
    """
    image = load_image(image_source)

    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif image.ndim != 2:
        raise ValueError("Format d'image non pris en charge.")

    image = cv2.resize(
        image,
        IMAGE_SIZE,
        interpolation=cv2.INTER_AREA
    )

    image = image.astype(np.float32) / 255.0

    return np.expand_dims(image, axis=-1)
