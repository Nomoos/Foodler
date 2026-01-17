# Kupi.cz Integration Guide

## Overview

This document explains how to use the Kupi.cz scraper to fetch current discounts and products from Czech supermarkets.

**Kupi.cz** is a Czech discount aggregator website that collects promotional offers from various supermarkets including Lidl, Kaufland, Albert, Penny, Billa, and others. This integration helps the Foodler project by:

- Finding discounted products that fit the dietary requirements
- Tracking prices across different stores
- Planning meals based on current offers
- Optimizing grocery shopping budget

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from kupi_scraper import KupiCzScraper

# Create scraper instance
with KupiCzScraper() as scraper:
    # Fetch current discounts
    products = scraper.get_current_discounts()
    
    # Display products
    for product in products:
        print(product)
```

### Search for Specific Products

```python
with KupiCzScraper() as scraper:
    # Search for specific items
    milk_products = scraper.search_products("mléko")
    protein_products = scraper.search_products("kuřecí")
    
    for product in milk_products:
        print(f"{product.name}: {product.discount_price} Kč at {product.store}")
```

### Filter by Store

```python
with KupiCzScraper() as scraper:
    # Get discounts from specific store
    lidl_discounts = scraper.get_current_discounts(store='lidl')
    
    # Get list of all available stores
    stores = scraper.get_stores()
    print(stores)
```

### Filter by Category

```python
with KupiCzScraper() as scraper:
    # Get discounts in specific category
    food_discounts = scraper.get_current_discounts(category='potraviny')
    beverage_discounts = scraper.get_current_discounts(category='napoje')
```

## Product Data Structure

Each product contains the following information:

```python
@dataclass
class Product:
    name: str                           # Product name
    original_price: Optional[float]     # Original price in CZK
    discount_price: float               # Discounted price in CZK
    discount_percentage: Optional[float] # Discount percentage
    store: str                          # Store name (e.g., "Lidl", "Kaufland")
    valid_from: Optional[datetime]      # Discount start date
    valid_until: Optional[datetime]     # Discount end date
    image_url: Optional[str]            # Product image URL
    product_url: Optional[str]          # Link to product details
    category: Optional[str]             # Product category
```

## Integration with Foodler Diet Plan

### Finding Keto-Friendly Products

```python
from kupi_scraper import KupiCzScraper

# Keywords for keto-friendly products
keto_keywords = [
    "kuřecí",      # chicken
    "maso",        # meat
    "ryba",        # fish
    "vejce",       # eggs
    "sýr",         # cheese
    "avokádo",     # avocado
    "olivy",       # olives
]

with KupiCzScraper() as scraper:
    keto_products = []
    for keyword in keto_keywords:
        products = scraper.search_products(keyword)
        keto_products.extend(products)
    
    # Sort by discount percentage
    keto_products.sort(key=lambda p: p.discount_percentage or 0, reverse=True)
    
    # Show best deals
    print("Top 10 Keto-Friendly Deals:")
    for product in keto_products[:10]:
        print(f"{product.name}: {product.discount_price} Kč ({product.discount_percentage}% off)")
```

### Weekly Meal Planning

```python
from kupi_scraper import KupiCzScraper

def find_weekly_deals():
    """Find best deals for weekly meal planning."""
    
    with KupiCzScraper() as scraper:
        # Categories needed for the diet plan
        categories = {
            'protein': ['kuřecí', 'krůtí', 'ryba', 'vejce'],
            'dairy': ['sýr', 'jogurt', 'tvaroh'],
            'vegetables': ['brokolice', 'špenát', 'salát'],
            'healthy_fats': ['avokádo', 'ořechy', 'olivový olej']
        }
        
        weekly_plan = {}
        
        for category, keywords in categories.items():
            products = []
            for keyword in keywords:
                results = scraper.search_products(keyword)
                products.extend(results)
            
            # Sort by best value (highest discount)
            products.sort(key=lambda p: p.discount_percentage or 0, reverse=True)
            weekly_plan[category] = products[:5]  # Top 5 deals per category
        
        return weekly_plan

# Use in meal planning
weekly_deals = find_weekly_deals()
for category, products in weekly_deals.items():
    print(f"\n{category.upper()} - Best Deals:")
    for product in products:
        print(f"  {product}")
```

## Customization

### Adjusting HTML Parsers

The scraper includes template parsing logic that may need customization based on the actual HTML structure of kupi.cz. To customize:

1. Inspect the website's HTML structure using browser developer tools
2. Update the CSS selectors in `_parse_products()` and `_extract_product_info()` methods
3. Test with small samples before running full scrapes

Example customization:

```python
def _parse_products(self, soup: BeautifulSoup) -> List[Product]:
    # Update these selectors based on actual site structure
    product_elements = soup.find_all('div', class_='actual-product-class')
    
    for elem in product_elements:
        # Customize extraction logic here
        pass
```

### Adding New Features

You can extend the scraper with additional methods:

```python
class KupiCzScraper:
    def get_weekly_leaflets(self):
        """Fetch weekly promotional leaflets."""
        # Implementation here
        pass
    
    def compare_prices(self, product_name: str) -> Dict[str, float]:
        """Compare prices across stores."""
        # Implementation here
        pass
```

## Error Handling

The scraper includes comprehensive error handling:

- Network errors: Logs error and returns empty list
- Parsing errors: Skips problematic items, continues processing
- Timeout handling: Configurable timeout (default 30 seconds)

```python
# Custom timeout
scraper = KupiCzScraper(timeout=60)

# Check for successful fetch
products = scraper.get_current_discounts()
if not products:
    print("No products found - check logs for details")
```

## Rate Limiting and Ethics

**Important Notes:**

1. **Respect robots.txt**: Always check the website's robots.txt file
2. **Rate limiting**: Add delays between requests to avoid overloading the server
3. **Caching**: Cache results to minimize repeated requests
4. **User-Agent**: Uses realistic browser headers
5. **Terms of Service**: Ensure compliance with website's terms

Example with rate limiting:

```python
import time

with KupiCzScraper() as scraper:
    stores = ['lidl', 'kaufland', 'albert']
    all_products = []
    
    for store in stores:
        products = scraper.get_current_discounts(store=store)
        all_products.extend(products)
        time.sleep(2)  # 2 second delay between requests
```

## Troubleshooting

### Common Issues

**Issue**: No products returned
- **Solution**: Website structure may have changed. Update CSS selectors.

**Issue**: Connection timeout
- **Solution**: Increase timeout parameter or check network connectivity.

**Issue**: 403 Forbidden error
- **Solution**: Website may be blocking scrapers. Consider:
  - Adding delays between requests
  - Using residential proxies
  - Contacting website owner for API access

**Issue**: Incorrect price parsing
- **Solution**: Check Czech price format (comma as decimal separator)

### Debug Mode

Enable detailed logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Now run scraper with detailed logs
with KupiCzScraper() as scraper:
    products = scraper.get_current_discounts()
```

## Running the Example

Run the included example:

```bash
python kupi_scraper.py
```

This will:
1. Display available stores
2. Fetch current discounts
3. Show sample search results

## Future Enhancements

Potential improvements:

- [ ] Add async support for faster scraping
- [ ] Implement caching mechanism
- [ ] Add database storage for price history
- [ ] Create price tracking and alerts
- [ ] Add visualization of price trends
- [ ] Integrate with meal planning system
- [ ] Support for multiple regions
- [ ] Mobile app notifications for deals

## Support for Foodler Diet Goals

The scraper specifically supports the Foodler project's dietary requirements:

- **Protein sources**: Chicken, turkey, fish, eggs
- **Low-carb foods**: Focus on meat, dairy, vegetables
- **Healthy fats**: Avocado, nuts, olive oil, fatty fish
- **Fiber sources**: Chia seeds, vegetables, psyllium

By tracking prices and discounts, it helps maintain the 2000 kcal daily plan while optimizing costs.

## License

This scraper is part of the Foodler project and intended for personal use in meal planning and budget optimization.

## Contact

For issues or questions about the scraper, please open an issue in the Foodler repository.
