import unittest

import cv2
import numpy as np

from src.recognition import predict_drawing


class FakeModel:
    """Faux modèle pour tester sans modèle IA entraîné."""

    def __init__(self, scores):
        self.scores = np.array([scores], dtype=np.float32)

    def predict(self, images, verbose=0):
        return self.scores


class TestRecognition(unittest.TestCase):

    def setUp(self):
        # Image blanche avec un trait noir simulant un dessin.
        self.drawing = np.full((200, 200, 3), 255, dtype=np.uint8)
        cv2.line(
            self.drawing,
            (50, 50),
            (150, 150),
            (0, 0, 0),
            5
        )

        self.classes = ["maison", "arbre", "voiture"]

    def test_recognize_drawing(self):
        model = FakeModel([0.10, 0.80, 0.10])

        result = predict_drawing(
            self.drawing,
            model,
            self.classes
        )

        self.assertEqual(result["class_name"], "arbre")
        self.assertAlmostEqual(result["confidence"], 0.80, places=5)

    def test_blank_image(self):
        blank = np.full((200, 200, 3), 255, dtype=np.uint8)
        model = FakeModel([0.10, 0.80, 0.10])

        result = predict_drawing(blank, model, self.classes)

        self.assertEqual(result["class_name"], "Aucun dessin")
        self.assertEqual(result["confidence"], 0.0)

    def test_low_confidence(self):
        model = FakeModel([0.40, 0.35, 0.25])

        result = predict_drawing(
            self.drawing,
            model,
            self.classes,
            threshold=0.60
        )

        self.assertEqual(result["class_name"], "Inconnu")


if __name__ == "__main__":
    unittest.main()
