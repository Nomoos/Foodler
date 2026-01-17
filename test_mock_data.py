#!/usr/bin/env python3
"""
Test script with mock data to demonstrate the nutrition data fetching functionality
"""

from bs4 import BeautifulSoup
import json


def test_with_mock_data():
    """Test the parsing logic with mock HTML data"""
    
    # Mock HTML structure similar to what we'd expect from kaloricketabulky.cz
    mock_html = """
    <html>
    <head><title>Whey Protein Chocolate & Cocoa 100% - Nutrend</title></head>
    <body>
        <h1>Whey Protein Chocolate & Cocoa 100% - Nutrend</h1>
        <div class="nutrition-info">
            <h2>Nutriční hodnoty na 100 g</h2>
            <table class="nutritional-table">
                <tr>
                    <th>Živina</th>
                    <th>Hodnota</th>
                </tr>
                <tr>
                    <td>Energie (kalorie)</td>
                    <td>380 kcal</td>
                </tr>
                <tr>
                    <td>Bílkoviny</td>
                    <td>78 g</td>
                </tr>
                <tr>
                    <td>Sacharidy</td>
                    <td>6 g</td>
                </tr>
                <tr>
                    <td>z toho cukry</td>
                    <td>5 g</td>
                </tr>
                <tr>
                    <td>Tuky</td>
                    <td>6 g</td>
                </tr>
                <tr>
                    <td>Vláknina</td>
                    <td>2 g</td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """
    
    # Parse the mock HTML
    soup = BeautifulSoup(mock_html, 'html.parser')
    
    # Extract product name
    product_name = None
    h1_tag = soup.find('h1')
    if h1_tag:
        product_name = h1_tag.get_text(strip=True)
    
    # Initialize nutrition data
    nutrition_data = {
        'product_name': product_name,
        'url': 'https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend',
        'macros': {},
        'vitamins': {},
        'minerals': {}
    }
    
    # Parse table
    tables = soup.find_all('table')
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                nutrient = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                
                nutrient_lower = nutrient.lower()
                
                # Map nutrients
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


if __name__ == "__main__":
    print("Testing nutrition data parser with mock HTML...")
    print("=" * 70)
    
    data = test_with_mock_data()
    
    print("\nParsed data (JSON format):")
    print("-" * 70)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 70)
    print("Summary for diet tracking (format from purpose file):")
    print("=" * 70)
    
    if data.get('product_name'):
        print(f"Product: {data['product_name']}")
    
    macros = data.get('macros', {})
    if macros:
        print("\nMacronutrients (per 100g):")
        for key, value in macros.items():
            print(f"  {key.capitalize()}: {value}")
    
    # Calculate for 30g serving (as mentioned in purpose file)
    print("\n" + "=" * 70)
    print("Calculation for 30g serving (as used in diet plan):")
    print("=" * 70)
    
    # Extract numeric values (simplified - assumes "XX g" or "XXX kcal" format)
    try:
        protein_per_100g = float(macros.get('protein', '0 g').split()[0])
        carbs_per_100g = float(macros.get('carbohydrates', '0 g').split()[0])
        fat_per_100g = float(macros.get('fat', '0 g').split()[0])
        fiber_per_100g = float(macros.get('fiber', '0 g').split()[0])
        calories_per_100g = float(macros.get('calories', '0 kcal').split()[0])
        
        serving_size = 30  # grams
        factor = serving_size / 100
        
        print(f"Serving size: {serving_size}g")
        print(f"  Calories: {calories_per_100g * factor:.1f} kcal")
        print(f"  Protein: {protein_per_100g * factor:.1f} g")
        print(f"  Carbohydrates: {carbs_per_100g * factor:.1f} g")
        print(f"  Fat: {fat_per_100g * factor:.1f} g")
        print(f"  Fiber: {fiber_per_100g * factor:.1f} g")
        
        # Compare with values in purpose file
        print("\n" + "=" * 70)
        print("Comparison with purpose file values (30g serving):")
        print("=" * 70)
        print("Purpose file states: B: 26, S: 6, T: 8, F: 14 (220 kcal)")
        print(f"Calculated values: B: {protein_per_100g * factor:.0f}, S: {carbs_per_100g * factor:.0f}, T: {fat_per_100g * factor:.0f}, F: {fiber_per_100g * factor:.0f} ({calories_per_100g * factor:.0f} kcal)")
        
    except Exception as e:
        print(f"Could not calculate serving: {e}")
    
    print("\n✓ Mock data test completed successfully!")
