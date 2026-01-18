#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor nákupního seznamu pro keto dietu
Vytváří optimalizované nákupní seznamy pro různé obchody
"""

import sys
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict

# Add parent directory to path for imports when running as standalone script
# This allows the script to be run directly (python3 src/planners/shopping_list_generator.py)
# For proper package imports, use: python3 -m src.planners.shopping_list_generator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.scrapers.kupi_scraper import KupiCzScraper
from src.analyzers.meat_analyzer import MeatAnalyzer
from modely.product import Product


class ShoppingListGenerator:
    """Generátor nákupního seznamu optimalizovaného pro keto dietu."""
    
    def __init__(self, location: str = "Valašské Meziříčí"):
        """
        Inicializace generátoru.
        
        Args:
            location: Lokace pro filtrování obchodů
        """
        self.location = location
        self.scraper = KupiCzScraper()
        self.meat_analyzer = MeatAnalyzer(location=location)
    
    def generate_weekly_list(self, stores: List[str], 
                            target_date: datetime,
                            family_size: int = 3) -> Dict[str, List[Product]]:
        """
        Vygeneruje týdenní nákupní seznam pro rodinu.
        
        Args:
            stores: Seznam obchodů (např. ['kaufland', 'albert', 'tesco', 'billa'])
            target_date: Cílové datum pro platnost akcí
            family_size: Počet osob v rodině
            
        Returns:
            Slovník obchod -> seznam doporučených produktů
        """
        shopping_lists = {}
        
        for store in stores:
            print(f"\n📍 Generování seznamu pro {store.upper()}...")
            products = self._fetch_store_products(store, target_date)
            
            if products:
                # Seřadit podle keto skóre a ceny
                scored_products = []
                for product in products:
                    score = self.meat_analyzer.score_product_for_keto(product)
                    scored_products.append((product, score))
                
                scored_products.sort(key=lambda x: x[1], reverse=True)
                
                # Vybrat top produkty
                top_products = [p for p, s in scored_products[:15]]
                shopping_lists[store] = top_products
                print(f"   ✅ Vybráno {len(top_products)} produktů")
            else:
                shopping_lists[store] = []
                print(f"   ⚠️  Žádné produkty nenalezeny")
        
        return shopping_lists
    
    def _fetch_store_products(self, store: str, target_date: datetime) -> List[Product]:
        """
        Načte produkty z konkrétního obchodu.
        
        Args:
            store: Název obchodu
            target_date: Datum platnosti
            
        Returns:
            Seznam produktů
        """
        all_products = []
        
        # Načíst masné produkty
        meat_products = self.meat_analyzer.fetch_meat_products(store=store, page=1)
        all_products.extend(meat_products)
        
        # Načíst další keto-friendly kategorie
        keto_keywords = ['sýr', 'tvaroh', 'vejce', 'avokádo', 'ořechy']
        for keyword in keto_keywords[:3]:  # Omezit pro rychlost
            try:
                products = self.scraper.search_products(keyword)
                # Filtrovat podle obchodu
                store_products = [p for p in products if store.lower() in p.store.lower()]
                all_products.extend(store_products[:5])  # Max 5 na klíčové slovo
            except Exception as e:
                print(f"   Chyba při hledání '{keyword}': {e}")
        
        # Filtrovat podle data platnosti
        valid_products = self.meat_analyzer.filter_valid_on_date(all_products, target_date)
        
        return valid_products
    
    def format_shopping_list(self, shopping_lists: Dict[str, List[Product]], 
                            format_type: str = "text") -> str:
        """
        Formátuje nákupní seznam do požadovaného formátu.
        
        Args:
            shopping_lists: Slovník obchod -> produkty
            format_type: Typ formátu ('text', 'markdown')
            
        Returns:
            Formátovaný nákupní seznam
        """
        if format_type == "markdown":
            return self._format_as_markdown(shopping_lists)
        else:
            return self._format_as_text(shopping_lists)
    
    def _format_as_text(self, shopping_lists: Dict[str, List[Product]]) -> str:
        """Formátuje jako prostý text."""
        lines = []
        lines.append("=" * 80)
        lines.append("DOPORUČENÝ TÝDENNÍ NÁKUPNÍ SEZNAM PRO KETO DIETU")
        lines.append(f"Lokace: {self.location}")
        lines.append(f"Vygenerováno: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        lines.append("=" * 80)
        lines.append("")
        
        for store, products in shopping_lists.items():
            lines.append(f"\n{'='*80}")
            lines.append(f"{store.upper()}")
            lines.append(f"{'='*80}")
            
            if not products:
                lines.append("  Žádné doporučené produkty")
                continue
            
            # Rozdělení podle kategorií
            categorized = self._categorize_products(products)
            
            total_cost = 0.0
            for category, items in categorized.items():
                if not items:
                    continue
                
                lines.append(f"\n{category}:")
                lines.append("-" * 80)
                
                for i, product in enumerate(items, 1):
                    discount_info = ""
                    if product.discount_percentage:
                        discount_info = f" (sleva {product.discount_percentage:.0f}%)"
                    
                    lines.append(f"  ☑ {product.name}")
                    lines.append(f"     {product.discount_price:.2f} Kč{discount_info}")
                    total_cost += product.discount_price
            
            lines.append(f"\n{'─'*80}")
            lines.append(f"Odhadované náklady pro {store.upper()}: {total_cost:.2f} Kč")
        
        # Celkový souhrn
        total_all_stores = sum(
            sum(p.discount_price for p in products) 
            for products in shopping_lists.values()
        )
        
        lines.append(f"\n{'='*80}")
        lines.append(f"CELKOVÉ ODHADOVANÉ NÁKLADY: {total_all_stores:.2f} Kč")
        lines.append(f"{'='*80}")
        
        lines.append("\n💡 TIPY:")
        lines.append("  • Porovnejte ceny mezi obchody před nákupem")
        lines.append("  • Kontrolujte datum platnosti akcí")
        lines.append("  • Ověřte nutriční hodnoty na obalech produktů")
        lines.append("  • Preferujte čerstvé maso před zmrazeným")
        
        return "\n".join(lines)
    
    def _format_as_markdown(self, shopping_lists: Dict[str, List[Product]]) -> str:
        """Formátuje jako Markdown."""
        lines = []
        lines.append("# Doporučený týdenní nákupní seznam pro keto dietu\n")
        lines.append(f"**Lokace:** {self.location}  ")
        lines.append(f"**Vygenerováno:** {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
        lines.append("---\n")
        
        for store, products in shopping_lists.items():
            lines.append(f"## {store.upper()}\n")
            
            if not products:
                lines.append("*Žádné doporučené produkty*\n")
                continue
            
            categorized = self._categorize_products(products)
            total_cost = 0.0
            
            for category, items in categorized.items():
                if not items:
                    continue
                
                lines.append(f"### {category}\n")
                
                for product in items:
                    discount_info = ""
                    if product.discount_percentage:
                        discount_info = f" *(sleva {product.discount_percentage:.0f}%)*"
                    
                    lines.append(f"- [ ] **{product.name}**  ")
                    lines.append(f"  {product.discount_price:.2f} Kč{discount_info}\n")
                    total_cost += product.discount_price
            
            lines.append(f"**Odhadované náklady:** {total_cost:.2f} Kč\n")
            lines.append("---\n")
        
        # Celkový souhrn
        total_all_stores = sum(
            sum(p.discount_price for p in products) 
            for products in shopping_lists.values()
        )
        
        lines.append(f"\n## Celkové odhadované náklady: {total_all_stores:.2f} Kč\n")
        
        lines.append("\n## 💡 Tipy\n")
        lines.append("- Porovnejte ceny mezi obchody před nákupem\n")
        lines.append("- Kontrolujte datum platnosti akcí\n")
        lines.append("- Ověřte nutriční hodnoty na obalech produktů\n")
        lines.append("- Preferujte čerstvé maso před zmrazeným\n")
        
        return "".join(lines)
    
    def _categorize_products(self, products: List[Product]) -> Dict[str, List[Product]]:
        """
        Kategorizuje produkty podle typu.
        
        Args:
            products: Seznam produktů
            
        Returns:
            Slovník kategorie -> produkty
        """
        categories = {
            'Maso a drůbež': [],
            'Mléčné výrobky': [],
            'Vejce': [],
            'Zelenina': [],
            'Ostatní': []
        }
        
        for product in products:
            name_lower = product.name.lower()
            
            if any(meat in name_lower for meat in ['kuřecí', 'krůtí', 'vepřové', 'hovězí', 'maso']):
                categories['Maso a drůbež'].append(product)
            elif any(dairy in name_lower for dairy in ['sýr', 'tvaroh', 'jogurt', 'máslo', 'smetana']):
                categories['Mléčné výrobky'].append(product)
            elif 'vejce' in name_lower or 'vajíčk' in name_lower:
                categories['Vejce'].append(product)
            elif any(veg in name_lower for veg in ['zelenina', 'salát', 'brokolice', 'špenát', 'paprika']):
                categories['Zelenina'].append(product)
            else:
                categories['Ostatní'].append(product)
        
        return categories
    
    def export_to_file(self, shopping_lists: Dict[str, List[Product]], 
                      filename: str, format_type: str = "text"):
        """
        Exportuje nákupní seznam do souboru.
        
        Args:
            shopping_lists: Slovník obchod -> produkty
            filename: Název souboru
            format_type: Typ formátu ('text', 'markdown')
        """
        content = self.format_shopping_list(shopping_lists, format_type)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ Nákupní seznam exportován do: {filename}")
    
    def close(self):
        """Zavře resources."""
        self.scraper.close()
        self.meat_analyzer.close()
    
    def __enter__(self):
        """Context manager vstup."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager výstup."""
        self.close()


def main():
    """Příklad použití ShoppingListGenerator."""
    print("🛒 Foodler - Generátor nákupního seznamu pro keto dietu")
    print("=" * 80)
    
    # Nastavení
    target_date = datetime(2026, 1, 18)  # 18.1.2026
    stores = ['kaufland', 'tesco', 'albert', 'billa']
    location = "Valašské Meziříčí"
    
    print(f"Lokace: {location}")
    print(f"Datum platnosti: {target_date.strftime('%d.%m.%Y')}")
    print(f"Obchody: {', '.join(store.upper() for store in stores)}")
    print()
    
    try:
        with ShoppingListGenerator(location=location) as generator:
            # Vygenerovat týdenní seznam
            print("Generování týdenního nákupního seznamu...")
            shopping_lists = generator.generate_weekly_list(
                stores=stores,
                target_date=target_date,
                family_size=3
            )
            
            # Zobrazit seznam
            print("\n" + "=" * 80)
            list_text = generator.format_shopping_list(shopping_lists, format_type="text")
            print(list_text)
            
            # Exportovat do souboru
            output_dir = "/home/runner/work/Foodler/Foodler/nakup"
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            
            # Text format
            text_file = os.path.join(output_dir, f"nakupni_seznam_{timestamp}.txt")
            generator.export_to_file(shopping_lists, text_file, format_type="text")
            
            # Markdown format
            md_file = os.path.join(output_dir, f"nakupni_seznam_{timestamp}.md")
            generator.export_to_file(shopping_lists, md_file, format_type="markdown")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Přerušeno uživatelem")
    except Exception as e:
        print(f"\n❌ Chyba: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
