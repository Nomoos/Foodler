#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profil osoby 1 - Muž
Obsahuje osobní údaje a cíle pro hubnutí
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class OsobniProfil:
    """Osobní profil s antropometrickými daty a dietními cíli."""
    
    jmeno: str = "Osoba 1"
    vaha: float = 135.0  # kg
    vyska: int = 183  # cm
    pohlavi: str = "muž"
    procento_tuku: float = 41.0  # %
    
    # Dietní cíle (denní příjem)
    cil_kalorie: int = 2000  # kcal
    cil_bilkoviny: int = 140  # g (minimum)
    cil_sacharidy: int = 70   # g (maximum)
    cil_tuky: int = 129       # g
    cil_vlaknina: int = 20    # g (minimum, ideálně více)
    
    # Počet jídel denně
    pocet_jidel: int = 6
    
    # Zdravotní poznámky
    zdravotni_poznamky: List[str] = None
    
    def __post_init__(self):
        if self.zdravotni_poznamky is None:
            self.zdravotni_poznamky = [
                "Léky na krevní tlak",
                "Léčba refluxu (Omeprazol)",
                "Kardiovaskulární monitoring"
            ]
    
    def vypocti_bmi(self) -> float:
        """Vypočítá BMI (Body Mass Index)."""
        vyska_m = self.vyska / 100
        return round(self.vaha / (vyska_m ** 2), 1)
    
    def vypocti_idealniVahu(self) -> float:
        """Vypočítá ideální váhu podle BMI 25."""
        vyska_m = self.vyska / 100
        return round(25 * (vyska_m ** 2), 1)
    
    def vypocti_kalorickouPotrebu(self, aktivita: str = "sedava") -> int:
        """
        Vypočítá denní kalorickou potřebu podle vzorce Mifflin-St Jeor.
        
        Args:
            aktivita: Úroveň aktivity ("sedava", "lehka", "stredni", "vysoka")
        """
        # Bazální metabolismus (BMR) podle Mifflin-St Jeor
        bmr = 10 * self.vaha + 6.25 * self.vyska - 5 * 40 + 5  # Předpokládáme věk 40
        
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
  Ideální váha (BMI 25): {idealni_vaha} kg
  
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
