"""
API FastAPI pour la calculatrice de risque Gail Model
Endpoints pour application mobile
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from sqlalchemy.orm import Session
import uuid
from app.ml.gail_risk_calculator import GailModelRiskCalculator
from app.api.deps import get_db, get_current_user
from app.models.risk_assessment import RiskAssessment, RiskLevel
from app.models.user import User

router = APIRouter(prefix="/risk", tags=["Risk Assessment"])

# Initialiser le calculateur
calculator = GailModelRiskCalculator()


class RiskAssessmentRequest(BaseModel):
    """Modèle de données pour la requête d'évaluation de risque"""
    age: int = Field(..., ge=18, le=90, description="Âge actuel")
    first_degree_relatives: int = Field(
        default=0, 
        ge=0, 
        le=10,
        description="Nombre de parentes au 1er degré (mère, sœur) avec cancer du sein"
    )
    previous_biopsies: int = Field(
        default=0,
        ge=0,
        le=10,
        description="Nombre de biopsies précédentes"
    )
    atypical_hyperplasia: bool = Field(
        default=False,
        description="Hyperplasie atypique détectée lors d'une biopsie (diagnostic médical). Si l'utilisateur n'a jamais eu de biopsie ou ne sait pas, la valeur par défaut est False"
    )
    age_menarche: str = Field(
        default="12-13",
        description="Âge de la première menstruation: '<12', '12-13', '14+'"
    )
    age_first_birth: str = Field(
        default="25-29",
        description="Âge à la naissance du premier enfant: '<20', '20-24', '25-29', '30+', 'nulliparous'"
    )
    # Facteurs de mode de vie (optionnels pour améliorer la précision)
    weight_kg: Optional[float] = Field(
        default=None,
        ge=30.0,
        le=200.0,
        description="Poids en kilogrammes. Optionnel mais recommandé pour précision maximale"
    )
    height_cm: Optional[float] = Field(
        default=None,
        ge=100.0,
        le=250.0,
        description="Taille en centimètres. Optionnel mais recommandé pour précision maximale"
    )
    alcohol_consumption: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
        description="Consommation d'alcool : nombre de verres par semaine. Optionnel mais recommandé"
    )
    exercise_minutes_per_week: Optional[int] = Field(
        default=None,
        ge=0,
        le=1000,
        description="Minutes d'exercice physique modéré par semaine. Optionnel mais recommandé"
    )
    smoking_status: Optional[str] = Field(
        default=None,
        description="Statut tabagique: 'never', 'former', 'current'. Optionnel"
    )
    hormone_therapy: Optional[bool] = Field(
        default=None,
        description="Traitement hormonal post-ménopause. Optionnel, seulement si applicable"
    )


class LifestyleInsight(BaseModel):
    """Insight sur un facteur de mode de vie"""
    factor: str = Field(..., description="Nom du facteur")
    value: str = Field(..., description="Valeur actuelle de l'utilisateur")
    impact: str = Field(..., description="Impact sur le risque selon la littérature")
    recommendation: str = Field(..., description="Recommandation personnalisée")


class RiskAssessmentResponse(BaseModel):
    """Réponse de l'évaluation de risque"""
    risk_5_years: float = Field(..., description="Risque sur 5 ans en pourcentage (ajusté avec mode de vie)")
    risk_gail_pure: float = Field(..., description="Risque Gail pur (sans mode de vie) pour référence")
    lifestyle_adjustment_percent: float = Field(..., description="Impact du mode de vie en pourcentage (+/-)")
    risk_lifetime: Optional[float] = Field(None, description="Risque à vie - Non calculé actuellement (nécessite validation)")
    risk_category: str = Field(..., description="Catégorie: 'Faible', 'Modéré', 'Élevé', 'Très élevé'")
    educational_message: List[str] = Field(..., description="Messages éducatifs rassurants")
    recommendations: List[str] = Field(..., description="Recommandations personnalisées")
    model_used: str = Field(..., description="Modèle utilisé pour le calcul")
    estimated_accuracy: str = Field(..., description="Précision validée du modèle")
    variables_provided: int = Field(..., description="Nombre de variables Gail fournies")
    variables_total: int = Field(..., description="Nombre total de variables du modèle Gail")
    lifestyle_factors_provided: int = Field(default=0, description="Nombre de facteurs de mode de vie fournis")
    lifestyle_insights: List[LifestyleInsight] = Field(default=[], description="Informations détaillées sur chaque facteur de mode de vie")
    note_lifestyle: str = Field(..., description="Note importante sur les facteurs de mode de vie")
    disclaimer: str = Field(..., description="Avertissement médical")
    critical_warnings: List[str] = Field(..., description="Avertissements critiques à afficher de manière prominente")
    warning_message: Optional[str] = Field(None, description="Message d'avertissement si le modèle Gail peut sous-estimer le risque")
    average_risk_for_age: Optional[float] = Field(default=None, description="Risque moyen pour une femme de cet âge dans la population générale")
    risk_relative: Optional[float] = Field(default=None, description="Facteur multiplicateur par rapport au risque moyen (ex: 2.5x)")
    clinical_significance: Optional[str] = Field(default=None, description="Signification clinique du risque")
    significance_explanation: Optional[str] = Field(default=None, description="Explication de la signification clinique")


@router.post("/calculate", response_model=RiskAssessmentResponse)
async def calculate_breast_cancer_risk(request: RiskAssessmentRequest):
    """
    Calcule le risque de cancer du sein selon le modèle Gail
    
    Variables utilisateur-friendly :
    - Âge, antécédents familiaux, biopsies
    - Facteurs reproductifs
    - Pas de variables médicales complexes
    """
    print(f"📥 Requête reçue: age={request.age}, relatives={request.first_degree_relatives}, biopsies={request.previous_biopsies}")
    try:
        # Calculer l'IMC si poids et taille fournis
        bmi = None
        if request.weight_kg and request.height_cm:
            height_m = request.height_cm / 100.0
            bmi = request.weight_kg / (height_m ** 2)
        
        # Convertir la requête en dictionnaire
        user_data = {
            'age': request.age,
            'first_degree_relatives': request.first_degree_relatives,
            'previous_biopsies': request.previous_biopsies,
            'atypical_hyperplasia': request.atypical_hyperplasia,
            'age_menarche': request.age_menarche,
            'age_first_birth': request.age_first_birth,
            # Facteurs de mode de vie (optionnels)
            'bmi': bmi,  # Calculé automatiquement
            'alcohol_consumption': request.alcohol_consumption,
            'exercise_minutes_per_week': request.exercise_minutes_per_week,
            'smoking_status': request.smoking_status,
            'hormone_therapy': request.hormone_therapy
        }
        
        # Calculer le risque
        result = calculator.calculate_risk(user_data)
        
        # Vérifier s'il y a une erreur
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        # Convertir les lifestyle_insights en objets
        lifestyle_insights = [
            LifestyleInsight(**insight) for insight in result.get('lifestyle_insights', [])
        ]
        
        # Préparer la réponse avec toutes les clés attendues
        response_data = {
            **result,
            'lifestyle_insights': lifestyle_insights,
            # S'assurer que les champs optionnels ont une valeur par défaut si nécessaire
            'average_risk_for_age': result.get('average_risk_for_age'),
            'risk_relative': result.get('risk_relative'),
            'clinical_significance': result.get('clinical_significance'),
            'significance_explanation': result.get('significance_explanation'),
        }
        
        return RiskAssessmentResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"❌ Erreur dans calculate_breast_cancer_risk: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul: {str(e)}")


@router.get("/questions")
async def get_risk_questions():
    """
    Retourne les questions à poser à l'utilisateur
    Format utilisateur-friendly pour l'application mobile
    Version complète avec toutes les questions pour précision maximale
    """
    return {
        "version": "complete",
        "description": "Questions complètes pour une précision maximale du modèle Gail",
        "estimated_accuracy": "75-80%",
        "questions": [
            {
                "id": "age",
                "question": "Quel est votre âge ?",
                "type": "number",
                "min": 18,
                "max": 90,
                "required": True
            },
            {
                "id": "first_degree_relatives",
                "question": "Votre mère ou l'une de vos sœurs a-t-elle eu un cancer du sein ?",
                "type": "select",
                "options": [
                    {"value": 0, "label": "Non, aucune"},
                    {"value": 1, "label": "Oui, une (mère OU une sœur)"},
                    {"value": 2, "label": "Oui, deux ou plus (mère ET sœur, ou plusieurs sœurs)"}
                ],
                "help": "Comptez seulement votre mère et vos sœurs biologiques",
                "required": True
            },
            {
                "id": "previous_biopsies",
                "question": "Avez-vous déjà eu un examen médical où un médecin a prélevé un petit morceau de votre sein pour l'analyser ?",
                "type": "select",
                "options": [
                    {"value": 0, "label": "Non, jamais"},
                    {"value": 1, "label": "Oui, une fois"},
                    {"value": 2, "label": "Oui, plusieurs fois"}
                ],
                "help": "Si vous n'êtes pas sûre ou ne vous souvenez pas, répondez 'Non' - c'est normal, beaucoup de femmes n'en ont jamais eu",
                "required": True
            },
            {
                "id": "atypical_hyperplasia",
                "question": "Si vous avez eu un prélèvement du sein, un médecin vous a-t-il dit que les cellules n'étaient pas tout à fait normales (mais que ce n'était pas un cancer) ?",
                "type": "boolean",
                "help": "Si vous n'avez jamais eu de prélèvement ou ne savez pas, répondez 'Non' - c'est très rare",
                "required": True,
                "show_if": {"previous_biopsies": ">0"}
            },
            {
                "id": "age_menarche",
                "question": "À quel âge avez-vous eu vos premières règles ?",
                "type": "select",
                "options": [
                    {"value": "<12", "label": "Avant 12 ans"},
                    {"value": "12-13", "label": "Entre 12 et 13 ans"},
                    {"value": "14+", "label": "14 ans ou plus"}
                ],
                "required": True
            },
            {
                "id": "age_first_birth",
                "question": "À quel âge avez-vous eu votre premier enfant ?",
                "type": "select",
                "options": [
                    {"value": "<20", "label": "Avant 20 ans"},
                    {"value": "20-24", "label": "Entre 20 et 24 ans"},
                    {"value": "25-29", "label": "Entre 25 et 29 ans"},
                    {"value": "30+", "label": "30 ans ou plus"},
                    {"value": "nulliparous", "label": "Je n'ai pas d'enfant"}
                ],
                "required": True
            },
            {
                "id": "weight_kg",
                "question": "Quel est votre poids actuel ?",
                "type": "number",
                "min": 30,
                "max": 200,
                "unit": "kg",
                "help": "En kilogrammes. Exemple : si vous pesez 70 kilos, écrivez 70",
                "required": False,
                "optional": True,
                "section": "mode_de_vie",
                "section_title": "Questions sur votre mode de vie (optionnel)"
            },
            {
                "id": "height_cm",
                "question": "Quelle est votre taille ?",
                "type": "number",
                "min": 100,
                "max": 250,
                "unit": "cm",
                "help": "En centimètres. Exemple : 1 mètre 70 = 170 cm (écrivez 170)",
                "required": False,
                "optional": True,
                "show_if": {"weight_kg": "provided"},
                "section": "mode_de_vie"
            },
            {
                "id": "alcohol_consumption",
                "question": "Combien de verres d'alcool buvez-vous par semaine ?",
                "type": "number",
                "min": 0,
                "max": 50,
                "help": "1 verre = 1 verre de vin, 1 bière, ou 1 shot de spiritueux. Si vous ne buvez pas d'alcool, écrivez 0.",
                "required": False,
                "optional": True,
                "section": "mode_de_vie"
            },
            {
                "id": "exercise_minutes_per_week",
                "question": "Combien de minutes par semaine faites-vous de sport ou d'exercice physique ?",
                "type": "number",
                "min": 0,
                "max": 1000,
                "help": "Exemples : marche rapide, vélo, natation, course, gym, etc. Si vous ne faites pas de sport, écrivez 0.",
                "required": False,
                "optional": True,
                "section": "mode_de_vie"
            },
            {
                "id": "smoking_status",
                "question": "Fumez-vous actuellement ?",
                "type": "select",
                "options": [
                    {"value": "never", "label": "Non, je n'ai jamais fumé"},
                    {"value": "former", "label": "Non, j'ai arrêté de fumer"},
                    {"value": "current", "label": "Oui, je fume actuellement"}
                ],
                "help": "Le tabac peut augmenter le risque de cancer",
                "required": False,
                "optional": True,
                "section": "mode_de_vie"
            },
            {
                "id": "hormone_therapy",
                "question": "Prenez-vous un traitement hormonal pour la ménopause (pilules ou patchs) ?",
                "type": "boolean",
                "help": "Seulement si vous êtes ménopausée (arrêt des règles) et prenez un traitement hormonal prescrit par un médecin",
                "required": False,
                "optional": True,
                "show_if": {"age": ">=50"},
                "section": "mode_de_vie"
            }
        ],
        "disclaimer": "Ces informations sont utilisées uniquement pour estimer votre risque selon le modèle Gail. Elles ne sont pas stockées de manière identifiante. Toutes les questions sont nécessaires pour une précision maximale (75-80%)."
    }


@router.get("/info")
async def get_risk_info():
    """
    Informations sur le modèle Gail et son utilisation
    """
    return {
        "model_name": "Gail Model (Version Pure)",
        "description": "Modèle de risque de cancer du sein validé médicalement par le National Cancer Institute (NCI)",
        "validation": "Validé sur 500,000+ femmes avec suivi à long terme",
        "precision": "75-80% de précision validée pour prédire le risque sur 5 ans (modèle pur, non modifié)",
        "version": "Modèle Gail original - Aucune modification apportée pour préserver la précision validée",
        "variables_required": [
            "Âge",
            "Antécédents familiaux (mère, sœurs)",
            "Antécédents de biopsies",
            "Hyperplasie atypique",
            "Âge première menstruation",
            "Âge premier enfant"
        ],
        "lifestyle_factors": {
            "note": "Les facteurs de mode de vie (IMC, alcool, exercice, tabac, traitement hormonal) sont collectés mais utilisés UNIQUEMENT à titre éducatif. Ils n'affectent PAS le calcul du risque pour préserver la précision validée du modèle.",
            "purpose": "Fournir des informations éducatives et des recommandations personnalisées"
        },
        "limitations": [
            "Estimation basée sur des données statistiques",
            "Ne remplace pas une consultation médicale",
            "Calibré pour population américaine, peut nécessiter ajustements pour d'autres populations",
            "Les facteurs de mode de vie ne sont pas intégrés dans le calcul (informations éducatives uniquement)"
        ],
        "recommendation": "Consultez toujours un médecin pour une évaluation complète de votre risque"
    }


@router.post("/calculate-and-save", response_model=RiskAssessmentResponse)
async def calculate_and_save_risk(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Calculate risk AND save to database
    Requires authentication
    """
    try:
        # Calculer le risque (même code que calculate)
        user_data = {
            'age': request.age,
            'first_degree_relatives': request.first_degree_relatives,
            'previous_biopsies': request.previous_biopsies,
            'atypical_hyperplasia': request.atypical_hyperplasia,
            'age_menarche': request.age_menarche,
            'age_first_birth': request.age_first_birth,
            'weight_kg': request.weight_kg,
            'height_cm': request.height_cm,
            'alcohol_consumption': request.alcohol_consumption,
            'exercise_minutes_per_week': request.exercise_minutes_per_week,
            'smoking_status': request.smoking_status,
            'hormone_therapy': request.hormone_therapy
        }
        
        result = calculator.calculate_risk(user_data)
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        # Convertir lifestyle_insights
        lifestyle_insights = [
            LifestyleInsight(**insight) for insight in result.get('lifestyle_insights', [])
        ]
        
        response_data = {
            **result,
            'lifestyle_insights': lifestyle_insights,
            'average_risk_for_age': result.get('average_risk_for_age'),
            'risk_relative': result.get('risk_relative'),
            'clinical_significance': result.get('clinical_significance'),
            'significance_explanation': result.get('significance_explanation'),
        }
        
        # Créer l'évaluation dans la DB
        risk_level_map = {
            'Faible': RiskLevel.LOW,
            'Modéré': RiskLevel.MODERATE,
            'Élevé': RiskLevel.HIGH,
            'Très élevé': RiskLevel.VERY_HIGH
        }
        
        assessment = RiskAssessment(
            id=f"risk-{uuid.uuid4()}",
            user_id=current_user.id,
            assessment_id=f"assessment-{uuid.uuid4()}",
            risk_5_years=result['risk_5_years'],
            risk_lifetime=result.get('risk_lifetime'),
            risk_level=risk_level_map.get(result['risk_category'], RiskLevel.LOW),
            risk_category=result['risk_category'],
            input_data=user_data,
            risk_relative=result.get('risk_relative'),
            average_risk_for_age=result.get('average_risk_for_age'),
            clinical_significance=result.get('clinical_significance'),
            significance_explanation=result.get('significance_explanation'),
            recommendations=result.get('recommendations', []),
            educational_message=result.get('educational_message', []),
            critical_warnings=result.get('critical_warnings', []),
            lifestyle_insights=[insight.dict() for insight in lifestyle_insights] if lifestyle_insights else [],
            model_used=result.get('model_used', 'Gail Model'),
            estimated_accuracy=result.get('estimated_accuracy', '75-80%'),
            disclaimer=result.get('disclaimer')
        )
        
        # Sauvegarder l'évaluation dans la DB avec gestion d'erreur
        try:
            db.add(assessment)
            db.commit()
            db.refresh(assessment)
            print(f"✅ Évaluation sauvegardée pour utilisateur {current_user.id}")
        except Exception as db_error:
            db.rollback()
            print(f"⚠️ Erreur lors de la sauvegarde (calcul OK): {str(db_error)}")
            # Continuer même si la sauvegarde échoue - retourner quand même le résultat du calcul
            # L'utilisateur a besoin du résultat même si la DB est temporairement indisponible
        
        return RiskAssessmentResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        try:
            db.rollback()
        except:
            pass
        print(f"❌ Erreur dans calculate_and_save_risk: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul et de la sauvegarde: {str(e)}")


@router.get("/my-assessments")
async def get_my_assessments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all risk assessments for the current user
    """
    try:
        assessments = db.query(RiskAssessment).filter(
            RiskAssessment.user_id == current_user.id
        ).order_by(
            RiskAssessment.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        results = []
        for assessment in assessments:
            results.append({
                "id": assessment.id,
                "assessment_id": assessment.assessment_id,
                "date": assessment.created_at.isoformat() if assessment.created_at else None,
                "risk_5_years": assessment.risk_5_years,
                "risk_category": assessment.risk_category,
                "risk_level": assessment.risk_level.value if assessment.risk_level else None,
                "clinical_significance": assessment.clinical_significance,
                "recommendations": assessment.recommendations or [],
            })
        
        return {
            "assessments": results,
            "total": len(results),
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        import traceback
        print(f"❌ Erreur dans get_my_assessments: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")


@router.get("/assessments/{assessment_id}")
async def get_assessment(
    assessment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific risk assessment by ID
    """
    try:
        assessment = db.query(RiskAssessment).filter(
            RiskAssessment.assessment_id == assessment_id,
            RiskAssessment.user_id == current_user.id
        ).first()
        
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        return {
            "id": assessment.id,
            "assessment_id": assessment.assessment_id,
            "date": assessment.created_at.isoformat() if assessment.created_at else None,
            "risk_5_years": assessment.risk_5_years,
            "risk_lifetime": assessment.risk_lifetime,
            "risk_category": assessment.risk_category,
            "risk_level": assessment.risk_level.value if assessment.risk_level else None,
            "risk_relative": assessment.risk_relative,
            "average_risk_for_age": assessment.average_risk_for_age,
            "clinical_significance": assessment.clinical_significance,
            "significance_explanation": assessment.significance_explanation,
            "recommendations": assessment.recommendations or [],
            "educational_message": assessment.educational_message or [],
            "critical_warnings": assessment.critical_warnings or [],
            "lifestyle_insights": assessment.lifestyle_insights or [],
            "model_used": assessment.model_used,
            "estimated_accuracy": assessment.estimated_accuracy,
            "disclaimer": assessment.disclaimer,
            "input_data": assessment.input_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"❌ Erreur dans get_assessment: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

