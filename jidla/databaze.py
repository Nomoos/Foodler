#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jídla - Modul pro správu hotových jídel složených z více potravin

Tento modul spravuje kompletní jídla připravená ke konzumaci,
která jsou složena z více potravin/ingrediencí.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


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
    """Databáze připravených jídel."""
    
    JIDLA: List[Jidlo] = [
        Jidlo(
            nazev="Kuřecí prsa s brokolicí a olivovým olejem",
            typ="obed",
            ingredience=[
                Ingredience("Kuřecí prsa", 200, "hlavni"),
                Ingredience("Brokolice", 200, "priloha"),
                Ingredience("Olivový olej", 10, "omacka"),
                Ingredience("Česnek", 5, "koření"),
            ],
            kalorie_celkem=428,
            bilkoviny_celkem=67.6,
            sacharidy_celkem=14.7,
            tuky_celkem=15.8,
            vlaknina_celkem=5.2,
            priprava_cas_min=25,
            priprava_postup="1. Kuřecí prsa nakrájet a osolit. 2. Opéct na olivovém oleji s česnekem. 3. Brokolici uvařit na páře nebo blanšírovat.",
            obtiznost="snadna",
            porce=1,
            vhodne_pro_meal_prep=True,
            vydrzi_dni=3,
            poznamky="Ideální pro meal prep, lze připravit 3-4 porce najednou"
        ),
        Jidlo(
            nazev="Salát s tuňákem, vejcem a zeleninou",
            typ="obed",
            ingredience=[
                Ingredience("Tuňák konzervovaný", 100, "hlavni"),
                Ingredience("Vejce", 100, "hlavni"),
                Ingredience("Zelený salát", 100, "priloha"),
                Ingredience("Okurka", 50, "priloha"),
                Ingredience("Rajčata", 50, "priloha"),
                Ingredience("Olivový olej", 10, "omacka"),
            ],
            kalorie_celkem=373,
            bilkoviny_celkem=42.4,
            sacharidy_celkem=5.6,
            tuky_celkem=21.4,
            vlaknina_celkem=2.4,
            priprava_cas_min=15,
            priprava_postup="1. Vejce uvařit natvrdo (10 min). 2. Zeleninu omýt a nakrájet. 3. Smíchat s tuňákem, vejcem a olivovým olejem.",
            obtiznost="snadna",
            porce=1,
            vhodne_pro_meal_prep=True,
            vydrzi_dni=1,
            poznamky="Nejlepší čerstvý, lze připravit den dopředu"
        ),
        Jidlo(
            nazev="Hovězí maso s cuketou",
            typ="vecere",
            ingredience=[
                Ingredience("Hovězí maso libové", 200, "hlavni"),
                Ingredience("Cuketa", 200, "priloha"),
                Ingredience("Cibule", 50, "priloha"),
                Ingredience("Rajčata", 100, "priloha"),
                Ingredience("Olivový olej", 10, "omacka"),
            ],
            kalorie_celkem=660,
            bilkoviny_celkem=54.6,
            sacharidy_celkem=16.3,
            tuky_celkem=43.1,
            vlaknina_celkem=4.5,
            priprava_cas_min=30,
            priprava_postup="1. Hovězí nakrájet na kostky. 2. Opéct na oleji s cibulí. 3. Přidat cuketu a rajčata, dusit 15 min.",
            obtiznost="stredni",
            porce=1,
            vhodne_pro_meal_prep=True,
            vydrzi_dni=4,
            poznamky="Výborné pro víkendový meal prep"
        ),
        Jidlo(
            nazev="Vaječná omeleta se špenátem a sýrem",
            typ="snidane",
            ingredience=[
                Ingredience("Vejce", 150, "hlavni"),
                Ingredience("Špenát čerstvý", 100, "priloha"),
                Ingredience("Sýr eidam", 30, "priloha"),
                Ingredience("Máslo", 10, "omacka"),
            ],
            kalorie_celkem=365,
            bilkoviny_celkem=29.5,
            sacharidy_celkem=5.2,
            tuky_celkem=26.0,
            vlaknina_celkem=2.2,
            priprava_cas_min=10,
            priprava_postup="1. Vejce rozšlehat s trochou soli. 2. Špenát nakrájet. 3. Smažit na másle, přidat špenát a sýr.",
            obtiznost="snadna",
            porce=1,
            vhodne_pro_meal_prep=False,
            poznamky="Nejlepší čerstvě připravená"
        ),
        Jidlo(
            nazev="Tvaroh s lněným semínkem a skořicí",
            typ="svacina",
            ingredience=[
                Ingredience("Tvaroh polotučný", 200, "hlavni"),
                Ingredience("Lněné semínko mleté", 20, "priloha"),
                Ingredience("Skořice", 2, "koření"),
            ],
            kalorie_celkem=313,
            bilkoviny_celkem=35.6,
            sacharidy_celkem=12.8,
            tuky_celkem=16.4,
            vlaknina_celkem=5.4,
            priprava_cas_min=2,
            priprava_postup="1. Tvaroh smíchat s mletým lněným semínkem. 2. Posypat skořicí.",
            obtiznost="snadna",
            porce=1,
            vhodne_pro_meal_prep=True,
            vydrzi_dni=2,
            poznamky="Rychlá proteinová svačina"
        ),
        Jidlo(
            nazev="Losos s kedlubnou a koprem",
            typ="vecere",
            ingredience=[
                Ingredience("Losos", 200, "hlavni"),
                Ingredience("Kedlubna", 200, "priloha"),
                Ingredience("Olivový olej", 10, "omacka"),
                Ingredience("Citrón", 20, "koření"),
                Ingredience("Kopr", 5, "koření"),
            ],
            kalorie_celkem=524,
            bilkoviny_celkem=43.4,
            sacharidy_celkem=13.2,
            tuky_celkem=35.2,
            vlaknina_celkem=7.2,
            priprava_cas_min=25,
            priprava_postup="1. Losos pokapat citrónem a posypat koprem. 2. Péct v troubě 15 min při 180°C. 3. Kedlubnu nakrájet a opéct na pánvi.",
            obtiznost="stredni",
            porce=1,
            vhodne_pro_meal_prep=True,
            vydrzi_dni=2,
            poznamky="Bohatý na Omega-3, vhodné 2x týdně"
        ),
        Jidlo(
            nazev="Cottage cheese s vlašskými ořechy",
            typ="svacina",
            ingredience=[
                Ingredience("Cottage cheese", 200, "hlavni"),
                Ingredience("Vlašské ořechy", 20, "priloha"),
                Ingredience("Skořice", 2, "koření"),
            ],
            kalorie_celkem=327,
            bilkoviny_celkem=31.0,
            sacharidy_celkem=10.8,
            tuky_celkem=21.0,
            vlaknina_celkem=1.3,
            priprava_cas_min=2,
            priprava_postup="1. Cottage cheese dát do misky. 2. Přidat nasekané ořechy. 3. Posypat skořicí.",
            obtiznost="snadna",
            porce=1,
            vhodne_pro_meal_prep=True,
            vydrzi_dni=1,
            poznamky="Rychlá proteinová svačina"
        ),
    ]
    
    @classmethod
    def najdi_podle_nazvu(cls, nazev: str) -> Optional[Jidlo]:
        """Najde jídlo podle názvu."""
        for jidlo in cls.JIDLA:
            if jidlo.nazev.lower() == nazev.lower():
                return jidlo
        return None
    
    @classmethod
    def najdi_podle_typu(cls, typ: str) -> List[Jidlo]:
        """Najde všechna jídla daného typu."""
        return [j for j in cls.JIDLA if j.typ == typ]
    
    @classmethod
    def najdi_meal_prep(cls) -> List[Jidlo]:
        """Najde jídla vhodná pro meal prep."""
        return [j for j in cls.JIDLA if j.vhodne_pro_meal_prep]
    
    @classmethod
    def najdi_rychla(cls, max_minut: int = 15) -> List[Jidlo]:
        """Najde rychlá jídla."""
        return [j for j in cls.JIDLA if j.priprava_cas_min <= max_minut]
    
    @classmethod
    def najdi_low_carb(cls, max_sacharidy: float = 15.0) -> List[Jidlo]:
        """Najde nízkosacharidová jídla."""
        return [j for j in cls.JIDLA if j.je_low_carb(max_sacharidy)]
    
    @classmethod
    def najdi_high_protein(cls, min_bilkoviny: float = 25.0) -> List[Jidlo]:
        """Najde vysokobílkovinová jídla."""
        return [j for j in cls.JIDLA if j.je_high_protein(min_bilkoviny)]


def main():
    """Ukázka použití modulu jídel."""
    print("=" * 70)
    print("DATABÁZE HOTOVÝCH JÍDEL")
    print("=" * 70)
    
    # Všechna jídla
    print("\n🍽️  VŠECHNA JÍDLA:\n")
    for i, jidlo in enumerate(DatabzeJidel.JIDLA, 1):
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
