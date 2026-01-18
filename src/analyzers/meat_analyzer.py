#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyzátor masných produktů pro keto dietu
Analyzuje produkty z kupi.cz a ověřuje je pomocí nutričních databází
"""

import sys
import os
from typing import List, Dict, Optional
from datetime import datetime
import logging

# Přidání rodičovské složky do cesty pro importy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.scrapers.kupi_scraper import KupiCzScraper
from modely.product import Product
from fetch_nutrition_data import fetch_by_product_name, search_product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MeatAnalyzer:
    """Analyzátor masných produktů pro keto dietu."""
    
    # Keto-vhodné kategorie masa
    KETO_MEAT_KEYWORDS = [
        'kuřecí prsa', 'kuřecí stehna', 'kuřecí',
        'krůtí prsa', 'krůtí', 
        'vepřové', 'vepřová kotleta', 'vepřová krkovice',
        'hovězí', 'hovězí maso',
        'telecí',
        'jehněčí',
        'kachna', 'husa'
    ]
    
    # Minimální požadavky na bílkoviny (g na 100g)
    MIN_PROTEIN_PER_100G = 15.0
    
    # Maximální sacharidy pro keto (g na 100g)
    MAX_CARBS_PER_100G = 5.0
    
    def __init__(self, location: str = "Valašské Meziříčí"):
        """
        Inicializace analyzátoru.
        
        Args:
            location: Lokace pro filtrování obchodů
        """
        self.location = location
        self.scraper = KupiCzScraper()
    
    def fetch_meat_products(self, store: Optional[str] = None, 
                           page: int = 1, sort_by_price: bool = True) -> List[Product]:
        """
        Stáhne masné produkty z kategorie drůbež.
        
        Args:
            store: Název obchodu (např. 'kaufland', 'albert', 'tesco', 'billa')
            page: Číslo stránky
            sort_by_price: Pokud True, řadí podle ceny za jednotku
            
        Returns:
            Seznam Product objektů
        """
        products = []
        
        # Stáhnout z kategorie drůbež (poultry)
        sort_order = 0 if sort_by_price else None
        
        logger.info(f"Fetching poultry products from {store or 'all stores'}, page {page}")
        poultry_products = self.scraper.get_current_discounts(
            category='drubez',
            store=store,
            sort_order=sort_order,
            page=page
        )
        products.extend(poultry_products)
        
        # Také vyhledat specifická klíčová slova pro širší pokrytí
        if not store:  # Pokud není specifikován obchod, hledat i obecně
            for keyword in ['vepřové', 'hovězí']:
                keyword_products = self.scraper.search_products(keyword)
                products.extend(keyword_products)
        
        logger.info(f"Found {len(products)} meat products")
        return products
    
    def verify_nutrition(self, product: Product) -> Optional[Dict]:
        """
        Ověří nutriční hodnoty produktu pomocí kaloricketabulky.cz.
        
        Args:
            product: Product objekt k ověření
            
        Returns:
            Slovník s nutričními informacemi nebo None
        """
        logger.info(f"Verifying nutrition for: {product.name}")
        
        try:
            # Pokusit se najít nutriční data podle názvu
            nutrition_data = fetch_by_product_name(product.name)
            
            if nutrition_data and nutrition_data.get('macros'):
                return nutrition_data
            
            # Pokud nenalezeno, zkusit jednodušší názvy
            simplified_names = self._simplify_product_name(product.name)
            for name in simplified_names:
                nutrition_data = fetch_by_product_name(name)
                if nutrition_data and nutrition_data.get('macros'):
                    logger.info(f"Found nutrition data using simplified name: {name}")
                    return nutrition_data
            
            logger.warning(f"No nutrition data found for: {product.name}")
            return None
            
        except Exception as e:
            logger.error(f"Error verifying nutrition: {e}")
            return None
    
    def _simplify_product_name(self, name: str) -> List[str]:
        """
        Vytvoří zjednodušené varianty názvu produktu pro lepší vyhledávání.
        
        Args:
            name: Původní název produktu
            
        Returns:
            Seznam zjednodušených názvů
        """
        simplified = []
        
        # Odstranit značky a váhy
        name_lower = name.lower()
        
        # Extrahovat typ masa
        meat_types = ['kuřecí', 'krůtí', 'vepřové', 'hovězí', 'telecí', 'jehněčí']
        cuts = ['prsa', 'prso', 'stehna', 'stehno', 'kotleta', 'krkovice', 'řízek', 'maso']
        
        for meat in meat_types:
            if meat in name_lower:
                # Přidat typ masa samostatně
                simplified.append(meat)
                
                # Přidat typ masa + část
                for cut in cuts:
                    if cut in name_lower:
                        simplified.append(f"{meat} {cut}")
        
        return simplified
    
    def score_product_for_keto(self, product: Product, nutrition_data: Optional[Dict] = None) -> float:
        """
        Ohodnotí produkt z hlediska vhodnosti pro keto dietu.
        
        Args:
            product: Product objekt
            nutrition_data: Volitelná nutriční data z databáze
            
        Returns:
            Skóre 0-100 (vyšší = vhodnější)
        """
        score = 50.0  # Základní skóre
        
        # Bonus za slevu
        if product.discount_percentage:
            score += min(product.discount_percentage * 0.3, 20)  # Max +20 bodů
        
        # Bonus za nízkou cenu
        if product.discount_price < 100:  # Méně než 100 Kč
            score += 10
        elif product.discount_price < 150:
            score += 5
        
        # Analýza podle nutričních dat
        if nutrition_data and nutrition_data.get('macros'):
            macros = nutrition_data['macros']
            
            # Extrahovat hodnoty (odstranit jednotky)
            try:
                protein_str = macros.get('protein', '0 g').replace('g', '').strip()
                carbs_str = macros.get('carbohydrates', '0 g').replace('g', '').strip()
                
                protein = float(protein_str.replace(',', '.'))
                carbs = float(carbs_str.replace(',', '.'))
                
                # Vysoký obsah bílkovin = bonus
                if protein >= self.MIN_PROTEIN_PER_100G:
                    score += min((protein - self.MIN_PROTEIN_PER_100G) * 2, 20)  # Max +20
                
                # Nízký obsah sacharidů = bonus
                if carbs <= self.MAX_CARBS_PER_100G:
                    score += 10
                else:
                    score -= (carbs - self.MAX_CARBS_PER_100G) * 2  # Penalizace za sacharidy
                
            except (ValueError, AttributeError) as e:
                logger.debug(f"Could not parse nutrition values: {e}")
        
        # Omezit skóre na rozsah 0-100
        return max(0, min(100, score))
    
    def filter_valid_on_date(self, products: List[Product], date: datetime) -> List[Product]:
        """
        Filtruje produkty platné k danému datu.
        
        Args:
            products: Seznam produktů
            date: Datum k ověření
            
        Returns:
            Seznam platných produktů
        """
        # Poznámka: Aktuálně kupi.cz nemusí vždy poskytnout přesná data platnosti
        # V budoucnu by se dalo vylepšit parsováním detailních stránek produktů
        valid_products = []
        
        for product in products:
            # Pokud nemáme informaci o platnosti, předpokládáme že je platný
            if product.valid_from is None and product.valid_until is None:
                valid_products.append(product)
            elif product.is_valid_on_date(date):
                valid_products.append(product)
        
        return valid_products
    
    def generate_report(self, products: List[Product], 
                       with_nutrition: bool = False) -> str:
        """
        Vygeneruje textový report o produktech.
        
        Args:
            products: Seznam produktů
            with_nutrition: Pokud True, ověří a zahrne nutriční data
            
        Returns:
            Formátovaný textový report
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("REPORT: MASNÉ PRODUKTY PRO KETO DIETU")
        report_lines.append(f"Lokace: {self.location}")
        report_lines.append(f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        if not products:
            report_lines.append("Žádné produkty nenalezeny.")
            return "\n".join(report_lines)
        
        # Seřadit produkty podle skóre
        scored_products = []
        for product in products:
            nutrition_data = None
            if with_nutrition:
                nutrition_data = self.verify_nutrition(product)
            
            score = self.score_product_for_keto(product, nutrition_data)
            scored_products.append((product, score, nutrition_data))
        
        scored_products.sort(key=lambda x: x[1], reverse=True)
        
        # Top 10 produktů
        report_lines.append(f"TOP 10 DOPORUČENÝCH PRODUKTŮ (celkem nalezeno: {len(products)})")
        report_lines.append("-" * 80)
        
        for i, (product, score, nutrition_data) in enumerate(scored_products[:10], 1):
            report_lines.append(f"\n{i}. {product.name}")
            report_lines.append(f"   Obchod: {product.store}")
            price_line = f"   Cena: {product.discount_price:.2f} Kč"
            if product.discount_percentage:
                price_line += f" (sleva {product.discount_percentage:.0f}%)"
            report_lines.append(price_line)
            report_lines.append(f"   Keto skóre: {score:.1f}/100")
            
            if nutrition_data and nutrition_data.get('macros'):
                macros = nutrition_data['macros']
                report_lines.append(f"   Nutriční hodnoty (na 100g):")
                if 'protein' in macros:
                    report_lines.append(f"     • Bílkoviny: {macros['protein']}")
                if 'carbohydrates' in macros:
                    report_lines.append(f"     • Sacharidy: {macros['carbohydrates']}")
                if 'fat' in macros:
                    report_lines.append(f"     • Tuky: {macros['fat']}")
                if 'calories' in macros:
                    report_lines.append(f"     • Energie: {macros['calories']}")
        
        report_lines.append("")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def close(self):
        """Zavře scraper."""
        self.scraper.close()
    
    def __enter__(self):
        """Context manager vstup."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager výstup."""
        self.close()


def main():
    """Příklad použití MeatAnalyzer."""
    print("🥩 Foodler - Analyzátor masných produktů pro keto dietu")
    print("=" * 80)
    
    target_date = datetime(2026, 1, 18)  # 18.1.2026
    print(f"Vyhledávání produktů platných k datu: {target_date.strftime('%d.%m.%Y')}")
    print(f"Lokace: Valašské Meziříčí")
    print()
    
    try:
        with MeatAnalyzer(location="Valašské Meziříčí") as analyzer:
            # Načíst produkty z různých obchodů
            stores = ['kaufland', 'albert', 'tesco', 'billa']
            all_products = []
            
            for store in stores:
                print(f"📍 Načítání produktů z {store.upper()}...")
                products = analyzer.fetch_meat_products(store=store, page=1)
                all_products.extend(products)
                print(f"   Nalezeno: {len(products)} produktů")
            
            # Filtrovat platné k datu
            valid_products = analyzer.filter_valid_on_date(all_products, target_date)
            print(f"\n✅ Celkem platných produktů: {len(valid_products)}")
            
            # Vygenerovat report (bez nutričního ověření pro rychlost)
            print("\n" + "=" * 80)
            print("Generování reportu...")
            print("=" * 80)
            report = analyzer.generate_report(valid_products[:20], with_nutrition=False)
            print(report)
            
            print("\n💡 TIP: Pro ověření nutričních hodnot použijte parametr --verify-nutrition")
            print("   To zabere více času, ale poskytne přesnější doporučení.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Přerušeno uživatelem")
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
        print(f"\n❌ Chyba: {e}")


if __name__ == "__main__":
    main()
