# Réalité des Centres de Dépistage au Bénin

## ⚠️ Situation réelle

### Infrastructure limitée
- **Pas de radiothérapie** au Bénin (évacuation nécessaire vers d'autres pays)
- **Équipement limité**: Très peu de mammographes dans le pays
- **Centre principal**: CNHU (chirurgie et chimiothérapie)
- **Problème majeur**: 70% des patientes arrivent à un stade avancé

### Absence de données centralisées
**Il n'existe PAS de base de données officielle** des centres de dépistage du cancer du sein au Bénin. Les sources disponibles proviennent de:
1. Campagnes ponctuelles (Octobre Rose, initiatives politiques, ONG)
2. Publications mentionnant quelques hôpitaux
3. Hôpitaux majeurs connus (CNHU, CHU-MEL)

## 📋 Ce que nous avons fait

### Centres ajoutés (basés sur sources web)
Les centres suivants ont été ajoutés car ils apparaissent dans les sources disponibles:

1. **CNHU Hubert Koutoukou Maga** (Cotonou) - Hôpital national de référence
2. **CHU-MEL Lagune** (Cotonou) - Santé maternelle/infantile
3. **Hôpital de Zone Suru-Léré** (Cotonou)
4. **Hôpital de Zone Mènontin** (Cotonou)
5. **Hôpital de Zone Abomey-Calavi** (Atlantique)
6. **Hôpital Départemental du Borgou** (Parakou)
7. **Centre de Santé de Référence** (Bohicon, Zou)

### Informations manquantes
Pour chaque centre:
- ✅ Nom et ville (confirmés par sources)
- ❌ Téléphones (à vérifier)
- ❌ Email (à vérifier)
- ❌ Adresses complètes (à vérifier)
- ❌ Équipement spécifique mammographe (à vérifier)
- ❌ Horaires réels (à vérifier)

Tous les centres sont marqués **`is_verified: False`** pour indiquer qu'ils nécessitent une vérification.

## 🔄 Prochaines étapes OBLIGATOIRES

### 1. Contacter le Ministère de la Santé Bénin
- Demander une liste officielle des centres autorisés
- Obtenir coordonnées téléphoniques et emails
- Vérifier services réellement offerts
- Obtenir horaires d'ouverture

### 2. Visite sur le terrain (recommandée)
- Vérifier existence réelle des centres
- Prendre photos pour frontend
- Collecter informations de contact
- Confirmer services de dépistage

### 3. Mise à jour de la base de données
- Remplacer `None` par vraies valeurs
- Marquer centres vérifiés `is_verified: True`
- Ajouter équipements spécifiques
- Corriger coordonnées GPS si nécessaire

## 💡 Recommandation importante

**Pour l'instant, la base contient des centres existants mais avec des informations incomplètes.**

**Action recommandée**: Afficher un message aux utilisateurs:
> "Cette liste est basée sur les informations disponibles. Nous recommandons de contacter directement les centres pour confirmer les services et horaires."

## 📞 Contacts pour vérification

- **Ministère de la Santé Bénin**: http://sante.gouv.bj/
- **CNHU**: À contacter pour coordonnées exactes
- **Direction Nationale de la Santé Publique**: À contacter

## 🎯 Objectif final

Construire progressivement une base de données vérifiée et complète des centres de dépistage au Bénin, en collaboration avec les autorités sanitaires.

