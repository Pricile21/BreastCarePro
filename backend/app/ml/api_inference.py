#!/usr/bin/env python3
"""
API FastAPI pour l'inference MedSigLIP
Endpoint pour prédire sur des mammographies
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import tempfile
from pathlib import Path
import json
from inference_service import MedSigLIPInferenceService

# Créer l'application FastAPI
app = FastAPI(
    title="MedSigLIP Mammography Analysis API",
    description="API pour l'analyse de mammographies avec MedSigLIP",
    version="1.0.0"
)

# Initialiser le service d'inference
inference_service = None

@app.on_event("startup")
async def startup_event():
    """Initialiser le service au démarrage"""
    global inference_service
    try:
        inference_service = MedSigLIPInferenceService()
        print("✅ Service MedSigLIP initialisé")
    except Exception as e:
        print(f"❌ Erreur initialisation: {e}")

@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "MedSigLIP Mammography Analysis API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Vérification de santé"""
    if inference_service is None:
        raise HTTPException(status_code=503, detail="Service non initialisé")
    
    return {
        "status": "healthy",
        "model_loaded": inference_service.model is not None
    }

@app.get("/model/info")
async def get_model_info():
    """Informations sur le modèle"""
    if inference_service is None:
        raise HTTPException(status_code=503, detail="Service non initialisé")
    
    info = inference_service.get_model_info()
    if info is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    
    return info

@app.post("/predict")
async def predict_mammography(file: UploadFile = File(...)):
    """Prédire sur une mammographie uploadée"""
    if inference_service is None:
        raise HTTPException(status_code=503, detail="Service non initialisé")
    
    # Vérifier le type de fichier
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image")
    
    try:
        # Sauvegarder temporairement le fichier
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Prédiction
        result = inference_service.predict_single_image(tmp_file_path)
        
        # Nettoyer le fichier temporaire
        os.unlink(tmp_file_path)
        
        if result is None:
            raise HTTPException(status_code=500, detail="Erreur lors de la prédiction")
        
        # Formater la réponse
        response = {
            "success": True,
            "filename": file.filename,
            "predictions": {
                "bi_rads": {
                    "class": result['bi_rads']['prediction'],
                    "confidence": round(result['bi_rads']['confidence'], 3),
                    "probabilities": {
                        k: round(v, 3) for k, v in result['bi_rads']['probabilities'].items()
                    }
                },
                "density": {
                    "class": result['density']['prediction'],
                    "confidence": round(result['density']['confidence'], 3),
                    "probabilities": {
                        k: round(v, 3) for k, v in result['density']['probabilities'].items()
                    }
                }
            }
        }
        
        return response
        
    except Exception as e:
        # Nettoyer en cas d'erreur
        if 'tmp_file_path' in locals():
            try:
                os.unlink(tmp_file_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.post("/predict/batch")
async def predict_batch_mammography(files: list[UploadFile] = File(...)):
    """Prédire sur plusieurs mammographies"""
    if inference_service is None:
        raise HTTPException(status_code=503, detail="Service non initialisé")
    
    if len(files) > 10:  # Limite de sécurité
        raise HTTPException(status_code=400, detail="Maximum 10 images par batch")
    
    # Vérifier les types de fichiers
    for file in files:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail=f"Le fichier {file.filename} doit être une image")
    
    try:
        # Sauvegarder temporairement les fichiers
        tmp_paths = []
        for file in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_paths.append(tmp_file.name)
        
        # Prédictions
        results = inference_service.predict_batch(tmp_paths)
        
        # Nettoyer les fichiers temporaires
        for tmp_path in tmp_paths:
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        # Formater la réponse
        response = {
            "success": True,
            "total_images": len(files),
            "results": []
        }
        
        for i, result in enumerate(results):
            if 'error' in result:
                response["results"].append({
                    "filename": files[i].filename,
                    "error": result['error']
                })
            else:
                response["results"].append({
                    "filename": files[i].filename,
                    "predictions": {
                        "bi_rads": {
                            "class": result['bi_rads']['prediction'],
                            "confidence": round(result['bi_rads']['confidence'], 3)
                        },
                        "density": {
                            "class": result['density']['prediction'],
                            "confidence": round(result['density']['confidence'], 3)
                        }
                    }
                })
        
        return response
        
    except Exception as e:
        # Nettoyer en cas d'erreur
        for tmp_path in tmp_paths:
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/classes")
async def get_classes():
    """Obtenir les classes disponibles"""
    if inference_service is None:
        raise HTTPException(status_code=503, detail="Service non initialisé")
    
    return {
        "bi_rads_classes": inference_service.bi_rads_classes,
        "density_classes": inference_service.density_classes
    }

if __name__ == "__main__":
    print("🚀 Démarrage de l'API MedSigLIP...")
    uvicorn.run(
        "api_inference:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
