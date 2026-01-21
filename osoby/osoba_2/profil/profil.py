#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profil osoby 2 - Pája (Pavla)
Obsahuje osobní údaje a cíle pro hubnutí

Pro vysvětlení metrik tělesného složení (PBF, SSM, VFA, atd.)
viz: docs/health/METRIKY_DEXA_BIA.md
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class OsobniProfil:
    """
    Osobní profil s antropometrickými daty a dietními cíli.
    
    Metriky tělesného složení (PBF, SSM, VFA):
    - PBF = Percent Body Fat (procento tuku)
    - SSM = Skeletal Muscle Mass (svalová hmota)
    - VFA = Visceral Fat Area (viscerální tuk)
    - Měřeno pomocí BIA (Bioelektrická impedanční analýza) - chytrá váha
    - Pro podrobné vysvětlení všech metrik viz: docs/health/METRIKY_DEXA_BIA.md
    """
    
    jmeno: str = "Pája (Pavla)"
    vaha: float = 77.3  # kg (měření 22.12.2025)
    vyska: int = 169  # cm
    pohlavi: str = "žena"
    procento_tuku: float = 39.6  # % (měření 22.12.2025)
    tuková_hmota: float = 30.6  # kg (měření 22.12.2025)
    svalová_hmota: float = 25.6  # kg (SSM, měření 22.12.2025)
    vfa: float = 147.2  # cm2/level (viscerální tuk, měření 22.12.2025)
    
    # Dietní cíle (denní příjem) - vypočteno Ankerl Keto Calculator
    cil_kalorie: int = 1508  # kcal (10% deficit, Ankerl)
    cil_bilkoviny: int = 92  # g (minimum 80g, max 100g, Ankerl)
    cil_sacharidy: int = 60   # g (maximum, Ankerl)
    cil_tuky: int = 100       # g (60-120g rozmezí, Ankerl)
    cil_vlaknina: int = 20    # g (minimum, ideálně více)
    
    # Počet jídel denně
    pocet_jidel: int = 5
    
    # Zdravotní poznámky
    zdravotni_poznamky: List[str] = None
    
    # Zdravotní stav - psychické a hormonální problémy
    zdravotni_stav: Dict = None
    
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
        
        if self.zdravotni_stav is None:
            self.zdravotni_stav = {
                "psychicke_zdravi": {
                    "diagnoza": "Středně těžká deprese s možným PMDD",
                    "symptomy": [
                        "Víkendová deprese - neschopnost vstát z postele",
                        "Pocity bezcennosti ('jsem k ničemu')",
                        "Fungování závislé na vnější struktuře (práce)",
                        "Extrémní agresivita cca týden před menstruací"
                    ],
                    "lecba": {
                        "aktualni_stav": "V léčbě od ledna 2026",
                        "terapie": "Psychoterapie 1x týdně (probíhá)",
                        "medikace": "Čeká na nové léky od psychiatra (leden 2026)",
                        "predchozi_medikace": "Antipsychotika + regulátor nálady (nefungovaly dobře - 'fungovala' ale nebylo jí dobře)",
                        "poznamka": "Důležité zmínit psychiatrovi možné PMDD (ne jen PMS)"
                    },
                    "pmdd_vysvetleni": {
                        "nazev": "PMDD = Premenstrual Dysphoric Disorder (Premenstruační dysforická porucha)",
                        "co_to_je": "Těžká forma PMS - vážná hormonální porucha způsobující extrémní psychické symptomy",
                        "rozdil_od_pms": {
                            "PMS": "Mírné až střední nálady, únava, bolest - běžné, 75% žen",
                            "PMDD": "Extrémní agresivita, deprese, úzkost, sebepoškozující myšlenky - vzácné, 3-8% žen"
                        },
                        "hlavni_symptomy": [
                            "Extrémní agresivita/vzteklost (ne jen podrážděnost)",
                            "Hluboká deprese týden před menstruací",
                            "Úzkost, panické ataky",
                            "Naprostá neschopnost fungovat",
                            "Symptomy mizí 1-2 dny po začátku menstruace"
                        ],
                        "paja_symptomy": [
                            "✅ Extrémní agresivita týden před periodou (match s PMDD)",
                            "✅ Problémy s fungováním o víkendech (může být horší před menstruací)",
                            "❓ Sledovat zda deprese/neschopnost vstát koreluje s cyklem"
                        ],
                        "lecba_pmdd": [
                            "SSRI antidepresiva (nejúčinnější - Prozac, Zoloft)",
                            "Hormonální antikoncepce (stabilizace hormonů)",
                            "Vitamin B6 1000mg denně",
                            "Evening primrose oil (pupalkový olej)",
                            "Hořčík 400-800mg denně",
                            "Sledování menstruačního cyklu (aplikace)"
                        ],
                        "proc_je_dulezite": [
                            "PMDD vyžaduje JINOU léčbu než běžná deprese",
                            "Antidepresiva (SSRI) jsou extrémně účinná pro PMDD",
                            "Někdy stačí brát SSRI jen 14 dní před menstruací",
                            "Neléčené PMDD může vést k sebevraždě (vážné!)"
                        ],
                        "akce": "Zmínit psychiatrovi podezření na PMDD + sledovat korelaci symptomů s cyklem"
                    }
                },
                "hormonalni_problemy": {
                    "snizene_libido": {
                        "popis": "Výrazně snížené libido - pravděpodobně hormonální nerovnováha",
                        "mozne_priciny": [
                            "Nízký testosteron (ano i u žen!)",
                            "Nedostatek oxytocinu (málo intimity)",
                            "Nízký serotonin (deprese)",
                            "Nedostatek vitaminu D",
                            "Nedostatek pohybu (žádné endorfiny)"
                        ],
                        "aktualni_frekvence_sexu": "1x za 3 týdny (extrémně málo pro zdraví)",
                        "zdrava_frekvence": "2-3x týdně (ideální pro hormonální rovnováhu)",
                        "plan_zlepseni": {
                            "faze_1": "Týdny 1-2: 1x týdně (využít čas 21-22h)",
                            "faze_2": "Týdny 3-4: 2x za 2 týdny",
                            "faze_3": "Měsíce 2-3: 2x týdně",
                            "dlouhodobe": "2-3x týdně standardně",
                            "poznamka": "ŽÁDNÝ TLAK - kvalita > kvantita, i mazlení/objímání pomáhá"
                        }
                    },
                    "emocionalni_prejedani": {
                        "popis": "Používá jídlo jako náhradu za emocionální naplnění",
                        "souvislost": "Nedostatek intimity → jídlo jako kompenzace",
                        "reseni": "Zvýšení intimity + pravidelný pohyb → menší potřeba kompenzovat jídlem"
                    }
                },
                "nedostatek_pohybu": {
                    "aktualni_stav": "Sedavý životní styl, minimální pohyb",
                    "dusledky": [
                        "Žádné endorfiny (přirozené antidepresivum)",
                        "Nízká energie",
                        "Horší nálada",
                        "Zhoršená hormonální rovnováha"
                    ],
                    "doporuceny_plan": {
                        "pondeli": "Volno/odpočinek",
                        "utery": "Plavání 45 min",
                        "streda": "Chůze 30 min",
                        "ctvrtek": "Jóga/strečink 30 min",
                        "patek": "Plavání 45 min",
                        "sobota": "Chůze/procházka 45 min",
                        "nedele": "Volno/lehká aktivita",
                        "poznamka": "Plus intimita 2-3x týdně (pohybová aktivita!)"
                    }
                },
                "suplementace_urgentni": {
                    "vitamin_d3": {
                        "davka": "5000 IU denně",
                        "proc": "Kritické pro zimní depresi, pravděpodobně má nedostatek",
                        "efekt": "2-4 týdny na zlepšení nálady",
                        "cena": "~200 Kč/měsíc"
                    },
                    "omega_3": {
                        "davka": "2-3g EPA+DHA denně",
                        "proc": "Prokázaný antidepresivní efekt, doplňuje léky",
                        "efekt": "2-4 týdny na zlepšení nálady",
                        "cena": "~300-400 Kč/měsíc"
                    },
                    "horcik": {
                        "davka": "400mg večer (citrate nebo glycinate)",
                        "proc": "Úzkost, lepší spánek, PMS/PMDD",
                        "efekt": "1-2 týdny",
                        "cena": "~150 Kč/měsíc"
                    },
                    "pro_pmdd_extra": {
                        "vitamin_b6": "100mg denně (až 1000mg pro PMDD)",
                        "evening_primrose_oil": "1000-1500mg denně",
                        "poznamka": "Zmínit psychiatrovi pro PMDD léčbu"
                    }
                },
                "vikendova_rutina": {
                    "problem": "O víkendu není schopná vstát z postele",
                    "reseni": {
                        "pevny_cas_vstavani": "8:00 i o víkendu (bez výjimky!)",
                        "ihned_po_vstavani": [
                            "Okno otevřít - světlo (30 sec)",
                            "Studená sprcha nebo omytí obličeje (aktivace)",
                            "Pohyb ven 10-15 min (i jen na balkon)",
                            "Snídaně s bílkovinami"
                        ],
                        "poznamka": "První 2 týdny bude těžké, pak se tělo přizpůsobí"
                    }
                },
                "spolecny_cas_v_posteli": {
                    "aktualni": "21-22h společně v posteli (výborný základ!)",
                    "vyuziti": "Ideální čas pro intimitu, povídání, mazlení",
                    "poznamka": "Využít tento už nastavený čas pro budování intimity"
                },
                "timeline_zlepseni": {
                    "2_4_tydny": "Nové léky začnou působit + D3/Omega-3 efekty, mírnější deprese, intimita 1x týdně",
                    "1_2_mesice": "Výrazně lepší nálada, zvládnutelné víkendy, mírnější PMS/PMDD, intimita 2x za 2 týdny",
                    "3_mesice": "Stabilní nálada většinu času, žádná víkendová deprese, kontrolované PMS/PMDD, intimita 2x týdně",
                    "6_mesicu": "Deprese vyřešená/kontrolovaná, optimální hormonální rovnováha, zdravý intimní vztah (2-3x týdně), možná diskuse o snížení léků (POUZE s psychiatrem!)"
                },
                "cile_hubnutia": {
                    "aktualni_vaha": "77.3 kg",
                    "cilova_vaha": "57 kg (BMI 22, ideální)",
                    "ubytek_potrebny": "20.3 kg",
                    "souvislost_s_psychikou": "Hubnutí pomůže s náladou (lepší hormony, více energie), ale psychika musí být stabilní NEJDŘÍV"
                }
            }
    
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
