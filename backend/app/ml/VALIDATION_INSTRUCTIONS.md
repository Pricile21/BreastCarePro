# Instructions de Validation du Modèle Gail

## Objectif
Valider notre implémentation du modèle Gail en comparant avec le calculateur officiel NCI.

## Étape 1 : Générer les Cas de Test

```bash
python -m app.ml.validate_gail_nci
```

Ce script génère 5 cas de test avec :
- Les données à entrer dans bcrisktool.cancer.gov
- Nos résultats calculés
- Les risques relatifs techniques

## Étape 2 : Tester avec le Calculateur Officiel

1. Ouvrir : https://bcrisktool.cancer.gov/
2. Pour chaque cas de test :
   - Entrer les données indiquées
   - Noter les résultats officiels (risque 5 ans et risque à vie)
   - Comparer avec nos résultats

## Étape 3 : Documenter les Résultats

Remplir le fichier `GAIL_VALIDATION_RESULTS.md` avec :
- Les résultats officiels NCI pour chaque cas
- Les écarts entre nos résultats et les résultats officiels
- Analyse des différences

## Étape 4 : Analyser les Écarts

### Si écarts < 2-3% :
✅ **Validation réussie** - Notre implémentation est correcte

### Si écarts 3-10% :
⚠️ **Corrections mineures nécessaires** :
- Vérifier les coefficients β exacts
- Ajuster les taux SEER
- Affiner le calcul du risque absolu

### Si écarts > 10% :
❌ **Corrections majeures nécessaires** :
- Revoir l'utilisation de l'intercept
- Vérifier la formule mathématique
- Revoir tous les coefficients

## Points Clés à Vérifier

### 1. Intercept
- **Problème actuel** : Intercept défini (-9.098) mais non utilisé
- **À vérifier** : Si l'intercept doit être inclus dans le calcul
- **Méthode** : Comparer nos résultats avec officiel → Si systématiquement différent, intercept mal utilisé

### 2. Coefficients β
- **Problème actuel** : Basés sur sources secondaires
- **Solution** : Extraire de l'article original Gail et al. (1989)
- **Référence** : Table 2 de l'article

### 3. Taux d'Incidence SEER
- **Problème actuel** : Valeurs approximatives
- **Solution** : Obtenir les taux exacts du NCI/SEER

### 4. Risque à Vie
- **Problème actuel** : Approximation simplifiée
- **Solution** : Implémenter l'intégration exacte si écart important

## Prochaines Actions Recommandées

Une fois les résultats de validation obtenus :

1. **Si validé** → Documenter la validation et utiliser en production
2. **Si corrections nécessaires** → Ajuster le code selon les écarts identifiés
3. **Réitérer** → Re-valider après corrections

## Ressources

- Calculateur officiel : https://bcrisktool.cancer.gov/
- Macro SAS NCI : https://dceg.cancer.gov/tools/risk-assessment/bcrasasmacro
- Article original : Gail et al. (1989), JNCI, Vol. 81, No. 24

