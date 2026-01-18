#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit testy pro novou funkcionalitu analyzátoru masa a generátoru nákupních seznamů
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
import os

# Add parent directory to path for test imports
# This is acceptable for test files to allow flexible test execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers.kupi_scraper import KupiCzScraper
from src.analyzers.meat_analyzer import MeatAnalyzer
from src.planners.shopping_list_generator import ShoppingListGenerator
from modely.product import Product


class TestEnhancedKupiScraper(unittest.TestCase):
    """Testy pro vylepšený Kupi.cz scraper."""
    
    def setUp(self):
        """Příprava testů."""
        self.scraper = KupiCzScraper()
    
    def tearDown(self):
        """Úklid po testech."""
        self.scraper.close()
    
    def test_enhanced_get_current_discounts(self):
        """Test vylepšené metody get_current_discounts s novými parametry."""
        # Test, že metoda přijímá nové parametry
        # Mock fetch_page aby neprováděla skutečné HTTP požadavky
        with patch.object(self.scraper, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = Mock()
            
            with patch.object(self.scraper, '_parse_products') as mock_parse:
                mock_parse.return_value = []
                
                # Test s category a store
                self.scraper.get_current_discounts(category='drubez', store='kaufland')
                
                # Test s sort_order
                self.scraper.get_current_discounts(store='kaufland', sort_order=0)
                
                # Test s page
                self.scraper.get_current_discounts(store='kaufland', page=2)
                
                # Ověř, že bylo voláno
                self.assertTrue(mock_fetch.called)
    
    def test_get_ajax_discounts(self):
        """Test AJAX endpointu."""
        with patch.object(self.scraper, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = Mock()
            
            with patch.object(self.scraper, '_parse_products') as mock_parse:
                mock_parse.return_value = []
                
                products = self.scraper.get_ajax_discounts('kaufland', page=5, sort_order=0)
                
                # Ověř, že byla sestavena správná URL
                call_args = mock_fetch.call_args[0][0]
                self.assertIn('/get-akce/kaufland', call_args)
                self.assertIn('page=5', call_args)
                self.assertIn('ord=0', call_args)
                self.assertIn('ajax=1', call_args)
    
    def test_parse_czech_date(self):
        """Test parsování českých datumů."""
        test_cases = [
            ("18.1.2026", datetime(2026, 1, 18)),
            ("18. 1. 2026", datetime(2026, 1, 18)),
            ("1.2.2026", datetime(2026, 2, 1)),
            ("18/1/2026", datetime(2026, 1, 18)),
        ]
        
        for date_str, expected in test_cases:
            result = self.scraper._parse_czech_date(date_str)
            self.assertIsNotNone(result, f"Failed to parse: {date_str}")
            self.assertEqual(result.date(), expected.date(), f"Wrong date for: {date_str}")
    
    def test_parse_czech_date_with_month_names(self):
        """Test parsování datumů s českými názvy měsíců."""
        test_cases = [
            ("18. ledna 2026", datetime(2026, 1, 18)),
            ("1. února 2026", datetime(2026, 2, 1)),
            ("15. března 2026", datetime(2026, 3, 15)),
        ]
        
        for date_str, expected in test_cases:
            result = self.scraper._parse_czech_date(date_str)
            self.assertIsNotNone(result, f"Failed to parse: {date_str}")
            self.assertEqual(result.date(), expected.date(), f"Wrong date for: {date_str}")


class TestProductModel(unittest.TestCase):
    """Testy pro vylepšený Product model."""
    
    def test_product_with_new_fields(self):
        """Test, že Product podporuje nová pole."""
        product = Product(
            name="Kuřecí prsa",
            original_price=150.0,
            discount_price=99.90,
            discount_percentage=33.4,
            store="Kaufland",
            valid_from=datetime(2026, 1, 15),
            valid_until=datetime(2026, 1, 20),
            image_url="https://example.com/image.jpg",
            product_url="https://example.com/product",
            category="Maso",
            barcode="1234567890123",
            location="Valašské Meziříčí",
            unit_price=199.80,
            unit="kg"
        )
        
        self.assertEqual(product.barcode, "1234567890123")
        self.assertEqual(product.location, "Valašské Meziříčí")
        self.assertEqual(product.unit_price, 199.80)
        self.assertEqual(product.unit, "kg")
    
    def test_is_valid_on_date(self):
        """Test metody is_valid_on_date."""
        product = Product(
            name="Test Product",
            original_price=100.0,
            discount_price=80.0,
            discount_percentage=20.0,
            store="Test Store",
            valid_from=datetime(2026, 1, 15),
            valid_until=datetime(2026, 1, 20),
            image_url=None,
            product_url=None,
            category=None
        )
        
        # Test platného data
        self.assertTrue(product.is_valid_on_date(datetime(2026, 1, 18)))
        
        # Test hraničních hodnot
        self.assertTrue(product.is_valid_on_date(datetime(2026, 1, 15)))
        self.assertTrue(product.is_valid_on_date(datetime(2026, 1, 20)))
        
        # Test mimo platnost
        self.assertFalse(product.is_valid_on_date(datetime(2026, 1, 14)))
        self.assertFalse(product.is_valid_on_date(datetime(2026, 1, 21)))
    
    def test_is_valid_on_date_no_dates_set(self):
        """Test is_valid_on_date když nejsou nastaveny datumy."""
        product = Product(
            name="Test Product",
            original_price=100.0,
            discount_price=80.0,
            discount_percentage=20.0,
            store="Test Store",
            valid_from=None,
            valid_until=None,
            image_url=None,
            product_url=None,
            category=None
        )
        
        # Bez nastavených datumů by měl být vždy platný
        self.assertTrue(product.is_valid_on_date(datetime(2026, 1, 18)))


class TestMeatAnalyzer(unittest.TestCase):
    """Testy pro MeatAnalyzer."""
    
    def setUp(self):
        """Příprava testů."""
        self.analyzer = MeatAnalyzer(location="Valašské Meziříčí")
    
    def tearDown(self):
        """Úklid po testech."""
        self.analyzer.close()
    
    def test_initialization(self):
        """Test inicializace analyzátoru."""
        self.assertEqual(self.analyzer.location, "Valašské Meziříčí")
        self.assertIsNotNone(self.analyzer.scraper)
    
    def test_simplify_product_name(self):
        """Test zjednodušení názvů produktů."""
        test_cases = [
            ("Kuřecí prsa 1kg", ['kuřecí']),
            ("Vepřové maso", ['vepřové']),
            ("Hovězí maso čerstvé", ['hovězí']),
        ]
        
        for product_name, expected_terms in test_cases:
            simplified = self.analyzer._simplify_product_name(product_name)
            # Ověř, že alespoň jeden očekávaný termín je ve výsledku
            has_match = any(term in simplified for term in expected_terms)
            self.assertTrue(has_match, f"No match for {product_name}, got: {simplified}")
    
    def test_score_product_for_keto(self):
        """Test skórování produktů pro keto dietu."""
        # Produkt se slevou
        product_with_discount = Product(
            name="Kuřecí prsa",
            original_price=150.0,
            discount_price=99.0,
            discount_percentage=34.0,
            store="Kaufland",
            valid_from=None,
            valid_until=None,
            image_url=None,
            product_url=None,
            category="Maso"
        )
        
        score = self.analyzer.score_product_for_keto(product_with_discount)
        
        # Skóre by mělo být mezi 0 a 100
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        
        # Se slevou by mělo být vyšší než základní skóre
        self.assertGreater(score, 50)
    
    def test_score_with_nutrition_data(self):
        """Test skórování s nutričními daty."""
        product = Product(
            name="Kuřecí prsa",
            original_price=150.0,
            discount_price=99.0,
            discount_percentage=34.0,
            store="Kaufland",
            valid_from=None,
            valid_until=None,
            image_url=None,
            product_url=None,
            category="Maso"
        )
        
        # Mock nutriční data - vysoké bílkoviny, nízké sacharidy (ideální pro keto)
        nutrition_data = {
            'macros': {
                'protein': '23 g',
                'carbohydrates': '0 g',
                'fat': '2 g',
                'calories': '110 kcal'
            }
        }
        
        score = self.analyzer.score_product_for_keto(product, nutrition_data)
        
        # S dobrými nutričními hodnotami by skóre mělo být vysoké
        self.assertGreater(score, 60)
    
    def test_filter_valid_on_date(self):
        """Test filtrace produktů podle data platnosti."""
        products = [
            Product("P1", 100, 80, 20, "Store1", 
                   datetime(2026, 1, 15), datetime(2026, 1, 20), None, None, None),
            Product("P2", 100, 80, 20, "Store2", 
                   datetime(2026, 1, 10), datetime(2026, 1, 17), None, None, None),
            Product("P3", 100, 80, 20, "Store3", 
                   None, None, None, None, None),  # Žádné datum = vždy platný
        ]
        
        target_date = datetime(2026, 1, 18)
        valid = self.analyzer.filter_valid_on_date(products, target_date)
        
        # P1 a P3 by měly být platné
        self.assertEqual(len(valid), 2)
        valid_names = [p.name for p in valid]
        self.assertIn("P1", valid_names)
        self.assertIn("P3", valid_names)
        self.assertNotIn("P2", valid_names)


class TestShoppingListGenerator(unittest.TestCase):
    """Testy pro ShoppingListGenerator."""
    
    def setUp(self):
        """Příprava testů."""
        self.generator = ShoppingListGenerator(location="Valašské Meziříčí")
    
    def tearDown(self):
        """Úklid po testech."""
        self.generator.close()
    
    def test_initialization(self):
        """Test inicializace generátoru."""
        self.assertEqual(self.generator.location, "Valašské Meziříčí")
        self.assertIsNotNone(self.generator.scraper)
        self.assertIsNotNone(self.generator.meat_analyzer)
    
    def test_categorize_products(self):
        """Test kategorizace produktů."""
        products = [
            Product("Kuřecí prsa", 100, 80, 20, "Store1", None, None, None, None, None),
            Product("Sýr Eidam", 60, 50, 17, "Store2", None, None, None, None, None),
            Product("Vejce čerstvá", 40, 35, 12, "Store3", None, None, None, None, None),
            Product("Avokádo", 30, 25, 17, "Store4", None, None, None, None, None),
        ]
        
        categorized = self.generator._categorize_products(products)
        
        # Ověř, že produkty jsou správně roztříděny
        self.assertEqual(len(categorized['Maso a drůbež']), 1)
        self.assertEqual(len(categorized['Mléčné výrobky']), 1)
        self.assertEqual(len(categorized['Vejce']), 1)
    
    def test_format_shopping_list_text(self):
        """Test formátování nákupního seznamu jako text."""
        shopping_lists = {
            'kaufland': [
                Product("Kuřecí prsa", 150, 99, 34, "Kaufland", None, None, None, None, None),
                Product("Sýr Eidam", 80, 65, 19, "Kaufland", None, None, None, None, None),
            ]
        }
        
        formatted = self.generator.format_shopping_list(shopping_lists, format_type="text")
        
        # Ověř, že výstup obsahuje klíčové informace
        self.assertIn("KAUFLAND", formatted)
        self.assertIn("Kuřecí prsa", formatted)
        self.assertIn("99", formatted)  # Cena
        self.assertIn("34", formatted)  # Sleva
    
    def test_format_shopping_list_markdown(self):
        """Test formátování nákupního seznamu jako Markdown."""
        shopping_lists = {
            'kaufland': [
                Product("Kuřecí prsa", 150, 99, 34, "Kaufland", None, None, None, None, None),
            ]
        }
        
        formatted = self.generator.format_shopping_list(shopping_lists, format_type="markdown")
        
        # Ověř, že výstup obsahuje Markdown syntaxi
        self.assertIn("##", formatted)  # Markdown nadpisy
        self.assertIn("- [ ]", formatted)  # Markdown checklist
        self.assertIn("Kuřecí prsa", formatted)


def run_tests():
    """Spustí všechny unit testy."""
    print("=" * 80)
    print("Spouštění unit testů pro novou funkcionalitu")
    print("=" * 80)
    print()
    
    # Vytvoř test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestEnhancedKupiScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestProductModel))
    suite.addTests(loader.loadTestsFromTestCase(TestMeatAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestShoppingListGenerator))
    
    # Spusť testy
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Souhrn
    print("\n" + "=" * 80)
    print("Souhrn testů")
    print("=" * 80)
    print(f"Celkem testů: {result.testsRun}")
    print(f"Úspěšných: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Selhání: {len(result.failures)}")
    print(f"Chyby: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
