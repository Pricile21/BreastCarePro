# Résultats de Validation du Modèle Gail

## Objectif
Comparer notre implémentation avec le calculateur officiel NCI : https://bcrisktool.cancer.gov/

## Instructions
1. Exécuter : `python -m app.ml.validate_gail_nci`
2. Entrer chaque cas de test dans bcrisktool.cancer.gov
3. Noter les résultats officiels
4. Comparer avec nos résultats
5. Documenter les écarts ici

---

## Cas de Test 1 : Femme 45 ans, profil moyen

### Données
- Age: 45
- Ménarche: 12-13
- Premier enfant: 25-29
- Biopsies: 0
- Hyperplasie atypique: Non
- Parentes au 1er degré: 0

### Nos Résultats
- Risque 5 ans: ___%
- Risque à vie: ___%

### Résultats NCI Officiel
- Risque 5 ans: ___%
- Risque à vie: ___%

### Écart
- Risque 5 ans: ___% (différence absolue)
- Risque à vie: ___% (différence absolue)
- Acceptable ? (écart < 5%)

---

## Cas de Test 2 : Femme 50 ans, 1 parente

### Données
- Age: 50
- Ménarche: 12-13
- Premier enfant: 25-29
- Biopsies: 0
- Hyperplasie atypique: Non
- Parentes au 1er degré: 1

### Nos Résultats
- Risque 5 ans: ___%
- Risque à vie: ___%

### Résultats NCI Officiel
- Risque 5 ans: ___%
- Risque à vie: ___%

### Écart
- Risque 5 ans: ___%
- Risque à vie: ___%
- Acceptable ?

---

## Analyse de l'Intercept

### Intercept dans notre code
- Valeur définie : -9.098
- Utilisé dans le calcul ? : NON (ligne 96 : `log_rr = 0.0`)

### Usage de l'intercept dans le modèle Gail officiel
À documenter après consultation de :
- Article original Gail et al. (1989)
- Macro SAS NCI
- Calculateur officiel

### Hypothèses
1. L'intercept sert à calibrer le risque absolu, pas le risque relatif
2. L'intercept est inclus dans la normalisation des taux SEER
3. L'intercept doit être ajouté au log(RR) avant calcul du risque absolu

---

## Conclusion

### Validé ✅
- [ ] Cas 1 : Risque 5 ans conforme
- [ ] Cas 2 : Risque 5 ans conforme
- [ ] Cas 3 : Risque 5 ans conforme
- [ ] Cas 4 : Risque 5 ans conforme
- [ ] Cas 5 : Risque 5 ans conforme

### Problèmes identifiés
1. 
2. 
3. 

### Actions correctives nécessaires
1. 
2. 
3. 

---

## Date de Validation
Date : __/__/____
Validé par : __________

