# Analyzátor masných produktů a generátor nákupního seznamu

## Přehled

Tento dokument popisuje novou funkcionalitu pro vyhledávání nejvhodnějších masných produktů z akčních nabídek a generování optimalizovaných nákupních seznamů pro keto dietu.

## Nové moduly

### 1. Vylepšený Kupi.cz Scraper

**Soubor:** `src/scrapers/kupi_scraper.py`

#### Nové funkce:

- **Kategorie a obchody**: Podpora URL jako `/slevy/drubez`, `/slevy/drubez/kaufland`
- **Řazení**: Možnost řazení podle ceny za jednotku (`ord=0`)
- **Stránkování**: Podpora parametru `page` pro procházení více stránek
- **AJAX endpoint**: Rychlejší načítání přes `/get-akce/{store}?page=X&ord=X&ajax=1`
- **Parsování českých datumů**: Podpora formátů jako "18.1.2026", "18. ledna 2026"

#### Příklady použití:

```python
from src.scrapers.kupi_scraper import KupiCzScraper

with KupiCzScraper() as scraper:
    # Drůbež ze všech obchodů
    products = scraper.get_current_discounts(category='drubez')
    
    # Kaufland řazený podle ceny, strana 2
    products = scraper.get_current_discounts(
        store='kaufland', 
        sort_order=0,  # 0 = cena za jednotku
        page=2
    )
    
    # Drůbež pouze z Kauflandu
    products = scraper.get_current_discounts(
        category='drubez',
        store='kaufland'
    )
    
    # AJAX endpoint (rychlejší)
    products = scraper.get_ajax_discounts('kaufland', page=5, sort_order=0)
```

### 2. MeatAnalyzer - Analyzátor masných produktů

**Soubor:** `src/analyzers/meat_analyzer.py`

Analyzuje masné produkty z hlediska vhodnosti pro keto dietu.

#### Klíčové funkce:

- **Načtení produktů**: `fetch_meat_products(store, page, sort_by_price)`
- **Ověření nutriční hodnoty**: `verify_nutrition(product)` - integruje s kaloricketabulky.cz
- **Keto skóre**: `score_product_for_keto(product, nutrition_data)` - hodnotí 0-100
- **Filtrace podle data**: `filter_valid_on_date(products, date)`
- **Generování reportu**: `generate_report(products, with_nutrition)`

#### Kritéria hodnocení:

- **Minimální bílkoviny**: 15g na 100g
- **Maximální sacharidy**: 5g na 100g (keto standard)
- **Sleva**: Bonus až +20 bodů podle procenta slevy
- **Cena**: Bonus za produkty pod 100 Kč

#### Příklad použití:

```python
from src.analyzers.meat_analyzer import MeatAnalyzer
from datetime import datetime

with MeatAnalyzer(location="Valašské Meziříčí") as analyzer:
    # Načíst masné produkty z Kauflandu
    products = analyzer.fetch_meat_products(store='kaufland', page=1)
    
    # Filtrovat platné k 18.1.2026
    target_date = datetime(2026, 1, 18)
    valid_products = analyzer.filter_valid_on_date(products, target_date)
    
    # Vygenerovat report
    report = analyzer.generate_report(valid_products, with_nutrition=False)
    print(report)
```

### 3. ShoppingListGenerator - Generátor nákupního seznamu

**Soubor:** `src/planners/shopping_list_generator.py`

Generuje optimalizované týdenní nákupní seznamy pro rodinu.

#### Klíčové funkce:

- **Týdenní seznam**: `generate_weekly_list(stores, target_date, family_size)`
- **Formátování**: `format_shopping_list(shopping_lists, format_type)` - text nebo markdown
- **Export**: `export_to_file(shopping_lists, filename, format_type)`
- **Kategorizace**: `_categorize_products(products)` - třídí podle typu

#### Podporované kategorie:

- Maso a drůbež
- Mléčné výrobky
- Vejce
- Zelenina
- Ostatní

#### Příklad použití:

```python
from src.planners.shopping_list_generator import ShoppingListGenerator
from datetime import datetime

with ShoppingListGenerator(location="Valašské Meziříčí") as generator:
    # Vygenerovat seznam pro 4 obchody
    shopping_lists = generator.generate_weekly_list(
        stores=['kaufland', 'tesco', 'albert', 'billa'],
        target_date=datetime(2026, 1, 18),
        family_size=3
    )
    
    # Zobrazit jako text
    text = generator.format_shopping_list(shopping_lists, format_type="text")
    print(text)
    
    # Exportovat jako Markdown
    generator.export_to_file(
        shopping_lists, 
        "nakup/seznam_18_01_2026.md",
        format_type="markdown"
    )
```

## Vylepšený Product model

**Soubor:** `modely/product.py`

### Nová pole:

- `barcode`: str - EAN čárový kód pro ověření v nutričních databázích
- `location`: str - Lokace obchodu (např. "Valašské Meziříčí")
- `unit_price`: float - Cena za jednotku (Kč/kg)
- `unit`: str - Jednotka (kg, l, ks)

### Nová metoda:

- `is_valid_on_date(date)`: Kontroluje platnost k danému datu

## Testování

### Unit testy

**Soubor:** `test_meat_analyzer_unit.py`

Spustit: `python3 test_meat_analyzer_unit.py`

**Pokrytí:**
- 16 unit testů
- 100% úspěšnost
- Testuje všechny nové komponenty

### Integrační testy

**Soubor:** `test_new_features.py`

Spustit: `python3 test_new_features.py`

**Co testuje:**
- Vylepšený scraper s reálnými URL
- Analyzátor masa s mock daty
- Generátor nákupního seznamu
- Parsování českých datumů

## Workflow pro splnění zadání

### 1. Vyhledání nejvhodnějšího masa

```python
from src.analyzers.meat_analyzer import MeatAnalyzer
from datetime import datetime

with MeatAnalyzer(location="Valašské Meziříčí") as analyzer:
    # Načíst produkty z různých obchodů
    stores = ['kaufland', 'tesco', 'albert', 'billa']
    all_products = []
    
    for store in stores:
        products = analyzer.fetch_meat_products(store=store)
        all_products.extend(products)
    
    # Filtrovat platné k 18.1.2026
    target_date = datetime(2026, 1, 18)
    valid_products = analyzer.filter_valid_on_date(all_products, target_date)
    
    # Report s nutričním ověřením
    report = analyzer.generate_report(valid_products[:20], with_nutrition=True)
    print(report)
```

### 2. Generování týdenního nákupního seznamu

```python
from src.planners.shopping_list_generator import ShoppingListGenerator
from datetime import datetime

with ShoppingListGenerator(location="Valašské Meziříčí") as generator:
    shopping_lists = generator.generate_weekly_list(
        stores=['kaufland', 'tesco', 'albert', 'billa'],
        target_date=datetime(2026, 1, 18),
        family_size=3
    )
    
    # Export do Markdown
    generator.export_to_file(
        shopping_lists,
        "nakup/tydenni_seznam_18_01_2026.md",
        format_type="markdown"
    )
```

## Příklady URL, které scraper podporuje

1. **Kategorie drůbež**: `https://www.kupi.cz/slevy/drubez`
2. **Drůbež v Kauflandu**: `https://www.kupi.cz/slevy/drubez/kaufland`
3. **Kaufland řazený podle ceny**: `https://www.kupi.cz/slevy/kaufland?ord=0`
4. **Stránkování**: `https://www.kupi.cz/slevy/kaufland?ord=0&page=2`
5. **AJAX endpoint**: `https://www.kupi.cz/get-akce/kaufland?page=5&ord=0&load_linear=0&ajax=1`

## Integrace s nutričními databázemi

Analyzátor automaticky ověřuje produkty pomocí:
- **kaloricketabulky.cz**: Hledá podle názvu produktu
- **Zjednodušené názvy**: Automaticky vytváří varianty (např. "Kuřecí prsa Bio 500g" → "kuřecí prsa", "kuřecí")
- **Barcode**: Připraveno pro budoucí ověření podle EAN kódu

## Formát českých datumů

Scraper podporuje tyto formáty:
- `18.1.2026`
- `18. 1. 2026`
- `18/1/2026`
- `18. ledna 2026`
- `1. února 2026`

## Tipy pro použití

1. **Rychlé testování**: Použijte `with_nutrition=False` v `generate_report()` pro rychlejší výsledky
2. **AJAX endpoint**: Pro velké objemy dat použijte `get_ajax_discounts()` místo `get_current_discounts()`
3. **Stránkování**: Procházejte všechny stránky pomocí cyklu s `page` parametrem
4. **Export**: Markdown formát je vhodný pro GitHub Issues, text pro print

## Známá omezení

1. **Struktura webu**: Scraper je závislý na aktuální struktuře kupi.cz
2. **Rate limiting**: Respektujte zpoždění mezi požadavky (min 2 sekundy)
3. **Lokace**: Aktuálně nepodporuje automatický výběr lokace na webu
4. **Barcode**: EAN kódy nejsou vždy dostupné na kupi.cz

## Další vývoj

Viz nové issue s plánem pokračování vývoje, které bude vytvořeno automaticky.

## Autor

Vytvořeno pro projekt Foodler - keto dietní plánovač pro českou rodinu.

---

**Datum vytvoření**: 18.1.2026  
**Verze**: 1.0.0  
**Status**: ✅ Funkční, otestováno
