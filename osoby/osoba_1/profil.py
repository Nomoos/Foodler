#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profil osoby 1 - Roman (Romča)
Obsahuje osobní údaje a cíle pro hubnutí

Pro vysvětlení metrik tělesného složení (procento_tuku, svalová_hmota, atd.)
viz: docs/health/METRIKY_DEXA_BIA.md
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class OsobniProfil:
    """
    Osobní profil s antropometrickými daty a dietními cíli.
    
    Metriky tělesného složení (procento_tuku, tuková_hmota, svalová_hmota):
    - Měřeno pomocí BIA (Bioelektrická impedanční analýza) - chytrá váha
    - Pro podrobné vysvětlení všech metrik viz: docs/health/METRIKY_DEXA_BIA.md
    """
    
    jmeno: str = "Roman (Romča)"
    vaha: float = 133.6  # kg (měření 18.1.2026 09:52)
    vyska: int = 183  # cm
    vek: int = 34  # roky
    pohlavi: str = "muž"
    procento_tuku: float = 37.0  # %
    tuková_hmota: float = 49.43  # kg (měřeno smart váhou)
    svalová_hmota: float = 84.17  # kg (vypočteno: 133.6 - 49.43)
    
    # Metabolismus
    bazalni_metabolismus: int = 2300  # kcal (vlastní BMR)
    
    # Dietní cíle (denní příjem) - udržitelná keto/low-carb dieta
    cil_kalorie: int = 2000  # kcal
    cil_bilkoviny: int = 140  # g (32%, minimum 93g, maximum 154g)
    cil_sacharidy: int = 70   # g (12%, maximum)
    cil_tuky: int = 129       # g (56%, minimum 30g, maximum 183g)
    cil_vlaknina: int = 30    # g (optimum pro trávení tuků: 14g/1000kcal, minimum 20g)
    cil_cukry: int = 10       # g (maximum)
    
    # Aktivita a lifestyle
    uroven_aktivity: str = "sedava"  # Mostly sedentary
    
    # Počet jídel denně
    pocet_jidel: int = 6
    
    # Zdravotní poznámky
    zdravotni_poznamky: List[str] = None
    
    # Detailní zdravotní stav
    zdravotni_stav: Dict[str, any] = None
    
    def __post_init__(self):
        if self.zdravotni_poznamky is None:
            self.zdravotni_poznamky = [
                "Léky na krevní tlak",
                "Léčba refluxu (Omeprazol)",
                "Kardiovaskulární monitoring",
                "Prasklina chrupavky levého kolene - omezená pohyblivost",
                "Chronické bolesti beder - špatná spánková poloha",
                "Akutní bolest krční páteře (cervikální)"
            ]
        
        if self.zdravotni_stav is None:
            self.zdravotni_stav = {
                "koleno_levy": {
                    "diagnoza": "Chondrální léze (prasklina chrupavky)",
                    "omezeni": [
                        "Žádné běhání, jogging",
                        "Žádné skoky a seskoky",
                        "Žádné bruslení",
                        "Žádné lyžování",
                        "Žádné náhlé pohyby (basketbal, volejbal)"
                    ],
                    "doporucene_aktivity": [
                        "Lehací kolo (recumbent bike)",
                        "Plavání",
                        "Aqua aerobik",
                        "Nordic walking",
                        "Eliptický trenažér"
                    ],
                    "suplementace": [
                        "Kolagen 10g denně (Alavis Maxima)",
                        "Glukosamin 1500mg",
                        "Chondroitin 1200mg",
                        "Omega-3 2-3g",
                        "Vitamin D3 2000-4000 IU",
                        "Vitamin C 500-1000mg"
                    ]
                },
                "bedra": {
                    "diagnoza": "Chronická bolest bederní páteře",
                    "pricina": "Špatná spánková poloha - Kubík kopá nohy pod záda",
                    "rizika": ["Výhřez ploténky", "Svalové spasmy", "Chronická bolest"],
                    "opatreni": [
                        "Změnit uspořádání postele - Kubík pryč od zad",
                        "Tvrdší matrace s podporou bederní páteře",
                        "Ortopedický polštář pod kolena",
                        "Denní protažení 5-10 minut",
                        "Posilování core (plank, bird dog)",
                        "Fyzioterapie"
                    ]
                },
                "krcni_pater": {
                    "diagnoza": "Akutní bolest cervikální páteře",
                    "pricina": "Příliš dlouhé polohování krku v nevhodné poloze při orálním sexu",
                    "lecba": [
                        "Led/studené obklady prvních 24-48h (15 min každé 2 hodiny)",
                        "Ibuprofen 400mg (po konzultaci s lékařem)",
                        "Teplé obklady po 48 hodinách",
                        "Jemná masáž",
                        "Vyhýbat se nevhodným polohám min. týden"
                    ],
                    "prevence": [
                        "Změna techniky/poloh - méně extrémní pozice krku",
                        "Časové limity - pravidelné přestávky",
                        "Protažení před/po aktivitě",
                        "Posilování šíje - izometrické cviky"
                    ]
                },
                "obezita": {
                    "bmi": 40.1,
                    "stupen": "Obezita III. stupně (těžká)",
                    "rizika": [
                        "Kardiovaskulární onemocnění (3-4x vyšší riziko infarktu)",
                        "Diabetes mellitus 2. typu",
                        "Vysoký krevní tlak",
                        "Cévní mozková příhoda",
                        "Artróza kloubů (zvýšení tlaku na koleno)",
                        "Apnoe spánku"
                    ],
                    "cil": "Úbytek 39.2 kg (134.2 → 95.0 kg) za 12 měsíců"
                }
            }
    
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
        bmr = 10 * self.vaha + 6.25 * self.vyska - 5 * self.vek + 5
        
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
            "vlaknina_g": self.cil_vlaknina,
            "cukry_g": self.cil_cukry
        }
    
    def ziskej_rozlozeni_na_jidlo(self) -> Dict[str, float]:
        """Vypočítá průměrné makronutrienty na jedno jídlo."""
        return {
            "kalorie": round(self.cil_kalorie / self.pocet_jidel, 1),
            "bilkoviny_g": round(self.cil_bilkoviny / self.pocet_jidel, 1),
            "sacharidy_g": round(self.cil_sacharidy / self.pocet_jidel, 1),
            "tuky_g": round(self.cil_tuky / self.pocet_jidel, 1),
            "vlaknina_g": round(self.cil_vlaknina / self.pocet_jidel, 1),
            "cukry_g": round(self.cil_cukry / self.pocet_jidel, 1)
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
  Věk: {self.vek} let
  Pohlaví: {self.pohlavi}
  BMI: {bmi}
  Procento tuku: {self.procento_tuku}%
  Tuková hmota: {self.tuková_hmota} kg
  Svalová hmota: {self.svalová_hmota} kg
  Ideální váha (BMI 25): {idealni_vaha} kg
  Úroveň aktivity: {self.uroven_aktivity}
  
Metabolismus:
  Bazální metabolismus: {self.bazalni_metabolismus} kcal
  
Denní cíle (udržitelná keto/low-carb dieta):
  Kalorie: {self.cil_kalorie} kcal ({self.pocet_jidel} jídel)
  Bílkoviny: {self.cil_bilkoviny}g (32%, range: 93-154g)
  Sacharidy: max {self.cil_sacharidy}g (12%)
  Tuky: {self.cil_tuky}g (56%, range: 30-183g)
  Vláknina: {self.cil_vlaknina}g optimum (min 20g, ideální pro trávení tuků)
  Cukry: max {self.cil_cukry}g
  
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
