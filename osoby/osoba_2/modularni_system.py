#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modulární systém jídel pro Páju

Každé jídlo má standardizovanou kalorickou hodnotu podle typu,
což umožňuje snadnou výměnu jídel v jídelníčku.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class TypJidla(Enum):
    """Typ jídla určuje jeho kalorickou kategorii."""
    SNIDANE = "snídaně"
    SVACINA_MALA = "malá svačina"
    SVACINA_VELKA = "velká svačina"
    OBED = "oběd"
    VECERE = "večeře"


@dataclass
class KalorickyModul:
    """
    Definuje cílové kalorie a makra pro každý typ jídla.
    
    Pája má 1508 kcal denně / 5 jídel = ~300 kcal průměr,
    ale chceme nerovnoměrné rozložení:
    - Snídaně: větší (nejvyšší hlad ráno)
    - Svačiny: menší (prevence přejedení)
    - Oběd: střední (ne příliš velký objem!)
    - Večeře: střední
    """
    
    typ: TypJidla
    cilove_kalorie: int
    rozmezi_kalorie: tuple  # (min, max) povolené rozpětí
    cilove_bilkoviny: int
    cilove_sacharidy: int
    cilove_tuky: int
    cilova_vlaknina: int
    
    def je_v_rozmezi(self, kalorie: int) -> bool:
        """Kontroluje, zda kalorie spadají do povoleného rozpětí."""
        return self.rozmezi_kalorie[0] <= kalorie <= self.rozmezi_kalorie[1]
    
    def __str__(self) -> str:
        return f"{self.typ.value}: {self.cilove_kalorie} kcal ({self.rozmezi_kalorie[0]}-{self.rozmezi_kalorie[1]} kcal)"


# Standardní moduly pro Páju (1508 kcal celkem)
MODULY_PAJA = {
    TypJidla.SNIDANE: KalorickyModul(
        typ=TypJidla.SNIDANE,
        cilove_kalorie=400,      # Větší - nejvyšší hlad ráno
        rozmezi_kalorie=(350, 450),
        cilove_bilkoviny=25,
        cilove_sacharidy=15,
        cilove_tuky=25,
        cilova_vlaknina=6
    ),
    TypJidla.SVACINA_MALA: KalorickyModul(
        typ=TypJidla.SVACINA_MALA,
        cilove_kalorie=150,      # Malá svačina
        rozmezi_kalorie=(120, 180),
        cilove_bilkoviny=10,
        cilove_sacharidy=8,
        cilove_tuky=8,
        cilova_vlaknina=3
    ),
    TypJidla.SVACINA_VELKA: KalorickyModul(
        typ=TypJidla.SVACINA_VELKA,
        cilove_kalorie=250,      # Kritické okno 15-16h
        rozmezi_kalorie=(220, 280),
        cilove_bilkoviny=15,
        cilove_sacharidy=12,
        cilove_tuky=15,
        cilova_vlaknina=5
    ),
    TypJidla.OBED: KalorickyModul(
        typ=TypJidla.OBED,
        cilove_kalorie=350,      # Menší než obvykle (problém s objemem)
        rozmezi_kalorie=(300, 400),
        cilove_bilkoviny=30,
        cilove_sacharidy=12,
        cilove_tuky=18,
        cilova_vlaknina=4
    ),
    TypJidla.VECERE: KalorickyModul(
        typ=TypJidla.VECERE,
        cilove_kalorie=350,      # Sdílená s rodinou
        rozmezi_kalorie=(300, 400),
        cilove_bilkoviny=28,
        cilove_sacharidy=13,
        cilove_tuky=18,
        cilova_vlaknina=3
    )
}


@dataclass
class ModularniJidlo:
    """
    Jedno modulární jídlo - lze snadno vyměnit za jiné stejného typu.
    """
    
    nazev: str
    typ: TypJidla
    kalorie: int
    bilkoviny: float
    sacharidy: float
    tuky: float
    vlaknina: float
    
    # Značky pro snadné vyhledávání
    tagy: List[str] = field(default_factory=list)
    
    # Příprava
    cas_pripravy: int = 0  # minuty
    meal_prep_vhodne: bool = False
    
    # Preference Páji
    syti_dobre: bool = False  # vláknina + objem
    problematicke: bool = False  # káva, tuk, atd.
    
    # Ingredience (pro nákupní seznam)
    ingredience: List[str] = field(default_factory=list)
    
    def je_kompatibilni_s_modulem(self, modul: KalorickyModul) -> bool:
        """Kontroluje, zda jídlo odpovídá danému modulu."""
        if self.typ != modul.typ:
            return False
        return modul.je_v_rozmezi(self.kalorie)
    
    def vypocti_odchylku_od_modulu(self, modul: KalorickyModul) -> int:
        """Vypočítá, o kolik se liší od cílových kalorií."""
        return abs(self.kalorie - modul.cilove_kalorie)
    
    def __str__(self) -> str:
        return f"{self.nazev} ({self.typ.value}): {self.kalorie} kcal, P{self.bilkoviny}g C{self.sacharidy}g F{self.tuky}g"


@dataclass
class ModularniJidelnicek:
    """
    Jídelníček sestavený z modulárních jídel.
    Snadno lze měnit jednotlivá jídla.
    """
    
    datum: str
    jidla: Dict[TypJidla, ModularniJidlo] = field(default_factory=dict)
    
    def pridej_jidlo(self, jidlo: ModularniJidlo):
        """Přidá jídlo do jídelníčku."""
        self.jidla[jidlo.typ] = jidlo
    
    def vymenit_jidlo(self, typ: TypJidla, nove_jidlo: ModularniJidlo):
        """Vymění jídlo daného typu za jiné."""
        if nove_jidlo.typ != typ:
            raise ValueError(f"Nové jídlo musí být typu {typ.value}")
        self.jidla[typ] = nove_jidlo
    
    def vypocti_celkove_makro(self) -> Dict[str, float]:
        """Vypočítá celkové makronutrienty za den."""
        return {
            "kalorie": sum(j.kalorie for j in self.jidla.values()),
            "bilkoviny": sum(j.bilkoviny for j in self.jidla.values()),
            "sacharidy": sum(j.sacharidy for j in self.jidla.values()),
            "tuky": sum(j.tuky for j in self.jidla.values()),
            "vlaknina": sum(j.vlaknina for j in self.jidla.values())
        }
    
    def je_v_cili(self, cil_kalorie: int = 1508, tolerance: int = 50) -> bool:
        """Kontroluje, zda je jídelníček v cílovém rozmezí kalorií."""
        celkem = self.vypocti_celkove_makro()
        return abs(celkem['kalorie'] - cil_kalorie) <= tolerance
    
    def __str__(self) -> str:
        makro = self.vypocti_celkove_makro()
        vysledek = f"\nJídelníček pro {self.datum}\n{'=' * 60}\n"
        
        poradi = [
            TypJidla.SNIDANE,
            TypJidla.SVACINA_MALA,
            TypJidla.OBED,
            TypJidla.SVACINA_VELKA,
            TypJidla.VECERE
        ]
        
        for typ in poradi:
            if typ in self.jidla:
                jidlo = self.jidla[typ]
                vysledek += f"\n{typ.value.upper()}: {jidlo.nazev}\n"
                vysledek += f"  {jidlo.kalorie} kcal | P{jidlo.bilkoviny}g C{jidlo.sacharidy}g F{jidlo.tuky}g V{jidlo.vlaknina}g\n"
                if jidlo.syti_dobre:
                    vysledek += f"  ✓ Sytící\n"
                if jidlo.problematicke:
                    vysledek += f"  ⚠️  Problematické\n"
        
        vysledek += f"\n{'=' * 60}\n"
        vysledek += f"CELKEM: {makro['kalorie']:.0f} kcal | "
        vysledek += f"P{makro['bilkoviny']:.0f}g C{makro['sacharidy']:.0f}g "
        vysledek += f"F{makro['tuky']:.0f}g V{makro['vlaknina']:.0f}g\n"
        
        return vysledek


def vytvor_ukatkovy_jidelnicek() -> ModularniJidelnicek:
    """Vytvoří ukázkový modulární jídelníček pro Páju."""
    
    # Definice modulárních jídel
    snidane = ModularniJidlo(
        nazev="Ovesná kaše s ovocem a jogurtem",
        typ=TypJidla.SNIDANE,
        kalorie=400,
        bilkoviny=25,
        sacharidy=45,
        tuky=12,
        vlaknina=8,
        tagy=["vláknina", "sytící", "meal_prep"],
        cas_pripravy=10,
        meal_prep_vhodne=True,
        syti_dobre=True,
        problematicke=False,
        ingredience=["ovesné vločky", "banán", "jogurt", "chia semínka"]
    )
    
    svacina_1 = ModularniJidlo(
        nazev="Jablko + hrst mandlí",
        typ=TypJidla.SVACINA_MALA,
        kalorie=150,
        bilkoviny=4,
        sacharidy=18,
        tuky=8,
        vlaknina=4,
        tagy=["rychlé", "přenosné"],
        cas_pripravy=2,
        meal_prep_vhodne=True,
        syti_dobre=False,
        problematicke=False,
        ingredience=["jablko", "mandle"]
    )
    
    obed = ModularniJidlo(
        nazev="Luštěniny s cuketou a semínky",
        typ=TypJidla.OBED,
        kalorie=350,
        bilkoviny=20,
        sacharidy=40,
        tuky=10,
        vlaknina=12,
        tagy=["vláknina", "sytící", "meal_prep", "lehké"],
        cas_pripravy=20,
        meal_prep_vhodne=True,
        syti_dobre=True,
        problematicke=False,
        ingredience=["čočka", "cuketa", "slunečnicová semínka", "olivový olej"]
    )
    
    svacina_2 = ModularniJidlo(
        nazev="Řecký jogurt s ovocem",
        typ=TypJidla.SVACINA_VELKA,
        kalorie=250,
        bilkoviny=20,
        sacharidy=25,
        tuky=8,
        vlaknina=3,
        tagy=["protein", "rychlé", "krabička"],
        cas_pripravy=5,
        meal_prep_vhodne=True,
        syti_dobre=True,
        problematicke=False,
        ingredience=["řecký jogurt", "jahody", "borůvky"]
    )
    
    vecere = ModularniJidlo(
        nazev="Kuřecí prsa s brokolicí",
        typ=TypJidla.VECERE,
        kalorie=350,
        bilkoviny=45,
        sacharidy=15,
        tuky=12,
        vlaknina=5,
        tagy=["protein", "lehké", "rodinné"],
        cas_pripravy=25,
        meal_prep_vhodne=True,
        syti_dobre=False,
        problematicke=False,
        ingredience=["kuřecí prsa", "brokolice", "olivový olej", "česnek"]
    )
    
    # Sestavení jídelníčku
    jidelnicek = ModularniJidelnicek(datum="2026-01-20")
    jidelnicek.pridej_jidlo(snidane)
    jidelnicek.pridej_jidlo(svacina_1)
    jidelnicek.pridej_jidlo(obed)
    jidelnicek.pridej_jidlo(svacina_2)
    jidelnicek.pridej_jidlo(vecere)
    
    return jidelnicek


def demo_vymena_jidla():
    """Ukázka výměny jídla v jídelníčku."""
    
    print("=" * 70)
    print("DEMO: MODULÁRNÍ SYSTÉM JÍDEL")
    print("=" * 70)
    
    # Zobrazit moduly
    print("\n📊 KALORIE MODULY PRO PÁJU:")
    print("-" * 70)
    for typ, modul in MODULY_PAJA.items():
        print(f"  {modul}")
    
    print(f"\n  Celkem: {sum(m.cilove_kalorie for m in MODULY_PAJA.values())} kcal/den")
    
    # Vytvořit jídelníček
    print("\n\n📅 PŮVODNÍ JÍDELNÍČEK:")
    jidelnicek = vytvor_ukatkovy_jidelnicek()
    print(jidelnicek)
    
    # Výměna snídaně
    print("\n🔄 VÝMĚNA SNÍDANĚ:")
    print("-" * 70)
    
    alternativni_snidane = ModularniJidlo(
        nazev="Vejce (3ks) + avokádo + celozrnný chléb",
        typ=TypJidla.SNIDANE,
        kalorie=420,
        bilkoviny=28,
        sacharidy=22,
        tuky=25,
        vlaknina=10,
        tagy=["protein", "tuky", "rychlé"],
        cas_pripravy=10,
        meal_prep_vhodne=False,
        syti_dobre=True,
        problematicke=False,
        ingredience=["vejce", "avokádo", "celozrnný chléb"]
    )
    
    print(f"Původní: {jidelnicek.jidla[TypJidla.SNIDANE]}")
    print(f"Nová:    {alternativni_snidane}")
    
    # Kontrola kompatibility
    modul_snidane = MODULY_PAJA[TypJidla.SNIDANE]
    if alternativni_snidane.je_kompatibilni_s_modulem(modul_snidane):
        print(f"✅ Kompatibilní s modulem {modul_snidane.typ.value}")
        odchylka = alternativni_snidane.vypocti_odchylku_od_modulu(modul_snidane)
        print(f"   Odchylka: {odchylka} kcal")
    
    # Provedení výměny
    jidelnicek.vymenit_jidlo(TypJidla.SNIDANE, alternativni_snidane)
    
    print("\n\n📅 JÍDELNÍČEK PO VÝMĚNĚ:")
    print(jidelnicek)
    
    # Kontrola cíle
    if jidelnicek.je_v_cili():
        print("✅ Jídelníček je v cílovém rozmezí!")
    else:
        print("⚠️  Jídelníček je mimo cílové rozmezí")


def main():
    """Hlavní demo."""
    demo_vymena_jidla()
    
    print("\n\n💡 VÝHODY MODULÁRNÍHO SYSTÉMU:")
    print("=" * 70)
    print("✅ Snadná výměna jídel stejného typu")
    print("✅ Kontrola kalorií v každém jídle")
    print("✅ Flexibilní plánování jídelníčku")
    print("✅ Automatická kontrola celkových kalorií")
    print("✅ Možnost mít databázi alternativ pro každý modul")
    print("\n📚 Použití:")
    print("  • Vyber typ jídla (snídaně, svačina, oběd, ...)")
    print("  • Vyfiltruj jídla kompatibilní s modulem")
    print("  • Vyměň za jakékoliv jídlo stejného typu")
    print("  • Systém automaticky kontroluje kalorie")
    print()


if __name__ == "__main__":
    main()
