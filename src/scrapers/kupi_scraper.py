"""
Scraper pro kupi.cz
Tento modul se zabývá pouze scrapováním dat z webu (Single Responsibility)
"""

import requests
from typing import List, Optional
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import logging

from modely.product import Product

# Konfigurace logování
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KupiCzScraper:
    """Scraper pro kupi.cz website."""
    
    BASE_URL = "https://www.kupi.cz"
    
    def __init__(self, timeout: int = 30):
        """
        Inicializace scraperu.
        
        Args:
            timeout: Časový limit požadavku v sekundách
        """
        self.timeout = timeout
        self.session = requests.Session()
        # Nastavení realistických hlaviček pro zabránění blokování
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
        Stáhne a zpracuje stránku z kupi.cz.
        
        Args:
            url: URL ke stažení
            
        Returns:
            BeautifulSoup objekt nebo None při chybě
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
        Stáhne aktuální slevy z kupi.cz.
        
        Args:
            category: Volitelný filtr kategorie (např. 'potraviny', 'napoje')
            store: Volitelný filtr obchodu (např. 'lidl', 'kaufland', 'albert')
            
        Returns:
            Seznam Product objektů s informacemi o slevách
        """
        products = []
        
        # Sestavení URL s filtry
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
        
        # Parsování produktů ze stránky
        try:
            products = self._parse_products(soup)
            logger.info(f"Found {len(products)} products")
        except Exception as e:
            logger.error(f"Error parsing products: {e}")
        
        return products
    
    def _parse_products(self, soup: BeautifulSoup) -> List[Product]:
        """
        Parsuje informace o produktech z BeautifulSoup objektu.
        
        Args:
            soup: BeautifulSoup objekt obsahující HTML stránky
            
        Returns:
            Seznam Product objektů
        """
        products = []
        
        # Toto je šablonová struktura, která musí být upravena
        # podle skutečné HTML struktury kupi.cz
        
        # Běžné vzory k hledání:
        # - Karty/dlaždice produktů (často div s třídou jako 'product', 'offer', 'item')
        # - Cenové informace (obvykle v span/div s třídou jako 'price', 'discount-price')
        # - Název obchodu (často v badge nebo tag)
        # - Obrázky a odkazy produktů
        
        # Příklad parsovací logiky (potřebuje úpravu podle reálného webu):
        product_elements = soup.find_all('div', class_='product-item')  # Zástupný selektor
        
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
        Extrahuje informace o produktu z HTML elementu.
        
        Args:
            element: BeautifulSoup element obsahující info o produktu
            
        Returns:
            Product objekt nebo None
        """
        # Toto je šablona, která musí být přizpůsobena podle
        # skutečné HTML struktury kupi.cz
        
        try:
            # Příklad extrakce (zástupné hodnoty):
            name = element.find('h3', class_='product-name')
            name = name.get_text(strip=True) if name else "Unknown"
            
            price_elem = element.find('span', class_='price')
            discount_price = 0.0
            if price_elem:
                # Extrahovat číselnou cenu z textu jako "49,90 Kč"
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
                valid_from=None,  # Bylo by třeba parsovat ze stránky
                valid_until=None,  # Bylo by třeba parsovat ze stránky
                image_url=image_url,
                product_url=product_url,
                category=None  # Bylo by třeba parsovat ze stránky
            )
        except Exception as e:
            logger.debug(f"Error extracting product info: {e}")
            return None
    
    def _parse_price(self, price_text: str) -> float:
        """
        Parsuje cenu z českého formátu řetězce.
        
        Args:
            price_text: Cenový řetězec jako "49,90 Kč" nebo "49.90"
            
        Returns:
            Číselná hodnota ceny
        """
        # Odstranění měnových symbolů a mezer
        price_text = price_text.replace('Kč', '').replace(',-', '').strip()
        # Nahrazení českého desetinného oddělovače
        price_text = price_text.replace(',', '.')
        # Odstranění oddělovačů tisíců
        price_text = price_text.replace(' ', '')
        
        try:
            return float(price_text)
        except ValueError:
            logger.warning(f"Could not parse price: {price_text}")
            return 0.0
    
    def search_products(self, query: str) -> List[Product]:
        """
        Vyhledá produkty podle názvu nebo klíčového slova.
        
        Args:
            query: Vyhledávací dotaz
            
        Returns:
            Seznam odpovídajících Product objektů
        """
        # Sestavení vyhledávací URL s odpovídajícím URL kódováním
        params = {'q': query}
        search_url = f"{self.BASE_URL}/vyhledavani?{urlencode(params)}"
        
        soup = self.fetch_page(search_url)
        if not soup:
            return []
        
        return self._parse_products(soup)
    
    def get_stores(self) -> List[dict]:
        """
        Získá seznam dostupných obchodů na kupi.cz.
        
        Returns:
            Seznam slovníků s názvem a identifikátorem obchodu
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
        """Zavře session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager vstup."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager výstup."""
        self.close()


def main():
    """Příklad použití KupiCzScraperu."""
    print("Kupi.cz Scraper - Načítání aktuálních slev\n")
    print("=" * 60)
    
    with KupiCzScraper() as scraper:
        # Získat seznam obchodů
        print("\nDostupné obchody:")
        stores = scraper.get_stores()
        for store in stores:
            print(f"  - {store['name']} ({store['id']})")
        
        # Načíst aktuální slevy
        print("\nNačítání aktuálních slev...")
        products = scraper.get_current_discounts()
        
        if products:
            print(f"\nNalezeno {len(products)} produktů ve slevě:\n")
            for i, product in enumerate(products[:10], 1):  # Zobrazit prvních 10
                print(f"{i}. {product}")
        else:
            print("\nŽádné produkty nenalezeny. To může být způsobeno:")
            print("  - Problémy s připojením k síti")
            print("  - Změnami struktury webu vyžadujícími aktualizaci parseru")
            print("  - Anti-scraping opatřeními webu")
            print("\nStruktura scraperu je připravena a čeká na přizpůsobení")
            print("podle skutečné HTML struktury kupi.cz")
        
        # Příklad vyhledávání
        print("\n" + "=" * 60)
        print("Příklad: Vyhledávání 'mléko'...")
        search_results = scraper.search_products("mléko")
        if search_results:
            print(f"Nalezeno {len(search_results)} výsledků")
            for product in search_results[:3]:
                print(f"  - {product}")


if __name__ == "__main__":
    main()
