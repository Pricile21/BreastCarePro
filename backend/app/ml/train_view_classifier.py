"""
Entraînement d'un classifieur de vues basé sur les vraies images
Utilise le dataset complet avec features extraites depuis les images
"""

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path
import cv2
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from scipy import ndimage, stats
import os

print("=" * 70)
print("ENTRAÎNEMENT DU CLASSIFIEUR DE VUES")
print("Basé sur les vraies images du dataset")
print("=" * 70)

# Configuration
BATCH_SIZE = 64
LEARNING_RATE = 1e-3
EPOCHS = 100
MAX_SAMPLES = None  # None = tous les échantillons

# 1. Charger les annotations
print("\n[1/6] Chargement des annotations...")
annotations = pd.read_csv('../../../breast-level_annotations (1).csv')
print(f"✓ {len(annotations)} annotations chargées")

# Garder seulement les échantillons d'entraînement
train_data = annotations[annotations['split'] == 'training']
print(f"✓ {len(train_data)} échantillons d'entraînement")

# Limiter si nécessaire
if MAX_SAMPLES:
    train_data = train_data.head(MAX_SAMPLES)
    print(f"  (Limité à {MAX_SAMPLES} pour test rapide)")

# 2. Préparer les paths des images
print("\n[2/6] Préparation des chemins d'images...")
image_paths = {
    'Extract': Path('../../../Extract/images_png'),
    'extracted_data': Path('../../../extracted_data/images_png')
}

def get_image_path(study_id, image_id):
    """Trouve le chemin de l'image"""
    for name, base_path in image_paths.items():
        path = base_path / study_id / f"{image_id}.png"
        if path.exists():
            return path
    return None

# 3. Extraction des features
print("\n[3/6] Extraction des features depuis les images (peut prendre du temps)...")

def extract_features_from_image(image_path):
    """Extrait 32 features depuis une image"""
    try:
        # Charger l'image
        image = Image.open(image_path)
        if image.mode != 'L':
            image = image.convert('L')
        
        # Redimensionner
        image_array = np.array(image).astype(np.float32) / 255.0
        image_array = cv2.resize(image_array, (448, 448))
        
        # Appliquer CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        image_array = clahe.apply((image_array * 255).astype(np.uint8)).astype(np.float32) / 255.0
        
        # Extraire features
        mean = np.mean(image_array)
        std = np.std(image_array)
        q25 = np.percentile(image_array, 25)
        q75 = np.percentile(image_array, 75)
        
        # Symétrie
        h_sym = np.mean(image_array[:, :224]) - np.mean(image_array[:, 224:])
        v_sym = np.mean(image_array[:224, :]) - np.mean(image_array[224:, :])
        
        # Densité de contours
        edges = cv2.Canny((image_array * 255).astype(np.uint8), 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Aspect ratio
        aspect = 1.0
        
        # Histogram features (16 bins)
        hist = cv2.calcHist([image_array], [0], None, [16], [0, 1])
        features = list(hist.flatten())
        
        # Statistiques de base (8 features)
        features.extend([mean, std, q25, q75, h_sym, v_sym, edge_density, aspect])
        
        # Gradient features (2 features)
        grad_x = cv2.Sobel(image_array, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(image_array, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        features.append(np.mean(gradient_magnitude))
        features.append(np.std(gradient_magnitude))
        
        # Texture features (6 features supplémentaires)
        # Variance locale
        local_variance = ndimage.generic_filter(image_array, np.var, size=3)
        features.append(np.mean(local_variance))
        
        # Skewness (asymétrie)
        features.append(stats.skew(image_array.flatten()))
        
        # Kurtosis (aplatissement)
        features.append(stats.kurtosis(image_array.flatten()))
        
        # Entropy locale
        hist_local, _ = np.histogram(image_array.flatten(), bins=32)
        hist_local = hist_local / (hist_local.sum() + 1e-8)
        features.append(stats.entropy(hist_local))
        
        # Min et Max
        features.append(np.min(image_array))
        features.append(np.max(image_array))
        
        # Total: 16 + 8 + 2 + 6 = 32 features
        return np.array(features, dtype=np.float32)
        
    except Exception as e:
        return None

# Extraire features et labels
features_list = []
labels_list = []
failed = 0

for idx, row in train_data.iterrows():
    if (idx + 1) % 500 == 0:
        print(f"  Traité {idx + 1}/{len(train_data)} images...")
    
    # Chercher l'image
    study_id = row['study_id']
    image_id = row['image_id']
    image_path = get_image_path(study_id, image_id)
    
    if image_path is None:
        failed += 1
        continue
    
    # Extraire features
    features = extract_features_from_image(image_path)
    if features is None:
        failed += 1
        continue
    
    # Label
    view_name = f"{row['view_position']}_{row['laterality']}"
    
    features_list.append(features)
    labels_list.append(view_name)

print(f"\n✓ {len(features_list)} images extraites avec succès")
print(f"  {failed} images non trouvées ou en erreur")

if len(features_list) < 100:
    print("❌ Pas assez d'images trouvées ! Vérifiez les chemins.")
    exit(1)

# 4. Préparer les données
print("\n[4/6] Préparation des données d'entraînement...")

# Encoder les labels
view_classes = sorted(set(labels_list))
view_to_idx = {cls: idx for idx, cls in enumerate(view_classes)}
idx_to_view = {idx: cls for cls, idx in view_to_idx.items()}

print(f"Classes de vues: {view_classes}")

X = np.array(features_list)
y = np.array([view_to_idx[label] for label in labels_list])

# Split train/val
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"✓ Train: {len(X_train)}, Val: {len(X_val)}")

# Vérifier les dimensions
print(f"\nDimensions des données:")
print(f"  X shape: {X.shape}")
print(f"  X_train shape: {X_train.shape}")
print(f"  X_val shape: {X_val.shape}")

# 5. Créer le modèle
print("\n[5/6] Création du modèle...")

class ViewClassifier(nn.Module):
    def __init__(self, num_views=4):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(32, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_views)
        )
    
    def forward(self, x):
        return self.model(x)

model = ViewClassifier(num_views=len(view_classes))
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

print(f"✓ Modèle créé avec {sum(p.numel() for p in model.parameters())} paramètres")

# 6. Entraînement
print("\n[6/6] Entraînement...")

X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.LongTensor(y_train)
X_val_tensor = torch.FloatTensor(X_val)
y_val_tensor = torch.LongTensor(y_val)

best_val_acc = 0.0

for epoch in range(EPOCHS):
    # Training
    model.train()
    train_loss = 0.0
    
    for i in range(0, len(X_train), BATCH_SIZE):
        batch_X = X_train_tensor[i:i+BATCH_SIZE]
        batch_y = y_train_tensor[i:i+BATCH_SIZE]
        
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        
        train_loss += loss.item()
    
    avg_train_loss = train_loss / (len(X_train) / BATCH_SIZE)
    
    # Validation
    model.eval()
    with torch.no_grad():
        val_outputs = model(X_val_tensor)
        val_preds = torch.argmax(val_outputs, dim=1)
        
        # Convertir en numpy pour sklearn
        val_preds_np = val_preds.cpu().numpy()
        y_val_np = y_val if isinstance(y_val, np.ndarray) else y_val.numpy()
        
        val_acc = accuracy_score(y_val_np, val_preds_np)
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
    
    if (epoch + 1) % 10 == 0:
        print(f"  Epoch {epoch+1}/{EPOCHS}, Loss: {avg_train_loss:.4f}, Val Acc: {val_acc:.4f}")
        print(f"  Classes prévues: {[idx_to_view[int(p)] for p in val_preds_np[:10]]}")

print(f"\n✓ Meilleure validation accuracy: {best_val_acc:.4f}")

# 7. Rapport final
print("\n" + "=" * 70)
print("RAPPORT D'ÉVALUATION")
print("=" * 70)

model.eval()
with torch.no_grad():
    final_outputs = model(X_val_tensor)
    final_preds = torch.argmax(final_outputs, dim=1)

# Convertir en numpy
final_preds_np = final_preds.cpu().numpy()
y_val_np = y_val if isinstance(y_val, np.ndarray) else y_val.numpy()

print("\nClassification Report:")
print(classification_report(y_val_np, final_preds_np, 
                          target_names=view_classes))

# 8. Sauvegarder le modèle
print("\n" + "=" * 70)
print("SAUVEGARDE DU MODÈLE")
print("=" * 70)

checkpoint = {
    'view_classifier': model.state_dict(),
    'view_classes': view_classes,
    'view_to_idx': view_to_idx,
    'idx_to_view': idx_to_view,
    'num_view_classes': len(view_classes),
    'best_val_acc': best_val_acc,
    'num_samples': len(features_list)
}

# Sauvegarder
model_path = Path('model/view_classifier_trained.pth')
torch.save(checkpoint, str(model_path))
print(f"\n✓ Modèle sauvegardé: {model_path}")

print("\n" + "=" * 70)
print("ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS!")
print("=" * 70)
print(f"\nLe classifieur peut détecter les 4 vues avec {best_val_acc*100:.1f}% de précision.")
print("Vous pouvez maintenant l'utiliser dans inference_service_simple.py")

