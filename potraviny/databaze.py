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
    POTRAVINY: List[Potravina] = [
        # Bílkoviny - maso a ryby
        Potravina(
            nazev="Kuřecí prsa",
            kategorie="bilkoviny",
            kalorie=165,
            bilkoviny=31.0,
            sacharidy=0.0,
            tuky=3.6,
            vlaknina=0.0,
            cena_za_kg=150.0,
            poznamky="Nejlepší zdroj libových bílkovin"
        ),
        Potravina(
            nazev="Krůtí prsa",
            kategorie="bilkoviny",
            kalorie=135,
            bilkoviny=30.0,
            sacharidy=0.0,
            tuky=1.0,
            vlaknina=0.0,
            cena_za_kg=180.0,
            poznamky="Velmi libové, vhodné pro diet"
        ),
        Potravina(
            nazev="Hovězí maso (libové)",
            kategorie="bilkoviny",
            kalorie=250,
            bilkoviny=26.0,
            sacharidy=0.0,
            tuky=17.0,
            vlaknina=0.0,
            cena_za_kg=220.0
        ),
        Potravina(
            nazev="Losos",
            kategorie="bilkoviny",
            kalorie=208,
            bilkoviny=20.0,
            sacharidy=0.0,
            tuky=13.0,
            vlaknina=0.0,
            cena_za_kg=350.0,
            poznamky="Bohatý na Omega-3"
        ),
        Potravina(
            nazev="Tuňák (konzervovaný)",
            kategorie="bilkoviny",
            kalorie=132,
            bilkoviny=28.0,
            sacharidy=0.0,
            tuky=1.3,
            vlaknina=0.0,
            cena_za_kg=200.0,
            poznamky="Praktický zdroj bílkovin"
        ),
        Potravina(
            nazev="Tuňák kousky v oleji",
            kategorie="bilkoviny",
            kalorie=159,
            bilkoviny=26.0,
            sacharidy=0.0,
            tuky=6.0,
            vlaknina=0.0,
            cena_za_kg=200.0,
            poznamky="Sun&Sea 750g, v slunečnicovém oleji, vysoký obsah bílkovin, sůl 1.2g/100g"
        ),
        Potravina(
            nazev="Vejce slepičí M",
            kategorie="bilkoviny",
            kalorie=151,  # 83 kcal per 55g = 151 per 100g
            bilkoviny=12.38,  # 6.81g per 55g = 12.38 per 100g
            sacharidy=0.95,  # 0.52g per 55g = 0.95 per 100g
            tuky=10.87,  # 5.98g per 55g = 10.87 per 100g
            vlaknina=0.0,
            cena_za_kg=40.0,
            poznamky="Velikost M (55g), kompletní aminokyselinový profil, cholesterol 237mg/ks"
        ),
        
        # Mléčné výrobky
        Potravina(
            nazev="Tvaroh polotučný",
            kategorie="mlecne_vyrobky",
            kalorie=103,
            bilkoviny=16.0,
            sacharidy=3.5,
            tuky=4.0,
            vlaknina=0.0,
            cena_za_kg=45.0
        ),
        Potravina(
            nazev="Cottage cheese",
            kategorie="mlecne_vyrobky",
            kalorie=98,
            bilkoviny=14.0,
            sacharidy=4.0,
            tuky=4.0,
            vlaknina=0.0,
            cena_za_kg=50.0
        ),
        Potravina(
            nazev="Řecký jogurt",
            kategorie="mlecne_vyrobky",
            kalorie=59,
            bilkoviny=10.0,
            sacharidy=3.6,
            tuky=0.4,
            vlaknina=0.0,
            cena_za_kg=60.0
        ),
        Potravina(
            nazev="Sýr eidam",
            kategorie="mlecne_vyrobky",
            kalorie=334,
            bilkoviny=27.0,
            sacharidy=0.5,
            tuky=25.0,
            vlaknina=0.0,
            cena_za_kg=180.0
        ),
        Potravina(
            nazev="Sýrařův výběr moravský bochník 45% Madeta",
            kategorie="mlecne_vyrobky",
            kalorie=350,
            bilkoviny=23.0,
            sacharidy=0.5,
            tuky=28.0,
            vlaknina=0.0,
            cena_za_kg=200.0,
            poznamky="Polotvrdý sýr s 45% tuku v sušině"
        ),
        Potravina(
            nazev="Gizycko klásek Gornicky",
            kategorie="mlecne_vyrobky",
            kalorie=320,
            bilkoviny=25.0,
            sacharidy=0.5,
            tuky=24.0,
            vlaknina=0.0,
            cena_za_kg=190.0,
            poznamky="Polský polotvrdý sýr"
        ),
        Potravina(
            nazev="Mozzarella",
            kategorie="mlecne_vyrobky",
            kalorie=280,
            bilkoviny=18.0,
            sacharidy=2.2,
            tuky=22.0,
            vlaknina=0.0,
            cena_za_kg=160.0,
            poznamky="Ideální na pizzu"
        ),
        Potravina(
            nazev="Parmazán",
            kategorie="mlecne_vyrobky",
            kalorie=392,
            bilkoviny=36.0,
            sacharidy=3.2,
            tuky=26.0,
            vlaknina=0.0,
            cena_za_kg=450.0,
            poznamky="Tvrdý sýr, bohatý na protein"
        ),
        Potravina(
            nazev="Gouda",
            kategorie="mlecne_vyrobky",
            kalorie=356,
            bilkoviny=25.0,
            sacharidy=2.2,
            tuky=27.0,
            vlaknina=0.0,
            cena_za_kg=180.0,
            poznamky="Polotvrdý holandský sýr"
        ),
        Potravina(
            nazev="Cheddar",
            kategorie="mlecne_vyrobky",
            kalorie=403,
            bilkoviny=23.0,
            sacharidy=3.1,
            tuky=33.0,
            vlaknina=0.0,
            cena_za_kg=220.0,
            poznamky="Tvrdý anglický sýr"
            nazev="Sýr gouda 45%",
            kategorie="mlecne_vyrobky",
            kalorie=344,
            bilkoviny=26.0,
            sacharidy=0.0,
            tuky=27.0,
            vlaknina=0.0,
            cena_za_kg=180.0,
            poznamky="Polotvrdý sýr, 45% tuku, nulové sacharidy"
        ),
        
        # Zelenina
        Potravina(
            nazev="Brokolice",
            kategorie="zelenina",
            kalorie=34,
            bilkoviny=2.8,
            sacharidy=7.0,
            tuky=0.4,
            vlaknina=2.6,
            cena_za_kg=50.0,
            sezona=["9", "10", "11", "12", "1", "2", "3", "4"]
        ),
        Potravina(
            nazev="Špenát",
            kategorie="zelenina",
            kalorie=23,
            bilkoviny=2.9,
            sacharidy=3.6,
            tuky=0.4,
            vlaknina=2.2,
            cena_za_kg=80.0
        ),
        Potravina(
            nazev="Zelí",
            kategorie="zelenina",
            kalorie=25,
            bilkoviny=1.3,
            sacharidy=5.8,
            tuky=0.1,
            vlaknina=2.5,
            cena_za_kg=20.0,
            sezona=["9", "10", "11", "12", "1", "2", "3"]
        ),
        Potravina(
            nazev="Kysané zelí",
            kategorie="zelenina",
            kalorie=19,
            bilkoviny=0.9,
            sacharidy=4.3,
            tuky=0.1,
            vlaknina=2.9,
            cena_za_kg=30.0,
            poznamky="Fermentované, probiotické, nízkokalorické"
        ),
        Potravina(
            nazev="Ledový salát",
            kategorie="zelenina",
            kalorie=16.1,
            bilkoviny=0.7,
            sacharidy=2.0,
            tuky=0.14,
            vlaknina=1.2,
            cena_za_kg=35.0,
            poznamky="Nízkokalorický, hodně vody, cukry 1.97g/100g"
        ),
        Potravina(
            nazev="Cuketa",
            kategorie="zelenina",
            kalorie=17,
            bilkoviny=1.2,
            sacharidy=3.1,
            tuky=0.3,
            vlaknina=1.0,
            cena_za_kg=40.0,
            sezona=["6", "7", "8", "9"]
        ),
        Potravina(
            nazev="Paprika",
            kategorie="zelenina",
            kalorie=31,
            bilkoviny=1.0,
            sacharidy=6.0,
            tuky=0.3,
            vlaknina=2.1,
            cena_za_kg=60.0,
            sezona=["7", "8", "9"]
        ),
        Potravina(
            nazev="Rajčata",
            kategorie="zelenina",
            kalorie=18,
            bilkoviny=0.9,
            sacharidy=3.9,
            tuky=0.2,
            vlaknina=1.2,
            cena_za_kg=45.0,
            sezona=["6", "7", "8", "9"]
        ),
        Potravina(
            nazev="Okurka",
            kategorie="zelenina",
            kalorie=15,
            bilkoviny=0.7,
            sacharidy=3.6,
            tuky=0.1,
            vlaknina=0.5,
            cena_za_kg=35.0,
            sezona=["6", "7", "8"]
        ),
        Potravina(
            nazev="Květák",
            kategorie="zelenina",
            kalorie=25,
            bilkoviny=1.9,
            sacharidy=5.0,
            tuky=0.3,
            vlaknina=2.0,
            cena_za_kg=45.0,
            sezona=["9", "10", "11"]
        ),
        Potravina(
            nazev="Kedlubna",
            kategorie="zelenina",
            kalorie=27,
            bilkoviny=1.7,
            sacharidy=6.2,
            tuky=0.1,
            vlaknina=3.6,
            cena_za_kg=30.0,
            sezona=["5", "6", "7", "8"]
        ),
        Potravina(
            nazev="Červená řepa",
            kategorie="zelenina",
            kalorie=43,
            bilkoviny=1.6,
            sacharidy=9.6,
            tuky=0.2,
            vlaknina=2.8,
            cena_za_kg=25.0,
            sezona=["9", "10", "11", "12", "1", "2"],
            poznamky="Hodnoty platí pro vařenou řepu"
        ),
        
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
    def _get_all_potraviny(cls) -> List[Potravina]:
        """Vrátí všechny potraviny (s cachováním)."""
        if cls._cache is None:
            cls._cache = cls._load_from_yaml_files()
        return cls._cache
    
    # Module-level access to POTRAVINY for backward compatibility
    @property
    def POTRAVINY(self) -> List[Potravina]:
        """Property for instance access to POTRAVINY."""
        return self.__class__._get_all_potraviny()
    
    @classmethod
    def reload(cls):
        """Znovu načte potraviny ze souborů (užitečné po přidání nových souborů)."""
        cls._cache = None
    
    @classmethod
    def najdi_podle_nazvu(cls, nazev: str) -> Optional[Potravina]:
        """Najde potravinu podle názvu."""
        for potravina in cls._get_all_potraviny():
            if potravina.nazev.lower() == nazev.lower():
                return potravina
        return None
    
    @classmethod
    def najdi_podle_kategorie(cls, kategorie: str) -> List[Potravina]:
        """Najde všechny potraviny v dané kategorii."""
        return [p for p in cls._get_all_potraviny() if p.kategorie == kategorie]
    
    @classmethod
    def najdi_low_carb(cls, max_sacharidy: float = 10.0) -> List[Potravina]:
        """Najde nízkosacharidové potraviny."""
        return [p for p in cls._get_all_potraviny() if p.je_low_carb(max_sacharidy)]
    
    @classmethod
    def najdi_high_protein(cls, min_bilkoviny: float = 15.0) -> List[Potravina]:
        """Najde vysokobílkovinové potraviny."""
        return [p for p in cls._get_all_potraviny() if p.je_high_protein(min_bilkoviny)]


# Module-level access to POTRAVINY for backward compatibility
DatabazePotravIn.POTRAVINY = DatabazePotravIn._get_all_potraviny()


def main():
    """Ukázka použití modulu potravin."""
    print("=" * 70)
    print("DATABÁZE POTRAVIN")
    print("=" * 70)
    
    # Ukázka kategorií
    all_potraviny = DatabazePotravIn._get_all_potraviny()
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
