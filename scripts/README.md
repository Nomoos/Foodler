# Scripts - Spustitelné Skripty

Tato složka obsahuje všechny spustitelné skripty pro generování jídelníčků, nákupních seznamů a další užitečné nástroje.

## 📋 Přehled Skriptů

### Generování Jídelníčků

#### `generate_meal_plan_date.py`
Generuje jídelníček pro konkrétní den.

**Použití:**
```bash
cd scripts
python3 generate_meal_plan_date.py                    # Dnešní den
python3 generate_meal_plan_date.py tomorrow           # Zítřek
python3 generate_meal_plan_date.py 19.1.2026          # Konkrétní datum
python3 generate_meal_plan_date.py 2026-01-19         # ISO formát
```

#### `generate_meal_plan_tomorrow.py`
Rychlé generování jídelníčku na zítřek.

**Použití:**
```bash
cd scripts
python3 generate_meal_plan_tomorrow.py
```

#### `generate_weekly_meal_plan.py`
Generuje kompletní týdenní jídelníček (7 dní) a ukládá do JSON souboru.

**Použití:**
```bash
cd scripts
python3 generate_weekly_meal_plan.py 19.1.2026        # Týden od 19.1.2026
python3 generate_weekly_meal_plan.py 2026-01-19       # ISO formát
```

**Výstup:**
- Vytiskne týdenní jídelníček do konzole
- Uloží JSON soubor do `../data/meal_plans/weekly/`

#### `generate_weekly_meal_plan_md.py` ⭐ NOVÉ - DOPORUČENO
Generuje kompletní týdenní jídelníček ve formátu Markdown - čitelný a tisknutelný!

**Použití:**
```bash
cd scripts
python3 generate_weekly_meal_plan_md.py 19.1.2026     # Týden od 19.1.2026
python3 generate_weekly_meal_plan_md.py 2026-01-19    # ISO formát
```

**Výstup složka:** `../data/meal_plans/weekly/week_YYYY-MM-DD/`
- ✅ `README.md` - Týdenní souhrn s odkazy na jednotlivé dny
- ✅ `day_1_YYYY-MM-DD_den.md` - Jídelníček pro každý den (7 souborů)
- ✅ `shopping_list.md` - Kompletní nákupní seznam s kategoriemi

**Výhody MD formátu:**
- 📖 Čitelný v textovém editoru, GitHub, nebo tištěný
- 🔗 Odkazy mezi soubory
- ☑️ Checkboxy pro nákupní seznam
- 📱 Snadno zobrazitelný na mobilu
- 🖨️ Připravený k tisku

#### `generate_optimized_plan.py`
Generuje optimalizovaný jídelníček s ohledem na nutriční cíle.

**Použití:**
```bash
cd scripts
python3 generate_optimized_plan.py
```

### Nákupní Nástroje

#### `doporuc_balene_produkty.py`
Doporučuje balené produkty vhodné pro ketogenní dietu.

**Použití:**
```bash
cd scripts
python3 doporuc_balene_produkty.py
```

#### `scrape_and_save_discounts.py`
Stahuje aktuální slevy z internetových obchodů.

**Použití:**
```bash
cd scripts
python3 scrape_and_save_discounts.py
```

### Komplexní Nástroje

#### `zpracuj_dotazniky_a_vytvor_plan.py`
Zpracuje dotazníky a vytvoří personalizovaný dietní plán.

**Použití:**
```bash
cd scripts
python3 zpracuj_dotazniky_a_vytvor_plan.py
```

## 📂 Struktura Výstupů

```
data/
└── meal_plans/
    ├── meal_plan_28_days.json       # Základní 28denní cyklus
    └── weekly/
        ├── weekly_plan_YYYY-MM-DD_to_YYYY-MM-DD.json  # Týdenní plány (JSON)
        └── week_YYYY-MM-DD/         # 📁 Týdenní plány (Markdown) ⭐
            ├── README.md            # Týdenní souhrn s odkazy
            ├── day_1_YYYY-MM-DD_den.md  # Pondělí
            ├── day_2_YYYY-MM-DD_den.md  # Úterý
            ├── day_3_YYYY-MM-DD_den.md  # Středa
            ├── day_4_YYYY-MM-DD_den.md  # Čtvrtek
            ├── day_5_YYYY-MM-DD_den.md  # Pátek
            ├── day_6_YYYY-MM-DD_den.md  # Sobota
            ├── day_7_YYYY-MM-DD_den.md  # Neděle
            └── shopping_list.md     # Nákupní seznam
```

### Příklad MD Struktury (week_2026-01-19)

**README.md obsahuje:**
- 📅 Přehled týdne s odkazy na jednotlivé dny
- 📊 Statistiky týdne (35 jídel, vegetariánské varianty)
- 🛒 Odkaz na nákupní seznam

**day_X_YYYY-MM-DD_den.md obsahuje:**
- 🌅 Snídaně
- 🍎 Dopolední svačina
- 🍽️ Oběd (včetně vegetariánských variant)
- 🥤 Odpolední svačina
- 🌙 Večeře
- 💡 Tipy pro přípravu

**shopping_list.md obsahuje:**
- ☑️ Checkboxy pro označení položek
- 📦 Kategorie: Zelenina, Ovoce, Maso, Mléčné produkty, Obiloviny, Ořechy, Koření
- 🔢 Počet použití každé ingredience během týdne
- 💡 Tipy pro nákup (čerstvost, slevy, meal prep)

## 🔧 Technické Detaily

### Relativní Cesty
Všechny skripty používají relativní cesty k datovým souborům:
- `../data/meal_plans/` - Jídelníčky
- `../potraviny/` - Databáze potravin
- `../osoby/` - Osobní profily

### 28denní Cyklus
Jídelníčky pracují s 28denním cyklem, který se opakuje po celý rok. Den v cyklu se vypočítá:
```python
start_of_year = datetime(target_date.year, 1, 1)
days_since_start = (target_date - start_of_year).days
cycle_day = (days_since_start % 28) + 1
```

## 📚 Související Dokumentace

- **[README.md](../README.md)** - Hlavní dokumentace projektu
- **[docs/getting-started/](../docs/getting-started/)** - Návody k použití
- **[docs/meal-planning/](../docs/meal-planning/)** - Plánování jídel

## ℹ️ Poznámky

- Před spuštěním se ujistěte, že máte nainstalované závislosti: `pip install -r ../requirements.txt`
- Všechny skripty jsou v UTF-8 kódování pro správnou práci s českými znaky
- Pro spuštění skriptů se přesuňte do složky `scripts/` nebo použijte úplné cesty
