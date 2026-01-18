#!/usr/bin/env python3
"""
Skript pro stažení a uložení slev ze všech obchodů na kupi.cz.
Stahuje kompletní seznamy slev včetně dat platnosti a ukládá je do JSON.
"""

import sys
import os
from datetime import datetime

# Přidání cesty pro import modulů
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers.kupi_scraper import KupiCzScraper


def main():
    """Hlavní funkce pro stažení a uložení slev."""
    print("=" * 70)
    print("Kupi.cz - Stahování slev ze všech obchodů")
    print("=" * 70)
    print()
    
    # Vytvoření scraperu
    with KupiCzScraper() as scraper:
        print("📥 Začínám stahovat slevy ze všech obchodů...")
        print("⏱️  To může trvat několik minut (respektujeme rate limiting)")
        print()
        
        # Stažení slev ze všech obchodů
        all_discounts = scraper.scrape_all_shop_discounts()
        
        # Statistiky
        print()
        print("=" * 70)
        print("📊 Statistiky stažených dat:")
        print("=" * 70)
        
        total_products = 0
        for store_id, products in all_discounts.items():
            count = len(products)
            total_products += count
            store_name = next(
                (s['name'] for s in scraper.get_stores() if s['id'] == store_id), 
                store_id
            )
            print(f"  {store_name:15} - {count:4} produktů")
        
        print("-" * 70)
        print(f"  {'CELKEM':15} - {total_products:4} produktů")
        print()
        
        # Příklad produktů s datumy
        print("=" * 70)
        print("📅 Příklady produktů s datumy platnosti:")
        print("=" * 70)
        
        products_with_dates = []
        for store_id, products in all_discounts.items():
            for product in products:
                if product.valid_from or product.valid_until:
                    products_with_dates.append(product)
                    if len(products_with_dates) >= 5:
                        break
            if len(products_with_dates) >= 5:
                break
        
        if products_with_dates:
            for product in products_with_dates:
                print(f"\n  📦 {product.name}")
                print(f"     💰 Cena: {product.discount_price} Kč", end="")
                if product.discount_percentage:
                    print(f" (-{product.discount_percentage}%)", end="")
                print()
                print(f"     🏪 Obchod: {product.store}")
                if product.valid_from:
                    print(f"     📅 Platnost od: {product.valid_from.strftime('%d.%m.%Y')}")
                if product.valid_until:
                    print(f"     📅 Platnost do: {product.valid_until.strftime('%d.%m.%Y')}")
        else:
            print("  ⚠️  Nepodařilo se extrahovat data platnosti z HTML")
            print("  ℹ️  Data jsou uložena, ale bez informací o platnosti")
        
        # Uložení do JSON
        print()
        print("=" * 70)
        print("💾 Ukládám data do JSON souboru...")
        print("=" * 70)
        
        filepath = scraper.save_discounts_to_json(all_discounts)
        
        print(f"✅ Data úspěšně uložena do: {filepath}")
        print(f"📊 Celkem: {total_products} produktů z {len(all_discounts)} obchodů")
        print()
        
        # Informace o struktuře souboru
        print("=" * 70)
        print("📄 Struktura JSON souboru:")
        print("=" * 70)
        print("""
  {
    "scraped_at": "2026-01-18T10:30:00",
    "total_stores": 8,
    "total_products": 1234,
    "stores": {
      "lidl": {
        "product_count": 150,
        "products": [
          {
            "name": "Produkt",
            "original_price": 100.0,
            "discount_price": 75.0,
            "discount_percentage": 25.0,
            "store": "Lidl",
            "valid_from": "2026-01-15T00:00:00",
            "valid_until": "2026-01-21T00:00:00",
            "image_url": "https://...",
            "product_url": "https://...",
            "category": null
          }
        ]
      }
    }
  }
        """)
        
        print("=" * 70)
        print("✨ Hotovo!")
        print("=" * 70)
        print()
        print("Načtení dat:")
        print(f"  discounts = scraper.load_discounts_from_json('{filepath}')")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Přerušeno uživatelem")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Chyba: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
