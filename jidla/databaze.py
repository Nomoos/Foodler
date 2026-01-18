#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jídla - Modul pro správu hotových jídel složených z více potravin

Tento modul spravuje kompletní jídla připravená ke konzumaci,
která jsou složena z více potravin/ingrediencí.

Jídla jsou nyní ukládána jako jednotlivé YAML soubory v adresáři jidla/soubory/
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import yaml


@dataclass
class Ingredience:
    """Reprezentuje jednu ingredienci v jídle."""
    nazev: str
    mnozstvi_g: float
    kategorie: str  # "hlavni", "priloha", "koření", "omacka"


@dataclass
class Jidlo:
    """Reprezentuje kompletní hotové jídlo."""
    
    nazev: str
    typ: str  # "snidane", "obed", "vecere", "svacina"
    ingredience: List[Ingredience]
    
    # Celkové nutriční hodnoty jídla
    kalorie_celkem: float
    bilkoviny_celkem: float
    sacharidy_celkem: float
    tuky_celkem: float
    vlaknina_celkem: float
    
    # Příprava
    priprava_cas_min: int
    priprava_postup: str
    obtiznost: str  # "snadna", "stredni", "narocna"
    
    # Metadata
    porce: int = 1  # Počet porcí
    vhodne_pro_meal_prep: bool = False
    vydrzi_dni: Optional[int] = None
    poznamky: Optional[str] = None
    datum_pripravy: Optional[datetime] = None
    
    def vypocitej_makra_na_porci(self) -> Dict[str, float]:
        """Vypočítá makronutrienty na jednu porci."""
        return {
            "kalorie": round(self.kalorie_celkem / self.porce, 1),
            "bilkoviny": round(self.bilkoviny_celkem / self.porce, 1),
            "sacharidy": round(self.sacharidy_celkem / self.porce, 1),
            "tuky": round(self.tuky_celkem / self.porce, 1),
            "vlaknina": round(self.vlaknina_celkem / self.porce, 1)
        }
    
    def je_low_carb(self, limit_na_porci: float = 15.0) -> bool:
        """Kontroluje, zda je jídlo nízkosacharidové."""
        makra = self.vypocitej_makra_na_porci()
        return makra["sacharidy"] <= limit_na_porci
    
    def je_high_protein(self, limit_na_porci: float = 25.0) -> bool:
        """Kontroluje, zda je jídlo vysokobílkovinové."""
        makra = self.vypocitej_makra_na_porci()
        return makra["bilkoviny"] >= limit_na_porci
    
    def je_cerstve(self, max_dni: int = 3) -> bool:
        """Kontroluje, zda je jídlo stále čerstvé."""
        if not self.datum_pripravy:
            return True
        dny_od_pripravy = (datetime.now() - self.datum_pripravy).days
        return dny_od_pripravy <= max_dni


class DatabzeJidel:
    """Databáze připravených jídel.
    
    Jídla jsou načítána z jednotlivých YAML souborů v adresáři jidla/soubory/.
    To umožňuje přidávat nová jídla bez konfliktů při spolupráci více lidí.
    """
    
    _cache: Optional[List[Jidlo]] = None
    
    @classmethod
    def _load_from_yaml_files(cls) -> List[Jidlo]:
        """Načte jídla z YAML souborů."""
        jidla = []
        jidla_dir = Path(__file__).parent / "soubory"
        
        if not jidla_dir.exists():
            print(f"Warning: Directory {jidla_dir} does not exist. No dishes loaded.")
            return []
        
        # Načte všechny YAML soubory
        for yaml_file in sorted(jidla_dir.glob("*.yaml")):
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                
                if not data:
                    continue
                
                # Převede ingredience na objekty
                ingredience = [
                    Ingredience(
                        nazev=ing["nazev"],
                        mnozstvi_g=float(ing["mnozstvi_g"]),
                        kategorie=ing["kategorie"]
                    )
                    for ing in data.get("ingredience", [])
                ]
                
                # Vytvoří objekt Jidlo
                jidlo = Jidlo(
                    nazev=data["nazev"],
                    typ=data["typ"],
                    ingredience=ingredience,
                    kalorie_celkem=float(data["kalorie_celkem"]),
                    bilkoviny_celkem=float(data["bilkoviny_celkem"]),
                    sacharidy_celkem=float(data["sacharidy_celkem"]),
                    tuky_celkem=float(data["tuky_celkem"]),
                    vlaknina_celkem=float(data["vlaknina_celkem"]),
                    priprava_cas_min=int(data["priprava_cas_min"]),
                    priprava_postup=data["priprava_postup"],
                    obtiznost=data["obtiznost"],
                    porce=int(data.get("porce", 1)),
                    vhodne_pro_meal_prep=bool(data.get("vhodne_pro_meal_prep", False)),
                    vydrzi_dni=data.get("vydrzi_dni"),
                    poznamky=data.get("poznamky"),
                    datum_pripravy=None
                )
                jidla.append(jidlo)
                
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file.name}: {e}")
                continue
        
        return jidla
    
    @classmethod
    def _get_all_jidla(cls) -> List[Jidlo]:
        """Vrátí všechna jídla (s cachováním)."""
        if cls._cache is None:
            cls._cache = cls._load_from_yaml_files()
        return cls._cache
    
    # Class variable that acts like the old JIDLA list
    # Accessed as DatabzeJidel.JIDLA
    @property  
    def JIDLA(self) -> List[Jidlo]:
        """Property for instance access to JIDLA."""
        return self.__class__._get_all_jidla()
    
    @classmethod
    def reload(cls):
        """Znovu načte jídla ze souborů (užitečné po přidání nových souborů)."""
        cls._cache = None
    
    @classmethod
    def najdi_podle_nazvu(cls, nazev: str) -> Optional[Jidlo]:
        """Najde jídlo podle názvu."""
        for jidlo in cls._get_all_jidla():
            if jidlo.nazev.lower() == nazev.lower():
                return jidlo
        return None
    
    @classmethod
    def najdi_podle_typu(cls, typ: str) -> List[Jidlo]:
        """Najde všechna jídla daného typu."""
        return [j for j in cls._get_all_jidla() if j.typ == typ]
    
    @classmethod
    def najdi_meal_prep(cls) -> List[Jidlo]:
        """Najde jídla vhodná pro meal prep."""
        return [j for j in cls._get_all_jidla() if j.vhodne_pro_meal_prep]
    
    @classmethod
    def najdi_rychla(cls, max_minut: int = 15) -> List[Jidlo]:
        """Najde rychlá jídla."""
        return [j for j in cls._get_all_jidla() if j.priprava_cas_min <= max_minut]
    
    @classmethod
    def najdi_low_carb(cls, max_sacharidy: float = 15.0) -> List[Jidlo]:
        """Najde nízkosacharidová jídla."""
        return [j for j in cls._get_all_jidla() if j.je_low_carb(max_sacharidy)]
    
    @classmethod
    def najdi_high_protein(cls, min_bilkoviny: float = 25.0) -> List[Jidlo]:
        """Najde vysokobílkovinová jídla."""
        return [j for j in cls._get_all_jidla() if j.je_high_protein(min_bilkoviny)]


# Module-level access to JIDLA for backward compatibility
# This allows: from jidla.databaze import DatabzeJidel; ... for j in DatabzeJidel.JIDLA
DatabzeJidel.JIDLA = DatabzeJidel._get_all_jidla()


def main():
    """Ukázka použití modulu jídel."""
    print("=" * 70)
    print("DATABÁZE HOTOVÝCH JÍDEL")
    print("=" * 70)
    
    # Všechna jídla
    all_jidla = DatabzeJidel._get_all_jidla()
    print("\n🍽️  VŠECHNA JÍDLA:\n")
    for i, jidlo in enumerate(all_jidla, 1):
        makra = jidlo.vypocitej_makra_na_porci()
        print(f"{i}. {jidlo.nazev} ({jidlo.typ})")
        print(f"   Čas: {jidlo.priprava_cas_min} min | Makra: B:{makra['bilkoviny']}g S:{makra['sacharidy']}g T:{makra['tuky']}g")
        print(f"   Ingredience: {len(jidlo.ingredience)} položek")
        print()
    
    # Meal prep jídla
    print("=" * 70)
    print("JÍDLA PRO MEAL PREP")
    print("=" * 70)
    meal_prep = DatabzeJidel.najdi_meal_prep()
    for jidlo in meal_prep:
        print(f"  • {jidlo.nazev}")
        print(f"    Vydrží: {jidlo.vydrzi_dni} dní | {jidlo.poznamky}")
    
    # Rychlá jídla
    print("\n" + "=" * 70)
    print("RYCHLÁ JÍDLA (≤15 min)")
    print("=" * 70)
    rychla = DatabzeJidel.najdi_rychla(15)
    for jidlo in rychla:
        print(f"  ⚡ {jidlo.nazev} - {jidlo.priprava_cas_min} min")
    
    # Low-carb jídla
    print("\n" + "=" * 70)
    print("NÍZKOSACHARIDOVÁ JÍDLA (≤15g na porci)")
    print("=" * 70)
    low_carb = DatabzeJidel.najdi_low_carb(15.0)
    for jidlo in low_carb:
        makra = jidlo.vypocitej_makra_na_porci()
        print(f"  • {jidlo.nazev} - {makra['sacharidy']}g sacharidů")


if __name__ == "__main__":
    main()
