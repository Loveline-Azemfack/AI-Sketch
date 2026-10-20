# 🎨 AI-Sketch — Reconnaissance intelligente de dessins

## 📌 Présentation du projet

**AI-Sketch** est une application de reconnaissance de dessins basée sur l'intelligence artificielle. Elle a pour objectif de permettre à un utilisateur de dessiner un objet dans une interface graphique, puis de prédire automatiquement la catégorie à laquelle cet objet appartient.

Le projet utilise le traitement d'images et un modèle de réseau de neurones convolutif (CNN) pour analyser les dessins et proposer une prédiction.

## 🎯 Objectifs

- Créer une interface permettant de dessiner à l'aide de la souris.
- Prétraiter les images avant leur analyse.
- Utiliser un modèle entraîné pour reconnaître les dessins.
- Afficher la catégorie prédite et le niveau de confiance.
- Détecter les zones de dessin vides.
- Organiser le code en modules indépendants et testables.

## 🖼️ Catégories reconnues

Le fichier `models/classes.txt` contient les six catégories suivantes :

| Nom anglais | Signification |
|---|---|
| `house` | Maison |
| `tree` | Arbre |
| `car` | Voiture |
| `fish` | Poisson |
| `sun` | Soleil |
| `apple` | Pomme |

## 🛠️ Technologies utilisées

- **Python** : langage de programmation.
- **OpenCV** : traitement des images.
- **NumPy** : manipulation des tableaux numériques.
- **TensorFlow/Keras** : chargement et utilisation du modèle d'intelligence artificielle.
- **PyQt** : création de l'interface graphique.
- **Git et GitHub** : gestion des versions et collaboration.

## 📁 Structure du projet

```text
AI-Sketch/
├── models/
│   ├── classes.txt
│   └── sketch_model.h5
├── model/
│   ├── class_names.json
│   └── sketch_model.keras
├── src/
│   ├── data_preparation.py
│   ├── drawing_interface.py
│   ├── image_processing.py
│   ├── main.py
│   ├── predict.py
│   └── recognition.py
├── tests/
│   ├── test_data_preparation.py
│   ├── test_image_processing.py
│   ├── test_integration.py
│   └── test_recognition.py
├── app.py
├── train_offline.py
├── requirements.txt
├── .gitignore
└── README.md
```

*Remarque : cette structure présente les principaux fichiers repérés dans le projet. Les noms exacts de certains fichiers de test peuvent varier selon la version du dépôt.*

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Loveline-Azemfack/AI-Sketch.git
```

### 2. Accéder au dossier du projet

```bash
cd AI-Sketch
```

### 3. Créer un environnement virtuel

Sous Windows :

```powershell
py -m venv .venv
```

Activer l'environnement :

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloque l'activation, il est possible d'utiliser directement l'interpréteur de l'environnement virtuel avec `.\.venv\Scripts\python.exe`.

### 4. Installer les dépendances

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Le fichier `requirements.txt` doit contenir les dépendances nécessaires au projet, notamment celles utilisées pour le traitement des images, le modèle et l'interface graphique.

## 🚀 Exécution de l'application

Le dépôt contient un fichier `app.py`. Pour essayer de lancer l'application depuis la racine du projet :

```powershell
python app.py
```

Si l'application est démarrée par un autre fichier, utiliser le point d'entrée défini par l'équipe dans la version finale du projet.

**Important :** le lancement doit être vérifié après l'installation des dépendances et le contrôle des chemins du modèle.

## 🧠 Fonctionnement général

Le fonctionnement prévu de l'application se déroule en plusieurs étapes :

1. L'utilisateur dessine un objet dans la zone de dessin.
2. L'image est transmise au module de traitement.
3. Le dessin est converti en niveaux de gris, recadré, centré et redimensionné.
4. Les valeurs des pixels sont normalisées.
5. Le modèle analyse l'image et produit des scores pour les catégories.
6. La catégorie ayant le score le plus élevé est proposée comme prédiction.
7. L'application affiche le résultat et le niveau de confiance.

Le prédicteur présent dans `src/predict.py` prépare les images au format `28 × 28` et les transmet au modèle sous la forme d'un tableau de dimensions `(1, 28, 28, 1)`.

## 🧪 Tests

Les tests peuvent être exécutés depuis la racine du projet.

Pour tester la reconnaissance :

```powershell
py -m unittest discover -s tests -p "test_recognition.py" -v
```

Pour lancer l'ensemble des tests compatibles avec `unittest` :

```powershell
py -m unittest discover -s tests -v
```

Les tests doivent vérifier notamment :

- le traitement d'une image ;
- la détection d'une zone vide ;
- la prédiction d'une catégorie ;
- la gestion d'une confiance insuffisante ;
- l'intégration des différents modules.

La reconnaissance avec le modèle réel doit également être testée. Des tests réalisés uniquement avec un faux modèle ne permettent pas de mesurer la précision de l'intelligence artificielle.

## 🤝 Collaboration et Git

Le projet est développé en équipe avec Git et GitHub.

Pour consulter les branches disponibles :

```powershell
git branch -a
```

Pour récupérer les informations les plus récentes du dépôt distant :

```powershell
git fetch origin
```

Les modifications doivent être réalisées dans des branches dédiées, puis proposées à l'équipe par une *Pull Request* lorsque cela est nécessaire.

Exemple de création d'une branche :

```powershell
git switch -c feature/nom-de-la-fonctionnalite
```

Avant de partager des modifications, vérifier l'état du dépôt :

```powershell
git status
```

## ⚠️ Limites actuelles

Le fonctionnement complet de l'application doit être confirmé dans l'environnement final. En particulier, il faut vérifier :

- le chargement du modèle entraîné ;
- la correspondance entre les sorties du modèle et les classes ;
- la compatibilité entre le prétraitement et les données d'entraînement ;
- l'intégration du prédicteur dans l'interface ;
- les performances de reconnaissance sur des dessins réels.

## 🔮 Améliorations possibles

- Ajouter de nouvelles catégories d'objets.
- Améliorer la diversité des données d'entraînement.
- Évaluer les performances du modèle sur un jeu de test indépendant.
- Améliorer la gestion des dessins ambigus.
- Afficher des messages plus explicites lorsque le dessin n'est pas reconnu.
- Améliorer l'ergonomie de l'interface graphique.

## 👥 Équipe

**Projet :** AI-Sketch  
**Domaine :** Intelligence artificielle et vision par ordinateur  
**Année académique :** 2026–2027

Les noms des membres du groupe peuvent être ajoutés ici.

## 📄 Licence

La licence du projet reste à définir par l'équipe selon les conditions de diffusion du code et des données utilisés.

---

*AI-Sketch — Dessiner, reconnaître et apprendre grâce à l'intelligence artificielle.*