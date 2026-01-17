#!/usr/bin/env python3
"""
Example script showing how to work with nutrition data,
including caching for offline use.
"""

import json
import os
from fetch_nutrition_data import fetch_nutrition_data


def save_nutrition_data(data, filename="nutrition_cache.json"):
    """Save nutrition data to a JSON file"""
    cache_dir = os.path.dirname(filename)
    if cache_dir and not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    # Load existing cache if it exists
    cache = {}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    
    # Add new data
    url = data.get('url', 'unknown')
    cache[url] = data
    
    # Save updated cache
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)
    
    print(f"Data saved to {filename}")


def load_nutrition_data(url, filename="nutrition_cache.json"):
    """Load nutrition data from cache"""
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'r', encoding='utf-8') as f:
        cache = json.load(f)
    
    return cache.get(url)


def get_nutrition_data(url, use_cache=True, cache_file="nutrition_cache.json"):
    """
    Get nutrition data - try cache first, then fetch from web
    
    Args:
        url: URL to fetch data from
        use_cache: Whether to use cached data
        cache_file: Path to cache file
    
    Returns:
        Nutrition data dictionary or None
    """
    # Try cache first if enabled
    if use_cache:
        data = load_nutrition_data(url, cache_file)
        if data:
            print(f"Loaded from cache: {url}")
            return data
    
    # Fetch from web
    print(f"Fetching from web: {url}")
    data = fetch_nutrition_data(url)
    
    # Save to cache if successful
    if data and use_cache:
        save_nutrition_data(data, cache_file)
    
    return data


def calculate_serving(nutrition_data, serving_size_g, per_100g=True):
    """
    Calculate nutrition for a specific serving size
    
    Args:
        nutrition_data: Dictionary with nutrition data
        serving_size_g: Serving size in grams
        per_100g: Whether the data is per 100g (default True)
    
    Returns:
        Dictionary with calculated values for the serving
    """
    if not per_100g:
        return nutrition_data  # Already in serving size
    
    factor = serving_size_g / 100
    serving_data = {
        'serving_size_g': serving_size_g,
        'macros': {}
    }
    
    macros = nutrition_data.get('macros', {})
    for key, value in macros.items():
        # Extract numeric value
        try:
            numeric_value = float(value.split()[0])
            unit = ' '.join(value.split()[1:])
            calculated_value = numeric_value * factor
            serving_data['macros'][key] = f"{calculated_value:.1f} {unit}"
        except (ValueError, IndexError):
            serving_data['macros'][key] = value
    
    return serving_data


def example_usage():
    """Example of how to use the nutrition data fetcher"""
    
    # URLs for products from the diet plan
    urls = [
        "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend",
        # Add more URLs as needed
    ]
    
    print("Nutrition Data Fetcher - Example Usage")
    print("=" * 70)
    
    for url in urls:
        print(f"\nProcessing: {url}")
        print("-" * 70)
        
        # Get data (will use cache if available)
        data = get_nutrition_data(url, use_cache=True)
        
        if data:
            print(f"\nProduct: {data.get('product_name', 'Unknown')}")
            
            # Show data per 100g
            print("\nPer 100g:")
            for key, value in data.get('macros', {}).items():
                print(f"  {key.capitalize()}: {value}")
            
            # Calculate for 30g serving (as used in diet plan)
            serving = calculate_serving(data, 30)
            print(f"\nPer {serving['serving_size_g']}g serving:")
            for key, value in serving.get('macros', {}).items():
                print(f"  {key.capitalize()}: {value}")
        else:
            print("Failed to fetch data")
    
    print("\n" + "=" * 70)
    print("Example completed!")


if __name__ == "__main__":
    example_usage()
