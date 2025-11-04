"""
Articles endpoints for educational content
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import json
import os
from pathlib import Path
from pydantic import ValidationError

from app.schemas.article import ArticleResponse, ArticleListResponse, ArticleSummary, ArticleContent

router = APIRouter()

# Chemin vers les articles
# Solution robuste qui cherche dans plusieurs emplacements possibles

def find_articles_dir():
    """Trouve le dossier articles en essayant plusieurs chemins possibles"""
    current_file = Path(__file__).resolve()
    work_dir = Path(os.getcwd()).resolve()
    
    # Liste des chemins candidats à tester
    candidates = [
        # Depuis le répertoire de travail actuel (si lancé depuis la racine)
        work_dir / "articles",
        # Depuis le répertoire de travail actuel remontant d'un niveau (si lancé depuis backend/)
        work_dir.parent / "articles",
        # DEPUIS DOCKER: Avec le volume monté à /articles (racine)
        Path("/articles"),
        # Depuis le fichier actuel en remontant jusqu'à la racine
        current_file.parent.parent.parent.parent.parent.parent / "articles",
        # Depuis le fichier actuel en remontant jusqu'à backend/ puis parent
        current_file.parent.parent.parent.parent.parent / "articles",
        # Chemin absolu explicite (si le dossier backend existe)
        work_dir.parent / "articles" if (work_dir / "backend").exists() else None,
    ]
    
    # Filtrer les None et tester chaque candidat
    for candidate in candidates:
        if candidate is None:
            continue
        candidate = candidate.resolve()
        if candidate.exists() and candidate.is_dir():
            json_files = list(candidate.glob('*.json'))
            if json_files:  # Vérifier qu'il y a des fichiers JSON
                return candidate
    
    # Si aucun n'est trouvé, essayer de créer le chemin le plus probable
    # (depuis le répertoire de travail)
    fallback = work_dir / "articles"
    if work_dir.parent.name == "Breast_Cancer" or work_dir.name == "Breast_Cancer":
        # Si on est dans la racine du projet
        fallback = work_dir / "articles"
    elif (work_dir / "backend").exists():
        # Si on est dans backend/, remonter d'un niveau
        fallback = work_dir.parent / "articles"
    
    print(f"Warning: Aucun dossier articles trouvé, utilisation du fallback: {fallback}")
    return fallback

ARTICLES_DIR = find_articles_dir()

# Log pour debug
print(f"Articles directory: {ARTICLES_DIR}")
print(f"Articles directory exists: {ARTICLES_DIR.exists()}")
if ARTICLES_DIR.exists():
    json_files = list(ARTICLES_DIR.glob('*.json'))
    print(f"Found {len(json_files)} article(s): {[f.name for f in json_files]}")


def load_article_from_json(article_id: str) -> dict:
    """Charge un article depuis un fichier JSON"""
    article_file = ARTICLES_DIR / f"{article_id}.json"
    
    print(f"Looking for article file: {article_file}")
    print(f"File exists: {article_file.exists()}")
    
    if not article_file.exists():
        # Lister les fichiers disponibles pour debug
        available_files = list(ARTICLES_DIR.glob("*.json")) if ARTICLES_DIR.exists() else []
        available_ids = [f.stem for f in available_files]
        print(f"Available articles: {available_ids}")
        raise HTTPException(
            status_code=404, 
            detail=f"Article '{article_id}' not found. Available articles: {', '.join(available_ids)}"
        )
    
    try:
        with open(article_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Successfully loaded article JSON")
            return data
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in article file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading article: {str(e)}")


def get_all_articles() -> List[dict]:
    """Récupère la liste de tous les articles disponibles"""
    articles = []
    
    if not ARTICLES_DIR.exists():
        return articles
    
    # Chercher tous les fichiers JSON d'articles
    for json_file in ARTICLES_DIR.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                article_data = json.load(f)
                # Extraire seulement les infos de résumé
                articles.append({
                    "id": article_data.get("id", json_file.stem),
                    "title": article_data.get("title", ""),
                    "description": article_data.get("description", ""),
                    "thumbnail_url": article_data.get("thumbnail_url"),
                    "reading_time": article_data.get("reading_time", 5),
                    "category": article_data.get("metadata", {}).get("category", "education"),
                    "publish_date": article_data.get("metadata", {}).get("publish_date")
                })
        except Exception as e:
            print(f"Error loading article {json_file}: {e}")
            continue
    
    return articles


@router.get("/", response_model=ArticleListResponse)
async def list_articles(
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Maximum number of articles to return")
):
    """
    Get list of all available articles
    """
    try:
        articles_data = get_all_articles()
        
        # Filtrer par catégorie si spécifié
        if category:
            articles_data = [a for a in articles_data if a.get("category") == category]
        
        # Limiter le nombre de résultats
        articles_data = articles_data[:limit]
        
        articles_summary = [ArticleSummary(**article) for article in articles_data]
        
        return ArticleListResponse(
            success=True,
            total=len(articles_summary),
            articles=articles_summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving articles: {str(e)}")


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: str):
    """
    Get full article content by ID
    """
    try:
        print(f"Loading article: {article_id}")
        print(f"Articles directory: {ARTICLES_DIR}")
        print(f"Articles directory exists: {ARTICLES_DIR.exists()}")
        
        if not ARTICLES_DIR.exists():
            raise HTTPException(
                status_code=500, 
                detail=f"Articles directory not found at {ARTICLES_DIR}"
            )
        
        article_data = load_article_from_json(article_id)
        
        # Afficher les erreurs de validation détaillées
        try:
            article = ArticleContent(**article_data)
        except ValidationError as validation_error:
            # Afficher toutes les erreurs de validation
            error_details = json.dumps(validation_error.errors(), indent=2, ensure_ascii=False)
            print(f"Validation error for article {article_id}:")
            print(f"   {error_details}")
            print(f"Article data keys: {list(article_data.keys())}")
            print(f"Metadata keys: {list(article_data.get('metadata', {}).keys())}")
            raise HTTPException(
                status_code=422,
                detail=f"Article validation failed: {error_details}"
            )
        
        print(f"Article loaded successfully: {article_id}")
        return ArticleResponse(
            success=True,
            article=article
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error loading article {article_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error retrieving article: {str(e)}")


@router.get("/categories/list")
async def get_categories():
    """
    Get list of all available article categories
    """
    try:
        articles_data = get_all_articles()
        categories = list(set([a.get("category", "education") for a in articles_data]))
        
        return {
            "success": True,
            "categories": sorted(categories)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving categories: {str(e)}")

