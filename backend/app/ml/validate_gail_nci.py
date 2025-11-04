"""
Script de validation du modèle Gail contre le calculateur officiel NCI
https://bcrisktool.cancer.gov/

Instructions d'utilisation :
1. Accéder à https://bcrisktool.cancer.gov/
2. Entrer les mêmes données pour chaque cas de test ci-dessous
3. Noter les résultats obtenus
4. Comparer avec les résultats de ce script
5. Documenter les écarts dans GAIL_VALIDATION_RESULTS.md
"""

from app.ml.gail_risk_calculator import GailModelRiskCalculator

def validate_gail_model():
    """
    Compare les résultats de notre implémentation avec le calculateur NCI officiel
    """
    
    calculator = GailModelRiskCalculator()
    
    print("=" * 80)
    print("VALIDATION DU MODÈLE GAIL - Comparaison avec bcrisktool.cancer.gov")
    print("=" * 80)
    print("\n⚠️  IMPORTANT : Entrez ces mêmes données dans https://bcrisktool.cancer.gov/")
    print("    puis comparez les résultats obtenus.\n")
    
    test_cases = [
        {
            'name': 'Femme 45 ans, profil moyen',
            'data': {
                'age': 45,
                'age_menarche': '12-13',
                'age_first_birth': '25-29',
                'previous_biopsies': 0,
                'atypical_hyperplasia': False,
                'first_degree_relatives': 0
            },
            'nci_input': {
                'Age': 45,
                'Age at first menstrual period': '12-13',
                'Age at first birth': '25-29',
                'Number of breast biopsies': 0,
                'Atypical hyperplasia': 'No',
                'First-degree relatives with breast cancer': 0
            }
        },
        {
            'name': 'Femme 50 ans, 1 parente, profil moyen',
            'data': {
                'age': 50,
                'age_menarche': '12-13',
                'age_first_birth': '25-29',
                'previous_biopsies': 0,
                'atypical_hyperplasia': False,
                'first_degree_relatives': 1
            },
            'nci_input': {
                'Age': 50,
                'Age at first menstrual period': '12-13',
                'Age at first birth': '25-29',
                'Number of breast biopsies': 0,
                'Atypical hyperplasia': 'No',
                'First-degree relatives with breast cancer': 1
            }
        },
        {
            'name': 'Femme 40 ans, ménarche précoce, 1 biopsie',
            'data': {
                'age': 40,
                'age_menarche': '<12',
                'age_first_birth': '30+',
                'previous_biopsies': 1,
                'atypical_hyperplasia': False,
                'first_degree_relatives': 0
            },
            'nci_input': {
                'Age': 40,
                'Age at first menstrual period': '<12',
                'Age at first birth': '30+',
                'Number of breast biopsies': 1,
                'Atypical hyperplasia': 'No',
                'First-degree relatives with breast cancer': 0
            }
        },
        {
            'name': 'Femme 55 ans, 2 parentes, 2 biopsies',
            'data': {
                'age': 55,
                'age_menarche': '12-13',
                'age_first_birth': 'nulliparous',
                'previous_biopsies': 2,
                'atypical_hyperplasia': True,
                'first_degree_relatives': 2
            },
            'nci_input': {
                'Age': 55,
                'Age at first menstrual period': '12-13',
                'Age at first birth': 'Never had children',
                'Number of breast biopsies': 2,
                'Atypical hyperplasia': 'Yes',
                'First-degree relatives with breast cancer': 2
            }
        },
        {
            'name': 'Femme 35 ans, profil jeune faible risque',
            'data': {
                'age': 35,
                'age_menarche': '14+',
                'age_first_birth': '20-24',
                'previous_biopsies': 0,
                'atypical_hyperplasia': False,
                'first_degree_relatives': 0
            },
            'nci_input': {
                'Age': 35,
                'Age at first menstrual period': '14+',
                'Age at first birth': '20-24',
                'Number of breast biopsies': 0,
                'Atypical hyperplasia': 'No',
                'First-degree relatives with breast cancer': 0
            }
        }
    ]
    
    results_comparison = []
    
    for i, test_case in enumerate(test_cases, 1):
        print("\n" + "=" * 80)
        print(f"CAS DE TEST {i} : {test_case['name']}")
        print("=" * 80)
        
        # Calculer avec notre implémentation
        our_result = calculator.calculate_risk(test_case['data'])
        
        print("\n📊 DONNÉES À ENTRER DANS bcrisktool.cancer.gov :")
        for key, value in test_case['nci_input'].items():
            print(f"   {key}: {value}")
        
        print("\n📈 RÉSULTATS DE NOTRE IMPLÉMENTATION :")
        print(f"   Risque 5 ans : {our_result['risk_5_years']:.4f}%")
        print(f"   Risque à vie : {our_result['risk_lifetime']:.4f}%")
        print(f"   Catégorie    : {our_result['risk_category']}")
        print(f"   Risque Gail pur (sans mode de vie) : {our_result['risk_gail_pure']:.4f}%")
        
        print("\n📋 RÉSULTATS À ENTRER DANS bcrisktool.cancer.gov :")
        print("   Entrez les données ci-dessus et notez :")
        print("   - Risque 5 ans (5-year risk) : _____%")
        print("   - Risque à vie (Lifetime risk) : _____%")
        
        # Calculer le risque relatif pour analyse
        rr = calculator._calculate_relative_risk_official(test_case['data'])
        print(f"\n🔍 DÉTAILS TECHNIQUES :")
        print(f"   Risque relatif calculé : {rr:.4f}x")
        
        results_comparison.append({
            'case': test_case['name'],
            'our_5year': our_result['risk_5_years'],
            'our_lifetime': our_result['risk_lifetime'],
            'our_category': our_result['risk_category'],
            'relative_risk': rr
        })
    
    print("\n" + "=" * 80)
    print("RÉSUMÉ DES TESTS")
    print("=" * 80)
    print("\nUne fois que vous avez entré ces données dans bcrisktool.cancer.gov,")
    print("documentez les résultats dans GAIL_VALIDATION_RESULTS.md")
    print("\nSi les écarts sont > 5%, vérifiez :")
    print("  1. Les coefficients β dans l'article original")
    print("  2. L'utilisation de l'intercept")
    print("  3. Les taux d'incidence SEER exacts")
    print("  4. La formule d'intégration du risque absolu")

if __name__ == "__main__":
    validate_gail_model()

