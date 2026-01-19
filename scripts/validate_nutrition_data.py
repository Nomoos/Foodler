#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validační skript pro kontrolu nutričních hodnot v databázi potravin

Tento skript kontroluje konzistenci nutričních hodnot a generuje report.
Lze jej spustit kdykoliv pro ověření stavu databáze.

DŮLEŽITÉ: V databázi kaloricketabulky.cz jsou "sacharidy" uvedeny jako
NET carbs (čisté sacharidy bez vlákniny). Vláknina je uvedena samostatně
a má ~2 kcal/g místo 4 kcal/g.

Vzorec: kalorie = (bílkoviny × 4) + (sacharidy × 4) + (vláknina × 2) + (tuky × 9)
"""

import sys
from pathlib import Path
from typing import List, Dict

# Přidáme cestu k projektu
sys.path.insert(0, str(Path(__file__).parent.parent))

from potraviny.databaze import DatabazePotravIn, Potravina

# Konstanty pro výpočet kalorií a tolerance
CALORIES_PER_GRAM_PROTEIN = 4.0
CALORIES_PER_GRAM_CARBS = 4.0  # Digestible carbs (net carbs)
CALORIES_PER_GRAM_FIBER = 2.0  # Fiber has lower caloric value
CALORIES_PER_GRAM_FAT = 9.0
TOLERANCE_PERCENTAGE = 0.15  # 15% tolerance pro akceptovatelné rozdíly
CRITICAL_THRESHOLD_PERCENTAGE = 0.20  # 20% hranice pro kritické problémy


def calculate_calories_from_macros(p: Potravina) -> float:
    """
    Vypočítá kalorie z makroživin.
    
    DŮLEŽITÉ: V databázi kaloricketabulky.cz jsou "sacharidy" uvedeny jako
    NET carbs (čisté sacharidy bez vlákniny). Vláknina je uvedena samostatně
    a má ~2 kcal/g místo 4 kcal/g.
    
    Vzorec: kalorie = (bílkoviny × 4) + (sacharidy × 4) + (vláknina × 2) + (tuky × 9)
    """
    return (p.bilkoviny * CALORIES_PER_GRAM_PROTEIN + 
            p.sacharidy * CALORIES_PER_GRAM_CARBS + 
            p.vlaknina * CALORIES_PER_GRAM_FIBER +
            p.tuky * CALORIES_PER_GRAM_FAT)


def check_macro_consistency(p: Potravina) -> Dict:
    """Kontrola konzistence makroživin a kalkulace kalorií"""
    calculated_kcal = calculate_calories_from_macros(p)
    tolerance = p.kalorie * TOLERANCE_PERCENTAGE
    difference = abs(calculated_kcal - p.kalorie)
    
    return {
        'consistent': difference <= tolerance,
        'calculated_calories': calculated_kcal,
        'stated_calories': p.kalorie,
        'difference': difference,
        'difference_percent': (difference / p.kalorie * 100) if p.kalorie > 0 else 0,
        'tolerance': tolerance
    }


def validate_database(verbose: bool = False) -> Dict:
    """Validuje celou databázi a vrátí report"""
    potraviny = DatabazePotravIn.get_all()
    
    results = {
        'total_count': len(potraviny),
        'ok': [],
        'issues': [],
        'critical_issues': []
    }
    
    for p in potraviny:
        consistency = check_macro_consistency(p)
        
        if consistency['consistent']:
            results['ok'].append(p.nazev)
        else:
            issue_data = {
                'nazev': p.nazev,
                'kategorie': p.kategorie,
                'kalorie_stated': p.kalorie,
                'kalorie_calculated': consistency['calculated_calories'],
                'difference': consistency['difference'],
                'difference_percent': consistency['difference_percent']
            }
            
            # Kritický problém je rozdíl > 20%
            if consistency['difference_percent'] > 20:
                results['critical_issues'].append(issue_data)
            else:
                results['issues'].append(issue_data)
        
        if verbose:
            status = "✅" if consistency['consistent'] else "❌"
            print(f"{status} {p.nazev:30} | Uvedeno: {p.kalorie:6.1f} kcal | "
                  f"Vypočteno: {consistency['calculated_calories']:6.1f} kcal | "
                  f"Rozdíl: {consistency['difference']:5.1f} kcal "
                  f"({consistency['difference_percent']:4.1f}%)")
    
    return results


def print_summary(results: Dict):
    """Vytiskne souhrn validace"""
    total = results['total_count']
    ok_count = len(results['ok'])
    issues_count = len(results['issues'])
    critical_count = len(results['critical_issues'])
    
    print("\n" + "=" * 70)
    print("📊 VALIDACE NUTRIČNÍCH HODNOT - SOUHRN")
    print("=" * 70)
    
    print(f"\n✅ Celkem produktů v databázi: {total}")
    print(f"✅ Produkty v pořádku: {ok_count} ({ok_count/total*100:.1f}%)")
    print(f"⚠️  Produkty s problémy: {issues_count} ({issues_count/total*100:.1f}%)")
    print(f"❌ Produkty s kritickými problémy: {critical_count} ({critical_count/total*100:.1f}%)")
    
    if critical_count > 0:
        print("\n" + "=" * 70)
        print("❌ KRITICKÉ PROBLÉMY (rozdíl > 20%)")
        print("=" * 70)
        for item in sorted(results['critical_issues'], key=lambda x: x['difference_percent'], reverse=True):
            print(f"\n📦 {item['nazev']} ({item['kategorie']})")
            print(f"   Uvedeno: {item['kalorie_stated']:.1f} kcal")
            print(f"   Vypočteno: {item['kalorie_calculated']:.1f} kcal")
            print(f"   Rozdíl: {item['difference']:.1f} kcal ({item['difference_percent']:.1f}%)")
    
    if issues_count > 0:
        print("\n" + "=" * 70)
        print("⚠️  MENŠÍ PROBLÉMY (rozdíl < 20%)")
        print("=" * 70)
        for item in sorted(results['issues'], key=lambda x: x['difference_percent'], reverse=True):
            print(f"   • {item['nazev']:30} | Rozdíl: {item['difference']:5.1f} kcal "
                  f"({item['difference_percent']:4.1f}%)")
    
    if ok_count > 0 and len(sys.argv) > 1 and '--show-ok' in sys.argv:
        print("\n" + "=" * 70)
        print("✅ PRODUKTY V POŘÁDKU")
        print("=" * 70)
        for i, nazev in enumerate(sorted(results['ok']), 1):
            print(f"   {i:2}. {nazev}")
    
    print("\n" + "=" * 70)
    
    if critical_count > 0 or issues_count > 0:
        print("💡 TIP:")
        print("   Pro aktualizaci hodnot použijte:")
        print("   python scripts/update_nutrition_values.py <název_produktu>")
        print()
        print("   Nebo dávkovou aktualizaci:")
        print("   python scripts/update_nutrition_values.py --batch priority_update_list.txt")
        print()
        print("   Více informací v dokumentaci:")
        print("   docs/technical/NAVOD_AKTUALIZACE_NUTRICNICH_HODNOT.md")
    else:
        print("🎉 GRATULUJEME!")
        print("   Všechny nutriční hodnoty v databázi jsou konzistentní!")
    
    print("=" * 70)


def main():
    """Main funkce"""
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    print("🔍 Validuji nutriční hodnoty v databázi potravin...\n")
    
    if verbose:
        print("Status | Produkt                        | Uvedeno | Vypočteno | Rozdíl")
        print("-" * 90)
    
    results = validate_database(verbose=verbose)
    print_summary(results)
    
    # Exit code: 0 = OK, 1 = mají problémy, 2 = kritické problémy
    if len(results['critical_issues']) > 0:
        sys.exit(2)
    elif len(results['issues']) > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
