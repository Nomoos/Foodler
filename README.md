# Foodler - Nutrition Data Fetcher

A tool to fetch nutritional data from Czech nutrition database (kaloricketabulky.cz) for diet and meal planning.

## Purpose

This project helps with diet tracking and meal planning by fetching nutritional information from online databases. It's designed to support a family diet plan with specific macro targets.

## Installation

1. Install Python 3.7 or higher
2. (Optional but recommended) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Fetch nutrition data from a URL

```bash
python fetch_nutrition_data.py "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend"
```

### Use in Python code

```python
from fetch_nutrition_data import fetch_nutrition_data

url = "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend"
data = fetch_nutrition_data(url)

if data:
    print(f"Product: {data['product_name']}")
    print(f"Protein: {data['macros'].get('protein', 'N/A')}")
    print(f"Carbs: {data['macros'].get('carbohydrates', 'N/A')}")
    print(f"Fat: {data['macros'].get('fat', 'N/A')}")
```

## Features

- Fetches product information from kaloricketabulky.cz
- Parses nutritional data (calories, protein, carbs, fat, fiber, sugar)
- Outputs data in JSON format
- Handles Czech language nutrition terms
- Provides formatted summary for diet tracking

## Example Output

```json
{
  "product_name": "Whey Protein Chocolate & Cocoa 100% - Nutrend",
  "url": "https://www.kaloricketabulky.cz/potraviny/whey-protein-chocolate-a-cocoa-100-nutrend",
  "macros": {
    "calories": "380 kcal",
    "protein": "78 g",
    "carbohydrates": "6 g",
    "fat": "6 g",
    "fiber": "2 g"
  }
}
```

## Diet Plan Reference

The `purpose` file contains the original diet plan with daily macro targets:
- Protein: minimum 140g
- Carbohydrates: max 70g
- Fat: 129g
- Fiber: at least 20g (ideally more)
- Total: 2000 kcal in 6 meals

## Network Requirements

This script requires internet access to fetch data from kaloricketabulky.cz. If running in a restricted environment, the script will fail gracefully with an error message.

## Error Handling

The script includes error handling for:
- **Network connection issues**: Returns error message "Error fetching data: [details]" and exits with code 1
- **Invalid URLs**: Returns HTTP error with status code
- **Parsing errors**: Returns error message "Error parsing data: [details]" 
- **Missing data fields**: Fields not found in HTML will be omitted from output JSON

When errors occur, the script will print an error message to stderr and return None (in library mode) or exit with code 1 (in CLI mode).

## Contributing

Feel free to add support for:
- Other nutrition databases
- Additional data fields (vitamins, minerals)
- Export formats (CSV, Excel)
- Database storage for tracked foods
