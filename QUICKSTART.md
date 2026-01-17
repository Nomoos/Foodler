# How to Use - Quick Start Guide

## Fetch Nutrition Data from kaloricketabulky.cz

This guide shows you how to fetch nutritional data from the URL provided in the issue.

### Step 1: Install Dependencies

```bash
# Optional: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Fetch Data

#### Option A: Command Line Usage

```bash
python fetch_nutrition_data.py "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend"
```

**Example Output:**
```json
{
  "product_name": "Whey Protein Chocolate & Cocoa 100% - Nutrend",
  "url": "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend",
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

#### Option B: Use in Python Code

```python
from fetch_nutrition_data import fetch_nutrition_data

url = "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend"
data = fetch_nutrition_data(url)

if data:
    print(f"Product: {data['product_name']}")
    print(f"Protein per 100g: {data['macros']['protein']}")
```

#### Option C: With Caching (Recommended)

```python
from example_usage import get_nutrition_data, calculate_serving

# Fetch data (uses cache if available)
url = "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend"
data = get_nutrition_data(url, use_cache=True)

# Calculate for 30g serving
serving = calculate_serving(data, 30)
print(f"Per 30g serving:")
for key, value in serving['macros'].items():
    print(f"  {key}: {value}")
```

### Step 3: Test with Mock Data (No Internet Required)

If you want to test the parser logic without internet access:

```bash
python test_mock_data.py
```

This will demonstrate the parsing functionality using mock HTML data.

## Troubleshooting

### Network Error
If you get a network error, make sure:
- You have internet access
- The website is accessible from your location
- Your firewall/proxy allows HTTPS connections

### Parsing Error
If the data doesn't parse correctly, the website structure may have changed. You may need to update the parsing logic in `fetch_nutrition_data.py`.

### Empty Results
If you get empty macros in the result, the website might use different Czech terms. Check the HTML source and update the nutrient mapping in the script.

## Integration with Diet Plan

The fetched data can be used to update the diet plan in the `purpose` file. For example:

**From purpose file (30g serving):**
```
30 g Nutrend Whey protein (chocolate cacao)
B: 26 S: 6 T: 8 F: 14
220 kcal
```

**Using the fetcher:**
```python
from example_usage import get_nutrition_data, calculate_serving

url = "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend"
data = get_nutrition_data(url)
serving = calculate_serving(data, 30)

# Print in the format used in purpose file
print(f"30 g {data['product_name']}")
print(f"B: {serving['macros']['protein']} S: {serving['macros']['carbohydrates']} T: {serving['macros']['fat']} F: {serving['macros']['fiber']}")
print(f"{serving['macros']['calories']}")
```

## Next Steps

- Add more food URLs to track other items from your diet plan
- Export data to CSV or Excel for better tracking
- Create a database to store all fetched nutrition data
- Build a meal planner that uses this data
