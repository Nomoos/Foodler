#!/usr/bin/env python3
"""
Příklad integračního testu scraperů s reálnými webovými daty.

Tento soubor demonstruje, jak testovat scrapery s reálnými daty z webů
kaloricketabulky.cz a kupi.cz.

UPOZORNĚNÍ: Pro spuštění těchto testů je potřeba:
1. Aktivní internetové připojení
2. Přístup k cílovým webům
3. GitHub Copilot Pro+ s povoleným webovým přístupem (pro testování přes Copilot)

Použití:
    python test_scrapers_integration.py
"""

import sys
import time
from typing import List, Dict, Optional

# Import scraperů
from fetch_nutrition_data import fetch_by_product_name, search_product, fetch_nutrition_data
from src.scrapers.kupi_scraper import KupiCzScraper


def print_section(title: str):
    """Vytiskne nadpis sekce."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def test_nutrition_scraper():
    """
    Test scraperu pro kaloricketabulky.cz s reálnými daty.
    """
    print_section("Test 1: Scraper nutričních dat (kaloricketabulky.cz)")
    
    # Test 1: Vyhledání produktu podle názvu
    print("1.1 - Vyhledání produktu 'Kuřecí prsa'...")
    try:
        results = search_product("Kuřecí prsa")
        if results:
            print(f"✅ Nalezeno {len(results)} výsledků")
            for i, result in enumerate(results[:3], 1):
                print(f"   {i}. {result['name']}")
        else:
            print("❌ Žádné výsledky nenalezeny")
        time.sleep(2)  # Respekt k serveru
    except Exception as e:
        print(f"❌ Chyba: {e}")
    
    # Test 2: Získání nutričních dat podle názvu
    print("\n1.2 - Získání nutričních dat pro 'Tvaroh tučný'...")
    try:
        data = fetch_by_product_name("Tvaroh tučný")
        if data:
            print(f"✅ Produkt: {data.get('product_name', 'N/A')}")
            print(f"   URL: {data.get('url', 'N/A')}")
            macros = data.get('macros', {})
            if macros:
                print("   Makronutrienty:")
                for key, value in macros.items():
                    print(f"     - {key}: {value}")
            
            # Validace dat
            if 'protein' in macros:
                print("✅ Obsahuje protein data")
            else:
                print("⚠️  Chybí protein data")
        else:
            print("❌ Nepodařilo se získat data")
        time.sleep(2)
    except Exception as e:
        print(f"❌ Chyba: {e}")
    
    # Test 3: Získání dat z konkrétní URL
    print("\n1.3 - Získání dat z konkrétní URL...")
    try:
        url = "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend"
        data = fetch_nutrition_data(url)
        if data:
            print(f"✅ Produkt: {data.get('product_name', 'N/A')}")
            macros = data.get('macros', {})
            if 'protein' in macros:
                print(f"   Protein: {macros['protein']}")
            if 'carbohydrates' in macros:
                print(f"   Sacharidy: {macros['carbohydrates']}")
        else:
            print("❌ Nepodařilo se získat data")
    except Exception as e:
        print(f"❌ Chyba: {e}")


def test_kupi_scraper():
    """
    Test scraperu pro kupi.cz s reálnými daty.
    """
    print_section("Test 2: Scraper slev (kupi.cz)")
    
    try:
        with KupiCzScraper() as scraper:
            # Test 1: Seznam obchodů
            print("2.1 - Získání seznamu obchodů...")
            stores = scraper.get_stores()
            print(f"✅ Nalezeno {len(stores)} obchodů:")
            for store in stores[:5]:
                print(f"   - {store['name']}")
            time.sleep(2)
            
            # Test 2: Vyhledání produktu
            print("\n2.2 - Vyhledání produktu 'kuřecí'...")
            products = scraper.search_products("kuřecí")
            if products:
                print(f"✅ Nalezeno {len(products)} produktů")
                for i, product in enumerate(products[:3], 1):
                    print(f"   {i}. {product.name}")
                    print(f"      Cena: {product.discount_price} Kč")
                    print(f"      Obchod: {product.store}")
            else:
                print("❌ Žádné produkty nenalezeny")
            time.sleep(2)
            
            # Test 3: Aktuální slevy
            print("\n2.3 - Získání aktuálních slev...")
            products = scraper.get_current_discounts()
            if products:
                print(f"✅ Nalezeno {len(products)} produktů ve slevě")
                # Najít nejvyšší slevu
                if products:
                    sorted_products = sorted(
                        [p for p in products if p.discount_percentage],
                        key=lambda x: x.discount_percentage or 0,
                        reverse=True
                    )
                    if sorted_products:
                        best_deal = sorted_products[0]
                        print(f"   Nejlepší sleva: {best_deal.name}")
                        print(f"   Sleva: {best_deal.discount_percentage}%")
                        print(f"   Obchod: {best_deal.store}")
            else:
                print("❌ Žádné produkty nenalezeny nebo web má jinou strukturu")
                
    except Exception as e:
        print(f"❌ Chyba: {e}")


def test_keto_deals():
    """
    Test hledání keto-friendly produktů ve slevě.
    Kombinuje oba scrapery pro komplexní use case.
    """
    print_section("Test 3: Hledání keto-friendly slev")
    
    keto_keywords = ["kuřecí", "vejce", "sýr", "tvaroh", "losos"]
    
    try:
        with KupiCzScraper() as scraper:
            all_keto_products = []
            
            for keyword in keto_keywords:
                print(f"Hledám '{keyword}'...")
                try:
                    products = scraper.search_products(keyword)
                    if products:
                        all_keto_products.extend(products)
                        print(f"  ✅ Nalezeno {len(products)} produktů")
                    time.sleep(2)  # Respekt k serveru
                except Exception as e:
                    print(f"  ❌ Chyba při hledání '{keyword}': {e}")
            
            if all_keto_products:
                # Seřadit podle slevy
                sorted_products = sorted(
                    [p for p in all_keto_products if p.discount_percentage],
                    key=lambda x: x.discount_percentage or 0,
                    reverse=True
                )
                
                print(f"\n✅ Celkem nalezeno {len(all_keto_products)} keto produktů")
                print("\nTop 5 keto slev:")
                for i, product in enumerate(sorted_products[:5], 1):
                    print(f"\n{i}. {product.name}")
                    print(f"   Obchod: {product.store}")
                    print(f"   Cena: {product.discount_price} Kč")
                    print(f"   Sleva: {product.discount_percentage}%")
            else:
                print("❌ Žádné keto produkty nenalezeny")
                
    except Exception as e:
        print(f"❌ Chyba: {e}")


def test_combined_workflow():
    """
    Komplexní test - najdi produkt, získej nutriční data a cenu.
    """
    print_section("Test 4: Kombinovaný workflow")
    
    product_name = "Kuřecí prsa"
    print(f"Hledám informace o produktu: {product_name}\n")
    
    # Krok 1: Nutriční data
    print("1. Získávám nutriční data...")
    try:
        nutrition_data = fetch_by_product_name(product_name)
        if nutrition_data:
            print(f"✅ Nutriční data získána")
            print(f"   Produkt: {nutrition_data.get('product_name', 'N/A')}")
            macros = nutrition_data.get('macros', {})
            if 'protein' in macros:
                print(f"   Protein: {macros['protein']}")
        else:
            print("❌ Nutriční data nenalezena")
        time.sleep(2)
    except Exception as e:
        print(f"❌ Chyba: {e}")
    
    # Krok 2: Aktuální ceny a slevy
    print("\n2. Získávám aktuální ceny...")
    try:
        with KupiCzScraper() as scraper:
            products = scraper.search_products(product_name)
            if products:
                print(f"✅ Nalezeno {len(products)} nabídek")
                for i, product in enumerate(products[:3], 1):
                    print(f"\n   Nabídka {i}:")
                    print(f"   - Obchod: {product.store}")
                    print(f"   - Cena: {product.discount_price} Kč")
                    if product.discount_percentage:
                        print(f"   - Sleva: {product.discount_percentage}%")
            else:
                print("⚠️  Žádné nabídky nenalezeny")
    except Exception as e:
        print(f"❌ Chyba: {e}")
    
    # Krok 3: Doporučení
    print("\n3. Doporučení:")
    if nutrition_data and 'macros' in nutrition_data:
        macros = nutrition_data['macros']
        if 'protein' in macros:
            protein_value = macros['protein']
            print(f"   ✅ {product_name} obsahuje {protein_value} proteinů")
            print(f"   ✅ Vhodné pro high-protein keto dietu")


def main():
    """
    Hlavní funkce - spustí všechny testy.
    """
    print("\n" + "=" * 70)
    print("  INTEGRAČNÍ TESTY SCRAPERŮ S REÁLNÝMI DATY")
    print("=" * 70)
    print("\n⚠️  UPOZORNĚNÍ:")
    print("   - Tyto testy vyžadují aktivní internetové připojení")
    print("   - Respektují rate limiting (2s prodleva mezi požadavky)")
    print("   - Webová struktura se může měnit - testy mohou selhat")
    print("\n")
    
    try:
        # Spustit všechny testy
        test_nutrition_scraper()
        test_kupi_scraper()
        test_keto_deals()
        test_combined_workflow()
        
        # Závěrečné shrnutí
        print_section("SHRNUTÍ")
        print("✅ Všechny testy dokončeny")
        print("\nPokud některé testy selhaly:")
        print("  1. Zkontrolujte internetové připojení")
        print("  2. Ověřte, že weby jsou dostupné")
        print("  3. HTML struktura webů se mohla změnit - aktualizujte scrapery")
        print("  4. Zkontrolujte, že nejste blokováni rate limitingem")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Testy přerušeny uživatelem")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Neočekávaná chyba: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
