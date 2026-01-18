"""
Scraper pro kupi.cz
Tento modul se zabývá pouze scrapováním dat z webu (Single Responsibility)
"""

import requests
from typing import List, Optional
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote_plus
import logging
import re
from datetime import datetime

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
        # Poznámka: Accept-Encoding odstraněno, protože způsobovalo problémy s kupi.cz
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'cs-CZ,cs;q=0.9,en;q=0.8',
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
    
    def get_current_discounts(self, category: Optional[str] = None, store: Optional[str] = None, 
                             sort_order: Optional[int] = None, page: int = 1) -> List[Product]:
        """
        Stáhne aktuální slevy z kupi.cz.
        
        Args:
            category: Volitelný filtr kategorie (např. 'slevy/drubez', 'slevy/potraviny')
            store: Volitelný filtr obchodu (např. 'kaufland', 'albert', 'tesco', 'billa')
            sort_order: Řazení (0=cena za jednotku, další hodnoty dle webu)
            page: Číslo stránky pro stránkování
            
        Returns:
            Seznam Product objektů s informacemi o slevách
        """
        products = []
        
        # Sestavení URL s filtry
        url = self.BASE_URL
        params = {}
        
        # Pokud je zadána kategorie, přidej ji do URL
        if category and store:
            # URL ve formátu /slevy/kategorie/obchod
            url += f"/slevy/{category}/{store}"
        elif category:
            # URL ve formátu /slevy/kategorie
            url += f"/slevy/{category}"
        elif store:
            # URL ve formátu /slevy/obchod
            url += f"/slevy/{store}"
        
        # Přidání parametrů pro řazení a stránkování
        if sort_order is not None:
            params['ord'] = sort_order
        if page > 1:
            params['page'] = page
        
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
    
    def get_ajax_discounts(self, store: str, page: int = 1, sort_order: int = 0) -> List[Product]:
        """
        Stáhne slevy pomocí AJAX endpointu pro rychlejší načítání.
        
        Args:
            store: Název obchodu (např. 'kaufland', 'albert', 'tesco')
            page: Číslo stránky
            sort_order: Řazení (0=cena za jednotku)
            
        Returns:
            Seznam Product objektů
        """
        # AJAX endpoint: /get-akce/obchod?page=X&ord=X&load_linear=0&ajax=1
        url = f"{self.BASE_URL}/get-akce/{store}"
        params = {
            'page': page,
            'ord': sort_order,
            'load_linear': 0,
            'ajax': 1
        }
        url += f"?{urlencode(params)}"
        
        soup = self.fetch_page(url)
        if not soup:
            logger.warning(f"Failed to fetch AJAX data for {store}")
            return []
        
        try:
            products = self._parse_products(soup)
            logger.info(f"Found {len(products)} products via AJAX")
            return products
        except Exception as e:
            logger.error(f"Error parsing AJAX products: {e}")
            return []
    
    def _parse_products(self, soup: BeautifulSoup) -> List[Product]:
        """
        Parsuje informace o produktech z BeautifulSoup objektu.
        
        Args:
            soup: BeautifulSoup objekt obsahující HTML stránky
            
        Returns:
            Seznam Product objektů
        """
        products = []
        
        # Kupi.cz používá div s třídou 'product--wrap' pro produktové kontejnery
        product_elements = soup.find_all('div', class_='product--wrap')
        
        if not product_elements:
            logger.debug("No products found with class 'product--wrap'")
        
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
        try:
            # Extrakce názvu produktu z div s třídou 'product_name'
            name_elem = element.find('div', class_='product_name')
            if name_elem:
                # Vyčistit název od extra textu (např. "Přidat produkt do oblíbených")
                name = name_elem.get_text(strip=True)
                # Odstraň nežádoucí části textu
                for unwanted in ['Přidat produkt do oblíbených', 'Zapněte si oblíbené', 
                                'a upozorníme vás na novou akci', 'Běžná cena:', 'Není v akci']:
                    name = name.replace(unwanted, '')
                
                # Odstraň cenové informace z názvu (např. "243,77Kč" nebo "243,77 Kč")
                import re
                name = re.sub(r'\d+[,\.]\d+\s*Kč', '', name)
                name = re.sub(r'\d+\s*Kč', '', name)
                name = name.strip()
            else:
                name = "Unknown"
            
            # Extrakce průměrné ceny z div s třídou 'avg_price'
            avg_price_elem = element.find('div', class_='avg_price')
            discount_price = 0.0
            original_price = None
            
            if avg_price_elem:
                # Získej text jako "Běžná cena:243,77Kč"
                price_text = avg_price_elem.get_text(strip=True)
                # Extrahuj pouze číslo
                price_text = price_text.replace('Běžná cena:', '').replace('Není v akci', '')
                if price_text:
                    discount_price = self._parse_price(price_text)
                    original_price = discount_price  # Pro zobrazení běžné ceny
            
            # Pokusit se najít akční cenu
            discounts_div = element.find('div', class_='product_discounts')
            if discounts_div:
                price_divs = discounts_div.find_all('div', class_=lambda x: x and 'price' in str(x).lower())
                if price_divs:
                    # Použij první nalezenou cenu jako akční cenu
                    for price_div in price_divs:
                        price_text = price_div.get_text(strip=True)
                        if price_text and 'Kč' in price_text:
                            parsed_price = self._parse_price(price_text)
                            if parsed_price > 0 and parsed_price < discount_price:
                                discount_price = parsed_price
                                break
            
            # Vypočítat procento slevy
            discount_percentage = None
            if original_price and discount_price and original_price > discount_price:
                discount_percentage = round(((original_price - discount_price) / original_price) * 100, 1)
            
            # Hledat název obchodu v odkazech na letáky
            store = "Různé obchody"  # Výchozí hodnota
            store_links = element.find_all('a', href=lambda x: x and '/letaky/' in str(x))
            if store_links:
                # Vezmi první obchod
                store_text = store_links[0].get_text(strip=True)
                if store_text:
                    store = store_text
            
            # Obrázek produktu
            img_elem = element.find('img')
            image_url = None
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src')
                if image_url and not image_url.startswith('http'):
                    image_url = self.BASE_URL + image_url
            
            # Link na detail produktu
            link_elem = element.find('a', href=True)
            product_url = None
            if link_elem:
                product_url = link_elem.get('href')
                if product_url and not product_url.startswith('http'):
                    product_url = self.BASE_URL + product_url
            
            # Pouze vracet produkt pokud má smysluplný název
            if name and name != "Unknown" and len(name) > 2:
                return Product(
                    name=name,
                    original_price=original_price,
                    discount_price=discount_price,
                    discount_percentage=discount_percentage,
                    store=store,
                    valid_from=None,
                    valid_until=None,
                    image_url=image_url,
                    product_url=product_url,
                    category=None
                )
            return None
            
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
        # Odstranění nechtěného textu
        price_text = price_text.replace('Běžná cena:', '').replace('Běžnácena:', '')
        price_text = price_text.replace('cena', '').replace('Kč', '').replace(',-', '').strip()
        
        # Nahrazení českého desetinného oddělovače
        price_text = price_text.replace(',', '.')
        # Odstranění oddělovačů tisíců a mezer
        price_text = price_text.replace(' ', '').replace('\xa0', '')
        
        try:
            return float(price_text)
        except ValueError:
            logger.warning(f"Could not parse price: {price_text}")
            return 0.0
    
    def _parse_czech_date(self, date_text: str) -> Optional[datetime]:
        """
        Parsuje datum v českém formátu.
        
        Args:
            date_text: Datum jako "18.1.2026", "18. 1. 2026", nebo "18. ledna 2026"
            
        Returns:
            datetime objekt nebo None při chybě
        """
        if not date_text:
            return None
        
        # Čištění textu
        date_text = date_text.strip()
        
        # České názvy měsíců
        mesice = {
            'leden': 1, 'ledna': 1,
            'únor': 2, 'února': 2,
            'březen': 3, 'března': 3,
            'duben': 4, 'dubna': 4,
            'květen': 5, 'května': 5,
            'červen': 6, 'června': 6,
            'červenec': 7, 'července': 7,
            'srpen': 8, 'srpna': 8,
            'září': 9,
            'říjen': 10, 'října': 10,
            'listopad': 11, 'listopadu': 11,
            'prosinec': 12, 'prosince': 12
        }
        
        # Pokus o parsování s názvem měsíce
        for mesic_nazev, mesic_cislo in mesice.items():
            if mesic_nazev in date_text.lower():
                try:
                    # Extrahuj den a rok
                    parts = re.findall(r'\d+', date_text)
                    if len(parts) >= 2:
                        den = int(parts[0])
                        rok = int(parts[1])
                        return datetime(rok, mesic_cislo, den)
                except (ValueError, IndexError):
                    pass
        
        # Pokus o parsování čísleného formátu (d.m.yyyy nebo dd.mm.yyyy)
        patterns = [
            r'(\d{1,2})\.?\s*(\d{1,2})\.?\s*(\d{4})',  # 18.1.2026 nebo 18. 1. 2026
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # 18/1/2026
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_text)
            if match:
                try:
                    den = int(match.group(1))
                    mesic = int(match.group(2))
                    rok = int(match.group(3))
                    return datetime(rok, mesic, den)
                except (ValueError, IndexError):
                    pass
        
        logger.debug(f"Could not parse date: {date_text}")
        return None
    
    def search_products(self, query: str) -> List[Product]:
        """
        Vyhledá produkty podle názvu nebo klíčového slova.
        
        Args:
            query: Vyhledávací dotaz
            
        Returns:
            Seznam odpovídajících Product objektů
        """
        # Kupi.cz používá parametr 'f' pro vyhledávání
        # Použijeme quote_plus pro správné kódování českých znaků
        encoded_query = quote_plus(query)
        search_url = f"{self.BASE_URL}/hledej?f={encoded_query}"
        
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
