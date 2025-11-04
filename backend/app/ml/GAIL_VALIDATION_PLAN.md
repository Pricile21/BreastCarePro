# Plan de Validation du Modèle Gail Officiel

## Problème

Les coefficients actuellement utilisés doivent être validés contre les sources officielles publiées.

## Sources Officielles à Consulter

1. **Article Original** : 
   - Gail et al. (1989) "Projecting individualized probabilities of developing breast cancer"
   - Journal of the National Cancer Institute, Vol. 81, No. 24
   - Doi: 10.1093/jnci/81.24.1879

2. **Macro SAS Officielle du NCI** :
   - https://dceg.cancer.gov/tools/risk-assessment/bcrasasmacro
   - Contient la formule exacte et les coefficients validés

3. **Calculateur Officiel NCI** :
   - https://bcrisktool.cancer.gov/
   - Pour validation des résultats

## Coefficients à Valider

Les valeurs suivantes doivent être vérifiées dans l'article original :

```python
# Intercept
'intercept': -9.098

# Âge
'age_coef': 0.029
'age_squared_coef': -0.0002

# Ménarche
'menarche_lt12': 0.2192
'menarche_14plus': -0.1736

# Premier enfant
'birth_age_20_24': -0.2684
'birth_age_30plus': 0.0733
'nulliparous': 0.1386

# Biopsies
'biopsy_1': 0.4384
'biopsy_2plus': 0.5805

# Hyperplasie atypique
'atypical_hyperplasia': 0.9675

# Antécédents familiaux
'relatives_1': 0.4353
'relatives_2plus': 0.7674
```

## Actions Requises

1. **Obtenir l'article original** (PDF ou accès bibliothèque)
2. **Extraire les coefficients de la Table 2** (ou table équivalente)
3. **Comparer avec les valeurs actuelles**
4. **Mettre à jour si nécessaire**
5. **Valider avec des cas de test** contre bcrisktool.cancer.gov

## Statut Actuel

⚠️ **À VALIDER** - Les coefficients doivent être vérifiés avant usage médical

