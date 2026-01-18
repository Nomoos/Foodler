#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor optimalizovaného jídelníčku pro konkrétní datum
Optimized meal plan generator for specific dates using fitness functions

Použití:
    python generate_optimized_plan.py                    # Dnes
    python generate_optimized_plan.py tomorrow           # Zítra
    python generate_optimized_plan.py 19.1.2026          # Konkrétní datum
"""

import sys
from datetime import datetime, timedelta
from typing import Optional

# Import meal planner modules
from src.planners.day_plan_builder import (
    DayPlanBuilder, FitnessThresholds, Meal, MealType, DayPlan
)

# Import profile and meal database
from osoby.osoba_1.profil import OsobniProfil
from jidla.databaze import DatabzeJidel


def parse_date_argument(arg: Optional[str] = None) -> datetime:
    """Parse date argument from command line."""
    if arg is None or arg.lower() == "today":
        return datetime.now()
    elif arg.lower() == "tomorrow":
        return datetime.now() + timedelta(days=1)
    else:
        # Try parsing Czech format (DD.M.YYYY)
        try:
            return datetime.strptime(arg, "%d.%m.%Y")
        except ValueError:
            pass
        # Try ISO format (YYYY-MM-DD)
        try:
            return datetime.strptime(arg, "%Y-%m-%d")
        except ValueError:
            print(f"❌ Neplatný formát data: {arg}")
            print("   Použijte: DD.M.YYYY nebo YYYY-MM-DD nebo 'tomorrow'")
            sys.exit(1)


def convert_jidla_to_meals() -> list[Meal]:
    """Convert Czech meal database to English Meal objects for planner."""
    meals = []
    
    # Map Czech meal types to English enum
    typ_map = {
        "snidane": MealType.BREAKFAST,
        "obed": MealType.LUNCH,
        "vecere": MealType.DINNER,
        "svacina": MealType.AFTERNOON_SNACK,
        "dopoledni_svacina": MealType.MORNING_SNACK
    }
    
    for jidlo in DatabzeJidel.JIDLA:
        # Get meal type or default to lunch
        meal_type = typ_map.get(jidlo.typ, MealType.LUNCH)
        
        # Extract ingredients list
        ingredients = [ing.nazev for ing in jidlo.ingredience]
        
        # Calculate per-portion values
        makra = jidlo.vypocitej_makra_na_porci()
        
        meal = Meal(
            name=jidlo.nazev,
            meal_type=meal_type,
            calories=makra["kalorie"],
            protein_g=makra["bilkoviny"],
            carbs_g=makra["sacharidy"],
            fat_g=makra["tuky"],
            fiber_g=makra["vlaknina"],
            ingredients=ingredients,
            preparation_time_min=jidlo.priprava_cas_min,
            cost_estimate=0.0  # Could be added later
        )
        meals.append(meal)
    
    return meals


def generate_optimized_plan_for_date(target_date: datetime):
    """Generate optimized meal plan for specific date using fitness functions."""
    
    # Load profile
    profil = OsobniProfil()
    
    # Create fitness thresholds from profile
    thresholds = FitnessThresholds(
        target_calories=profil.cil_kalorie,
        target_protein_g=profil.cil_bilkoviny,
        target_carbs_g=profil.cil_sacharidy,
        target_fat_g=profil.cil_tuky,
        min_fiber_g=profil.cil_vlaknina,
        max_daily_cost=500.0,  # CZK
        max_daily_prep_time=120  # minutes
    )
    
    # Create day plan builder
    builder = DayPlanBuilder(thresholds)
    
    # Convert meals from database
    meals = convert_jidla_to_meals()
    builder.set_meal_database(meals)
    
    print("=" * 70)
    print(f"🍽️  OPTIMALIZOVANÝ JÍDELNÍČEK - {target_date.strftime('%d.%m.%Y (%A)')}")
    print("=" * 70)
    print(f"Profil: {profil.jmeno}")
    print(f"Cíle: {profil.cil_kalorie} kcal | P: {profil.cil_bilkoviny}g | "
          f"C: {profil.cil_sacharidy}g | F: {profil.cil_tuky}g")
    print("=" * 70)
    print()
    
    # Build optimized plan
    print("🔄 Generování optimalizovaného plánu...")
    print(f"   Databáze: {len(meals)} jídel")
    print(f"   Iterace: 1000 kombinací")
    print()
    
    plan, score = builder.build_optimized_plan(
        num_meals=profil.pocet_jidel,
        iterations=1000
    )
    
    # Set date on plan
    plan.date = target_date.strftime("%Y-%m-%d")
    
    # Display results
    print("=" * 70)
    print("📋 DENNÍ JÍDELNÍČEK")
    print("=" * 70)
    print()
    
    # Group meals by type
    meal_type_names = {
        MealType.BREAKFAST: "🌅 SNÍDANĚ",
        MealType.MORNING_SNACK: "🍎 DOPOLEDNÍ SVAČINA",
        MealType.LUNCH: "🍽️  OBĚD",
        MealType.AFTERNOON_SNACK: "🥤 ODPOLEDNÍ SVAČINA",
        MealType.DINNER: "🌙 VEČEŘE",
        MealType.EVENING_SNACK: "🌃 VEČERNÍ SVAČINA"
    }
    
    for meal_type in MealType:
        type_meals = [m for m in plan.meals if m.meal_type == meal_type]
        if type_meals:
            print(meal_type_names[meal_type])
            for meal in type_meals:
                print(f"   {meal.name}")
                print(f"   {meal.calories:.0f} kcal | "
                      f"P: {meal.protein_g:.0f}g | "
                      f"C: {meal.carbs_g:.0f}g | "
                      f"F: {meal.fat_g:.0f}g | "
                      f"Vláknina: {meal.fiber_g:.0f}g")
                print(f"   Příprava: {meal.preparation_time_min} min")
                if meal.ingredients:
                    print(f"   Ingredience: {', '.join(meal.ingredients[:3])}...")
                print()
    
    # Display totals
    print("=" * 70)
    print("📊 DENNÍ SOUČTY")
    print("=" * 70)
    totals = plan.get_total_macros()
    print(f"Kalorie:  {totals['calories']:.0f} kcal (cíl: {profil.cil_kalorie})")
    print(f"Bílkoviny: {totals['protein']:.0f}g (cíl: {profil.cil_bilkoviny}g)")
    print(f"Sacharidy: {totals['carbs']:.0f}g (cíl: {profil.cil_sacharidy}g)")
    print(f"Tuky:      {totals['fat']:.0f}g (cíl: {profil.cil_tuky}g)")
    print(f"Vláknina:  {totals['fiber']:.0f}g (min: {profil.cil_vlaknina}g)")
    print(f"Celkový čas přípravy: {plan.get_total_time()} min")
    print()
    
    # Display fitness score
    print("=" * 70)
    print("⭐ FITNESS SKÓRE")
    print("=" * 70)
    print(f"Celkové skóre: {score.total_score:.1f}/100")
    print()
    print(f"  Kalorie:     {score.calorie_score:.1f}/100")
    print(f"  Bílkoviny:   {score.protein_score:.1f}/100")
    print(f"  Sacharidy:   {score.carbs_score:.1f}/100")
    print(f"  Tuky:        {score.fat_score:.1f}/100")
    print(f"  Vláknina:    {score.fiber_score:.1f}/100")
    print(f"  Cena:        {score.cost_score:.1f}/100")
    print(f"  Čas:         {score.time_score:.1f}/100")
    print(f"  Distribuce:  {score.meal_distribution_score:.1f}/100")
    print()
    
    if score.is_acceptable():
        print("✅ Plán splňuje všechny požadavky!")
    else:
        print("⚠️  Plán nesplňuje všechny požadavky (pod prahem 70/100)")
    
    print()
    print("=" * 70)
    print("💡 NÁKUPNÍ SEZNAM")
    print("=" * 70)
    
    # Collect all ingredients
    all_ingredients = set()
    egg_count = 0
    for meal in plan.meals:
        all_ingredients.update(meal.ingredients)
        # Count eggs used
        for ingredient in meal.ingredients:
            if "vejce" in ingredient.lower():
                # Find the meal to get exact egg count
                for m in plan.meals:
                    if ingredient in m.ingredients:
                        # Estimate egg count from meal name
                        if "3 vejce" in m.name or "3 ks" in m.name:
                            egg_count += 3
                        elif "4 vejce" in m.name:
                            egg_count += 4
                        elif "2 vejce" in m.name:
                            egg_count += 2
                        elif ingredient == "Vejce" or ingredient == "Vejce slepičí M":
                            # Default to 2 eggs if not specified
                            egg_count += 2
                        break
    
    # Show egg usage prominently
    if egg_count > 0:
        print("=" * 70)
        print("🥚 SPOTŘEBA VAJEC")
        print("=" * 70)
        print(f"Celkem použito: {egg_count} vajec")
        print(f"Zbývá v lednici: {40 - egg_count} vajec (z původních 40)")
        print()
    
    for ingredient in sorted(all_ingredients):
        print(f"   ✓ {ingredient}")
    
    print()
    print("=" * 70)
    print("✅ Příjemnou chuť!")
    print("=" * 70)
    
    return plan, score


def main():
    """Main entry point."""
    # Parse date argument
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    target_date = parse_date_argument(arg)
    
    # Generate plan
    plan, score = generate_optimized_plan_for_date(target_date)
    
    # Return success if plan is acceptable
    if score.is_acceptable():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
