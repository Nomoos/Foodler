#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor týdenního jídelníčku ve formátu Markdown
Weekly meal plan generator in Markdown format

Generuje:
- Jednotlivé MD soubory pro každý den
- Týdenní souhrn s odkazy na jednotlivé dny
- Nákupní seznam ingrediencí

Usage:
    python generate_weekly_meal_plan_md.py 19.1.2026         # Start date
    python generate_weekly_meal_plan_md.py 2026-01-19        # Start date (ISO format)
"""

import json
import sys
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict

# Cesta k meal plan datům
MEAL_PLAN_JSON = '../data/meal_plans/meal_plan_28_days.json'
WEEKLY_PLANS_DIR = '../data/meal_plans/weekly'


def load_meal_plan_json():
    """Načte jídelníček z JSON souboru"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, MEAL_PLAN_JSON)
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Chyba: Soubor '{json_path}' nenalezen!")
        return None
    except json.JSONDecodeError as e:
        print(f"Chyba: Neplatný JSON formát - {e}")
        return None


def parse_date_argument(arg):
    """
    Parsuje argument s datem.
    
    Args:
        arg: String s datem (např. "19.1.2026", "2026-01-19")
        
    Returns:
        datetime objekt nebo None při chybě
    """
    if not arg:
        return datetime.now()
    
    # Zkusíme různé formáty
    for fmt in ["%d.%m.%Y", "%d.%m.%y", "%Y-%m-%d"]:
        try:
            return datetime.strptime(arg, fmt)
        except ValueError:
            continue
    
    print(f"Chyba: Nepodařilo se rozpoznat formát data '{arg}'")
    print("Podporované formáty: 'DD.M.YYYY', 'YYYY-MM-DD'")
    return None


def get_cycle_day_for_date(target_date):
    """
    Vypočítá den v 28denním cyklu pro dané datum.
    
    Args:
        target_date: datetime objekt pro cílové datum
        
    Returns:
        Den v cyklu (1-28)
    """
    start_of_year = datetime(target_date.year, 1, 1)
    days_since_start = (target_date - start_of_year).days
    cycle_day = (days_since_start % 28) + 1
    return cycle_day


def get_czech_day_name(date):
    """Vrátí český název dne v týdnu"""
    days = ['pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', 'sobota', 'neděle']
    return days[date.weekday()]


def extract_ingredients(meal_text):
    """
    Extrahuje ingredience z textu jídla.
    
    Args:
        meal_text: Text popisující jídlo
        
    Returns:
        List ingrediencí
    """
    if not meal_text:
        return []
    
    # Odstraníme poznámky o vegetariánských variantách
    text = re.split(r'/\s*Vegetarián:', meal_text)[0]
    
    # Rozdělíme podle čárek a "/" (ne před slovem Vegetarián)
    ingredients = re.split(r'[,/]', text)
    
    # Vyčistíme a normalizujeme
    cleaned = []
    for ing in ingredients:
        ing = ing.strip()
        if ing and len(ing) > 2:  # Ignorujeme velmi krátké fragmenty
            # Odstraníme poznámky v závorkách
            ing = re.sub(r'\([^)]*\)', '', ing).strip()
            cleaned.append(ing)
    
    return cleaned


def generate_day_markdown(date, day_data, cycle_day):
    """
    Vygeneruje Markdown obsah pro jeden den.
    
    Args:
        date: datetime objekt pro datum
        day_data: Data jídel pro tento den
        cycle_day: Den v 28denním cyklu
        
    Returns:
        String s Markdown obsahem
    """
    day_name = get_czech_day_name(date)
    date_str = date.strftime("%d.%m.%Y")
    
    md = f"""# Jídelníček - {day_name.capitalize()} {date_str}

**Den {cycle_day} z 28denního cyklu**

---

## 🌅 Snídaně

{day_data.get('breakfast', 'N/A')}

---

## 🍎 Dopolední Svačina

{day_data.get('morning_snack', 'N/A')}

---

## 🍽️ Oběd

{day_data.get('lunch', 'N/A')}

---

## 🥤 Odpolední Svačina

{day_data.get('afternoon_snack', 'N/A')}

---

## 🌙 Večeře

{day_data.get('dinner', 'N/A')}

---

## 🌃 Večerní Svačina

{day_data.get('evening_snack', 'N/A')}

---

## 💡 Tipy

- Připravte si ingredience předem
- Můžete meal-prep některá jídla dopředu
- Vegetariánské varianty jsou uvedeny tam, kde jsou k dispozici

---

*Vygenerováno: {datetime.now().strftime("%d.%m.%Y %H:%M")}*
"""
    
    return md


def generate_weekly_summary(start_date, days_info):
    """
    Vygeneruje týdenní souhrn s odkazy na jednotlivé dny.
    
    Args:
        start_date: datetime objekt pro začátek týdne
        days_info: List informací o dnech
        
    Returns:
        String s Markdown obsahem
    """
    end_date = start_date + timedelta(days=6)
    week_str = f"{start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}"
    
    md = f"""# Týdenní Jídelníček

**Týden: {week_str}**

---

## 📅 Přehled Týdne

"""
    
    for day_info in days_info:
        date = day_info['date']
        day_name = day_info['day_name']
        filename = day_info['filename']
        breakfast = day_info['breakfast'][:50] + "..." if len(day_info['breakfast']) > 50 else day_info['breakfast']
        
        md += f"""### {day_name.capitalize()} {date.strftime('%d.%m.%Y')}

**Snídaně:** {breakfast}

[📄 Celý jídelníček]({filename})

---

"""
    
    md += f"""
## 🛒 Nákupní Seznam

Pro kompletní nákupní seznam včetně množství, viz [shopping_list.md](shopping_list.md)

---

## 📊 Statistiky Týdne

- **Počet jídel:** {len(days_info) * 5} (5 jídel denně × {len(days_info)} dní)
- **Vegetariánské varianty:** Dostupné u většiny hlavních jídel
- **Meal prep možnosti:** Některá jídla lze připravit předem

---

*Vygenerováno: {datetime.now().strftime("%d.%m.%Y %H:%M")}*
"""
    
    return md


def generate_shopping_list(days_info):
    """
    Vygeneruje nákupní seznam z jídel týdne.
    
    Args:
        days_info: List informací o dnech
        
    Returns:
        String s Markdown obsahem
    """
    # Sbíráme všechny ingredience
    all_ingredients = defaultdict(int)
    
    for day_info in days_info:
        for meal_type in ['breakfast', 'morning_snack', 'lunch', 'afternoon_snack', 'dinner', 'evening_snack']:
            meal_text = day_info.get(meal_type, '')
            ingredients = extract_ingredients(meal_text)
            for ing in ingredients:
                # Normalizujeme název (lowercase pro srovnání)
                key = ing.lower().strip()
                all_ingredients[key] += 1
    
    # Seřadíme podle frekvence (nejčastější nahoře)
    sorted_ingredients = sorted(all_ingredients.items(), key=lambda x: x[1], reverse=True)
    
    # Kategorizace (základní)
    categories = {
        'Zelenina': ['mrkev', 'brokolice', 'celer', 'salát', 'špenát', 'cuketa', 'červená řepa', 
                     'ředkvičk', 'okurek', 'kedlubn', 'dýň'],
        'Ovoce': ['jablko', 'hruška', 'ananas', 'kiwi', 'pomelo', 'meruňk', 'datle', 'rozink', 
                  'švestk', 'ovocn'],
        'Maso a Ryby': ['kuřecí', 'krůtí', 'treska', 'tuňák', 'vepřov'],
        'Mléčné Produkty': ['sýr', 'jogurt', 'mléko', 'tvaroh', 'brynza'],
        'Vejce a Náhražky': ['vejce', 'tofu', 'bílk'],
        'Obiloviny': ['pohank', 'jáhl', 'těstovin'],
        'Ořechy a Semínka': ['vlašské ořechy', 'mandle', 'ořech'],
        'Koření a Doplňky': ['med', 'česnek', 'máslo', 'olej'],
    }
    
    # Kategorizujeme ingredience
    categorized = defaultdict(list)
    uncategorized = []
    
    for ing, count in sorted_ingredients:
        found = False
        for cat, keywords in categories.items():
            if any(kw in ing for kw in keywords):
                categorized[cat].append((ing, count))
                found = True
                break
        if not found:
            uncategorized.append((ing, count))
    
    # Generujeme markdown
    start_date = days_info[0]['date']
    end_date = days_info[-1]['date']
    week_str = f"{start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}"
    
    md = f"""# Nákupní Seznam

**Týden: {week_str}**

Tento seznam obsahuje všechny ingredience potřebné pro jídelníček na celý týden.

---

## 📝 Instrukce

1. ✅ Zkontrolujte, co již máte doma
2. 📋 Označte položky, které potřebujete koupit
3. 🛒 Vezměte seznam do obchodu
4. 💰 Hledejte slevy (použijte `kupi.cz` scraper)

---

## 🛒 Ingredience v Přehledné Tabulce

| Kategorie | Ingredience | Četnost |
|-----------|-------------|---------|
"""
    
    # Kategorizované ingredience v tabulkovém formátu
    for cat in ['Zelenina', 'Ovoce', 'Maso a Ryby', 'Mléčné Produkty', 'Vejce a Náhražky', 
                'Obiloviny', 'Ořechy a Semínka', 'Koření a Doplňky']:
        if cat in categorized:
            for idx, (ing, count) in enumerate(categorized[cat]):
                # Kapitalizujeme první písmeno
                ing_display = ing[0].upper() + ing[1:]
                # První řádek kategorie má název kategorie, ostatní mají prázdné pole
                cat_display = f"**{cat}**" if idx == 0 else ""
                md += f"| {cat_display} | {ing_display} | {count}× týdně |\n"
    
    # Ostatní kategorie
    if uncategorized:
        for idx, (ing, count) in enumerate(uncategorized):
            ing_display = ing[0].upper() + ing[1:]
            cat_display = "**Ostatní**" if idx == 0 else ""
            md += f"| {cat_display} | {ing_display} | {count}× týdně |\n"
    
    md += f"""
---

## 💡 Tipy pro Nákup

- **Preferujte čerstvé produkty** - Zelenina a ovoce by měly být čerstvé
- **Hledejte slevy** - Použijte scraper pro kupi.cz: `python ../scripts/scrape_and_save_discounts.py`
- **Meal prep** - Některé ingredience můžete nakoupit ve větším množství a připravit dopředu
- **Vegetariánské alternativy** - Tofu, luštěniny místo masa
- **Kvalita před cenou** - U masa a ryb preferujte kvalitu

---

## 📊 Statistiky

- **Celkem položek:** {len(all_ingredients)}
- **Nejčastější ingredience:** {sorted_ingredients[0][0] if sorted_ingredients else 'N/A'} ({sorted_ingredients[0][1]}× během týdne)
- **Počet kategorií:** {len(categorized)}

---

*Vygenerováno: {datetime.now().strftime("%d.%m.%Y %H:%M")}*
"""
    
    return md


def generate_weekly_plan(start_date, meal_plan_data):
    """
    Vygeneruje kompletní týdenní plán včetně jednotlivých dnů a nákupního seznamu.
    
    Args:
        start_date: datetime objekt pro začátek týdne
        meal_plan_data: Načtená data z JSON souboru
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, WEEKLY_PLANS_DIR)
    
    # Vytvoř složku pokud neexistuje
    os.makedirs(output_dir, exist_ok=True)
    
    # Vytvoř podsložku pro tento týden
    week_folder_name = f"week_{start_date.strftime('%Y-%m-%d')}"
    week_folder = os.path.join(output_dir, week_folder_name)
    os.makedirs(week_folder, exist_ok=True)
    
    days_data = meal_plan_data['meal_plan']['days']
    days_info = []
    
    print(f"\n{'='*70}")
    print(f"🍽️  GENEROVÁNÍ TÝDENNÍHO JÍDELNÍČKU")
    print(f"{'='*70}\n")
    
    # Generuj soubor pro každý den
    for day_offset in range(7):
        current_date = start_date + timedelta(days=day_offset)
        cycle_day = get_cycle_day_for_date(current_date)
        
        # Najdeme den v cyklu (cycle_day je 1-28, index je 0-27)
        day_data = days_data[cycle_day - 1]
        
        # Generuj Markdown obsah
        md_content = generate_day_markdown(current_date, day_data, cycle_day)
        
        # Název souboru
        filename = f"day_{day_offset + 1}_{current_date.strftime('%Y-%m-%d')}_{get_czech_day_name(current_date)}.md"
        filepath = os.path.join(week_folder, filename)
        
        # Ulož soubor
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ {get_czech_day_name(current_date).capitalize()} {current_date.strftime('%d.%m.%Y')} → {filename}")
        
        # Uložíme info pro souhrn
        days_info.append({
            'date': current_date,
            'day_name': get_czech_day_name(current_date),
            'filename': filename,
            'breakfast': day_data.get('breakfast', ''),
            'morning_snack': day_data.get('morning_snack', ''),
            'lunch': day_data.get('lunch', ''),
            'afternoon_snack': day_data.get('afternoon_snack', ''),
            'dinner': day_data.get('dinner', ''),
            'evening_snack': day_data.get('evening_snack', '')
        })
    
    # Generuj týdenní souhrn
    print(f"\n📋 Generuji týdenní souhrn...")
    summary_md = generate_weekly_summary(start_date, days_info)
    summary_path = os.path.join(week_folder, 'README.md')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_md)
    print(f"✅ Týdenní souhrn → README.md")
    
    # Generuj nákupní seznam
    print(f"\n🛒 Generuji nákupní seznam...")
    shopping_md = generate_shopping_list(days_info)
    shopping_path = os.path.join(week_folder, 'shopping_list.md')
    with open(shopping_path, 'w', encoding='utf-8') as f:
        f.write(shopping_md)
    print(f"✅ Nákupní seznam → shopping_list.md")
    
    print(f"\n{'='*70}")
    print(f"✅ HOTOVO!")
    print(f"{'='*70}")
    print(f"\n📁 Všechny soubory uloženy v: {week_folder}\n")
    print(f"📖 Pro zobrazení: cd {week_folder} && cat README.md\n")


def main():
    """Hlavní funkce"""
    # Parsuj argumenty
    if len(sys.argv) < 2:
        print("Použití: python generate_weekly_meal_plan_md.py <datum>")
        print("Příklad: python generate_weekly_meal_plan_md.py 19.1.2026")
        sys.exit(1)
    
    start_date = parse_date_argument(sys.argv[1])
    if start_date is None:
        sys.exit(1)
    
    # Načti meal plan data
    meal_plan_data = load_meal_plan_json()
    if meal_plan_data is None:
        sys.exit(1)
    
    # Vygeneruj týdenní plán
    generate_weekly_plan(start_date, meal_plan_data)


if __name__ == '__main__':
    main()
