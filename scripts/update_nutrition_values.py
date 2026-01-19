#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper script pro aktualizaci nutričních hodnot v databázi potravin

Tento skript usnadňuje aktualizaci nutričních hodnot pomocí web scraperu
z kaloricketabulky.cz a validaci konzistence dat.
"""

import sys
import os
import json
import yaml
from pathlib import Path
from typing import Optional, Dict, List

# Přidáme cestu k root projektu
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Zkusíme různé cesty pro import
fetch_by_product_name = None
fetch_nutrition_data = None

try:
    from src.scrapers.fetch_nutrition_data import fetch_by_product_name, fetch_nutrition_data
except ImportError:
    try:
        # Zkusíme přímý import ze scrapers directory
        scrapers_path = project_root / "src" / "scrapers"
        sys.path.insert(0, str(scrapers_path))
        from fetch_nutrition_data import fetch_by_product_name, fetch_nutrition_data
    except ImportError:
        print("⚠️  Nepodařilo se načíst modul fetch_nutrition_data")
        print("   Ujistěte se, že jste ve správném adresáři projektu")
        print(f"   Project root: {project_root}")
        print(f"   Hledal jsem v: {project_root / 'src' / 'scrapers' / 'fetch_nutrition_data.py'}")
        sys.exit(1)


def load_yaml_food(food_file: Path) -> Optional[Dict]:
    """Načte YAML soubor s potravinou"""
    try:
        with open(food_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Chyba při načítání {food_file}: {e}")
        return None


def save_yaml_food(food_file: Path, data: Dict) -> bool:
    """Uloží YAML soubor s potravinou"""
    try:
        with open(food_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"❌ Chyba při ukládání {food_file}: {e}")
        return False


def calculate_calories_from_macros(protein: float, carbs: float, fat: float) -> float:
    """Vypočítá kalorie z makroživin"""
    return (protein * 4) + (carbs * 4) + (fat * 9)


def check_consistency(data: Dict) -> Dict:
    """Zkontroluje konzistenci nutričních hodnot"""
    protein = float(data.get('bilkoviny', 0))
    carbs = float(data.get('sacharidy', 0))
    fat = float(data.get('tuky', 0))
    calories = float(data.get('kalorie', 0))
    
    calculated_calories = calculate_calories_from_macros(protein, carbs, fat)
    difference = abs(calculated_calories - calories)
    tolerance = calories * 0.15  # 15% tolerance
    
    return {
        'consistent': difference <= tolerance,
        'calculated_calories': calculated_calories,
        'stated_calories': calories,
        'difference': difference,
        'tolerance': tolerance
    }


def parse_scraped_value(value_str: str) -> float:
    """Parsuje hodnotu ze scraped dat (např. '34 kcal' -> 34.0)"""
    if not value_str:
        return 0.0
    
    # Odstranit jednotky a převést na float
    cleaned = value_str.replace('kcal', '').replace('g', '').replace('kJ', '').strip()
    
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def fetch_and_compare(product_name: str, current_data: Dict) -> Optional[Dict]:
    """Stáhne data ze scraperu a porovná s aktuálními hodnotami"""
    print(f"\n🔍 Vyhledávám: {product_name}")
    print("-" * 60)
    
    scraped_data = fetch_by_product_name(product_name)
    
    if not scraped_data or not scraped_data.get('macros'):
        print(f"❌ Nepodařilo se najít data pro: {product_name}")
        return None
    
    macros = scraped_data['macros']
    
    # Parsování hodnot
    new_data = {
        'kalorie': parse_scraped_value(macros.get('calories', '0')),
        'bilkoviny': parse_scraped_value(macros.get('protein', '0')),
        'sacharidy': parse_scraped_value(macros.get('carbohydrates', '0')),
        'tuky': parse_scraped_value(macros.get('fat', '0')),
        'vlaknina': parse_scraped_value(macros.get('fiber', '0'))
    }
    
    # Pokud některé hodnoty chybí, použij současné
    for key in ['kalorie', 'bilkoviny', 'sacharidy', 'tuky', 'vlaknina']:
        if new_data[key] == 0.0 and current_data.get(key, 0) != 0.0:
            print(f"⚠️  {key} nenalezeno, ponechávám současnou hodnotu")
            new_data[key] = current_data[key]
    
    # Zobraz porovnání
    print("\n📊 POROVNÁNÍ:")
    print(f"{'Hodnota':<15} {'Současné':<12} {'Nalezené':<12} {'Rozdíl':<12}")
    print("-" * 60)
    
    for key, label in [
        ('kalorie', 'Kalorie'),
        ('bilkoviny', 'Bílkoviny'),
        ('sacharidy', 'Sacharidy'),
        ('tuky', 'Tuky'),
        ('vlaknina', 'Vláknina')
    ]:
        current = float(current_data.get(key, 0))
        new = new_data.get(key, 0)
        diff = new - current
        diff_str = f"{diff:+.1f}" if diff != 0 else "0"
        
        print(f"{label:<15} {current:<12.1f} {new:<12.1f} {diff_str:<12}")
    
    # Kontrola konzistence nových dat
    print("\n🔍 KONTROLA KONZISTENCE NOVÝCH DAT:")
    consistency = check_consistency(new_data)
    
    print(f"Uvedené kalorie: {consistency['stated_calories']:.1f} kcal")
    print(f"Vypočtené kalorie: {consistency['calculated_calories']:.1f} kcal")
    print(f"Rozdíl: {consistency['difference']:.1f} kcal")
    
    if consistency['consistent']:
        print("✅ Data jsou konzistentní")
    else:
        print(f"⚠️  Data nejsou konzistentní (tolerance {consistency['tolerance']:.1f} kcal)")
    
    print(f"\n🌐 Zdroj: {scraped_data.get('url', 'N/A')}")
    
    return new_data


def update_food_interactive(food_name: str):
    """Interaktivně aktualizuje potravinu"""
    
    # Najdi soubor
    potraviny_dir = Path(__file__).parent.parent / "potraviny" / "soubory"
    
    # Převeď název na název souboru (zjednodušeně)
    food_file_name = food_name.lower().replace(' ', '_').replace('(', '').replace(')', '') + '.yaml'
    food_file = potraviny_dir / food_file_name
    
    if not food_file.exists():
        print(f"❌ Soubor nenalezen: {food_file}")
        print("\n💡 Dostupné soubory v potraviny/soubory/:")
        for f in sorted(potraviny_dir.glob("*.yaml")):
            print(f"   - {f.stem}")
        return
    
    # Načti současná data
    current_data = load_yaml_food(food_file)
    if not current_data:
        return
    
    print(f"\n📦 AKTUÁLNÍ DATA PRO: {current_data.get('nazev', food_name)}")
    print("=" * 60)
    print(f"Kategorie: {current_data.get('kategorie', 'N/A')}")
    print(f"Kalorie: {current_data.get('kalorie', 0)} kcal")
    print(f"Bílkoviny: {current_data.get('bilkoviny', 0)} g")
    print(f"Sacharidy: {current_data.get('sacharidy', 0)} g")
    print(f"Tuky: {current_data.get('tuky', 0)} g")
    print(f"Vláknina: {current_data.get('vlaknina', 0)} g")
    
    # Kontrola konzistence současných dat
    consistency = check_consistency(current_data)
    if not consistency['consistent']:
        print(f"\n⚠️  VAROVÁNÍ: Současná data nejsou konzistentní")
        print(f"   Vypočtené kalorie: {consistency['calculated_calories']:.1f} kcal")
        print(f"   Rozdíl: {consistency['difference']:.1f} kcal")
    
    # Fetch nových dat
    new_data = fetch_and_compare(current_data.get('nazev', food_name), current_data)
    
    if not new_data:
        return
    
    # Zeptej se uživatele
    print("\n" + "=" * 60)
    response = input("Chcete použít nová data? (a=ano, n=ne, m=manuální úprava): ").lower()
    
    if response == 'a' or response == 'ano':
        # Aktualizuj data
        for key in ['kalorie', 'bilkoviny', 'sacharidy', 'tuky', 'vlaknina']:
            current_data[key] = new_data[key]
        
        # Ulož
        if save_yaml_food(food_file, current_data):
            print(f"✅ Soubor {food_file.name} byl úspěšně aktualizován")
        else:
            print(f"❌ Nepodařilo se uložit soubor")
    
    elif response == 'm' or response == 'manuální':
        print("\n📝 MANUÁLNÍ ÚPRAVA:")
        for key, label in [
            ('kalorie', 'Kalorie (kcal)'),
            ('bilkoviny', 'Bílkoviny (g)'),
            ('sacharidy', 'Sacharidy (g)'),
            ('tuky', 'Tuky (g)'),
            ('vlaknina', 'Vláknina (g)')
        ]:
            current_value = current_data.get(key, 0)
            new_value = input(f"{label} [{current_value}]: ").strip()
            
            if new_value:
                try:
                    current_data[key] = float(new_value)
                except ValueError:
                    print(f"⚠️  Neplatná hodnota, ponechávám {current_value}")
        
        # Kontrola
        consistency = check_consistency(current_data)
        print(f"\nVypočtené kalorie: {consistency['calculated_calories']:.1f} kcal")
        print(f"Uvedené kalorie: {consistency['stated_calories']:.1f} kcal")
        
        if consistency['consistent']:
            print("✅ Data jsou konzistentní")
        else:
            print("⚠️  Data nejsou konzistentní")
        
        response2 = input("\nUložit změny? (a/n): ").lower()
        if response2 == 'a' or response2 == 'ano':
            if save_yaml_food(food_file, current_data):
                print(f"✅ Soubor {food_file.name} byl úspěšně aktualizován")
        else:
            print("❌ Změny nebyly uloženy")
    
    else:
        print("❌ Aktualizace zrušena")


def batch_update_from_list(list_file: str):
    """Dávková aktualizace ze seznamu produktů"""
    
    try:
        with open(list_file, 'r', encoding='utf-8') as f:
            products = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except Exception as e:
        print(f"❌ Chyba při načítání seznamu: {e}")
        return
    
    print(f"\n📋 Načteno {len(products)} produktů k aktualizaci")
    print("=" * 60)
    
    for i, product_name in enumerate(products, 1):
        print(f"\n[{i}/{len(products)}] Zpracovávám: {product_name}")
        print("-" * 60)
        
        update_food_interactive(product_name)
        
        if i < len(products):
            response = input("\nPokračovat na další? (a/n): ").lower()
            if response != 'a' and response != 'ano':
                print("⏸️  Přerušeno uživatelem")
                break


def main():
    """Main funkce"""
    
    print("=" * 60)
    print("🔧 HELPER PRO AKTUALIZACI NUTRIČNÍCH HODNOT")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n📖 POUŽITÍ:")
        print("  python update_nutrition_values.py <název_produktu>")
        print("  python update_nutrition_values.py --batch <soubor_se_seznamem>")
        print("\n📝 PŘÍKLADY:")
        print("  python update_nutrition_values.py Brokolice")
        print("  python update_nutrition_values.py 'Kuřecí prsa'")
        print("  python update_nutrition_values.py --batch priority_list.txt")
        print("\n💡 TIP:")
        print("  Seznam produktů k aktualizaci najdete v:")
        print("  docs/technical/SEZNAM_K_AKTUALIZACI_NUTRICNICH_HODNOT.md")
        sys.exit(1)
    
    if sys.argv[1] == '--batch':
        if len(sys.argv) < 3:
            print("❌ Chybí soubor se seznamem produktů")
            sys.exit(1)
        batch_update_from_list(sys.argv[2])
    else:
        product_name = ' '.join(sys.argv[1:])
        update_food_interactive(product_name)


if __name__ == "__main__":
    main()
