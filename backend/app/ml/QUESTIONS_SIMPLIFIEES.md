# Questions Utilisateur Lambda - Version Simplifiée

## ✅ QUESTIONS SIMPLIFIÉES POUR UTILISATEURS NON-MÉDICAUX

### **SECTION 1 : Questions Essentielles (6 questions)**

#### **1. Âge**
```
Question : "Quel est votre âge ?"
Réponse : 45 ans
```
✅ **Simple** : Tout le monde connaît son âge

---

#### **2. Antécédents familiaux**
```
Question : "Votre mère ou l'une de vos sœurs a-t-elle eu un cancer du sein ?"
Options :
  - Non, aucune
  - Oui, une (mère OU une sœur)
  - Oui, deux ou plus
Réponse : Exemple : "Oui, une"
```
✅ **Simple** : Question claire sur la famille proche

---

#### **3. Prélèvement du sein**
```
Question : "Avez-vous déjà eu un examen médical où un médecin a prélevé 
            un petit morceau de votre sein pour l'analyser ?"
Options :
  - Non, jamais
  - Oui, une fois
  - Oui, plusieurs fois
Aide : "Si vous n'êtes pas sûre, répondez 'Non' - c'est normal"
Réponse : Exemple : "Non, jamais"
```
✅ **Simplifié** : Explication simple de ce qu'est un prélèvement (pas besoin de connaître le mot "biopsie")

---

#### **4. Cellules anormales (SEULEMENT si prélèvement = Oui)**
```
Question : "Si vous avez eu un prélèvement du sein, un médecin vous a-t-il dit 
            que les cellules n'étaient pas tout à fait normales (mais que ce n'était pas un cancer) ?"
Réponse : Oui/Non
Aide : "Si vous ne savez pas, répondez 'Non' - c'est très rare"
```
✅ **Conditionnelle** : Question apparaît seulement si question 3 = Oui
✅ **Simplifié** : Explication claire (pas besoin de connaître "hyperplasie atypique")

---

#### **5. Premières règles**
```
Question : "À quel âge avez-vous eu vos premières règles ?"
Options :
  - Avant 12 ans
  - Entre 12 et 13 ans
  - 14 ans ou plus
Réponse : Exemple : "Entre 12 et 13 ans"
```
✅ **Simple** : Question personnelle compréhensible

---

#### **6. Premier enfant**
```
Question : "À quel âge avez-vous eu votre premier enfant ?"
Options :
  - Avant 20 ans
  - Entre 20 et 24 ans
  - Entre 25 et 29 ans
  - 30 ans ou plus
  - Je n'ai pas d'enfant
Réponse : Exemple : "Entre 25 et 29 ans"
```
✅ **Simple** : Question claire avec option "pas d'enfant"

---

### **SECTION 2 : Questions Mode de Vie (Optionnelles)**

#### **7. Poids**
```
Question : "Quel est votre poids actuel ?"
Réponse : 70 kg
Aide : "En kilogrammes. Exemple : si vous pesez 70 kilos, écrivez 70"
```
✅ **Simple** : Pas besoin de connaître IMC

---

#### **8. Taille**
```
Question : "Quelle est votre taille ?"
Réponse : 170 cm
Aide : "En centimètres. Exemple : 1 mètre 70 = 170 cm (écrivez 170)"
```
✅ **Simple** : Exemple concret

**Note** : L'IMC est calculé automatiquement : IMC = poids / (taille/100)²

---

#### **9. Alcool**
```
Question : "Combien de verres d'alcool buvez-vous par semaine ?"
Réponse : 5 verres
Aide : "1 verre = 1 verre de vin, 1 bière, ou 1 shot de spiritueux. 
        Si vous ne buvez pas d'alcool, écrivez 0."
```
✅ **Simple** : Exemples concrets de ce qu'est "1 verre"

---

#### **10. Exercice**
```
Question : "Combien de minutes par semaine faites-vous de sport ou d'exercice physique ?"
Réponse : 120 minutes
Aide : "Exemples : marche rapide, vélo, natation, course, gym, etc. 
        Si vous ne faites pas de sport, écrivez 0."
```
✅ **Simple** : Exemples concrets d'exercices

---

#### **11. Tabac**
```
Question : "Fumez-vous actuellement ?"
Options :
  - Non, je n'ai jamais fumé
  - Non, j'ai arrêté de fumer
  - Oui, je fume actuellement
Réponse : Exemple : "Non, je n'ai jamais fumé"
```
✅ **Simple** : Question directe

---

#### **12. Traitement hormonal (SEULEMENT si âge ≥50)**
```
Question : "Prenez-vous un traitement hormonal pour la ménopause (pilules ou patchs) ?"
Réponse : Oui/Non
Aide : "Seulement si vous êtes ménopausée (arrêt des règles) et prenez 
        un traitement hormonal prescrit par un médecin"
```
✅ **Conditionnelle** : Question apparaît seulement si âge ≥50 ans
✅ **Simplifié** : Explication de ce qu'est la ménopause

---

## 📊 IMPACT DE CHAQUE QUESTION SUR LE CALCUL

### **Questions Requises (Impact sur Risque Gail)**

| Question | Réponse | Impact |
|----------|---------|--------|
| **Âge** | 45 ans | Risque de base : 0.05% |
| **Antécédents** | 1 parente | ×2.0 (risque doublé) |
| **Prélèvement** | 1 fois | ×2.0 (risque doublé) |
| **Cellules anormales** | Non | ×1.0 (pas d'impact) |
| **Premières règles** | 12-13 ans | ×1.0 (pas d'impact) |
| **Premier enfant** | 25-29 ans | ×1.0 (pas d'impact) |

**Risque Gail = 0.05% × 2.0 × 2.0 × 1.0 × 1.0 × 1.0 = 0.2%**

---

### **Questions Mode de Vie (Ajustement)**

| Question | Réponse | Impact |
|----------|---------|--------|
| **Poids/Taille** | 80kg, 170cm (IMC=27.7) | ×1.15 (+15%) |
| **Alcool** | 5 verres/semaine | ×1.08 (+8%) |
| **Exercice** | 120 min/semaine | ×0.95 (-5%) |
| **Tabac** | Jamais fumé | ×1.0 (pas d'impact) |
| **THS** | Non | ×1.0 (pas d'impact) |

**Ajustement Mode de Vie = 1.15 × 1.08 × 0.95 × 1.0 × 1.0 = 1.18**

---

### **Risque Final**

```
Risque Final = Risque Gail × Ajustement Mode de Vie
Risque Final = 0.2% × 1.18 = 0.236% ≈ 0.24%
```

---

## ✅ RÉSUMÉ DES AMÉLIORATIONS

### **Avant** ❌
- "Avez-vous eu une biopsie ?" → Confus
- "Hyperplasie atypique ?" → Incompréhensible
- "Quel est votre IMC ?" → Inconnu

### **Après** ✅
- "Avez-vous eu un examen où un médecin a prélevé un petit morceau ?" → Clair
- "Médecin a dit que les cellules n'étaient pas normales ?" → Compréhensible
- "Quel est votre poids ?" + "Quelle est votre taille ?" → Simple

**Toutes les questions sont maintenant compréhensibles par un utilisateur lambda !** ✅

