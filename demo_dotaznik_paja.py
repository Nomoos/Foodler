#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo skript - ukázka použití dotazníku pro Páju

Tento skript demonstruje, jak funguje systém dotazníku a doporučení.
"""

import sys
import os

# Přidej parent directory do path pro import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from osoby.osoba_2.dotaznik_paja import (
    DotaznikPaja,
    ZivotniStyl,
    CasovePreference,
    JidelniPreference,
    ZdravotniCile,
    PraktickéOmezeni,
    SociálníAEmoce
)
from datetime import time


def demo_dotaznik():
    """Ukázka vyplněného dotazníku s vygenerovanými doporučeními."""
    
    print("=" * 80)
    print("🎯 DEMO: Dotazník pro Páju - Ukázka použití")
    print("=" * 80)
    print()
    
    # Vytvoření ukázkového vyplněného dotazníku
    print("📝 Vytváříme ukázkový vyplněný dotazník...")
    print()
    
    zivotni_styl = ZivotniStyl(
        pracovni_tyden_dnu=5,
        cas_buzeni=time(6, 30),
        cas_spanku=time(22, 30),
        kvalita_spanku="dobra",
        energie_rano="nizka",
        energie_poledne="stredni",
        energie_vecer="stredni",
        nejvetsi_hlad="vecer",
        uroven_stresu="stredni",
        problemy_s_travoreanim=["nadýmání občas"]
    )
    
    casove_preference = CasovePreference(
        cas_na_pripravu_vikendy=90,
        cas_na_pripravu_vsedni_den=20,
        nejlepsi_cas_pro_meal_prep="nedele_odpoledne",
        preskakuje_jidla=[]
    )
    
    jidelni_preference = JidelniPreference(
        top_oblibena_jidla=[
            "Kuřecí prsa s brokolicí",
            "Losos se špenátem",
            "Tvarohový krém s ovocem",
            "Řecký salát",
            "Chili con carne (bez fazolí)"
        ],
        chtela_bych_casteji=[
            "Losos",
            "Avokádový salát",
            "Tvarohové dezerty"
        ],
        unavena_z_jidel=[
            "Kuřecí stehna s rýží",
            "Nudle"
        ],
        preferuje_teplá_jidla=True,
        ochota_jist_studene_meal_prep=True,
        ochotna_varit_slozitejsi=False,
        preferuje_jednoduche_recepty=True,
        preferuje_sladke_snacky=False,
        preferuje_slane_snacky=True,
        ochota_zkouset_nove="stredni"
    )
    
    zdravotni_cile = ZdravotniCile(
        hlavni_cile=["úbytek váhy", "více energie"],
        cilova_vaha_1_mesic=75.0,
        cilova_vaha_3_mesice=72.0,
        cilova_vaha_6_mesicu=68.0,
        problemove_oblasti=["břicho", "boky"],
        zdravotni_problemy=["únava odpoledne"],
        uzivane_suplementy=["Multivitamin", "Omega-3", "Vitamin D"],
        ovlivnuje_cyklus_chut_k_jidlu=True,
        kdy_nejvetsi_chut="před menstruací"
    )
    
    prakticke_omezeni = PraktickéOmezeni(
        tydenni_rozpocet_osoba=700.0,
        ochota_nakupovat_drazsi_kvalitni=True,
        kde_nakupuje_nejcasteji=["Lidl", "Kaufland"],
        jak_casto_nakupuje="1x_tyden",
        ma_kuchynske_vybaveni=["airfryer", "mixér", "multicooker"],
        velikost_lednice="stredni",
        ma_mrazak=True,
        ma_misto_na_meal_prep_krabicky=True,
        jak_casto_vari_pro_celu_rodinu="denne",
        rodina_sdili_stejne_jidlo=False
    )
    
    socialni_emoce = SociálníAEmoce(
        ji_kdyz_je_stres=False,
        ji_kdyz_je_nuda=True,
        ji_kdyz_je_smutna=False,
        co_pomaha_odolat=[
            "připravené zdravé svačiny",
            "pitná voda",
            "žvýkačka"
        ],
        obtizne_situace=["oslavy", "víkendové snídaně"],
        ma_podporu_rodiny=True,
        chce_hubnout_s_partnerem=True
    )
    
    dotaznik = DotaznikPaja(
        zivotni_styl=zivotni_styl,
        casove_preference=casove_preference,
        jidelni_preference=jidelni_preference,
        zdravotni_cile=zdravotni_cile,
        prakticke_omezeni=prakticke_omezeni,
        socialni_emoce=socialni_emoce,
        dalsi_poznamky="Chci se cítit lépe ve svém těle a mít více energie na rodinu."
    )
    
    # Zobrazení vyplněných odpovědí
    print("✅ Dotazník vyplněn! Zde je shrnutí:")
    print()
    print("-" * 80)
    print("👤 ŽIVOTNÍ STYL")
    print("-" * 80)
    print(f"• Buzení: {zivotni_styl.cas_buzeni}")
    print(f"• Spánek: {zivotni_styl.cas_spanku}")
    print(f"• Energie ráno: {zivotni_styl.energie_rano}")
    print(f"• Největší hlad: {zivotni_styl.nejvetsi_hlad}")
    print()
    
    print("-" * 80)
    print("⏰ ČASOVÉ PREFERENCE")
    print("-" * 80)
    print(f"• Čas na přípravu (víkend): {casove_preference.cas_na_pripravu_vikendy} min")
    print(f"• Čas na přípravu (všední den): {casove_preference.cas_na_pripravu_vsedni_den} min")
    print(f"• Meal prep: {casove_preference.nejlepsi_cas_pro_meal_prep}")
    print()
    
    print("-" * 80)
    print("🍽️  JÍDELNÍ PREFERENCE")
    print("-" * 80)
    print("• TOP oblíbená jídla:")
    for i, jidlo in enumerate(jidelni_preference.top_oblibena_jidla, 1):
        print(f"  {i}. {jidlo}")
    print(f"• Preferuje jednoduché recepty: {jidelni_preference.preferuje_jednoduche_recepty}")
    print(f"• Ochota jíst studené meal prep: {jidelni_preference.ochota_jist_studene_meal_prep}")
    print()
    
    print("-" * 80)
    print("🎯 ZDRAVOTNÍ CÍLE")
    print("-" * 80)
    print(f"• Hlavní cíle: {', '.join(zdravotni_cile.hlavni_cile)}")
    print(f"• Cílová váha za 1 měsíc: {zdravotni_cile.cilova_vaha_1_mesic} kg")
    print(f"• Cílová váha za 3 měsíce: {zdravotni_cile.cilova_vaha_3_mesice} kg")
    print(f"• Cílová váha za 6 měsíců: {zdravotni_cile.cilova_vaha_6_mesicu} kg")
    print()
    
    print("-" * 80)
    print("💰 PRAKTICKÁ OMEZENÍ")
    print("-" * 80)
    print(f"• Týdenní rozpočet: {prakticke_omezeni.tydenni_rozpocet_osoba} Kč/osoba")
    print(f"• Nakupuje v: {', '.join(prakticke_omezeni.kde_nakupuje_nejcasteji)}")
    print(f"• Kuchyňské vybavení: {', '.join(prakticke_omezeni.ma_kuchynske_vybaveni)}")
    print()
    
    print("-" * 80)
    print("🧘 EMOČNÍ FAKTORY")
    print("-" * 80)
    print(f"• Jí při nudě: {socialni_emoce.ji_kdyz_je_nuda}")
    print(f"• Co pomáhá: {', '.join(socialni_emoce.co_pomaha_odolat)}")
    print(f"• Obtížné situace: {', '.join(socialni_emoce.obtizne_situace)}")
    print()
    
    # Vygenerování doporučení
    print()
    print("=" * 80)
    print("🎯 PERSONALIZOVANÁ DOPORUČENÍ")
    print("=" * 80)
    print()
    
    doporuceni = dotaznik.ziskej_doporuceni()
    
    for i, d in enumerate(doporuceni, 1):
        print(f"{i}. {d}")
        print()
    
    # Uložení do souboru
    print("=" * 80)
    print("💾 ULOŽENÍ ODPOVĚDÍ")
    print("=" * 80)
    print()
    
    cesta = "/tmp/demo_dotaznik_paja.json"
    dotaznik.uloz_do_souboru(cesta)
    print(f"✅ Odpovědi uloženy do: {cesta}")
    print()
    
    print("🔗 Pro zobrazení uložených dat:")
    print(f"   cat {cesta}")
    print()
    
    print("=" * 80)
    print("✅ DEMO DOKONČENO")
    print("=" * 80)
    print()
    print("📚 Další kroky:")
    print("1. Projdi si soubor DOTAZNIK_OTAZKY.md s úplným seznamem otázek")
    print("2. Vyplň dotazník ručně nebo spusť: python osoby/osoba_2/dotaznik_paja.py")
    print("3. Přečti si PRIKLAD_DOPORUCENI.md s konkrétními recepty a plány")
    print("4. Využij doporučení k úpravě jídelníčku")
    print()


if __name__ == "__main__":
    demo_dotaznik()
