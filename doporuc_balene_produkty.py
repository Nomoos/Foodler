#!/usr/bin/env python3
"""
Doporučení balených mléčných výrobků vhodných pro keto/low-carb dietu.
Vyhledává jogurty, tvarohy a podobné produkty v akci pomocí Kupi.cz.
"""

import sys
import os
from typing import List, Dict, Tuple
from datetime import datetime

# Přidání cesty pro import modulů
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers.kupi_scraper import KupiCzScraper
from modely.product import Product


# Kategorie mléčných výrobků vhodných pro keto dietu
DAIRY_CATEGORIES = {
    'tvarohy': {
        'keywords': ['tvaroh', 'tvaroh tučný', 'cottage cheese', 'tvaroh měkký'],
        'description': '🧀 Tvarohy',
        'suitable_keywords': ['tučný', 'plnotučný', 'nesladký', 'přírodní'],
        'unsuitable_keywords': ['ochucený sladký', 's džemem', 's ovocem', 'vanilkový s cukrem'],
        'max_carbs_per_100g': 5.0,  # max sacharidy na 100g
        'priority': 1
    },
    'jogurty': {
        'keywords': ['jogurt', 'řecký jogurt', 'bílý jogurt', 'kysaný výrobek', 'jogurt řecký'],
        'description': '🥛 Jogurty',
        'suitable_keywords': ['řecký', 'bílý', 'přírodní', 'nesladený', 'celotučný'],
        'unsuitable_keywords': ['ovocný', 's ovocem', 'jahoda', 'malina', 'broskev'],
        'max_carbs_per_100g': 6.0,
        'priority': 2
    },
    'syry': {
        'keywords': ['sýr', 'eidam', 'gouda', 'ementál', 'čedar', 'parmazán', 'mozzarella'],
        'description': '🧀 Sýry',
        'suitable_keywords': ['tvrdý', 'polotvrdý', 'přírodní', 'zrající'],
        'unsuitable_keywords': ['tavený', 'sýr s příchutí', 'sýr uzený'],
        'max_carbs_per_100g': 2.0,
        'priority': 1
    },
    'smetanove_produkty': {
        'keywords': ['zakysaná smetana', 'smetana', 'mascarpone', 'smetanový sýr'],
        'description': '🍶 Smetanové produkty',
        'suitable_keywords': ['zakysaná', 'ke šlehání', 'mascarpone', 'plnotučná'],
        'unsuitable_keywords': ['light', 'nízkotučná'],
        'max_carbs_per_100g': 5.0,
        'priority': 3
    }
}


def evaluate_product_suitability(product: Product, category_info: Dict) -> Tuple[bool, int, str]:
    """
    Vyhodnotí vhodnost produktu pro keto dietu.
    
    Args:
        product: Product objekt
        category_info: Informace o kategorii
        
    Returns:
        Tuple (je_vhodný, skóre 0-100, důvod)
    """
    score = 50  # základní skóre
    reasons = []
    
    product_name_lower = product.name.lower()
    
    # Kontrola nevhodných klíčových slov (disqualifikace)
    for unsuitable in category_info.get('unsuitable_keywords', []):
        if unsuitable in product_name_lower:
            return False, 0, f"Obsahuje nevhodné: {unsuitable}"
    
    # Bonus za vhodná klíčová slova
    suitable_found = []
    for suitable in category_info.get('suitable_keywords', []):
        if suitable in product_name_lower:
            score += 15
            suitable_found.append(suitable)
    
    if suitable_found:
        reasons.append(f"Obsahuje: {', '.join(suitable_found)}")
    
    # Penalizace za vysoké sacharidy (odhadnuto z názvu)
    # Pokud obsahuje 'nízkotučný' nebo 'light', pravděpodobně má více sacharidů
    if 'nízkotučný' in product_name_lower or 'light' in product_name_lower:
        score -= 20
        reasons.append("Může obsahovat více sacharidů (light verze)")
    
    # Bonus za vysokou slevu
    if product.discount_percentage:
        if product.discount_percentage >= 30:
            score += 10
            reasons.append(f"Vysoká sleva {product.discount_percentage:.0f}%")
        elif product.discount_percentage >= 20:
            score += 5
    
    # Kontrola priority kategorie
    priority_bonus = (4 - category_info.get('priority', 3)) * 5
    score += priority_bonus
    
    is_suitable = score >= 60
    reason_text = '; '.join(reasons) if reasons else "Základní vhodnost"
    
    return is_suitable, min(score, 100), reason_text


def search_dairy_products(scraper: KupiCzScraper) -> Dict[str, List[Tuple[Product, int, str]]]:
    """
    Vyhledá mléčné produkty v akci a vyhodnotí jejich vhodnost.
    
    Args:
        scraper: KupiCzScraper instance
        
    Returns:
        Slovník s produkty podle kategorií (produkt, skóre, důvod)
    """
    all_results = {}
    
    for category_id, category_info in DAIRY_CATEGORIES.items():
        print(f"\n{category_info['description']} - Vyhledávání...")
        print("=" * 70)
        
        category_products = []
        seen_names = set()  # Pro odstranění duplikátů
        
        for keyword in category_info['keywords']:
            print(f"  🔍 Vyhledávám: '{keyword}'...", end=' ')
            try:
                import time
                time.sleep(2)  # Rate limiting
                
                products = scraper.search_products(keyword)
                
                if products:
                    print(f"✓ {len(products)} nalezeno")
                    
                    for product in products:
                        # Odstranění duplikátů podle názvu
                        if product.name in seen_names:
                            continue
                        seen_names.add(product.name)
                        
                        # Vyhodnocení vhodnosti
                        is_suitable, score, reason = evaluate_product_suitability(
                            product, category_info
                        )
                        
                        if is_suitable:
                            category_products.append((product, score, reason))
                else:
                    print("✗ Žádné výsledky")
                    
            except Exception as e:
                print(f"✗ Chyba: {e}")
        
        # Seřazení podle skóre
        category_products.sort(key=lambda x: x[1], reverse=True)
        all_results[category_id] = category_products
        
        print(f"  ✅ Celkem nalezeno {len(category_products)} vhodných produktů")
    
    return all_results


def display_recommendations(results: Dict[str, List[Tuple[Product, int, str]]]):
    """
    Zobrazí doporučené produkty pro každou kategorii.
    
    Args:
        results: Slovník s výsledky vyhledávání
    """
    print("\n" + "=" * 80)
    print("🎯 DOPORUČENÉ BALENÉ PRODUKTY PRO KETO/LOW-CARB DIETU")
    print("=" * 80)
    print("\nTyto produkty jsou aktuálně v akci a jsou vhodné pro dietní plán:")
    print("  • Roman: max 70g sacharidů/den")
    print("  • Pája: max 60g sacharidů/den")
    print("  • Důraz na vysoký obsah bílkovin a zdravých tuků")
    
    for category_id, products_with_scores in results.items():
        if not products_with_scores:
            continue
        
        category_info = DAIRY_CATEGORIES[category_id]
        print(f"\n{category_info['description']}")
        print("=" * 80)
        
        # Zobrazit top 10 produktů z každé kategorie
        for i, (product, score, reason) in enumerate(products_with_scores[:10], 1):
            print(f"\n{i}. {product.name}")
            print(f"   💰 Cena: {product.discount_price:.2f} Kč", end="")
            if product.discount_percentage:
                print(f" (sleva {product.discount_percentage:.0f}%)", end="")
            if product.original_price:
                print(f" - původní {product.original_price:.2f} Kč", end="")
            print()
            print(f"   🏪 Obchod: {product.store}")
            print(f"   ⭐ Skóre vhodnosti: {score}/100")
            print(f"   📋 Důvod: {reason}")
            
            if product.valid_from or product.valid_until:
                validity = "   📅 Platnost:"
                if product.valid_from:
                    validity += f" od {product.valid_from.strftime('%d.%m.%Y')}"
                if product.valid_until:
                    validity += f" do {product.valid_until.strftime('%d.%m.%Y')}"
                print(validity)


def generate_shopping_summary(results: Dict[str, List[Tuple[Product, int, str]]]):
    """
    Vygeneruje shrnutí doporučeného nákupu.
    
    Args:
        results: Slovník s výsledky vyhledávání
    """
    print("\n" + "=" * 80)
    print("📋 SHRNUTÍ DOPORUČENÉHO NÁKUPU")
    print("=" * 80)
    
    total_products = sum(len(products) for products in results.values())
    print(f"\nCelkem nalezeno {total_products} vhodných produktů v akci")
    
    print("\n🥇 TOP 5 DOPORUČENÍ (napříč všemi kategoriemi):")
    print("-" * 80)
    
    # Spojit všechny produkty a vybrat top 5
    all_products = []
    for category_id, products_with_scores in results.items():
        category_info = DAIRY_CATEGORIES[category_id]
        for product, score, reason in products_with_scores:
            all_products.append((product, score, reason, category_info['description']))
    
    # Seřadit podle skóre
    all_products.sort(key=lambda x: x[1], reverse=True)
    
    for i, (product, score, reason, category_desc) in enumerate(all_products[:5], 1):
        print(f"\n{i}. {product.name}")
        print(f"   Kategorie: {category_desc}")
        print(f"   Cena: {product.discount_price:.2f} Kč u {product.store}", end="")
        if product.discount_percentage:
            print(f" (-{product.discount_percentage:.0f}%)")
        else:
            print()
        print(f"   Skóre: {score}/100 - {reason}")
    
    print("\n" + "=" * 80)
    print("💡 TIPY PRO VÝBĚR:")
    print("=" * 80)
    print("""
✓ Tvarohy:
  - Preferujte tučné nebo plnotučné varianty
  - Přírodní tvaroh je nejlepší volba
  - Tvaroh s cibulkou nebo bylinkami je OK
  - VYHNĚTE SE: tvarohům s džemem, ovocem nebo sladkým příchutím

✓ Jogurty:
  - Řecký jogurt má nejvíce bílkovin
  - Bílý přírodní jogurt bez přidaného cukru
  - Celotučné varianty jsou vhodnější než light
  - VYHNĚTE SE: ovocným jogurtům, sladkým příchutím

✓ Sýry:
  - Tvrdé a polotvrdé sýry mají minimum sacharidů
  - Přírodní zrající sýry jsou nejlepší
  - Eidam, gouda, čedar jsou výborné volby
  - VYHNĚTE SE: taveným sýrům (více sacharidů)

✓ Ochucené produkty:
  - Ochucené SLANÉ produkty jsou OK (cibulka, byliny, česnek)
  - Ochucené SLADKÉ produkty NEJSOU vhodné (vanilka, ovoce)
    
⚠️  VŽDY si ověřte nutriční hodnoty na obalu!
    Tyto doporučení jsou založeny na obecných znalostech o produktech.
    """)


def main():
    """Hlavní funkce pro doporučení balených produktů."""
    print("=" * 80)
    print("🧀 FOODLER - DOPORUČENÍ BALENÝCH MLÉČNÝCH VÝROBKŮ")
    print("=" * 80)
    print("\nVyhledávání jogurtů, tvarohů a podobných produktů v akci")
    print("vhodných pro keto/low-carb dietu\n")
    
    try:
        with KupiCzScraper() as scraper:
            # Zobrazit dostupné obchody
            print("📍 Vyhledávání v obchodech:")
            stores = scraper.get_stores()
            print("   " + ", ".join(store['name'] for store in stores))
            
            # Vyhledat produkty
            results = search_dairy_products(scraper)
            
            # Zobrazit doporučení
            display_recommendations(results)
            
            # Vygenerovat shrnutí
            generate_shopping_summary(results)
            
            print("\n" + "=" * 80)
            print("✅ HOTOVO!")
            print("=" * 80)
            print("\nPro aktuální nutriční hodnoty produktů použijte:")
            print("  python fetch_nutrition_data.py")
            print("\nPro komplexní nákupní asistent použijte:")
            print("  python src/assistants/keto_shopping_assistant.py")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Přerušeno uživatelem")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Chyba: {e}")
        print("\nMožné příčiny:")
        print("  • Nejste připojeni k internetu")
        print("  • Struktura webu kupi.cz se změnila")
        print("  • Web dočasně nedostupný")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
