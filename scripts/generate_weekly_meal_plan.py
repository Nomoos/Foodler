#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor týdenního jídelníčku
Weekly meal plan generator

Generuje kompletní jídelníček na celý týden (7 dní) a uloží ho do souboru.

Usage:
    python generate_weekly_meal_plan.py 19.1.2026         # Start date
    python generate_weekly_meal_plan.py 2026-01-19        # Start date (ISO format)
"""

import json
import sys
import os
from datetime import datetime, timedelta

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


def generate_weekly_plan(start_date, meal_plan_data):
    """
    Vygeneruje týdenní jídelníček od zadaného data.
    
    Args:
        start_date: datetime objekt pro začátek týdne
        meal_plan_data: Načtená data z JSON souboru
        
    Returns:
        Dictionary s týdenním plánem
    """
    weekly_plan = {
        "week_start": start_date.strftime("%d.%m.%Y"),
        "week_end": (start_date + timedelta(days=6)).strftime("%d.%m.%Y"),
        "generated": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "days": []
    }
    
    days_data = meal_plan_data['meal_plan']['days']
    
    for day_offset in range(7):
        current_date = start_date + timedelta(days=day_offset)
        cycle_day = get_cycle_day_for_date(current_date)
        
        # Najdeme den v cyklu (cycle_day je 1-28, index je 0-27)
        day_data = days_data[cycle_day - 1]
        
        day_info = {
            "date": current_date.strftime("%d.%m.%Y"),
            "day_name": get_czech_day_name(current_date),
            "cycle_day": cycle_day,
            "breakfast": day_data.get("breakfast", ""),
            "morning_snack": day_data.get("morning_snack", ""),
            "lunch": day_data.get("lunch", ""),
            "afternoon_snack": day_data.get("afternoon_snack", ""),
            "dinner": day_data.get("dinner", ""),
            "evening_snack": day_data.get("evening_snack", "")
        }
        
        weekly_plan["days"].append(day_info)
    
    return weekly_plan


def print_weekly_plan(weekly_plan):
    """Vytiskne týdenní jídelníček v hezké formě"""
    print("\n" + "="*70)
    print(f"🍽️  TÝDENNÍ JÍDELNÍČEK")
    print(f"📅  {weekly_plan['week_start']} - {weekly_plan['week_end']}")
    print("="*70)
    
    for day in weekly_plan['days']:
        print(f"\n{'='*70}")
        print(f"📆 {day['day_name'].upper()} - {day['date']}")
        print(f"   (Den {day['cycle_day']} z 28denního cyklu)")
        print(f"{'='*70}")
        
        print(f"\n🌅 SNÍDANĚ")
        print(f"   {day['breakfast']}")
        
        print(f"\n🍎 DOPOLEDNÍ SVAČINA")
        print(f"   {day['morning_snack']}")
        
        print(f"\n🍽️  OBĚD")
        print(f"   {day['lunch']}")
        
        print(f"\n🥤 ODPOLEDNÍ SVAČINA")
        print(f"   {day['afternoon_snack']}")
        
        print(f"\n🌙 VEČEŘE")
        print(f"   {day['dinner']}")
        
        if day.get('evening_snack'):
            print(f"\n🌃 VEČERNÍ SVAČINA")
            print(f"   {day['evening_snack']}")
    
    print("\n" + "="*70)
    print("✅ Příjemnou chuť po celý týden!")
    print("="*70 + "\n")


def save_weekly_plan(weekly_plan, filename):
    """Uloží týdenní jídelníček do JSON souboru"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, WEEKLY_PLANS_DIR)
    
    # Vytvoř složku pokud neexistuje
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(weekly_plan, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Jídelníček uložen do: {output_path}\n")


def main():
    """Hlavní funkce"""
    # Parsuj argumenty
    if len(sys.argv) < 2:
        print("Použití: python generate_weekly_meal_plan.py <datum>")
        print("Příklad: python generate_weekly_meal_plan.py 19.1.2026")
        sys.exit(1)
    
    start_date = parse_date_argument(sys.argv[1])
    if start_date is None:
        sys.exit(1)
    
    # Načti meal plan data
    meal_plan_data = load_meal_plan_json()
    if meal_plan_data is None:
        sys.exit(1)
    
    # Vygeneruj týdenní plán
    weekly_plan = generate_weekly_plan(start_date, meal_plan_data)
    
    # Vytiskni plán
    print_weekly_plan(weekly_plan)
    
    # Ulož do souboru
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = (start_date + timedelta(days=6)).strftime("%Y-%m-%d")
    filename = f"weekly_plan_{start_str}_to_{end_str}.json"
    save_weekly_plan(weekly_plan, filename)


if __name__ == '__main__':
    main()
