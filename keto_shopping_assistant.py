#!/usr/bin/env python3
"""
Example: Keto Diet Shopping Assistant

This script demonstrates how to use the Kupi.cz scraper to find
discounted products that fit the Foodler keto diet plan.
"""

from kupi_scraper import KupiCzScraper, Product
from typing import List, Dict
import time


# Keto-friendly food categories based on Foodler diet plan
KETO_FOODS = {
    'high_protein': {
        'keywords': ['kuřecí', 'krůtí', 'hovězí', 'vepřové', 'ryba', 'losos', 'tuňák', 'vejce'],
        'description': 'High Protein Sources (Chicken, Turkey, Beef, Fish, Eggs)',
        'target_macros': {'protein': 'high', 'carbs': 'low', 'fat': 'medium'}
    },
    'dairy': {
        'keywords': ['sýr', 'tvaroh', 'jogurt', 'máslo', 'smetana'],
        'description': 'Dairy Products (Cheese, Cottage Cheese, Yogurt)',
        'target_macros': {'protein': 'medium', 'carbs': 'low', 'fat': 'high'}
    },
    'vegetables': {
        'keywords': ['brokolice', 'špenát', 'salát', 'cuketa', 'paprika', 'rajčata'],
        'description': 'Low-Carb Vegetables',
        'target_macros': {'protein': 'low', 'carbs': 'low', 'fat': 'low'}
    },
    'healthy_fats': {
        'keywords': ['avokádo', 'olivový olej', 'ořechy', 'mandle', 'vlašské ořechy'],
        'description': 'Healthy Fats (Avocado, Olive Oil, Nuts)',
        'target_macros': {'protein': 'low', 'carbs': 'low', 'fat': 'high'}
    },
    'supplements': {
        'keywords': ['chia', 'psyllium', 'protein', 'omega'],
        'description': 'Supplements and Seeds',
        'target_macros': {'protein': 'varies', 'carbs': 'varies', 'fat': 'varies'}
    }
}


def find_keto_deals(scraper: KupiCzScraper, category: str, keywords: List[str], 
                    max_results: int = 5) -> List[Product]:
    """
    Find discounted keto-friendly products.
    
    Args:
        scraper: KupiCzScraper instance
        category: Category name
        keywords: List of search keywords
        max_results: Maximum number of results per keyword
        
    Returns:
        List of Product objects
    """
    print(f"\n🔍 Searching for {category}...")
    all_products = []
    
    for keyword in keywords:
        print(f"  Searching: {keyword}...", end=' ')
        try:
            products = scraper.search_products(keyword)
            if products:
                print(f"✓ Found {len(products)}")
                all_products.extend(products[:max_results])
            else:
                print("✗ No results")
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Remove duplicates and sort by discount
    unique_products = {p.name: p for p in all_products}.values()
    sorted_products = sorted(
        unique_products, 
        key=lambda p: p.discount_percentage or 0, 
        reverse=True
    )
    
    return list(sorted_products)


def display_products(products: List[Product], title: str, max_display: int = 10):
    """Display products in a formatted table."""
    if not products:
        print(f"\n{title}")
        print("  No products found.")
        return
    
    print(f"\n{title}")
    print("=" * 80)
    print(f"{'#':<3} {'Product':<35} {'Price':<12} {'Discount':<10} {'Store':<15}")
    print("-" * 80)
    
    for i, product in enumerate(products[:max_display], 1):
        name = product.name[:32] + "..." if len(product.name) > 35 else product.name
        price = f"{product.discount_price:.2f} Kč"
        discount = f"{product.discount_percentage:.0f}%" if product.discount_percentage else "N/A"
        store = product.store[:12]
        
        print(f"{i:<3} {name:<35} {price:<12} {discount:<10} {store:<15}")


def generate_shopping_list(keto_deals: Dict[str, List[Product]]) -> None:
    """Generate a shopping list from the best deals."""
    print("\n" + "=" * 80)
    print("📋 RECOMMENDED SHOPPING LIST FOR KETO DIET")
    print("=" * 80)
    
    for category, products in keto_deals.items():
        if not products:
            continue
        
        info = KETO_FOODS.get(category, {})
        description = info.get('description', category)
        
        print(f"\n{description}:")
        for product in products[:3]:  # Top 3 from each category
            discount_info = f" (-{product.discount_percentage:.0f}%)" if product.discount_percentage else ""
            print(f"  ☑ {product.name}")
            print(f"     {product.discount_price:.2f} Kč at {product.store}{discount_info}")


def calculate_weekly_budget(keto_deals: Dict[str, List[Product]]) -> None:
    """Calculate estimated weekly budget based on deals."""
    print("\n" + "=" * 80)
    print("💰 WEEKLY BUDGET ESTIMATION")
    print("=" * 80)
    
    # Estimate weekly needs (7 days, 6 meals/day)
    weekly_needs = {
        'high_protein': 7,   # 7 protein sources per week (1 per day for main meals)
        'dairy': 3,          # 3 dairy items
        'vegetables': 4,     # 4 vegetable packs
        'healthy_fats': 2,   # 2 fat sources
        'supplements': 2     # 2 supplement items
    }
    
    total_cost = 0
    print("\nCategory               Items  Avg Price    Subtotal")
    print("-" * 60)
    
    for category, products in keto_deals.items():
        if not products or category not in weekly_needs:
            continue
        
        items_needed = weekly_needs[category]
        avg_price = sum(p.discount_price for p in products[:items_needed]) / min(len(products), items_needed)
        subtotal = avg_price * items_needed
        total_cost += subtotal
        
        info = KETO_FOODS.get(category, {})
        description = info.get('description', category)[:20]
        
        print(f"{description:<20} {items_needed:>5}  {avg_price:>8.2f} Kč  {subtotal:>8.2f} Kč")
    
    print("-" * 60)
    print(f"{'TOTAL WEEKLY COST:':<20}              {total_cost:>8.2f} Kč")
    print(f"\nEstimated daily cost: {total_cost/7:.2f} Kč")


def main():
    """Main function to run the keto shopping assistant."""
    print("=" * 80)
    print("🥑 FOODLER KETO DIET SHOPPING ASSISTANT")
    print("=" * 80)
    print("\nThis tool helps you find discounted keto-friendly products from Czech supermarkets")
    print("based on the Foodler diet plan requirements:")
    print("  • Daily: 2000 kcal, 140g+ protein, <70g carbs, 129g fat")
    print("  • 6 meals per day")
    print("  • Ketogenic/Low-carb approach")
    
    try:
        with KupiCzScraper() as scraper:
            print("\n📍 Available stores:")
            stores = scraper.get_stores()
            for store in stores:
                print(f"  • {store['name']}")
            
            # Collect deals for each category
            keto_deals = {}
            
            for category, info in KETO_FOODS.items():
                products = find_keto_deals(
                    scraper, 
                    info['description'], 
                    info['keywords'],
                    max_results=5
                )
                keto_deals[category] = products
                
                # Display results
                display_products(
                    products, 
                    f"\n🏆 Top Deals: {info['description']}",
                    max_display=5
                )
            
            # Generate shopping list
            generate_shopping_list(keto_deals)
            
            # Calculate budget
            calculate_weekly_budget(keto_deals)
            
            print("\n" + "=" * 80)
            print("✅ Shopping assistant completed!")
            print("\nNote: Prices and availability may vary. Always check product details")
            print("and nutritional information before purchasing.")
            print("\nFor more information, see KUPI_INTEGRATION.md")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\nThis might happen if:")
        print("  • You're not connected to the internet")
        print("  • The website structure has changed")
        print("  • The website is blocking automated requests")
        print("\nThe scraper structure is ready but may need customization")
        print("based on the actual HTML structure of kupi.cz")


if __name__ == "__main__":
    main()
