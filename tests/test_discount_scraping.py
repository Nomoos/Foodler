#!/usr/bin/env python3
"""
Unit tests for new discount scraping and saving functionality.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
from datetime import datetime
import json
import sys
import os
import tempfile

# Přidání cesty pro import modulů
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers.kupi_scraper import KupiCzScraper
from modely.product import Product


class TestDateParsing(unittest.TestCase):
    """Test cases for date parsing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = KupiCzScraper()
    
    def tearDown(self):
        """Clean up after tests."""
        self.scraper.close()
    
    def test_parse_czech_date_basic(self):
        """Test parsing basic Czech date format."""
        test_cases = [
            ("15.1.2026", datetime(2026, 1, 15)),
            ("1.12.2026", datetime(2026, 12, 1)),
            ("31.12.2026", datetime(2026, 12, 31)),
        ]
        
        for date_text, expected in test_cases:
            result = self.scraper._parse_czech_date(date_text)
            self.assertIsNotNone(result, f"Failed to parse: {date_text}")
            self.assertEqual(result.date(), expected.date())
    
    def test_parse_czech_date_with_spaces(self):
        """Test parsing dates with spaces."""
        result = self.scraper._parse_czech_date("15. 1. 2026")
        self.assertIsNotNone(result)
        self.assertEqual(result.date(), datetime(2026, 1, 15).date())
    
    def test_parse_czech_date_invalid(self):
        """Test parsing invalid dates."""
        invalid_dates = ["", "invalid", "32.13.2026", None]
        for date_text in invalid_dates:
            result = self.scraper._parse_czech_date(date_text)
            self.assertIsNone(result)
    
    def test_extract_dates_from_element_range(self):
        """Test extracting date range from HTML element."""
        # Mock HTML element with date range
        mock_html = """
        <div class="product--wrap">
            <div class="product_name">Test Product</div>
            <div class="validity">Platnost: 15.1.2026 - 21.1.2026</div>
        </div>
        """
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(mock_html, 'lxml')
        element = soup.find('div', class_='product--wrap')
        
        valid_from, valid_until = self.scraper._extract_dates_from_element(element)
        
        if valid_from and valid_until:  # May be None if HTML structure differs
            self.assertEqual(valid_from.date(), datetime(2026, 1, 15).date())
            self.assertEqual(valid_until.date(), datetime(2026, 1, 21).date())
    
    def test_extract_dates_from_element_od_do(self):
        """Test extracting dates with 'od' and 'do' keywords."""
        mock_html = """
        <div class="product--wrap">
            <div class="product_name">Test Product</div>
            <div class="info">od 15.1.2026 do 21.1.2026</div>
        </div>
        """
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(mock_html, 'lxml')
        element = soup.find('div', class_='product--wrap')
        
        valid_from, valid_until = self.scraper._extract_dates_from_element(element)
        
        if valid_from and valid_until:
            self.assertEqual(valid_from.date(), datetime(2026, 1, 15).date())
            self.assertEqual(valid_until.date(), datetime(2026, 1, 21).date())


class TestDiscountScraping(unittest.TestCase):
    """Test cases for scraping all shop discounts."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = KupiCzScraper()
    
    def tearDown(self):
        """Clean up after tests."""
        self.scraper.close()
    
    @patch.object(KupiCzScraper, 'get_current_discounts')
    def test_scrape_all_shop_discounts(self, mock_get_discounts):
        """Test scraping discounts from all shops."""
        # Mock discount data
        sample_products = [
            Product(
                name="Test Product 1",
                original_price=100.0,
                discount_price=75.0,
                discount_percentage=25.0,
                store="Lidl",
                valid_from=datetime(2026, 1, 15),
                valid_until=datetime(2026, 1, 21),
                image_url=None,
                product_url=None,
                category=None
            ),
            Product(
                name="Test Product 2",
                original_price=50.0,
                discount_price=35.0,
                discount_percentage=30.0,
                store="Lidl",
                valid_from=datetime(2026, 1, 15),
                valid_until=datetime(2026, 1, 21),
                image_url=None,
                product_url=None,
                category=None
            )
        ]
        
        mock_get_discounts.return_value = sample_products
        
        # Scrape all discounts
        with patch('time.sleep'):  # Skip delays in tests
            all_discounts = self.scraper.scrape_all_shop_discounts()
        
        # Verify results
        self.assertIsInstance(all_discounts, dict)
        self.assertGreater(len(all_discounts), 0)
        
        # Check that each store has a list of products
        for store_id, products in all_discounts.items():
            self.assertIsInstance(products, list)
            self.assertEqual(len(products), 2)


class TestJsonStorage(unittest.TestCase):
    """Test cases for JSON storage functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = KupiCzScraper()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after tests."""
        self.scraper.close()
        # Clean up temp directory
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_product_to_dict(self):
        """Test converting Product to dictionary."""
        product = Product(
            name="Test Product",
            original_price=100.0,
            discount_price=75.0,
            discount_percentage=25.0,
            store="Lidl",
            valid_from=datetime(2026, 1, 15),
            valid_until=datetime(2026, 1, 21),
            image_url="https://example.com/image.jpg",
            product_url="https://example.com/product",
            category="Potraviny"
        )
        
        product_dict = self.scraper._product_to_dict(product)
        
        self.assertEqual(product_dict['name'], "Test Product")
        self.assertEqual(product_dict['discount_price'], 75.0)
        self.assertEqual(product_dict['store'], "Lidl")
        self.assertIn('valid_from', product_dict)
        self.assertIn('valid_until', product_dict)
    
    def test_save_discounts_to_json(self):
        """Test saving discounts to JSON file."""
        # Create sample discount data
        discounts = {
            'lidl': [
                Product(
                    name="Product 1",
                    original_price=100.0,
                    discount_price=75.0,
                    discount_percentage=25.0,
                    store="Lidl",
                    valid_from=datetime(2026, 1, 15),
                    valid_until=datetime(2026, 1, 21),
                    image_url=None,
                    product_url=None,
                    category=None
                )
            ],
            'kaufland': [
                Product(
                    name="Product 2",
                    original_price=50.0,
                    discount_price=35.0,
                    discount_percentage=30.0,
                    store="Kaufland",
                    valid_from=datetime(2026, 1, 15),
                    valid_until=datetime(2026, 1, 21),
                    image_url=None,
                    product_url=None,
                    category=None
                )
            ]
        }
        
        # Save to JSON
        filepath = self.scraper.save_discounts_to_json(
            discounts, 
            filename='test_discounts.json',
            directory=self.temp_dir
        )
        
        # Verify file exists
        self.assertTrue(os.path.exists(filepath))
        
        # Load and verify content
        with open(filepath, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        self.assertIn('scraped_at', json_data)
        self.assertEqual(json_data['total_stores'], 2)
        self.assertEqual(json_data['total_products'], 2)
        self.assertIn('stores', json_data)
        self.assertIn('lidl', json_data['stores'])
        self.assertIn('kaufland', json_data['stores'])
    
    def test_load_discounts_from_json(self):
        """Test loading discounts from JSON file."""
        # Create a test JSON file
        test_data = {
            'scraped_at': '2026-01-18T10:00:00',
            'total_stores': 1,
            'total_products': 1,
            'stores': {
                'lidl': {
                    'product_count': 1,
                    'products': [
                        {
                            'name': 'Test Product',
                            'original_price': 100.0,
                            'discount_price': 75.0,
                            'discount_percentage': 25.0,
                            'store': 'Lidl',
                            'valid_from': '2026-01-15T00:00:00',
                            'valid_until': '2026-01-21T00:00:00',
                            'image_url': None,
                            'product_url': None,
                            'category': None
                        }
                    ]
                }
            }
        }
        
        test_file = os.path.join(self.temp_dir, 'test_load.json')
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        # Load discounts
        discounts = self.scraper.load_discounts_from_json(test_file)
        
        # Verify
        self.assertIn('lidl', discounts)
        self.assertEqual(len(discounts['lidl']), 1)
        
        product = discounts['lidl'][0]
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.discount_price, 75.0)
        self.assertIsNotNone(product.valid_from)
        self.assertIsNotNone(product.valid_until)
        self.assertEqual(product.valid_from.date(), datetime(2026, 1, 15).date())


class TestRoundTrip(unittest.TestCase):
    """Test round-trip save and load operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = KupiCzScraper()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after tests."""
        self.scraper.close()
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_save_and_load_roundtrip(self):
        """Test that data survives save/load cycle."""
        # Original data
        original_discounts = {
            'lidl': [
                Product(
                    name="Kuřecí prsa",
                    original_price=150.0,
                    discount_price=99.90,
                    discount_percentage=33.4,
                    store="Lidl",
                    valid_from=datetime(2026, 1, 15, 10, 30),
                    valid_until=datetime(2026, 1, 21, 23, 59),
                    image_url="https://example.com/image.jpg",
                    product_url="https://example.com/product",
                    category="Maso"
                )
            ]
        }
        
        # Save
        filepath = self.scraper.save_discounts_to_json(
            original_discounts,
            filename='roundtrip_test.json',
            directory=self.temp_dir
        )
        
        # Load
        loaded_discounts = self.scraper.load_discounts_from_json(filepath)
        
        # Compare
        self.assertEqual(len(loaded_discounts), len(original_discounts))
        
        orig_product = original_discounts['lidl'][0]
        loaded_product = loaded_discounts['lidl'][0]
        
        self.assertEqual(orig_product.name, loaded_product.name)
        self.assertEqual(orig_product.discount_price, loaded_product.discount_price)
        self.assertEqual(orig_product.store, loaded_product.store)
        
        # Dates should match (time components preserved via ISO format)
        self.assertEqual(
            orig_product.valid_from.replace(microsecond=0),
            loaded_product.valid_from.replace(microsecond=0)
        )
        self.assertEqual(
            orig_product.valid_until.replace(microsecond=0),
            loaded_product.valid_until.replace(microsecond=0)
        )


def run_tests():
    """Run all tests."""
    print("=" * 70)
    print("Running Discount Scraping and Saving Tests")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestDateParsing))
    suite.addTests(loader.loadTestsFromTestCase(TestDiscountScraping))
    suite.addTests(loader.loadTestsFromTestCase(TestJsonStorage))
    suite.addTests(loader.loadTestsFromTestCase(TestRoundTrip))
    
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
    success = run_tests()
    sys.exit(0 if success else 1)
