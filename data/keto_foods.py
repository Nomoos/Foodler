"""
Keto dietní data a kategorie potravin
Tento modul obsahuje pouze datové definice (Single Responsibility)
"""

from typing import Dict, List


# Keto-friendly kategorie potravin podle Foodler dietního plánu
KETO_FOODS = {
    'high_protein': {
        'keywords': ['kuřecí', 'krůtí', 'hovězí', 'vepřové', 'ryba', 'losos', 'tuňák', 'vejce'],
        'description': 'Zdroje bílkovin (Kuře, Krůta, Hovězí, Ryby, Vejce)',
        'target_macros': {'protein': 'high', 'carbs': 'low', 'fat': 'medium'}
    },
    'dairy': {
        'keywords': ['sýr', 'tvaroh', 'jogurt', 'máslo', 'smetana'],
        'description': 'Mléčné výrobky (Sýr, Tvaroh, Jogurt)',
        'target_macros': {'protein': 'medium', 'carbs': 'low', 'fat': 'high'}
    },
    'vegetables': {
        'keywords': ['brokolice', 'špenát', 'salát', 'cuketa', 'paprika', 'rajčata'],
        'description': 'Nízkosacharidová zelenina',
        'target_macros': {'protein': 'low', 'carbs': 'low', 'fat': 'low'}
    },
    'healthy_fats': {
        'keywords': ['avokádo', 'olivový olej', 'ořechy', 'mandle', 'vlašské ořechy'],
        'description': 'Zdravé tuky (Avokádo, Olivový olej, Ořechy)',
        'target_macros': {'protein': 'low', 'carbs': 'low', 'fat': 'high'}
    },
    'supplements': {
        'keywords': ['chia', 'psyllium', 'protein', 'omega'],
        'description': 'Doplňky a semínka',
        'target_macros': {'protein': 'varies', 'carbs': 'varies', 'fat': 'varies'}
    }
}


def get_keto_categories() -> Dict[str, Dict]:
    """Vrátí všechny keto kategorie."""
    return KETO_FOODS


def get_category_keywords(category: str) -> List[str]:
    """Vrátí klíčová slova pro danou kategorii."""
    return KETO_FOODS.get(category, {}).get('keywords', [])


def get_all_keywords() -> List[str]:
    """Vrátí všechna klíčová slova napříč všemi kategoriemi."""
    all_keywords = []
    for category_data in KETO_FOODS.values():
        all_keywords.extend(category_data.get('keywords', []))
    return all_keywords
