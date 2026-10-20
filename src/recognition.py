
from pathlib import Path
import json

import numpy as np

from src.image_processing import preprocess_image, is_blank_image


MODEL_PATH = Path("model/sketch_model.keras")
CLASS_NAMES_PATH = Path("model/class_names.json")

CONFIDENCE_THRESHOLD = 0.60


def load_class_names(path=CLASS_NAMES_PATH):
    """Charge la liste ordonnée des catégories du modèle."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Fichier des catégories introuvable : {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        class_names = json.load(file)

    if not isinstance(class_names, list) or not class_names:
        raise ValueError(
            "Le fichier des catégories doit contenir une liste non vide."
        )

    return class_names


def load_trained_model(path=MODEL_PATH):
    """Charge le modèle Keras entraîné."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Modèle introuvable : {path}. "
            "Le modèle doit être entraîné avant la reconnaissance."
        )

    import tensorflow as tf

    return tf.keras.models.load_model(path)


def predict_drawing(
    image,
    model,
    class_names,
    threshold=CONFIDENCE_THRESHOLD
):
    """
    Reconnaît un dessin.

    Retourne un dictionnaire contenant la classe,
    la confiance et un message.
    """
    if is_blank_image(image):
        return {
            "class_name": "Inconnu",
            "confidence": 0.0,
            "message": "Veuillez dessiner un objet."
        }

    processed_image = preprocess_image(image)
    input_batch = np.expand_dims(processed_image, axis=0)

    predictions = np.asarray(
        model.predict(input_batch, verbose=0)
    )

    if predictions.ndim != 2 or predictions.shape[0] != 1:
        raise ValueError(
            "Le modèle doit retourner un score par classe pour une image."
        )

    scores = predictions[0]

    if len(scores) != len(class_names):
        raise ValueError(
            "Le nombre de scores ne correspond pas au nombre de classes."
        )

    if not np.all(np.isfinite(scores)):
        raise ValueError("Le modèle a retourné des scores invalides.")

    predicted_index = int(np.argmax(scores))
    confidence = float(scores[predicted_index])

    if not 0.0 <= threshold <= 1.0:
        raise ValueError("Le seuil doit être compris entre 0 et 1.")

    if confidence < threshold:
        class_name = "Inconnu"
        message = "Dessin non reconnu avec suffisamment de confiance."
    else:
        class_name = class_names[predicted_index]
        message = "Reconnaissance réussie."

    return {
        "class_name": class_name,
        "confidence": confidence,
        "message": message
    }
