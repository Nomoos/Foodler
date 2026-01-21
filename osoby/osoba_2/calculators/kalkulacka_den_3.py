#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kalkulačka makronutrientů pro Páju - Den 3
Vypočítá přesné makronutrienty z aktuálních potravin a navrhne doplňky
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class Food:
    """Potravina s nutričními hodnotami na 100g."""
    name: str
    calories: float  # kcal
    protein: float   # g
    carbs: float     # g
    fat: float       # g
    fiber: float = 0.0  # g
    
    def calculate_portion(self, grams: float) -> 'FoodPortion':
        """Vypočítá nutriční hodnoty pro danou porci."""
        multiplier = grams / 100
        return FoodPortion(
            name=f"{self.name} {grams}g",
            calories=self.calories * multiplier,
            protein=self.protein * multiplier,
            carbs=self.carbs * multiplier,
            fat=self.fat * multiplier,
            fiber=self.fiber * multiplier
        )


@dataclass
class FoodPortion:
    """Porce jídla s vypočítanými nutričními hodnotami."""
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float = 0.0
    
    def __str__(self) -> str:
        return (f"{self.name:40s} | "
                f"{self.calories:6.0f} kcal | "
                f"{self.protein:5.1f}g P | "
                f"{self.carbs:5.1f}g C | "
                f"{self.fat:5.1f}g F | "
                f"{self.fiber:5.1f}g fiber")


# Databáze potravin (nutriční hodnoty na 100g)
FOODS_DB = {
    'susene_fiky': Food('Sušené fíky', 274, 3.8, 64.0, 1.2, 9.0),
    'cottage_cheese': Food('Cottage cheese', 98, 14.0, 4.0, 4.0, 0.0),
    'ledovy_salat': Food('Ledový salát', 16.1, 0.7, 2.0, 0.14, 1.2),
    'kapusta': Food('Kapusta bílá', 25, 1.3, 5.8, 0.1, 2.5),
    'vejce': Food('Vejce natvrdo', 155, 13.0, 1.1, 11.0, 0.0),
    'tunak_olej': Food('Tuňák v oleji', 198, 26.5, 0.0, 10.0, 0.0),
    'kurice_prsa': Food('Kuřecí prsa', 165, 31.0, 0.0, 3.6, 0.0),
    'hovezi_maso': Food('Hovězí libové', 186, 26.0, 0.0, 8.5, 0.0),
    'spinat': Food('Špenát', 23, 2.9, 3.6, 0.4, 2.2),
    'brokolice': Food('Brokolice', 34, 2.8, 7.0, 0.4, 2.6),
    'cuketa': Food('Cuketa', 17, 1.2, 3.1, 0.3, 1.0),
    'mandle': Food('Mandle', 579, 21.0, 22.0, 50.0, 12.0),
    'vlaske_orechy': Food('Vlašské ořechy', 654, 15.2, 13.7, 65.2, 6.7),
    'recky_jogurt': Food('Řecký jogurt', 97, 10.0, 4.0, 5.0, 0.0),
    'olivy': Food('Olivy', 115, 0.8, 6.3, 10.7, 3.2),
    'olivovy_olej': Food('Olivový olej', 884, 0.0, 0.0, 100.0, 0.0),
}


def calculate_meal(meal_name: str, foods: List[Tuple[str, float]]) -> Dict:
    """
    Vypočítá makronutrienty pro jedno jídlo.
    
    Args:
        meal_name: Název jídla (např. "Snídaně")
        foods: Seznam (název_potraviny, gramy)
    
    Returns:
        Slovník s vypočítanými makry
    """
    print(f"\n{'='*80}")
    print(f"{meal_name}")
    print(f"{'='*80}")
    
    total = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0}
    
    for food_key, grams in foods:
        if food_key not in FOODS_DB:
            print(f"⚠️  VAROVÁNÍ: {food_key} není v databázi!")
            continue
        
        food = FOODS_DB[food_key]
        portion = food.calculate_portion(grams)
        print(f"  {portion}")
        
        total['calories'] += portion.calories
        total['protein'] += portion.protein
        total['carbs'] += portion.carbs
        total['fat'] += portion.fat
        total['fiber'] += portion.fiber
    
    print(f"{'-'*80}")
    print(f"{'CELKEM:':40s} | "
          f"{total['calories']:6.0f} kcal | "
          f"{total['protein']:5.1f}g P | "
          f"{total['carbs']:5.1f}g C | "
          f"{total['fat']:5.1f}g F | "
          f"{total['fiber']:5.1f}g fiber")
    
    return total


def main():
    """Hlavní program - kalkulace dne pro Páju."""
    
    print("\n" + "="*80)
    print(" "*20 + "PÁJA - DEN 3 - VÝPOČET MAKRONUTRIENTŮ")
    print("="*80)
    
    # Cíle Páji
    targets = {
        'calories': 1508,
        'protein': 92,
        'carbs': 60,  # maximum
        'fat': 100,
        'fiber': 20
    }
    
    print("\n🎯 DENNÍ CÍLE:")
    print(f"   Kalorie: {targets['calories']} kcal")
    print(f"   Bílkoviny: min {targets['protein']}g")
    print(f"   Sacharidy: max {targets['carbs']}g")
    print(f"   Tuky: {targets['fat']}g")
    print(f"   Vláknina: min {targets['fiber']}g")
    
    # Definice jídel s aktuálními potravinami
    meals = []
    
    # Snídaně - zbytky
    meals.append(calculate_meal(
        "🌅 SNÍDANĚ (7:00) - Zbytky z úterý",
        [
            ('vejce', 55),
            ('tunak_olej', 60),
            ('ledovy_salat', 50),
        ]
    ))
    
    # Dopolední svačina
    meals.append(calculate_meal(
        "🍎 DOPOLEDNÍ SVAČINA (10:00)",
        [
            ('cottage_cheese', 90),
            ('mandle', 15),
        ]
    ))
    
    # Oběd - varianta s cottage
    meals.append(calculate_meal(
        "🍽️ OBĚD (12:30) - Varianta cottage",
        [
            ('cottage_cheese', 90),
            ('kapusta', 40),
            ('vejce', 55),
        ]
    ))
    
    # Odpolední svačina - fíky!
    meals.append(calculate_meal(
        "🥤 ODPOLEDNÍ SVAČINA (15:30) - Sladká odměna",
        [
            ('susene_fiky', 20),  # 2 fíky
            ('vlaske_orechy', 10),
        ]
    ))
    
    # Večeře
    meals.append(calculate_meal(
        "🌙 VEČEŘE (18:30) - Doma",
        [
            ('hovezi_maso', 140),
            ('cuketa', 120),
            ('brokolice', 100),
            ('olivovy_olej', 10),
        ]
    ))
    
    # Večerní svačina
    meals.append(calculate_meal(
        "🌃 VEČERNÍ SVAČINA (21:00)",
        [
            ('susene_fiky', 20),  # 2 fíky
            ('recky_jogurt', 80),
        ]
    ))
    
    # Celkový součet
    print("\n" + "="*80)
    print(" "*25 + "CELKOVÝ DENNÍ SOUČET")
    print("="*80)
    
    daily_total = {
        'calories': sum(m['calories'] for m in meals),
        'protein': sum(m['protein'] for m in meals),
        'carbs': sum(m['carbs'] for m in meals),
        'fat': sum(m['fat'] for m in meals),
        'fiber': sum(m['fiber'] for m in meals),
    }
    
    print(f"\n{'Makronutrient':20s} | {'Cíl':>10s} | {'Skutečnost':>12s} | {'Rozdíl':>10s} | Status")
    print("-"*80)
    
    for key, target in targets.items():
        actual = daily_total[key]
        diff = actual - target
        
        # Pro sacharidy je cíl maximum, takže invertujeme logiku
        if key == 'carbs':
            status = "✅" if actual <= target else "⚠️"
            diff_str = f"{diff:+.1f}g"
        elif key in ['protein', 'fiber']:
            status = "✅" if actual >= target else "⚠️"
            diff_str = f"{diff:+.1f}g"
        else:
            status = "✅" if abs(diff) <= target * 0.1 else "🟡"  # 10% tolerance
            diff_str = f"{diff:+.0f}"
        
        unit = "kcal" if key == 'calories' else "g"
        print(f"{key.capitalize():20s} | {target:>8.0f}{unit:2s} | "
              f"{actual:>10.1f}{unit:2s} | {diff_str:>10s} | {status}")
    
    print("="*80)
    
    # Doporučení
    print("\n💡 DOPORUČENÍ:")
    
    if daily_total['protein'] < targets['protein']:
        deficit = targets['protein'] - daily_total['protein']
        print(f"   ⚠️  Chybí {deficit:.0f}g bílkovin")
        print(f"       → Přidej: tuňák 80g (+21g) nebo vejce 2 ks (+26g)")
    
    if daily_total['carbs'] > targets['carbs']:
        excess = daily_total['carbs'] - targets['carbs']
        print(f"   ⚠️  Překročeny sacharidy o {excess:.0f}g")
        print(f"       → Zvaž méně fíků nebo jiné zeleniny")
    
    if daily_total['calories'] < targets['calories'] * 0.85:
        deficit = targets['calories'] - daily_total['calories']
        print(f"   🟡 Chybí {deficit:.0f} kcal")
        print(f"       → Přidej: ořechy 30g (+180kcal) nebo avokádo 50g (+80kcal)")
    
    if daily_total['fiber'] < targets['fiber']:
        deficit = targets['fiber'] - daily_total['fiber']
        print(f"   🟡 Chybí {deficit:.1f}g vlákniny")
        print(f"       → Přidej: chia semínka 15g (+5g) nebo více zeleniny")
    
    if all([
        daily_total['protein'] >= targets['protein'],
        daily_total['carbs'] <= targets['carbs'],
        daily_total['calories'] >= targets['calories'] * 0.85
    ]):
        print("   ✅ Skvělý plán! Všechny cíle splněny!")
    
    print("\n" + "="*80)
    print(" "*30 + "HOTOVO! ✨")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
