#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor jídelníčku pro konkrétní datum
Meal plan generator for a specific date

Usage:
    python generate_meal_plan_date.py                    # Today
    python generate_meal_plan_date.py tomorrow           # Tomorrow
    python generate_meal_plan_date.py 18.1.2026          # Specific date
    python generate_meal_plan_date.py 2026-01-18         # Specific date (ISO format)
"""

import json
import sys
from datetime import datetime, timedelta

# Cesta k meal plan datům
MEAL_PLAN_JSON = '../data/meal_plans/meal_plan_28_days.json'


def load_meal_plan_json():
    """Načte jídelníček z JSON souboru"""
    try:
        with open(MEAL_PLAN_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Chyba: Soubor '{MEAL_PLAN_JSON}' nenalezen!")
        return None
    except json.JSONDecodeError as e:
        print(f"Chyba: Neplatný JSON formát - {e}")
        return None


def parse_date_argument(arg, base_date=None):
    """
    Parsuje argument s datem.
    
    Args:
        arg: String s datem (např. "tomorrow", "18.1.2026", "2026-01-18")
        base_date: Základní datum pro relativní výpočty (default: now)
        
    Returns:
        datetime objekt nebo None při chybě
    """
    if base_date is None:
        base_date = datetime.now()
    
    if not arg or arg.lower() == "today":
        return base_date
    
    if arg.lower() == "tomorrow":
        return base_date + timedelta(days=1)
    
    # Zkusíme formát DD.M.YYYY nebo D.M.YYYY
    for fmt in ["%d.%m.%Y", "%d.%m.%y", "%Y-%m-%d"]:
        try:
            return datetime.strptime(arg, fmt)
        except ValueError:
            continue
    
    print(f"Chyba: Nepodařilo se rozpoznat formát data '{arg}'")
    print("Podporované formáty: 'today', 'tomorrow', 'DD.M.YYYY', 'YYYY-MM-DD'")
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


def get_meal_for_day(day_number):
    """Získá všechna jídla pro daný den"""
    data = load_meal_plan_json()
    if data is None:
        return None
    if 1 <= day_number <= 28:
        day = data['meal_plan']['days'][day_number - 1]
        return {
            'den': day['day'],
            'snídaně': day['breakfast'],
            'dopolední_svačina': day['morning_snack'],
            'oběd': day['lunch'],
            'odpolední_svačina': day['afternoon_snack'],
            'večeře': day['dinner']
        }
    return None


def get_czech_day_name(date_obj):
    """Vrátí český název dne v týdnu"""
    days = {
        0: "pondělí",
        1: "úterý",
        2: "středa",
        3: "čtvrtek",
        4: "pátek",
        5: "sobota",
        6: "neděle"
    }
    return days.get(date_obj.weekday(), "")


def format_meal_plan(target_date, cycle_day, meals):
    """
    Formátuje jídelníček do pěkného výstupu.
    
    Args:
        target_date: datetime objekt cílového data
        cycle_day: Den v 28denním cyklu
        meals: Dictionary s jídly
        
    Returns:
        Naformátovaný string
    """
    output = []
    
    day_name = get_czech_day_name(target_date)
    date_str = target_date.strftime(f"%d.%m.%Y ({day_name})")
    
    output.append("=" * 70)
    output.append(f"🍽️  JÍDELNÍČEK - {date_str}")
    output.append("=" * 70)
    output.append(f"Den {cycle_day} z 28denního cyklu")
    output.append("=" * 70)
    output.append("")
    
    output.append("🌅 SNÍDANĚ")
    output.append(f"   {meals['snídaně']}")
    output.append("")
    
    output.append("🍎 DOPOLEDNÍ SVAČINA")
    output.append(f"   {meals['dopolední_svačina']}")
    output.append("")
    
    output.append("🍽️  OBĚD")
    output.append(f"   {meals['oběd']}")
    output.append("")
    
    output.append("🥤 ODPOLEDNÍ SVAČINA")
    output.append(f"   {meals['odpolední_svačina']}")
    output.append("")
    
    output.append("🌙 VEČEŘE")
    output.append(f"   {meals['večeře']}")
    output.append("")
    
    output.append("=" * 70)
    output.append("")
    
    # Pokud jsou v jídle vegetariánské varianty, zvýrazníme je
    has_vegetarian = any("vegetarián" in str(meal).lower() for meal in meals.values())
    if has_vegetarian:
        output.append("💡 Tip: Jídla obsahují i vegetariánské varianty!")
        output.append("")
    
    return "\n".join(output)


def extract_ingredients_from_meals(meals):
    """
    Extrahuje ingredience z jídel.
    
    Args:
        meals: Dictionary s jídly
        
    Returns:
        Sorted list ingrediencí
    """
    all_meals_text = " ".join([
        meal for meal_type, meal in meals.items() 
        if meal_type != 'den'
    ]).lower()
    
    # Seznam běžných ingrediencí k detekci
    common_ingredients = [
        "bílý jogurt", "vlašské ořechy", "med", "skořice", "rozinky",
        "hruška", "jablko", "ananas", "kiwi", "pomelo", "ovocné pyré",
        "červená řepa", "cibule", "tuňák", "vejce", "vařené vejce",
        "okurka", "okurkový salát", "salát", "kuřecí prsa", "brokolice",
        "česnek", "strouhaný sýr", "zázvor", "fazolové lusky",
        "mrkev", "cuketové placky", "cuketa", "dýně", "jáhly",
        "sušené švestky", "mandlemi", "ředkvičkový salát", "ředkvičky",
        "zeleninový krém", "zeleninový salát"
    ]
    
    ingredients_found = []
    for ingredient in common_ingredients:
        if ingredient in all_meals_text:
            if ingredient not in ingredients_found:
                ingredients_found.append(ingredient)
    
    return sorted(ingredients_found)


def main():
    """Hlavní funkce - generuje jídelníček pro zvolené datum"""
    
    # Parsujeme argumenty
    date_arg = sys.argv[1] if len(sys.argv) > 1 else "today"
    
    target_date = parse_date_argument(date_arg)
    if target_date is None:
        sys.exit(1)
    
    # Vypočítáme den v cyklu
    cycle_day = get_cycle_day_for_date(target_date)
    
    # Načteme jídelníček pro tento den
    meals = get_meal_for_day(cycle_day)
    
    if meals is None:
        print("Chyba: Nepodařilo se načíst jídelníček!")
        sys.exit(1)
    
    # Vytiskneme jídelníček
    print(format_meal_plan(target_date, cycle_day, meals))
    
    # Vygenerujeme nákupní seznam
    print("🛒 HLAVNÍ INGREDIENCE")
    print("=" * 70)
    
    ingredients = extract_ingredients_from_meals(meals)
    if ingredients:
        for ingredient in ingredients:
            print(f"   ✓ {ingredient}")
    else:
        print("   (žádné specifické ingredience nenalezeny)")
    
    print("\n" + "=" * 70)
    print("\n💡 TIPY PRO PŘÍPRAVU:")
    print("   • Některá jídla lze připravit předem")
    print("   • Využívejte vegetariánské varianty podle preference")
    print("   • Připravte si ingredience den předem pro rychlejší vaření")
    print("\n✅ Příjemnou chuť!")
    print()


if __name__ == '__main__':
    main()
