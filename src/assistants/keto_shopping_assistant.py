#!/usr/bin/env python3
"""
Keto dietní nákupní asistent
Tento modul obsahuje logiku asistenta (Single Responsibility)
"""

import sys
import os

# Přidání rodičovské složky do cesty pro importy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scrapers.kupi_scraper import KupiCzScraper
from modely.product import Product
from data.keto_foods import KETO_FOODS
from typing import List, Dict
import time


def find_keto_deals(scraper: KupiCzScraper, category: str, keywords: List[str], 
                    max_results: int = 5) -> List[Product]:
    """
    Najde zlevněné keto-friendly produkty.
    
    Args:
        scraper: KupiCzScraper instance
        category: Název kategorie
        keywords: Seznam vyhledávacích klíčových slov
        max_results: Maximální počet výsledků na klíčové slovo
        
    Returns:
        Seznam Product objektů
    """
    print(f"\n🔍 Vyhledávání {category}...")
    all_products = []
    
    for keyword in keywords:
        print(f"  Vyhledávání: {keyword}...", end=' ')
        try:
            products = scraper.search_products(keyword)
            if products:
                print(f"✓ Nalezeno {len(products)}")
                all_products.extend(products[:max_results])
            else:
                print("✗ Žádné výsledky")
            time.sleep(1)  # Omezení rychlosti
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    # Odstranění duplikátů a řazení podle slevy
    unique_products = {p.name: p for p in all_products}.values()
    sorted_products = sorted(
        unique_products, 
        key=lambda p: p.discount_percentage or 0, 
        reverse=True
    )
    
    return list(sorted_products)


def display_products(products: List[Product], title: str, max_display: int = 10):
    """Zobrazí produkty ve formátované tabulce."""
    if not products:
        print(f"\n{title}")
        print("  Žádné produkty nenalezeny.")
        return
    
    print(f"\n{title}")
    print("=" * 80)
    print(f"{'#':<3} {'Produkt':<35} {'Cena':<12} {'Sleva':<10} {'Obchod':<15}")
    print("-" * 80)
    
    for i, product in enumerate(products[:max_display], 1):
        name = product.name[:32] + "..." if len(product.name) > 35 else product.name
        price = f"{product.discount_price:.2f} Kč"
        discount = f"{product.discount_percentage:.0f}%" if product.discount_percentage else "N/A"
        store = product.store[:12]
        
        print(f"{i:<3} {name:<35} {price:<12} {discount:<10} {store:<15}")


def generate_shopping_list(keto_deals: Dict[str, List[Product]]) -> None:
    """Vygeneruje nákupní seznam z nejlepších nabídek."""
    print("\n" + "=" * 80)
    print("📋 DOPORUČENÝ NÁKUPNÍ SEZNAM PRO KETO DIETU")
    print("=" * 80)
    
    for category, products in keto_deals.items():
        if not products:
            continue
        
        info = KETO_FOODS.get(category, {})
        description = info.get('description', category)
        
        print(f"\n{description}:")
        for product in products[:3]:  # Top 3 z každé kategorie
            discount_info = f" (-{product.discount_percentage:.0f}%)" if product.discount_percentage else ""
            print(f"  ☑ {product.name}")
            print(f"     {product.discount_price:.2f} Kč u {product.store}{discount_info}")


def calculate_weekly_budget(keto_deals: Dict[str, List[Product]]) -> None:
    """Vypočítá odhadovaný týdenní rozpočet na základě nabídek."""
    print("\n" + "=" * 80)
    print("💰 ODHAD TÝDENNÍHO ROZPOČTU")
    print("=" * 80)
    
    # Odhad týdenních potřeb (7 dní, 6 jídel/den)
    weekly_needs = {
        'high_protein': 7,   # 7 zdrojů bílkovin týdně (1 denně pro hlavní jídla)
        'dairy': 3,          # 3 mléčné výrobky
        'vegetables': 4,     # 4 balení zeleniny
        'healthy_fats': 2,   # 2 zdroje tuků
        'supplements': 2     # 2 doplňkové položky
    }
    
    total_cost = 0
    print("\nKategorie              Položky  Průměr cena  Mezisoučet")
    print("-" * 60)
    
    for category, products in keto_deals.items():
        if not products or category not in weekly_needs:
            continue
        
        items_needed = weekly_needs[category]
        avg_price = sum(p.discount_price for p in products[:items_needed]) / min(len(products), items_needed)
        subtotal = avg_price * items_needed
        total_cost += subtotal
        
        info = KETO_FOODS.get(category, {})
        description = info.get('description', category)[:20]
        
        print(f"{description:<20} {items_needed:>7}  {avg_price:>11.2f} Kč  {subtotal:>10.2f} Kč")
    
    print("-" * 60)
    print(f"{'CELKOVÉ TÝDENNÍ NÁKLADY:':<20}              {total_cost:>10.2f} Kč")
    print(f"\nOdhadované denní náklady: {total_cost/7:.2f} Kč")


def main():
    """Hlavní funkce pro spuštění keto nákupního asistenta."""
    print("=" * 80)
    print("🥑 FOODLER KETO DIETNÍ NÁKUPNÍ ASISTENT")
    print("=" * 80)
    print("\nTento nástroj vám pomůže najít zlevněné keto-friendly produkty")
    print("z českých supermarketů podle požadavků Foodler dietního plánu:")
    print("  • Denně: 2000 kcal, 140g+ bílkovin, <70g sacharidů, 129g tuků")
    print("  • 6 jídel denně")
    print("  • Ketogenní/Nízkosacharidový přístup")
    
    try:
        with KupiCzScraper() as scraper:
            print("\n📍 Dostupné obchody:")
            stores = scraper.get_stores()
            for store in stores:
                print(f"  • {store['name']}")
            
            # Shromáždění nabídek pro každou kategorii
            keto_deals = {}
            
            for category, info in KETO_FOODS.items():
                products = find_keto_deals(
                    scraper, 
                    info['description'], 
                    info['keywords'],
                    max_results=5
                )
                keto_deals[category] = products
                
                # Zobrazení výsledků
                display_products(
                    products, 
                    f"\n🏆 Top nabídky: {info['description']}",
                    max_display=5
                )
            
            # Vygenerování nákupního seznamu
            generate_shopping_list(keto_deals)
            
            # Výpočet rozpočtu
            calculate_weekly_budget(keto_deals)
            
            print("\n" + "=" * 80)
            print("✅ Nákupní asistent dokončen!")
            print("\nPoznámka: Ceny a dostupnost se mohou lišit. Vždy zkontrolujte")
            print("detaily produktů a nutriční informace před nákupem.")
            print("\nPro více informací viz KUPI_INTEGRATION.md")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Přerušeno uživatelem")
    except Exception as e:
        print(f"\n\n❌ Chyba: {e}")
        print("\nTo se může stát pokud:")
        print("  • Nejste připojeni k internetu")
        print("  • Struktura webu se změnila")
        print("  • Web blokuje automatizované požadavky")
        print("\nStruktura scraperu je připravena, ale může vyžadovat přizpůsobení")
        print("na základě skutečné HTML struktury kupi.cz")


if __name__ == "__main__":
    main()
