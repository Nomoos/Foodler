"""
Scraper pro kupi.cz
Tento modul se zabývá pouze scrapováním dat z webu (Single Responsibility)
"""

import requests
from typing import List, Optional, Dict
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote_plus
import logging
from datetime import datetime
import json
import os
import re

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
            
            # Extrakce dat platnosti
            valid_from, valid_until = self._extract_dates_from_element(element)
            
            # Pouze vracet produkt pokud má smysluplný název
            if name and name != "Unknown" and len(name) > 2:
                return Product(
                    name=name,
                    original_price=original_price,
                    discount_price=discount_price,
                    discount_percentage=discount_percentage,
                    store=store,
                    valid_from=valid_from,
                    valid_until=valid_until,
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
        Parsuje datum z českého formátu.
        
        Args:
            date_text: Datum ve formátu "dd.mm.yyyy", "d.m.yyyy", nebo "d. m. yyyy"
            
        Returns:
            datetime objekt nebo None při chybě
        """
        if not date_text:
            return None
        
        # Odstranění nadbytečných znaků
        date_text = date_text.strip()
        
        # Zkusit různé formáty
        date_formats = [
            '%d.%m.%Y',     # 15.1.2026
            '%d. %m. %Y',   # 15. 1. 2026
            '%d.%m.%y',     # 15.1.26
        ]
        
        for date_format in date_formats:
            try:
                return datetime.strptime(date_text, date_format)
            except ValueError:
                continue
        
        logger.debug(f"Could not parse date: {date_text}")
        return None
    
    def _extract_dates_from_element(self, element) -> tuple[Optional[datetime], Optional[datetime]]:
        """
        Extrahuje platnost akce z HTML elementu.
        
        Args:
            element: BeautifulSoup element obsahující info o produktu
            
        Returns:
            Tuple (valid_from, valid_until) nebo (None, None)
        """
        valid_from = None
        valid_until = None
        
        try:
            # Hledat všechny texty v elementu, které mohou obsahovat data
            all_text = element.get_text()
            
            # Vzory pro hledání dat
            # Pattern pro rozsah: "od 15.1.2026 do 21.1.2026", "15.1. - 21.1.2026", etc.
            range_patterns = [
                r'od\s+(\d{1,2}\.\s*\d{1,2}\.\s*\d{4})\s+do\s+(\d{1,2}\.\s*\d{1,2}\.\s*\d{4})',
                r'platnost\s*:?\s*(\d{1,2}\.\s*\d{1,2}\.\s*\d{4})\s*[-–]\s*(\d{1,2}\.\s*\d{1,2}\.\s*\d{4})',
                r'(\d{1,2}\.\s*\d{1,2}\.\s*\d{4})\s*[-–]\s*(\d{1,2}\.\s*\d{1,2}\.\s*\d{4})',
            ]
            
            for pattern in range_patterns:
                match = re.search(pattern, all_text, re.IGNORECASE)
                if match:
                    date1_text = match.group(1).replace(' ', '')
                    date2_text = match.group(2).replace(' ', '')
                    valid_from = self._parse_czech_date(date1_text)
                    valid_until = self._parse_czech_date(date2_text)
                    if valid_from and valid_until:
                        return valid_from, valid_until
            
            # Pattern pro jednotlivá data
            single_date_patterns = [
                r'od\s+(\d{1,2}\.\s*\d{1,2}\.\s*\d{4})',
                r'platí?\s+do\s+(\d{1,2}\.\s*\d{1,2}\.\s*\d{4})',
            ]
            
            for i, pattern in enumerate(single_date_patterns):
                match = re.search(pattern, all_text, re.IGNORECASE)
                if match:
                    date_text = match.group(1).replace(' ', '')
                    parsed_date = self._parse_czech_date(date_text)
                    if parsed_date:
                        if i == 0:  # "od" pattern
                            valid_from = parsed_date
                        else:  # "do" pattern
                            valid_until = parsed_date
            
        except Exception as e:
            logger.debug(f"Error extracting dates: {e}")
        
        return valid_from, valid_until
    
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
    
    def scrape_all_shop_discounts(self) -> Dict[str, List[Product]]:
        """
        Stáhne slevy ze všech dostupných obchodů.
        
        Returns:
            Slovník kde klíč je ID obchodu a hodnota je seznam produktů
        """
        all_discounts = {}
        stores = self.get_stores()
        
        logger.info(f"Starting to scrape discounts from {len(stores)} stores")
        
        for store in stores:
            store_id = store['id']
            store_name = store['name']
            
            logger.info(f"Scraping {store_name}...")
            try:
                # Přidáme zpoždění mezi požadavky (etika scrapování)
                import time
                if all_discounts:  # Pokud již nějaké obchody zpracovány
                    time.sleep(2)  # 2 sekundové zpoždění
                
                products = self.get_current_discounts(store=store_id)
                all_discounts[store_id] = products
                logger.info(f"Found {len(products)} products from {store_name}")
                
            except Exception as e:
                logger.error(f"Error scraping {store_name}: {e}")
                all_discounts[store_id] = []
        
        return all_discounts
    
    def save_discounts_to_json(
        self, 
        discounts: Dict[str, List[Product]], 
        filename: Optional[str] = None,
        directory: str = "data"
    ) -> str:
        """
        Uloží slevy do JSON souboru.
        
        Args:
            discounts: Slovník s produkty z jednotlivých obchodů
            filename: Název souboru (pokud None, použije se timestamp)
            directory: Adresář pro uložení (výchozí: "data")
            
        Returns:
            Cesta k uloženému souboru
        """
        # Vytvoření adresáře pokud neexistuje
        os.makedirs(directory, exist_ok=True)
        
        # Generování názvu souboru s časovým razítkem
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"kupi_discounts_{timestamp}.json"
        
        filepath = os.path.join(directory, filename)
        
        # Konverze produktů na serializovatelný formát
        json_data = {
            'scraped_at': datetime.now().isoformat(),
            'total_stores': len(discounts),
            'total_products': sum(len(products) for products in discounts.values()),
            'stores': {}
        }
        
        for store_id, products in discounts.items():
            json_data['stores'][store_id] = {
                'product_count': len(products),
                'products': [self._product_to_dict(p) for p in products]
            }
        
        # Uložení do souboru
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved {json_data['total_products']} products to {filepath}")
        return filepath
    
    def _product_to_dict(self, product: Product) -> dict:
        """
        Převede Product objekt na slovník pro JSON serializaci.
        
        Args:
            product: Product objekt
            
        Returns:
            Slovník s informacemi o produktu
        """
        return {
            'name': product.name,
            'original_price': product.original_price,
            'discount_price': product.discount_price,
            'discount_percentage': product.discount_percentage,
            'store': product.store,
            'valid_from': product.valid_from.isoformat() if product.valid_from else None,
            'valid_until': product.valid_until.isoformat() if product.valid_until else None,
            'image_url': product.image_url,
            'product_url': product.product_url,
            'category': product.category
        }
    
    def load_discounts_from_json(self, filepath: str) -> Dict[str, List[Product]]:
        """
        Načte slevy z JSON souboru.
        
        Args:
            filepath: Cesta k JSON souboru
            
        Returns:
            Slovník s produkty z jednotlivých obchodů
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        discounts = {}
        for store_id, store_data in json_data.get('stores', {}).items():
            products = []
            for prod_dict in store_data.get('products', []):
                # Převést datumy zpět na datetime objekty
                valid_from = None
                valid_until = None
                
                if prod_dict.get('valid_from'):
                    try:
                        valid_from = datetime.fromisoformat(prod_dict['valid_from'])
                    except:
                        pass
                
                if prod_dict.get('valid_until'):
                    try:
                        valid_until = datetime.fromisoformat(prod_dict['valid_until'])
                    except:
                        pass
                
                product = Product(
                    name=prod_dict['name'],
                    original_price=prod_dict.get('original_price'),
                    discount_price=prod_dict['discount_price'],
                    discount_percentage=prod_dict.get('discount_percentage'),
                    store=prod_dict['store'],
                    valid_from=valid_from,
                    valid_until=valid_until,
                    image_url=prod_dict.get('image_url'),
                    product_url=prod_dict.get('product_url'),
                    category=prod_dict.get('category')
                )
                products.append(product)
            
            discounts[store_id] = products
        
        logger.info(f"Loaded {sum(len(p) for p in discounts.values())} products from {filepath}")
        return discounts
    
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
