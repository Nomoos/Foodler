#!/usr/bin/env python3
"""
Komplexní test webového přístupu k scraperům
 
Tento skript testuje přístup k:
- kaloricketabulky.cz (scraper nutričních dat)
- kupi.cz (scraper slev)

A vytváří podrobnou zprávu o funkčnosti.
"""

import sys
import time
from typing import Dict, List
import json

# Import scraperů
from fetch_nutrition_data import fetch_nutrition_data, search_product
from src.scrapers.kupi_scraper import KupiCzScraper


def print_header(title: str):
    """Vytiskne nadpis sekce."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_test_result(test_name: str, success: bool, details: str = ""):
    """Vytiskne výsledek testu."""
    icon = "✅" if success else "❌"
    print(f"{icon} {test_name}")
    if details:
        for line in details.split('\n'):
            if line.strip():
                print(f"   {line}")
    print()


def test_kaloricketabulky_cz():
    """
    Test scraperu pro kaloricketabulky.cz s různými produkty.
    """
    print_header("TEST 1: Scraper kaloricketabulky.cz")
    
    results = {
        'accessible': False,
        'data_extraction_works': False,
        'tested_products': [],
        'issues': []
    }
    
    # Seznam testovacích produktů (známé URL)
    test_products = [
        {
            'name': 'Whey Protein',
            'url': 'https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend'
        },
        {
            'name': 'Kuřecí prsa',
            'url': 'https://www.kaloricketabulky.cz/potraviny/kuřecí-prsa'
        },
        {
            'name': 'Tvaroh',
            'url': 'https://www.kaloricketabulky.cz/potraviny/tvaroh'
        }
    ]
    
    successful_tests = 0
    
    for product in test_products:
        print(f"Testuji produkt: {product['name']}...")
        try:
            data = fetch_nutrition_data(product['url'])
            
            if data:
                results['accessible'] = True
                
                # Zkontroluj, zda máme nějaká makra
                has_macros = len(data.get('macros', {})) > 0
                
                if has_macros:
                    results['data_extraction_works'] = True
                    successful_tests += 1
                    
                    details = f"Produkt: {data.get('product_name', 'N/A')}\n"
                    macros = data.get('macros', {})
                    if macros:
                        details += "   Extrahovaná makra:\n"
                        for key, value in macros.items():
                            details += f"     - {key}: {value}\n"
                    
                    print_test_result(
                        f"Produkt '{product['name']}' - data extrahována",
                        True,
                        details.strip()
                    )
                    
                    results['tested_products'].append({
                        'name': product['name'],
                        'url': product['url'],
                        'success': True,
                        'macros_count': len(macros)
                    })
                else:
                    print_test_result(
                        f"Produkt '{product['name']}' - žádná data",
                        False,
                        "Stránka dostupná, ale data nebyla extrahována"
                    )
                    results['issues'].append(f"No macros extracted for {product['name']}")
                    results['tested_products'].append({
                        'name': product['name'],
                        'url': product['url'],
                        'success': False,
                        'reason': 'No macros extracted'
                    })
            else:
                print_test_result(
                    f"Produkt '{product['name']}' - nedostupný",
                    False,
                    f"URL: {product['url']}"
                )
                results['tested_products'].append({
                    'name': product['name'],
                    'url': product['url'],
                    'success': False,
                    'reason': 'Failed to fetch'
                })
        
        except Exception as e:
            print_test_result(
                f"Produkt '{product['name']}' - chyba",
                False,
                f"Chyba: {str(e)}"
            )
            results['issues'].append(f"Exception for {product['name']}: {str(e)}")
        
        time.sleep(2)  # Respekt k serveru
    
    # Test vyhledávání
    print("\nTest vyhledávací funkce...")
    try:
        search_results = search_product("tvaroh")
        if search_results:
            print_test_result(
                "Vyhledávání produktů",
                True,
                f"Nalezeno {len(search_results)} výsledků"
            )
            results['search_works'] = True
        else:
            print_test_result(
                "Vyhledávání produktů",
                False,
                "Žádné výsledky (může být způsobeno JavaScriptem na webu)"
            )
            results['search_works'] = False
            results['issues'].append("Search functionality doesn't return results (likely JS-based)")
    except Exception as e:
        print_test_result(
            "Vyhledávání produktů",
            False,
            f"Chyba: {str(e)}"
        )
        results['search_works'] = False
        results['issues'].append(f"Search error: {str(e)}")
    
    # Shrnutí
    print("\n" + "-" * 80)
    print(f"Shrnutí testu kaloricketabulky.cz:")
    print(f"  - Web dostupný: {'✅ Ano' if results['accessible'] else '❌ Ne'}")
    print(f"  - Extrakce dat funguje: {'✅ Ano' if results['data_extraction_works'] else '❌ Ne'}")
    print(f"  - Úspěšných testů: {successful_tests}/{len(test_products)}")
    print(f"  - Vyhledávání funguje: {'✅ Ano' if results.get('search_works', False) else '❌ Ne'}")
    
    return results


def test_kupi_cz():
    """
    Test scraperu pro kupi.cz.
    """
    print_header("TEST 2: Scraper kupi.cz")
    
    results = {
        'accessible': False,
        'dns_resolves': False,
        'issues': []
    }
    
    # Test DNS resoluce
    print("Test DNS resoluce a přístupu k webu...")
    try:
        with KupiCzScraper() as scraper:
            # Pokus o přístup k hlavní stránce
            soup = scraper.fetch_page('https://www.kupi.cz')
            
            if soup:
                results['accessible'] = True
                results['dns_resolves'] = True
                
                print_test_result(
                    "Přístup k kupi.cz",
                    True,
                    f"Web dostupný\n   Titulek stránky: {soup.title.string if soup.title else 'N/A'}"
                )
                
                # Test vyhledávání
                print("Test vyhledávání produktů...")
                time.sleep(2)
                products = scraper.search_products("kuřecí")
                
                if products:
                    print_test_result(
                        "Vyhledávání produktů na kupi.cz",
                        True,
                        f"Nalezeno {len(products)} produktů"
                    )
                else:
                    print_test_result(
                        "Vyhledávání produktů na kupi.cz",
                        False,
                        "Žádné produkty nenalezeny (může vyžadovat aktualizaci parseru)"
                    )
                
                # Test aktuálních slev
                print("Test získání aktuálních slev...")
                time.sleep(2)
                discounts = scraper.get_current_discounts()
                
                if discounts:
                    print_test_result(
                        "Získání slev z kupi.cz",
                        True,
                        f"Nalezeno {len(discounts)} produktů ve slevě"
                    )
                else:
                    print_test_result(
                        "Získání slev z kupi.cz",
                        False,
                        "Žádné slevy nenalezeny (vyžaduje aktualizaci HTML parseru)"
                    )
                    results['issues'].append("Product parsing needs to be updated for current HTML structure")
            
            else:
                results['dns_resolves'] = False
                print_test_result(
                    "Přístup k kupi.cz",
                    False,
                    "Web nedostupný - DNS resoluce selhala nebo web je zablokován"
                )
                results['issues'].append("Cannot resolve www.kupi.cz - DNS or network issue")
    
    except Exception as e:
        print_test_result(
            "Test kupi.cz",
            False,
            f"Chyba: {str(e)}"
        )
        results['issues'].append(f"Exception: {str(e)}")
    
    # Shrnutí
    print("\n" + "-" * 80)
    print(f"Shrnutí testu kupi.cz:")
    print(f"  - DNS resoluce: {'✅ Ano' if results.get('dns_resolves', False) else '❌ Ne'}")
    print(f"  - Web dostupný: {'✅ Ano' if results['accessible'] else '❌ Ne'}")
    
    return results


def generate_summary_report(kt_results: Dict, kupi_results: Dict):
    """
    Vygeneruje finální shrnutí všech testů.
    """
    print_header("FINÁLNÍ SHRNUTÍ TESTŮ WEBOVÉHO PŘÍSTUPU")
    
    # Celkový status
    kt_ok = kt_results['accessible'] and kt_results['data_extraction_works']
    kupi_ok = kupi_results['accessible']
    
    print("📊 STATUS SCRAPERŮ:")
    print()
    print(f"kaloricketabulky.cz scraper: {'✅ FUNKČNÍ' if kt_ok else '⚠️  ČÁSTEČNĚ FUNKČNÍ' if kt_results['accessible'] else '❌ NEFUNKČNÍ'}")
    print(f"  - Web přístup: {'✅' if kt_results['accessible'] else '❌'}")
    print(f"  - Extrakce dat: {'✅' if kt_results['data_extraction_works'] else '❌'}")
    print(f"  - Vyhledávání: {'✅' if kt_results.get('search_works', False) else '⚠️ '}")
    
    print()
    print(f"kupi.cz scraper: {'✅ FUNKČNÍ' if kupi_ok else '❌ NEFUNKČNÍ'}")
    print(f"  - Web přístup: {'✅' if kupi_results['accessible'] else '❌'}")
    print(f"  - DNS resoluce: {'✅' if kupi_results.get('dns_resolves', False) else '❌'}")
    
    # Podrobné informace
    print()
    print("📝 PODROBNOSTI:")
    print()
    
    # kaloricketabulky.cz detaily
    if kt_results['tested_products']:
        successful = [p for p in kt_results['tested_products'] if p.get('success', False)]
        print(f"kaloricketabulky.cz - Otestováno {len(kt_results['tested_products'])} produktů:")
        print(f"  - Úspěšných: {len(successful)}")
        print(f"  - Neúspěšných: {len(kt_results['tested_products']) - len(successful)}")
    
    # Známé problémy
    print()
    print("⚠️  ZNÁMÉ PROBLÉMY:")
    print()
    
    all_issues = []
    all_issues.extend([f"[kaloricketabulky.cz] {issue}" for issue in kt_results.get('issues', [])])
    all_issues.extend([f"[kupi.cz] {issue}" for issue in kupi_results.get('issues', [])])
    
    if all_issues:
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("  Žádné problémy nebyly detekovány! 🎉")
    
    # Doporučení
    print()
    print("💡 DOPORUČENÍ:")
    print()
    
    if not kt_results.get('search_works', False):
        print("  • kaloricketabulky.cz: Vyhledávání nefunguje (pravděpodobně vyžaduje JavaScript).")
        print("    → Používejte přímé URL produktů nebo implementujte API, pokud je dostupné.")
    
    if not kupi_results['accessible']:
        print("  • kupi.cz: Web není přístupný z tohoto prostředí.")
        print("    → Zkontrolujte síťová omezení, firewall nebo použijte proxy.")
        print("    → Doména www.kupi.cz nemůže být vyřešena - možná DNS problém.")
    elif kupi_results['accessible'] and kupi_results.get('issues'):
        print("  • kupi.cz: Web je přístupný, ale parsování produktů nefunguje.")
        print("    → Aktualizujte HTML parsovací logiku podle aktuální struktury webu.")
    
    if kt_ok:
        print("  • kaloricketabulky.cz scraper funguje dobře! ✅")
        print("    → Můžete jej používat pro získávání nutričních dat.")
    
    # JSON výstup pro případné automatické zpracování
    print()
    print("=" * 80)
    print("JSON výstup výsledků:")
    print("=" * 80)
    
    json_output = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'kaloricketabulky_cz': kt_results,
        'kupi_cz': kupi_results,
        'summary': {
            'kaloricketabulky_functional': kt_ok,
            'kupi_functional': kupi_ok,
            'total_issues': len(all_issues)
        }
    }
    
    print(json.dumps(json_output, indent=2, ensure_ascii=False))


def main():
    """
    Hlavní funkce - spustí všechny testy.
    """
    print("=" * 80)
    print("  TEST WEBOVÉHO PŘÍSTUPU K SCRAPERŮM")
    print("  Foodler - Dietní plánovač")
    print("=" * 80)
    print()
    print("Tento test ověřuje:")
    print("  1. Přístup k webům kaloricketabulky.cz a kupi.cz")
    print("  2. Funkčnost scraperů pro získávání dat")
    print("  3. Kvalitu extrahovaných dat")
    print()
    print("⏳ Začínám testování...")
    
    try:
        # Test 1: kaloricketabulky.cz
        kt_results = test_kaloricketabulky_cz()
        
        # Test 2: kupi.cz
        kupi_results = test_kupi_cz()
        
        # Vygeneruj finální zprávu
        generate_summary_report(kt_results, kupi_results)
        
        print()
        print("=" * 80)
        print("  TESTOVÁNÍ DOKONČENO")
        print("=" * 80)
        
        # Exit code based on results
        if kt_results['accessible'] or kupi_results['accessible']:
            sys.exit(0)  # At least one scraper is accessible
        else:
            sys.exit(1)  # No scrapers are accessible
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Testování přerušeno uživatelem")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Neočekávaná chyba: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
