"""
Kupi.cz Scraper Module

This module provides functionality to connect to https://www.kupi.cz/
and fetch current discounts and products from Czech supermarkets.

Kupi.cz is a Czech discount aggregator that collects promotional offers
from various supermarkets, making it easier to find deals on groceries.
"""

import requests
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Product:
    """Represents a product with discount information."""
    name: str
    original_price: Optional[float]
    discount_price: float
    discount_percentage: Optional[float]
    store: str
    valid_from: Optional[datetime]
    valid_until: Optional[datetime]
    image_url: Optional[str]
    product_url: Optional[str]
    category: Optional[str]
    
    def __str__(self):
        discount_info = f"{self.discount_percentage}% off" if self.discount_percentage else "Discount"
        return f"{self.name} - {self.discount_price} Kč ({discount_info}) at {self.store}"


class KupiCzScraper:
    """Scraper for kupi.cz website to fetch discounts and products."""
    
    BASE_URL = "https://www.kupi.cz"
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the scraper.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        # Set realistic headers to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'cs-CZ,cs;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a page from kupi.cz.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if request fails
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def get_current_discounts(self, category: Optional[str] = None, store: Optional[str] = None) -> List[Product]:
        """
        Fetch current discounts from kupi.cz.
        
        Args:
            category: Optional category filter (e.g., 'potraviny', 'napoje')
            store: Optional store filter (e.g., 'lidl', 'kaufland', 'albert')
            
        Returns:
            List of Product objects with discount information
        """
        products = []
        
        # Build URL with filters
        url = self.BASE_URL
        params = {}
        
        if category:
            url += f"/{category}"
        if store:
            params['store'] = store
        
        if params:
            url += f"?{urlencode(params)}"
        
        soup = self.fetch_page(url)
        if not soup:
            logger.warning("Failed to fetch main page")
            return products
        
        # Parse products from the page
        # Note: This is a template structure. Actual parsing logic would need
        # to be adjusted based on the real HTML structure of kupi.cz
        try:
            products = self._parse_products(soup)
            logger.info(f"Found {len(products)} products")
        except Exception as e:
            logger.error(f"Error parsing products: {e}")
        
        return products
    
    def _parse_products(self, soup: BeautifulSoup) -> List[Product]:
        """
        Parse product information from BeautifulSoup object.
        
        Args:
            soup: BeautifulSoup object containing the page HTML
            
        Returns:
            List of Product objects
        """
        products = []
        
        # This is a template structure that needs to be adjusted
        # based on actual kupi.cz HTML structure
        
        # Common patterns to look for:
        # - Product cards/tiles (often div with class like 'product', 'offer', 'item')
        # - Price information (usually in span/div with class like 'price', 'discount-price')
        # - Store name (often in a badge or tag)
        # - Product images and links
        
        # Example parsing logic (needs adjustment based on real site):
        product_elements = soup.find_all('div', class_='product-item')  # Placeholder selector
        
        for elem in product_elements:
            try:
                product = self._extract_product_info(elem)
                if product:
                    products.append(product)
            except Exception as e:
                logger.debug(f"Error parsing product element: {e}")
                continue
        
        return products
    
    def _extract_product_info(self, element) -> Optional[Product]:
        """
        Extract product information from a HTML element.
        
        Args:
            element: BeautifulSoup element containing product info
            
        Returns:
            Product object or None
        """
        # This is a template that needs to be customized based on
        # the actual HTML structure of kupi.cz
        
        try:
            # Example extraction (placeholders):
            name = element.find('h3', class_='product-name')
            name = name.get_text(strip=True) if name else "Unknown"
            
            price_elem = element.find('span', class_='price')
            discount_price = 0.0
            if price_elem:
                # Extract numeric price from text like "49,90 Kč"
                price_text = price_elem.get_text(strip=True)
                discount_price = self._parse_price(price_text)
            
            original_price_elem = element.find('span', class_='original-price')
            original_price = None
            if original_price_elem:
                original_price = self._parse_price(original_price_elem.get_text(strip=True))
            
            discount_percentage = None
            if original_price and discount_price:
                discount_percentage = round(((original_price - discount_price) / original_price) * 100, 1)
            
            store_elem = element.find('span', class_='store-name')
            store = store_elem.get_text(strip=True) if store_elem else "Unknown"
            
            img_elem = element.find('img')
            image_url = img_elem.get('src') if img_elem else None
            
            link_elem = element.find('a')
            product_url = link_elem.get('href') if link_elem else None
            if product_url and not product_url.startswith('http'):
                product_url = self.BASE_URL + product_url
            
            return Product(
                name=name,
                original_price=original_price,
                discount_price=discount_price,
                discount_percentage=discount_percentage,
                store=store,
                valid_from=None,  # Would need to parse from page
                valid_until=None,  # Would need to parse from page
                image_url=image_url,
                product_url=product_url,
                category=None  # Would need to parse from page
            )
        except Exception as e:
            logger.debug(f"Error extracting product info: {e}")
            return None
    
    def _parse_price(self, price_text: str) -> float:
        """
        Parse price from Czech format string.
        
        Args:
            price_text: Price string like "49,90 Kč" or "49.90"
            
        Returns:
            Float price value
        """
        # Remove currency symbols and extra spaces
        price_text = price_text.replace('Kč', '').replace(',-', '').strip()
        # Replace Czech decimal separator
        price_text = price_text.replace(',', '.')
        # Remove thousands separators
        price_text = price_text.replace(' ', '')
        
        try:
            return float(price_text)
        except ValueError:
            logger.warning(f"Could not parse price: {price_text}")
            return 0.0
    
    def search_products(self, query: str) -> List[Product]:
        """
        Search for products by name or keyword.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching Product objects
        """
        # Build search URL with proper URL encoding
        params = {'q': query}
        search_url = f"{self.BASE_URL}/vyhledavani?{urlencode(params)}"
        
        soup = self.fetch_page(search_url)
        if not soup:
            return []
        
        return self._parse_products(soup)
    
    def get_stores(self) -> List[Dict[str, str]]:
        """
        Get list of available stores on kupi.cz.
        
        Returns:
            List of store dictionaries with name and identifier
        """
        stores = [
            {'name': 'Lidl', 'id': 'lidl'},
            {'name': 'Kaufland', 'id': 'kaufland'},
            {'name': 'Albert', 'id': 'albert'},
            {'name': 'Penny', 'id': 'penny'},
            {'name': 'Billa', 'id': 'billa'},
            {'name': 'Tesco', 'id': 'tesco'},
            {'name': 'Globus', 'id': 'globus'},
            {'name': 'Makro', 'id': 'makro'},
        ]
        return stores
    
    def close(self):
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def main():
    """Example usage of the KupiCzScraper."""
    print("Kupi.cz Scraper - Fetching current discounts\n")
    print("=" * 60)
    
    with KupiCzScraper() as scraper:
        # Get list of stores
        print("\nAvailable stores:")
        stores = scraper.get_stores()
        for store in stores:
            print(f"  - {store['name']} ({store['id']})")
        
        # Fetch current discounts
        print("\nFetching current discounts...")
        products = scraper.get_current_discounts()
        
        if products:
            print(f"\nFound {len(products)} products on sale:\n")
            for i, product in enumerate(products[:10], 1):  # Show first 10
                print(f"{i}. {product}")
        else:
            print("\nNo products found. This could be due to:")
            print("  - Network connectivity issues")
            print("  - Website structure changes requiring parser updates")
            print("  - Anti-scraping measures by the website")
            print("\nThe scraper structure is in place and ready to be customized")
            print("based on the actual HTML structure of kupi.cz")
        
        # Example search
        print("\n" + "=" * 60)
        print("Example: Searching for 'mléko' (milk)...")
        search_results = scraper.search_products("mléko")
        if search_results:
            print(f"Found {len(search_results)} results")
            for product in search_results[:3]:
                print(f"  - {product}")


if __name__ == "__main__":
    main()
