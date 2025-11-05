# Articles API Documentation

Ce dossier contient les articles éducatifs pour la plateforme BreastCare Pro.

## Structure des fichiers

- `*.md` : Version markdown source de l'article
- `*.json` : Version JSON formatée pour l'API mobile

## Format JSON des articles

Chaque article doit suivre la structure définie dans `backend/app/schemas/article.py` :

```json
{
  "id": "identifiant-unique",
  "title": "Titre de l'article",
  "description": "Description courte",
  "reading_time": 5,
  "metadata": {
    "category": "education",
    "tags": ["tag1", "tag2"],
    "author": "Auteur",
    "publish_date": "2024-01-15"
  },
  "introduction": "...",
  "sections": [...],
  "conclusion": "...",
  "disclaimer": "...",
  "sources": [...]
}
```

## API Endpoints

### Liste des articles
```
GET /api/v1/articles/
Query params:
  - category: filtre par catégorie (optionnel)
  - limit: nombre maximum d'articles (défaut: 10, max: 100)
```

### Détails d'un article
```
GET /api/v1/articles/{article_id}
```

### Catégories disponibles
```
GET /api/v1/articles/categories/list
```

## Exemple de réponse

### Liste d'articles
```json
{
  "success": true,
  "total": 1,
  "articles": [
    {
      "id": "quest-ce-que-le-cancer-du-sein",
      "title": "Qu'est-ce que le cancer du sein?",
      "description": "Comprendre les bases...",
      "reading_time": 5,
      "category": "education",
      "publish_date": "2024-01-15"
    }
  ]
}
```

### Article complet
Voir `quest-ce-que-le-cancer-du-sein.json` pour un exemple complet.

## Utilisation mobile

Le format JSON est optimisé pour l'affichage mobile :
- Sections structurées avec sous-sections
- Listes à puces et listes numérotées séparées
- Contenu HTML optionnel pour rendu riche
- Markdown disponible pour parsing côté client

