from pathlib import Path
import json

import cv2
import numpy as np


# Racine du projet AI-Sketch.
BASE_DIR = Path(__file__).resolve().parent.parent

# Chemins vers le modèle entraîné et les catégories.
MODEL_PATH = BASE_DIR / "models" / "sketch_model.h5"
CLASS_NAMES_PATH = BASE_DIR / "model" / "class_names.json"

# Taille d'entrée attendue par le modèle.
IMAGE_SIZE = 28

# Score minimal requis pour accepter une prédiction.
CONFIDENCE_THRESHOLD = 0.60

# Le modèle et les classes seront chargés une seule fois.
_model = None
_class_names = None


def load_class_names(path=CLASS_NAMES_PATH):
    """
    Charge les noms des classes depuis un fichier JSON.

    Le fichier doit contenir une liste de catégories dans le même
    ordre que les sorties du modèle.

    Args:
        path: chemin du fichier JSON.

    Returns:
        list: noms des classes.
    """

    path = Path(path)

    if not path.is_absolute():
        path = BASE_DIR / path

    if not path.exists():
        raise FileNotFoundError(
            f"Fichier des catégories introuvable : {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        class_names = json.load(file)

    if not isinstance(class_names, list) or not class_names:
        raise ValueError(
            "Le fichier des catégories doit contenir "
            "une liste non vide."
        )

    if not all(
        isinstance(name, str) and name.strip()
        for name in class_names
    ):
        raise ValueError(
            "Chaque catégorie doit être une chaîne de caractères "
            "non vide."
        )

    return class_names


def load_trained_model(path=MODEL_PATH):
    """
    Charge le modèle TensorFlow entraîné.

    Args:
        path: chemin du modèle .h5 ou .keras.

    Returns:
        Le modèle TensorFlow chargé.
    """

    path = Path(path)

    if not path.is_absolute():
        path = BASE_DIR / path

    if not path.exists():
        raise FileNotFoundError(
            f"Modèle introuvable : {path}. "
            "Vérifie que le modèle a été entraîné."
        )

    import tensorflow as tf

    model = tf.keras.models.load_model(path)

    return model


def _to_grayscale(image):
    """
    Convertit une image Pillow, NumPy ou un chemin de fichier
    en image en niveaux de gris.

    Les tableaux NumPy à trois canaux sont interprétés comme
    des images RGB, ce qui convient aux dessins provenant
    de l'interface graphique Pillow.
    """

    # Image fournie sous forme de chemin.
    if isinstance(image, (str, Path)):
        image = cv2.imread(str(image), cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError(
                "Impossible de lire l'image fournie."
            )

        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Image fournie sous forme d'objet Pillow.
    if hasattr(image, "convert") and not isinstance(
        image, np.ndarray
    ):
        image = np.asarray(image.convert("RGB"))

    # Image fournie sous forme de tableau NumPy.
    if not isinstance(image, np.ndarray):
        raise TypeError(
            "L'image doit être un objet Pillow, "
            "un tableau NumPy ou un chemin de fichier."
        )

    if image.size == 0:
        raise ValueError("L'image fournie est vide.")

    if image.ndim == 2:
        grayscale = image

    elif image.ndim == 3 and image.shape[2] == 3:
        grayscale = cv2.cvtColor(
            image.astype(np.uint8),
            cv2.COLOR_RGB2GRAY
        )

    elif image.ndim == 3 and image.shape[2] == 4:
        grayscale = cv2.cvtColor(
            image.astype(np.uint8),
            cv2.COLOR_RGBA2GRAY
        )

    else:
        raise ValueError(
            "Format d'image non pris en charge. "
            "Utilise une image en niveaux de gris, RGB ou RGBA."
        )

    if grayscale.dtype != np.uint8:
        if np.issubdtype(grayscale.dtype, np.floating):
            if not np.all(np.isfinite(grayscale)):
                raise ValueError(
                    "L'image contient des valeurs invalides."
                )

            if grayscale.size and grayscale.min() >= 0 and (
                grayscale.max() <= 1
            ):
                grayscale = grayscale * 255.0

        grayscale = np.clip(
            grayscale, 0, 255
        ).astype(np.uint8)

    return grayscale


def is_blank_drawing(image):
    """
    Vérifie si l'image ne contient aucun trait significatif.

    L'interface utilise un fond blanc et des traits foncés.
    """

    grayscale = _to_grayscale(image)

    # Les pixels suffisamment foncés sont considérés comme des traits.
    number_of_strokes = np.count_nonzero(grayscale < 245)

    return number_of_strokes == 0


def preprocess_drawing(image):
    """
    Prépare le dessin pour le modèle.

    Étapes :
    1. Conversion en niveaux de gris.
    2. Inversion des couleurs pour obtenir des traits blancs
       sur un fond noir.
    3. Détection de la zone contenant le dessin.
    4. Centrage dans une image carrée.
    5. Redimensionnement en 28 x 28.
    6. Normalisation entre 0 et 1.
    7. Ajout du canal de couleur.

    Returns:
        np.ndarray: image de forme (28, 28, 1).
    """

    grayscale = _to_grayscale(image)

    # Fond blanc -> noir ; traits foncés -> blancs.
    inverted = 255 - grayscale

    # Détection des pixels qui appartiennent au dessin.
    _, binary = cv2.threshold(
        inverted,
        10,
        255,
        cv2.THRESH_BINARY
    )

    points = cv2.findNonZero(binary)

    if points is None:
        raise ValueError(
            "Aucun trait détectable dans le dessin."
        )

    # Récupération de la boîte entourant les traits.
    x, y, width, height = cv2.boundingRect(points)

    cropped = inverted[
        y:y + height,
        x:x + width
    ]

    # Ajout de marges pour conserver les proportions.
    size = max(width, height)
    padding = max(2, int(size * 0.15))
    canvas_size = size + 2 * padding

    square = np.zeros(
        (canvas_size, canvas_size),
        dtype=np.uint8
    )

    offset_x = (canvas_size - width) // 2
    offset_y = (canvas_size - height) // 2

    square[
        offset_y:offset_y + height,
        offset_x:offset_x + width
    ] = cropped

    # Redimensionnement à la taille attendue par le modèle.
    resized = cv2.resize(
        square,
        (IMAGE_SIZE, IMAGE_SIZE),
        interpolation=cv2.INTER_AREA
    )

    # Normalisation des pixels entre 0 et 1.
    normalized = resized.astype(np.float32) / 255.0

    # Le modèle attend une image avec un canal.
    return np.expand_dims(normalized, axis=-1)


def _build_result(class_name, confidence, message, unknown):
    """
    Construit un résultat compatible avec main.py tout en
    conservant les noms de clés de l'ancien module.
    """

    return {
        # Clés exigées par main.py.
        "classe": class_name,
        "confiance": float(confidence),
        "inconnu": bool(unknown),

        # Clés conservées pour compatibilité.
        "class_name": class_name,
        "confidence": float(confidence),
        "message": message
    }


def predict_drawing(
    image,
    model,
    class_names,
    threshold=CONFIDENCE_THRESHOLD
):
    """
    Prédit la catégorie correspondant au dessin.

    Args:
        image: dessin à reconnaître.
        model: modèle TensorFlow déjà chargé.
        class_names: liste des catégories.
        threshold: confiance minimale, entre 0 et 1.

    Returns:
        dict: classe, confiance, indicateur inconnu et message.
    """

    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "Le seuil doit être compris entre 0 et 1."
        )

    if is_blank_drawing(image):
        return _build_result(
            class_name="Aucun dessin",
            confidence=0.0,
            message="Veuillez dessiner un objet.",
            unknown=True
        )

    if not isinstance(class_names, list) or not class_names:
        raise ValueError(
            "La liste des catégories est vide ou invalide."
        )

    # Préparation de l'image pour le modèle.
    processed_image = preprocess_drawing(image)

    # Ajout de la dimension correspondant au lot d'images.
    input_batch = np.expand_dims(
        processed_image,
        axis=0
    )

    # Prédiction du modèle.
    predictions = np.asarray(
        model.predict(input_batch, verbose=0)
    )

    if predictions.ndim != 2 or predictions.shape[0] != 1:
        raise ValueError(
            "Le modèle doit retourner un score par classe "
            "pour une image."
        )

    scores = predictions[0]

    if len(scores) != len(class_names):
        raise ValueError(
            "Le nombre de scores ne correspond pas "
            "au nombre de catégories."
        )

    if not np.all(np.isfinite(scores)):
        raise ValueError(
            "Le modèle a retourné des scores invalides."
        )

    # Vérifie que les sorties représentent des probabilités.
    # Si elles ne sont pas normalisées, on les normalise.
    if np.any(scores < 0):
        # Cas de sorties assimilables à des logits.
        shifted_scores = scores - np.max(scores)
        probabilities = np.exp(shifted_scores)
        probabilities = probabilities / np.sum(probabilities)

    else:
        total = float(np.sum(scores))

        if total <= 0:
            raise ValueError(
                "Le modèle a retourné des scores nuls."
            )

        probabilities = scores / total

    predicted_index = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_index])

    if confidence < threshold:
        return _build_result(
            class_name="Inconnu",
            confidence=confidence,
            message=(
                "Dessin non reconnu avec suffisamment "
                "de confiance."
            ),
            unknown=True
        )

    return _build_result(
        class_name=class_names[predicted_index],
        confidence=confidence,
        message="Reconnaissance réussie.",
        unknown=False
    )


def recognize_drawing(image):
    """
    Fonction appelée par main.py.

    Elle charge le modèle et les catégories lors du premier appel,
    puis réutilise ces ressources pour les reconnaissances suivantes.

    Args:
        image: dessin provenant de l'interface.

    Returns:
        dict: résultat compatible avec main.py.
    """

    global _model, _class_names

    if image is None:
        return _build_result(
            class_name="Aucun dessin",
            confidence=0.0,
            message="Aucune image n'a été fournie.",
            unknown=True
        )

    # Chargement unique du modèle et des catégories.
    if _class_names is None:
        _class_names = load_class_names()

    if _model is None:
        _model = load_trained_model()

    # Reconnaissance du dessin.
    return predict_drawing(
        image=image,
        model=_model,
        class_names=_class_names,
        threshold=CONFIDENCE_THRESHOLD
    )