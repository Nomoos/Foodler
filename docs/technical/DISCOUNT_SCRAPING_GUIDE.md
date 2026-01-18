# Scrapování a ukládání slev z Kupi.cz

Tento dokument popisuje novou funkcionalitu pro stahování a ukládání kompletních seznamů slev ze všech obchodů na kupi.cz včetně dat platnosti.

## Přehled nové funkcionality

### 🎯 Co bylo přidáno

1. **Extrakce dat platnosti** - `_parse_czech_date()` a `_extract_dates_from_element()`
   - Parsování českých datových formátů (dd.mm.yyyy)
   - Automatická detekce rozsahu platnosti ("od ... do ...")
   - Podpora různých formátů zápisu data

2. **Stahování slev ze všech obchodů** - `scrape_all_shop_discounts()`
   - Automatické projití všech dostupných obchodů
   - Rate limiting (2 sekundy mezi požadavky)
   - Robustní error handling

3. **Ukládání do JSON** - `save_discounts_to_json()`
   - Strukturované ukládání s metadaty
   - ISO formát pro data
   - Zachování všech informací o produktu

4. **Načítání z JSON** - `load_discounts_from_json()`
   - Zpětná konverze do Product objektů
   - Automatická deserializace dat
   - Round-trip kompatibilita

## Použití

### 1. Základní použití - stažení a uložení všech slev

```python
from src.scrapers.kupi_scraper import KupiCzScraper

# Inicializace scraperu
with KupiCzScraper() as scraper:
    # Stáhnout slevy ze všech obchodů
    all_discounts = scraper.scrape_all_shop_discounts()
    
    # Uložit do JSON souboru
    filepath = scraper.save_discounts_to_json(all_discounts)
    print(f"Uloženo do: {filepath}")
```

### 2. Použití připraveného skriptu

```bash
python scrape_and_save_discounts.py
```

Tento skript:
- Stáhne slevy ze všech obchodů (Lidl, Kaufland, Albert, Penny, Billa, Tesco, Globus, Makro)
- Zobrazí statistiky (počet produktů z každého obchodu)
- Ukáže příklady produktů s datumy platnosti
- Uloží vše do JSON souboru ve složce `data/`

### 3. Načtení uložených dat

```python
from src.scrapers.kupi_scraper import KupiCzScraper

with KupiCzScraper() as scraper:
    # Načíst data z JSON souboru
    discounts = scraper.load_discounts_from_json('data/kupi_discounts_20260118_103000.json')
    
    # Zpracovat produkty
    for store_id, products in discounts.items():
        print(f"\n{store_id.upper()}:")
        for product in products:
            print(f"  - {product.name}: {product.discount_price} Kč")
            if product.valid_until:
                print(f"    Platí do: {product.valid_until.strftime('%d.%m.%Y')}")
```

### 4. Filtrace produktů podle data platnosti

```python
from datetime import datetime

# Najít produkty platné dnes
today = datetime.now()

active_deals = []
for store_id, products in discounts.items():
    for product in products:
        # Kontrola platnosti
        is_valid = True
        
        if product.valid_from and product.valid_from > today:
            is_valid = False  # Ještě nezačalo
        
        if product.valid_until and product.valid_until < today:
            is_valid = False  # Již skončilo
        
        if is_valid:
            active_deals.append(product)

print(f"Nalezeno {len(active_deals)} aktivních slev")
```

## Struktura JSON souboru

```json
{
  "scraped_at": "2026-01-18T10:30:00",
  "total_stores": 8,
  "total_products": 1234,
  "stores": {
    "lidl": {
      "product_count": 150,
      "products": [
        {
          "name": "Kuřecí prsa",
          "original_price": 150.0,
          "discount_price": 99.9,
          "discount_percentage": 33.4,
          "store": "Lidl",
          "valid_from": "2026-01-15T00:00:00",
          "valid_until": "2026-01-21T00:00:00",
          "image_url": "https://www.kupi.cz/...",
          "product_url": "https://www.kupi.cz/...",
          "category": null
        }
      ]
    }
  }
}
```

### Význam polí:

- **scraped_at**: Kdy byla data stažena
- **total_stores**: Počet obchodů
- **total_products**: Celkový počet produktů
- **stores**: Slovník s daty podle obchodů
  - **product_count**: Počet produktů v obchodě
  - **products**: Seznam produktů
    - **valid_from**: Začátek platnosti akce (ISO formát)
    - **valid_until**: Konec platnosti akce (ISO formát)

## API Reference

### `scrape_all_shop_discounts() -> Dict[str, List[Product]]`

Stáhne slevy ze všech dostupných obchodů.

**Returns:**
- Slovník kde klíč je ID obchodu (`'lidl'`, `'kaufland'`, ...) a hodnota je seznam `Product` objektů

**Příklad:**
```python
all_discounts = scraper.scrape_all_shop_discounts()
# Výsledek: {'lidl': [Product(...), ...], 'kaufland': [...], ...}
```

### `save_discounts_to_json(discounts, filename=None, directory='data') -> str`

Uloží slevy do JSON souboru.

**Parametry:**
- `discounts`: Slovník s produkty (výstup z `scrape_all_shop_discounts()`)
- `filename`: Název souboru (výchozí: `kupi_discounts_{timestamp}.json`)
- `directory`: Cílový adresář (výchozí: `'data'`)

**Returns:**
- Plná cesta k uloženému souboru

**Příklad:**
```python
filepath = scraper.save_discounts_to_json(
    discounts, 
    filename='slevy_leden.json',
    directory='archive'
)
```

### `load_discounts_from_json(filepath) -> Dict[str, List[Product]]`

Načte slevy z JSON souboru.

**Parametry:**
- `filepath`: Cesta k JSON souboru

**Returns:**
- Slovník s produkty ve stejném formátu jako `scrape_all_shop_discounts()`

**Příklad:**
```python
discounts = scraper.load_discounts_from_json('data/kupi_discounts_20260118.json')
```

### `_parse_czech_date(date_text: str) -> Optional[datetime]`

Parsuje české datum.

**Podporované formáty:**
- `"15.1.2026"`
- `"15. 1. 2026"`
- `"15.1.26"`

**Příklad:**
```python
date = scraper._parse_czech_date("15.1.2026")
# Vrací: datetime(2026, 1, 15, 0, 0)
```

### `_extract_dates_from_element(element) -> tuple[Optional[datetime], Optional[datetime]]`

Extrahuje data platnosti z HTML elementu.

**Detekuje vzory:**
- `"od 15.1.2026 do 21.1.2026"`
- `"Platnost: 15.1.2026 - 21.1.2026"`
- `"15.1.2026 - 21.1.2026"`
- `"od 15.1.2026"`
- `"platí do 21.1.2026"`

**Returns:**
- Tuple `(valid_from, valid_until)` nebo `(None, None)`

## Testování

Projekt obsahuje kompletní testovací sadu:

```bash
# Test nové funkcionality
python test_discount_scraping.py

# Test původní funkcionality (zajištění zpětné kompatibility)
python test_kupi_scraper.py
```

### Testované oblasti:

1. **Parsování dat** - různé formáty českých dat
2. **Extrakce dat z HTML** - rozsahy, jednotlivá data
3. **Scrapování ze všech obchodů** - mock testy
4. **JSON serializace/deserializace** - round-trip testy
5. **Zpětná kompatibilita** - původní testy stále fungují

## Příklady použití

### Weekly meal planning s aktuálními slevami

```python
from src.scrapers.kupi_scraper import KupiCzScraper
from datetime import datetime, timedelta

def find_this_week_deals():
    """Najde slevy platné tento týden."""
    
    with KupiCzScraper() as scraper:
        # Stáhnout všechny slevy
        all_discounts = scraper.scrape_all_shop_discounts()
        
        # Uložit pro pozdější použití
        filepath = scraper.save_discounts_to_json(all_discounts)
        
        # Filtrovat platné tento týden
        today = datetime.now()
        week_end = today + timedelta(days=7)
        
        weekly_deals = {}
        for store_id, products in all_discounts.items():
            valid_products = []
            
            for product in products:
                # Produkt je platný pokud:
                # - nemá valid_from NEBO valid_from <= dnes
                # - nemá valid_until NEBO valid_until >= konec týdne
                
                if product.valid_from and product.valid_from > today:
                    continue  # Ještě nezačalo
                
                if product.valid_until and product.valid_until < today:
                    continue  # Už skončilo
                
                valid_products.append(product)
            
            if valid_products:
                weekly_deals[store_id] = valid_products
        
        return weekly_deals, filepath

# Použití
deals, filepath = find_this_week_deals()
print(f"Nalezeno {sum(len(p) for p in deals.values())} slev platných tento týden")
print(f"Data uložena v: {filepath}")
```

### Srovnání cen mezi obchody

```python
def compare_prices_across_stores(product_name_pattern, discounts):
    """Porovná ceny produktu napříč obchody."""
    
    results = []
    
    for store_id, products in discounts.items():
        for product in products:
            if product_name_pattern.lower() in product.name.lower():
                results.append({
                    'store': product.store,
                    'name': product.name,
                    'price': product.discount_price,
                    'discount': product.discount_percentage,
                    'valid_until': product.valid_until
                })
    
    # Seřadit podle ceny
    results.sort(key=lambda x: x['price'])
    
    return results

# Použití
with KupiCzScraper() as scraper:
    discounts = scraper.load_discounts_from_json('data/kupi_discounts_latest.json')
    
    # Najít nejlevnější kuřecí prsa
    chicken_prices = compare_prices_across_stores("kuřecí prsa", discounts)
    
    if chicken_prices:
        best = chicken_prices[0]
        print(f"Nejlevnější: {best['name']}")
        print(f"Cena: {best['price']} Kč v {best['store']}")
        print(f"Sleva: {best['discount']}%")
        if best['valid_until']:
            print(f"Platí do: {best['valid_until'].strftime('%d.%m.%Y')}")
```

### Sledování historie cen

```python
import os
import json
from datetime import datetime

def track_price_history(data_directory='data'):
    """Analyzuje historii cen z uložených JSON souborů."""
    
    price_history = {}
    
    # Načíst všechny JSON soubory
    for filename in sorted(os.listdir(data_directory)):
        if not filename.startswith('kupi_discounts_') or not filename.endswith('.json'):
            continue
        
        filepath = os.path.join(data_directory, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        scraped_at = datetime.fromisoformat(data['scraped_at'])
        
        # Projít produkty
        for store_id, store_data in data['stores'].items():
            for product in store_data['products']:
                key = (product['name'], store_id)
                
                if key not in price_history:
                    price_history[key] = []
                
                price_history[key].append({
                    'date': scraped_at,
                    'price': product['discount_price'],
                    'discount': product.get('discount_percentage')
                })
    
    return price_history

# Použití
history = track_price_history()

# Najít produkt s největší změnou ceny
for (name, store), prices in history.items():
    if len(prices) >= 2:
        prices.sort(key=lambda x: x['date'])
        first_price = prices[0]['price']
        last_price = prices[-1]['price']
        change = ((last_price - first_price) / first_price) * 100
        
        if abs(change) > 10:  # Změna > 10%
            print(f"{name} ({store}): {change:+.1f}%")
```

## Best Practices

### 1. Rate Limiting
```python
# Funkce scrape_all_shop_discounts() automaticky přidává 2s zpoždění mezi obchody
# Pro ruční použití:
import time

for store in stores:
    products = scraper.get_current_discounts(store=store['id'])
    time.sleep(2)  # 2 sekundy mezi požadavky
```

### 2. Error Handling
```python
try:
    all_discounts = scraper.scrape_all_shop_discounts()
    filepath = scraper.save_discounts_to_json(all_discounts)
except Exception as e:
    logger.error(f"Chyba při scrapování: {e}")
    # Fallback: použít starší data
    discounts = scraper.load_discounts_from_json('data/backup.json')
```

### 3. Automatické stahování
```python
import schedule

def scrape_and_save():
    """Automaticky stahovat slevy každý den v 6:00."""
    with KupiCzScraper() as scraper:
        discounts = scraper.scrape_all_shop_discounts()
        scraper.save_discounts_to_json(discounts)
        print(f"Slevy aktualizovány: {datetime.now()}")

# Naplánovat denní spuštění
schedule.every().day.at("06:00").do(scrape_and_save)
```

## Známé limitace

1. **Data platnosti** - Extrakce dat závisí na HTML struktuře kupi.cz
   - Pokud web změní strukturu, může být potřeba aktualizovat regex vzory
   - Ne všechny produkty mají explicitně uvedené datum platnosti

2. **Rate Limiting** - Respektujeme 2s prodlevu mezi požadavky
   - Stažení všech obchodů trvá ~16 sekund (8 obchodů × 2s)

3. **Anti-scraping** - Kupi.cz může blokovat nadměrné požadavky
   - Doporučujeme stahovat maximálně 1× denně
   - Používejte cache (uložené JSON soubory)

## Migrace z předchozí verze

Pokud jste používali starší verzi scraperu:

```python
# STARÁ verze
products = scraper.get_current_discounts(store='lidl')
# valid_from a valid_until byly vždy None

# NOVÁ verze
products = scraper.get_current_discounts(store='lidl')
# valid_from a valid_until jsou nyní extrahovány z HTML

# Plus nové funkce:
all_discounts = scraper.scrape_all_shop_discounts()
filepath = scraper.save_discounts_to_json(all_discounts)
```

Zpětná kompatibilita je zachována - existující kód bude fungovat beze změn.

## Podpora

Pokud narazíte na problémy:

1. Zkontrolujte logy: `logging.basicConfig(level=logging.DEBUG)`
2. Ověřte HTML strukturu kupi.cz pomocí browser DevTools
3. Spusťte testy: `python test_discount_scraping.py`
4. Otevřete issue v repozitáři

## Changelog

### v2.0.0 (2026-01-18)

✨ **Nové funkce:**
- Extrakce dat platnosti slev (`valid_from`, `valid_until`)
- Funkce pro stažení slev ze všech obchodů
- JSON storage s metadaty
- Round-trip load/save funkcionalita

🧪 **Testy:**
- 10 nových unit testů pro novou funkcionalitu
- Zachována zpětná kompatibilita (11 původních testů)

📚 **Dokumentace:**
- Kompletní průvodce použitím
- Příklady pro běžné use case
- API reference

---

*Vytvořeno pro projekt Foodler - Family Diet Planning System*
