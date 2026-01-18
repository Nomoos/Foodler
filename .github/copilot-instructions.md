# GitHub Copilot Instructions for Foodler Project

## Project Overview

This is a family diet planning system focused on ketogenic/low-carb nutrition with meal planning and shopping optimization for a Czech family.

**Primary Goals**:
- Support weight loss through protein-first, low-carb diet (keto/low-carb approach)
- Track macronutrients (protein, carbs, fats, calories)
- Plan meals for multiple family members with different needs
- Optimize grocery shopping with discount tracking
- Fetch nutritional data from Czech databases

## Web Scrapers - IMPORTANT

This project includes web scrapers that require internet access to function properly. When testing or developing these scrapers, you need access to real web data.

### 1. Nutrition Data Scraper (kaloricketabulky.cz)

**Purpose**: Fetch nutritional information for Czech food items  
**File**: `fetch_nutrition_data.py`  
**Target URL**: https://www.kaloricketabulky.cz/  
**Access Required**: YES - for testing and validation

**Key Functions**:
```python
# Search for products by name (Czech language)
search_product(product_name: str) -> List[Dict]

# Extract nutrition data from product page
fetch_nutrition_data(url: str) -> Optional[Dict]

# Combined search and fetch
fetch_by_product_name(product_name: str) -> Optional[Dict]
```

**Test Examples**:
```python
# Test with real data
data = fetch_by_product_name("Tvaroh tučný")
data = fetch_by_product_name("Kuřecí prsa")
data = fetch_nutrition_data("https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend")
```

**Expected Output Structure**:
```json
{
  "product_name": "Whey Protein Chocolate & Cocoa 100% - Nutrend",
  "url": "https://www.kaloricketabulky.cz/...",
  "macros": {
    "calories": "380 kcal",
    "protein": "78 g",
    "carbohydrates": "6 g",
    "fat": "6 g",
    "fiber": "2 g",
    "sugar": "5 g"
  }
}
```

### 2. Discount Scraper (kupi.cz)

**Purpose**: Find discounts and deals from Czech supermarkets (Lidl, Kaufland, Albert, Penny, etc.)  
**File**: `src/scrapers/kupi_scraper.py`  
**Target URL**: https://www.kupi.cz/  
**Access Required**: YES - for testing and validation

**Key Functions**:
```python
# Get current discounts with optional filters
get_current_discounts(category: Optional[str] = None, store: Optional[str] = None) -> List[Product]

# Search for specific products
search_products(query: str) -> List[Product]

# Get list of available stores
get_stores() -> List[dict]
```

**Test Examples**:
```python
scraper = KupiCzScraper()
products = scraper.get_current_discounts(category='potraviny')
results = scraper.search_products("kuřecí prsa")
stores = scraper.get_stores()
```

**Expected Output Structure**:
```python
Product(
    name="Kuřecí prsa",
    original_price=150.0,
    discount_price=99.90,
    discount_percentage=33.4,
    store="Lidl",
    valid_from=None,
    valid_until=None,
    image_url="https://...",
    product_url="https://...",
    category="Maso"
)
```

## Testing Guidelines

### When testing scrapers with web access:

1. **Always verify web access is available** before suggesting scraper tests
2. **Use realistic test queries** - Czech product names like "kuřecí prsa", "tvaroh", "sýr eidam"
3. **Handle failures gracefully** - websites may be temporarily unavailable or have changed structure
4. **Add delays between requests** (2-3 seconds minimum) to avoid rate limiting:
   ```python
   import time
   time.sleep(2)  # Delay between requests
   ```
5. **Check robots.txt compliance**:
   - https://www.kaloricketabulky.cz/robots.txt
   - https://www.kupi.cz/robots.txt
6. **Validate data structure** - ensure scrapers return expected format
7. **Test with multiple examples** - don't rely on just one product

### Integration Testing Approach:

When asked to test scrapers:
1. First, check if web access is available
2. Start with a simple query to verify connectivity
3. Test core functionality with 2-3 different products
4. Verify data structure matches expected format
5. Check for edge cases (missing data, special characters)
6. Report any parsing issues or structure changes

## Code Style & Conventions

### Language
- **Code comments**: Czech language preferred (this is a Czech project)
- **Variable names**: English
- **Documentation**: Czech for user-facing docs, English for technical docs
- **Commit messages**: Can be either Czech or English

### Python Style
- Follow **PEP 8** style guide
- Use **type hints** for all function parameters and return values
- Include **docstrings** for all public functions (Czech is preferred)
- Use **dataclasses** for data structures (see `modely/product.py`)
- Handle **Czech characters** properly (UTF-8 encoding always)

### Example:
```python
def fetch_nutrition_data(url: str) -> Optional[Dict]:
    """
    Stáhne nutriční data z kaloricketabulky.cz
    
    Args:
        url: Plná URL produktové stránky
        
    Returns:
        Slovník s nutričními daty nebo None při chybě
    """
    # Implementation...
```

## Project Structure

```
Foodler/
├── docs/                   # 📚 Dokumentace
│   ├── getting-started/    # Návody a quickstart
│   ├── diet-plans/         # Dietní plány
│   ├── meal-planning/      # Plánování jídel
│   ├── health/             # Zdraví a metabolismus
│   └── technical/          # Technická dokumentace
├── osoby/                  # 👥 Osobní profily (Roman, Pája, Kubík)
├── potraviny/              # 🥩 Databáze potravin
├── jidla/                  # 🍽️ Recepty a hotová jídla
├── nakup/                  # 🛒 Nákupní seznamy
├── lednice/                # 🧊 Správa zásob
├── data/                   # 📊 Datové soubory
├── modely/                 # 🔧 Datové modely
└── src/                    # 💻 Zdrojový kód
    ├── assistants/         # Nákupní asistenti
    ├── scrapers/           # Web scrapers
    └── planners/           # Plánovače jídelníčků
```

## Diet Context - Important for Understanding Requirements

### Target Users

**Roman (Romča)**:
- Váha: 134.2 kg, Výška: 183 cm, Věk: 34 let
- Denní cíl: **2001 kcal**, **140g+ bílkovin**, **max 70g sacharidů**
- Diet: Ketogenic/low-carb, protein-first approach

**Pája (Pavla)**:
- Váha: 77.3 kg, Výška: 169 cm
- Denní cíl: **1508 kcal**, **92g bílkovin**, **max 60g sacharidů**
- Diet: Ketogenic/low-carb

**Kubík**:
- Věk: 4.5 let, Váha: 18 kg
- Denní cíl: **1400 kcal**, **19g bílkovin**, **130g sacharidů**
- Důraz na vitamin A (má brýle - problémy se zrakem)

### Key Dietary Priorities

1. **Protein first** - Always prioritize protein sources
2. **Low carb** - Maximum 60-70g carbs for adults (keto approach)
3. **Healthy fats** - Focus on quality fat sources
4. **Fiber** - At least 20g daily
5. **Budget optimization** - Use scrapers to find discounts

### Preferred Foods (for scraper testing)

**High Priority**:
- Maso: kuřecí prsa, krůtí prsa, vepřové maso
- Ryby: losos, makrela, tuňák
- Vejce
- Mléčné: tvaroh, sýr, řecký jogurt
- Zelenina: brokolice, špenát, salát, cuketa
- Tuky: avokádo, olivový olej, ořechy

**Avoid/Limit**:
- Cukr a sladkosti
- Bílé pečivo
- Těstoviny
- Brambory
- Rýže (kromě Kubíka)

## When Suggesting Code Changes

### Principles to Follow:

1. **Single Responsibility** - Keep scraper logic separate from business logic
2. **Use existing models** - Utilize `Product` dataclass from `modely/product.py`
3. **Error handling** - Always handle network errors, timeouts, parsing failures
4. **Logging** - Use the logging patterns already in place
5. **Type safety** - Use type hints consistently
6. **Testing** - Suggest unit tests with mock data AND integration tests with real data

### Example Pattern:

```python
from typing import Optional, List
import logging
from modely.product import Product

logger = logging.getLogger(__name__)

def scrape_products(category: str) -> List[Product]:
    """
    Stáhne produkty z dané kategorie.
    
    Args:
        category: Název kategorie
        
    Returns:
        Seznam Product objektů
    """
    try:
        # Scraping logic
        products = []
        # ... scraping ...
        logger.info(f"Nalezeno {len(products)} produktů")
        return products
    except Exception as e:
        logger.error(f"Chyba při scrapování: {e}")
        return []
```

## Testing with Real Web Data

### When I have web access:

If you ask me to test scrapers and I have web access enabled, I will:

1. **Verify connectivity** to target websites
2. **Fetch real data** from kaloricketabulky.cz or kupi.cz
3. **Validate scraper output** against actual website content
4. **Check data structure** matches expected format
5. **Test edge cases** with different product types
6. **Report issues** if website structure has changed
7. **Suggest fixes** if parsing fails

### Example Test Workflow:

```
User asks: "Test the nutrition scraper with real data"

My response would include:
1. Accessing https://www.kaloricketabulky.cz/
2. Testing search for "kuřecí prsa"
3. Extracting nutrition data
4. Comparing with scraper output
5. Reporting: ✅ Works / ❌ Needs fixes
```

## Important Files to Know

### Scrapers:
- `fetch_nutrition_data.py` - Main nutrition data scraper
- `src/scrapers/kupi_scraper.py` - Discount scraper
- `test_kupi_scraper.py` - Unit tests for Kupi scraper

### Data Models:
- `modely/product.py` - Product dataclass for scraped data

### Documentation:
- `docs/technical/GITHUB_COPILOT_WEB_ACCESS.md` - Guide for configuring web access
- `docs/technical/KUPI_INTEGRATION.md` - Kupi.cz integration documentation
- `README.md` - Main project documentation (Czech)
- `README_EN.md` - English documentation

### Configuration:
- `requirements.txt` - Python dependencies (requests, beautifulsoup4, lxml)

## Dependencies

Key libraries used:
- **requests** - HTTP requests for web scraping
- **beautifulsoup4** - HTML parsing
- **lxml** - Fast HTML parser
- **dataclasses** - For structured data (Product model)

## Ethical Scraping Guidelines

**Always follow these rules when suggesting scraper code:**

1. ✅ Respect `robots.txt` of target websites
2. ✅ Add delays between requests (minimum 2 seconds)
3. ✅ Use realistic User-Agent headers
4. ✅ Handle rate limiting gracefully (HTTP 429)
5. ✅ Cache results to minimize repeated requests
6. ✅ Only scrape publicly available data
7. ❌ Never bypass CAPTCHA or authentication
8. ❌ Never overload servers with rapid requests
9. ❌ Never scrape personal or sensitive data

## Common Tasks

### Task: Test nutrition scraper
```python
# If you have web access
from fetch_nutrition_data import fetch_by_product_name

# Test with real product
data = fetch_by_product_name("Kuřecí prsa")
print(data)

# Verify structure
assert data is not None
assert 'macros' in data
assert 'protein' in data['macros']
```

### Task: Test discount scraper
```python
from src.scrapers.kupi_scraper import KupiCzScraper

# Test with real data
with KupiCzScraper() as scraper:
    products = scraper.get_current_discounts(store='lidl')
    print(f"Found {len(products)} products")
    for p in products[:5]:
        print(f"- {p.name}: {p.discount_price} Kč")
```

### Task: Find keto-friendly deals
```python
from src.scrapers.kupi_scraper import KupiCzScraper

keto_keywords = ["kuřecí", "krůtí", "losos", "vejce", "sýr", "tvaroh"]

with KupiCzScraper() as scraper:
    keto_deals = []
    for keyword in keto_keywords:
        products = scraper.search_products(keyword)
        keto_deals.extend(products)
    
    # Sort by discount
    keto_deals.sort(key=lambda p: p.discount_percentage or 0, reverse=True)
    
    print("Top 10 Keto Deals:")
    for product in keto_deals[:10]:
        print(f"{product.name}: {product.discount_price} Kč ({product.discount_percentage}% off)")
```

## Summary

This project helps a Czech family with:
- 🎯 Weight loss through keto/low-carb diet
- 🍗 High-protein meal planning
- 💰 Budget optimization via discount tracking
- 📊 Nutrition data from Czech databases

**Key websites for scraping**:
- https://www.kaloricketabulky.cz/ - Nutrition database
- https://www.kupi.cz/ - Discount aggregator

When testing these scrapers, **you need web access enabled** to fetch real data and validate that the scrapers work correctly with current website structures.
