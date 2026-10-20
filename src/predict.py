import os
import cv2
import numpy as np
import tensorflow as tf


class SketchPredictor:
    def __init__(self, model_path="models/sketch_model.h5", classes_path="models/classes.txt"):
        self.model_path = model_path
        self.classes_path = classes_path
        self.classes = []
        self.model = None
        self.load_resources()

    def load_resources(self):
        if os.path.exists(self.classes_path):
            with open(self.classes_path, "r", encoding="utf-8") as f:
                self.classes = [line.strip() for line in f if line.strip()]
        else:
            self.classes = ["house", "tree", "car", "fish", "sun", "apple"]

        if os.path.exists(self.model_path):
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"[SketchPredictor] Modèle chargé avec succès ({len(self.classes)} classes).")
        else:
            print(f"[SketchPredictor] Avertissement : modèle '{self.model_path}' introuvable.")

    def preprocess_image(self, bgr_image):
        """
        Adapte le dessin utilisateur (trait noir / fond blanc)
        vers le standard Quick, Draw! (trait blanc / fond noir, centré en 28x28).
        """
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        inverted = cv2.bitwise_not(gray)

        coords = cv2.findNonZero(inverted)
        if coords is None:
            return np.zeros((1, 28, 28, 1), dtype=np.float32)

        x, y, w, h = cv2.boundingRect(coords)
        cropped = inverted[y:y + h, x:x + w]

        # Conserver le ratio d'aspect via une boîte carrée
        max_dim = max(w, h)
        square = np.zeros((max_dim, max_dim), dtype=np.uint8)
        offset_x = (max_dim - w) // 2
        offset_y = (max_dim - h) // 2
        square[offset_y:offset_y + h, offset_x:offset_x + w] = cropped

        # Marge de sécurité (padding)
        padded = cv2.copyMakeBorder(square, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=0)

        # Redimensionnement 28x28 et normalisation
        resized = cv2.resize(padded, (28, 28), interpolation=cv2.INTER_AREA)
        normalized = (resized / 255.0).astype(np.float32)
        return normalized.reshape(1, 28, 28, 1)

    def predict(self, bgr_image):
        if self.model is None:
            return "Modèle non chargé", 0.0

        processed = self.preprocess_image(bgr_image)
        if np.max(processed) == 0.0:
            return "Zone vide", 0.0

        probabilities = self.model.predict(processed, verbose=0)[0]
        best_idx = int(np.argmax(probabilities))
        confidence = float(probabilities[best_idx]) * 100.0
        predicted_class = self.classes[best_idx]

        return predicted_class, round(confidence, 2)