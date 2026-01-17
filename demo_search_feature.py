#!/usr/bin/env python3
"""
Demonstration of the product name search functionality
This shows how the new feature works with mock data
"""

def demo_product_search():
    """Demonstrate the product name search feature"""
    
    print("=" * 70)
    print("PRODUCT NAME SEARCH FEATURE DEMONSTRATION")
    print("=" * 70)
    
    print("\n📋 Overview:")
    print("  You can now search for products by name without needing the URL!")
    
    print("\n🔍 How it works:")
    print("  1. You provide a product name (e.g., 'Tvaroh tučný Pilos')")
    print("  2. Script searches kaloricketabulky.cz for matching products")
    print("  3. Shows all results found")
    print("  4. Automatically fetches data from the first result")
    
    print("\n💻 Command Line Usage:")
    print("  # Search by product name")
    print("  python fetch_nutrition_data.py \"Tvaroh tučný Pilos\"")
    print("")
    print("  # Still works with URLs")
    print("  python fetch_nutrition_data.py \"https://www.kaloricketabulky.cz/...\"")
    
    print("\n🐍 Python Code Usage:")
    print("  from fetch_nutrition_data import fetch_by_product_name")
    print("")
    print("  # Search and fetch in one call")
    print("  data = fetch_by_product_name('Tvaroh tučný Pilos')")
    print("  print(data['macros']['protein'])  # e.g., '12 g'")
    
    print("\n📦 Example Output:")
    print("  Searching for product: Tvaroh tučný Pilos")
    print("  ------------------------------------------------------------")
    print("  Found 3 result(s):")
    print("    1. Tvaroh tučný Pilos")
    print("    2. Tvaroh Pilos")
    print("    3. Tvaroh polotučný Pilos")
    print("")
    print("  Using first result: Tvaroh tučný Pilos")
    print("  {")
    print("    'product_name': 'Tvaroh tučný Pilos',")
    print("    'macros': {")
    print("      'calories': '145 kcal',")
    print("      'protein': '12 g',")
    print("      'carbohydrates': '3 g',")
    print("      'fat': '9 g'")
    print("    }")
    print("  }")
    
    print("\n✨ Benefits:")
    print("  ✓ No need to find the URL manually")
    print("  ✓ Quick lookups by product name")
    print("  ✓ Perfect for diet tracking")
    print("  ✓ Works in both CLI and code")
    
    print("\n🔧 Technical Details:")
    print("  - Uses kaloricketabulky.cz search API")
    print("  - URL encoding handles Czech characters (č, ř, š, etc.)")
    print("  - Returns top 10 matches")
    print("  - Automatically selects best match")
    print("  - Same caching support as URL-based fetching")
    
    print("\n📝 Integration with example_usage.py:")
    print("  from example_usage import get_nutrition_data")
    print("")
    print("  # Works with both URLs and product names")
    print("  data1 = get_nutrition_data('Tvaroh tučný Pilos', use_cache=True)")
    print("  data2 = get_nutrition_data('https://...', use_cache=True)")
    
    print("\n" + "=" * 70)
    print("READY TO USE!")
    print("=" * 70)
    print("\nTry it now:")
    print('  python fetch_nutrition_data.py "Tvaroh tučný Pilos"')
    print("")


if __name__ == "__main__":
    demo_product_search()
