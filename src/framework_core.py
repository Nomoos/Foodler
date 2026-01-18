#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modular Meal & Supplement System – Family-Scale Framework
===========================================================

Implementace kompletního framework pro správu jídel, suplementů a tělesných metrik
pro více osob v rodině s různými potřebami.

Autor: GitHub Copilot pro Foodler
Datum: 2026-01-18
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
from datetime import date, datetime
from decimal import Decimal


# ============================================================================
# ENUMS
# ============================================================================

class TypJidla(Enum):
    """Typ jídla/slotu v denním rozložení."""
    SNIDANE = "snídaně"
    DOPOLEDNI_SVACINA = "dopolední svačina"
    OBED = "oběd"
    ODPOLEDNI_SVACINA = "odpolední svačina"
    VECERE = "večeře"
    VECERNI_SVACINA = "večerní svačina"
    SHAKE = "shake"


class VekKategorie(Enum):
    """Věková kategorie osoby."""
    DITE = "dítě"
    DOSPELY = "dospělý"


class TypRozlozeni(Enum):
    """Typ rozložení kalorií během dne."""
    ROVNOMERNE = "rovnoměrné"
    NEROVNOMERNE = "nerovnoměrné"
    SKOLNI_REZIM = "školní režim"
    PRACOVNI_REZIM = "pracovní režim"


class TypDne(Enum):
    """Typ dne pro pravidla suplementů."""
    PRACOVNI = "pracovní"
    VIKEND = "víkend"
    SKOLKA = "školka"
    TRENINGOVY = "tréningový"


class PrepLevel(Enum):
    """Úroveň přípravy jídla."""
    ZADNA = "žádná"
    MINIMALNI = "minimální"
    STREDNI = "střední"
    VYSOKA = "vysoká"


# ============================================================================
# BODY METRICS (Time-Based)
# ============================================================================

@dataclass
class BodyMetric:
    """
    Časově ohraničená tělesná metrika.
    
    Body metrics jsou historická fakta, ne předpoklady.
    """
    metric_type: str  # "weight", "height", "body_fat", atd.
    value: float
    unit: str  # "kg", "cm", "%"
    measured_at: date
    poznamka: Optional[str] = None
    
    def __str__(self) -> str:
        return f"{self.metric_type}: {self.value} {self.unit} ({self.measured_at})"


@dataclass
class BodyMetricsHistory:
    """Historie tělesných metrik pro jednu osobu."""
    osoba_id: str
    metriky: List[BodyMetric] = field(default_factory=list)
    
    def pridej_mereni(self, metrika: BodyMetric):
        """Přidá nové měření."""
        self.metriky.append(metrika)
        # Seřaď podle data
        self.metriky.sort(key=lambda m: m.measured_at, reverse=True)
    
    def posledni_vaha(self) -> Optional[BodyMetric]:
        """Vrátí poslední měření váhy."""
        for m in self.metriky:
            if m.metric_type == "weight":
                return m
        return None
    
    def vaha_k_datu(self, datum: date) -> Optional[BodyMetric]:
        """Vrátí měření váhy k danému datu nebo nejbližší starší."""
        vahy = [m for m in self.metriky if m.metric_type == "weight" and m.measured_at <= datum]
        return vahy[0] if vahy else None


# ============================================================================
# MEAL MODULES
# ============================================================================

@dataclass
class Makra:
    """Makronutrienty jídla."""
    kalorie: int
    bilkoviny: float
    sacharidy: float
    tuky: float
    vlaknina: float = 0.0
    
    def __str__(self) -> str:
        return f"{self.kalorie} kcal | P{self.bilkoviny}g C{self.sacharidy}g F{self.tuky}g V{self.vlaknina}g"


@dataclass
class MealModule:
    """
    Základní jídelní modul - znovupoužitelný stavební blok.
    
    Moduly jsou sdílené napříč celou rodinou, mění se jen porce.
    """
    id: str
    nazev: str
    makra: Makra
    tagy: List[str] = field(default_factory=list)
    omezeni: List[str] = field(default_factory=list)  # "gluten-free", "lactose-free"
    prep_level: PrepLevel = PrepLevel.STREDNI
    zavislosti: List[str] = field(default_factory=list)  # ID jiných modulů
    je_addon: bool = False  # Je to doplněk?
    poznamky: Optional[str] = None
    
    def ma_tag(self, tag: str) -> bool:
        """Kontroluje, zda modul má daný tag."""
        return tag in self.tagy
    
    def splnuje_omezeni(self, omezeni: List[str]) -> bool:
        """Kontroluje, zda modul splňuje všechna omezení."""
        return all(o in self.omezeni for o in omezeni)
    
    def __str__(self) -> str:
        addon = " [ADD-ON]" if self.je_addon else ""
        return f"{self.nazev}{addon}: {self.makra}"


# ============================================================================
# DAY TEMPLATE SYSTEM
# ============================================================================

@dataclass
class Slot:
    """
    Jeden slot v denním šablonu (čas na jídlo).
    
    Slot definuje, kdy a co se má jíst.
    """
    slot_id: str
    slot_type: TypJidla
    vaha: float  # 0-1 podíl denních cílů (např. 0.25 = 25%)
    casove_okno: Optional[Tuple[str, str]] = None  # ("06:00", "07:00")
    omezeni_slotu: List[str] = field(default_factory=list)
    povolene_tagy: List[str] = field(default_factory=list)
    poznamka: Optional[str] = None
    
    def je_v_casovem_okne(self, cas: str) -> bool:
        """Kontroluje, zda čas spadá do časového okna."""
        if not self.casove_okno:
            return True
        return self.casove_okno[0] <= cas <= self.casove_okno[1]
    
    def __str__(self) -> str:
        okno = f" ({self.casove_okno[0]}-{self.casove_okno[1]})" if self.casove_okno else ""
        return f"{self.slot_type.value}{okno}: {self.vaha*100:.0f}% denních cílů"


@dataclass
class DayTemplate:
    """
    Šablona dne - definuje, jak je den rozdělen na jídelní sloty.
    
    Různé osoby mohou používat různé šablony i se stejným počtem jídel.
    """
    template_id: str
    nazev: str
    pocet_jidel: int
    typ_rozlozeni: TypRozlozeni
    sloty: List[Slot] = field(default_factory=list)
    
    def pridej_slot(self, slot: Slot):
        """Přidá slot do šablony."""
        self.sloty.append(slot)
    
    def validuj(self) -> Tuple[bool, Optional[str]]:
        """
        Validuje šablonu.
        
        Returns:
            (je_validni, chybova_zprava)
        """
        # Kontrola počtu slotů
        if len(self.sloty) != self.pocet_jidel:
            return False, f"Počet slotů ({len(self.sloty)}) != počet jídel ({self.pocet_jidel})"
        
        # Kontrola součtu vah
        soucet_vah = sum(s.vaha for s in self.sloty)
        if abs(soucet_vah - 1.0) > 0.01:
            return False, f"Součet vah slotů ({soucet_vah:.2f}) != 1.0"
        
        return True, None
    
    def __str__(self) -> str:
        validni, _ = self.validuj()
        status = "✅" if validni else "❌"
        return f"{self.nazev} ({self.typ_rozlozeni.value}): {self.pocet_jidel} jídel {status}"


# ============================================================================
# SUPPLEMENT SYSTEM
# ============================================================================

@dataclass
class SupplementDefinition:
    """
    Definice suplementu - co to je a jak se užívá.
    """
    id: str
    nazev: str
    davka: str
    timing_pravidla: List[str] = field(default_factory=list)  # "ráno", "s jídlem", "večer"
    podminky: List[str] = field(default_factory=list)  # "nalačno", "30min před jídlem"
    konflikty: List[str] = field(default_factory=list)  # ID jiných suplementů
    poznamka: Optional[str] = None
    
    def je_kompatibilni_s(self, jiny_suplement_id: str) -> bool:
        """Kontroluje, zda je kompatibilní s jiným suplementem."""
        return jiny_suplement_id not in self.konflikty
    
    def __str__(self) -> str:
        return f"{self.nazev} ({self.davka}) - {', '.join(self.timing_pravidla)}"


@dataclass
class SupplementPack:
    """
    Balíček suplementů - logické seskupení.
    
    Např.: Ranní balíček, Večerní balíček, Školní balíček
    """
    pack_id: str
    nazev: str
    suplementy: List[str] = field(default_factory=list)  # ID suplementů
    povolene_sloty: List[str] = field(default_factory=list)  # ID slotů
    pravidla_typu_dne: List[TypDne] = field(default_factory=list)
    poznamka: Optional[str] = None
    
    def je_aktivni_pro_typ_dne(self, typ_dne: TypDne) -> bool:
        """Kontroluje, zda je balíček aktivní pro daný typ dne."""
        if not self.pravidla_typu_dne:
            return True
        return typ_dne in self.pravidla_typu_dne
    
    def __str__(self) -> str:
        return f"{self.nazev}: {len(self.suplementy)} suplementů"


# ============================================================================
# PERSON PROFILE
# ============================================================================

@dataclass
class DailyTargets:
    """Denní cíle pro jednu osobu."""
    kalorie: int
    bilkoviny: Optional[float] = None
    sacharidy: Optional[float] = None
    tuky: Optional[float] = None
    vlaknina: Optional[float] = None
    
    def __str__(self) -> str:
        result = f"{self.kalorie} kcal"
        if self.bilkoviny:
            result += f" | P{self.bilkoviny}g"
        if self.sacharidy:
            result += f" | C{self.sacharidy}g"
        if self.tuky:
            result += f" | F{self.tuky}g"
        if self.vlaknina:
            result += f" | V{self.vlaknina}g"
        return result


@dataclass
class PersonProfile:
    """
    Profil jedné osoby - obsahuje všechny osobní parametry.
    """
    id: str
    jmeno: str
    vek_kategorie: VekKategorie
    daily_targets: DailyTargets
    pocet_jidel: int
    day_template_id: str
    dietni_omezeni: List[str] = field(default_factory=list)
    supplement_pack_ids: List[str] = field(default_factory=list)
    body_metrics: Optional[BodyMetricsHistory] = None
    poznamky: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.body_metrics is None:
            self.body_metrics = BodyMetricsHistory(osoba_id=self.id)
    
    def posledni_vaha(self) -> Optional[float]:
        """Vrátí poslední zaznamenanou váhu."""
        metrika = self.body_metrics.posledni_vaha()
        return metrika.value if metrika else None
    
    def __str__(self) -> str:
        vaha = self.posledni_vaha()
        vaha_str = f", Váha: {vaha} kg" if vaha else ""
        return f"{self.jmeno} ({self.vek_kategorie.value}): {self.daily_targets}{vaha_str}"


# ============================================================================
# MODULE LIBRARY & SUPPLEMENT CATALOG
# ============================================================================

@dataclass
class ModuleLibrary:
    """
    Sdílená knihovna jídelních modulů pro celou rodinu.
    """
    moduly: Dict[str, MealModule] = field(default_factory=dict)
    
    def pridej_modul(self, modul: MealModule):
        """Přidá modul do knihovny."""
        self.moduly[modul.id] = modul
    
    def najdi_podle_tagu(self, tag: str) -> List[MealModule]:
        """Najde všechny moduly s daným tagem."""
        return [m for m in self.moduly.values() if m.ma_tag(tag)]
    
    def najdi_podle_omezeni(self, omezeni: List[str]) -> List[MealModule]:
        """Najde všechny moduly splňující omezení."""
        return [m for m in self.moduly.values() if m.splnuje_omezeni(omezeni)]
    
    def __len__(self) -> int:
        return len(self.moduly)


@dataclass
class SupplementCatalog:
    """
    Sdílený katalog suplementů pro celou rodinu.
    """
    suplementy: Dict[str, SupplementDefinition] = field(default_factory=dict)
    balicky: Dict[str, SupplementPack] = field(default_factory=dict)
    
    def pridej_suplement(self, suplement: SupplementDefinition):
        """Přidá suplement do katalogu."""
        self.suplementy[suplement.id] = suplement
    
    def pridej_balicek(self, balicek: SupplementPack):
        """Přidá balíček do katalogu."""
        self.balicky[balicek.pack_id] = balicek
    
    def __len__(self) -> int:
        return len(self.suplementy)


# ============================================================================
# FAMILY STRUCTURE
# ============================================================================

@dataclass
class Family:
    """
    Rodina - kolekce nezávislých systémů pro jednotlivé členy.
    
    Rodina sdílí knihovnu modulů a katalog suplementů, ale každý člen
    je zpracováván nezávisle.
    """
    family_id: str
    nazev: str
    members: Dict[str, PersonProfile] = field(default_factory=dict)
    module_library: ModuleLibrary = field(default_factory=ModuleLibrary)
    supplement_catalog: SupplementCatalog = field(default_factory=SupplementCatalog)
    day_templates: Dict[str, DayTemplate] = field(default_factory=dict)
    kdo_vari: Optional[str] = None  # ID osoby, která vaří
    kdo_nakupuje: Optional[str] = None  # ID osoby, která nakupuje
    
    def pridej_clena(self, profil: PersonProfile):
        """Přidá člena do rodiny."""
        self.members[profil.id] = profil
    
    def pridej_template(self, template: DayTemplate):
        """Přidá denní šablonu."""
        self.day_templates[template.template_id] = template
    
    def ziskej_celkove_kalorie(self) -> int:
        """Vypočítá celkové denní kalorie pro celou rodinu."""
        return sum(m.daily_targets.kalorie for m in self.members.values())
    
    def ziskej_celkovy_pocet_jidel(self) -> int:
        """Vypočítá celkový počet jídel denně."""
        return sum(m.pocet_jidel for m in self.members.values())
    
    def ziskej_celkovy_pocet_suplementu(self) -> int:
        """Vypočítá celkový počet suplementů denně."""
        celkem = 0
        for member in self.members.values():
            for pack_id in member.supplement_pack_ids:
                if pack_id in self.supplement_catalog.balicky:
                    pack = self.supplement_catalog.balicky[pack_id]
                    celkem += len(pack.suplementy)
        return celkem
    
    def validuj_vsechny_cleny(self) -> Dict[str, Tuple[bool, Optional[str]]]:
        """
        Validuje všechny členy rodiny.
        
        Returns:
            Dict[osoba_id, (je_validni, chybova_zprava)]
        """
        vysledky = {}
        for member_id, member in self.members.items():
            # Validuj template
            if member.day_template_id not in self.day_templates:
                vysledky[member_id] = (False, f"Template {member.day_template_id} neexistuje")
                continue
            
            template = self.day_templates[member.day_template_id]
            je_validni, chyba = template.validuj()
            vysledky[member_id] = (je_validni, chyba)
        
        return vysledky
    
    def __str__(self) -> str:
        return f"""
{'=' * 70}
RODINA: {self.nazev}
{'=' * 70}
Členové: {len(self.members)}
Celkové kalorie: {self.ziskej_celkove_kalorie()} kcal/den
Celkový počet jídel: {self.ziskej_celkovy_pocet_jidel()} jídel/den
Celkový počet suplementů: {self.ziskej_celkovy_pocet_suplementu()} suplementů/den
Knihovna modulů: {len(self.module_library)} modulů
Katalog suplementů: {len(self.supplement_catalog)} suplementů
Vaří: {self.members[self.kdo_vari].jmeno if self.kdo_vari and self.kdo_vari in self.members else 'Neurčeno'}
Nakupuje: {self.members[self.kdo_nakupuje].jmeno if self.kdo_nakupuje and self.kdo_nakupuje in self.members else 'Neurčeno'}
"""


# ============================================================================
# VALIDATION & SUMMARY
# ============================================================================

def vygeneruj_rodinny_prehled(rodina: Family) -> str:
    """Vygeneruje kompletní přehled rodiny."""
    
    result = str(rodina)
    
    result += "\n📊 PŘEHLED ČLENŮ:\n"
    result += "-" * 70 + "\n"
    
    for member_id, member in rodina.members.items():
        result += f"\n{member}\n"
        result += f"  Template: {member.day_template_id}\n"
        result += f"  Jídel: {member.pocet_jidel}\n"
        result += f"  Supplement packy: {len(member.supplement_pack_ids)}\n"
        if member.dietni_omezeni:
            result += f"  Omezení: {', '.join(member.dietni_omezeni)}\n"
    
    result += "\n" + "=" * 70 + "\n"
    result += "VALIDACE\n"
    result += "=" * 70 + "\n"
    
    validace = rodina.validuj_vsechny_cleny()
    for member_id, (je_validni, chyba) in validace.items():
        member = rodina.members[member_id]
        status = "✅" if je_validni else "❌"
        result += f"{status} {member.jmeno}"
        if chyba:
            result += f": {chyba}"
        result += "\n"
    
    return result


# ============================================================================
# MAIN DEMO
# ============================================================================

def main():
    """Demo kompletního framework."""
    print("=" * 70)
    print("MODULAR MEAL & SUPPLEMENT SYSTEM - FAMILY FRAMEWORK")
    print("=" * 70)
    print("\nFramework implementuje:")
    print("  ✅ Family Structure")
    print("  ✅ Person Profile s DailyTargets")
    print("  ✅ Body Metrics (time-based)")
    print("  ✅ Day Template System (Slots)")
    print("  ✅ Meal Modules (base + add-ons)")
    print("  ✅ Supplement System (Definitions + Packs)")
    print("  ✅ Module Library (shared)")
    print("  ✅ Supplement Catalog (shared)")
    print("  ✅ Validation & Consistency")
    print("  ✅ Family-Level Summary")
    print("\nVíce detailů v dokumentaci a implementačních funkcích.")
    print("=" * 70)


if __name__ == "__main__":
    main()
