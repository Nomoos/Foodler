#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Potraviny - Modul pro správu čistých potravin (ingrediencí)

Tento modul spravuje jednotlivé potraviny/ingredience, které lze použít
k přípravě jídel. Obsahuje nutriční hodnoty a další metadata.

Potraviny jsou nyní ukládány jako jednotlivé YAML soubory v adresáři potraviny/soubory/
"""

from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path
import yaml


@dataclass
class Potravina:
    """Reprezentuje jednu čistou potravinu/ingredienci."""
    
    nazev: str
    kategorie: str  # "bilkoviny", "zelenina", "tuky", "orechy", "mlecne_vyrobky", atd.
    
    # Nutriční hodnoty na 100g
    kalorie: float
    bilkoviny: float  # g
    sacharidy: float  # g
    tuky: float  # g
    vlaknina: float  # g
    
    # Volitelné informace
    cena_za_kg: Optional[float] = None  # Kč/kg
    sezona: Optional[List[str]] = None  # Měsíce dostupnosti
    poznamky: Optional[str] = None
    
    # Zdroj dat - pro budoucí korekci a tracking
    zdroj: Optional[str] = None  # "kaloricketabulky.cz", "USDA", "manuální", atd.
    datum_aktualizace: Optional[str] = None  # YYYY-MM-DD formát
    
    def vypocitej_makra(self, mnozstvi_g: float) -> dict:
        """Vypočítá makronutrienty pro dané množství."""
        koeficient = mnozstvi_g / 100
        return {
            "kalorie": round(self.kalorie * koeficient, 1),
            "bilkoviny": round(self.bilkoviny * koeficient, 1),
            "sacharidy": round(self.sacharidy * koeficient, 1),
            "tuky": round(self.tuky * koeficient, 1),
            "vlaknina": round(self.vlaknina * koeficient, 1)
        }
    
    def je_low_carb(self, limit: float = 10.0) -> bool:
        """Kontroluje, zda je potravina nízkosacharidová."""
        return self.sacharidy <= limit
    
    def je_high_protein(self, limit: float = 15.0) -> bool:
        """Kontroluje, zda je potravina vysokobílkovinová."""
        return self.bilkoviny >= limit


class DatabazePotravIn:
    """Databáze běžných potravin použitých v dietě.
    
    Potraviny jsou načítány z jednotlivých YAML souborů v adresáři potraviny/soubory/.
    To umožňuje přidávat nové potraviny bez konfliktů při spolupráci více lidí.
    """
    
    _cache: Optional[List[Potravina]] = None
    
    @classmethod
    def _load_from_yaml_files(cls) -> List[Potravina]:
        """Načte potraviny z YAML souborů."""
        potraviny = []
        potraviny_dir = Path(__file__).parent / "soubory"
        
        if not potraviny_dir.exists():
            print(f"Warning: Directory {potraviny_dir} does not exist. No ingredients loaded.")
            return []
        
        # Načte všechny YAML soubory
        for yaml_file in sorted(potraviny_dir.glob("*.yaml")):
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                
                if not data:
                    continue
                
                # Vytvoří objekt Potravina
                potravina = Potravina(
                    nazev=data["nazev"],
                    kategorie=data["kategorie"],
                    kalorie=float(data["kalorie"]),
                    bilkoviny=float(data["bilkoviny"]),
                    sacharidy=float(data["sacharidy"]),
                    tuky=float(data["tuky"]),
                    vlaknina=float(data["vlaknina"]),
                    cena_za_kg=data.get("cena_za_kg"),
                    sezona=data.get("sezona"),
                    poznamky=data.get("poznamky")
                )
                potraviny.append(potravina)
                
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file.name}: {e}")
                continue
        
        return potraviny
    
    @classmethod
    def get_all(cls) -> List[Potravina]:
        """Vrátí všechny potraviny (s cachováním). Preferovaný způsob přístupu."""
        if cls._cache is None:
            cls._cache = cls._load_from_yaml_files()
        return cls._cache
    
    # Backward compatibility - can also be accessed as class attribute
    @property
    def POTRAVINY(self) -> List[Potravina]:
        """Property for backward compatibility. Use get_all() classmethod instead."""
        return self.__class__.get_all()
    
    @classmethod
    def reload(cls):
        """Znovu načte potraviny ze souborů (užitečné po přidání nových souborů)."""
        cls._cache = None
    
    @classmethod
    def najdi_podle_nazvu(cls, nazev: str) -> Optional[Potravina]:
        """Najde potravinu podle názvu."""
        for potravina in cls.get_all():
            if potravina.nazev.lower() == nazev.lower():
                return potravina
        return None
    
    @classmethod
    def najdi_podle_kategorie(cls, kategorie: str) -> List[Potravina]:
        """Najde všechny potraviny v dané kategorii."""
        return [p for p in cls.get_all() if p.kategorie == kategorie]
    
    @classmethod
    def najdi_low_carb(cls, max_sacharidy: float = 10.0) -> List[Potravina]:
        """Najde nízkosacharidové potraviny."""
        return [p for p in cls.get_all() if p.je_low_carb(max_sacharidy)]
    
    @classmethod
    def najdi_high_protein(cls, min_bilkoviny: float = 15.0) -> List[Potravina]:
        """Najde vysokobílkovinové potraviny."""
        return [p for p in cls.get_all() if p.je_high_protein(min_bilkoviny)]


# For backward compatibility with code that accesses DatabazePotravIn.POTRAVINY directly
# This creates a class variable that lazy-loads the data
class _PotravinyDescriptor:
    """Descriptor for lazy loading POTRAVINY as a class attribute."""
    def __get__(self, obj, objtype=None):
        return objtype.get_all()

DatabazePotravIn.POTRAVINY = _PotravinyDescriptor()


def main():
    """Ukázka použití modulu potravin."""
    print("=" * 70)
    print("DATABÁZE POTRAVIN")
    print("=" * 70)
    
    # Ukázka kategorií
    all_potraviny = DatabazePotravIn.get_all()
    print("\n📊 KATEGORIE POTRAVIN:\n")
    kategorie = {}
    for potravina in all_potraviny:
        if potravina.kategorie not in kategorie:
            kategorie[potravina.kategorie] = []
        kategorie[potravina.kategorie].append(potravina.nazev)
    
    for kat, potraviny in sorted(kategorie.items()):
        print(f"\n{kat.upper().replace('_', ' ')}:")
        for p in potraviny:
            print(f"  • {p}")
    
    # Ukázka výpočtu makronutrientů
    print("\n" + "=" * 70)
    print("PŘÍKLAD: Kuřecí prsa 200g")
    print("=" * 70)
    
    kureci = DatabazePotravIn.najdi_podle_nazvu("Kuřecí prsa")
    if kureci:
        makra = kureci.vypocitej_makra(200)
        print(f"\nPotravina: {kureci.nazev}")
        print(f"Množství: 200g")
        print(f"\nMakronutrienty:")
        print(f"  Kalorie: {makra['kalorie']} kcal")
        print(f"  Bílkoviny: {makra['bilkoviny']}g")
        print(f"  Sacharidy: {makra['sacharidy']}g")
        print(f"  Tuky: {makra['tuky']}g")
        print(f"  Vláknina: {makra['vlaknina']}g")
    
    # Low-carb potraviny
    print("\n" + "=" * 70)
    print("NÍZKOSACHARIDOVÉ POTRAVINY (≤10g/100g)")
    print("=" * 70)
    
    low_carb = DatabazePotravIn.najdi_low_carb(10.0)
    for p in low_carb[:10]:
        print(f"  • {p.nazev} - {p.sacharidy}g sacharidů")
    
    # High-protein potraviny
    print("\n" + "=" * 70)
    print("VYSOKOBÍLKOVINOVÉ POTRAVINY (≥15g/100g)")
    print("=" * 70)
    
    high_protein = DatabazePotravIn.najdi_high_protein(15.0)
    for p in high_protein:
        print(f"  • {p.nazev} - {p.bilkoviny}g bílkovin")


if __name__ == "__main__":
    main()
