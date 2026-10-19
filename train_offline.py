import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models

# 1. Configuration des catégories et des dossiers
CLASSES = ["house", "tree", "car", "fish", "sun", "apple"]
DATA_DIR = "data"
MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

# 4000 dessins par classe pour un apprentissage rapide sur CPU
SAMPLES_PER_CLASS = 4000

X_list = []
y_list = []

print("Chargement des données Quick, Draw!...")
for idx, label in enumerate(CLASSES):
    file_path = os.path.join(DATA_DIR, f"{label}.npy")
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Fichier manquant : {file_path}. Placez les fichiers .npy dans le dossier data/."
        )

    data = np.load(file_path)
    data = data[:SAMPLES_PER_CLASS]

    X_list.append(data)
    y_list.append(np.full(len(data), idx))
    print(f"  -> {label} : {len(data)} croquis chargés.")

# 2. Concaténation, normalisation et redimensionnement
X = np.concatenate(X_list, axis=0)
y = np.concatenate(y_list, axis=0)

X = X.reshape(-1, 28, 28, 1).astype("float32") / 255.0
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Architecture du Réseau de Neurones Convolutif (CNN)
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(len(CLASSES), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# 4. Entraînement
history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=64,
    validation_data=(X_val, y_val)
)

# 5. Sauvegarde du modèle et du dictionnaire des classes
model_path = os.path.join(MODELS_DIR, "sketch_model.h5")
model.save(model_path)
print(f"\n[Succès] Modèle sauvegardé sous : {model_path}")

classes_path = os.path.join(MODELS_DIR, "classes.txt")
with open(classes_path, "w", encoding="utf-8") as f:
    f.write("\n".join(CLASSES))
print(f"[Succès] Noms des classes sauvegardés sous : {classes_path}")

# 6. Génération des graphiques pour le rapport
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="Entraînement")
plt.plot(history.history["val_accuracy"], label="Validation")
plt.title("Précision (Accuracy)")
plt.xlabel("Époque")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="Entraînement")
plt.plot(history.history["val_loss"], label="Validation")
plt.title("Perte (Loss)")
plt.xlabel("Époque")
plt.legend()

plt.tight_layout()
plt.savefig("courbes_apprentissage.png")
print("[Succès] Graphiques de performance exportés sous courbes_apprentissage.png")