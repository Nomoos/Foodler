#!/usr/bin/env python3
"""
Unit tests for the Kupi.cz scraper module.

This demonstrates the expected functionality with mock data.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
import os

# Přidání cesty pro import modulů
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers.kupi_scraper import KupiCzScraper
from modely.product import Product


class TestKupiCzScraper(unittest.TestCase):
    """Test cases for KupiCzScraper."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = KupiCzScraper()
    
    def tearDown(self):
        """Clean up after tests."""
        self.scraper.close()
    
    def test_scraper_initialization(self):
        """Test that scraper initializes correctly."""
        self.assertEqual(self.scraper.BASE_URL, "https://www.kupi.cz")
        self.assertEqual(self.scraper.timeout, 30)
        self.assertIn('User-Agent', self.scraper.session.headers)
    
    def test_scraper_custom_timeout(self):
        """Test scraper with custom timeout."""
        scraper = KupiCzScraper(timeout=60)
        self.assertEqual(scraper.timeout, 60)
        scraper.close()
    
    def test_parse_price(self):
        """Test price parsing from Czech format."""
        test_cases = [
            ("49,90 Kč", 49.90),
            ("99,- Kč", 99.0),
            ("125.50", 125.50),
            ("1 299,99 Kč", 1299.99),
        ]
        
        for price_text, expected in test_cases:
            result = self.scraper._parse_price(price_text)
            self.assertEqual(result, expected, f"Failed to parse: {price_text}")
    
    def test_get_stores(self):
        """Test getting list of stores."""
        stores = self.scraper.get_stores()
        self.assertIsInstance(stores, list)
        self.assertGreater(len(stores), 0)
        
        # Check store structure
        first_store = stores[0]
        self.assertIn('name', first_store)
        self.assertIn('id', first_store)
        
        # Check for expected stores
        store_names = [s['name'] for s in stores]
        self.assertIn('Lidl', store_names)
        self.assertIn('Kaufland', store_names)
    
    def test_context_manager(self):
        """Test using scraper as context manager."""
        with KupiCzScraper() as scraper:
            self.assertIsNotNone(scraper)
            stores = scraper.get_stores()
            self.assertIsInstance(stores, list)
    
    def test_product_dataclass(self):
        """Test Product dataclass."""
        product = Product(
            name="Kuřecí prsa",
            original_price=150.0,
            discount_price=99.90,
            discount_percentage=33.4,
            store="Lidl",
            valid_from=None,
            valid_until=None,
            image_url="https://example.com/image.jpg",
            product_url="https://example.com/product",
            category="Maso"
        )
        
        self.assertEqual(product.name, "Kuřecí prsa")
        self.assertEqual(product.discount_price, 99.90)
        self.assertEqual(product.store, "Lidl")
        
        # Test string representation
        product_str = str(product)
        self.assertIn("Kuřecí prsa", product_str)
        self.assertIn("99.9", product_str)
        self.assertIn("Lidl", product_str)
    
    @patch('src.scrapers.kupi_scraper.requests.Session.get')
    def test_fetch_page_success(self, mock_get):
        """Test successful page fetch."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body>Test</body></html>"
        mock_get.return_value = mock_response
        
        soup = self.scraper.fetch_page("https://test.com")
        self.assertIsNotNone(soup)
        self.assertEqual(soup.body.text, "Test")
    
    @patch('src.scrapers.kupi_scraper.requests.Session.get')
    def test_fetch_page_failure(self, mock_get):
        """Test handling of failed page fetch."""
        # Mock failed response - need to mock raise_for_status as well
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        soup = self.scraper.fetch_page("https://test.com")
        self.assertIsNone(soup)
    
    @patch('src.scrapers.kupi_scraper.KupiCzScraper.fetch_page')
    def test_get_current_discounts_with_filters(self, mock_fetch):
        """Test getting discounts with filters."""
        # Mock response
        mock_soup = Mock()
        mock_fetch.return_value = mock_soup
        
        # Mock _parse_products to return sample data
        sample_products = [
            Product(
                name="Test Product",
                original_price=100.0,
                discount_price=75.0,
                discount_percentage=25.0,
                store="Lidl",
                valid_from=None,
                valid_until=None,
                image_url=None,
                product_url=None,
                category=None
            )
        ]
        
        with patch.object(self.scraper, 'fetch_page', return_value=Mock()):
            with patch.object(self.scraper, '_parse_products', return_value=sample_products):
                # Test with category
                products = self.scraper.get_current_discounts(category='potraviny')
                self.assertEqual(len(products), 1)
                
                # Test with store
                products = self.scraper.get_current_discounts(store='lidl')
                self.assertEqual(len(products), 1)
                
                # Test with both
                products = self.scraper.get_current_discounts(category='potraviny', store='lidl')
                self.assertEqual(len(products), 1)


class TestIntegration(unittest.TestCase):
    """Integration tests with mock data."""
    
    def test_keto_product_filtering(self):
        """Test filtering for keto-friendly products."""
        # Sample products
        products = [
            Product("Kuřecí prsa", 150.0, 99.0, 34.0, "Lidl", None, None, None, None, "Maso"),
            Product("Sýr Eidam", 80.0, 59.0, 26.3, "Kaufland", None, None, None, None, "Mléčné"),
            Product("Bageta", 25.0, 15.0, 40.0, "Albert", None, None, None, None, "Pečivo"),
            Product("Avokádo", 45.0, 29.0, 35.6, "Penny", None, None, None, None, "Ovoce"),
        ]
        
        # Filter keto-friendly (assume low-carb categories)
        keto_categories = ["Maso", "Mléčné", "Ovoce"]
        keto_products = [p for p in products if p.category in keto_categories]
        
        self.assertEqual(len(keto_products), 3)
        self.assertNotIn("Bageta", [p.name for p in keto_products])
    
    def test_best_deals_sorting(self):
        """Test sorting products by discount percentage."""
        products = [
            Product("Product A", 100.0, 80.0, 20.0, "Lidl", None, None, None, None, None),
            Product("Product B", 100.0, 50.0, 50.0, "Kaufland", None, None, None, None, None),
            Product("Product C", 100.0, 70.0, 30.0, "Albert", None, None, None, None, None),
        ]
        
        # Sort by discount percentage
        sorted_products = sorted(products, key=lambda p: p.discount_percentage or 0, reverse=True)
        
        self.assertEqual(sorted_products[0].name, "Product B")
        self.assertEqual(sorted_products[0].discount_percentage, 50.0)
        self.assertEqual(sorted_products[2].name, "Product A")


def run_tests():
    """Run all tests."""
    print("=" * 70)
    print("Running Kupi.cz Scraper Tests")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestKupiCzScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
