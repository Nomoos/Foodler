#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kalkulačka makronutrientů pro Páju - Den 3 - MINIMÁLNÍ VARIANTA
Vypočítá přesné makronutrienty JEN z toho, co má Pája u sebe
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
        return (f"{self.name:45s} | "
                f"{self.calories:6.0f} kcal | "
                f"{self.protein:5.1f}g P | "
                f"{self.carbs:5.1f}g C | "
                f"{self.fat:5.1f}g F | "
                f"{self.fiber:5.1f}g fiber")


# Databáze potravin (nutriční hodnoty na 100g)
FOODS_DB = {
    # Co má Pája u sebe
    'susene_fiky': Food('Sušené fíky', 274, 3.8, 64.0, 1.2, 9.0),
    'kesu': Food('Kešu ořechy', 580, 18.2, 33.0, 46.3, 3.3),
    'cottage_cheese': Food('Cottage cheese', 98, 14.0, 4.0, 4.0, 0.0),
    'ledovy_salat': Food('Ledový salát', 16.1, 0.7, 2.0, 0.14, 1.2),
    
    # Co by měla přidat (pro srovnání)
    'vejce': Food('Vejce natvrdo', 155, 13.0, 1.1, 11.0, 0.0),
    'tunak_olej': Food('Tuňák v oleji', 198, 26.5, 0.0, 10.0, 0.0),
    'kurice_prsa': Food('Kuřecí prsa', 165, 31.0, 0.0, 3.6, 0.0),
    'hovezi_maso': Food('Hovězí libové', 186, 26.0, 0.0, 8.5, 0.0),
    'brokolice': Food('Brokolice', 34, 2.8, 7.0, 0.4, 2.6),
    'cuketa': Food('Cuketa', 17, 1.2, 3.1, 0.3, 1.0),
    'olivovy_olej': Food('Olivový olej', 884, 0.0, 0.0, 100.0, 0.0),
    'recky_jogurt': Food('Řecký jogurt', 97, 10.0, 4.0, 5.0, 0.0),
}


def calculate_meal(meal_name: str, foods: List[Tuple[str, float]]) -> Dict:
    """Vypočítá makronutrienty pro jedno jídlo."""
    print(f"\n{'='*90}")
    print(f"{meal_name}")
    print(f"{'='*90}")
    
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
    
    print(f"{'-'*90}")
    print(f"{'CELKEM:':45s} | "
          f"{total['calories']:6.0f} kcal | "
          f"{total['protein']:5.1f}g P | "
          f"{total['carbs']:5.1f}g C | "
          f"{total['fat']:5.1f}g F | "
          f"{total['fiber']:5.1f}g fiber")
    
    return total


def main():
    """Hlavní program - kalkulace JEN s tím co má Pája."""
    
    print("\n" + "="*90)
    print(" "*20 + "PÁJA - DEN 3 - CO MÁ U SEBE (MINIMÁLNÍ VARIANTA)")
    print("="*90)
    
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
    
    print("\n" + "="*90)
    print("ČÁST 1: JEN S TÍM CO MÁ PÁJA U SEBE")
    print("="*90)
    
    meals_current = []
    
    # Snídaně - zbytky (MUSÍ MÍT)
    print("\n⚠️  SNÍDANĚ: Pája MUSÍ mít zbytky z úterý (vejce/tuňák)")
    print("   Bez toho nebude mít energii!")
    meals_current.append(calculate_meal(
        "🌅 SNÍDANĚ (7:00) - POTŘEBUJE ZBYTKY",
        [
            ('ledovy_salat', 30),
        ]
    ))
    
    # Dopolední svačina
    meals_current.append(calculate_meal(
        "🍎 DOPOLEDNÍ SVAČINA (10:00) - Malá porce",
        [
            ('cottage_cheese', 60),
            ('ledovy_salat', 15),
        ]
    ))
    
    # Oběd
    meals_current.append(calculate_meal(
        "🍽️ OBĚD (12:30) - Pracovní (VELMI MALÁ PORCE)",
        [
            ('cottage_cheese', 60),
            ('kesu', 15),
            ('ledovy_salat', 15),
        ]
    ))
    
    # Odpolední svačina - fíky!
    meals_current.append(calculate_meal(
        "🥤 ODPOLEDNÍ SVAČINA (15:30) - Sladká odměna",
        [
            ('susene_fiky', 20),  # 2 fíky
            ('kesu', 15),
        ]
    ))
    
    # Večeře - MUSÍ PŘIDAT
    print("\n⚠️  VEČEŘE: Pája MUSÍ něco uvařit doma!")
    print("   Jen se salátem nebude mít energii!")
    
    # Večerní svačina
    meals_current.append(calculate_meal(
        "🌃 VEČERNÍ SVAČINA (21:00)",
        [
            ('susene_fiky', 20),  # 2 fíky
            ('cottage_cheese', 60),
            ('kesu', 10),
        ]
    ))
    
    # Celkový součet - JEN S TÍM CO MÁ
    print("\n" + "="*90)
    print(" "*25 + "CELKEM - JEN S TÍM CO MÁ PÁJA")
    print("="*90)
    
    daily_current = {
        'calories': sum(m['calories'] for m in meals_current),
        'protein': sum(m['protein'] for m in meals_current),
        'carbs': sum(m['carbs'] for m in meals_current),
        'fat': sum(m['fat'] for m in meals_current),
        'fiber': sum(m['fiber'] for m in meals_current),
    }
    
    print(f"\n{'Makronutrient':20s} | {'Cíl':>10s} | {'Co má':>12s} | {'Rozdíl':>12s} | {'% Cíle':>8s} | Status")
    print("-"*90)
    
    for key, target in targets.items():
        actual = daily_current[key]
        diff = actual - target
        pct = (actual / target * 100) if target > 0 else 0
        
        if key == 'carbs':
            status = "✅" if actual <= target else "⚠️"
        elif key in ['protein', 'fiber']:
            status = "✅" if actual >= target else "⚠️"
        else:
            status = "✅" if pct >= 85 else "⚠️"
        
        unit = "kcal" if key == 'calories' else "g"
        print(f"{key.capitalize():20s} | {target:>8.0f}{unit:2s} | "
              f"{actual:>10.1f}{unit:2s} | {diff:+11.1f}{unit:2s} | "
              f"{pct:>7.0f}% | {status}")
    
    print("="*90)
    
    # VAROVÁNÍ
    print("\n" + "!"*90)
    print(" "*30 + "⚠️  VAROVÁNÍ PRO PÁJU  ⚠️")
    print("!"*90)
    print(f"\n❌ Jen s tím co má: {daily_current['calories']:.0f} kcal = "
          f"{daily_current['calories']/targets['calories']*100:.0f}% denního cíle!")
    print(f"❌ Chybí: {targets['calories'] - daily_current['calories']:.0f} kcal "
          f"({(targets['calories'] - daily_current['calories'])/targets['calories']*100:.0f}% denní energie)")
    print(f"❌ Bílkoviny: {daily_current['protein']:.1f}g z {targets['protein']}g "
          f"({daily_current['protein']/targets['protein']*100:.0f}%)")
    print(f"❌ Tuky: {daily_current['fat']:.1f}g z {targets['fat']}g "
          f"({daily_current['fat']/targets['fat']*100:.0f}%)")
    print(f"❌ Vláknina: {daily_current['fiber']:.1f}g z {targets['fiber']}g "
          f"({daily_current['fiber']/targets['fiber']*100:.0f}%)")
    
    print("\n⚠️  S tímto plánem:")
    print("   - Bude mít HLAD během dne")
    print("   - Nebude mít energii")
    print("   - Nesplní keto cíle")
    print("   - Zdravotní problémy z podvýživy")
    
    # ČÁST 2: S MINIMÁLNÍM DOPLNĚNÍM
    print("\n" + "="*90)
    print("ČÁST 2: S MINIMÁLNÍM DOPLNĚNÍM (DOPORUČENO)")
    print("="*90)
    
    meals_with_additions = []
    
    # Snídaně - s vejci
    meals_with_additions.append(calculate_meal(
        "🌅 SNÍDANĚ (7:00) - S vejci (PŘIDÁNO)",
        [
            ('vejce', 110),  # 2 ks
            ('ledovy_salat', 30),
        ]
    ))
    
    # Dopolední svačina
    meals_with_additions.append(calculate_meal(
        "🍎 DOPOLEDNÍ SVAČINA (10:00)",
        [
            ('cottage_cheese', 60),
            ('ledovy_salat', 15),
        ]
    ))
    
    # Oběd - s vejcem
    meals_with_additions.append(calculate_meal(
        "🍽️ OBĚD (12:30) - S vejcem (PŘIDÁNO)",
        [
            ('cottage_cheese', 60),
            ('kesu', 15),
            ('ledovy_salat', 15),
            ('vejce', 55),  # 1 ks
        ]
    ))
    
    # Odpolední svačina
    meals_with_additions.append(calculate_meal(
        "🥤 ODPOLEDNÍ SVAČINA (15:30)",
        [
            ('susene_fiky', 20),
            ('kesu', 15),
        ]
    ))
    
    # Večeře - S MASEM
    meals_with_additions.append(calculate_meal(
        "🌙 VEČEŘE (18:30) - S kuřecím (PŘIDÁNO)",
        [
            ('kurice_prsa', 120),
            ('brokolice', 150),
            ('olivovy_olej', 10),
        ]
    ))
    
    # Večerní svačina
    meals_with_additions.append(calculate_meal(
        "🌃 VEČERNÍ SVAČINA (21:00)",
        [
            ('susene_fiky', 20),
            ('cottage_cheese', 60),
            ('kesu', 10),
        ]
    ))
    
    # Celkový součet - S DOPLNĚNÍM
    print("\n" + "="*90)
    print(" "*25 + "CELKEM - S MINIMÁLNÍM DOPLNĚNÍM")
    print("="*90)
    
    daily_with_additions = {
        'calories': sum(m['calories'] for m in meals_with_additions),
        'protein': sum(m['protein'] for m in meals_with_additions),
        'carbs': sum(m['carbs'] for m in meals_with_additions),
        'fat': sum(m['fat'] for m in meals_with_additions),
        'fiber': sum(m['fiber'] for m in meals_with_additions),
    }
    
    print(f"\n{'Makronutrient':20s} | {'Cíl':>10s} | {'S doplňky':>12s} | {'Rozdíl':>12s} | {'% Cíle':>8s} | Status")
    print("-"*90)
    
    for key, target in targets.items():
        actual = daily_with_additions[key]
        diff = actual - target
        pct = (actual / target * 100) if target > 0 else 0
        
        if key == 'carbs':
            status = "✅" if actual <= target else "⚠️"
        elif key in ['protein', 'fiber']:
            status = "✅" if actual >= target * 0.85 else "⚠️"
        else:
            status = "✅" if pct >= 85 else "⚠️"
        
        unit = "kcal" if key == 'calories' else "g"
        print(f"{key.capitalize():20s} | {target:>8.0f}{unit:2s} | "
              f"{actual:>10.1f}{unit:2s} | {diff:+11.1f}{unit:2s} | "
              f"{pct:>7.0f}% | {status}")
    
    print("="*90)
    
    # CO PŘIDAT
    print("\n" + "="*90)
    print(" "*30 + "💡 CO PŘIDAT (MINIMÁLNĚ)")
    print("="*90)
    print("\n✅ PŘIDAT:")
    print("   1. Vejce 3 ks (~15 Kč)")
    print("   2. Kuřecí prsa 120g (~30 Kč)")
    print("   3. Brokolice 150g (~10 Kč)")
    print("   4. Olivový olej (už má doma)")
    print("\n💰 CELKEM: ~55 Kč")
    print("\n✅ VÝSLEDEK:")
    print(f"   - {daily_with_additions['calories']:.0f} kcal "
          f"({daily_with_additions['calories']/targets['calories']*100:.0f}% cíle)")
    print(f"   - {daily_with_additions['protein']:.0f}g bílkovin "
          f"({daily_with_additions['protein']/targets['protein']*100:.0f}% cíle) ✅")
    print(f"   - {daily_with_additions['carbs']:.0f}g sacharidů "
          f"({daily_with_additions['carbs']/targets['carbs']*100:.0f}% max limitu) ✅")
    print(f"   - Malé porce (jak Pája chce!) ✅")
    print(f"   - Sladké uspokojení (fíky!) ✅")
    
    print("\n" + "="*90)
    print(" "*35 + "HOTOVO! ✨")
    print("="*90 + "\n")


if __name__ == "__main__":
    main()
