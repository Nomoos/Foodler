# Reorganizace Projektu - Leden 2026

## 🎯 Cíl Reorganizace

Zlepšit strukturu projektu přesunutím souborů do logických složek pro lepší orientaci a údržbu.

## 📁 Nová Struktura

```
Foodler/
├── README.md                    # Hlavní dokumentace
├── README_EN.md                 # Anglická dokumentace
├── requirements.txt             # Python závislosti
│
├── data/                        # Datové soubory
│   └── meal_plans/
│       ├── meal_plan_28_days.json
│       └── weekly/              # ⭐ Týdenní plány
│
├── docs/                        # Dokumentace
│   ├── archive/                 # ⭐ Archivní dokumenty
│   ├── diet-plans/              # Dietní plány
│   ├── getting-started/         # Návody
│   ├── health/                  # Zdravotní informace
│   ├── meal-planning/           # Plánování jídel
│   └── technical/               # Technická dokumentace
│
├── examples/                    # ⭐ Demo a příklady použití
│   ├── demo_dotaznik_paja.py
│   ├── demo_dotaznik_roman.py
│   └── ...
│
├── scripts/                     # ⭐ Spustitelné skripty
│   ├── README.md
│   ├── generate_meal_plan_date.py
│   ├── generate_weekly_meal_plan.py  # ⭐ NOVÝ
│   └── ...
│
├── tests/                       # ⭐ Testovací soubory
│   ├── test_kupi_scraper.py
│   └── ...
│
├── src/                         # Zdrojový kód
│   ├── analyzers/
│   ├── assistants/
│   ├── planners/
│   ├── scrapers/
│   │   └── fetch_nutrition_data.py  # ⭐ Přesunuto
│   ├── framework_core.py            # ⭐ Přesunuto
│   ├── framework_implementation.py   # ⭐ Přesunuto
│   └── modularni_system_rodina.py   # ⭐ Přesunuto
│
├── jidla/                       # Databáze jídel
├── lednice/                     # Správa zásob
├── modely/                      # Datové modely
├── nakup/                       # Nákupní seznamy
├── osoby/                       # Osobní profily
└── potraviny/                   # Databáze potravin
```

## 📊 Změny

### Přesunuté Soubory

#### ✅ Do `scripts/` (spustitelné skripty)
- `generate_meal_plan_date.py`
- `generate_meal_plan_tomorrow.py`
- `generate_optimized_plan.py`
- `scrape_and_save_discounts.py`
- `doporuc_balene_produkty.py`
- `zpracuj_dotazniky_a_vytvor_plan.py`

#### ✅ Do `tests/` (testovací soubory)
- `test_*.py` (všechny testovací soubory)

#### ✅ Do `examples/` (demo skripty)
- `demo_*.py` (všechny demo soubory)
- `example_usage.py`

#### ✅ Do `src/` (framework a knihovny)
- `framework_core.py`
- `framework_implementation.py`
- `modularni_system_rodina.py`
- `fetch_nutrition_data.py` → `src/scrapers/`

#### ✅ Do `docs/archive/` (archivní dokumentace)
- Všechny .md soubory kromě README*.md a requirements.txt

### Nově Vytvořené

#### ⭐ Nové Skripty
- `scripts/generate_weekly_meal_plan.py` - Generátor týdenních jídelníčků

#### ⭐ Nové Složky
- `scripts/` - Spustitelné skripty
- `tests/` - Testovací soubory
- `examples/` - Demo příklady
- `docs/archive/` - Archivní dokumenty
- `data/meal_plans/weekly/` - Týdenní jídelníčky

#### ⭐ Nová Dokumentace
- `scripts/README.md` - Dokumentace skriptů

## 🎉 Výsledek

### Před reorganizací
- **Root složka:** 26 Python souborů + 21 Markdown souborů = 47 souborů
- **Chaos:** Těžké najít potřebné soubory

### Po reorganizaci
- **Root složka:** 2 Markdown soubory + 1 requirements.txt = 3 soubory
- **Přehlednost:** Logická struktura, snadná navigace

## 📅 Datum Reorganizace
18. ledna 2026

## 📝 Poznámky
- Všechny relativní cesty ve skriptech byly aktualizovány
- Git historie zachována pomocí `git mv`
- Zpětná kompatibilita zachována (skripty fungují stejně)
