# Foodler - Family Weight Loss Assistant

## English Summary

**Foodler** is a family health management repository focused on structured weight loss and dietary tracking. It supports a ketogenic/low-carb dietary approach for family members with specific health considerations.

### Key Features
- 📊 Structured daily meal planning (6 meals, 2000 kcal)
- 🥗 Ketogenic macro tracking (140g+ protein, <70g carbs, 129g fat)
- 💊 Medication and supplement scheduling
- 🚴 Exercise routine coordination (recumbent cycling)
- 📈 Health metrics tracking
- 🔬 Diet methodology research (keto, mackerel diet)

### Health Goals
- **Primary User:** 135kg → target weight (41% body fat reduction)
- **Secondary User:** ~80kg → target weight (details TBD)

### Medical Context
This program is medically supervised and includes management of:
- Cardiovascular health (blood pressure medications)
- Digestive health (acid reflux treatment)
- Overall metabolic health improvement

---

## Česky (Czech)

**Foodler** je rodinný zdravotní management systém zaměřený na strukturované hubnutí a sledování stravy. Podporuje ketogenní/nízko-sacharidovou dietu pro členy rodiny se specifickými zdravotními ohledu.

### Klíčové vlastnosti
- 📊 Strukturované denní plánování jídel (6 jídel, 2000 kcal)
- 🥗 Sledování ketogenních makr (140g+ bílkovin, <70g sacharidů, 129g tuku)
- 💊 Plánování léků a suplementů
- 🚴 Koordinace cvičení (recumbent)
- 📈 Sledování zdravotních metrik
- 🔬 Výzkum dietních metodik (keto, mačinková dieta)

### Zdravotní cíle
- **Primární uživatel:** 135kg → cílová váha (snížení 41% tuku)
- **Sekundární uživatel:** ~80kg → cílová váha (upřesní se později)

### Lékařský kontext
Program je lékařsky sledován a zahrnuje řízení:
- Kardiovaskulárního zdraví (léky na krevní tlak)
- Trávicího zdraví (léčba refluxu)
- Celkové zlepšení metabolického zdraví

---

## Repository Structure

```
Foodler/
├── purpose                     # Original purpose document (Czech)
├── README.md                   # This file - Project overview
├── PURPOSE_ANALYSIS.md         # Detailed analysis and documentation
├── kupi_scraper.py            # Kupi.cz discount scraper module
├── keto_shopping_assistant.py # Keto diet shopping assistant tool
├── KUPI_INTEGRATION.md        # Kupi.cz integration guide
└── requirements.txt           # Python dependencies
```

## Documentation

- [PURPOSE_ANALYSIS.md](./PURPOSE_ANALYSIS.md) - Comprehensive analysis of dietary plan and methodology
- [KUPI_INTEGRATION.md](./KUPI_INTEGRATION.md) - Guide for using the Kupi.cz discount scraper

## Features

### 🛒 Smart Shopping Integration

The repository includes tools to connect to **Kupi.cz**, a Czech discount aggregator, to help find the best deals on keto-friendly foods:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the keto shopping assistant
python keto_shopping_assistant.py

# Or use the scraper directly
python kupi_scraper.py
```

The shopping tools help:
- Find discounted proteins, dairy, vegetables, and healthy fats
- Compare prices across Czech supermarkets (Lidl, Kaufland, Albert, etc.)
- Plan weekly shopping based on current offers
- Optimize grocery budget while maintaining diet requirements

See [KUPI_INTEGRATION.md](./KUPI_INTEGRATION.md) for detailed usage instructions.

## Status

**Active Development** - The repository includes:
- ✅ Documented dietary plan and health objectives
- ✅ Kupi.cz integration for finding grocery discounts
- ✅ Keto diet shopping assistant
- 🚧 Future: Meal tracking, progress monitoring, recipe database
