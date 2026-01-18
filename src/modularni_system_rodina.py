#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Škálovatelný modulární systém pro více osob

Umožňuje vytvořit moduly pro různé osoby s různými:
- počty jídel (Roman 6, Pája 5, Kubík 5)
- cílovými kaloriemi
- suplementy
- preferencemi
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class TypJidla(Enum):
    """Typ jídla - univerzální pro všechny osoby."""
    SNIDANE = "snídaně"
    DOPOLEDNI_SVACINA = "dopolední svačina"
    OBED = "oběd"
    ODPOLEDNI_SVACINA = "odpolední svačina"
    VECERE = "večeře"
    VECERNI_SVACINA = "večerní svačina"  # Pro Romana


@dataclass
class Suplement:
    """Definice suplementu."""
    nazev: str
    davka: str
    cas_podani: str  # "ráno", "s jídlem", "večer"
    poznamka: Optional[str] = None


@dataclass
class KalorickyModul:
    """
    Definuje cílové kalorie a makra pro každý typ jídla.
    Univerzální pro všechny osoby.
    """
    
    typ: TypJidla
    cilove_kalorie: int
    rozmezi_kalorie: Tuple[int, int]  # (min, max)
    cilove_bilkoviny: int
    cilove_sacharidy: int
    cilove_tuky: int
    cilova_vlaknina: int
    
    def je_v_rozmezi(self, kalorie: int) -> bool:
        """Kontroluje, zda kalorie spadají do povoleného rozpětí."""
        return self.rozmezi_kalorie[0] <= kalorie <= self.rozmezi_kalorie[1]
    
    def vypocti_odchylku(self, kalorie: int) -> int:
        """Vypočítá odchylku od cílových kalorií."""
        return abs(kalorie - self.cilove_kalorie)
    
    def __str__(self) -> str:
        return f"{self.typ.value}: {self.cilove_kalorie} kcal ({self.rozmezi_kalorie[0]}-{self.rozmezi_kalorie[1]} kcal)"


@dataclass
class OsobniModularniSystem:
    """
    Modulární systém pro jednu osobu.
    
    Každá osoba má vlastní:
    - počet jídel
    - kalorie moduly
    - suplementy
    - preference
    """
    
    jmeno: str
    celkove_kalorie: int
    pocet_jidel: int
    moduly: Dict[TypJidla, KalorickyModul] = field(default_factory=dict)
    suplementy: List[Suplement] = field(default_factory=list)
    poznamky: List[str] = field(default_factory=list)
    
    def pridej_modul(self, modul: KalorickyModul):
        """Přidá kalorický modul."""
        self.moduly[modul.typ] = modul
    
    def pridej_suplement(self, suplement: Suplement):
        """Přidá suplement."""
        self.suplementy.append(suplement)
    
    def ziskej_sumu_modulu(self) -> int:
        """Vypočítá celkové kalorie ze všech modulů."""
        return sum(m.cilove_kalorie for m in self.moduly.values())
    
    def je_konzistentni(self, tolerance: int = 50) -> bool:
        """
        Kontroluje, zda suma modulů odpovídá celkovým kaloriím.
        
        Args:
            tolerance: Povolená odchylka v kcal
        """
        suma = self.ziskej_sumu_modulu()
        return abs(suma - self.celkove_kalorie) <= tolerance
    
    def __str__(self) -> str:
        suma = self.ziskej_sumu_modulu()
        konzistence = "✅" if self.je_konzistentni() else "⚠️"
        
        vysledek = f"\n{'=' * 60}\n"
        vysledek += f"MODULÁRNÍ SYSTÉM: {self.jmeno}\n"
        vysledek += f"{'=' * 60}\n\n"
        vysledek += f"Cílové kalorie: {self.celkove_kalorie} kcal/den\n"
        vysledek += f"Počet jídel: {self.pocet_jidel}\n"
        vysledek += f"Suma modulů: {suma} kcal {konzistence}\n"
        
        if self.moduly:
            vysledek += f"\n📊 KALORIE MODULY:\n"
            vysledek += "-" * 60 + "\n"
            for typ in TypJidla:
                if typ in self.moduly:
                    vysledek += f"  {self.moduly[typ]}\n"
        
        if self.suplementy:
            vysledek += f"\n💊 SUPLEMENTY:\n"
            vysledek += "-" * 60 + "\n"
            for sup in self.suplementy:
                vysledek += f"  • {sup.nazev} ({sup.davka}) - {sup.cas_podani}\n"
                if sup.poznamka:
                    vysledek += f"    Poznámka: {sup.poznamka}\n"
        
        if self.poznamky:
            vysledek += f"\n📝 POZNÁMKY:\n"
            vysledek += "-" * 60 + "\n"
            for poznamka in self.poznamky:
                vysledek += f"  • {poznamka}\n"
        
        return vysledek


def vytvor_system_pro_romanu() -> OsobniModularniSystem:
    """
    Vytvoří modulární systém pro Romana.
    
    Roman má:
    - 6 jídel denně
    - 2001 kcal
    - Více suplementů (Omeprazol, tlak)
    """
    
    system = OsobniModularniSystem(
        jmeno="Roman",
        celkove_kalorie=2001,
        pocet_jidel=6
    )
    
    # Moduly - 6 jídel, relativně rovnoměrné
    # Kalorie: 2001 / 6 = ~333 kcal průměr
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.SNIDANE,
        cilove_kalorie=350,
        rozmezi_kalorie=(300, 400),
        cilove_bilkoviny=25,
        cilove_sacharidy=12,
        cilove_tuky=22,
        cilova_vlaknina=4
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.DOPOLEDNI_SVACINA,
        cilove_kalorie=250,
        rozmezi_kalorie=(200, 300),
        cilove_bilkoviny=15,
        cilove_sacharidy=10,
        cilove_tuky=15,
        cilova_vlaknina=3
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.OBED,
        cilove_kalorie=450,  # Větší oběd
        rozmezi_kalorie=(400, 500),
        cilove_bilkoviny=35,
        cilove_sacharidy=15,
        cilove_tuky=28,
        cilova_vlaknina=5
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.ODPOLEDNI_SVACINA,
        cilove_kalorie=250,
        rozmezi_kalorie=(200, 300),
        cilove_bilkoviny=15,
        cilove_sacharidy=10,
        cilove_tuky=15,
        cilova_vlaknina=3
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.VECERE,
        cilove_kalorie=450,
        rozmezi_kalorie=(400, 500),
        cilove_bilkoviny=35,
        cilove_sacharidy=15,
        cilove_tuky=28,
        cilova_vlaknina=4
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.VECERNI_SVACINA,
        cilove_kalorie=250,
        rozmezi_kalorie=(200, 300),
        cilove_bilkoviny=15,
        cilove_sacharidy=8,
        cilove_tuky=18,
        cilova_vlaknina=2
    ))
    
    # Suplementy - Roman má víc
    system.pridej_suplement(Suplement(
        nazev="Omeprazol",
        davka="20 mg",
        cas_podani="ráno nalačno",
        poznamka="Léčba refluxu - 30 min před jídlem"
    ))
    
    system.pridej_suplement(Suplement(
        nazev="Léky na tlak",
        davka="dle předpisu",
        cas_podani="ráno",
        poznamka="Kardiovaskulární podpora"
    ))
    
    system.pridej_suplement(Suplement(
        nazev="Multivitamin",
        davka="1 tableta",
        cas_podani="s jídlem"
    ))
    
    system.pridej_suplement(Suplement(
        nazev="Omega-3",
        davka="1000 mg",
        cas_podani="s jídlem"
    ))
    
    system.pridej_suplement(Suplement(
        nazev="Vitamin D",
        davka="2000 IU",
        cas_podani="s jídlem"
    ))
    
    system.pridej_suplement(Suplement(
        nazev="Probiotika",
        davka="1 kapsle",
        cas_podani="ráno"
    ))
    
    # Poznámky
    system.poznamky = [
        "6 jídel denně - menší, častější",
        "Protein first přístup",
        "Max 70g sacharidů denně",
        "Večerní svačina pomáhá s nočním hladem"
    ]
    
    return system


def vytvor_system_pro_paju() -> OsobniModularniSystem:
    """
    Vytvoří modulární systém pro Páju.
    
    Pája má:
    - 5 jídel denně
    - 1508 kcal
    - Letrox + hormonální antikoncepce
    - Nerovnoměrné rozložení (větší snídaně, menší oběd)
    """
    
    system = OsobniModularniSystem(
        jmeno="Pája",
        celkove_kalorie=1508,
        pocet_jidel=5
    )
    
    # Moduly - 5 jídel, NErovnoměrné podle preferencí
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.SNIDANE,
        cilove_kalorie=400,  # Větší - nejvyšší hlad ráno
        rozmezi_kalorie=(350, 450),
        cilove_bilkoviny=25,
        cilove_sacharidy=15,
        cilove_tuky=25,
        cilova_vlaknina=6
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.DOPOLEDNI_SVACINA,
        cilove_kalorie=150,  # Malá
        rozmezi_kalorie=(120, 180),
        cilove_bilkoviny=10,
        cilove_sacharidy=8,
        cilove_tuky=8,
        cilova_vlaknina=3
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.OBED,
        cilove_kalorie=350,  # Menší - problém s objemem
        rozmezi_kalorie=(300, 400),
        cilove_bilkoviny=30,
        cilove_sacharidy=12,
        cilove_tuky=18,
        cilova_vlaknina=4
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.ODPOLEDNI_SVACINA,
        cilove_kalorie=250,  # Větší - kritické okno 15-16h
        rozmezi_kalorie=(220, 280),
        cilove_bilkoviny=15,
        cilove_sacharidy=12,
        cilove_tuky=15,
        cilova_vlaknina=5
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.VECERE,
        cilove_kalorie=350,
        rozmezi_kalorie=(300, 400),
        cilove_bilkoviny=28,
        cilove_sacharidy=13,
        cilove_tuky=18,
        cilova_vlaknina=3
    ))
    
    # Suplementy
    system.pridej_suplement(Suplement(
        nazev="Letrox",
        davka="dle předpisu",
        cas_podani="5:35 ráno nalačno",
        poznamka="Štítná žláza - 30 min před jídlem!"
    ))
    
    system.pridej_suplement(Suplement(
        nazev="Hormonální antikoncepce",
        davka="dle předpisu",
        cas_podani="večer",
        poznamka="Pravidelnost důležitá"
    ))
    
    system.pridej_suplement(Suplement(
        nazev="Vitamin D",
        davka="1000-2000 IU",
        cas_podani="5:36 s vodou",
        poznamka="Nedostatečně pravidelně - zlepšit!"
    ))
    
    system.pridej_suplement(Suplement(
        nazev="Omega-3",
        davka="1000 mg",
        cas_podani="5:36 s vodou",
        poznamka="Nedostatečně pravidelně - zlepšit!"
    ))
    
    system.pridej_suplement(Suplement(
        nazev="Magnesium",
        davka="300 mg",
        cas_podani="5:36 s vodou",
        poznamka="Nedostatečně pravidelně - zlepšit!"
    ))
    
    # Poznámky
    system.poznamky = [
        "5 jídel denně - nerovnoměrné rozložení",
        "Největší snídaně (400 kcal) - nejvyšší hlad ráno",
        "Menší oběd (350 kcal) - citlivost na objem",
        "Větší odpolední svačina (250 kcal) - kritické okno 15-16h",
        "Sytost: vláknina + objem + sladkost (NE tuk!)",
        "Vyhnout se: káva (spouští chutě), velké porce"
    ]
    
    return system


def vytvor_system_pro_kubika() -> OsobniModularniSystem:
    """
    Vytvoří modulární systém pro Kubíka.
    
    Kubík má:
    - 5 jídel denně (pracovní den: 2 doma + 3 školka)
    - 1400 kcal
    - Důraz na vitamin A (zrak)
    - Více sacharidů (dětská potřeba)
    """
    
    system = OsobniModularniSystem(
        jmeno="Kubík",
        celkove_kalorie=1400,
        pocet_jidel=5
    )
    
    # Moduly - 5 jídel, rovnoměrnější než dospělí
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.SNIDANE,
        cilove_kalorie=350,  # 25% (doma)
        rozmezi_kalorie=(300, 400),
        cilove_bilkoviny=10,
        cilove_sacharidy=45,  # Více sacharidů pro dítě
        cilove_tuky=12,
        cilova_vlaknina=5
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.DOPOLEDNI_SVACINA,
        cilove_kalorie=140,  # 10% (školka)
        rozmezi_kalorie=(100, 180),
        cilove_bilkoviny=4,
        cilove_sacharidy=20,
        cilove_tuky=5,
        cilova_vlaknina=3
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.OBED,
        cilove_kalorie=420,  # 30% (školka)
        rozmezi_kalorie=(380, 460),
        cilove_bilkoviny=12,
        cilove_sacharidy=55,
        cilove_tuky=15,
        cilova_vlaknina=6
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.ODPOLEDNI_SVACINA,
        cilove_kalorie=140,  # 10% (školka)
        rozmezi_kalorie=(100, 180),
        cilove_bilkoviny=4,
        cilove_sacharidy=20,
        cilove_tuky=5,
        cilova_vlaknina=3
    ))
    
    system.pridej_modul(KalorickyModul(
        typ=TypJidla.VECERE,
        cilove_kalorie=350,  # 25% (doma)
        rozmezi_kalorie=(300, 400),
        cilove_bilkoviny=10,
        cilove_sacharidy=45,
        cilove_tuky=12,
        cilova_vlaknina=5
    ))
    
    # Suplementy - zaměřené na zrak
    system.pridej_suplement(Suplement(
        nazev="Vitamin A",
        davka="400 mcg",
        cas_podani="s jídlem",
        poznamka="Pro zrak - 4 dioptrie!"
    ))
    
    system.pridej_suplement(Suplement(
        nazev="Omega-3 (DHA)",
        davka="900 mg",
        cas_podani="s jídlem",
        poznamka="Vývoj mozku a očí"
    ))
    
    # Poznámky
    system.poznamky = [
        "Pracovní den: 2 jídla doma, 3 ve školce",
        "Víkend: všech 5 jídel doma",
        "Důraz na vitamin A - mrkev, sladké brambory, špenát",
        "Beta-karoten z oranžové a zelené zeleniny",
        "Zvýšená vláknina kvůli zácpě (18g/den)",
        "Hodně tekutin (1.3 l/den)",
        "Více sacharidů než dospělí (130g min. pro mozek)"
    ]
    
    return system


def porovnej_systemy():
    """Porovná modulární systémy všech tří osob."""
    
    roman = vytvor_system_pro_romanu()
    paja = vytvor_system_pro_paju()
    kubik = vytvor_system_pro_kubika()
    
    print("\n" + "=" * 70)
    print("POROVNÁNÍ MODULÁRNÍCH SYSTÉMŮ RODINY")
    print("=" * 70)
    
    print(roman)
    print(paja)
    print(kubik)
    
    # Souhrnná tabulka
    print("\n" + "=" * 70)
    print("SOUHRNNÉ POROVNÁNÍ")
    print("=" * 70)
    
    print(f"\n{'Osoba':<15} {'Kalorie':<12} {'Jídel':<8} {'Suplementy':<12} {'Konzistence'}")
    print("-" * 70)
    
    for system in [roman, paja, kubik]:
        konzistence = "✅" if system.je_konzistentni() else "⚠️"
        print(f"{system.jmeno:<15} {system.celkove_kalorie:<12} {system.pocet_jidel:<8} {len(system.suplementy):<12} {konzistence}")
    
    celkem_kalorie = roman.celkove_kalorie + paja.celkove_kalorie + kubik.celkove_kalorie
    print("-" * 70)
    print(f"{'CELKEM RODINA':<15} {celkem_kalorie:<12} {'13-16':<8} {'12-14':<12}")
    
    # Klíčové rozdíly
    print("\n" + "=" * 70)
    print("KLÍČOVÉ ROZDÍLY")
    print("=" * 70)
    
    print("\n🍽️ POČET JÍDEL:")
    print(f"  • Roman: {roman.pocet_jidel} jídel (včetně večerní svačiny)")
    print(f"  • Pája: {paja.pocet_jidel} jídel (bez večerní svačiny)")
    print(f"  • Kubík: {kubik.pocet_jidel} jídel (2 doma + 3 školka)")
    
    print("\n💊 SUPLEMENTY:")
    print(f"  • Roman: {len(roman.suplementy)} suplementů (Omeprazol + tlak)")
    print(f"  • Pája: {len(paja.suplementy)} suplementů (Letrox + antikoncepce)")
    print(f"  • Kubík: {len(kubik.suplementy)} suplementů (vitamin A pro zrak)")
    
    print("\n📊 ROZLOŽENÍ KALORIÍ:")
    print(f"  • Roman: Rovnoměrné (~333 kcal/jídlo)")
    print(f"  • Pája: NErovnoměrné (400→150→350→250→350)")
    print(f"  • Kubík: Školní režim (25%→10%→30%→10%→25%)")
    
    print("\n🎯 SPECIÁLNÍ POŽADAVKY:")
    print(f"  • Roman: Večerní svačina proti nočnímu hladu")
    print(f"  • Pája: Větší snídaně (hlad ráno), menší oběd (objem)")
    print(f"  • Kubík: Vitamin A pro zrak, víc sacharidů")


def main():
    """Hlavní demo."""
    porovnej_systemy()
    
    print("\n\n💡 VÝHODY ŠKÁLOVATELNÉHO SYSTÉMU:")
    print("=" * 70)
    print("✅ Každá osoba má vlastní počet jídel")
    print("✅ Každá osoba má vlastní kalorické moduly")
    print("✅ Každá osoba má vlastní suplementy")
    print("✅ Systém kontroluje konzistenci (suma = cíl)")
    print("✅ Snadno přidáš další osobu")
    print("✅ Sdílená databáze jídel pro všechny")
    
    print("\n📚 POUŽITÍ:")
    print("  1. Vytvoř systém pro osobu: vytvor_system_pro_xxx()")
    print("  2. Systém obsahuje všechny moduly + suplementy")
    print("  3. Použij stejná jídla, jen s různými kaloriemi")
    print("  4. Např. \"Ovesná kaše\" může být 400 kcal pro Páju,")
    print("     350 kcal pro Romana, 350 kcal pro Kubíka")
    print()


if __name__ == "__main__":
    main()
