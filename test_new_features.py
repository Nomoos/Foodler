#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script pro novou funkcionalitu vyhledávání masa a generování nákupního seznamu
"""

import sys
import os
from datetime import datetime

# Přidání cesty pro importy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers.kupi_scraper import KupiCzScraper
from src.analyzers.meat_analyzer import MeatAnalyzer
from src.planners.shopping_list_generator import ShoppingListGenerator


def test_enhanced_scraper():
    """Test vylepšeného scraperu."""
    print("=" * 80)
    print("TEST 1: Vylepšený Kupi.cz Scraper")
    print("=" * 80)
    
    with KupiCzScraper() as scraper:
        # Test 1: Kategorie drůbež
        print("\n1. Test kategorie drůbež:")
        print("   URL: https://www.kupi.cz/slevy/drubez")
        products = scraper.get_current_discounts(category='drubez')
        print(f"   ✓ Nalezeno {len(products)} produktů")
        if products:
            print(f"   Ukázka: {products[0].name} - {products[0].discount_price} Kč")
        
        # Test 2: Obchod Kaufland s řazením
        print("\n2. Test obchodu Kaufland s řazením podle ceny:")
        print("   URL: https://www.kupi.cz/slevy/kaufland?ord=0")
        products = scraper.get_current_discounts(store='kaufland', sort_order=0, page=1)
        print(f"   ✓ Nalezeno {len(products)} produktů")
        if products:
            print(f"   Ukázka: {products[0].name} - {products[0].discount_price} Kč")
        
        # Test 3: Kombinace kategorie a obchodu
        print("\n3. Test kategorie drůbež v Kauflandu:")
        print("   URL: https://www.kupi.cz/slevy/drubez/kaufland")
        products = scraper.get_current_discounts(category='drubez', store='kaufland')
        print(f"   ✓ Nalezeno {len(products)} produktů")
        if products:
            print(f"   Ukázka: {products[0].name} - {products[0].discount_price} Kč")
        
        # Test 4: Stránkování
        print("\n4. Test stránkování (strana 2):")
        print("   URL: https://www.kupi.cz/slevy/kaufland?ord=0&page=2")
        products = scraper.get_current_discounts(store='kaufland', sort_order=0, page=2)
        print(f"   ✓ Nalezeno {len(products)} produktů na straně 2")
        
        # Test 5: AJAX endpoint
        print("\n5. Test AJAX endpointu:")
        print("   URL: https://www.kupi.cz/get-akce/kaufland?page=1&ord=0&load_linear=0&ajax=1")
        products = scraper.get_ajax_discounts(store='kaufland', page=1, sort_order=0)
        print(f"   ✓ Nalezeno {len(products)} produktů přes AJAX")
        if products:
            print(f"   Ukázka: {products[0].name} - {products[0].discount_price} Kč")
    
    print("\n✅ Test scraperu dokončen!\n")


def test_meat_analyzer():
    """Test analyzátoru masných produktů."""
    print("=" * 80)
    print("TEST 2: Analyzátor masných produktů")
    print("=" * 80)
    
    target_date = datetime(2026, 1, 18)
    print(f"\nCílové datum: {target_date.strftime('%d.%m.%Y')} (český formát)")
    print(f"Lokace: Valašské Meziříčí")
    
    with MeatAnalyzer(location="Valašské Meziříčí") as analyzer:
        # Test načtení produktů
        print("\n1. Načítání masných produktů z Kauflandu...")
        products = analyzer.fetch_meat_products(store='kaufland', page=1)
        print(f"   ✓ Nalezeno {len(products)} masných produktů")
        
        if products:
            # Test skórování
            print("\n2. Test skórování produktů pro keto dietu...")
            product = products[0]
            score = analyzer.score_product_for_keto(product)
            print(f"   Produkt: {product.name}")
            print(f"   Keto skóre: {score:.1f}/100")
            
            # Test filtrace podle data
            print("\n3. Test filtrace podle platnosti (18.1.2026)...")
            valid_products = analyzer.filter_valid_on_date(products, target_date)
            print(f"   ✓ Platných produktů: {len(valid_products)}")
            
            # Test reportu (bez nutričního ověření pro rychlost)
            print("\n4. Generování reportu...")
            report = analyzer.generate_report(products[:5], with_nutrition=False)
            print("   ✓ Report vygenerován (zkrácená verze):")
            print("\n" + report[:500] + "...\n")
        else:
            print("   ⚠️  Žádné produkty nenalezeny (může být problém s připojením)")
    
    print("\n✅ Test analyzátoru dokončen!\n")


def test_shopping_list_generator():
    """Test generátoru nákupního seznamu."""
    print("=" * 80)
    print("TEST 3: Generátor nákupního seznamu")
    print("=" * 80)
    
    target_date = datetime(2026, 1, 18)
    stores = ['kaufland', 'albert']  # Omezeno na 2 obchody pro rychlost
    
    print(f"\nCílové datum: {target_date.strftime('%d.%m.%Y')}")
    print(f"Obchody: {', '.join(s.upper() for s in stores)}")
    print(f"Lokace: Valašské Meziříčí")
    
    with ShoppingListGenerator(location="Valašské Meziříčí") as generator:
        print("\n1. Generování týdenního nákupního seznamu...")
        shopping_lists = generator.generate_weekly_list(
            stores=stores,
            target_date=target_date,
            family_size=3
        )
        
        print(f"\n2. Formátování seznamu...")
        list_text = generator.format_shopping_list(shopping_lists, format_type="text")
        
        # Zobrazit zkrácenou verzi
        print("\n✓ Ukázka nákupního seznamu (první 1000 znaků):")
        print("-" * 80)
        print(list_text[:1000])
        print("...")
        print("-" * 80)
        
        # Test exportu
        print("\n3. Test exportu do souboru...")
        test_file = "/tmp/test_shopping_list.txt"
        generator.export_to_file(shopping_lists, test_file, format_type="text")
        print(f"   ✓ Seznam exportován do: {test_file}")
        
        # Ověření, že soubor existuje
        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            print(f"   ✓ Velikost souboru: {file_size} bytů")
        
    print("\n✅ Test generátoru dokončen!\n")


def test_czech_date_parsing():
    """Test parsování českých datumů."""
    print("=" * 80)
    print("TEST 4: Parsování českých datumů")
    print("=" * 80)
    
    from src.scrapers.kupi_scraper import KupiCzScraper
    
    scraper = KupiCzScraper()
    
    test_dates = [
        "18.1.2026",
        "18. 1. 2026",
        "18/1/2026",
        "18. ledna 2026",
        "1. února 2026",
    ]
    
    print("\nTestování různých formátů českých datumů:")
    for date_str in test_dates:
        parsed = scraper._parse_czech_date(date_str)
        if parsed:
            print(f"   ✓ '{date_str}' → {parsed.strftime('%d.%m.%Y')}")
        else:
            print(f"   ✗ '{date_str}' → parsování selhalo")
    
    scraper.close()
    print("\n✅ Test parsování datumů dokončen!\n")


def main():
    """Spustí všechny testy."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "FOODLER - TEST NOVÉ FUNKCIONALITY" + " " * 30 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    try:
        # Test 1: Vylepšený scraper
        test_enhanced_scraper()
        
        # Test 2: Analyzátor masa
        test_meat_analyzer()
        
        # Test 3: Generátor nákupního seznamu
        test_shopping_list_generator()
        
        # Test 4: Parsování českých datumů
        test_czech_date_parsing()
        
        print("=" * 80)
        print("✅ VŠECHNY TESTY DOKONČENY!")
        print("=" * 80)
        print("\n💡 Poznámky:")
        print("   • Některé testy mohou selhat kvůli nedostupnosti webu nebo změnám struktury")
        print("   • Pro úplné testování s nutričním ověřením je potřeba webový přístup")
        print("   • Výsledky jsou optimalizovány pro keto dietu (vysoké bílkoviny, nízké sacharidy)")
        print("\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Testy přerušeny uživatelem")
    except Exception as e:
        print(f"\n❌ Chyba během testování: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
