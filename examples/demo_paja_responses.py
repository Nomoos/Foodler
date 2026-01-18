#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: Jak používat zaznamenané odpovědi Páji (část 1)

Tento skript ukazuje praktické použití nových tříd pro analýzu jídel
na základě zaznamenaných odpovědí Páji o hladu, energii, sytosti a reakcích těla.
"""

from osoby.osoba_2.preference import (
    PreferenceJidel,
    HladAEnergie,
    StrukturaJidel,
    SyticiJidla,
    ProblematickaJidla,
    ReakceTela
)


def demo_meal_check(meal_name: str):
    """
    Kompletní kontrola jídla podle všech preferencí a reakcí Páji.
    
    Args:
        meal_name: Název jídla ke kontrole
    """
    print(f"\n{'=' * 70}")
    print(f"🍽️  ANALÝZA JÍDLA: {meal_name}")
    print(f"{'=' * 70}")
    
    # 1. Základní preference (textury)
    is_suitable = PreferenceJidel.je_jidlo_vhodne(meal_name)
    print(f"\n✓ Základní vhodnost (bez slizké textury): {'✅ ANO' if is_suitable else '❌ NE'}")
    
    # 2. Sytící potenciál
    is_satisfying = SyticiJidla.je_jidlo_sytici(meal_name)
    print(f"✓ Sytící potenciál (vláknina+objem+sladkost): {'✅ ANO' if is_satisfying else '❌ NE'}")
    
    # 3. Problematická jídla
    is_problematic = ProblematickaJidla.je_jidlo_problematicke(meal_name)
    if is_problematic:
        reason = ProblematickaJidla.ziskej_duvod_problemu(meal_name)
        print(f"⚠️  PROBLEMATICKÉ JÍDLO: {reason}")
    else:
        print(f"✓ Není mezi problematickými jídly: ✅")
    
    # 4. Tělesné reakce
    print("\n📋 Možné tělesné reakce:")
    
    can_cause_bloating = ReakceTela.muze_zpusobit_nadymani(meal_name)
    print(f"  • Nadýmání: {'⚠️  ANO' if can_cause_bloating else '✅ NE'}")
    
    can_cause_fatigue = ReakceTela.muze_zpusobit_unavu(meal_name)
    print(f"  • Únava: {'⚠️  ANO' if can_cause_fatigue else '✅ NE'}")
    
    can_trigger_cravings = ReakceTela.muze_spustit_chute_na_sladke(meal_name)
    print(f"  • Chutě na sladké: {'⚠️  ANO' if can_trigger_cravings else '✅ NE'}")
    
    # 5. Celkové doporučení
    print("\n" + "=" * 70)
    
    all_clear = is_suitable and not is_problematic and not can_cause_fatigue
    if all_clear and is_satisfying:
        print("✅ DOPORUČENO - Výborná volba pro Páju!")
    elif all_clear:
        print("⚠️  PŘIJATELNÉ - Mělo by být OK, ale možná méně sytící")
    elif is_suitable and not can_cause_fatigue:
        print("⚠️  VAROVÁNÍ - Může způsobit problémy (nadýmání/chutě)")
    else:
        print("❌ NEDOPORUČENO - Obsahuje problematické složky")
    
    print("=" * 70)


def demo_meal_planning():
    """Ukázka plánování jídel s ohledem na zaznamenané preference."""
    
    print("\n" + "=" * 70)
    print("📅 PLÁNOVÁNÍ JÍDEL PRO PÁJU")
    print("=" * 70)
    
    # Získat doporučení pro strukturu jídel
    struktura = StrukturaJidel.ziskej_doporuceni_porci()
    print(f"\n⚠️  Problematické jídlo: {struktura['problematicke_jidlo']}")
    print(f"   Důvod: {struktura['duvod']}")
    print(f"   Preference: {struktura['preference']}")
    
    print("\n💡 Doporučení pro plánování:")
    for dop in struktura['doporuceni']:
        print(f"   • {dop}")
    
    # Hlad a energie
    hlad = HladAEnergie.ziskej_prehled()
    print(f"\n🧠 Nejvyšší hlad: {hlad['nejvyssi_hlad']}")
    print(f"   → Doporučení: Zaměřit se na vydatnější snídani")
    
    # Sytící jídla
    sytici = SyticiJidla.ziskej_prehled()
    print("\n🥣 Pro maximální sytost použít:")
    for jidlo in sytici['dobre_syti'][:3]:
        print(f"   ✓ {jidlo}")
    
    print(f"\n📝 Klíčové poznámky:")
    for poznamka in hlad['poznamky']:
        print(f"   • {poznamka}")


def main():
    """Hlavní demo."""
    
    print("\n╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "DEMO: ZAZNAMENANÉ ODPOVĚDI PÁJI (ČÁST 1)" + " " * 17 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # 1. Demo analýzy různých jídel
    print("\n\n📊 ČÁST 1: ANALÝZA JEDNOTLIVÝCH JÍDEL")
    print("=" * 70)
    
    test_meals = [
        "ovesná kaše s ovocem a jogurtem",
        "káva s mlékem",
        "kuřecí prsa s brokolicí",
        "pečené brambory",
        "čokoládový dezert",
        "luštěniny se semínky"
    ]
    
    for meal in test_meals:
        demo_meal_check(meal)
    
    # 2. Demo plánování jídel
    print("\n\n📋 ČÁST 2: PLÁNOVÁNÍ JÍDEL")
    demo_meal_planning()
    
    # 3. Varování o kávě
    print("\n\n☕ ČÁST 3: DŮLEŽITÉ UPOZORNĚNÍ O KÁVĚ")
    print("=" * 70)
    for upozorneni in ProblematickaJidla.UPOZORNENI_KAVA:
        print(f"⚠️  {upozorneni}")
    print("=" * 70)
    
    print("\n\n✅ Demo dokončeno!")
    print("\nVíce informací:")
    print("  • python osoby/osoba_2/preference.py - kompletní přehled preferencí")
    print("  • python test_paja_preferences.py - testy všech funkcí")
    print()


if __name__ == "__main__":
    main()
