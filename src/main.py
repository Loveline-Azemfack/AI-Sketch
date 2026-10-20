"""
Programme principal de l'application AI-Sketch.

Ce module relie l'interface graphique au module de reconnaissance.
"""

import logging
import sys

from src.drawing_interface import launch_app
from src.recognition import recognize_drawing


# Configuration des messages de journalisation.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def traiter_dessin(image):
    """
    Reçoit un dessin de l'interface et lance sa reconnaissance.

    Args:
        image: Tableau NumPy représentant le dessin.

    Returns:
        dict: Classe prédite, confiance et état de reconnaissance.
    """

    if image is None:
        logger.warning("Aucun dessin n'a été transmis.")

        return {
            "classe": "Aucun dessin",
            "confiance": 0.0,
            "inconnu": True,
            "erreur": "Aucune image n'a été fournie."
        }

    try:
        # Appel du module chargé de reconnaître le dessin.
        resultat = recognize_drawing(image)

        # Vérification du résultat reçu.
        if not isinstance(resultat, dict):
            raise TypeError(
                "Le module de reconnaissance doit renvoyer un dictionnaire."
            )

        if "classe" not in resultat:
            raise ValueError(
                "Le résultat ne contient pas la classe prédite."
            )

        if "confiance" not in resultat:
            raise ValueError(
                "Le résultat ne contient pas le score de confiance."
            )

        if "inconnu" not in resultat:
            raise ValueError(
                "Le résultat ne contient pas l'indicateur inconnu."
            )

        classe = resultat["classe"]
        confiance = resultat["confiance"]
        inconnu = resultat["inconnu"]

        # Vérification du nom de la classe.
        if not isinstance(classe, str) or not classe.strip():
            raise ValueError("Le nom de la classe est invalide.")

        # Vérification du score de confiance.
        if (
            isinstance(confiance, bool)
            or not isinstance(confiance, (int, float))
            or not 0.0 <= confiance <= 1.0
        ):
            raise ValueError(
                "Le score de confiance doit être compris entre 0 et 1."
            )

        # Vérification de l'indicateur inconnu.
        if not isinstance(inconnu, bool):
            raise ValueError(
                "L'indicateur inconnu doit être un booléen."
            )

        logger.info(
            "Reconnaissance terminée : classe=%s, confiance=%.2f%%",
            classe,
            confiance * 100
        )

        return resultat

    except Exception as erreur:
        logger.exception(
            "Une erreur est survenue pendant la reconnaissance."
        )

        return {
            "classe": "Erreur",
            "confiance": 0.0,
            "inconnu": True,
            "erreur": str(erreur)
        }


def main():
    """
    Point d'entrée de l'application AI-Sketch.
    """

    logger.info("Démarrage de l'application AI-Sketch.")

    try:
        # Démarrage de l'interface graphique.
        launch_app(on_recognize=traiter_dessin)

    except KeyboardInterrupt:
        logger.info("Arrêt demandé par l'utilisateur.")

    except Exception:
        logger.exception(
            "Impossible de démarrer correctement l'application."
        )
        return 1

    logger.info("Arrêt de l'application AI-Sketch.")

    return 0


if __name__ == "__main__":
    sys.exit(main())