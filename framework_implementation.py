#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Framework Implementation - Foodler Family
==========================================

Konkrétní implementace framework pro rodinu:
- Roman (vaří a nakupuje)
- Pája
- Kubík

Autor: GitHub Copilot pro Foodler
Datum: 2026-01-18
"""

from datetime import date
from framework_core import *


# ============================================================================
# DAY TEMPLATES
# ============================================================================

def vytvor_template_roman() -> DayTemplate:
    """Template pro Romana - 6 jídel, rovnoměrné rozložení."""
    template = DayTemplate(
        template_id="roman_6meals",
        nazev="Roman - 6 jídel rovnoměrně",
        pocet_jidel=6,
        typ_rozlozeni=TypRozlozeni.ROVNOMERNE
    )
    
    # 6 jídel s přibližně stejnými kaloriemi
    template.pridej_slot(Slot(
        slot_id="r_snidane",
        slot_type=TypJidla.SNIDANE,
        vaha=0.175,  # 17.5%
        casove_okno=("06:00", "07:00"),
        povolene_tagy=["protein", "low-carb"]
    ))
    
    template.pridej_slot(Slot(
        slot_id="r_dop_svacina",
        slot_type=TypJidla.DOPOLEDNI_SVACINA,
        vaha=0.125,  # 12.5%
        casove_okno=("09:00", "10:00"),
        povolene_tagy=["snack", "quick"]
    ))
    
    template.pridej_slot(Slot(
        slot_id="r_obed",
        slot_type=TypJidla.OBED,
        vaha=0.225,  # 22.5%
        casove_okno=("12:00", "13:00"),
        povolene_tagy=["protein", "main-meal"]
    ))
    
    template.pridej_slot(Slot(
        slot_id="r_odp_svacina",
        slot_type=TypJidla.ODPOLEDNI_SVACINA,
        vaha=0.125,  # 12.5%
        casove_okno=("15:00", "16:00"),
        povolene_tagy=["snack", "quick"]
    ))
    
    template.pridej_slot(Slot(
        slot_id="r_vecere",
        slot_type=TypJidla.VECERE,
        vaha=0.225,  # 22.5%
        casove_okno=("18:00", "19:00"),
        povolene_tagy=["protein", "main-meal", "family"]
    ))
    
    template.pridej_slot(Slot(
        slot_id="r_vec_svacina",
        slot_type=TypJidla.VECERNI_SVACINA,
        vaha=0.125,  # 12.5%
        casove_okno=("21:00", "22:00"),
        povolene_tagy=["snack", "light"],
        poznamka="Proti nočnímu hladu"
    ))
    
    return template


def vytvor_template_paja() -> DayTemplate:
    """Template pro Páju - 5 jídel, nerovnoměrné rozložení."""
    template = DayTemplate(
        template_id="paja_5meals",
        nazev="Pája - 5 jídel nerovnoměrně",
        pocet_jidel=5,
        typ_rozlozeni=TypRozlozeni.NEROVNOMERNE
    )
    
    # Nerovnoměrné rozložení podle preferencí
    template.pridej_slot(Slot(
        slot_id="p_snidane",
        slot_type=TypJidla.SNIDANE,
        vaha=0.27,  # 27% - největší (nejvyšší hlad ráno)
        casove_okno=("06:00", "06:30"),
        povolene_tagy=["sytici", "vlaknina", "meal-prep"],
        poznamka="Nejvyšší hlad ráno - větší porce"
    ))
    
    template.pridej_slot(Slot(
        slot_id="p_dop_svacina",
        slot_type=TypJidla.DOPOLEDNI_SVACINA,
        vaha=0.10,  # 10% - malá
        casove_okno=("09:00", "10:00"),
        povolene_tagy=["quick", "portable"]
    ))
    
    template.pridej_slot(Slot(
        slot_id="p_obed",
        slot_type=TypJidla.OBED,
        vaha=0.23,  # 23% - menší (problém s objemem)
        casove_okno=("12:00", "13:00"),
        povolene_tagy=["lehke", "vlaknina"],
        poznamka="Menší porce - citlivost na objem"
    ))
    
    template.pridej_slot(Slot(
        slot_id="p_odp_svacina",
        slot_type=TypJidla.ODPOLEDNI_SVACINA,
        vaha=0.17,  # 17% - větší (kritické okno)
        casove_okno=("15:00", "16:00"),
        povolene_tagy=["sytici", "protein"],
        poznamka="Kritické okno 15-16h - důležitá svačina"
    ))
    
    template.pridej_slot(Slot(
        slot_id="p_vecere",
        slot_type=TypJidla.VECERE,
        vaha=0.23,  # 23%
        casove_okno=("18:00", "19:00"),
        povolene_tagy=["lehke", "family"]
    ))
    
    return template


def vytvor_template_kubik() -> DayTemplate:
    """Template pro Kubíka - 5 jídel, školní režim."""
    template = DayTemplate(
        template_id="kubik_5meals",
        nazev="Kubík - 5 jídel školní režim",
        pocet_jidel=5,
        typ_rozlozeni=TypRozlozeni.SKOLNI_REZIM
    )
    
    # Školní režim: 2 doma, 3 ve školce
    template.pridej_slot(Slot(
        slot_id="k_snidane",
        slot_type=TypJidla.SNIDANE,
        vaha=0.25,  # 25% - doma
        casove_okno=("06:30", "07:00"),
        povolene_tagy=["deti", "vitamin-a"],
        poznamka="Doma před školkou"
    ))
    
    template.pridej_slot(Slot(
        slot_id="k_dop_svacina",
        slot_type=TypJidla.DOPOLEDNI_SVACINA,
        vaha=0.10,  # 10% - školka
        casove_okno=("09:00", "10:00"),
        povolene_tagy=["skolka"],
        poznamka="Ve školce"
    ))
    
    template.pridej_slot(Slot(
        slot_id="k_obed",
        slot_type=TypJidla.OBED,
        vaha=0.30,  # 30% - školka (největší)
        casove_okno=("11:30", "12:30"),
        povolene_tagy=["skolka", "hlavni-jidlo"],
        poznamka="Ve školce"
    ))
    
    template.pridej_slot(Slot(
        slot_id="k_odp_svacina",
        slot_type=TypJidla.ODPOLEDNI_SVACINA,
        vaha=0.10,  # 10% - školka
        casove_okno=("14:30", "15:30"),
        povolene_tagy=["skolka"],
        poznamka="Ve školce"
    ))
    
    template.pridej_slot(Slot(
        slot_id="k_vecere",
        slot_type=TypJidla.VECERE,
        vaha=0.25,  # 25% - doma
        casove_okno=("18:00", "19:00"),
        povolene_tagy=["deti", "family", "vitamin-a"],
        poznamka="Doma s rodinou"
    ))
    
    return template


# ============================================================================
# SUPPLEMENT PACKS
# ============================================================================

def vytvor_supplement_catalog() -> SupplementCatalog:
    """Vytvoří katalog suplementů pro celou rodinu."""
    catalog = SupplementCatalog()
    
    # ---- ROMAN ----
    catalog.pridej_suplement(SupplementDefinition(
        id="omeprazol",
        nazev="Omeprazol",
        davka="20 mg",
        timing_pravidla=["ráno", "nalačno"],
        podminky=["30 min před jídlem"],
        poznamka="Léčba refluxu"
    ))
    
    catalog.pridej_suplement(SupplementDefinition(
        id="tlak_leky",
        nazev="Léky na tlak",
        davka="dle předpisu",
        timing_pravidla=["ráno"],
        poznamka="Kardiovaskulární podpora"
    ))
    
    catalog.pridej_suplement(SupplementDefinition(
        id="multivitamin_r",
        nazev="Multivitamin",
        davka="1 tableta",
        timing_pravidla=["s jídlem"]
    ))
    
    catalog.pridej_suplement(SupplementDefinition(
        id="omega3_r",
        nazev="Omega-3",
        davka="1000 mg",
        timing_pravidla=["s jídlem"]
    ))
    
    catalog.pridej_suplement(SupplementDefinition(
        id="vitamin_d_r",
        nazev="Vitamin D",
        davka="2000 IU",
        timing_pravidla=["s jídlem"]
    ))
    
    catalog.pridej_suplement(SupplementDefinition(
        id="probiotika_r",
        nazev="Probiotika",
        davka="1 kapsle",
        timing_pravidla=["ráno"]
    ))
    
    # ---- PÁJA ----
    catalog.pridej_suplement(SupplementDefinition(
        id="letrox",
        nazev="Letrox",
        davka="dle předpisu",
        timing_pravidla=["ráno", "nalačno"],
        podminky=["5:35", "30 min před jídlem"],
        poznamka="Štítná žláza - DŮLEŽITÉ načasování!"
    ))
    
    catalog.pridej_suplement(SupplementDefinition(
        id="antikoncepce",
        nazev="Hormonální antikoncepce",
        davka="dle předpisu",
        timing_pravidla=["večer"],
        poznamka="Pravidelnost důležitá"
    ))
    
    catalog.pridej_suplement(SupplementDefinition(
        id="vitamin_d_p",
        nazev="Vitamin D",
        davka="1000-2000 IU",
        timing_pravidla=["ráno"],
        poznamka="Zlepšit pravidelnost!"
    ))
    
    catalog.pridej_suplement(SupplementDefinition(
        id="omega3_p",
        nazev="Omega-3",
        davka="1000 mg",
        timing_pravidla=["ráno"],
        poznamka="Zlepšit pravidelnost!"
    ))
    
    catalog.pridej_suplement(SupplementDefinition(
        id="magnesium_p",
        nazev="Magnesium",
        davka="300 mg",
        timing_pravidla=["ráno"],
        poznamka="Zlepšit pravidelnost!"
    ))
    
    # ---- KUBÍK ----
    catalog.pridej_suplement(SupplementDefinition(
        id="vitamin_a_k",
        nazev="Vitamin A",
        davka="400 mcg",
        timing_pravidla=["s jídlem"],
        poznamka="Pro zrak - 4 dioptrie!"
    ))
    
    catalog.pridej_suplement(SupplementDefinition(
        id="omega3_dha_k",
        nazev="Omega-3 (DHA)",
        davka="900 mg",
        timing_pravidla=["s jídlem"],
        poznamka="Vývoj mozku a očí"
    ))
    
    # ---- BALÍČKY ----
    
    # Roman - Ranní balíček
    catalog.pridej_balicek(SupplementPack(
        pack_id="roman_am",
        nazev="Roman - Ranní balíček",
        suplementy=["omeprazol", "tlak_leky", "probiotika_r"],
        povolene_sloty=["r_snidane"],
        pravidla_typu_dne=[TypDne.PRACOVNI, TypDne.VIKEND]
    ))
    
    # Roman - S jídlem
    catalog.pridej_balicek(SupplementPack(
        pack_id="roman_meal",
        nazev="Roman - S jídlem",
        suplementy=["multivitamin_r", "omega3_r", "vitamin_d_r"],
        povolene_sloty=["r_snidane", "r_obed", "r_vecere"],
        pravidla_typu_dne=[TypDne.PRACOVNI, TypDne.VIKEND]
    ))
    
    # Pája - Ranní balíček (DŮLEŽITÉ načasování)
    catalog.pridej_balicek(SupplementPack(
        pack_id="paja_am",
        nazev="Pája - Ranní balíček (5:35!)",
        suplementy=["letrox", "vitamin_d_p", "omega3_p", "magnesium_p"],
        povolene_sloty=["p_snidane"],
        pravidla_typu_dne=[TypDne.PRACOVNI, TypDne.VIKEND],
        poznamka="Letrox v 5:35, ostatní v 5:36!"
    ))
    
    # Pája - Večerní balíček
    catalog.pridej_balicek(SupplementPack(
        pack_id="paja_pm",
        nazev="Pája - Večerní balíček",
        suplementy=["antikoncepce"],
        povolene_sloty=["p_vecere"],
        pravidla_typu_dne=[TypDne.PRACOVNI, TypDne.VIKEND]
    ))
    
    # Kubík - S jídlem
    catalog.pridej_balicek(SupplementPack(
        pack_id="kubik_meal",
        nazev="Kubík - S jídlem",
        suplementy=["vitamin_a_k", "omega3_dha_k"],
        povolene_sloty=["k_snidane", "k_obed", "k_vecere"],
        pravidla_typu_dne=[TypDne.PRACOVNI, TypDne.SKOLKA, TypDne.VIKEND]
    ))
    
    return catalog


# ============================================================================
# PERSON PROFILES
# ============================================================================

def vytvor_profil_roman() -> PersonProfile:
    """Vytvoří profil pro Romana."""
    profil = PersonProfile(
        id="roman",
        jmeno="Roman (Romča)",
        vek_kategorie=VekKategorie.DOSPELY,
        daily_targets=DailyTargets(
            kalorie=2001,
            bilkoviny=140.0,
            sacharidy=70.0,
            tuky=129.0,
            vlaknina=20.0
        ),
        pocet_jidel=6,
        day_template_id="roman_6meals",
        dietni_omezeni=["low-carb", "keto"],
        supplement_pack_ids=["roman_am", "roman_meal"],
        poznamky=[
            "Vaří pro celou rodinu",
            "Nakupuje pro celou rodinu",
            "Omeprazol ráno nalačno (reflux)",
            "Léky na tlak",
            "Večerní svačina proti nočnímu hladu",
            "Protein first přístup",
            "Max 70g sacharidů denně"
        ]
    )
    
    # Přidat body metrics
    profil.body_metrics.pridej_mereni(BodyMetric(
        metric_type="weight",
        value=133.6,
        unit="kg",
        measured_at=date(2026, 1, 18),
        poznamka="Měření ráno"
    ))
    
    profil.body_metrics.pridej_mereni(BodyMetric(
        metric_type="body_fat",
        value=37.0,
        unit="%",
        measured_at=date(2026, 1, 18)
    ))
    
    return profil


def vytvor_profil_paja() -> PersonProfile:
    """Vytvoří profil pro Páju."""
    profil = PersonProfile(
        id="paja",
        jmeno="Pája (Pavla)",
        vek_kategorie=VekKategorie.DOSPELY,
        daily_targets=DailyTargets(
            kalorie=1508,
            bilkoviny=92.0,
            sacharidy=60.0,
            tuky=100.0,
            vlaknina=20.0
        ),
        pocet_jidel=5,
        day_template_id="paja_5meals",
        dietni_omezeni=["low-carb", "keto"],
        supplement_pack_ids=["paja_am", "paja_pm"],
        poznamky=[
            "Letrox v 5:35 nalačno (štítná žláza)",
            "Hormonální antikoncepce večer",
            "Největší hlad ráno - větší snídaně",
            "Menší oběd - citlivost na objem",
            "Kritické okno 15-16h - důležitá svačina",
            "Sytost: vláknina + objem + sladkost (NE tuk!)",
            "Vyhnout se: káva (spouští chutě), velké porce",
            "Chronicky vysoký stres - PMS efekty"
        ]
    )
    
    # Přidat body metrics
    profil.body_metrics.pridej_mereni(BodyMetric(
        metric_type="weight",
        value=77.3,
        unit="kg",
        measured_at=date(2025, 12, 22),
        poznamka="Měření tělesného složení"
    ))
    
    profil.body_metrics.pridej_mereni(BodyMetric(
        metric_type="body_fat",
        value=39.6,
        unit="%",
        measured_at=date(2025, 12, 22)
    ))
    
    return profil


def vytvor_profil_kubik() -> PersonProfile:
    """Vytvoří profil pro Kubíka."""
    profil = PersonProfile(
        id="kubik",
        jmeno="Kubík",
        vek_kategorie=VekKategorie.DITE,
        daily_targets=DailyTargets(
            kalorie=1400,
            bilkoviny=19.0,
            sacharidy=130.0,
            tuky=47.0,
            vlaknina=18.0
        ),
        pocet_jidel=5,
        day_template_id="kubik_5meals",
        dietni_omezeni=[],
        supplement_pack_ids=["kubik_meal"],
        poznamky=[
            "Pracovní den: 2 jídla doma, 3 ve školce",
            "Víkend: všech 5 jídel doma",
            "Důraz na vitamin A - mrkev, sladké brambory, špenát",
            "Beta-karoten z oranžové a zelené zeleniny",
            "Zvýšená vláknina kvůli zácpě (18g/den)",
            "Hodně tekutin (1.3 l/den)",
            "Více sacharidů než dospělí (130g min. pro mozek)",
            "Brýle 4 dioptrie - podpora zraku!"
        ]
    )
    
    # Přidat body metrics
    profil.body_metrics.pridej_mereni(BodyMetric(
        metric_type="weight",
        value=17.0,
        unit="kg",
        measured_at=date(2026, 1, 18),
        poznamka="Aktuální měření"
    ))
    
    return profil


# ============================================================================
# FAMILY CREATION
# ============================================================================

def vytvor_foodler_family() -> Family:
    """Vytvoří kompletní rodinu Foodler s frameworkem."""
    
    # Vytvoř rodinu
    rodina = Family(
        family_id="foodler_family",
        nazev="Rodina Foodler",
        kdo_vari="roman",
        kdo_nakupuje="roman"
    )
    
    # Přidej templates
    rodina.pridej_template(vytvor_template_roman())
    rodina.pridej_template(vytvor_template_paja())
    rodina.pridej_template(vytvor_template_kubik())
    
    # Přidej supplement catalog
    rodina.supplement_catalog = vytvor_supplement_catalog()
    
    # Přidej členy
    rodina.pridej_clena(vytvor_profil_roman())
    rodina.pridej_clena(vytvor_profil_paja())
    rodina.pridej_clena(vytvor_profil_kubik())
    
    return rodina


# ============================================================================
# MAIN DEMO
# ============================================================================

def main():
    """Hlavní demo - vytvoření a zobrazení rodiny."""
    
    print("\n" + "=" * 70)
    print("FRAMEWORK IMPLEMENTATION - FOODLER FAMILY")
    print("=" * 70)
    
    # Vytvoř rodinu
    rodina = vytvor_foodler_family()
    
    # Zobraz přehled
    print(vygeneruj_rodinny_prehled(rodina))
    
    # Zobraz detaily jednotlivých členů
    print("\n" + "=" * 70)
    print("DETAILNÍ PŘEHLED ČLENŮ")
    print("=" * 70)
    
    for member_id in ["roman", "paja", "kubik"]:
        member = rodina.members[member_id]
        template = rodina.day_templates[member.day_template_id]
        
        print(f"\n{member.jmeno.upper()}")
        print("-" * 70)
        print(f"Template: {template}")
        print(f"Daily Targets: {member.daily_targets}")
        print(f"Poslední váha: {member.posledni_vaha()} kg")
        
        print(f"\nSloty ({len(template.sloty)}):")
        for slot in template.sloty:
            cil_kcal = int(member.daily_targets.kalorie * slot.vaha)
            print(f"  {slot.slot_type.value:25} {slot.vaha*100:5.1f}% = {cil_kcal:4} kcal")
            if slot.poznamka:
                print(f"    → {slot.poznamka}")
        
        print(f"\nSupplement packy ({len(member.supplement_pack_ids)}):")
        for pack_id in member.supplement_pack_ids:
            pack = rodina.supplement_catalog.balicky[pack_id]
            print(f"  • {pack.nazev}")
            for supp_id in pack.suplementy:
                supp = rodina.supplement_catalog.suplementy[supp_id]
                print(f"    - {supp}")
        
        if member.poznamky:
            print(f"\nPoznámky:")
            for poznamka in member.poznamky[:5]:  # První 5
                print(f"  • {poznamka}")
    
    print("\n" + "=" * 70)
    print("✅ FRAMEWORK ÚSPĚŠNĚ IMPLEMENTOVÁN")
    print("=" * 70)
    print("\n📚 Další kroky:")
    print("  1. Naplnit ModuleLibrary jídelnými moduly")
    print("  2. Implementovat meal assembly logiku")
    print("  3. Vytvořit týdenní jídelníčky")
    print("  4. Integrovat s existujícím kódem")
    print()


if __name__ == "__main__":
    main()
