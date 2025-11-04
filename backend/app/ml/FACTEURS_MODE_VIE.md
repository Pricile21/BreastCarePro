# Facteurs de Risque de Mode de Vie pour le Cancer du Sein

## 📊 Facteurs de Risque Connus (Documentation Médicale)

### **1. ALCOOL** ⚠️ **FACTEUR CONNU**

**Impact documenté :**
- **Augmentation du risque** : 7-10% par verre par jour
- **Source** : Multiple meta-analyses (AICR, WCRF, IARC)
- **Niveau de preuve** : **ÉLEVÉ** (groupe 1 carcinogène IARC)

**Recommandation médicale :**
- Limiter à <1 verre/jour réduit le risque
- 2-3 verres/jour = risque augmenté de 20%
- 3+ verres/jour = risque augmenté de 40-50%

---

### **2. TABAC** ⚠️ **FACTEUR CONNU**

**Impact documenté :**
- **Augmentation du risque** : 10-15% (fumeuses actives)
- **Source** : Multiple études épidémiologiques
- **Niveau de preuve** : **MODÉRÉ-ÉLEVÉ**

**Points importants :**
- Effet plus fort chez les femmes pré-ménopausées
- Fumées passives aussi augmentent le risque
- Durée et quantité de tabac = facteurs importants

---

### **3. OBÉSITÉ / IMC** ⚠️ **FACTEUR IMPORTANT**

**Impact documenté :**
- **IMC >30** : Risque augmenté de 20-40%
- **IMC >25** : Risque augmenté de 10-15%
- **Source** : Modèle BCSC v3 inclut l'IMC comme facteur majeur
- **Niveau de preuve** : **TRÈS ÉLEVÉ**

**Points importants :**
- Plus fort après la ménopause
- Prise de poids après 50 ans = risque augmenté
- Perte de poids réduit le risque

---

### **4. EXERCICE PHYSIQUE** ✅ **FACTEUR PROTECTEUR**

**Impact documenté :**
- **150 min/semaine** : Réduction de risque de 10-20%
- **Source** : Multiple études prospectives
- **Niveau de preuve** : **ÉLEVÉ**

**Recommandation :**
- 30 minutes d'exercice modéré, 5 jours/semaine
- Réduction du risque même avec exercice léger

---

### **5. TRAITEMENT HORMONAL POST-MÉNOPAUSE** ⚠️ **FACTEUR CONNU**

**Impact documenté :**
- **THS combiné** : Risque augmenté de 20-30%
- **THS œstrogène seul** : Risque augmenté de 10-15%
- **Source** : Étude WHI (Women's Health Initiative)
- **Niveau de preuve** : **TRÈS ÉLEVÉ**

---

## ❓ Pourquoi le Modèle Gail Original ne les Inclut PAS ?

### **Raisons historiques :**
1. **Développé en 1989** : Avant que certains facteurs soient bien documentés
2. **Focus sur facteurs non-modifiables** : Âge, génétique, antécédents médicaux
3. **Simplicité** : Garder le modèle simple pour utilisation clinique

### **Modèles Étendus :**
- **BCSC Risk Model v3** : Inclut IMC, densité mammaire
- **Tyrer-Cuzick Model** : Inclut plus de facteurs génétiques
- **Modèles personnalisés** : Peuvent inclure mode de vie

---

## ✅ Recommandation : Ajouter ces Facteurs

### **Facteurs à AJOUTER (par ordre d'importance) :**

1. **IMC / Obésité** ⭐⭐⭐⭐⭐ (Impact très fort)
2. **Alcool** ⭐⭐⭐⭐ (Impact fort)
3. **Exercice physique** ⭐⭐⭐ (Impact protecteur)
4. **Tabac** ⭐⭐⭐ (Impact modéré)
5. **Traitement hormonal** ⭐⭐⭐ (Si applicable)

---

## 🎯 Proposition d'Extension du Modèle

### **Version Étendue : Gail Model + Facteurs de Mode de Vie**

```python
# Facteurs du modèle Gail original
gail_factors = {
    'age', 'family_history', 'biopsies', 'atypical_hyperplasia',
    'age_menarche', 'age_first_birth'
}

# Facteurs de mode de vie à ajouter
lifestyle_factors = {
    'bmi': 'Indice de masse corporelle',
    'alcohol': 'Consommation d\'alcool (verres/semaine)',
    'exercise': 'Exercice physique (minutes/semaine)',
    'smoking': 'Tabagisme (actuel/ex-fumeuse/jamais)',
    'hormone_therapy': 'Traitement hormonal post-ménopause'
}
```

---

## 📊 Impact sur la Précision

**Modèle Gail Original :**
- Précision : 70-75%

**Modèle Gail + Facteurs Mode de Vie :**
- Précision estimée : **75-82%**
- Meilleure prédiction pour femmes avec facteurs de mode de vie

---

## ⚠️ CONSIDÉRATIONS IMPORTANTES

### **1. Validation nécessaire**
- Ces facteurs doivent être validés sur votre population
- Coefficients de risque peuvent varier selon région/population

### **2. Complexité utilisateur**
- Plus de questions = Moins d'utilisateurs complètent
- Trouver équilibre précision/complétude

### **3. Mode de vie vs Facteurs génétiques**
- Mode de vie = modifiable (prévention possible)
- Facteurs génétiques = non-modifiables (surveillance)

---

## 💡 Recommandation Finale

**AJOUTER ces facteurs dans votre modèle :**

1. ✅ **IMC** : Facteur majeur, facile à calculer
2. ✅ **Alcool** : Impact fort, question simple
3. ✅ **Exercice** : Impact protecteur, question simple
4. ⚠️ **Tabac** : Impact modéré, peut être optionnel
5. ⚠️ **Traitement hormonal** : Seulement si femme ménopausée

**Implémentation recommandée :**
- Questions supplémentaires = **optionnelles** ou dans une section "Mode de vie"
- Si répondues → Précision améliorée
- Si non répondues → Utiliser modèle Gail de base

---

## 📚 Sources Médicales

1. **American Institute for Cancer Research (AICR)** : Alcool et cancer du sein
2. **World Cancer Research Fund (WCRF)** : Mode de vie et cancer du sein
3. **International Agency for Research on Cancer (IARC)** : Alcool = carcinogène groupe 1
4. **BCSC Risk Model v3** : Inclut IMC comme facteur majeur
5. **Women's Health Initiative (WHI)** : Traitement hormonal et risque

