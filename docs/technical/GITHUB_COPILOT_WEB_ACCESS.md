# Návod: Konfigurace GitHub Copilot Pro+ pro testování scraperů

## 📋 Obsah

1. [Přehled](#přehled)
2. [Požadavky](#požadavky)
3. [Konfigurace repozitáře](#konfigurace-repozitáře)
4. [Povolení přístupu k webovým stránkám](#povolení-přístupu-k-webovým-stránkám)
5. [Vytvoření Copilot instrukcí](#vytvoření-copilot-instrukcí)
6. [Testování scraperů](#testování-scraperů)
7. [Řešení problémů](#řešení-problémů)

---

## Přehled

Tento návod vysvětluje, jak nakonfigurovat GitHub Copilot Pro+ pro práci s web scrapery v tomto repozitáři. Konkrétně se zaměřuje na povolení přístupu k:

- **https://www.kaloricketabulky.cz/** - databáze nutričních hodnot potravin
- **https://www.kupi.cz/** - agregátor slev z českých obchodů

### Co je GitHub Copilot Pro+?

GitHub Copilot Pro+ je rozšířená verze AI asistenta, která umí:
- 🌐 Přistupovat k internetu a načítat data z webových stránek
- 📚 Indexovat a prohledávat váš repozitář
- 🔍 Testovat a validovat kód s reálnými daty
- 🤖 Provádět interaktivní testování API a scraperů

---

## Požadavky

### 1. GitHub Copilot Pro+ Subscription

Pro přístup k webovým datům je nutné:
- ✅ Aktivní předplatné **GitHub Copilot Pro** nebo **GitHub Copilot Enterprise**
- ✅ Povolení funkce "Web Search" v nastavení GitHub Copilot

### 2. Ověření přístupu k funkci

1. Přejděte do nastavení GitHub účtu: https://github.com/settings/copilot
2. Zkontrolujte, že máte aktivní předplatné
3. Ujistěte se, že je povolena funkce **"Allow GitHub Copilot to access the web"**

### 3. VS Code nebo GitHub Codespaces

- VS Code s rozšířením GitHub Copilot (verze 1.145+)
- Nebo GitHub Codespaces s povoleným Copilotem

---

## Konfigurace repozitáře

### Krok 1: Vytvoření `.github` složky

Vytvořte strukturu pro GitHub Copilot instrukce:

```bash
mkdir -p .github
cd .github
```

### Krok 2: Konfigurace přístupu k webům

GitHub Copilot Pro+ vyžaduje explicitní povolení pro přístup k externím webovým stránkám. Toto se konfiguruje na úrovni organizace nebo účtu.

#### Pro osobní repozitáře:

1. Přejděte do nastavení: https://github.com/settings/copilot
2. V sekci **"Permissions"** najděte **"Allow requests to external domains"**
3. Přidejte následující domény:
   ```
   www.kaloricketabulky.cz
   kaloricketabulky.cz
   www.kupi.cz
   kupi.cz
   ```

#### Pro organizační repozitáře:

1. Administrátor organizace musí přejít do nastavení organizace
2. Navigujte do `Settings → Copilot → Policies`
3. Povolte **"Web browsing"** pro členy organizace
4. Přidejte povolené domény do whitelistu

---

## Vytvoření Copilot instrukcí

### Krok 3: Vytvořte `.github/copilot-instructions.md`

Tento soubor říká GitHub Copilotu, jak pracovat s vaším projektem:

```markdown
# GitHub Copilot Instructions for Foodler Project

## Project Overview

This is a family diet planning system focused on ketogenic/low-carb nutrition with meal planning and shopping optimization.

## Web Scrapers

### 1. Nutrition Data Scraper (kaloricketabulky.cz)

**Purpose**: Fetch nutritional information for food items
**File**: `fetch_nutrition_data.py`
**Target URL**: https://www.kaloricketabulky.cz/

**Key Functions**:
- `search_product(product_name)` - Search for products by name
- `fetch_nutrition_data(url)` - Extract nutrition data from product page
- `fetch_by_product_name(product_name)` - Combined search and fetch

**Test Examples**:
```python
# Test with real data
data = fetch_by_product_name("Tvaroh tučný")
data = fetch_nutrition_data("https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend")
```

### 2. Discount Scraper (kupi.cz)

**Purpose**: Find discounts and deals from Czech supermarkets
**File**: `src/scrapers/kupi_scraper.py`
**Target URL**: https://www.kupi.cz/

**Key Functions**:
- `get_current_discounts(category, store)` - Get current deals
- `search_products(query)` - Search for specific products
- `get_stores()` - List available stores

**Test Examples**:
```python
# Test with real data
scraper = KupiCzScraper()
products = scraper.get_current_discounts(category='potraviny')
results = scraper.search_products("kuřecí prsa")
```

## Testing Guidelines

### When testing scrapers:

1. **Always verify web access is enabled** before running scraper tests
2. **Use small samples first** to avoid rate limiting
3. **Check robots.txt** compliance: 
   - https://www.kaloricketabulky.cz/robots.txt
   - https://www.kupi.cz/robots.txt
4. **Add delays** between requests (2-3 seconds minimum)
5. **Handle errors gracefully** - sites may change structure

### Expected Data Structures:

**Nutrition Data (kaloricketabulky.cz)**:
```json
{
  "product_name": "Product Name",
  "url": "https://www.kaloricketabulky.cz/...",
  "macros": {
    "calories": "380 kcal",
    "protein": "78 g",
    "carbohydrates": "6 g",
    "fat": "6 g",
    "fiber": "2 g"
  }
}
```

**Discount Data (kupi.cz)**:
```python
Product(
    name="Kuřecí prsa",
    original_price=150.0,
    discount_price=99.90,
    discount_percentage=33.4,
    store="Lidl",
    category="Maso"
)
```

## Code Style & Conventions

- Use Czech language for comments and documentation
- Follow PEP 8 for Python code
- Use type hints for function parameters
- Include docstrings for all public functions
- Handle Czech characters properly (UTF-8 encoding)

## Diet Context

Target macros for the diet plan:
- **Protein**: minimum 140g daily
- **Carbohydrates**: max 70g daily (ketogenic approach)
- **Calories**: 2000 kcal daily target
- Focus on: meat, fish, eggs, dairy, low-carb vegetables

## When suggesting code changes:

1. Maintain compatibility with existing code structure
2. Keep scraper logic separate (Single Responsibility Principle)
3. Use the existing `Product` dataclass from `modely/product.py`
4. Follow the logging patterns already in place
5. Test with real web data when web access is available
```

### Krok 4: Uložte soubor

Soubor uložte jako `.github/copilot-instructions.md` v kořenovém adresáři repozitáře.

---

## Povolení přístupu k webovým stránkám

### Metoda 1: Pomocí GitHub Copilot Chat v VS Code

1. Otevřete VS Code s tímto repozitářem
2. Otevřete GitHub Copilot Chat (Ctrl+Shift+I nebo Cmd+Shift+I)
3. Zkuste požadavek s webovým přístupem:

```
@workspace Načti reálná data z www.kaloricketabulky.cz pro produkt "Tvaroh" 
a ověř, že scraper funguje správně
```

4. Copilot by měl:
   - Požádat o povolení k přístupu na web
   - Po povolení načíst data
   - Analyzovat výsledky scraperu

### Metoda 2: Pomocí GitHub Codespaces

1. Otevřete repozitář v GitHub Codespaces
2. GitHub Copilot bude mít automaticky povolen webový přístup (pokud je zapnut v nastavení)
3. Použijte Copilot Chat pro testování:

```
Otestuj fetch_nutrition_data.py s reálným produktem z kaloricketabulky.cz
```

### Metoda 3: Povolení v organizačních policies

Pro organizační repozitáře musí administrátor:

1. Přejít do `Organization Settings → Copilot → Policies`
2. Povolit **"Allow Copilot to browse the web"**
3. V sekci **"Allow requests to external domains"** přidat:
   ```
   *.kaloricketabulky.cz
   *.kupi.cz
   ```

---

## Testování scraperů

### Testování s GitHub Copilot

#### Test 1: Ověření přístupu k webům

V GitHub Copilot Chat zadejte:

```
Ověř, že můžeš přistupovat na www.kaloricketabulky.cz a načíst HTML strukturu 
hlavní stránky. Ukaž mi, jaké elementy tam jsou.
```

Copilot by měl:
1. Přistoupit na stránku
2. Načíst HTML
3. Popsat strukturu stránky

#### Test 2: Testování nutrition scraperu

```
@workspace Spusť fetch_nutrition_data.py s produktem "Kuřecí prsa" 
a ověř, že scraper správně parsuje nutriční hodnoty. 
Porovnej výsledky s reálnými daty na webu.
```

#### Test 3: Testování discount scraperu

```
@workspace Otestuj kupi_scraper.py - načti aktuální slevy z Lidlu 
a ověř, že ceny a produkty odpovídají tomu, co je aktuálně na www.kupi.cz
```

#### Test 4: Komplexní integrační test

```
@workspace Vytvoř komplexní test, který:
1. Vyhledá produkt "tvaroh" na kaloricketabulky.cz
2. Získá nutriční hodnoty
3. Vyhledá stejný produkt na kupi.cz
4. Zjistí aktuální ceny a slevy
5. Vytvoří report s porovnáním
```

### Automatizované testy

Můžete také vytvořit Python testy, které Copilot může spouštět:

```python
# tests/test_scrapers_with_real_data.py
import pytest
from fetch_nutrition_data import fetch_by_product_name
from src.scrapers.kupi_scraper import KupiCzScraper

@pytest.mark.integration
@pytest.mark.requires_web_access
def test_nutrition_scraper_real_data():
    """Test nutrition scraper with real data from kaloricketabulky.cz"""
    # This test requires web access
    data = fetch_by_product_name("Kuřecí prsa")
    
    assert data is not None
    assert 'product_name' in data
    assert 'macros' in data
    assert 'protein' in data['macros']
    
    # Verify protein content is reasonable for chicken
    protein_value = float(data['macros']['protein'].split()[0])
    assert 20 <= protein_value <= 35  # Chicken is typically 20-30g protein per 100g

@pytest.mark.integration
@pytest.mark.requires_web_access
def test_kupi_scraper_real_data():
    """Test Kupi.cz scraper with real data"""
    with KupiCzScraper() as scraper:
        products = scraper.get_current_discounts()
        
        # Should find at least some products
        assert len(products) > 0
        
        # Verify product structure
        first_product = products[0]
        assert hasattr(first_product, 'name')
        assert hasattr(first_product, 'discount_price')
        assert hasattr(first_product, 'store')
```

Spusťte testy:

```bash
# Spustit pouze integrační testy s webovým přístupem
pytest -m "requires_web_access" -v

# Copilot může spustit tyto testy a analyzovat výsledky
```

---

## Řešení problémů

### Problém 1: Copilot nemůže přistupovat na web

**Příznaky**:
- Copilot vrací chybu "I cannot access external websites"
- Scraper testy selhávají s "Network access denied"

**Řešení**:
1. Ověřte předplatné GitHub Copilot Pro
2. Zkontrolujte nastavení: https://github.com/settings/copilot
3. Ujistěte se, že je zaškrtnuto "Allow GitHub Copilot to access the web"
4. Restartujte VS Code / Codespaces

### Problém 2: Přístup blokován pro konkrétní domény

**Příznaky**:
- Copilot může přistupovat na jiné stránky, ale ne na kaloricketabulky.cz nebo kupi.cz
- Chyba "Access to this domain is not allowed"

**Řešení**:
1. Přidejte domény do whitelistu v nastavení organizace
2. Pro osobní účty: kontaktujte GitHub support
3. Alternativně použijte GitHub Codespaces, které mají méně restrikcí

### Problém 3: Scraper nefunguje s reálnými daty

**Příznaky**:
- Copilot přistupuje na web, ale scraper nevrací data
- Parsování HTML selhává

**Řešení**:
1. Zkontrolujte strukturu HTML na cílovém webu (může se změnit)
2. Použijte Copilot k analýze:
   ```
   Načti HTML z www.kaloricketabulky.cz/potraviny/kuřecí-prsa 
   a porovnej ho s CSS selektory v našem scraperu. 
   Co se změnilo?
   ```
3. Aktualizujte CSS selektory v scraperu podle aktuální struktury

### Problém 4: Rate limiting / blokování

**Příznaky**:
- První požadavek funguje, další jsou blokovány
- HTTP 429 nebo 403 chyby

**Řešení**:
1. Přidejte delays mezi požadavky:
   ```python
   import time
   time.sleep(2)  # 2 sekundy mezi požadavky
   ```
2. Použijte reálnější User-Agent (už je v kódu)
3. Respektujte robots.txt:
   ```
   @workspace Zkontroluj robots.txt na www.kupi.cz 
   a ověř, že náš scraper respektuje pravidla
   ```

### Problém 5: Copilot instrukce se neaplikují

**Příznaky**:
- Copilot nerozumí kontextu projektu
- Navrhuje nekonzistentní kód

**Řešení**:
1. Ověřte, že soubor je na správné cestě: `.github/copilot-instructions.md`
2. Soubor musí být commitnutý do repozitáře
3. Restartujte VS Code nebo reload Copilot extension
4. Použijte `@workspace` prefix pro kontextové dotazy

---

## Pokročilé použití

### Kontinuální monitoring scraperů

Můžete požádat Copilot o vytvoření monitoring skriptu:

```
@workspace Vytvoř skript, který každou hodinu:
1. Testuje oba scrapery s reálnými daty
2. Loguje, jestli fungují správně
3. Pošle notifikaci, pokud něco selže
4. Uloží výsledky do CSV pro analýzu
```

### Automatická aktualizace scraperů

Když se struktura webu změní:

```
@workspace Web kaloricketabulky.cz změnil strukturu HTML. 
Načti aktuální HTML produktové stránky, 
zjisti novou strukturu a uprav fetch_nutrition_data.py 
tak, aby fungoval s novou strukturou.
```

### Vytváření testovacích dat

```
@workspace Načti 10 různých produktů z kaloricketabulky.cz 
a vytvoř z nich mock data pro unit testy. 
Ulož je do tests/fixtures/nutrition_data.json
```

---

## Best Practices

### ✅ Doporučení

1. **Vždy testujte s reálnými daty** před nasazením do produkce
2. **Používejte delays** mezi požadavky (min. 2 sekundy)
3. **Cachujte výsledky** pro opakované dotazy
4. **Respektujte robots.txt** obou webů
5. **Monitorujte rate limiting** a přizpůsobte frekvenci požadavků
6. **Verzujte strukturu dat** - weby se mohou měnit
7. **Logujte všechny requesty** pro debugging

### ❌ Co nedělat

1. ❌ Nepřetěžujte servery - neklaďte desítky requestů za sekundu
2. ❌ Neukládejte citlivá data z webů bez povolení
3. ❌ Neobcházejte CAPTCHA nebo anti-bot ochranu
4. ❌ Neignorujte rate limiting chyby
5. ❌ Nepředpokládejte, že HTML struktura zůstane stejná

---

## Reference

### Oficiální dokumentace

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Copilot Pro Features](https://github.com/features/copilot)
- [Copilot Instructions Format](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)

### Relevantní soubory v tomto repozitáři

- `fetch_nutrition_data.py` - Scraper pro kaloricketabulky.cz
- `src/scrapers/kupi_scraper.py` - Scraper pro kupi.cz
- `test_kupi_scraper.py` - Unit testy pro Kupi scraper
- `docs/technical/KUPI_INTEGRATION.md` - Dokumentace Kupi integrace
- `requirements.txt` - Python závislosti

### Externí odkazy

- [www.kaloricketabulky.cz](https://www.kaloricketabulky.cz/)
- [www.kupi.cz](https://www.kupi.cz/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://requests.readthedocs.io/)

---

## Kontakt a podpora

Pokud máte problémy s konfigurací:

1. Zkontrolujte [GitHub Copilot Status](https://www.githubstatus.com/)
2. Přečtěte si [Troubleshooting Guide](https://docs.github.com/en/copilot/troubleshooting-github-copilot)
3. Otevřete issue v tomto repozitáři
4. Kontaktujte GitHub Support pro problémy s předplatným

---

## Changelog

- **2026-01-18**: Vytvoření návodu pro GitHub Copilot Pro+ web access
- Přidána konfigurace pro kaloricketabulky.cz a kupi.cz
- Přidány testovací příklady a troubleshooting

---

**Autor**: Foodler Project Team  
**Poslední aktualizace**: 18. ledna 2026  
**Licence**: MIT
