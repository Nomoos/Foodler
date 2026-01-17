# Generátory jídelníčků / Meal Plan Generators

Tento soubor popisuje použití nových generátorů jídelníčků v projektu Foodler.

## Popis / Description

Projekt nyní obsahuje dva nové skripty pro generování jídelníčků ze stávajícího 28denního cyklu jídel:

1. **`generate_meal_plan_tomorrow.py`** - Vygeneruje jídelníček konkrétně na 18.1.2026
2. **`generate_meal_plan_date.py`** - Flexibilní generátor pro libovolné datum

## Použití / Usage

### 1. Jídelníček na 18.1.2026

```bash
python generate_meal_plan_tomorrow.py
```

Tento skript vygeneruje kompletní jídelníček na 18. ledna 2026, včetně:
- ✅ Kompletní rozvrh jídel (snídaně, svačiny, oběd, večeře)
- ✅ Vegetariánské varianty
- ✅ Nákupní seznam ingrediencí
- ✅ Tipy pro přípravu

### 2. Flexibilní generátor pro libovolné datum

```bash
# Dnes
python generate_meal_plan_date.py today
python generate_meal_plan_date.py

# Zítra
python generate_meal_plan_date.py tomorrow

# Konkrétní datum (různé formáty)
python generate_meal_plan_date.py 18.1.2026
python generate_meal_plan_date.py 2026-01-18
python generate_meal_plan_date.py 25.1.2026
```

## Jak to funguje / How It Works

Systém využívá 28denní cyklus jídel uložený v souboru:
```
data/meal_plans/meal_plan_28_days.json
```

### Výpočet dne v cyklu

Pro každé datum skript vypočítá odpovídající den v 28denním cyklu:

```python
# Počet dní od začátku roku
days_since_start = (target_date - start_of_year).days

# Den v cyklu (1-28)
cycle_day = (days_since_start % 28) + 1
```

**Příklad:**
- 18. ledna 2026 = 17 dní od začátku roku
- (17 % 28) + 1 = 18. den v cyklu

### Struktura výstupu

Každý jídelníček obsahuje:

```
🍽️  JÍDELNÍČEK - DD.MM.YYYY (den v týdnu)
Den X z 28denního cyklu

🌅 SNÍDANĚ
   [obsah snídaně]

🍎 DOPOLEDNÍ SVAČINA
   [obsah svačiny]

🍽️  OBĚD
   [obsah obědu]

🥤 ODPOLEDNÍ SVAČINA
   [obsah svačiny]

🌙 VEČEŘE
   [obsah večeře]

💡 Tip: [informace o vegetariánských variantách]

🛒 HLAVNÍ INGREDIENCE
   ✓ ingredience 1
   ✓ ingredience 2
   ...

💡 TIPY PRO PŘÍPRAVU:
   • tip 1
   • tip 2
```

## Příklad výstupu pro 18.1.2026

```
Den 18 z 28denního cyklu

🌅 SNÍDANĚ
   Bílý jogurt, vlašské ořechy, med, skořice

🍎 DOPOLEDNÍ SVAČINA
   Hruška

🍽️  OBĚD
   Červená řepa, cibule, tuňák / Vegetarián: Červená řepa, cibule, vejce

🥤 ODPOLEDNÍ SVAČINA
   Okurkový salát s jogurtem

🌙 VEČEŘE
   Salát z červené řepy, smažená kuřecí prsa obalená ve vlašských ořech. 
   / Vegetarián: Brokolicové karbanátky, salát z červené řepy
```

## Technické detaily / Technical Details

### Požadavky
- Python 3.6+
- Standardní knihovna (json, datetime)
- Soubor: `data/meal_plans/meal_plan_28_days.json`

### Funkce

**`load_meal_plan_json()`**
- Načte JSON soubor s 28denním plánem
- Zpracuje chyby (soubor nenalezen, chybný JSON)

**`get_cycle_day_for_date(target_date)`**
- Vypočítá den v 28denním cyklu pro dané datum
- Args: datetime objekt
- Returns: číslo dne (1-28)

**`get_meal_for_day(day_number)`**
- Získá všechna jídla pro daný den cyklu
- Returns: dictionary s klíči (snídaně, oběd, večeře, svačiny)

**`format_meal_plan(date, cycle_day, meals)`**
- Naformátuje jídelníček do čitelného výstupu
- Používá emoji ikony pro lepší čitelnost

**`extract_ingredients_from_meals(meals)`**
- Extrahuje hlavní ingredience z názvů jídel
- Returns: seřazený seznam ingrediencí

## Rozšíření / Extensions

Skripty lze snadno rozšířit o:

1. **Export do PDF/HTML** - přidat funkci pro export jídelníčku
2. **Týdenní plány** - vygenerovat celý týden najednou
3. **Nutriční hodnoty** - připojit informace o kaloriích a makronutrientech
4. **Integrace s nákupním seznamem** - propojit s moduly `nakup/`
5. **Mobilní notifikace** - denní upomínka s jídelníčkem

## Viz také / See Also

- [example_usage.py](example_usage.py) - Příklady práce s 28denním plánem
- [docs/meal-planning/TYDENNI_PLANOVANI.md](docs/meal-planning/TYDENNI_PLANOVANI.md) - Strategie týdenního plánování
- [data/meal_plans/](data/meal_plans/) - Datové soubory s jídelními plány

## Autor / Author

Vytvořeno jako součást projektu Foodler pro potřeby rodinného dietního plánování.
