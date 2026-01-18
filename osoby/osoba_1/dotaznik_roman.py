#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dotazník pro Romana - Příprava jídel a nákup potravin

Tento dotazník se zaměřuje na:
- Týdenní přípravu jídel (meal prep 1x za týden)
- Optimalizaci nákupů potravin
- Efektivitu v kuchyni
- Praktické strategie pro hubnutí
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import time
import json


@dataclass
class ZivotniStyl:
    """Otázky týkající se životního stylu a denní rutiny."""
    
    # Pracovní režim
    pracovni_tyden_dnu: int = 5  # Kolik dní v týdnu pracuje?
    pracovni_doba_zacatek: Optional[time] = None  # Kdy začíná práce?
    pracovni_doba_konec: Optional[time] = None  # Kdy končí práce?
    prace_z_domu: bool = False  # Pracuje z domu?
    
    # Spánek a energie
    cas_buzeni: Optional[time] = None  # Kdy obvykle vstává?
    cas_spanku: Optional[time] = None  # Kdy obvykle jde spát?
    kvalita_spanku: str = "dobra"  # "vyborná", "dobra", "stredni", "spatna"
    
    # Energetické hladiny během dne
    energie_rano: str = "stredni"  # "vysoka", "stredni", "nizka"
    energie_poledne: str = "stredni"
    energie_vecer: str = "stredni"
    
    # Kdy pociťuje největší hlad?
    nejvetsi_hlad: str = "vecer"  # "rano", "dopoledne", "obed", "odpoledne", "vecer", "noc"
    
    # Stres a problémy
    uroven_stresu: str = "stredni"  # "nizka", "stredni", "vysoka"
    problemy_s_travenim: List[str] = field(default_factory=list)  # např. "nadýmání", "pálení žáhy", "zácpa"


@dataclass
class MealPrepPreference:
    """Preference pro týdenní přípravu jídel."""
    
    # Kolik času má na meal prep?
    cas_na_meal_prep_tyden: int = 180  # minuty týdně (3 hodiny)
    
    # Kdy má nejvíce času na velký meal prep?
    nejlepsi_den_pro_meal_prep: str = "nedele"  # "sobota", "nedele", "jiny"
    nejlepsi_cas_pro_meal_prep: str = "odpoledne"  # "rano", "dopoledne", "odpoledne", "vecer"
    
    # Na kolik dní dopředu chce připravovat?
    priprava_na_dni: int = 7  # Připravit na celý týden (7 dní)
    
    # Denní čas na vaření (pro doplňování)
    cas_na_vareni_vsedni_den: int = 30  # minuty denně
    
    # Preference skladování
    preferuje_vakuovani: bool = True
    preferuje_mrazeni: bool = True
    preferuje_lednici: bool = True
    
    # Jaká jídla je ochoten připravovat dopředu?
    ochota_pripravit_dopredu: List[str] = field(default_factory=lambda: [
        "hlavní jídla",
        "saláty",
        "snídaně",
        "svačiny"
    ])
    
    # Kolik různých jídel chce mít připravených?
    pocet_ruznych_jidel: int = 4  # 4 různá jídla v rotaci


@dataclass
class NakupniPreference:
    """Preference pro nákup potravin."""
    
    # Rozpočet
    tydenni_rozpocet_rodina: Optional[float] = None  # Kč/týden pro celou rodinu
    tydenni_rozpocet_osoba: Optional[float] = None  # Kč/týden/osobu
    
    # Nákupní návyky
    kde_nakupuje_nejcasteji: List[str] = field(default_factory=list)  # např. ["Lidl", "Kaufland"]
    jak_casto_nakupuje: str = "1x_tyden"  # "denne", "2x_tyden", "1x_tyden"
    preferovany_den_nakupu: str = "sobota"  # "pondeli", "sobota", "nedele", ...
    
    # Využívání slev
    sleduje_slevy: bool = True
    ochotny_nakupovat_ve_vice_obchodech: bool = True  # Kvůli slevám
    
    # Plánování nákupu
    dela_nakupni_seznam: bool = True
    planuje_nakup_podle_jidelnicku: bool = True
    
    # Preference kvalita vs cena
    preferuje_kvalitu_nad_cenou: bool = False  # Cena je důležitá
    ochotny_nakupovat_levnejsi_kusy_masa: bool = True  # Např. kuřecí stehna místo prsou
    
    # Zásoby
    nakupuje_do_zasoby: bool = True  # Např. mražené maso, konzervy


@dataclass
class VareniAKuchyne:
    """Dovednosti a vybavení v kuchyni."""
    
    # Vaření
    jak_rad_vari: str = "rad"  # "velmi_rad", "rad", "neutralne", "nerad"
    uroven_vareni: str = "pokrocily"  # "zacatecnik", "stredni", "pokrocily", "expert"
    
    # Kuchyňské vybavení
    ma_kuchynske_vybaveni: List[str] = field(default_factory=list)
    # např. ["tlakový hrnec", "airfryer", "trouba", "multicooker", "vakuovačka", "mixér"]
    
    # Preference metod přípravy
    oblibene_metody_pripravy: List[str] = field(default_factory=list)
    # např. ["pečení na plechu", "tlakový hrnec", "airfryer", "grilování"]
    
    # Časová efektivita
    preferuje_batch_cooking: bool = True  # Připravit hodně najednou
    ochoten_pripravovat_slozitejsi: bool = False  # Preferuje jednoduché
    
    # Skladování
    velikost_lednice: str = "stredni"  # "mala", "stredni", "velka"
    ma_mrazak: bool = True
    ma_vakuovacku: bool = True
    ma_meal_prep_krabicky: int = 20  # Počet krabiček


@dataclass
class JidelniPreference:
    """Jídelní preference a oblíbená jídla."""
    
    # TOP oblíbená jídla (která rád vaří a jí)
    top_oblibena_jidla: List[str] = field(default_factory=list)
    
    # Jídla vhodná pro meal prep
    jidla_vhodna_pro_meal_prep: List[str] = field(default_factory=list)
    
    # Jídla, ze kterých je unavený
    unavena_z_jidel: List[str] = field(default_factory=list)
    
    # Preference teploty
    preferuje_tepla_jidla: bool = True
    ochota_jist_studene_meal_prep: bool = True  # Např. studené kuřecí prsa
    
    # Preference typu jídel
    preferuje_jednoduche_recepty: bool = True
    oblibuje_jednohrnce: bool = True  # One-pot meals
    
    # Protein preference
    oblibene_zdroje_bilkovin: List[str] = field(default_factory=list)
    # např. ["kuřecí prsa", "krůtí maso", "vejce", "tvaroh", "losos"]
    
    # Zelenina
    oblibena_zelenina: List[str] = field(default_factory=list)
    
    # Ochota experimentovat
    ochota_zkouset_nove: str = "stredni"  # "vysoka", "stredni", "nizka"


@dataclass
class ZdravotniCile:
    """Zdravotní cíle a specifické potřeby."""
    
    # Hlavní cíle
    hlavni_cile: List[str] = field(default_factory=lambda: ["úbytek váhy", "více energie"])
    
    # Konkrétní váhové cíle
    aktualni_vaha: float = 134.2  # kg (měření 9.1.2026)
    cilova_vaha_1_mesic: Optional[float] = None
    cilova_vaha_3_mesice: Optional[float] = None
    cilova_vaha_6_mesicu: Optional[float] = None
    cilova_vaha_konecna: Optional[float] = None  # Dlouhodobý cíl
    
    # Problémové oblasti
    problemove_oblasti: List[str] = field(default_factory=lambda: ["břicho", "boky"])
    
    # Zdravotní problémy
    zdravotni_problemy: List[str] = field(default_factory=list)
    # např. ["pálení žáhy", "GERD", "únava po jídle"]
    
    # Suplementy
    uzivane_suplementy: List[str] = field(default_factory=list)
    
    # Priorita bílkovin
    priorita_bilkoviny: bool = True  # Protein-first approach
    denni_cil_bilkoviny: int = 140  # gramy (32%)
    denni_cil_kalorie: int = 2000  # kcal
    denni_limit_sacharidy: int = 70  # gramy (12%)
    denni_cil_tuky: int = 129  # gramy (56%)
    denni_cil_vlaknina: int = 50  # gramy
    denni_limit_cukry: int = 10  # gramy
    
    # Metabolismus
    bazalni_metabolismus: int = 2300  # kcal


@dataclass
class RodinaASpolecneStravovani:
    """Rodinné stravování a spolupráce."""
    
    # Vaření pro rodinu
    vari_pro_celu_rodinu: bool = True
    jak_casto_vari_pro_rodinu: str = "denne"  # "denne", "vikendy", "obcas"
    
    # Sdílená jídla
    rodina_sdili_stejne_jidlo: bool = False  # Každý má jiné potřeby
    kdo_sdili_jidlo_s_romanem: List[str] = field(default_factory=list)  # např. ["Pája částečně"]
    
    # Spolupráce s partnerkou
    partner_pomaha_s_varenim: bool = True
    partner_pomaha_s_nakupem: bool = True
    deli_se_o_meal_prep: bool = True
    
    # Kubík
    vari_zvlast_pro_kubika: bool = True
    kubik_ma_odlisne_jidelnicek: bool = True


@dataclass
class DotaznikRoman:
    """Kompletní dotazník pro Romana."""
    
    zivotni_styl: ZivotniStyl
    meal_prep_preference: MealPrepPreference
    nakupni_preference: NakupniPreference
    vareni_a_kuchyne: VareniAKuchyne
    jidelni_preference: JidelniPreference
    zdravotni_cile: ZdravotniCile
    rodina_spolecne_stravovani: RodinaASpolecneStravovani
    
    # Volné poznámky
    dalsi_poznamky: str = ""
    
    def to_dict(self) -> Dict:
        """Převede dotazník na slovník."""
        return {
            "zivotni_styl": self.zivotni_styl.__dict__,
            "meal_prep_preference": self.meal_prep_preference.__dict__,
            "nakupni_preference": self.nakupni_preference.__dict__,
            "vareni_a_kuchyne": self.vareni_a_kuchyne.__dict__,
            "jidelni_preference": self.jidelni_preference.__dict__,
            "zdravotni_cile": self.zdravotni_cile.__dict__,
            "rodina_spolecne_stravovani": self.rodina_spolecne_stravovani.__dict__,
            "dalsi_poznamky": self.dalsi_poznamky
        }
    
    def uloz_do_souboru(self, cesta: str = "dotaznik_roman_odpovedi.json"):
        """Uloží odpovědi do JSON souboru."""
        with open(cesta, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2, default=str)
    
    def ziskej_doporuceni(self) -> List[str]:
        """
        Na základě odpovědí vygeneruje doporučení pro meal prep a nákupy.
        
        Returns:
            Seznam konkrétních doporučení
        """
        doporuceni = []
        
        # === MEAL PREP DOPORUČENÍ ===
        if self.meal_prep_preference.priprava_na_dni >= 7:
            doporuceni.append(
                f"📅 Týdenní meal prep: Plánuj přípravu na {self.meal_prep_preference.nejlepsi_den_pro_meal_prep} "
                f"{self.meal_prep_preference.nejlepsi_cas_pro_meal_prep}. "
                f"Připrav {self.meal_prep_preference.pocet_ruznych_jidel} různá jídla v dávkách pro celý týden."
            )
        
        if self.meal_prep_preference.cas_na_meal_prep_tyden >= 120:
            doporuceni.append(
                f"⏱️ Časový plán: Máš {self.meal_prep_preference.cas_na_meal_prep_tyden} minut týdně. "
                "Doporučení: 2 hodiny hlavní meal prep + 1 hodina příprava snídaní a svačin."
            )
        
        if self.vareni_a_kuchyne.preferuje_batch_cooking:
            doporuceni.append(
                "🍳 Batch cooking: Využij trouba na pečení více plechů najednou "
                "(2-3 kg kuřecích prsou, zelenina). Tlakový hrnec na rychlou přípravu masa."
            )
        
        # === NÁKUPNÍ DOPORUČENÍ ===
        if self.nakupni_preference.sleduje_slevy:
            doporuceni.append(
                "💰 Slevy: Každý týden kontroluj Kupi.cz pro slevy na kuřecí maso, vejce, tvaroh, zeleninu. "
                "Nakupuj ve více obchodech pro maximální úspory."
            )
        
        if self.nakupni_preference.planuje_nakup_podle_jidelnicku:
            doporuceni.append(
                "📝 Nákupní seznam: Vytvoř týdenní jídelníček nejprve, pak sestav přesný nákupní seznam. "
                "Nákup v sobotu, meal prep v neděli."
            )
        
        if self.nakupni_preference.tydenni_rozpocet_rodina:
            rozpocet_osoba = self.nakupni_preference.tydenni_rozpocet_rodina / 3  # 3 osoby
            doporuceni.append(
                f"💵 Rozpočet: {self.nakupni_preference.tydenni_rozpocet_rodina:.0f} Kč/týden pro rodinu "
                f"({rozpocet_osoba:.0f} Kč/osoba). Zaměř se na cenově výhodné proteiny: "
                "vejce (3-4 Kč/kus), kuřecí stehna (80-100 Kč/kg), tvaroh (25-30 Kč/250g)."
            )
        
        # === JÍDELNÍ DOPORUČENÍ ===
        if self.zdravotni_cile.priorita_bilkoviny:
            doporuceni.append(
                f"🥩 Protein first: Tvůj denní cíl je {self.zdravotni_cile.denni_cil_bilkoviny}g bílkovin (32% z {self.zdravotni_cile.denni_cil_kalorie} kcal). "
                "Připravuj ve velkém: 2kg kuřecích prsou = 14 porcí po 140g (35g proteinu). "
                "Doplň vejci (6g protein/kus), tvarohem (18g/100g). "
                f"Rozložení: 6x 370 kcal + 1x 158 kcal (celkem 6 jídel denně)."
            )
        
        if self.jidelni_preference.preferuje_jednoduche_recepty:
            doporuceni.append(
                "📖 Jednoduché recepty pro meal prep:\n"
                "   • Pečená kuřecí prsa + brokolice + olivový olej (3 ingredience)\n"
                "   • Mleté maso + cuketa + rajčatová omáčka (3 ingredience)\n"
                "   • Losos + špenát + česnek (3 ingredience)\n"
                "   • Vejce napečené + cherry rajčata + špenát (3 ingredience)"
            )
        
        # === SKLADOVÁNÍ ===
        if self.vareni_a_kuchyne.ma_vakuovacku:
            doporuceni.append(
                "📦 Vakuování: Vakuuj hotová jídla po porcích. "
                "Mražené vydrží 2-3 měsíce, v lednici 5-7 dní. "
                "Označuj datum přípravy."
            )
        
        if self.vareni_a_kuchyne.ma_meal_prep_krabicky >= 15:
            doporuceni.append(
                f"🥡 Meal prep krabičky: Máš {self.vareni_a_kuchyne.ma_meal_prep_krabicky} krabiček. "
                "Doporučené rozdělení: 7 obědů + 7 večeří + 6 snídaní/svačin. "
                "Používej průhledné krabičky pro snadnou identifikaci."
            )
        
        # === TÝDENNÍ STRATEGIE ===
        doporuceni.append(
            "📅 Týdenní strategie:\n"
            "   Sobota: Velký nákup (1.5h), příprava seznamu\n"
            "   Neděle: Meal prep session (3h) - hlavní jídla na celý týden\n"
            "   Po-Pá: Pouze ohřívání (5-10 min) + případně rychlá zelenina\n"
            "   Středa večer: Mini refresh (30 min) - doplnit zeleninu, ohřát další porce"
        )
        
        # === OPTIMALIZACE ČASU ===
        if self.meal_prep_preference.cas_na_meal_prep_tyden >= 150:
            doporuceni.append(
                "⚡ Časová optimalizace:\n"
                "   • Troubu využij na maximum: 2 plechy najednou (maso + zelenina)\n"
                "   • Tlakový hrnec: Kuřecí prsa 15 min, vejce 5 min\n"
                "   • Během pečení: Připrav saláty, nakrájej zeleninu\n"
                "   • Airfryer: Rychlé dopečení, řízky za 12 min"
            )
        
        # === RODINA ===
        if self.rodina_spolecne_stravovani.vari_pro_celu_rodinu:
            doporuceni.append(
                "👨‍👩‍👦 Rodinné meal prep: Připravuj 3 různé verze:\n"
                "   • Roman: High-protein, low-carb (140g+ protein, <70g carbs)\n"
                "   • Pája: Medium-protein, low-carb (92g protein, <60g carbs)\n"
                "   • Kubík: Normální sacharidy (19g protein, 130g carbs)\n"
                "   Základní komponenty stejné, jen velikost porcí a přílohy jiné"
            )
        
        # === VÁHOVÉ CÍLE ===
        if self.zdravotni_cile.cilova_vaha_1_mesic:
            ubytek_1m = self.zdravotni_cile.aktualni_vaha - self.zdravotni_cile.cilova_vaha_1_mesic
            doporuceni.append(
                f"📉 Váhový cíl: Aktuálně {self.zdravotni_cile.aktualni_vaha}kg → "
                f"cíl za měsíc {self.zdravotni_cile.cilova_vaha_1_mesic}kg ({ubytek_1m:.1f}kg). "
                f"Udržuj deficit {self.zdravotni_cile.denni_cil_kalorie} kcal denně "
                f"(BMR: {self.zdravotni_cile.bazalni_metabolismus} kcal), "
                f"prioritizuj protein ({self.zdravotni_cile.denni_cil_bilkoviny}g/32%), "
                f"limituj sacharidy ({self.zdravotni_cile.denni_limit_sacharidy}g/12%), "
                f"tuky ({self.zdravotni_cile.denni_cil_tuky}g/56%)."
            )
        
        if not doporuceni:
            doporuceni.append("✅ Pokračuj v současném meal prep plánu a postupně optimalizuj.")
        
        return doporuceni


def interaktivni_dotaznik() -> DotaznikRoman:
    """
    Interaktivní dotazník - klade otázky a ukládá odpovědi.
    
    Returns:
        Vyplněný DotaznikRoman objekt
    """
    print("=" * 80)
    print("DOTAZNÍK PRO ROMANA - Příprava jídel a nákup potravin")
    print("=" * 80)
    print("\nTento dotazník se zaměřuje na týdenní meal prep a optimalizaci nákupů.")
    print("U každé otázky můžeš odpovědět nebo stisknout Enter pro přeskočení.\n")
    
    # === ŽIVOTNÍ STYL ===
    print("\n" + "=" * 80)
    print("1️⃣  ŽIVOTNÍ STYL A DENNÍ RUTINA")
    print("=" * 80)
    
    pracovni_tyden = input("\nKolik dní v týdnu pracuješ? [5]: ") or "5"
    
    cas_buzeni_str = input("V kolik hodin obvykle vstáváš? (např. 06:30): ")
    cas_buzeni = None
    if cas_buzeni_str:
        h, m = map(int, cas_buzeni_str.split(':'))
        cas_buzeni = time(h, m)
    
    cas_spanku_str = input("V kolik hodin obvykle jdeš spát? (např. 22:30): ")
    cas_spanku = None
    if cas_spanku_str:
        h, m = map(int, cas_spanku_str.split(':'))
        cas_spanku = time(h, m)
    
    print("\nKdy pociťuješ největší hlad?")
    print("(rano / dopoledne / obed / odpoledne / vecer / noc)")
    nejvetsi_hlad = input("  [vecer] ") or "vecer"
    
    zivotni_styl = ZivotniStyl(
        pracovni_tyden_dnu=int(pracovni_tyden),
        cas_buzeni=cas_buzeni,
        cas_spanku=cas_spanku,
        nejvetsi_hlad=nejvetsi_hlad
    )
    
    # === MEAL PREP ===
    print("\n" + "=" * 80)
    print("2️⃣  TÝDENNÍ MEAL PREP")
    print("=" * 80)
    
    print("\nKolik času máš na meal prep týdně? (minuty)")
    cas_meal_prep = input("  [180 minut = 3 hodiny] ") or "180"
    
    print("\nKterý den ti nejvíce vyhovuje pro meal prep?")
    print("(sobota / nedele / jiny)")
    den_meal_prep = input("  [nedele] ") or "nedele"
    
    print("\nV jakou denní dobu je pro tebe nejlepší čas na meal prep?")
    print("(rano / dopoledne / odpoledne / vecer)")
    cas_meal_prep_denni = input("  [odpoledne] ") or "odpoledne"
    
    print("\nNa kolik dní dopředu chceš připravovat?")
    priprava_dni = input("  [7 = celý týden] ") or "7"
    
    print("\nKolik různých jídel chceš mít v rotaci?")
    pocet_jidel = input("  [4 různá jídla] ") or "4"
    
    meal_prep_preference = MealPrepPreference(
        cas_na_meal_prep_tyden=int(cas_meal_prep),
        nejlepsi_den_pro_meal_prep=den_meal_prep,
        nejlepsi_cas_pro_meal_prep=cas_meal_prep_denni,
        priprava_na_dni=int(priprava_dni),
        pocet_ruznych_jidel=int(pocet_jidel)
    )
    
    # === NÁKUPY ===
    print("\n" + "=" * 80)
    print("3️⃣  NÁKUP POTRAVIN")
    print("=" * 80)
    
    rozpocet = input("\nTýdenní rozpočet na potraviny pro celou rodinu (Kč): ")
    
    print("\nKde nejčastěji nakupuješ? (každý obchod na nový řádek, Enter pro konec)")
    obchody = []
    while True:
        obchod = input("  ")
        if not obchod:
            break
        obchody.append(obchod)
    
    print("\nKterý den nejčastěji nakupuješ?")
    print("(pondeli / utery / streda / ctvrtek / patek / sobota / nedele)")
    den_nakupu = input("  [sobota] ") or "sobota"
    
    slevy = input("\nSleduješ aktivně slevy? (ano/ne): [ano] ") or "ano"
    vice_obchodu = input("Jsi ochoten nakupovat ve více obchodech kvůli slevám? (ano/ne): [ano] ") or "ano"
    
    nakupni_preference = NakupniPreference(
        tydenni_rozpocet_rodina=float(rozpocet) if rozpocet else None,
        kde_nakupuje_nejcasteji=obchody,
        preferovany_den_nakupu=den_nakupu,
        sleduje_slevy=(slevy.lower() == "ano"),
        ochotny_nakupovat_ve_vice_obchodech=(vice_obchodu.lower() == "ano")
    )
    
    # === VAŘENÍ A KUCHYNĚ ===
    print("\n" + "=" * 80)
    print("4️⃣  VAŘENÍ A KUCHYŇSKÉ VYBAVENÍ")
    print("=" * 80)
    
    print("\nJak rád vaříš?")
    print("(velmi_rad / rad / neutralne / nerad)")
    rad_vari = input("  [rad] ") or "rad"
    
    print("\nJaké kuchyňské vybavení máš? (každé na nový řádek, Enter pro konec)")
    print("(např: tlakový hrnec, airfryer, trouba, multicooker, vakuovačka, mixér)")
    vybaveni = []
    while True:
        item = input("  ")
        if not item:
            break
        vybaveni.append(item)
    
    ma_vakuovacku = input("\nMáš vakuovačku? (ano/ne): [ano] ") or "ano"
    pocet_krabicek = input("Kolik meal prep krabiček máš? [20]: ") or "20"
    
    vareni_a_kuchyne = VareniAKuchyne(
        jak_rad_vari=rad_vari,
        ma_kuchynske_vybaveni=vybaveni,
        ma_vakuovacku=(ma_vakuovacka.lower() == "ano"),
        ma_meal_prep_krabicky=int(pocet_krabicek)
    )
    
    # === JÍDELNÍ PREFERENCE ===
    print("\n" + "=" * 80)
    print("5️⃣  JÍDELNÍ PREFERENCE")
    print("=" * 80)
    
    print("\nJaká jsou tvoje TOP 5 oblíbených jídel? (každé na nový řádek)")
    oblibena_jidla = []
    for i in range(1, 6):
        jidlo = input(f"  {i}. ")
        if jidlo:
            oblibena_jidla.append(jidlo)
    
    print("\nJaká jídla jsou ideální pro meal prep? (každé na nový řádek, Enter pro konec)")
    jidla_meal_prep = []
    while True:
        jidlo = input("  ")
        if not jidlo:
            break
        jidla_meal_prep.append(jidlo)
    
    print("\nJaké jsou tvoje oblíbené zdroje bílkovin? (každý na nový řádek, Enter pro konec)")
    print("(např: kuřecí prsa, krůtí maso, vejce, tvaroh, losos, tuňák)")
    bilkoviny = []
    while True:
        protein = input("  ")
        if not protein:
            break
        bilkoviny.append(protein)
    
    jidelni_preference = JidelniPreference(
        top_oblibena_jidla=oblibena_jidla,
        jidla_vhodna_pro_meal_prep=jidla_meal_prep,
        oblibene_zdroje_bilkovin=bilkoviny
    )
    
    # === ZDRAVOTNÍ CÍLE ===
    print("\n" + "=" * 80)
    print("6️⃣  ZDRAVOTNÍ CÍLE")
    print("=" * 80)
    
    print(f"\nAktuální váha: {134.2} kg (měření 9.1.2026)")
    cilova_1m = input("Cílová váha za 1 měsíc (kg): ")
    cilova_3m = input("Cílová váha za 3 měsíce (kg): ")
    cilova_6m = input("Cílová váha za 6 měsíců (kg): ")
    cilova_konecna = input("Konečná cílová váha (kg): ")
    
    zdravotni_cile = ZdravotniCile(
        cilova_vaha_1_mesic=float(cilova_1m) if cilova_1m else None,
        cilova_vaha_3_mesice=float(cilova_3m) if cilova_3m else None,
        cilova_vaha_6_mesicu=float(cilova_6m) if cilova_6m else None,
        cilova_vaha_konecna=float(cilova_konecna) if cilova_konecna else None
    )
    
    # === RODINA ===
    print("\n" + "=" * 80)
    print("7️⃣  RODINNÉ STRAVOVÁNÍ")
    print("=" * 80)
    
    print("\nVaříš pro celou rodinu?")
    vari_rodina = input("  (ano/ne): [ano] ") or "ano"
    
    print("\nPomáhá ti partnerka s meal prepem?")
    partner_pomaha = input("  (ano/ne): [ano] ") or "ano"
    
    rodina = RodinaASpolecneStravovani(
        vari_pro_celu_rodinu=(vari_rodina.lower() == "ano"),
        partner_pomaha_s_varenim=(partner_pomaha.lower() == "ano")
    )
    
    # === POZNÁMKY ===
    print("\n" + "=" * 80)
    poznamky = input("\nDalší poznámky nebo speciální požadavky:\n")
    
    # Vytvoření dotazníku
    dotaznik = DotaznikRoman(
        zivotni_styl=zivotni_styl,
        meal_prep_preference=meal_prep_preference,
        nakupni_preference=nakupni_preference,
        vareni_a_kuchyne=vareni_a_kuchyne,
        jidelni_preference=jedelni_preference,
        zdravotni_cile=zdravotni_cile,
        rodina_spolecne_stravovani=rodina,
        dalsi_poznamky=poznamky
    )
    
    print("\n" + "=" * 80)
    print("✅ DOTAZNÍK DOKONČEN!")
    print("=" * 80)
    
    return dotaznik


def zobraz_otazky_seznam() -> None:
    """
    Zobrazí seznam všech otázek v dotazníku bez interakce.
    Užitečné pro tisk nebo sdílení.
    """
    print("=" * 80)
    print("DOTAZNÍK PRO ROMANA - Seznam otázek")
    print("=" * 80)
    
    print("\n1️⃣  ŽIVOTNÍ STYL A DENNÍ RUTINA")
    print("-" * 80)
    print("1. Kolik dní v týdnu pracuješ?")
    print("2. V kolik hodin obvykle vstáváš?")
    print("3. V kolik hodin obvykle jdeš spát?")
    print("4. Kdy pociťuješ největší hlad?")
    
    print("\n2️⃣  TÝDENNÍ MEAL PREP")
    print("-" * 80)
    print("5. Kolik času máš na meal prep týdně? (minuty)")
    print("6. Který den ti nejvíce vyhovuje pro meal prep?")
    print("7. V jakou denní dobu je pro tebe nejlepší čas?")
    print("8. Na kolik dní dopředu chceš připravovat?")
    print("9. Kolik různých jídel chceš mít v rotaci?")
    print("10. Jaká jídla jsi ochoten připravovat dopředu?")
    
    print("\n3️⃣  NÁKUP POTRAVIN")
    print("-" * 80)
    print("11. Jaký je týdenní rozpočet na potraviny pro celou rodinu?")
    print("12. Kde nejčastěji nakupuješ?")
    print("13. Který den nejčastěji nakupuješ?")
    print("14. Sleduješ aktivně slevy?")
    print("15. Jsi ochoten nakupovat ve více obchodech kvůli slevám?")
    print("16. Děláš nákupní seznam?")
    print("17. Plánuješ nákup podle jídelníčku?")
    print("18. Nakupuješ levnější kusy masa (např. stehna místo prsou)?")
    
    print("\n4️⃣  VAŘENÍ A KUCHYŇSKÉ VYBAVENÍ")
    print("-" * 80)
    print("19. Jak rád vaříš?")
    print("20. Jaké kuchyňské vybavení máš?")
    print("21. Máš vakuovačku?")
    print("22. Kolik meal prep krabiček máš?")
    print("23. Jaké metody přípravy preferuješ?")
    print("24. Preferuješ batch cooking (připravit hodně najednou)?")
    
    print("\n5️⃣  JÍDELNÍ PREFERENCE")
    print("-" * 80)
    print("25. Jaká jsou tvoje TOP 5 oblíbených jídel?")
    print("26. Jaká jídla jsou ideální pro meal prep?")
    print("27. Ze kterých jídel jsi už unavený?")
    print("28. Jaké jsou tvoje oblíbené zdroje bílkovin?")
    print("29. Jakou zeleninu nejraději jíš?")
    print("30. Preferuješ jednoduché recepty?")
    print("31. Oblíbuješ jednohrnce (one-pot meals)?")
    
    print("\n6️⃣  ZDRAVOTNÍ CÍLE")
    print("-" * 80)
    print("32. Jaké jsou tvoje hlavní cíle?")
    print("33. Aktuální váha?")
    print("34. Cílová váha za 1 měsíc?")
    print("35. Cílová váha za 3 měsíce?")
    print("36. Cílová váha za 6 měsíců?")
    print("37. Konečná cílová váha?")
    print("38. Jaké jsou tvoje problémové oblasti?")
    
    print("\n7️⃣  RODINNÉ STRAVOVÁNÍ")
    print("-" * 80)
    print("39. Vaříš pro celou rodinu?")
    print("40. Jak často vaříš pro rodinu?")
    print("41. Sdílí rodina stejné jídlo?")
    print("42. Pomáhá ti partnerka s meal prepem?")
    print("43. Vaříš zvlášť pro Kubíka?")
    
    print("\n8️⃣  DALŠÍ POZNÁMKY")
    print("-" * 80)
    print("44. Jakékoli další poznámky nebo speciální požadavky?")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--seznam":
        # Zobraz pouze seznam otázek
        zobraz_otazky_seznam()
    else:
        # Spusť interaktivní dotazník
        dotaznik = interaktivni_dotaznik()
        
        # Zobraz doporučení
        print("\n📋 DOPORUČENÍ NA ZÁKLADĚ TVÝCH ODPOVĚDÍ:")
        print("=" * 80)
        for i, doporuceni in enumerate(dotaznik.ziskej_doporuceni(), 1):
            print(f"\n{i}. {doporuceni}")
        
        # Ulož odpovědi
        cesta = input("\n\nChceš uložit odpovědi? (zadej název souboru nebo Enter pro přeskočení): ")
        if cesta:
            if not cesta.endswith('.json'):
                cesta += '.json'
            dotaznik.uloz_do_souboru(cesta)
            print(f"✅ Odpovědi uloženy do: {cesta}")
