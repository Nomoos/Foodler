#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profil osoby 2 - Pája (Pavla)
Obsahuje osobní údaje a cíle pro hubnutí
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class OsobniProfil:
    """Osobní profil s antropometrickými daty a dietními cíli."""
    
    jmeno: str = "Pája (Pavla)"
    vaha: float = 77.3  # kg (měření 22.12.2025)
    vyska: int = 170  # cm
    pohlavi: str = "žena"
    procento_tuku: float = 39.6  # % (měření 22.12.2025)
    tuková_hmota: float = 30.6  # kg (měření 22.12.2025)
    svalová_hmota: float = 25.6  # kg (SSM, měření 22.12.2025)
    vfa: float = 147.2  # cm2/level (viscerální tuk, měření 22.12.2025)
    
    # Dietní cíle (denní příjem) - budou zpřesněny
    cil_kalorie: int = 1600  # kcal (nižší než osoba 1)
    cil_bilkoviny: int = 100  # g (minimum)
    cil_sacharidy: int = 60   # g (maximum)
    cil_tuky: int = 100       # g
    cil_vlaknina: int = 20    # g (minimum, ideálně více)
    
    # Počet jídel denně
    pocet_jidel: int = 5
    
    # Zdravotní poznámky
    zdravotni_poznamky: List[str] = None
    
    def __post_init__(self):
        if self.zdravotni_poznamky is None:
            self.zdravotni_poznamky = [
                "Měření tělesného složení (22.12.2025):",
                "  • Váha: 77.3 kg, PBF: 39.6%, Tuk: 30.6 kg",
                "  • SSM: 25.6 kg, VFA: 147.2 cm²/level",
                "Předchozí měření (19.11.2025):",
                "  • Váha: 76.7 kg, PBF: 39.1%, Tuk: 30.0 kg",
                "  • SSM: 25.6 kg, VFA: 143 cm²/level"
            ]
    
    def vypocti_bmi(self) -> float:
        """Vypočítá BMI (Body Mass Index)."""
        vyska_m = self.vyska / 100
        return round(self.vaha / (vyska_m ** 2), 1)
    
    def vypocti_idealniVahu(self) -> float:
        """Vypočítá ideální váhu podle BMI 22 (ženy)."""
        vyska_m = self.vyska / 100
        return round(22 * (vyska_m ** 2), 1)
    
    def vypocti_kalorickouPotrebu(self, aktivita: str = "sedava") -> int:
        """
        Vypočítá denní kalorickou potřebu podle vzorce Mifflin-St Jeor.
        
        Args:
            aktivita: Úroveň aktivity ("sedava", "lehka", "stredni", "vysoka")
        """
        # Bazální metabolismus (BMR) podle Mifflin-St Jeor pro ženy
        bmr = 10 * self.vaha + 6.25 * self.vyska - 5 * 35 - 161  # Předpokládáme věk 35
        
        # Multiplikátory aktivity
        multiplikatory = {
            "sedava": 1.2,
            "lehka": 1.375,
            "stredni": 1.55,
            "vysoka": 1.725
        }
        
        return int(bmr * multiplikatory.get(aktivita, 1.2))
    
    def ziskej_denni_rozlozeni(self) -> Dict[str, int]:
        """Vrátí denní rozložení makronutrientů."""
        return {
            "kalorie": self.cil_kalorie,
            "bilkoviny_g": self.cil_bilkoviny,
            "sacharidy_g": self.cil_sacharidy,
            "tuky_g": self.cil_tuky,
            "vlaknina_g": self.cil_vlaknina
        }
    
    def ziskej_rozlozeni_na_jidlo(self) -> Dict[str, float]:
        """Vypočítá průměrné makronutrienty na jedno jídlo."""
        return {
            "kalorie": round(self.cil_kalorie / self.pocet_jidel, 1),
            "bilkoviny_g": round(self.cil_bilkoviny / self.pocet_jidel, 1),
            "sacharidy_g": round(self.cil_sacharidy / self.pocet_jidel, 1),
            "tuky_g": round(self.cil_tuky / self.pocet_jidel, 1),
            "vlaknina_g": round(self.cil_vlaknina / self.pocet_jidel, 1)
        }
    
    def __str__(self) -> str:
        """Lidsky čitelný výpis profilu."""
        bmi = self.vypocti_bmi()
        idealni_vaha = self.vypocti_idealniVahu()
        
        return f"""
Profil: {self.jmeno}
{'=' * 50}
Antropometrie:
  Váha: {self.vaha} kg
  Výška: {self.vyska} cm
  Pohlaví: {self.pohlavi}
  BMI: {bmi}
  Procento tuku: {self.procento_tuku}%
  Tuková hmota: {self.tuková_hmota} kg
  Svalová hmota (SSM): {self.svalová_hmota} kg
  VFA (viscerální tuk): {self.vfa} cm²/level
  Ideální váha (BMI 22): {idealni_vaha} kg
  
Denní cíle:
  Kalorie: {self.cil_kalorie} kcal ({self.pocet_jidel} jídel)
  Bílkoviny: min {self.cil_bilkoviny}g
  Sacharidy: max {self.cil_sacharidy}g
  Tuky: {self.cil_tuky}g
  Vláknina: min {self.cil_vlaknina}g
  
Zdravotní poznámky:
  {chr(10).join(f'• {p}' for p in self.zdravotni_poznamky)}
"""


def main():
    """Ukázka použití profilu."""
    profil = OsobniProfil()
    print(profil)
    
    print("\nPrůměrné makro na jídlo:")
    for klic, hodnota in profil.ziskej_rozlozeni_na_jidlo().items():
        print(f"  {klic}: {hodnota}")
    
    print(f"\nOdhadovaná kalorická potřeba (sedavá): {profil.vypocti_kalorickouPotrebu('sedava')} kcal")


if __name__ == "__main__":
    main()
