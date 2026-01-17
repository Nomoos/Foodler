#!/usr/bin/env python3
"""
Script to fetch nutritional data from kaloricketabulky.cz

This script fetches and parses nutritional information from Czech nutrition database
for products like whey protein and other food items.
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
from typing import Dict, Optional


def fetch_nutrition_data(url: str) -> Optional[Dict]:
    """
    Fetch nutritional data from kaloricketabulky.cz URL
    
    Args:
        url: Full URL to the product page on kaloricketabulky.cz
        
    Returns:
        Dictionary containing nutritional information or None if failed
    """
    try:
        # Set headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the webpage
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract product name
        product_name = None
        h1_tag = soup.find('h1')
        if h1_tag:
            product_name = h1_tag.get_text(strip=True)
        
        # Initialize nutrition data dictionary
        nutrition_data = {
            'product_name': product_name,
            'url': url,
            'macros': {},
            'vitamins': {},
            'minerals': {}
        }
        
        # Find nutrition table - typically in a table with class containing 'nutritional' or 'tabulka'
        # Czech sites often use specific table structures
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    # Extract nutrient name and value
                    nutrient = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    
                    # Map common Czech terms to English
                    nutrient_lower = nutrient.lower()
                    
                    # Macros
                    if 'energie' in nutrient_lower or 'kalorie' in nutrient_lower:
                        nutrition_data['macros']['calories'] = value
                    elif 'bílkovin' in nutrient_lower or 'protein' in nutrient_lower:
                        nutrition_data['macros']['protein'] = value
                    elif 'sacharid' in nutrient_lower or 'carbohydrate' in nutrient_lower:
                        nutrition_data['macros']['carbohydrates'] = value
                    elif 'tuk' in nutrient_lower or 'fat' in nutrient_lower:
                        nutrition_data['macros']['fat'] = value
                    elif 'vláknin' in nutrient_lower or 'fiber' in nutrient_lower:
                        nutrition_data['macros']['fiber'] = value
                    elif 'cukr' in nutrient_lower or 'sugar' in nutrient_lower:
                        nutrition_data['macros']['sugar'] = value
        
        return nutrition_data
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error parsing data: {e}", file=sys.stderr)
        return None


def main():
    """Main function to demonstrate usage"""
    
    # Example URL from the problem statement
    url = "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend"
    
    # Allow URL to be passed as command line argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    print(f"Fetching nutrition data from: {url}")
    print("-" * 60)
    
    # Fetch the data
    data = fetch_nutrition_data(url)
    
    if data:
        # Pretty print the results
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Also create a summary in the format used in the purpose file
        print("\n" + "=" * 60)
        print("Summary for diet tracking:")
        print("=" * 60)
        if data.get('product_name'):
            print(f"Product: {data['product_name']}")
        
        macros = data.get('macros', {})
        if macros:
            print("\nMacronutrients (per 100g):")
            for key, value in macros.items():
                print(f"  {key.capitalize()}: {value}")
    else:
        print("Failed to fetch nutrition data. Please check the URL and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
