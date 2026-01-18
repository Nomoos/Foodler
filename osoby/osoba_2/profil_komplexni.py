#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Komplexní profil Páji - slouží pro doporučovací systém

Na základě dotazníkových odpovědí a summary profilu.
Tento soubor obsahuje všechny relevantní informace pro generování
personalizovaných jídelníčků a doporučení.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class EnergieLvl(Enum):
    """Úroveň energie během dne."""
    NIZKA = "nízká"
    STREDNI = "střední"
    VYSOKA = "vysoká"


class StresLvl(Enum):
    """Úroveň stresu."""
    NIZKY = "nízký"
    STREDNI = "střední"
    VYSOKY = "vysoký"
    CHRONICKY_VYSOKY = "chronicky vysoký"


@dataclass
class DenniRezim:
    """Denní režim a časové uspořádání."""
    
    # Časy
    cas_vstani: str = "5:30–6:00"
    cas_konce_prace: str = "16:00"
    cas_vecere: str = "18:00"
    
    # Pracovní režim
    prace_dnu_tydne: str = "5–6 dní týdně"
    
    # Časové tlaky
    rano_casovy_tlak: bool = True  # Dojíždění + školka
    
    # Klíčová poznámka
    poznamka: str = "Ráno rozhoduje o celém dni"
    
    def get_kriticke_okno(self) -> str:
        """Vrátí kritické časové okno pro hlad."""
        return "15:00–16:00"
    
    def get_pozadavky_jidelnicku(self) -> List[str]:
        """Vrátí klíčové požadavky na jídelníček."""
        return [
            "fungovat bez přemýšlení",
            "být připravený dopředu",
            "tolerovat chaos rána"
        ]


@dataclass
class EnergieAStres:
    """Energie a stresové faktory."""
    
    # Energie
    energie_cely_den: EnergieLvl = EnergieLvl.STREDNI
    zadne_extremy: bool = True
    
    # Stres
    uroven_stresu: StresLvl = StresLvl.CHRONICKY_VYSOKY
    
    # Hormonální vlivy
    pms_zvyseny_hlad: bool = True
    kolisani_nalad: bool = True
    unava_po_jidle: bool = True
    horsi_koncentrace: bool = True
    
    def get_pozadavky_na_jidlo(self) -> List[str]:
        """Co jídlo nesmí dělat."""
        return [
            "zvyšovat stres (hlad / těžkost)",
            "způsobovat glykemické výkyvy",
            "být 'všechno nebo nic'"
        ]


@dataclass
class HladAChute:
    """Vzorce hladu, chutí a přejídání."""
    
    # Hlad
    nejvyssi_hlad: str = "ráno"
    kriticke_okno: str = "15:00–16:00"
    
    # Přejídání
    prejedeni_bez_hladu: bool = True
    
    # Averze
    averze: List[str] = field(default_factory=lambda: [
        "těžkost",
        "plnost",
        "mastná jídla"
    ])
    
    def get_hlavni_problem(self) -> Dict[str, str]:
        """Identifikuje hlavní problém (ne kalorie!)."""
        return {
            "problem": "Ne množství kcal, ale:",
            "faktory": ["objem", "špatné načasování", "neuspokojivé jídlo"]
        }
    
    def get_scenar_selhani(self) -> str:
        """Typický scénář selhání."""
        return "Jídlo mě neuspokojilo → kafe / automat → sladké → únava → výčitky"


@dataclass
class CoFungujeNefunguje:
    """Co funguje dlouhodobě vs. co spouští problémy."""
    
    # Funguje dlouhodobě
    funguje: List[str] = field(default_factory=lambda: [
        "kaše + ovoce + jogurt",
        "luštěniny + semínka",
        "lehká, objemová jídla"
    ])
    
    # Spouští problémy
    spousti_problemy: Dict[str, str] = field(default_factory=lambda: {
        "káva": "chutě, pád energie",
        "tučná / masná jídla": "těžkost, únava",
        "hodně sladké": "glykemické výkyvy",
        "knedlíky": "nadýmání",
        "velké porce": "přejedení, těžkost"
    })


@dataclass
class TraveniAZdravi:
    """Trávení a zdravotní poznámky."""
    
    # Trávicí problémy
    nadymani: bool = True
    reflux: bool = True
    zacpa: bool = True
    pocit_plnosti: bool = True
    
    # Léky a suplementy
    leky: List[str] = field(default_factory=lambda: [
        "Letrox (štítná žláza)",
        "hormonální antikoncepce"
    ])
    
    suplementy: List[str] = field(default_factory=lambda: [
        "Vitamin D (nedostatečně pravidelně)",
        "Omega-3 (nedostatečně pravidelně)",
        "Magnesium (nedostatečně pravidelně)"
    ])
    
    def get_pozadavky(self) -> List[str]:
        """Co je nutné pro trávení."""
        return [
            "menší porce",
            "méně tuku",
            "pravidelnost",
            "hlídat kombinace (káva × kaše)"
        ]


@dataclass
class RodinaAZazemi:
    """Rodinné zázemí a podpora."""
    
    # Vaření
    kdo_vari: str = "převážně Roman"
    vari_jako_bonus: bool = True
    
    # Jídlo
    ji_stejne_jako_rodina: bool = True
    
    # Vybavení
    velka_lednice: bool = True
    dost_krabiček: bool = True
    meal_prep_zvladnutelny: bool = True
    
    # Dítě (Kubík)
    dite_oblibuje: List[str] = field(default_factory=lambda: [
        "sýr",
        "mrkev",
        "fíky"
    ])
    kompatibilita: str = "snadná"


@dataclass
class Motivace:
    """Motivační faktory a rizika."""
    
    # Co funguje
    funguje: List[str] = field(default_factory=lambda: [
        "výsledky na váze",
        "pocit lehkosti",
        "podpora partnera"
    ])
    
    # Co nezvládá
    nezvlada: List[str] = field(default_factory=lambda: [
        "přísná pravidla",
        "hlad",
        "pocit selhání"
    ])
    
    # Hlavní poznámka
    potrebuje: str = "rámec, ne disciplínu"


@dataclass
class HlavniRizika:
    """Hlavní rizika nedodržování režimu."""
    
    rizika: List[str] = field(default_factory=lambda: [
        "Ráno bez jasné snídaně",
        "Oběd s příliš velkým objemem",
        "Okno 15–16 h bez 'plánu B'",
        "Káva jako berlička",
        "Sociální situace (práce, oslavy, TV večer)"
    ])
    
    def get_kriticke_body(self) -> List[str]:
        """Vrátí kritické body pro monitoring."""
        return [
            "Ranní snídaně (do 7:00)",
            "Velikost oběda (kontrola objemu)",
            "Odpolední svačina (15:00-16:00)",
            "Večerní káva (vyhnout se)",
            "Sociální události (naplánovat předem)"
        ]


@dataclass
class KomplexniProfilPaji:
    """
    Komplexní profil Páji pro doporučovací systém.
    
    Kombinuje všechny aspekty života relevantní pro jídelníček:
    - Denní režim a časové omezení
    - Energie a stres
    - Hlad a chutě
    - Co funguje/nefunguje
    - Trávení a zdraví
    - Rodina a zázemí
    - Motivace
    - Rizika
    """
    
    # Základní info
    jmeno: str = "Pája (Pavla)"
    
    # Komponenty profilu
    denni_rezim: DenniRezim = field(default_factory=DenniRezim)
    energie_stres: EnergieAStres = field(default_factory=EnergieAStres)
    hlad_chute: HladAChute = field(default_factory=HladAChute)
    co_funguje: CoFungujeNefunguje = field(default_factory=CoFungujeNefunguje)
    traveni: TraveniAZdravi = field(default_factory=TraveniAZdravi)
    rodina: RodinaAZazemi = field(default_factory=RodinaAZazemi)
    motivace: Motivace = field(default_factory=Motivace)
    rizika: HlavniRizika = field(default_factory=HlavniRizika)
    
    def get_denni_pozadavky(self) -> Dict[str, List[str]]:
        """
        Vrátí kompletní denní požadavky pro jídelníček.
        """
        return {
            "jidelnicek_musi": self.denni_rezim.get_pozadavky_jidelnicku(),
            "jidlo_nesmi": self.energie_stres.get_pozadavky_na_jidlo(),
            "traveni_vyzaduje": self.traveni.get_pozadavky(),
            "funguje_dlouhodobe": self.co_funguje.funguje,
            "vyhybat_se": list(self.co_funguje.spousti_problemy.keys())
        }
    
    def get_kriticke_casy(self) -> Dict[str, str]:
        """Vrátí kritické časy během dne."""
        return {
            "rano": self.denni_rezim.cas_vstani,
            "kriticke_okno_hladu": self.hlad_chute.kriticke_okno,
            "konec_prace": self.denni_rezim.cas_konce_prace,
            "vecere": self.denni_rezim.cas_vecere
        }
    
    def get_doporuceni_pro_planovani(self) -> Dict[str, any]:
        """
        Generuje klíčová doporučení pro plánování jídelníčku.
        """
        return {
            "priorita_1_rano": {
                "duvod": "Nejvyšší hlad ráno",
                "akce": "Vydatnější snídaně, připravená dopředu",
                "priklad": self.co_funguje.funguje[0]  # kaše + ovoce + jogurt
            },
            "priorita_2_kriticke_okno": {
                "duvod": f"Kritické okno {self.hlad_chute.kriticke_okno}",
                "akce": "Mít připravenou svačinu, vyhnout se kávě",
                "riziko": "Bez plánu B → automat → sladké"
            },
            "priorita_3_obed": {
                "duvod": "Oběd s příliš velkým objemem",
                "akce": "Menší porce, víc vlákniny, méně tuku",
                "vyhybat_se": "masná jídla, velké porce"
            },
            "priorita_4_meal_prep": {
                "duvod": "Časový tlak ráno",
                "akce": "Meal prep o víkendu, hotová jídla v lednici",
                "podpora": "Roman vaří, velká lednice, dost krabiček"
            },
            "priorita_5_suplementy": {
                "duvod": "Nedostatečná pravidelnost",
                "akce": "Nastavit denní rutinu (ráno s první vodou)",
                "potreba": self.traveni.suplementy
            }
        }
    
    def __str__(self) -> str:
        """Lidsky čitelný výpis profilu."""
        return f"""
{'=' * 70}
KOMPLEXNÍ PROFIL: {self.jmeno}
{'=' * 70}

⏰ DENNÍ REŽIM
  Vstávání: {self.denni_rezim.cas_vstani}
  Práce: {self.denni_rezim.prace_dnu_tydne}, konec {self.denni_rezim.cas_konce_prace}
  Večeře: {self.denni_rezim.cas_vecere}
  ⚠️  {self.denni_rezim.poznamka}
  
🔋 ENERGIE & STRES
  Energie: {self.energie_stres.energie_cely_den.value}
  Stres: {self.energie_stres.uroven_stresu.value}
  PMS: {'Ano' if self.energie_stres.pms_zvyseny_hlad else 'Ne'} - zvýšený hlad
  Únava po jídle: {'Ano' if self.energie_stres.unava_po_jidle else 'Ne'}
  
🍽️ HLAD & CHUTĚ
  Nejvyšší hlad: {self.hlad_chute.nejvyssi_hlad}
  Kritické okno: {self.hlad_chute.kriticke_okno}
  Přejídání bez hladu: {'Ano' if self.hlad_chute.prejedeni_bez_hladu else 'Ne'}
  
  ⚠️  Typický scénář selhání:
     {self.hlad_chute.get_scenar_selhani()}
  
✅ CO FUNGUJE
  {chr(10).join(f'  • {item}' for item in self.co_funguje.funguje)}
  
❌ CO SPOUŠTÍ PROBLÉMY
  {chr(10).join(f'  • {k}: {v}' for k, v in self.co_funguje.spousti_problemy.items())}
  
🩺 TRÁVENÍ & ZDRAVÍ
  Problémy: {'nadýmání, ' if self.traveni.nadymani else ''}{'reflux, ' if self.traveni.reflux else ''}{'zácpa' if self.traveni.zacpa else ''}
  Léky: {', '.join(self.traveni.leky)}
  Suplementy: {len(self.traveni.suplementy)} položek
  
👨‍👩‍👦 RODINA & ZÁZEMÍ
  Vaří: {self.rodina.kdo_vari}
  Meal prep: {'Zvládnutelný' if self.rodina.meal_prep_zvladnutelny else 'Náročný'}
  Vybavení: {'✅ Velká lednice, dost krabiček' if self.rodina.velka_lednice else ''}
  
🎯 MOTIVACE
  Funguje: {', '.join(self.motivace.funguje)}
  Nezvládá: {', '.join(self.motivace.nezvlada)}
  💡 Potřebuje: {self.motivace.potrebuje}
  
🚨 HLAVNÍ RIZIKA
  {chr(10).join(f'  {i+1}. {r}' for i, r in enumerate(self.rizika.rizika))}

{'=' * 70}
"""


def main():
    """Ukázka použití komplexního profilu."""
    profil = KomplexniProfilPaji()
    
    print(profil)
    
    print("\n" + "=" * 70)
    print("KLÍČOVÁ DOPORUČENÍ PRO PLÁNOVÁNÍ")
    print("=" * 70)
    
    doporuceni = profil.get_doporuceni_pro_planovani()
    
    for klic, hodnota in doporuceni.items():
        print(f"\n{klic.upper().replace('_', ' ')}")
        print(f"  Důvod: {hodnota['duvod']}")
        print(f"  Akce: {hodnota['akce']}")
        if 'priklad' in hodnota:
            print(f"  Příklad: {hodnota['priklad']}")
        if 'riziko' in hodnota:
            print(f"  ⚠️  Riziko: {hodnota['riziko']}")
        if 'vyhybat_se' in hodnota:
            print(f"  ❌ Vyhýbat se: {hodnota['vyhybat_se']}")
        if 'podpora' in hodnota:
            print(f"  ✅ Podpora: {hodnota['podpora']}")
        if 'potreba' in hodnota:
            print(f"  📋 Potřeba: {', '.join(hodnota['potreba'][:2])}")
    
    print("\n" + "=" * 70)
    print("KRITICKÉ ČASY")
    print("=" * 70)
    
    casy = profil.get_kriticke_casy()
    for nazev, cas in casy.items():
        print(f"  • {nazev}: {cas}")


if __name__ == "__main__":
    main()
