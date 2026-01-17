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
from typing import Dict, Optional, List
from urllib.parse import quote_plus


def search_product(product_name: str) -> List[Dict]:
    """
    Search for products by name on kaloricketabulky.cz
    
    Args:
        product_name: Name of the product to search for (in Czech)
        
    Returns:
        List of dictionaries with search results, each containing 'name' and 'url'
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Encode the search query
        search_query = quote_plus(product_name)
        search_url = f"https://www.kaloricketabulky.cz/vyhledavani/?q={search_query}"
        
        print(f"Searching for: {product_name}", file=sys.stderr)
        print(f"Search URL: {search_url}", file=sys.stderr)
        
        # Fetch search results
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = []
        
        # Look for search result links - adjust selectors based on actual site structure
        # Common patterns: links in result listings, product cards, etc.
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            # Filter for product links (typically contain /potraviny/)
            if '/potraviny/' in href and href not in [r['url'] for r in results]:
                # Get the product name from the link text or title
                name = link.get_text(strip=True)
                if not name:
                    name = link.get('title', '')
                
                # Make sure URL is absolute
                if href.startswith('/'):
                    href = f"https://www.kaloricketabulky.cz{href}"
                
                if name and len(name) > 2:  # Filter out empty or very short names
                    results.append({
                        'name': name,
                        'url': href
                    })
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_results = []
        for result in results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)
        
        return unique_results[:10]  # Return top 10 results
        
    except requests.RequestException as e:
        print(f"Error searching for product: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error processing search results: {e}", file=sys.stderr)
        return []


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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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


def fetch_by_product_name(product_name: str) -> Optional[Dict]:
    """
    Search for a product by name and fetch its nutritional data
    
    Args:
        product_name: Name of the product to search for
        
    Returns:
        Dictionary containing nutritional information or None if not found
    """
    # Search for the product
    results = search_product(product_name)
    
    if not results:
        print(f"No results found for: {product_name}", file=sys.stderr)
        return None
    
    print(f"\nFound {len(results)} result(s):", file=sys.stderr)
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['name']}", file=sys.stderr)
    
    # Use the first result
    print(f"\nUsing first result: {results[0]['name']}", file=sys.stderr)
    return fetch_nutrition_data(results[0]['url'])


def main():
    """Main function to demonstrate usage"""
    
    # Example URL from the problem statement
    url = "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend"
    
    # Check if argument is a URL or product name
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        # If it starts with http, treat it as URL
        if arg.startswith('http://') or arg.startswith('https://'):
            url = arg
            print(f"Fetching nutrition data from: {url}")
            print("-" * 60)
            data = fetch_nutrition_data(url)
        else:
            # Otherwise, treat it as product name
            product_name = arg
            print(f"Searching for product: {product_name}")
            print("-" * 60)
            data = fetch_by_product_name(product_name)
    else:
        print(f"Fetching nutrition data from: {url}")
        print("-" * 60)
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
        print("Failed to fetch nutrition data. Please check the input and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
