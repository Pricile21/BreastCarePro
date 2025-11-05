# Guide : Voir les Logs Détaillés sur Render

## Comment Voir les Logs du Backend sur Render

### Méthode 1 : Via l'Interface Web Render

1. Allez sur https://dashboard.render.com
2. Cliquez sur votre service **breastcare-backend**
3. Dans le menu de gauche, cliquez sur **"Logs"**
4. Vous verrez les logs en temps réel

### Méthode 2 : Filtrer les Logs

Pour voir uniquement les logs de l'analyse :

1. Dans la page **Logs**, utilisez la barre de recherche en haut
2. Recherchez : `[ANALYSE]` ou `[SERVICE]` ou `[MIDDLEWARE]`
3. Cela filtrera les logs pour ne montrer que les requêtes d'analyse

### Méthode 3 : Logs en Temps Réel

1. Sur la page **Logs**, cliquez sur **"Live tail"** (si disponible)
2. Ou gardez la page ouverte et rafraîchissez régulièrement
3. Les nouveaux logs apparaîtront automatiquement

## Que Rechercher dans les Logs

### Si la Requête Arrive au Backend

Vous devriez voir :
```
================================================================================
🌐 [MIDDLEWARE] REQUÊTE REÇUE: POST /api/v1/mammography/analyze
🌐 [MIDDLEWARE] Timestamp: 2025-11-05T...
🌐 [MIDDLEWARE] Client: ...
📦 [MIDDLEWARE] Body info: Content-Type=multipart/form-data, Length=...
================================================================================

🔍 [ANALYSE] Début de l'analyse - ...
🔍 [ANALYSE] Patient ID: ...
🔍 [ANALYSE] Nombre de fichiers: 4
```

### Si la Requête N'Arrive PAS au Backend

Si vous ne voyez **AUCUN** log `[MIDDLEWARE]` pour `/api/v1/mammography/analyze` :

**Causes possibles :**
1. **Problème CORS** - Le frontend ne peut pas envoyer la requête
2. **Backend endormi** - Sur le plan gratuit, le backend "s'endort" après 15 minutes d'inactivité
3. **URL incorrecte** - Le frontend pointe vers une mauvaise URL
4. **Timeout avant d'atteindre le backend** - La requête expire avant d'arriver

**Solutions :**
- Vérifiez que `NEXT_PUBLIC_API_URL` est correct dans les variables d'environnement du frontend
- Attendez 30-50 secondes après avoir lancé l'analyse (le backend peut être en train de se réveiller)
- Vérifiez les logs du frontend pour voir s'il y a des erreurs CORS

### Si la Requête Arrive mais Bloque

Si vous voyez `[MIDDLEWARE] REQUÊTE REÇUE` mais pas `[ANALYSE] Début` :

**Causes possibles :**
1. **Problème d'authentification** - Le token JWT est invalide
2. **Timeout pendant le parsing** - La requête est trop lente à parser
3. **Erreur dans le middleware CORS**

**Solutions :**
- Vérifiez que vous êtes bien connecté
- Vérifiez que le token JWT est valide
- Regardez s'il y a des erreurs après le log `[MIDDLEWARE]`

### Si l'Analyse Démarre mais Échoue

Si vous voyez `[ANALYSE] Début` mais pas `✅ [ANALYSE] Analyse terminée` :

**Cherchez ces logs :**
```
🔍 [SERVICE] Début analyze_mammography
🔍 [SERVICE] Sauvegarde des fichiers uploadés...
✅ [SERVICE] 4 fichiers sauvegardés
🔍 [SERVICE] Recherche du patient...
🔍 [SERVICE] Lancement de l'analyse ML...
```

**Le dernier log que vous voyez indique où ça bloque :**
- Si vous ne voyez pas `[SERVICE] Sauvegarde des fichiers` → Problème lors de l'initialisation du service
- Si vous voyez `[SERVICE] Sauvegarde` mais pas `Lancement de l'analyse ML` → Problème avec le patient
- Si vous voyez `Lancement de l'analyse ML` mais pas `Analyse ML terminée` → Problème avec le modèle ML (peut prendre plusieurs minutes)

## Commandes Utiles

### Voir les Derniers Logs

Dans Render, les logs sont affichés automatiquement. Pour voir les logs les plus récents :

1. Allez sur la page **Logs**
2. Faites défiler vers le bas (les logs les plus récents sont en bas)
3. Ou utilisez la recherche pour filtrer par timestamp

## Exemple de Logs Complets (Succès)

```
================================================================================
🌐 [MIDDLEWARE] REQUÊTE REÇUE: POST /api/v1/mammography/analyze
🌐 [MIDDLEWARE] Timestamp: 2025-11-05T10:30:00.123456
🌐 [MIDDLEWARE] Client: 10.0.0.1
📦 [MIDDLEWARE] Body info: Content-Type=multipart/form-data, Length=5242880
📦 [MIDDLEWARE] Origin: https://breastcare-frontend.onrender.com
================================================================================

================================================================================
🔍 [ANALYSE] Début de l'analyse - 2025-11-05T10:30:00.123456
🔍 [ANALYSE] Patient ID: P-2025-1
🔍 [ANALYSE] Nombre de fichiers: 4
🔍 [ANALYSE] Informations patient: name=John Doe, age=45
🔍 [ANALYSE] User ID: abc-123-def
🔍 [ANALYSE] User email: doctor@example.com
================================================================================

🔍 [ANALYSE] Validation des fichiers...
🔍 [ANALYSE] Fichier 1: image1.png, Content-Type: image/png
🔍 [ANALYSE] Fichier 2: image2.png, Content-Type: image/png
🔍 [ANALYSE] Fichier 3: image3.png, Content-Type: image/png
🔍 [ANALYSE] Fichier 4: image4.png, Content-Type: image/png
✅ [ANALYSE] Validation des fichiers terminée

🔍 [ANALYSE] Initialisation du MammographyService...
✅ [ANALYSE] MammographyService initialisé, lancement de l'analyse ML...

🔍 [SERVICE] Début analyze_mammography - patient_id=P-2025-1, user_id=abc-123-def
🔍 [SERVICE] Analysis ID généré: 123e4567-e89b-12d3-a456-426614174000
🔍 [SERVICE] Sauvegarde des fichiers uploadés...
✅ [SERVICE] 4 fichiers sauvegardés
🔍 [SERVICE] Recherche du patient: patient_id=P-2025-1
✅ [SERVICE] Patient trouvé: UUID=83dccc95-1140-46b0-8b74-44e78b73b762
🔍 [SERVICE] Lancement de l'analyse ML...
✅ [SERVICE] Analyse ML terminée
🔍 [SERVICE] Création de l'enregistrement d'analyse...
🔍 [SERVICE] Ajout à la base de données...
✅ [SERVICE] Enregistrement créé avec succès - ID: 456e7890-e89b-12d3-a456-426614174001

✅ [ANALYSE] Analyse terminée avec succès - ID: 456e7890-e89b-12d3-a456-426614174001
================================================================================

✅ [MIDDLEWARE] Réponse envoyée: 200 (en 45.234s)
```

## Prochaines Étapes

1. **Lancez une analyse depuis le frontend**
2. **Ouvrez les logs du backend sur Render**
3. **Recherchez les logs `[ANALYSE]` ou `[SERVICE]`**
4. **Identifiez où ça bloque** en comparant avec l'exemple ci-dessus
5. **Partagez les logs** avec moi pour que je puisse vous aider à résoudre le problème

