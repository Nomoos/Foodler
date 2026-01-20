#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyzátor jídelníčku pro Páju
Umožňuje zadat potraviny a analyzovat, jak splňují denní cíle
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class NutritionalTarget:
    """Denní nutriční cíle pro Páju"""
    kalorie: int = 1508
    bilkoviny: int = 92  # minimum
    sacharidy: int = 60  # maximum
    tuky: int = 100
    vlaknina: int = 20


@dataclass
class Food:
    """Potravina s nutričními hodnotami na 100g"""
    nazev: str
    kalorie: float
    bilkoviny: float
    sacharidy: float
    tuky: float
    vlaknina: float
    
    def scaled(self, mnozstvi_g: float) -> 'FoodPortion':
        """Vrátí porci potraviny s přepočítanými hodnotami"""
        factor = mnozstvi_g / 100.0
        return FoodPortion(
            nazev=self.nazev,
            mnozstvi=mnozstvi_g,
            kalorie=self.kalorie * factor,
            bilkoviny=self.bilkoviny * factor,
            sacharidy=self.sacharidy * factor,
            tuky=self.tuky * factor,
            vlaknina=self.vlaknina * factor
        )


@dataclass
class FoodPortion:
    """Konkrétní porce potraviny"""
    nazev: str
    mnozstvi: float  # gramy
    kalorie: float
    bilkoviny: float
    sacharidy: float
    tuky: float
    vlaknina: float


# Databáze potravin (na 100g)
POTRAVINY = {
    # Zelenina
    "ledový salát": Food("Ledový salát", 15, 1.4, 2.9, 0.2, 1.3),
    "paprika červená": Food("Paprika červená", 31, 1.0, 6.0, 0.3, 2.1),
    "paprika kapia": Food("Paprika kapia sladká", 27, 1.0, 6.0, 0.2, 2.1),
    "rajče": Food("Rajče", 18, 0.9, 3.9, 0.2, 1.2),
    "brokolice": Food("Brokolice", 34, 2.8, 7.0, 0.4, 2.6),
    "avokádo": Food("Avokádo", 160, 2.0, 8.5, 14.7, 6.7),
    "cuketa": Food("Cuketa", 17, 1.2, 3.1, 0.3, 1.0),
    
    # Bílkoviny
    "vejce": Food("Vejce", 143, 12.4, 1.1, 10.0, 0),
    "tuňák v oleji": Food("Tuňák v oleji", 191, 20.0, 0, 12.0, 0),
    "tvaroh polotučný": Food("Tvaroh polotučný", 101, 16.0, 3.5, 2.0, 0),
    "cottage cheese": Food("Cottage cheese", 98, 11.1, 3.4, 4.3, 0),
    "iso whey protein": Food("Iso whey protein", 380, 80.0, 0, 4.0, 0),
    
    # Mléčné výrobky
    "císařský sýr": Food("Císařský sýr 45%", 300, 26.0, 0, 22.0, 0),
    "gouda light": Food("Gouda Light", 300, 26.0, 0, 20.0, 0),
    "řecký jogurt": Food("Řecký jogurt 5%", 100, 10.0, 4.0, 5.0, 0),
    
    # Ořechy a semínka
    "mandle": Food("Mandle neloupané", 579, 21.2, 21.7, 49.4, 12.5),
    "vlašské ořechy": Food("Vlašské ořechy", 654, 15.2, 13.7, 65.2, 6.7),
    "kešu": Food("Kešu ořechy", 553, 18.2, 30.2, 43.9, 3.3),
    "pekanové ořechy": Food("Pekanové ořechy", 691, 9.2, 13.9, 72.0, 9.6),
    "chia semínka": Food("Chia semínka", 486, 16.5, 42.1, 30.7, 34.4),
    "lněná semínka": Food("Lněná semínka", 534, 18.3, 28.9, 42.2, 27.3),
    "slunečnicová semínka": Food("Slunečnicová semínka", 584, 20.8, 20.0, 51.5, 8.6),
    
    # Tuky
    "olivový olej": Food("Olivový olej", 900, 0, 0, 100.0, 0),
    "máslo": Food("Máslo", 717, 0.9, 0.1, 81.1, 0),
    
    # Ostatní
    "med": Food("Med včelí", 322, 0.6, 82.4, 0, 0.2),
    "mana": Food("MK8 choco nut Mana", 465, 18.0, 43.0, 22.0, 4.0),
}


class MealAnalyzer:
    """Analyzátor jídelníčku"""
    
    def __init__(self):
        self.cile = NutritionalTarget()
        self.porce: List[FoodPortion] = []
    
    def pridat_potravinu(self, nazev: str, mnozstvi_g: float) -> None:
        """Přidá potravinu do jídelníčku"""
        nazev_lower = nazev.lower()
        if nazev_lower not in POTRAVINY:
            print(f"⚠️  Potravina '{nazev}' není v databázi!")
            return
        
        potravina = POTRAVINY[nazev_lower]
        porce = potravina.scaled(mnozstvi_g)
        self.porce.append(porce)
        print(f"✓ Přidáno: {nazev} {mnozstvi_g}g")
    
    def vypocitat_celkem(self) -> Dict[str, float]:
        """Vypočítá celkové nutriční hodnoty"""
        celkem = {
            "kalorie": 0.0,
            "bilkoviny": 0.0,
            "sacharidy": 0.0,
            "tuky": 0.0,
            "vlaknina": 0.0
        }
        
        for porce in self.porce:
            celkem["kalorie"] += porce.kalorie
            celkem["bilkoviny"] += porce.bilkoviny
            celkem["sacharidy"] += porce.sacharidy
            celkem["tuky"] += porce.tuky
            celkem["vlaknina"] += porce.vlaknina
        
        return celkem
    
    def analyzovat(self) -> None:
        """Vypíše analýzu jídelníčku"""
        if not self.porce:
            print("⚠️  Žádné potraviny nebyly přidány!")
            return
        
        celkem = self.vypocitat_celkem()
        
        print("\n" + "=" * 60)
        print("📊 ANALÝZA JÍDELNÍČKU PRO PÁJU")
        print("=" * 60)
        print()
        
        # Vypsat všechny potraviny
        print("🍽️  SEZNAM POTRAVIN:")
        print("-" * 60)
        for porce in self.porce:
            print(f"  • {porce.nazev} {porce.mnozstvi:.0f}g: "
                  f"{porce.kalorie:.0f} kcal | "
                  f"P: {porce.bilkoviny:.1f}g | "
                  f"S: {porce.sacharidy:.1f}g | "
                  f"T: {porce.tuky:.1f}g | "
                  f"V: {porce.vlaknina:.1f}g")
        
        print()
        print("📊 CELKEM:")
        print("-" * 60)
        print(f"  Kalorie: {celkem['kalorie']:.0f} kcal")
        print(f"  Bílkoviny: {celkem['bilkoviny']:.1f}g")
        print(f"  Sacharidy: {celkem['sacharidy']:.1f}g")
        print(f"  Tuky: {celkem['tuky']:.1f}g")
        print(f"  Vláknina: {celkem['vlaknina']:.1f}g")
        print()
        
        # Porovnání s cíli
        print("🎯 POROVNÁNÍ S DENNÍMI CÍLY:")
        print("-" * 60)
        
        kal_procent = (celkem['kalorie'] / self.cile.kalorie) * 100
        bil_procent = (celkem['bilkoviny'] / self.cile.bilkoviny) * 100
        sach_procent = (celkem['sacharidy'] / self.cile.sacharidy) * 100
        tuky_procent = (celkem['tuky'] / self.cile.tuky) * 100
        vla_procent = (celkem['vlaknina'] / self.cile.vlaknina) * 100
        
        # Kalorie
        status = "✅" if 90 <= kal_procent <= 110 else ("⚠️" if 80 <= kal_procent <= 120 else "❌")
        zbyvajici_kal = self.cile.kalorie - celkem['kalorie']
        print(f"  {status} Kalorie: {celkem['kalorie']:.0f} / {self.cile.kalorie} "
              f"({kal_procent:.1f}%) → {'ZBÝVÁ' if zbyvajici_kal > 0 else 'PŘEBYTEK'}: "
              f"{abs(zbyvajici_kal):.0f} kcal")
        
        # Bílkoviny
        status = "✅" if bil_procent >= 100 else ("⚠️" if bil_procent >= 80 else "❌")
        zbyvajici_bil = self.cile.bilkoviny - celkem['bilkoviny']
        print(f"  {status} Bílkoviny: {celkem['bilkoviny']:.1f}g / {self.cile.bilkoviny}g min "
              f"({bil_procent:.1f}%) → {'CHYBÍ' if zbyvajici_bil > 0 else 'PŘEBYTEK'}: "
              f"{abs(zbyvajici_bil):.1f}g")
        
        # Sacharidy
        status = "✅" if sach_procent <= 100 else ("⚠️" if sach_procent <= 130 else "❌")
        zbyvajici_sach = self.cile.sacharidy - celkem['sacharidy']
        print(f"  {status} Sacharidy: {celkem['sacharidy']:.1f}g / {self.cile.sacharidy}g max "
              f"({sach_procent:.1f}%) → {'REZERVA' if zbyvajici_sach > 0 else 'PŘEBYTEK'}: "
              f"{abs(zbyvajici_sach):.1f}g")
        
        # Tuky
        status = "✅" if 60 <= tuky_procent <= 120 else ("⚠️" if 40 <= tuky_procent <= 140 else "❌")
        zbyvajici_tuky = self.cile.tuky - celkem['tuky']
        print(f"  {status} Tuky: {celkem['tuky']:.1f}g / {self.cile.tuky}g "
              f"({tuky_procent:.1f}%) → {'ZBÝVÁ' if zbyvajici_tuky > 0 else 'PŘEBYTEK'}: "
              f"{abs(zbyvajici_tuky):.1f}g")
        
        # Vláknina
        status = "✅" if vla_procent >= 100 else ("⚠️" if vla_procent >= 75 else "❌")
        zbyvajici_vla = self.cile.vlaknina - celkem['vlaknina']
        print(f"  {status} Vláknina: {celkem['vlaknina']:.1f}g / {self.cile.vlaknina}g min "
              f"({vla_procent:.1f}%) → {'CHYBÍ' if zbyvajici_vla > 0 else 'PŘEBYTEK'}: "
              f"{abs(zbyvajici_vla):.1f}g")
        
        print()
        
        # Doporučení
        self._doporuceni(celkem)
    
    def _doporuceni(self, celkem: Dict[str, float]) -> None:
        """Vypíše doporučení na základě analýzy"""
        doporuceni = []
        
        # Kalorie
        kal_procent = (celkem['kalorie'] / self.cile.kalorie) * 100
        if kal_procent < 80:
            zbyvajici = self.cile.kalorie - celkem['kalorie']
            doporuceni.append(
                f"❌ KALORIE příliš nízké! Chybí {zbyvajici:.0f} kcal. "
                f"Přidat tuky (olivový olej, ořechy, avokádo) nebo bílkoviny (tvaroh, tuňák)."
            )
        elif kal_procent > 120:
            prebytecne = celkem['kalorie'] - self.cile.kalorie
            doporuceni.append(
                f"⚠️ KALORIE příliš vysoké! Přebytek {prebytecne:.0f} kcal. "
                f"Snížit množství tuků nebo ořechů."
            )
        
        # Bílkoviny
        bil_procent = (celkem['bilkoviny'] / self.cile.bilkoviny) * 100
        if bil_procent < 80:
            zbyvajici = self.cile.bilkoviny - celkem['bilkoviny']
            doporuceni.append(
                f"❌ BÍLKOVINY nedostatečné! Chybí {zbyvajici:.1f}g. "
                f"Přidat: tvaroh, tuňák, vejce, sýr, protein."
            )
        
        # Sacharidy
        sach_procent = (celkem['sacharidy'] / self.cile.sacharidy) * 100
        if sach_procent > 130:
            prebytecne = celkem['sacharidy'] - self.cile.sacharidy
            doporuceni.append(
                f"⚠️ SACHARIDY příliš vysoké! Přebytek {prebytecne:.1f}g. "
                f"Snížit množství ovoce, medu nebo zeleniny s více sacharidy."
            )
        
        # Tuky
        tuky_procent = (celkem['tuky'] / self.cile.tuky) * 100
        if tuky_procent < 60:
            zbyvajici = self.cile.tuky - celkem['tuky']
            doporuceni.append(
                f"❌ TUKY příliš nízké! Chybí {zbyvajici:.1f}g. "
                f"Přidat: olivový olej, avokádo, ořechy, semínka."
            )
        
        # Vláknina
        vla_procent = (celkem['vlaknina'] / self.cile.vlaknina) * 100
        if vla_procent < 75:
            zbyvajici = self.cile.vlaknina - celkem['vlaknina']
            doporuceni.append(
                f"❌ VLÁKNINA nedostatečná! Chybí {zbyvajici:.1f}g. "
                f"Přidat: zeleninu (brokolice, salát, paprika), chia semínka, ořechy."
            )
        
        if doporuceni:
            print("💡 DOPORUČENÍ:")
            print("-" * 60)
            for i, d in enumerate(doporuceni, 1):
                print(f"{i}. {d}")
            print()
        else:
            print("🎉 VÝBORNĚ! Jídelníček splňuje všechny cíle!")
            print()


def main():
    """Příklad použití"""
    print("🍽️  ANALYZÁTOR JÍDELNÍČKU PRO PÁJU")
    print("=" * 60)
    print()
    
    # Vytvořit analyzátor
    analyzer = MealAnalyzer()
    
    # Příklad: Den 2 - co je nachystáno
    print("📝 Přidávám potraviny z Dne 2...")
    print()
    
    analyzer.pridat_potravinu("ledový salát", 100)
    analyzer.pridat_potravinu("císařský sýr", 100)
    analyzer.pridat_potravinu("vejce", 55)
    analyzer.pridat_potravinu("tuňák v oleji", 75)
    analyzer.pridat_potravinu("řecký jogurt", 100)
    analyzer.pridat_potravinu("med", 14)
    
    # Analyzovat
    analyzer.analyzovat()
    
    print()
    print("=" * 60)
    print("💡 PRO INTERAKTIVNÍ POUŽITÍ:")
    print("=" * 60)
    print("""
from analyze_paja_meals import MealAnalyzer

analyzer = MealAnalyzer()
analyzer.pridat_potravinu("ledový salát", 100)
analyzer.pridat_potravinu("mandle", 30)
analyzer.pridat_potravinu("avokádo", 80)
# ... přidat další potraviny
analyzer.analyzovat()
""")


if __name__ == "__main__":
    main()
