# RAPPORT DE PROJET : AI-SKETCH
## Conception d’une application intelligente de reconnaissance de dessins

**Filière :** AN-ING 2  
**Projet :** AI-Sketch  
**Technologies principales :** Python, OpenCV, NumPy, TensorFlow/Keras et PyQt  
**Année académique :** 2026–2027  
**Membres du groupe :** À compléter

---

# INTRODUCTION

L’intelligence artificielle occupe une place de plus en plus importante dans le développement des applications informatiques. Elle permet notamment aux machines d’analyser des données, de reconnaître des objets et d’effectuer des prédictions à partir de modèles entraînés.

C’est dans ce contexte que s’inscrit le projet AI-Sketch, qui consiste à concevoir une application capable de reconnaître des objets à partir de dessins réalisés par un utilisateur.

L’objectif est de permettre à l’utilisateur de dessiner un objet dans une interface graphique, puis de soumettre ce dessin à un système de reconnaissance basé sur un modèle d’intelligence artificielle.

# CHAPITRE I : PRÉSENTATION DU PROJET

## 1.1. Contexte et justification

La reconnaissance automatique de dessins constitue une application intéressante de la vision par ordinateur et de l’apprentissage automatique. Elle nécessite le traitement des images, l’extraction des informations utiles et l’utilisation d’un modèle capable de distinguer différentes catégories d’objets.

Le projet AI-Sketch permet ainsi de mettre en pratique plusieurs notions étudiées en informatique, notamment la programmation Python, le traitement d’images, l’apprentissage profond et la conception d’interfaces graphiques.

## 1.2. Problématique

Comment concevoir une application capable d’analyser un dessin réalisé librement par un utilisateur et de proposer automatiquement la catégorie d’objet correspondante ?

Cette problématique implique plusieurs difficultés : les dessins peuvent varier en taille, en position, en proportions et en qualité. Le système doit donc préparer les images de manière cohérente avant de les transmettre au modèle de reconnaissance.

## 1.3. Objectif général

L’objectif général du projet est de développer une application de reconnaissance de dessins utilisant un modèle d’intelligence artificielle.

## 1.4. Objectifs spécifiques

Les objectifs spécifiques sont les suivants :

- concevoir une interface permettant de dessiner à l’aide d’une souris ;
- préparer les images pour les rendre compatibles avec le modèle ;
- utiliser un modèle entraîné pour prédire la catégorie d’un dessin ;
- afficher la catégorie prédite et le niveau de confiance associé ;
- gérer les dessins vides ou les résultats insuffisamment fiables ;
- tester les différentes composantes de l’application et leur intégration.

## 1.5. Catégories visées

Le fichier de classes récupéré pour le projet contient six catégories :

1. House : maison ;
2. Tree : arbre ;
3. Car : voiture ;
4. Fish : poisson ;
5. Sun : soleil ;
6. Apple : pomme.

# CHAPITRE II : ENVIRONNEMENT TECHNIQUE

## 2.1. Python

Python est le langage principal utilisé pour développer l’application. Il permet de mettre en œuvre le traitement des images, le chargement du modèle et la logique de reconnaissance.

## 2.2. OpenCV

OpenCV est utilisé pour manipuler les images. Dans le code de prédiction du projet, il intervient notamment dans la conversion en niveaux de gris, l’inversion des couleurs, le recadrage du dessin et son redimensionnement.

## 2.3. NumPy

NumPy permet de manipuler les tableaux numériques représentant les images et les données transmises au modèle.

## 2.4. TensorFlow et Keras

TensorFlow/Keras est utilisé dans le code du projet pour charger le modèle de réseau de neurones et effectuer les prédictions.

Le dépôt contient un modèle nommé `sketch_model.h5` ainsi qu’un script d’entraînement. Le chargement effectif du modèle reste à valider dans l’environnement Python utilisé pour les tests.

## 2.5. PyQt

PyQt est destiné à la réalisation de l’interface graphique. Il permet de construire une fenêtre dans laquelle l’utilisateur peut dessiner et consulter le résultat de la reconnaissance.

# CHAPITRE III : ARCHITECTURE ET FONCTIONNEMENT

## 3.1. Architecture générale

Le fonctionnement envis