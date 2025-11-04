# Questions Utilisateur et Calcul du Risque

## 📋 QUESTIONS À POSER À L'UTILISATEUR

### **SECTION 1 : Questions Requises (Modèle Gail)**

#### **1. Âge**
```
Question : "Quel est votre âge ?"
Type : Nombre (18-90 ans)
Réponse : Exemple : 45 ans
```

**Impact sur le calcul :**
- Plus l'âge est élevé, plus le risque de base augmente
- Exemple : 
  - 30 ans → risque de base : 0.0001
  - 45 ans → risque de base : 0.0005
  - 60 ans → risque de base : 0.0018
- Formule : `base_risk = coefficients['age_base'][age_group]`

---

#### **2. Antécédents familiaux**
```
Question : "Votre mère ou l'une de vos sœurs a-t-elle eu un cancer du sein ?"
Type : Sélection
Options :
  - Non, aucune (0)
  - Oui, une (mère OU une sœur) (1)
  - Oui, deux ou plus (mère ET sœur, ou plusieurs sœurs) (2)
Réponse : Exemple : 1 (une parente)
```

**Impact sur le calcul :**
- 0 parente → facteur = 1.0 (pas d'augmentation)
- 1 parente → facteur = 2.0 (risque doublé)
- 2+ parentes → facteur = 3.0 (risque triplé)
- Formule : `family_factor = 1.0 + coefficients['family_history'][nombre]`

---

#### **3. Biopsies précédentes**
```
Question : "Avez-vous déjà eu un prélèvement (biopsie) du sein effectué par un médecin ?"
Type : Sélection
Options :
  - Non, jamais (0)
  - Oui, une fois (1)
  - Oui, deux fois ou plus (2)
Réponse : Exemple : 1 (une fois)
```

**Impact sur le calcul :**
- 0 biopsie → facteur = 1.0
- 1 biopsie → facteur = 2.0 (risque doublé)
- 2+ biopsies → facteur = 2.5 (risque × 2.5)
- Formule : `biopsy_factor = 1.0 + coefficients['biopsy'][nombre]`

---

#### **4. Hyperplasie atypique**
```
Question : "Lors d'un prélèvement du sein, un médecin vous a-t-il dit que vous aviez 
            des cellules anormales (mais pas un cancer) ?"
Type : Oui/Non
Réponse : Exemple : Non (False)
```

**Impact sur le calcul :**
- Non → facteur = 1.0
- Oui → facteur = 1.5 (risque augmenté de 50%)
- Formule : `hyperplasia_factor = 1.5 if True else 1.0`

---

#### **5. Âge première menstruation**
```
Question : "À quel âge avez-vous eu vos premières règles ?"
Type : Sélection
Options :
  - Avant 12 ans ("<12")
  - Entre 12 et 13 ans ("12-13")
  - 14 ans ou plus ("14+")
Réponse : Exemple : "12-13"
```

**Impact sur le calcul :**
- "<12" → facteur = 1.2 (risque augmenté de 20%)
- "12-13" → facteur = 1.0 (risque normal)
- "14+" → facteur = 0.9 (risque réduit de 10%)
- Formule : `menarche_factor = coefficients['age_menarche'][réponse]`

---

#### **6. Âge premier enfant**
```
Question : "À quel âge avez-vous eu votre premier enfant ?"
Type : Sélection
Options :
  - Avant 20 ans ("<20")
  - Entre 20 et 24 ans ("20-24")
  - Entre 25 et 29 ans ("25-29")
  - 30 ans ou plus ("30+")
  - Je n'ai pas d'enfant ("nulliparous")
Réponse : Exemple : "25-29"
```

**Impact sur le calcul :**
- "<20" → facteur = 1.0
- "20-24" → facteur = 0.9 (risque réduit de 10%)
- "25-29" → facteur = 1.0
- "30+" → facteur = 1.1 (risque augmenté de 10%)
- "nulliparous" → facteur = 1.2 (risque augmenté de 20%)
- Formule : `birth_factor = coefficients['first_birth'][réponse]`

---

### **SECTION 2 : Questions Optionnelles (Mode de Vie)**

#### **7. Poids et Taille**
```
Question 7a : "Quel est votre poids ?"
Type : Nombre (30-200 kg)
Réponse : Exemple : 70 kg

Question 7b : "Quelle est votre taille ?"
Type : Nombre (100-250 cm)
Réponse : Exemple : 170 cm
```

**Calcul automatique :**
- IMC = poids (kg) / (taille(m))²
- Exemple : IMC = 70 / (1.70)² = 24.2

**Impact sur le calcul :**
- Si IMC ≥30 ET âge ≥50 :
  - Ajustement = ×1.30 (risque augmenté de 30%)
- Si IMC ≥30 ET âge <50 :
  - Ajustement = ×1.15 (risque augmenté de 15%)
- Si IMC ≥25 ET âge ≥50 :
  - Ajustement = ×1.15 (risque augmenté de 15%)
- Si IMC ≥25 ET âge <50 :
  - Ajustement = ×1.08 (risque augmenté de 8%)
- Si IMC normal (<25) :
  - Ajustement = ×1.0 (pas d'impact)

---

#### **8. Consommation d'alcool**
```
Question : "Combien de verres d'alcool buvez-vous par semaine ?"
Type : Nombre (0-50)
Aide : "1 verre = 1 verre de vin, 1 bière, ou 1 shot de spiritueux"
Réponse : Exemple : 5 verres/semaine
```

**Impact sur le calcul :**
- 0-2 verres/semaine → ajustement = ×1.0 (pas d'impact)
- 3-6 verres/semaine → ajustement = ×1.08 (+8%)
- 7-13 verres/semaine (≈1 verre/jour) → ajustement = ×1.15 (+15%)
- 14+ verres/semaine (≥2 verres/jour) → ajustement = ×1.30 (+30%)

---

#### **9. Exercice physique**
```
Question : "Combien de minutes d'exercice physique modéré faites-vous par semaine ?"
Type : Nombre (0-1000)
Aide : "Exercice modéré = marche rapide, vélo, natation, etc."
Réponse : Exemple : 120 minutes/semaine
```

**Impact sur le calcul (facteur PROTECTEUR) :**
- 0-29 min/semaine → ajustement = ×1.0 (pas de protection)
- 30-74 min/semaine → ajustement = ×0.95 (-5%)
- 75-149 min/semaine → ajustement = ×0.90 (-10%)
- 150+ min/semaine → ajustement = ×0.85 (-15%)

---

#### **10. Tabagisme**
```
Question : "Quel est votre statut concernant le tabac ?"
Type : Sélection
Options :
  - Je n'ai jamais fumé ("never")
  - J'ai arrêté de fumer ("former")
  - Je fume actuellement ("current")
Réponse : Exemple : "never"
```

**Impact sur le calcul :**
- Jamais fumé → ajustement = ×1.0 (pas d'impact)
- Ex-fumeuse → ajustement = ×1.03 (+3%)
- Fumeuse actuelle (âge <50) → ajustement = ×1.20 (+20%)
- Fumeuse actuelle (âge ≥50) → ajustement = ×1.12 (+12%)

---

#### **11. Traitement hormonal**
```
Question : "Prenez-vous un traitement hormonal pour la ménopause ?"
Type : Oui/Non
Condition : Seulement si âge ≥50 ans
Réponse : Exemple : Non (False)
```

**Impact sur le calcul :**
- Non → ajustement = ×1.0 (pas d'impact)
- Oui (si âge ≥50) → ajustement = ×1.25 (+25%)

---

## 🧮 CALCUL COMPLET DU RISQUE

### **Étape 1 : Calcul du Risque Gail (Base)**

```python
# 1. Risque de base selon l'âge
age = 45
age_group = 45  # Arrondi à tranche de 5 ans → 45
base_risk = 0.0005  # Exemple pour 45 ans

# 2. Facteurs Gail
family_factor = 1.0 + 1.0 = 2.0  # 1 parente
biopsy_factor = 1.0 + 1.0 = 2.0  # 1 biopsie
hyperplasia_factor = 1.0  # Pas d'hyperplasie
menarche_factor = 1.0  # "12-13"
birth_factor = 1.0  # "25-29"

# 3. Risque relatif Gail
relative_risk = 2.0 × 2.0 × 1.0 × 1.0 × 1.0 = 4.0

# 4. Risque Gail pur (sur 5 ans)
risk_gail_pure = 0.0005 × 4.0 × 100 = 0.2% → 0.2%
```

**Exemple avec valeurs réelles :**
```python
age = 45
first_degree_relatives = 1
previous_biopsies = 1
atypical_hyperplasia = False
age_menarche = "12-13"
age_first_birth = "25-29"

# Calcul
base_risk = 0.0005  # Pour 45 ans
family_factor = 2.0  # 1 parente
biopsy_factor = 2.0  # 1 biopsie
hyperplasia_factor = 1.0
menarche_factor = 1.0
birth_factor = 1.0

relative_risk = 2.0 × 2.0 × 1.0 × 1.0 × 1.0 = 4.0
risk_gail_pure = 0.0005 × 4.0 × 100 = 0.2%
```

---

### **Étape 2 : Ajustement Mode de Vie**

```python
# Exemple utilisateur
weight_kg = 80
height_cm = 170
alcohol = 5  # verres/semaine
exercise = 120  # minutes/semaine
smoking = "never"
hormone_therapy = False

# 1. Calcul IMC
bmi = 80 / (1.70)² = 27.7

# 2. Calcul ajustements
bmi_adjustment = 1.15  # IMC 27.7, âge 45 (<50)
alcohol_adjustment = 1.08  # 5 verres/semaine
exercise_adjustment = 0.95  # 120 min/semaine (30-74)
smoking_adjustment = 1.0  # Jamais fumé
hormone_adjustment = 1.0  # Pas de THS

# 3. Ajustement total mode de vie
lifestyle_adjustment = 1.15 × 1.08 × 0.95 × 1.0 × 1.0
                     = 1.1799 ≈ 1.18
```

---

### **Étape 3 : Risque Final**

```python
# Risque final ajusté
risk_5_years = risk_gail_pure × lifestyle_adjustment
risk_5_years = 0.2% × 1.18 = 0.236% ≈ 0.24%

# Impact du mode de vie
lifestyle_impact = ((0.24 / 0.2) - 1) × 100 = +18%
```

---

## 📊 EXEMPLE COMPLET

### **Utilisateur :**
- Âge : 45 ans
- Antécédents : 1 parente (mère)
- Biopsies : 1 précédente
- Hyperplasie : Non
- Menstruation : 12-13 ans
- Premier enfant : 25-29 ans
- Poids : 80 kg, Taille : 170 cm (IMC = 27.7)
- Alcool : 5 verres/semaine
- Exercice : 120 min/semaine
- Tabac : Jamais fumé
- THS : Non

### **Calcul :**

**Étape 1 : Risque Gail**
```
base_risk (45 ans) = 0.0005
family_factor (1 parente) = 2.0
biopsy_factor (1 biopsie) = 2.0
hyperplasia_factor = 1.0
menarche_factor = 1.0
birth_factor = 1.0

relative_risk = 2.0 × 2.0 × 1.0 × 1.0 × 1.0 = 4.0
risk_gail_pure = 0.0005 × 4.0 × 100 = 0.2%
```

**Étape 2 : Mode de Vie**
```
bmi_adjustment (27.7, <50) = 1.15
alcohol_adjustment (5 verres) = 1.08
exercise_adjustment (120 min) = 0.95
smoking_adjustment (never) = 1.0
hormone_adjustment (no) = 1.0

lifestyle_adjustment = 1.15 × 1.08 × 0.95 × 1.0 × 1.0 = 1.18
```

**Étape 3 : Risque Final**
```
risk_5_years = 0.2% × 1.18 = 0.236% ≈ 0.24%
lifestyle_impact = +18%
```

### **Résultat :**
- Risque Gail pur : **0.2%**
- Risque ajusté : **0.24%**
- Impact mode de vie : **+18%**

---

## 🎯 FORMULE FINALE

```
Risque Final = Base_Risk × Family_Factor × Biopsy_Factor × 
               Hyperplasia_Factor × Menarche_Factor × Birth_Factor ×
               BMI_Adjustment × Alcohol_Adjustment × Exercise_Adjustment ×
               Smoking_Adjustment × Hormone_Adjustment × 100
```

**Où :**
- Base_Risk = Fonction de l'âge (0.0001 à 0.0045)
- Facteurs Gail = Entre 0.9 et 3.0
- Ajustements Mode de Vie = Entre 0.85 et 1.30

---

## ✅ RÉSUMÉ

**Questions Requises (6)** : Âge, Antécédents, Biopsies, Hyperplasie, Menstruation, Enfant
**Questions Optionnelles (5)** : Poids/Taille, Alcool, Exercice, Tabac, THS

**Chaque réponse modifie un facteur dans le calcul final.**

Voulez-vous que je crée un exemple interactif pour tester le calcul ?

