#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Příklad použití 28denního jídelníčku
Example usage of the 28-day meal plan
"""

import json
import csv
from datetime import datetime, timedelta

def load_meal_plan_json():
    """Načte jídelníček z JSON souboru"""
    try:
        with open('meal_plan_28_days.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Chyba: Soubor 'meal_plan_28_days.json' nenalezen!")
        return None
    except json.JSONDecodeError as e:
        print(f"Chyba: Neplatný JSON formát - {e}")
        return None

def load_meal_plan_csv():
    """Načte jídelníček z CSV souboru"""
    try:
        with open('meal_plan_28_days.csv', 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print("Chyba: Soubor 'meal_plan_28_days.csv' nenalezen!")
        return None

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
            'dopolední svačina': day['morning_snack'],
            'oběd': day['lunch'],
            'odpolední svačina': day['afternoon_snack'],
            'večeře': day['dinner']
        }
    return None

def print_day_menu(day_number):
    """Vytiskne menu pro daný den"""
    meal = get_meal_for_day(day_number)
    if meal:
        print(f"\n{'='*60}")
        print(f"DEN {meal['den']}")
        print(f"{'='*60}")
        print(f"🌅 Snídaně:            {meal['snídaně']}")
        print(f"🍎 Dopolední svačina:  {meal['dopolední svačina']}")
        print(f"🍽️  Oběd:              {meal['oběd']}")
        print(f"🥤 Odpolední svačina:  {meal['odpolední svačina']}")
        print(f"🌙 Večeře:             {meal['večeře']}")
        print(f"{'='*60}\n")

def get_week_menu(start_day):
    """Získá menu pro celý týden od daného dne"""
    week = []
    for i in range(7):
        day_num = ((start_day - 1 + i) % 28) + 1
        week.append(get_meal_for_day(day_num))
    return week

def print_week_menu(start_day):
    """Vytiskne menu na celý týden"""
    print(f"\n{'='*60}")
    print(f"MENU NA TÝDEN (dny {start_day}-{min(start_day+6, 28)})")
    print(f"{'='*60}")
    
    week = get_week_menu(start_day)
    for meal in week:
        if meal:
            print(f"\nDen {meal['den']}:")
            print(f"  Snídaně: {meal['snídaně']}")
            print(f"  Oběd:    {meal['oběd']}")
            print(f"  Večeře:  {meal['večeře']}")

def find_meals_with_ingredient(ingredient):
    """Najde všechna jídla obsahující danou ingredienci"""
    data = load_meal_plan_json()
    if data is None:
        return []
    results = []
    
    for day in data['meal_plan']['days']:
        day_meals = []
        for meal_type, meal_name in [
            ('Snídaně', day['breakfast']),
            ('Dopolední svačina', day['morning_snack']),
            ('Oběd', day['lunch']),
            ('Odpolední svačina', day['afternoon_snack']),
            ('Večeře', day['dinner'])
        ]:
            if ingredient.lower() in meal_name.lower():
                day_meals.append(f"{meal_type}: {meal_name}")
        
        if day_meals:
            results.append((day['day'], day_meals))
    
    return results

def print_ingredient_search(ingredient):
    """Vytiskne výsledky hledání ingredience"""
    results = find_meals_with_ingredient(ingredient)
    print(f"\n{'='*60}")
    print(f"Hledání ingredience: '{ingredient}'")
    print(f"Nalezeno v {len(results)} dnech")
    print(f"{'='*60}")
    
    for day, meals in results:
        print(f"\nDen {day}:")
        for meal in meals:
            print(f"  {meal}")

def main():
    """Hlavní funkce - příklady použití"""
    
    # Příklad 1: Zobrazit menu pro den 1
    print("\n=== PŘÍKLAD 1: Menu pro konkrétní den ===")
    print_day_menu(1)
    
    # Příklad 2: Zobrazit menu na týden
    print("\n=== PŘÍKLAD 2: Menu na první týden ===")
    print_week_menu(1)
    
    # Příklad 3: Najít všechna jídla s brokolici
    print("\n=== PŘÍKLAD 3: Hledání ingredience ===")
    print_ingredient_search("brokolice")
    
    # Příklad 4: Získat aktuální den v cyklu (od začátku roku)
    print("\n=== PŘÍKLAD 4: Aktuální den v cyklu ===")
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    days_since_start = (now - start_of_year).days
    current_cycle_day = (days_since_start % 28) + 1
    print(f"Aktuální datum: {now.strftime('%Y-%m-%d')}")
    print(f"Den v 28denním cyklu: {current_cycle_day}")
    print_day_menu(current_cycle_day)
    
    # Příklad 5: Statistiky
    print("\n=== PŘÍKLAD 5: Statistiky ===")
    data = load_meal_plan_json()
    if data is None:
        print("Nelze načíst data pro statistiky")
        return
    
    # Počet vegetariánských možností
    vege_count = sum(1 for day in data['meal_plan']['days'] 
                     if 'vegetarián' in day['lunch'].lower() or 'vegetarián' in day['dinner'].lower())
    print(f"Dny s vegetariánskou variantou: {vege_count}")
    
    # Nejčastější snídaně
    breakfasts = {}
    for day in data['meal_plan']['days']:
        b = day['breakfast']
        breakfasts[b] = breakfasts.get(b, 0) + 1
    
    most_common = max(breakfasts.items(), key=lambda x: x[1])
    print(f"\nNejčastější snídaně ({most_common[1]}x):")
    print(f"  {most_common[0]}")

if __name__ == '__main__':
    main()
