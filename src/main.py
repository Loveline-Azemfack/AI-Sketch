
"""
Programme principal de l'application AI-Sketch.

Ce module relie l'interface graphique au module de reconnaissance.
Il reçoit les dessins, vérifie les résultats de reconnaissance
et gère le démarrage ainsi que l'arrêt de l'application.
"""

import logging  # Importe le module permettant d'afficher et d'enregistrer les messages de journalisation.
import sys  # Importe le module système pour terminer le programme avec un code de retour.

from src.drawing_interface import launch_app  # Importe la fonction qui démarre l'interface graphique.
from src.recognition import recognize_drawing  # Importe la fonction qui reconnaît les dessins.


# Configure le système de journalisation pour contrôler les messages affichés.
logging.basicConfig(
    level=logging.INFO,  # Affiche les messages de niveau INFO, WARNING, ERROR et CRITICAL.
    format="%(asctime)s - %(levelname)s - %(message)s"  # Définit le format des messages avec la date, le niveau et le texte.
)

logger = logging.getLogger(__name__)  # Crée un journal associé au module actuel pour enregistrer les événements.


def traiter_dessin(image):  # Définit la fonction appelée lorsque l'utilisateur demande la reconnaissance d'un dessin.
    """
    Reçoit un dessin de l'interface et lance sa reconnaissance.

    Args:
        image: Tableau NumPy représentant le dessin.

    Returns:
        dict: Classe prédite, confiance et état de reconnaissance.
    """

    if image is None:  # Vérifie si aucune image n'a été transmise par l'interface.
        logger.warning("Aucun dessin n'a été transmis.")  # Enregistre un avertissement signalant l'absence de dessin.

        return {  # Retourne un dictionnaire décrivant l'absence d'image.
            "classe": "Aucun dessin",  # Indique qu'aucun dessin n'est disponible pour la reconnaissance.
            "confiance": 0.0,  # Définit le score de confiance à zéro puisqu'aucune reconnaissance n'a été effectuée.
            "inconnu": True,  # Indique qu'aucune classe connue n'a pu être identifiée.
            "erreur": "Aucune image n'a été fournie."  # Fournit une explication de l'absence de résultat.
        }

    try:  # Commence un bloc de protection pour intercepter les erreurs de reconnaissance et de validation.
        # Appel du module chargé de reconnaître le dessin.
        resultat = recognize_drawing(image)  # Transmet l'image au module de reconnaissance et récupère son résultat.

        # Vérification du résultat reçu.
        if not isinstance(resultat, dict):  # Vérifie que le résultat est bien un dictionnaire Python.
            raise TypeError(  # Déclenche une erreur si le résultat possède un type incorrect.
                "Le module de reconnaissance doit renvoyer un dictionnaire."  # Explique le type de résultat attendu.
            )

        if "classe" not in resultat:  # Vérifie que le dictionnaire contient le nom de la classe prédite.
            raise ValueError(  # Déclenche une erreur si la clé classe est absente.
                "Le résultat ne contient pas la classe prédite."  # Explique quelle information manque.
            )

        if "confiance" not in resultat:  # Vérifie que le dictionnaire contient le score de confiance.
            raise ValueError(  # Déclenche une erreur si la clé confiance est absente.
                "Le résultat ne contient pas le score de confiance."  # Explique quelle information manque.
            )

        if "inconnu" not in resultat:  # Vérifie que le dictionnaire indique si le dessin est inconnu.
            raise ValueError(  # Déclenche une erreur si la clé inconnu est absente.
                "Le résultat ne contient pas l'indicateur inconnu."  # Explique quelle information manque.
            )

        classe = resultat["classe"]  # Récupère le nom de la classe prédite par le modèle.
        confiance = resultat["confiance"]  # Récupère le score de confiance associé à la prédiction.
        inconnu = resultat["inconnu"]  # Récupère l'indicateur précisant si le dessin est considéré comme inconnu.

        # Vérification du nom de la classe.
        if not isinstance(classe, str) or not classe.strip():  # Vérifie que la classe est une chaîne non vide.
            raise ValueError("Le nom de la classe est invalide.")  # Signale une erreur si le nom de classe est invalide.

        # Vérification du score de confiance.
        if (  # Commence la vérification des conditions de validité du score.
            isinstance(confiance, bool)  # Refuse les booléens, car True et False sont aussi considérés comme des entiers en Python.
            or not isinstance(confiance, (int, float))  # Vérifie que le score est un nombre entier ou décimal.
            or not 0.0 <= confiance <= 1.0  # Vérifie que le score est compris entre 0 et 1 inclus.
        ):
            raise ValueError(  # Déclenche une erreur si le score ne respecte pas les conditions précédentes.
                "Le score de confiance doit être compris entre 0 et 1."  # Indique l'intervalle de valeurs autorisé.
            )

        # Vérification de l'indicateur inconnu.
        if not isinstance(inconnu, bool):  # Vérifie que l'indicateur inconnu est un booléen.
            raise ValueError(  # Déclenche une erreur si l'indicateur n'est pas un booléen.
                "L'indicateur inconnu doit être un booléen."  # Indique le type de valeur attendu.
            )

        logger.info(  # Enregistre un message informatif indiquant que la reconnaissance a réussi.
            "Reconnaissance terminée : classe=%s, confiance=%.2f%%",  # Définit le message avec deux emplacements de formatage.
            classe,  # Remplace le premier emplacement %s par le nom de la classe prédite.
            confiance * 100  # Convertit le score compris entre 0 et 1 en pourcentage.
        )

        return resultat  # Renvoie à l'interface le dictionnaire contenant les résultats validés.

    except Exception as erreur:  # Intercepte les exceptions survenues pendant la reconnaissance ou la validation.
        logger.exception(  # Enregistre le message d'erreur ainsi que les détails de l'exception.
            "Une erreur est survenue pendant la reconnaissance."  # Décrit le problème rencontré.
        )

        return {  # Retourne un dictionnaire standardisé pour signaler l'échec de la reconnaissance.
            "classe": "Erreur",  # Indique que la reconnaissance n'a pas pu aboutir normalement.
            "confiance": 0.0,  # Définit le score de confiance à zéro en cas d'erreur.
            "inconnu": True,  # Indique qu'aucune classe fiable n'a été reconnue.
            "erreur": str(erreur)  # Convertit l'exception en texte pour communiquer la cause de l'erreur.
        }


def main():  # Définit la fonction principale qui contrôle le cycle de vie de l'application.
    """
    Point d'entrée de l'application AI-Sketch.
    """

    logger.info("Démarrage de l'application AI-Sketch.")  # Enregistre un message indiquant le lancement de l'application.

    try:  # Commence un bloc de protection pour gérer les problèmes survenant au démarrage de l'interface.
        # Démarrage de l'interface graphique.
        launch_app()  # Lance l'interface et lui transmet la fonction de reconnaissance à appeler.

    except KeyboardInterrupt:  # Détecte une interruption volontaire du programme par l'utilisateur.
        logger.info("Arrêt demandé par l'utilisateur.")  # Enregistre le fait que l'utilisateur a demandé l'arrêt.

    except Exception:  # Intercepte les autres erreurs qui empêchent le démarrage ou le fonctionnement normal de l'interface.
        logger.exception(  # Enregistre les détails de l'erreur rencontrée.
            "Impossible de démarrer correctement l'application."  # Décrit le problème survenu.
        )
        return 1  # Renvoie le code 1 pour signaler un échec du programme.

    logger.info("Arrêt de l'application AI-Sketch.")  # Enregistre un message indiquant la fin de l'application.

    return 0  # Renvoie le code 0 pour signaler une fin normale du programme.


if __name__ == "__main__":  # Vérifie si ce fichier est exécuté directement plutôt qu'importé par un autre module.
    sys.exit(main())  # Exécute la fonction principale et transmet son code de retour au système d'exploitation.
