#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profil osoby 3 - Kubík
Obsahuje osobní údaje a výživové potřeby pro předškolní dítě
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Union
from datetime import date


@dataclass
class DetskyyProfil:
    """Profil předškolního dítěte s výživovými potřebami."""
    
    jmeno: str = "Kubík"
    datum_narozeni: str = "1.1.2021"
    vek_roky: float = 4.5  # roky
    vaha: float = 18.0  # kg (průměr pro 4.5 let)
    vyska: int = 106  # cm (průměr pro 4.5 let)
    pohlavi: str = "chlapec"
    
    # Dietní potřeby (denní příjem pro 4-5 let)
    cil_kalorie: int = 1400  # kcal (průměr pro předškoláky)
    cil_bilkoviny: int = 19  # g (doporučeno 0.95-1.1 g/kg)
    cil_sacharidy: int = 130  # g (minimum pro mozek)
    cil_tuky: int = 47  # g (30-35% energie z tuků)
    cil_vlaknina: int = 18  # g (zvýšeno kvůli zácpě, věk + 10-14g)
    cil_voda: float = 1.3  # l (důležité pro prevenci zácpy)
    
    # Vitamíny a minerály pro zrak
    cil_vitamin_a: int = 400  # mcg (pro 4-8 let)
    cil_vitamin_c: int = 25  # mg
    cil_vitamin_e: int = 7  # mg
    cil_omega_3: float = 0.9  # g (DHA+EPA)
    
    # Počet jídel denně
    pocet_jidel_skolka: int = 3  # dopolední svačina, oběd, odpolední svačina
    pocet_jidel_doma: int = 2  # snídaně, večeře
    pocet_jidel_vikend: int = 5  # všechna jídla doma
    
    # Zdravotní poznámky
    zdravotni_poznamky: List[str] = None
    
    def __post_init__(self):
        if self.zdravotni_poznamky is None:
            self.zdravotni_poznamky = [
                "Brýle: 4 dioptrie",
                "Astigmatismus",
                "Potřeba podpory zraku - vitamin A, beta-karoten",
                "Důraz na oranžovou a zelenou zeleninu",
                "Omega-3 pro zdravý vývoj mozku a očí",
                "Problémy se zácpou - horší průchodnost anusu",
                "Zvýšený příjem vlákniny a tekutin doporučen"
            ]
    
    def vypocti_idealniVahu(self) -> float:
        """
        Vypočítá ideální váhu pro věk podle WHO standardů.
        Pro 4.5 let: průměr 16-20 kg
        """
        # Aproximace: 2 x věk(roky) + 8
        return round(2 * self.vek_roky + 8, 1)
    
    def vypocti_kalorickouPotrebu(self, aktivita: str = "stredni") -> int:
        """
        Vypočítá denní kalorickou potřebu pro předškolní dítě.
        
        Args:
            aktivita: Úroveň aktivity ("nizka", "stredni", "vysoka")
        """
        # Základní potřeba pro předškoláky
        zakladni_potreba = {
            "nizka": 1200,
            "stredni": 1400,
            "vysoka": 1600
        }
        
        return zakladni_potreba.get(aktivita, 1400)
    
    def ziskej_denni_rozlozeni(self) -> Dict[str, Union[int, float]]:
        """Vrátí denní rozložení živin."""
        return {
            "kalorie": self.cil_kalorie,
            "bilkoviny_g": self.cil_bilkoviny,
            "sacharidy_g": self.cil_sacharidy,
            "tuky_g": self.cil_tuky,
            "vlaknina_g": self.cil_vlaknina,
            "voda_l": self.cil_voda,
            "vitamin_a_mcg": self.cil_vitamin_a,
            "vitamin_c_mg": self.cil_vitamin_c,
            "vitamin_e_mg": self.cil_vitamin_e,
            "omega_3_g": self.cil_omega_3
        }
    
    def ziskej_rozlozeni_pracovni_den(self) -> Dict[str, Dict[str, Union[str, float]]]:
        """
        Rozložení jídel během pracovního týdne.
        Snídaně a večeře doma, oběd a svačiny ve školce.
        """
        jidla_doma = self.pocet_jidel_doma
        jidla_skolka = self.pocet_jidel_skolka
        celkem_jidel = jidla_doma + jidla_skolka
        
        # Rozdělení energie: 25% snídaně, 10% svačina, 30% oběd, 10% svačina, 25% večeře
        return {
            "snidane_doma": {
                "kalorie": round(self.cil_kalorie * 0.25, 1),
                "bilkoviny_g": round(self.cil_bilkoviny * 0.25, 1),
                "poznamka": "Doma"
            },
            "dopoledni_svacina_skolka": {
                "kalorie": round(self.cil_kalorie * 0.10, 1),
                "bilkoviny_g": round(self.cil_bilkoviny * 0.10, 1),
                "poznamka": "Ve školce"
            },
            "obed_skolka": {
                "kalorie": round(self.cil_kalorie * 0.30, 1),
                "bilkoviny_g": round(self.cil_bilkoviny * 0.30, 1),
                "poznamka": "Ve školce"
            },
            "odpoledni_svacina_skolka": {
                "kalorie": round(self.cil_kalorie * 0.10, 1),
                "bilkoviny_g": round(self.cil_bilkoviny * 0.10, 1),
                "poznamka": "Ve školce"
            },
            "vecere_doma": {
                "kalorie": round(self.cil_kalorie * 0.25, 1),
                "bilkoviny_g": round(self.cil_bilkoviny * 0.25, 1),
                "poznamka": "Doma"
            }
        }
    
    def ziskej_rozlozeni_vikend(self) -> Dict[str, float]:
        """Rozložení jídel během víkendu - všechna jídla doma."""
        return {
            "kalorie_na_jidlo": round(self.cil_kalorie / self.pocet_jidel_vikend, 1),
            "bilkoviny_g_na_jidlo": round(self.cil_bilkoviny / self.pocet_jidel_vikend, 1),
            "sacharidy_g_na_jidlo": round(self.cil_sacharidy / self.pocet_jidel_vikend, 1),
            "tuky_g_na_jidlo": round(self.cil_tuky / self.pocet_jidel_vikend, 1),
            "pocet_jidel": self.pocet_jidel_vikend
        }
    
    def vypocti_vek_mesice(self) -> int:
        """Vypočítá věk v měsících."""
        return int(self.vek_roky * 12)
    
    def __str__(self) -> str:
        """Lidsky čitelný výpis profilu."""
        idealni_vaha = self.vypocti_idealniVahu()
        vek_mesice = self.vypocti_vek_mesice()
        
        return f"""
Profil: {self.jmeno}
{'=' * 50}
Základní údaje:
  Datum narození: {self.datum_narozeni}
  Věk: {self.vek_roky} let ({vek_mesice} měsíců)
  Váha: {self.vaha} kg
  Výška: {self.vyska} cm
  Pohlaví: {self.pohlavi}
  Ideální váha pro věk: {idealni_vaha} kg
  
Denní výživové potřeby:
  Kalorie: {self.cil_kalorie} kcal
  Bílkoviny: {self.cil_bilkoviny}g
  Sacharidy: {self.cil_sacharidy}g
  Tuky: {self.cil_tuky}g
  Vláknina: {self.cil_vlaknina}g (zvýšeno kvůli zácpě)
  Voda: {self.cil_voda} l/den (důležité!)
  
Podpora zraku (důležité!):
  Vitamin A: {self.cil_vitamin_a} mcg/den
  Vitamin C: {self.cil_vitamin_c} mg/den
  Vitamin E: {self.cil_vitamin_e} mg/den
  Omega-3: {self.cil_omega_3} g/den
  
Stravovací režim:
  Pracovní den: {self.pocet_jidel_doma} jídel doma + {self.pocet_jidel_skolka} jídel ve školce
  Víkend: {self.pocet_jidel_vikend} jídel doma
  
Zdravotní poznámky:
  {chr(10).join(f'• {p}' for p in self.zdravotni_poznamky)}
"""


def main():
    """Ukázka použití profilu."""
    profil = DetskyyProfil()
    print(profil)
    
    print("\n" + "=" * 50)
    print("ROZLOŽENÍ JÍDEL - PRACOVNÍ DEN")
    print("=" * 50)
    rozlozeni_pracovni = profil.ziskej_rozlozeni_pracovni_den()
    for jidlo, data in rozlozeni_pracovni.items():
        print(f"\n{jidlo.replace('_', ' ').title()}:")
        print(f"  Kalorie: {data['kalorie']} kcal")
        print(f"  Bílkoviny: {data['bilkoviny_g']}g")
        print(f"  Kde: {data['poznamka']}")
    
    print("\n" + "=" * 50)
    print("ROZLOŽENÍ JÍDEL - VÍKEND")
    print("=" * 50)
    rozlozeni_vikend = profil.ziskej_rozlozeni_vikend()
    print(f"Počet jídel: {rozlozeni_vikend['pocet_jidel']}")
    print(f"Kalorie na jídlo: {rozlozeni_vikend['kalorie_na_jidlo']} kcal")
    print(f"Bílkoviny na jídlo: {rozlozeni_vikend['bilkoviny_g_na_jidlo']}g")
    print(f"Sacharidy na jídlo: {rozlozeni_vikend['sacharidy_g_na_jidlo']}g")
    print(f"Tuky na jídlo: {rozlozeni_vikend['tuky_g_na_jidlo']}g")
    
    print(f"\nOdhadovaná kalorická potřeba (střední aktivita): {profil.vypocti_kalorickouPotrebu('stredni')} kcal")


if __name__ == "__main__":
    main()
