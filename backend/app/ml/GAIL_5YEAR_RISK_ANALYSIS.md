# Analyse du Calcul du Risque 5 Ans

## Problèmes Identifiés

### 1. **Intercept non utilisé**
- Intercept défini : `-9.098`
- **PAS utilisé dans le calcul du risque relatif** (ligne 96: `log_rr = 0.0`)
- ⚠️ **Question : L'intercept doit-il être utilisé ?**

Dans le modèle Gail officiel, l'intercept peut servir à :
- Calibrer le risque absolu de base
- Normaliser par rapport à une population de référence

**Impact potentiel : CRITIQUE** - Si l'intercept doit être inclus, le calcul est incorrect.

### 2. **Coefficients β non vérifiés**
- Valeurs utilisées basées sur sources secondaires
- Non comparées avec Table 2 de Gail et al. (1989)
- ⚠️ **Risque : Valeurs incorrectes possible**

### 3. **Taux d'incidence SEER approximatifs**
- Valeurs dans `base_hazard_rates` sont approximatives
- Pas les valeurs exactes utilisées par le NCI
- ⚠️ **Impact : Risques absolus peuvent être légèrement incorrects**

### 4. **Calcul du risque absolu simplifié**
- Formule : `annual_prob * 5` (si < 0.01) ou `1 - (1 - p)^5`
- Le modèle officiel peut utiliser une intégration plus complexe
- ⚠️ **Impact : Peut différer de quelques pourcentages**

## Test de Cohérence

Exemple : Femme 50 ans, 1 parente
- Risque calculé : 0.346%
- Risque relatif : 1.1523x
- Augmentation vs 0 parente : 54.5%

**Cohérence interne : ✅ OK**
- Les facteurs de risque semblent se combiner correctement
- L'augmentation avec 1 parente est logique

## Verdict

**Le risque 5 ans PROBABLEMENT approximatif mais pas garanti exact.**

**Raisons :**
- ✅ Structure mathématique correcte
- ✅ Cohérence interne (facteurs se combinent bien)
- ❓ Intercept non utilisé (impact inconnu)
- ❓ Coefficients non vérifiés
- ❓ Taux SEER approximatifs
- ❓ Pas de validation empirique

**Score : 6-7/10** ⚠️

**Pour être sûr :**
1. ✅ Vérifier si l'intercept doit être utilisé
2. ✅ Extraire les coefficients exacts de l'article original
3. ✅ Obtenir les taux SEER exacts
4. ✅ Comparer avec bcrisktool.cancer.gov sur plusieurs cas

