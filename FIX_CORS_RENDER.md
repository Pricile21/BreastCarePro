# 🔧 Fix CORS sur Render - URGENT

## Problème

Vous avez cette erreur dans la console du navigateur :
```
Access to fetch at 'https://breastcare-backend.onrender.com/api/v1/mammography/analyze' 
from origin 'https://breastcare-frontend.onrender.com' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

## Solution : Ajouter la Variable d'Environnement CORS

### Étapes à Suivre

1. **Allez sur Render Dashboard**
   - https://dashboard.render.com
   - Cliquez sur votre service **breastcare-backend**

2. **Ouvrez la Section "Environment"**
   - Dans le menu de gauche, cliquez sur **"Environment"**

3. **Ajoutez la Variable BACKEND_CORS_ORIGINS**
   - Cliquez sur **"Add Environment Variable"**
   - **Key** : `BACKEND_CORS_ORIGINS`
   - **Value** : `https://breastcare-frontend.onrender.com,http://localhost:3000`
   - Cliquez sur **"Save Changes"**

4. **Redéployez le Backend**
   - Render redéploiera automatiquement après avoir sauvegardé la variable
   - Ou cliquez manuellement sur **"Manual Deploy"** → **"Deploy latest commit"**

5. **Vérifiez les Logs**
   - Allez dans la section **"Logs"**
   - Vous devriez voir au démarrage :
   ```
   🌐 CORS Origins autorisées: ['https://breastcare-frontend.onrender.com', 'http://localhost:3000']
   🌐 BACKEND_CORS_ORIGINS env: https://breastcare-frontend.onrender.com,http://localhost:3000
   ```

6. **Testez à Nouveau**
   - Retournez sur https://breastcare-frontend.onrender.com/professional/upload
   - Lancez une analyse
   - L'erreur CORS devrait disparaître

## Pourquoi Cette Erreur ?

Le backend FastAPI utilise un middleware CORS qui bloque les requêtes provenant d'origines non autorisées. Par défaut, seules les origines locales (`localhost:3000`) sont autorisées.

Pour que le frontend sur Render (`https://breastcare-frontend.onrender.com`) puisse communiquer avec le backend, il faut ajouter cette URL dans la liste des origines autorisées via la variable d'environnement `BACKEND_CORS_ORIGINS`.

## Format de la Variable

Si vous avez plusieurs frontends, séparez-les par des virgules :
```
https://breastcare-frontend.onrender.com,http://localhost:3000,https://votre-autre-frontend.com
```

## Vérification

Après avoir ajouté la variable et redéployé :

1. **Vérifiez les logs de démarrage** - Vous devriez voir les origines CORS listées
2. **Testez une requête simple** - Par exemple, la connexion devrait fonctionner
3. **Testez l'analyse** - L'upload d'images devrait maintenant fonctionner

## Si le Problème Persiste

1. Vérifiez que la variable est bien sauvegardée dans Render
2. Vérifiez que le backend a bien redémarré (regardez les logs)
3. Vérifiez que l'URL dans `BACKEND_CORS_ORIGINS` correspond exactement à l'URL de votre frontend (sans `/` à la fin)
4. Videz le cache du navigateur et réessayez

