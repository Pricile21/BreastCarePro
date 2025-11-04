# Logique de Connexion - Plateforme Mobile

## Vue d'ensemble

La plateforme mobile utilise un système d'authentification basé sur JWT (JSON Web Tokens) avec une restriction spécifique pour empêcher les administrateurs de se connecter via cette interface.

## Flux de Connexion

### 1. **Frontend - Page de Login** (`frontend/app/mobile/login/page.tsx`)

#### Points clés :
- **Route** : `/mobile/login`
- **Formulaire** : Email + Mot de passe
- **Paramètre source** : La connexion envoie explicitement `source='mobile'` pour identifier la plateforme

#### Processus :

```typescript
handleLogin() {
  1. Validation du formulaire
  2. Appel API avec source='mobile'
     → apiClient.login(email, password, 'mobile')
  3. Stockage du token dans localStorage
  4. Mise à jour du contexte d'authentification
  5. Redirection vers /mobile (page d'accueil)
}
```

#### Gestion des erreurs :
- Messages d'erreur détaillés selon le type :
  - Erreurs réseau → Message de connexion serveur
  - Erreurs 403 → Message spécifique pour les admins bloqués
  - Erreurs d'authentification → Messages génériques sécurisés

---

### 2. **API Client** (`frontend/lib/api.ts`)

#### Méthode `login()` :

```typescript
async login(email: string, password: string, source?: string) {
  1. Construction des données : { email, password, source }
  2. Requête POST vers /api/v1/auth/login
  3. Stockage du token reçu dans localStorage
  4. Retour de la réponse { access_token, token_type }
}
```

#### Gestion des erreurs HTTP :
- **403 Forbidden** : Extrait le message du backend ou utilise un message par défaut
- **Timeout** : Gestion des timeouts de 30 secondes
- **Réseau** : Détection des erreurs de connexion au serveur

---

### 3. **Backend - Endpoint Login** (`backend/app/api/v1/endpoints/auth.py`)

#### Route : `POST /api/v1/auth/login`

#### Processus d'authentification :

```python
@router.post("/login")
async def login(login_data: LoginRequest, db: Session):
  1. Récupération de l'email, password et source
  2. Authentification via AuthService
     → auth_service.authenticate_user(email, password)
  3. Vérification du type d'utilisateur
  4. BLOQUAGE si source='mobile' ET user_type='admin'
  5. Création du token JWT
  6. Retour du token
```

#### 🔒 **Sécurité Anti-Admin** :

```python
# LIGNE CRITIQUE : Blocage des admins sur mobile
if source == 'mobile' and user_type == 'admin':
    raise HTTPException(
        status_code=403,
        detail="Les administrateurs doivent se connecter via la plateforme admin (/admin/login)"
    )
```

**Logique** :
- Si la requête vient de `source='mobile'` ET que l'utilisateur est `user_type='admin'`
- → Erreur 403 Forbidden avec message explicite
- → Les patients et professionnels peuvent se connecter normalement

---

### 4. **Service d'Authentification** (`backend/app/services/auth_service.py`)

#### Méthode `authenticate_user()` :

```python
def authenticate_user(self, email: str, password: str) -> Optional[User]:
  1. Recherche de l'utilisateur par email
     → user = get_user_by_email(email)
  2. Vérification de l'existence
  3. Vérification du mot de passe hashé
     → verify_password(password, user.hashed_password)
  4. Retour de l'utilisateur si valide, None sinon
```

---

### 5. **Contexte d'Authentification** (`frontend/contexts/auth-context.tsx`)

#### Gestion de l'état global :

```typescript
checkAuth() {
  1. Vérification de la présence du token dans localStorage
  2. Si token présent :
     → Appel API /auth/me pour récupérer les infos utilisateur
     → Mise à jour de l'état user
  3. Si pas de token :
     → user = null
}
```

#### Synchronisation :
- Écoute des changements dans `localStorage` (multi-onglets)
- Vérification périodique (toutes les secondes)
- Vérification au focus de la fenêtre

---

## Schéma de Flux Complet

```
┌─────────────────────────────────────────────────────────┐
│ 1. UTILISATEUR SAISIT EMAIL + PASSWORD                  │
│    (frontend/app/mobile/login/page.tsx)                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 2. APPEL API AVEC source='mobile'                       │
│    apiClient.login(email, password, 'mobile')           │
│    (frontend/lib/api.ts)                                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 3. REQUÊTE HTTP POST /api/v1/auth/login                 │
│    Body: { email, password, source: "mobile" }          │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 4. BACKEND ENDPOINT /auth/login                          │
│    (backend/app/api/v1/endpoints/auth.py)               │
│                                                          │
│    - AuthService.authenticate_user()                    │
│    - Vérification email/password                        │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 5. VÉRIFICATION TYPE UTILISATEUR                        │
│                                                          │
│    IF source='mobile' AND user_type='admin':            │
│      → ❌ ERREUR 403 FORBIDDEN                          │
│                                                          │
│    ELSE:                                                 │
│      → ✅ CRÉATION TOKEN JWT                            │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 6. RETOUR DU TOKEN                                       │
│    { access_token: "...", token_type: "bearer" }       │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 7. STOCKAGE DU TOKEN                                     │
│    localStorage.setItem('auth_token', token)            │
│    (frontend/lib/api.ts)                                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 8. MISE À JOUR CONTEXTE                                  │
│    checkAuth() → Appel /auth/me                         │
│    (frontend/contexts/auth-context.tsx)                 │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 9. REDIRECTION                                           │
│    router.replace('/mobile')                            │
│    (vers la page d'accueil mobile)                      │
└─────────────────────────────────────────────────────────┘
```

---

## Points Importants

### 🔐 Sécurité

1. **Blocage des admins** : Protection explicite pour empêcher les admins de se connecter via mobile
2. **Tokens JWT** : Tokens avec expiration configurable
3. **Hashage des mots de passe** : Utilisation de `bcrypt` via `verify_password()`
4. **Messages d'erreur sécurisés** : Pas de divulgation d'informations sensibles

### 🔄 Redirection

- **Succès** : Redirection vers `/mobile` (page d'accueil, pas le dashboard)
- **Paramètre redirect** : Possibilité de rediriger vers une URL spécifique via `?redirect=...`

### 📝 Logs et Debug

- Logs détaillés à chaque étape dans la console
- Préfixes visuels : 🔐, ✅, ❌, 📥, etc.
- Gestion d'erreurs avec messages explicites

### 🌐 API Configuration

- **URL Base** : `http://localhost:8000/api/v1` (configurable via env)
- **Timeout** : 30 secondes pour les requêtes
- **CORS** : Configuration pour permettre les requêtes cross-origin

---

## Types d'Utilisateurs

| Type        | Peut se connecter via `/mobile/login` ? | Note                           |
|-------------|-----------------------------------------|--------------------------------|
| `patient`   | ✅ Oui                                   | Utilisateurs mobiles           |
| `professional` | ✅ Oui                               | Professionnels de santé        |
| `admin`     | ❌ Non                                  | Bloqué avec erreur 403         |

---

## Endpoints API Utilisés

1. **POST `/api/v1/auth/login`**
   - Authentification et récupération du token
   - Paramètre `source` optionnel

2. **GET `/api/v1/auth/me`**
   - Récupération des informations de l'utilisateur connecté
   - Nécessite un token valide dans le header `Authorization: Bearer <token>`

---

## Variables d'Environnement

- `NEXT_PUBLIC_API_URL` : URL de base de l'API backend (défaut: `http://localhost:8000/api/v1`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` : Durée de validité du token JWT (backend)

---

## Dépannage

### Erreur "Erreur de connexion au serveur"
- Vérifier que le backend est démarré sur `http://localhost:8000`
- Vérifier les logs du backend pour les erreurs serveur

### Erreur 403 "Les administrateurs doivent se connecter via..."
- Normal si vous essayez de vous connecter avec un compte admin
- Utiliser `/admin/login` à la place

### Token non stocké
- Vérifier que `localStorage` est disponible (pas en SSR)
- Vérifier les logs du navigateur pour les erreurs JavaScript


