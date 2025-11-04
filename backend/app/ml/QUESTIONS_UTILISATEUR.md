# Questions Utilisateur-Friendly pour Calculatrice de Risque

## ✅ Questions Simplifiées pour Utilisateurs Non-Médicaux

### 1. **Âge**
- **Question** : "Quel est votre âge ?"
- **Type** : Nombre (18-90 ans)
- **✅ Simple** : Tout le monde connaît son âge

---

### 2. **Antécédents familiaux**
- **Question** : "Votre mère ou l'une de vos sœurs a-t-elle eu un cancer du sein ?"
- **Options** :
  - Non, aucune
  - Oui, une (mère OU une sœur)
  - Oui, deux ou plus (mère ET sœur, ou plusieurs sœurs)
- **✅ Simple** : Questions claires sur la famille proche
- **Aide** : "Comptez seulement votre mère et vos sœurs biologiques"

---

### 3. **Biopsie**
- **Question** : "Avez-vous déjà eu un prélèvement (biopsie) du sein effectué par un médecin ?"
- **Options** :
  - Non, jamais
  - Oui, une fois
  - Oui, deux fois ou plus
- **✅ Simple** : Explication du terme "prélèvement" entre parenthèses
- **Aide** : "Si vous n'êtes pas sûre, vous pouvez répondre 'Non'"

---

### 4. **Hyperplasie atypique** (OPTIONNEL)
- **Question** : "Lors d'un prélèvement du sein, un médecin vous a-t-il dit que vous aviez des cellules anormales (mais pas un cancer) ?"
- **Options** : Oui / Non
- **✅ Optionnel** : L'utilisateur peut dire "Je ne sais pas"
- **Aide** : "Si vous ne savez pas, répondez 'Non' - cela concerne des résultats de biopsie spécifiques"

---

### 5. **Âge des premières règles**
- **Question** : "À quel âge avez-vous eu vos premières règles ?"
- **Options** :
  - Avant 12 ans
  - Entre 12 et 13 ans
  - 14 ans ou plus
- **✅ Simple** : Question personnelle compréhensible

---

### 6. **Âge du premier enfant**
- **Question** : "À quel âge avez-vous eu votre premier enfant ?"
- **Options** :
  - Avant 20 ans
  - Entre 20 et 24 ans
  - Entre 25 et 29 ans
  - 30 ans ou plus
  - Je n'ai pas d'enfant
- **✅ Simple** : Question claire avec option "pas d'enfant"

---

## 🎯 Règles de Design

### ✅ À FAIRE
- Utiliser un langage simple et familier
- Expliquer les termes médicaux entre parenthèses
- Proposer des options plutôt que des champs numériques
- Permettre "Je ne sais pas" pour les questions médicales
- Ajouter des textes d'aide rassurants

### ❌ À ÉVITER
- Termes techniques médicaux sans explication
- Questions trop précises que l'utilisateur ne peut pas connaître
- Forcer une réponse si l'utilisateur ne sait pas
- Questions effrayantes ou alarmantes

---

## 📱 Exemple d'Interface Mobile

```
┌─────────────────────────────────┐
│  Calculatrice de Risque         │
│  Cancer du Sein                 │
├─────────────────────────────────┤
│                                  │
│  Votre mère ou l'une de vos     │
│  sœurs a-t-elle eu un cancer    │
│  du sein ?                       │
│                                  │
│  ○ Non, aucune                  │
│  ○ Oui, une (mère OU sœur)      │
│  ○ Oui, deux ou plus            │
│                                  │
│  ℹ️ Comptez seulement votre     │
│     mère et sœurs biologiques   │
│                                  │
│  [ ← Précédent ] [ Suivant → ]  │
└─────────────────────────────────┘
```

---

## ⚠️ Important

**Toutes les questions peuvent avoir une option "Je ne préfère pas répondre"** qui utilisera une valeur par défaut prudente (valeur la plus sûre).

