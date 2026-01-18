#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo skript - ukázka použití dotazníku pro Romana (Romču/Noma)

Tento skript demonstruje, jak funguje systém dotazníku a doporučení
se zaměřením na týdenní meal prep a optimalizaci nákupů.
"""

import sys
import os

# Přidej projekt root directory do path pro import
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from osoby.osoba_1.dotaznik_roman import (
    DotaznikRoman,
    ZivotniStyl,
    MealPrepPreference,
    NakupniPreference,
    VareniAKuchyne,
    JidelniPreference,
    ZdravotniCile,
    RodinaASpolecneStravovani
)
from datetime import time


def demo_dotaznik():
    """Ukázka vyplněného dotazníku s vygenerovanými doporučeními."""
    
    print("=" * 80)
    print("🎯 DEMO: Dotazník pro Romana (Romču/Noma) - Meal Prep a Nákupy")
    print("=" * 80)
    print()
    
    # Vytvoření ukázkového vyplněného dotazníku
    print("📝 Vytváříme ukázkový vyplněný dotazník...")
    print()
    
    zivotni_styl = ZivotniStyl(
        pracovni_tyden_dnu=5,
        cas_buzeni=time(6, 0),
        cas_spanku=time(22, 30),
        kvalita_spanku="dobra",
        energie_rano="stredni",
        energie_poledne="stredni",
        energie_vecer="stredni",
        nejvetsi_hlad="vecer",
        uroven_stresu="stredni",
        problemy_s_travenim=["pálení žáhy občas", "nadýmání"]
    )
    
    meal_prep_preference = MealPrepPreference(
        cas_na_meal_prep_tyden=180,  # 3 hodiny
        nejlepsi_den_pro_meal_prep="nedele",
        nejlepsi_cas_pro_meal_prep="odpoledne",
        priprava_na_dni=7,  # Celý týden
        cas_na_vareni_vsedni_den=30,
        preferuje_vakuovani=True,
        preferuje_mrazeni=True,
        preferuje_lednici=True,
        ochota_pripravit_dopredu=["hlavní jídla", "snídaně", "svačiny", "saláty"],
        pocet_ruznych_jidel=4
    )
    
    nakupni_preference = NakupniPreference(
        tydenni_rozpocet_rodina=2500.0,  # 3 osoby
        tydenni_rozpocet_osoba=833.0,
        kde_nakupuje_nejcasteji=["Lidl", "Kaufland", "Albert"],
        jak_casto_nakupuje="1x_tyden",
        preferovany_den_nakupu="sobota",
        sleduje_slevy=True,
        ochotny_nakupovat_ve_vice_obchodech=True,
        dela_nakupni_seznam=True,
        planuje_nakup_podle_jidelnicku=True,
        preferuje_kvalitu_nad_cenou=False,
        ochotny_nakupovat_levnejsi_kusy_masa=True,
        nakupuje_do_zasoby=True
    )
    
    vareni_a_kuchyne = VareniAKuchyne(
        jak_rad_vari="rad",
        uroven_vareni="pokrocily",
        ma_kuchynske_vybaveni=[
            "tlakový hrnec",
            "airfryer",
            "trouba",
            "multicooker",
            "vakuovačka",
            "mixér"
        ],
        oblibene_metody_pripravy=[
            "pečení na plechu",
            "tlakový hrnec",
            "airfryer"
        ],
        preferuje_batch_cooking=True,
        ochoten_pripravovat_slozitejsi=False,
        velikost_lednice="stredni",
        ma_mrazak=True,
        ma_vakuovacku=True,
        ma_meal_prep_krabicky=20
    )
    
    jidelni_preference = JidelniPreference(
        top_oblibena_jidla=[
            "Pečená kuřecí prsa s brokolicí",
            "Mleté maso s cuketou",
            "Losos se špenátem",
            "Vejce s avokádem",
            "Grilovaná krůta s paprikou"
        ],
        jidla_vhodna_pro_meal_prep=[
            "Kuřecí prsa batch cooked",
            "Mleté maso s rajčatovou omáčkou",
            "Pečený losos",
            "Napečená vejce"
        ],
        unavena_z_jidel=[
            "Kuřecí stehna s rýží",
            "Těstoviny"
        ],
        preferuje_tepla_jidla=True,
        ochota_jist_studene_meal_prep=True,
        preferuje_jednoduche_recepty=True,
        oblibuje_jednohrnce=True,
        oblibene_zdroje_bilkovin=[
            "Kuřecí prsa",
            "Krůtí maso",
            "Vejce",
            "Losos",
            "Tvaroh",
            "Řecký jogurt"
        ],
        oblibena_zelenina=[
            "Brokolice",
            "Špenát",
            "Paprika",
            "Cuketa",
            "Rajčata"
        ],
        ochota_zkouset_nove="stredni"
    )
    
    zdravotni_cile = ZdravotniCile(
        hlavni_cile=["úbytek váhy", "více energie", "lepší trávení"],
        aktualni_vaha=134.2,
        cilova_vaha_1_mesic=131.0,
        cilova_vaha_3_mesice=125.0,
        cilova_vaha_6_mesicu=115.0,
        cilova_vaha_konecna=95.0,
        problemove_oblasti=["břicho", "boky"],
        zdravotni_problemy=["pálení žáhy", "únava odpoledne"],
        uzivane_suplementy=["Multivitamin", "Omega-3", "Vitamin D"],
        priorita_bilkoviny=True,
        denni_cil_bilkoviny=140,
        denni_cil_kalorie=2000,
        denni_limit_sacharidy=70,
        denni_cil_tuky=129,
        denni_cil_vlaknina=50,
        denni_limit_cukry=10,
        bazalni_metabolismus=2300
    )
    
    rodina_spolecne_stravovani = RodinaASpolecneStravovani(
        vari_pro_celu_rodinu=True,
        jak_casto_vari_pro_rodinu="denne",
        rodina_sdili_stejne_jidlo=False,
        kdo_sdili_jidlo_s_romanem=["Pája částečně - nižší porce"],
        partner_pomaha_s_varenim=True,
        partner_pomaha_s_nakupem=True,
        deli_se_o_meal_prep=True,
        vari_zvlast_pro_kubika=True,
        kubik_ma_odlisne_jidelnicek=True
    )
    
    dotaznik = DotaznikRoman(
        zivotni_styl=zivotni_styl,
        meal_prep_preference=meal_prep_preference,
        nakupni_preference=nakupni_preference,
        vareni_a_kuchyne=vareni_a_kuchyne,
        jidelni_preference=jidelni_preference,
        zdravotni_cile=zdravotni_cile,
        rodina_spolecne_stravovani=rodina_spolecne_stravovani,
        dalsi_poznamky="Chci efektivní meal prep systém - připravit 1x za týden a minimalizovat denní vaření."
    )
    
    # Zobrazení vyplněných odpovědí
    print("✅ Dotazník vyplněn! Zde je shrnutí:")
    print()
    print("-" * 80)
    print("👤 ŽIVOTNÍ STYL")
    print("-" * 80)
    print(f"• Buzení: {zivotni_styl.cas_buzeni}")
    print(f"• Spánek: {zivotni_styl.cas_spanku}")
    print(f"• Největší hlad: {zivotni_styl.nejvetsi_hlad}")
    print()
    
    print("-" * 80)
    print("📅 MEAL PREP")
    print("-" * 80)
    print(f"• Čas na meal prep týdně: {meal_prep_preference.cas_na_meal_prep_tyden} minut")
    print(f"• Den: {meal_prep_preference.nejlepsi_den_pro_meal_prep} {meal_prep_preference.nejlepsi_cas_pro_meal_prep}")
    print(f"• Připrava na: {meal_prep_preference.priprava_na_dni} dní")
    print(f"• Počet různých jídel: {meal_prep_preference.pocet_ruznych_jidel}")
    print()
    
    print("-" * 80)
    print("🛒 NÁKUPY")
    print("-" * 80)
    print(f"• Týdenní rozpočet: {nakupni_preference.tydenni_rozpocet_rodina} Kč (rodina)")
    print(f"• Obchody: {', '.join(nakupni_preference.kde_nakupuje_nejcasteji)}")
    print(f"• Den nákupu: {nakupni_preference.preferovany_den_nakupu}")
    print(f"• Sleduje slevy: {nakupni_preference.sleduje_slevy}")
    print()
    
    print("-" * 80)
    print("🍳 VAŘENÍ")
    print("-" * 80)
    print(f"• Jak rád vaří: {vareni_a_kuchyne.jak_rad_vari}")
    print(f"• Úroveň: {vareni_a_kuchyne.uroven_vareni}")
    print(f"• Vybavení: {', '.join(vareni_a_kuchyne.ma_kuchynske_vybaveni)}")
    print(f"• Meal prep krabičky: {vareni_a_kuchyne.ma_meal_prep_krabicky} ks")
    print()
    
    print("-" * 80)
    print("🍽️  JÍDELNÍ PREFERENCE")
    print("-" * 80)
    print("• TOP oblíbená jídla:")
    for i, jidlo in enumerate(jidelni_preference.top_oblibena_jidla, 1):
        print(f"  {i}. {jidlo}")
    print(f"• Preferuje jednoduché recepty: {jidelni_preference.preferuje_jednoduche_recepty}")
    print(f"• Oblíbené proteiny: {', '.join(jidelni_preference.oblibene_zdroje_bilkovin[:3])}")
    print()
    
    print("-" * 80)
    print("🎯 ZDRAVOTNÍ CÍLE")
    print("-" * 80)
    print(f"• Aktuální váha: {zdravotni_cile.aktualni_vaha} kg")
    print(f"• Cíl za 1 měsíc: {zdravotni_cile.cilova_vaha_1_mesic} kg")
    print(f"• Cíl za 3 měsíce: {zdravotni_cile.cilova_vaha_3_mesice} kg")
    print(f"• Konečný cíl: {zdravotni_cile.cilova_vaha_konecna} kg")
    print(f"• Denní kalorie: {zdravotni_cile.denni_cil_kalorie} kcal (BMR: {zdravotni_cile.bazalni_metabolismus} kcal)")
    print(f"• Makra: {zdravotni_cile.denni_cil_bilkoviny}g P / {zdravotni_cile.denni_limit_sacharidy}g C / {zdravotni_cile.denni_cil_tuky}g F")
    print()
    
    print("-" * 80)
    print("👨‍👩‍👦 RODINA")
    print("-" * 80)
    print(f"• Vaří pro rodinu: {rodina_spolecne_stravovani.vari_pro_celu_rodinu}")
    print(f"• Pája pomáhá: {rodina_spolecne_stravovani.partner_pomaha_s_varenim}")
    print(f"• Kubík jiný jídelníček: {rodina_spolecne_stravovani.kubik_ma_odlisne_jidelnicek}")
    print()
    
    # Vygenerování doporučení
    print()
    print("=" * 80)
    print("🎯 PERSONALIZOVANÁ DOPORUČENÍ - MEAL PREP A NÁKUPY")
    print("=" * 80)
    print()
    
    doporuceni = dotaznik.ziskej_doporuceni()
    
    for i, d in enumerate(doporuceni, 1):
        print(f"\n{i}. {d}")
        print()
    
    # Ukázka týdenního plánu
    print()
    print("=" * 80)
    print("📅 UKÁZKOVÝ TÝDENNÍ PLÁN")
    print("=" * 80)
    print()
    
    print("SOBOTA:")
    print("  09:00-10:30 - Velký nákup (Lidl + Kaufland)")
    print("  11:00-12:00 - Kontrola slev na Kupi.cz, plánování jídelníčku")
    print()
    
    print("NEDĚLE:")
    print("  14:00-17:00 - VELKÝ MEAL PREP (3 hodiny)")
    print("    • Pečení: 2kg kuřecích prsou (2 plechy)")
    print("    • Tlakový hrnec: 1kg mletého masa + rajčatová omáčka")
    print("    • Airfryer: Zelenina (brokolice, paprika)")
    print("    • Příprava: 20 vajec napečených, salátová zelenina")
    print("    • Vakuování: 14 porcí na celý týden")
    print("    • Výsledek: 7 obědů + 7 večeří připraveno")
    print()
    
    print("PONDĚLÍ-PÁTEK:")
    print("  • Ráno (5 min): Ohřát předpřipravené jídlo")
    print("  • Oběd (0 min): Meal prep krabička z lednice")
    print("  • Večer (5 min): Ohřát vakuované jídlo")
    print()
    
    print("STŘEDA večer (30 min):")
    print("  • Mini refresh: Doplnit čerstvou zeleninu")
    print("  • Přemístit jídla z mrazáku do lednice")
    print()
    
    # Ukázka nákupního seznamu
    print()
    print("=" * 80)
    print("🛒 UKÁZKOVÝ NÁKUPNÍ SEZNAM (týdenní)")
    print("=" * 80)
    print()
    
    print("PROTEINY (~1200 Kč):")
    print("  • Kuřecí prsa: 2 kg (160-200 Kč)")
    print("  • Mleté maso: 1 kg (120-150 Kč)")
    print("  • Losos filety: 500g (200-250 Kč)")
    print("  • Vejce: 20 ks (70-80 Kč)")
    print("  • Tvaroh: 1 kg (100-120 Kč)")
    print("  • Řecký jogurt: 1 kg (80-100 Kč)")
    print("  • Sýr (např. eidam): 500g (120-150 Kč)")
    print()
    
    print("ZELENINA (~500 Kč):")
    print("  • Brokolice: 1.5 kg (90-120 Kč)")
    print("  • Špenát: 1 kg (80-100 Kč)")
    print("  • Paprika: 1 kg (80-120 Kč)")
    print("  • Cuketa: 1 kg (50-70 Kč)")
    print("  • Rajčata: 1 kg (60-80 Kč)")
    print("  • Salátová zelenina: 500g (40-60 Kč)")
    print("  • Okurky: 500g (30-40 Kč)")
    print()
    
    print("TUKY A DOPLŇKY (~400 Kč):")
    print("  • Olivový olej: 500ml (120-150 Kč)")
    print("  • Avokádo: 4 ks (80-100 Kč)")
    print("  • Ořechy (mandle, vlašské): 500g (150-180 Kč)")
    print()
    
    print("PRO KUBÍKA (~400 Kč):")
    print("  • Rýže, těstoviny, ovoce, jogurty")
    print()
    
    print("CELKEM: ~2500 Kč/týden")
    print()
    
    # Uložení do souboru
    print("=" * 80)
    print("💾 ULOŽENÍ ODPOVĚDÍ")
    print("=" * 80)
    print()
    
    cesta = "/tmp/demo_dotaznik_roman.json"
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
    print("2. Vyplň dotazník ručně nebo spusť: python osoby/osoba_1/dotaznik_roman.py")
    print("3. Využij doporučení k sestavení týdenního meal prep plánu")
    print("4. Každou sobotu: kontrola slev na Kupi.cz + nákup")
    print("5. Každou neděli: 3 hodiny meal prep = celý týden hotovo")
    print()


if __name__ == "__main__":
    demo_dotaznik()
