#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dotazník pro Páju - Personalizované otázky na lepší přizpůsobení jídelníčku

Tento dotazník pomáhá lépe pochopit:
- Životní styl a denní rutinu
- Preference v jídle a přípravě
- Zdravotní potřeby a cíle
- Praktická omezení (čas, rozpočet, vybavení)
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
    problemy_s_travoreanim: List[str] = field(default_factory=list)  # např. "nadýmání", "pálení žáhy", "zácpa"


@dataclass
class CasovePreference:
    """Časové preference pro jídla a přípravu."""
    
    # Preferované časy jídel (pokud se liší od defaultu)
    preferovany_cas_snidane: Optional[time] = None
    preferovany_cas_svaciny_dopoledne: Optional[time] = None
    preferovany_cas_obeda: Optional[time] = None
    preferovany_cas_svaciny_odpoledne: Optional[time] = None
    preferovany_cas_vecere: Optional[time] = None
    
    # Jídla, která přeskakuje nebo kombinuje
    preskakuje_jidla: List[str] = field(default_factory=list)  # např. ["snídaně", "dopolední svačina"]
    
    # Časové okno pro meal prep
    cas_na_pripravu_vikendy: int = 60  # minuty víkendově
    cas_na_pripravu_vsedni_den: int = 30  # minuty ve všední den
    
    # Kdy má nejvíce času na vaření?
    nejlepsi_cas_pro_meal_prep: str = "nedele_odpoledne"  # např. "sobota_rano", "nedele_odpoledne"


@dataclass
class JidelniPreference:
    """Detailní jídelní preference."""
    
    # TOP 5 oblíbených jídel/receptů
    top_oblibena_jidla: List[str] = field(default_factory=list)
    
    # Jídla, která by chtěla jíst častěji
    chtela_bych_casteji: List[str] = field(default_factory=list)
    
    # Jídla, která už nechce (unavená z nich)
    unavena_z_jidel: List[str] = field(default_factory=list)
    
    # Preference teploty jídel
    preferuje_teplá_jidla: bool = True  # nebo chladná/studená jídla
    ochota_jist_studene_meal_prep: bool = True  # např. předpřipravené saláty
    
    # Preference přípravy
    ochotna_varit_slozitejsi: bool = False  # Složitější recepty (>5 ingrediencí)?
    preferuje_jednoduche_recepty: bool = True
    
    # Sladká vs. slaná
    preferuje_sladke_snacky: bool = False
    preferuje_slane_snacky: bool = True
    
    # Něco nového vs. ověřené
    ochota_zkouset_nove: str = "stredni"  # "vysoka", "stredni", "nizka"


@dataclass
class ZdravotniCile:
    """Zdravotní cíle a specifické potřeby."""
    
    # Hlavní cíle (může být více)
    hlavni_cile: List[str] = field(default_factory=list)  
    # např. ["úbytek váhy", "více energie", "lepší trávení", "méně tuku", "více svalů"]
    
    # Konkrétní váhové cíle
    cilova_vaha_1_mesic: Optional[float] = None
    cilova_vaha_3_mesice: Optional[float] = None
    cilova_vaha_6_mesicu: Optional[float] = None
    
    # Problémové oblasti
    problemove_oblasti: List[str] = field(default_factory=list)
    # např. ["břicho", "boky", "stehna", "paže"]
    
    # Zdravotní problémy související se stravou
    zdravotni_problemy: List[str] = field(default_factory=list)
    # např. ["nadýmání", "únava po jídle", "problémy se spaním", "kolísání nálad"]
    
    # Léky a suplementy
    uzivane_leky: List[str] = field(default_factory=list)
    uzivane_suplementy: List[str] = field(default_factory=list)
    
    # Měsíční cyklus (ovlivňuje chuť k jídlu)
    ovlivnuje_cyklus_chut_k_jidlu: bool = True
    kdy_nejvetsi_chut: Optional[str] = None  # např. "před menstruací", "během menstruace"


@dataclass
class PraktickéOmezeni:
    """Praktická omezení a možnosti."""
    
    # Rozpočet na potraviny
    tydenni_rozpocet_osoba: Optional[float] = None  # Kč/týden/osobu
    ochota_nakupovat_drazsi_kvalitni: bool = True
    
    # Nákupní návyky
    kde_nakupuje_nejcasteji: List[str] = field(default_factory=list)  # např. ["Lidl", "Kaufland", "Albert"]
    jak_casto_nakupuje: str = "1x_tyden"  # "denne", "2-3x_tyden", "1x_tyden"
    
    # Kuchyňské vybavení
    ma_kuchynske_vybaveni: List[str] = field(default_factory=list)
    # např. ["multicooker", "airfryer", "mixér", "pomalý hrnec"]
    
    # Skladování
    velikost_lednice: str = "stredni"  # "mala", "stredni", "velka"
    ma_mrazak: bool = True
    ma_misto_na_meal_prep_krabicky: bool = True
    
    # Rodina a společné jídlo
    jak_casto_vari_pro_celu_rodinu: str = "denne"  # "denne", "vikendy", "obcas"
    rodina_sdili_stejne_jidlo: bool = False  # Jí stejně jako Roman a Kubík?


@dataclass
class SociálníAEmoce:
    """Sociální faktory a emoční stravování."""
    
    # Emoční stravování
    ji_kdyz_je_stres: bool = False
    ji_kdyz_je_nuda: bool = False
    ji_kdyz_je_smutna: bool = False
    
    # Co pomáhá odolat pokušení?
    co_pomaha_odolat: List[str] = field(default_factory=list)
    # např. ["mít připravené zdravé svačiny", "voda", "zubní pasta", "procházka"]
    
    # Sociální situace
    obtizne_situace: List[str] = field(default_factory=list)
    # např. ["oslavy", "návštěvy", "restaurace", "víkendové snídaně"]
    
    # Podpora z okolí
    ma_podporu_rodiny: bool = True
    chce_hubnout_s_partnerem: bool = True


@dataclass
class DotaznikPaja:
    """Kompletní dotazník pro Páju."""
    
    zivotni_styl: ZivotniStyl
    casove_preference: CasovePreference
    jidelni_preference: JidelniPreference
    zdravotni_cile: ZdravotniCile
    prakticke_omezeni: PraktickéOmezeni
    socialni_emoce: SociálníAEmoce
    
    # Volné poznámky
    dalsi_poznamky: str = ""
    
    def to_dict(self) -> Dict:
        """Převede dotazník na slovník."""
        return {
            "zivotni_styl": self.zivotni_styl.__dict__,
            "casove_preference": self.casove_preference.__dict__,
            "jidelni_preference": self.jidelni_preference.__dict__,
            "zdravotni_cile": self.zdravotni_cile.__dict__,
            "prakticke_omezeni": self.prakticke_omezeni.__dict__,
            "socialni_emoce": self.socialni_emoce.__dict__,
            "dalsi_poznamky": self.dalsi_poznamky
        }
    
    def uloz_do_souboru(self, cesta: str = "dotaznik_odpovedi.json"):
        """Uloží odpovědi do JSON souboru."""
        with open(cesta, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2, default=str)
    
    def ziskej_doporuceni(self) -> List[str]:
        """
        Na základě odpovědí vygeneruje doporučení pro meal planning.
        
        Returns:
            Seznam konkrétních doporučení
        """
        doporuceni = []
        
        # Doporučení na základě energetických hladin
        if self.zivotni_styl.energie_rano == "nizka":
            doporuceni.append("🌅 Ranní jídlo: Zaměř se na bílkoviny a zdravé tuky na snídani (vejce, tvaroh, avokádo) pro stabilní energii.")
        
        if self.zivotni_styl.nejvetsi_hlad == "vecer":
            doporuceni.append("🌙 Večerní hlad: Naplánuj větší večeři s dostatkem bílkovin (30-35g) a zeleniny pro sytost.")
        
        # Doporučení na základě časových možností
        if self.casove_preference.cas_na_pripravu_vsedni_den < 30:
            doporuceni.append("⏰ Meal prep: S omezeným časem ve všední dny doporuč víkendový meal prep - příprava pro 3-4 dny dopředu.")
        
        # Doporučení na základě preferencí
        if self.jidelni_preference.preferuje_jednoduche_recepty:
            doporuceni.append("📝 Jednoduché recepty: Zaměř se na recepty do 5 ingrediencí (kuřecí + brokolice + sýr, losos + špenát + česnek).")
        
        if self.jidelni_preference.ochota_jist_studene_meal_prep:
            doporuceni.append("🥗 Studená jídla: Můžeš využít předpřipravené saláty, cold meal prep misky, studené kuřecí prsa s zeleninou.")
        
        # Doporučení na základě zdravotních cílů
        if "úbytek váhy" in self.zdravotni_cile.hlavni_cile:
            doporuceni.append("📉 Úbytek váhy: Udržuj kalorický deficit (1508 kcal), prioritizuj bílkoviny (90g+) a minimalizuj sacharidy (<60g).")
        
        if "více energie" in self.zdravotni_cile.hlavni_cile:
            doporuceni.append("⚡ Více energie: Ujisti se o dostatku omega-3 (losos, ořechy), vitaminu B (maso, vejce) a hydrataci (2-3L vody).")
        
        # Doporučení na základě emocí
        if self.socialni_emoce.ji_kdyz_je_stres or self.socialni_emoce.ji_kdyz_je_nuda:
            doporuceni.append("🧘 Emoční stravování: Připrav si zdravé low-carb svačiny předem (zelenina s hummusem, tvaroh, ořechy v porcích).")
        
        # Doporučení na základě rozpočtu
        if self.prakticke_omezeni.tydenni_rozpocet_osoba and self.prakticke_omezeni.tydenni_rozpocet_osoba < 800:
            doporuceni.append("💰 Rozpočet: Zaměř se na cenově výhodné proteiny (vejce, kuřecí stehna, tvaroh), využij slevy z Kupi.cz.")
        
        if not doporuceni:
            doporuceni.append("✅ Pokračuj v současném plánu a postupně přidávej variace podle chuti.")
        
        return doporuceni


def interaktivni_dotaznik() -> DotaznikPaja:
    """
    Interaktivní dotazník - klade otázky a ukládá odpovědi.
    
    Returns:
        Vyplněný DotaznikPaja objekt
    """
    print("=" * 80)
    print("DOTAZNÍK PRO PÁJU - Personalizace jídelníčku")
    print("=" * 80)
    print("\nTento dotazník pomůže vytvořit jídelníček šitý přímo na míru tvým potřebám.")
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
    
    print("\nJaká je tvoje energie v různých částech dne?")
    print("(vysoka / stredni / nizka)")
    energie_rano = input("  Ráno: [stredni] ") or "stredni"
    energie_poledne = input("  Poledne: [stredni] ") or "stredni"
    energie_vecer = input("  Večer: [stredni] ") or "stredni"
    
    print("\nKdy pociťuješ největší hlad?")
    print("(rano / dopoledne / obed / odpoledne / vecer / noc)")
    nejvetsi_hlad = input("  [vecer] ") or "vecer"
    
    zivotni_styl = ZivotniStyl(
        pracovni_tyden_dnu=int(pracovni_tyden),
        cas_buzeni=cas_buzeni,
        cas_spanku=cas_spanku,
        energie_rano=energie_rano,
        energie_poledne=energie_poledne,
        energie_vecer=energie_vecer,
        nejvetsi_hlad=nejvetsi_hlad
    )
    
    # === ČASOVÉ PREFERENCE ===
    print("\n" + "=" * 80)
    print("2️⃣  ČASOVÉ PREFERENCE")
    print("=" * 80)
    
    print("\nKolik času máš na přípravu jídel?")
    cas_vikend = input("  Víkend (minuty): [60] ") or "60"
    cas_vsedni = input("  Všední den (minuty): [30] ") or "30"
    
    print("\nKdy ti nejvíc vyhovuje meal prep?")
    print("(sobota_rano / sobota_odpoledne / nedele_rano / nedele_odpoledne)")
    meal_prep_cas = input("  [nedele_odpoledne] ") or "nedele_odpoledne"
    
    casove_preference = CasovePreference(
        cas_na_pripravu_vikendy=int(cas_vikend),
        cas_na_pripravu_vsedni_den=int(cas_vsedni),
        nejlepsi_cas_pro_meal_prep=meal_prep_cas
    )
    
    # === JÍDELNÍ PREFERENCE ===
    print("\n" + "=" * 80)
    print("3️⃣  JÍDELNÍ PREFERENCE")
    print("=" * 80)
    
    print("\nJaká jsou tvoje TOP 5 oblíbených jídel/receptů?")
    print("(každé na nový řádek, prázdný řádek pro konec)")
    oblibena_jidla = []
    for i in range(1, 6):
        jidlo = input(f"  {i}. ")
        if jidlo:
            oblibena_jidla.append(jidlo)
        else:
            break
    
    print("\nJaká jídla bys chtěla jíst častěji?")
    print("(každé na nový řádek, prázdný řádek pro konec)")
    chtela_casteji = []
    while True:
        jidlo = input("  ")
        if not jidlo:
            break
        chtela_casteji.append(jidlo)
    
    print("\nZ jakých jídel jsi už unavená? (neměla bys je na jídelníčku)")
    print("(každé na nový řádek, prázdný řádek pro konec)")
    unavena_z = []
    while True:
        jidlo = input("  ")
        if not jidlo:
            break
        unavena_z.append(jidlo)
    
    preferuje_jednoduche = input("\nPreferuješ jednoduché recepty (do 5 ingrediencí)? (ano/ne): [ano] ") or "ano"
    ochota_nove = input("Jak moc jsi ochotná zkoušet nové recepty? (vysoka/stredni/nizka): [stredni] ") or "stredni"
    
    jidelni_preference = JidelniPreference(
        top_oblibena_jidla=oblibena_jidla,
        chtela_bych_casteji=chtela_casteji,
        unavena_z_jidel=unavena_z,
        preferuje_jednoduche_recepty=(preferuje_jednoduche.lower() == "ano"),
        ochota_zkouset_nove=ochota_nove
    )
    
    # === ZDRAVOTNÍ CÍLE ===
    print("\n" + "=" * 80)
    print("4️⃣  ZDRAVOTNÍ CÍLE")
    print("=" * 80)
    
    print("\nJaké jsou tvoje hlavní cíle? (vyber všechny, které platí)")
    print("(úbytek váhy / více energie / lepší trávení / méně tuku / více svalů)")
    print("(každý na nový řádek, prázdný řádek pro konec)")
    cile = []
    while True:
        cil = input("  ")
        if not cil:
            break
        cile.append(cil)
    
    cilova_1m = input("\nCílová váha za 1 měsíc (kg): ")
    cilova_3m = input("Cílová váha za 3 měsíce (kg): ")
    cilova_6m = input("Cílová váha za 6 měsíců (kg): ")
    
    zdravotni_cile = ZdravotniCile(
        hlavni_cile=cile,
        cilova_vaha_1_mesic=float(cilova_1m) if cilova_1m else None,
        cilova_vaha_3_mesice=float(cilova_3m) if cilova_3m else None,
        cilova_vaha_6_mesicu=float(cilova_6m) if cilova_6m else None
    )
    
    # === PRAKTICKÁ OMEZENÍ ===
    print("\n" + "=" * 80)
    print("5️⃣  PRAKTICKÁ OMEZENÍ")
    print("=" * 80)
    
    rozpocet = input("\nTýdenní rozpočet na potraviny na osobu (Kč): ")
    
    print("\nKde nejčastěji nakupuješ? (každý obchod na nový řádek)")
    obchody = []
    while True:
        obchod = input("  ")
        if not obchod:
            break
        obchody.append(obchod)
    
    prakticke_omezeni = PraktickéOmezeni(
        tydenni_rozpocet_osoba=float(rozpocet) if rozpocet else None,
        kde_nakupuje_nejcasteji=obchody
    )
    
    # === SOCIÁLNÍ A EMOCE ===
    print("\n" + "=" * 80)
    print("6️⃣  EMOČNÍ STRAVOVÁNÍ A PODPORA")
    print("=" * 80)
    
    ji_stres = input("\nJíš, když jsi ve stresu? (ano/ne): [ne] ") or "ne"
    ji_nuda = input("Jíš, když je ti nuda? (ano/ne): [ne] ") or "ne"
    
    print("\nCo ti pomáhá odolat pokušení? (každé na nový řádek)")
    pomoc = []
    while True:
        item = input("  ")
        if not item:
            break
        pomoc.append(item)
    
    socialni_emoce = SociálníAEmoce(
        ji_kdyz_je_stres=(ji_stres.lower() == "ano"),
        ji_kdyz_je_nuda=(ji_nuda.lower() == "ano"),
        co_pomaha_odolat=pomoc
    )
    
    # === POZNÁMKY ===
    print("\n" + "=" * 80)
    poznamky = input("\nDalší poznámky nebo speciální požadavky:\n")
    
    # Vytvoření dotazníku
    dotaznik = DotaznikPaja(
        zivotni_styl=zivotni_styl,
        casove_preference=casove_preference,
        jidelni_preference=jidelni_preference,
        zdravotni_cile=zdravotni_cile,
        prakticke_omezeni=prakticke_omezeni,
        socialni_emoce=socialni_emoce,
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
    print("DOTAZNÍK PRO PÁJU - Seznam otázek")
    print("=" * 80)
    
    print("\n1️⃣  ŽIVOTNÍ STYL A DENNÍ RUTINA")
    print("-" * 80)
    print("1. Kolik dní v týdnu pracuješ?")
    print("2. V kolik hodin obvykle vstáváš?")
    print("3. V kolik hodin obvykle jdeš spát?")
    print("4. Jaká je tvoje kvalita spánku? (výborná/dobrá/střední/špatná)")
    print("5. Jaká je tvoje energie ráno? (vysoká/střední/nízká)")
    print("6. Jaká je tvoje energie o poledni? (vysoká/střední/nízká)")
    print("7. Jaká je tvoje energie večer? (vysoká/střední/nízká)")
    print("8. Kdy pociťuješ největší hlad? (ráno/dopoledne/oběd/odpoledne/večer/noc)")
    print("9. Jaká je tvoje úroveň stresu? (nízká/střední/vysoká)")
    print("10. Máš nějaké problémy s trávením? (nadýmání/pálení žáhy/zácpa/jiné)")
    
    print("\n2️⃣  ČASOVÉ PREFERENCE")
    print("-" * 80)
    print("11. Kolik času máš na přípravu jídel o víkendu? (minuty)")
    print("12. Kolik času máš na přípravu jídel ve všední den? (minuty)")
    print("13. Kdy ti nejvíc vyhovuje meal prep? (sobota ráno/odpoledne, neděle ráno/odpoledne)")
    print("14. Přeskakuješ nějaká jídla? (která?)")
    print("15. Liší se tvoje preferované časy jídel od standardu (7:30, 10:00, 12:30, 15:30, 18:30)?")
    
    print("\n3️⃣  JÍDELNÍ PREFERENCE")
    print("-" * 80)
    print("16. Jaká jsou tvoje TOP 5 oblíbených jídel/receptů?")
    print("17. Jaká jídla bys chtěla jíst častěji?")
    print("18. Z jakých jídel jsi už unavená?")
    print("19. Preferuješ teplá jídla nebo ti nevadí studené meal prep?")
    print("20. Jsi ochotná jíst studené předpřipravené saláty a misky?")
    print("21. Jsi ochotná vařit složitější recepty (>5 ingrediencí)?")
    print("22. Preferuješ jednoduché recepty?")
    print("23. Preferuješ sladké nebo slané svačiny?")
    print("24. Jak moc jsi ochotná zkoušet nové recepty? (vysoká/střední/nízká)")
    
    print("\n4️⃣  ZDRAVOTNÍ CÍLE")
    print("-" * 80)
    print("25. Jaké jsou tvoje hlavní cíle? (úbytek váhy/více energie/lepší trávení/méně tuku/více svalů)")
    print("26. Jaká je tvoje cílová váha za 1 měsíc?")
    print("27. Jaká je tvoje cílová váha za 3 měsíce?")
    print("28. Jaká je tvoje cílová váha za 6 měsíců?")
    print("29. Jaké jsou tvoje problémové oblasti? (břicho/boky/stehna/paže)")
    print("30. Máš nějaké zdravotní problémy související se stravou?")
    print("31. Užíváš nějaké léky?")
    print("32. Užíváš nějaké doplňky stravy?")
    print("33. Ovlivňuje menstruační cyklus tvoji chuť k jídlu? Kdy je největší?")
    
    print("\n5️⃣  PRAKTICKÁ OMEZENÍ")
    print("-" * 80)
    print("34. Jaký je tvůj týdenní rozpočet na potraviny na osobu? (Kč)")
    print("35. Jsi ochotná nakupovat dražší kvalitní potraviny?")
    print("36. Kde nejčastěji nakupuješ? (Lidl/Kaufland/Albert/Penny/jiné)")
    print("37. Jak často nakupuješ? (denně/2-3x týdně/1x týdně)")
    print("38. Jaké kuchyňské vybavení máš? (multicooker/airfryer/mixér/pomalý hrnec)")
    print("39. Jaká je velikost tvé lednice? (malá/střední/velká)")
    print("40. Máš mrazák?")
    print("41. Máš místo na meal prep krabičky?")
    print("42. Jak často vaříš pro celou rodinu?")
    print("43. Sdílí rodina stejné jídlo?")
    
    print("\n6️⃣  EMOČNÍ STRAVOVÁNÍ A PODPORA")
    print("-" * 80)
    print("44. Jíš, když jsi ve stresu?")
    print("45. Jíš, když je ti nuda?")
    print("46. Jíš, když jsi smutná?")
    print("47. Co ti pomáhá odolat pokušení?")
    print("48. Jaké jsou pro tebe obtížné situace? (oslavy/návštěvy/restaurace)")
    print("49. Máš podporu rodiny?")
    print("50. Chceš hubnout společně s partnerem?")
    
    print("\n7️⃣  DALŠÍ POZNÁMKY")
    print("-" * 80)
    print("51. Jakékoli další poznámky nebo speciální požadavky?")
    
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
            print(f"{i}. {doporuceni}")
        
        # Ulož odpovědi
        cesta = input("\n\nChceš uložit odpovědi? (zadej název souboru nebo Enter pro přeskočení): ")
        if cesta:
            if not cesta.endswith('.json'):
                cesta += '.json'
            dotaznik.uloz_do_souboru(cesta)
            print(f"✅ Odpovědi uloženy do: {cesta}")
