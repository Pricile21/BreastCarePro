"""
Service de génération de rapports PDF pour les analyses mammographiques
"""

import io
from datetime import datetime
from typing import Optional
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
import copy
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib import colors


class ReportService:
    """
    Service pour générer des rapports PDF professionnels
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configure les styles personnalisés pour le rapport"""
        # Style pour le titre principal - toujours modifier si existe
        if 'Title' in self.styles:
            self.styles['Title'].fontSize = 24
            self.styles['Title'].textColor = HexColor('#1a1a1a')
            self.styles['Title'].spaceAfter = 30
            self.styles['Title'].alignment = TA_CENTER
            self.styles['Title'].fontName = 'Helvetica-Bold'
        
        # Style pour les titres de section
        try:
            self.styles.add(ParagraphStyle(
                name='SectionTitle',
                parent=self.styles['Heading2'],
                fontSize=16,
                textColor=HexColor('#2563eb'),
                spaceAfter=12,
                spaceBefore=20,
                fontName='Helvetica-Bold'
            ))
        except KeyError:
            # Le style existe déjà, ne rien faire
            pass
        
        # Style pour le texte normal
        try:
            self.styles.add(ParagraphStyle(
                name='BodyText',
                parent=self.styles['Normal'],
                fontSize=11,
                textColor=HexColor('#374151'),
                spaceAfter=12,
                alignment=TA_JUSTIFY,
                leading=14
            ))
        except KeyError:
            # Le style existe déjà, ne rien faire
            pass
        
        # Style pour les badges/informations importantes
        try:
            self.styles.add(ParagraphStyle(
                name='Badge',
                parent=self.styles['Normal'],
                fontSize=12,
                textColor=HexColor('#ffffff'),
                backColor=HexColor('#2563eb'),
                borderPadding=8,
                alignment=TA_CENTER
            ))
        except KeyError:
            # Le style existe déjà, ne rien faire
            pass
    
    def generate_report_pdf(self, analysis_data: dict, patient_data: Optional[dict] = None) -> bytes:
        """
        Génère un rapport PDF professionnel à partir des données d'analyse
        
        Args:
            analysis_data: Données de l'analyse mammographique
            patient_data: Données du patient (optionnel)
        
        Returns:
            bytes: Contenu du PDF généré
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Header
        story.extend(self._create_header(analysis_data, patient_data))
        story.append(Spacer(1, 0.5*cm))
        
        # Informations patient
        story.extend(self._create_patient_section(analysis_data, patient_data))
        story.append(Spacer(1, 0.3*cm))
        
        # Résultats principaux
        story.extend(self._create_results_section(analysis_data))
        story.append(Spacer(1, 0.3*cm))
        
        # Observations détaillées
        story.extend(self._create_findings_section(analysis_data))
        story.append(Spacer(1, 0.3*cm))
        
        # Recommandations
        story.extend(self._create_recommendations_section(analysis_data))
        story.append(Spacer(1, 0.3*cm))
        
        # Informations techniques
        story.extend(self._create_technical_section(analysis_data))
        story.append(Spacer(1, 0.3*cm))
        
        # Footer
        story.extend(self._create_footer(analysis_data))
        
        # Générer le PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _create_header(self, analysis_data: dict, patient_data: Optional[dict]) -> list:
        """Crée l'en-tête du rapport"""
        elements = []
        
        # Titre principal
        title = Paragraph("RAPPORT D'ANALYSE MAMMOGRAPHIQUE", self.styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*cm))
        
        # Sous-titre
        subtitle = Paragraph("Analyse par Intelligence Artificielle - Classification BI-RADS", 
                           self.styles['BodyText'])
        subtitle.alignment = TA_CENTER
        elements.append(subtitle)
        elements.append(Spacer(1, 0.3*cm))
        
        return elements
    
    def _create_patient_section(self, analysis_data: dict, patient_data: Optional[dict]) -> list:
        """Crée la section informations patient"""
        elements = []
        
        elements.append(Paragraph("INFORMATIONS PATIENT", self.styles['SectionTitle']))
        
        # Tableau des informations
        patient_id = analysis_data.get('patient_id', 'N/A')
        patient_name = patient_data.get('full_name', f'Patient {patient_id}') if patient_data else f'Patient {patient_id}'
        date_str = analysis_data.get('created_at')
        
        # Parser la date
        formatted_date = 'N/A'
        if date_str:
            try:
                if isinstance(date_str, str):
                    # Gérer différents formats de date
                    if 'T' in date_str:
                        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                elif isinstance(date_str, datetime):
                    date_obj = date_str
                else:
                    date_obj = datetime.now()
                formatted_date = date_obj.strftime('%d/%m/%Y')
            except Exception:
                formatted_date = str(date_str) if date_str else 'N/A'
        else:
            formatted_date = datetime.now().strftime('%d/%m/%Y')
        
        data = [
            ['ID Patient:', patient_id],
            ['Nom:', patient_name],
            ['Date d\'analyse:', formatted_date]
        ]
        
        if patient_data:
            if patient_data.get('age'):
                data.append(['Âge:', str(patient_data['age'])])
            if patient_data.get('phone_number'):
                data.append(['Téléphone:', patient_data['phone_number']])
        
        table = Table(data, colWidths=[4*cm, 10*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#1a1a1a')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e5e7eb')),
        ]))
        
        elements.append(table)
        return elements
    
    def _create_results_section(self, analysis_data: dict) -> list:
        """Crée la section résultats principaux"""
        elements = []
        
        elements.append(Paragraph("RÉSULTATS DE L'ANALYSE", self.styles['SectionTitle']))
        
        # Classification BI-RADS
        bi_rads = analysis_data.get('bi_rads_category', 'BI-RADS 2')
        # Extraire le numéro BI-RADS de différents formats possibles
        bi_rads_num = '2'
        if isinstance(bi_rads, str):
            if 'BI-RADS' in bi_rads.upper():
                parts = bi_rads.upper().split('BI-RADS')
                if len(parts) > 1:
                    bi_rads_num = parts[1].strip().split()[0]
            elif bi_rads.isdigit():
                bi_rads_num = bi_rads
            elif 'CATEGORY_' in bi_rads:
                bi_rads_num = bi_rads.split('CATEGORY_')[-1]
        
        confidence_score = analysis_data.get('confidence_score', 0.8)
        # S'assurer que c'est un float entre 0 et 1
        if isinstance(confidence_score, (int, float)):
            confidence = float(confidence_score) * 100 if confidence_score <= 1.0 else float(confidence_score)
        else:
            confidence = 80.0
        
        # Couleur selon le niveau de risque
        risk_level = self._get_risk_level(bi_rads_num)
        color_map = {
            'low': '#10b981',      # Vert
            'medium': '#f59e0b',   # Orange
            'high': '#ef4444'      # Rouge
        }
        bg_color = HexColor(color_map.get(risk_level, '#6b7280'))
        
        # Box principal avec BI-RADS
        bi_rads_data = [
            ['Classification BI-RADS:', f'BI-RADS {bi_rads_num}'],
            ['Confiance du modèle:', f'{confidence:.1f}%'],
            ['Niveau de risque:', risk_level.upper()],
        ]
        
        bi_rads_table = Table(bi_rads_data, colWidths=[6*cm, 8*cm])
        bi_rads_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#f9fafb')),
            ('BACKGROUND', (1, 0), (1, 0), bg_color),
            ('TEXTCOLOR', (1, 0), (1, 0), HexColor('#ffffff')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#d1d5db')),
        ]))
        
        elements.append(bi_rads_table)
        elements.append(Spacer(1, 0.2*cm))
        
        # Densité mammaire
        density = analysis_data.get('breast_density', 'Unknown')
        density_data = [['Densité mammaire:', density]]
        density_table = Table(density_data, colWidths=[6*cm, 8*cm])
        density_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#f9fafb')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e5e7eb')),
        ]))
        
        elements.append(density_table)
        return elements
    
    def _create_findings_section(self, analysis_data: dict) -> list:
        """Crée la section observations détaillées"""
        elements = []
        
        elements.append(Paragraph("OBSERVATIONS DÉTAILLÉES", self.styles['SectionTitle']))
        
        findings = analysis_data.get('findings', 'Aucune observation disponible')
        findings_para = Paragraph(findings, self.styles['BodyText'])
        elements.append(findings_para)
        
        return elements
    
    def _create_recommendations_section(self, analysis_data: dict) -> list:
        """Crée la section recommandations"""
        elements = []
        
        elements.append(Paragraph("RECOMMANDATIONS", self.styles['SectionTitle']))
        
        recommendations = analysis_data.get('recommendations', 'Aucune recommandation disponible')
        rec_para = Paragraph(recommendations, self.styles['BodyText'])
        elements.append(rec_para)
        
        return elements
    
    def _create_technical_section(self, analysis_data: dict) -> list:
        """Crée la section informations techniques"""
        elements = []
        
        elements.append(Paragraph("INFORMATIONS TECHNIQUES", self.styles['SectionTitle']))
        
        model_version = analysis_data.get('model_version', 'MedSigLIP')
        analysis_id = analysis_data.get('analysis_id', analysis_data.get('id', 'N/A'))
        
        tech_data = [
            ['ID Analyse:', analysis_id],
            ['Modèle utilisé:', model_version],
        ]
        
        if analysis_data.get('processing_time'):
            tech_data.append(['Temps de traitement:', f"{analysis_data['processing_time']} secondes"])
        
        tech_table = Table(tech_data, colWidths=[5*cm, 9*cm])
        tech_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#f9fafb')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e5e7eb')),
        ]))
        
        elements.append(tech_table)
        return elements
    
    def _create_footer(self, analysis_data: dict) -> list:
        """Crée le pied de page"""
        elements = []
        
        elements.append(Spacer(1, 0.5*cm))
        elements.append(Paragraph("_" * 80, self.styles['BodyText']))
        
        disclaimer = (
            "<i>Ce rapport a été généré automatiquement par un système d'intelligence artificielle. "
            "Il est recommandé qu'un radiologue qualifié examine et valide ces résultats avant toute décision médicale.</i>"
        )
        elements.append(Paragraph(disclaimer, self.styles['BodyText']))
        elements.append(Spacer(1, 0.3*cm))
        
        date_str = datetime.now().strftime('%d/%m/%Y à %H:%M')
        footer = Paragraph(f"Rapport généré le {date_str}", self.styles['BodyText'])
        footer.alignment = TA_CENTER
        elements.append(footer)
        
        return elements
    
    def _get_risk_level(self, bi_rads_num: str) -> str:
        """Détermine le niveau de risque selon BI-RADS"""
        try:
            num = int(bi_rads_num)
            if num <= 2:
                return 'low'
            elif num == 3:
                return 'medium'
            else:
                return 'high'
        except:
            return 'low'

