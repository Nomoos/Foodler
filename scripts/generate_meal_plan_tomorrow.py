#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor jídelníčku na zítra (18.1.2026)
Meal plan generator for tomorrow (18.1.2026)
"""

import json
from datetime import datetime, timedelta

# Cesta k meal plan datům
MEAL_PLAN_JSON = 'data/meal_plans/meal_plan_28_days.json'


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
            'večeře': day['dinner'],
            'večerní_svačina': day.get('evening_snack', '')
        }
    return None


def format_meal_plan(date_str, cycle_day, meals):
    """
    Formátuje jídelníček do pěkného výstupu.
    
    Args:
        date_str: Datum jako string
        cycle_day: Den v 28denním cyklu
        meals: Dictionary s jídly
        
    Returns:
        Naformátovaný string
    """
    output = []
    output.append("=" * 70)
    output.append(f"🍽️  JÍDELNÍČEK NA ZÍTRA - {date_str}")
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
    
    if meals.get('večerní_svačina'):
        output.append("🌃 VEČERNÍ SVAČINA")
        output.append(f"   {meals['večerní_svačina']}")
        output.append("")
    
    output.append("=" * 70)
    output.append("")
    
    # Pokud jsou v jídle vegetariánské varianty, zvýrazníme je
    has_vegetarian = any("vegetarián" in str(meal).lower() for meal in meals.values())
    if has_vegetarian:
        output.append("💡 Tip: Jídla obsahují i vegetariánské varianty!")
        output.append("")
    
    return "\n".join(output)


def generate_shopping_list(meals):
    """
    Vygeneruje nákupní seznam z jídel.
    
    Args:
        meals: Dictionary s jídly
        
    Returns:
        List ingrediencí
    """
    # Jednoduchý parsing ingrediencí z názvů jídel
    ingredients = set()
    
    for meal_name, meal_content in meals.items():
        if meal_name == 'den':
            continue
        # Rozdělíme jídlo podle čárek a "/"
        parts = meal_content.replace('/', ',').split(',')
        for part in parts:
            part = part.strip()
            if part and not part.startswith('Vegetarián'):
                # Přidáme jednotlivé ingredience
                ingredients.add(part)
    
    return sorted(list(ingredients))


def main():
    """Hlavní funkce - generuje jídelníček na zítra"""
    
    # Zítra je 18.1.2026 (jak uvedeno v požadavku)
    tomorrow = datetime(2026, 1, 18)
    
    # Vypočítáme den v cyklu
    cycle_day = get_cycle_day_for_date(tomorrow)
    
    # Načteme jídelníček pro tento den
    meals = get_meal_for_day(cycle_day)
    
    if meals is None:
        print("Chyba: Nepodařilo se načíst jídelníček!")
        return
    
    # Vytiskneme jídelníček
    date_str = "18.01.2026 (sobota)"  # Přesné datum z požadavku
    
    print(format_meal_plan(date_str, cycle_day, meals))
    
    # Vygenerujeme nákupní seznam
    print("🛒 NÁKUPNÍ SEZNAM")
    print("=" * 70)
    
    # Pro lepší organizaci rozdělíme ingredience podle typu
    print("\n📝 Ingredience pro přípravu jídel:")
    
    all_meals_text = " ".join([
        meal for meal_type, meal in meals.items() 
        if meal_type != 'den'
    ]).lower()
    
    # Extrahujeme běžné ingredience
    common_ingredients = [
        "bílý jogurt", "vlašské ořechy", "med", "skořice",
        "hruška", "červená řepa", "cibule", "tuňák", "vejce",
        "okurka", "salát", "kuřecí prsa", "brokolice"
    ]
    
    ingredients_found = []
    for ingredient in common_ingredients:
        if ingredient in all_meals_text:
            if ingredient not in ingredients_found:
                ingredients_found.append(ingredient)
    
    for ingredient in sorted(ingredients_found):
        print(f"   ✓ {ingredient}")
    
    print("\n" + "=" * 70)
    print("\n💡 TIPY PRO PŘÍPRAVU:")
    print("   • Některá jídla lze připravit předem (např. salát z červené řepy)")
    print("   • Vejce nebo tuňák lze zvolit podle preference (oběd)")
    print("   • Kuřecí prsa nebo brokolicové karbanátky (večeře - vegetariánská varianta)")
    print("\n✅ Příjemnou chuť!")
    print()


if __name__ == '__main__':
    main()
