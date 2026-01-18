#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: Integrace komplexního profilu s doporučovacím systémem

Tento skript ukazuje, jak použít nový KomplexniProfilPaji
společně s existujícími třídami pro generování konkrétních doporučení.
"""

from osoby.osoba_2.profil_komplexni import KomplexniProfilPaji
from osoby.osoba_2.preference import (
    PreferenceJidel,
    SyticiJidla,
    ProblematickaJidla,
    ReakceTela,
    HladAEnergie,
    StrukturaJidel
)


def demo_generovani_doporuceni():
    """Ukázka generování personalizovaných doporučení."""
    
    print("=" * 70)
    print("GENEROVÁNÍ PERSONALIZOVANÝCH DOPORUČENÍ PRO PÁJU")
    print("=" * 70)
    
    # Načíst komplexní profil
    profil = KomplexniProfilPaji()
    
    print("\n📋 ANALÝZA PROFILU")
    print("-" * 70)
    
    # Kritické časy
    casy = profil.get_kriticke_casy()
    print(f"\n⏰ Kritické časy:")
    print(f"  • Vstávání: {casy['rano']}")
    print(f"  • Hlad peak: {casy['kriticke_okno_hladu']}")
    print(f"  • Konec práce: {casy['konec_prace']}")
    print(f"  • Večeře: {casy['vecere']}")
    
    # Denní požadavky
    pozadavky = profil.get_denni_pozadavky()
    print(f"\n✅ Co jídelníček MUSÍ:")
    for pozadavek in pozadavky['jidelnicek_musi']:
        print(f"  • {pozadavek}")
    
    print(f"\n❌ Co jídlo NESMÍ:")
    for pozadavek in pozadavky['jidlo_nesmi']:
        print(f"  • {pozadavek}")
    
    # Hlavní rizika
    print(f"\n🚨 HLAVNÍ RIZIKA:")
    for i, riziko in enumerate(profil.rizika.rizika, 1):
        print(f"  {i}. {riziko}")
    
    print("\n" + "=" * 70)
    print("KONKRÉTNÍ JÍDELNÍ DOPORUČENÍ")
    print("=" * 70)
    
    # Doporučení na základě profilu
    doporuceni = profil.get_doporuceni_pro_planovani()
    
    # 1. SNÍDANĚ (Priorita 1)
    print("\n🌅 SNÍDANĚ (5:30-6:00)")
    print("-" * 70)
    priorita_rano = doporuceni['priorita_1_rano']
    print(f"Problém: {priorita_rano['duvod']}")
    print(f"Řešení: {priorita_rano['akce']}")
    print(f"\n✅ DOPORUČENÉ JÍDLO: {priorita_rano['priklad']}")
    
    # Ověřit, že je sytící
    if SyticiJidla.je_jidlo_sytici(priorita_rano['priklad']):
        print("   ✓ Sytící (vláknina + objem + jemná sladkost)")
    else:
        print("   ⚠️ Méně sytící - zvážit doplnění vlákniny")
    
    # Zkontrolovat reakce
    if not ReakceTela.muze_zpusobit_unavu(priorita_rano['priklad']):
        print("   ✓ Nezpůsobuje únavu")
    else:
        print("   ⚠️ Může způsobit únavu - pozor na velikost porce")
    
    print("\n💡 Příprava:")
    print("   • Připravit večer (kvůli časovému tlaku ráno)")
    print("   • Porce podle hladu (ráno je nejvyšší)")
    print("   • Nenaplnit se až po okraj (citlivost na objem)")
    
    # 2. ODPOLEDNÍ SVAČINA (Priorita 2)
    print("\n\n🍎 ODPOLEDNÍ SVAČINA (15:00-16:00)")
    print("-" * 70)
    priorita_okno = doporuceni['priorita_2_kriticke_okno']
    print(f"Problém: {priorita_okno['duvod']}")
    print(f"Řešení: {priorita_okno['akce']}")
    print(f"⚠️  Riziko: {priorita_okno['riziko']}")
    
    print("\n✅ DOPORUČENÉ JÍDLO:")
    print("   • Jogurt + ovoce (připravený v krabičce)")
    print("   • Luštěniny se semínky (meal prep)")
    print("   • Ovesné vločky s ořechy")
    
    print("\n❌ VYHÝBAT SE:")
    print("   • Káva (→ spouští chutě + pád energie)")
    print("   • Automat (→ sladké → výčitky)")
    print("   • Nic (→ přejedení u večeře)")
    
    # 3. OBĚD (Priorita 3)
    print("\n\n🍽️ OBĚD (12:30)")
    print("-" * 70)
    priorita_obed = doporuceni['priorita_3_obed']
    print(f"Problém: {priorita_obed['duvod']}")
    print(f"Řešení: {priorita_obed['akce']}")
    print(f"Vyhýbat se: {priorita_obed['vyhybat_se']}")
    
    print("\n💡 Strategie:")
    print("   • Použít menší talíř (optický trik)")
    print("   • Víc zeleniny, méně masa")
    print("   • Víc vlákniny (sytí bez objemu)")
    print("   • Jíst pomalu (20 min minimum)")
    
    # Test konkrétních jídel
    print("\n✅ Vhodná oběda:")
    testovaci_jidla = [
        "Luštěniny s cuketou a semínky",
        "Kuřecí + brokolice + malá porce",
        "Salát s vejci a avokádem"
    ]
    
    for jidlo in testovaci_jidla:
        vhodne = PreferenceJidel.je_jidlo_vhodne(jidlo)
        syti = SyticiJidla.je_jidlo_sytici(jidlo)
        problemy = ProblematickaJidla.je_jidlo_problematicke(jidlo)
        
        if vhodne and not problemy:
            status = "✓" if syti else "○"
            print(f"   {status} {jidlo}")
    
    # 4. MEAL PREP (Priorita 4)
    print("\n\n📦 MEAL PREP PLÁN")
    print("-" * 70)
    priorita_prep = doporuceni['priorita_4_meal_prep']
    print(f"Důvod: {priorita_prep['duvod']}")
    print(f"Podpora: {priorita_prep['podpora']}")
    
    print("\n💡 Nedělní rutina (90 min):")
    print("   1. Uvařit velkou porci luštěnin (30 min)")
    print("   2. Připravit kaši do krabiček (15 min)")
    print("   3. Nakrájet zeleninu (15 min)")
    print("   4. Uvařit vajíčka natvrdo (15 min)")
    print("   5. Rozdělit do krabiček (15 min)")
    print("\n   → Hotovo na 4 dny (snídaně + svačiny)")
    
    # 5. SUPLEMENTY (Priorita 5)
    print("\n\n💊 SUPLEMENTY")
    print("-" * 70)
    priorita_supl = doporuceni['priorita_5_suplementy']
    print(f"Problém: {priorita_supl['duvod']}")
    print(f"Řešení: {priorita_supl['akce']}")
    
    print("\n✅ Denní rutina:")
    print("   • 5:30 - Vstát, sklenice vody")
    print("   • 5:35 - Letrox (nalačno, 30 min před jídlem)")
    print("   • 5:36 - Vitamin D + Omega-3 + Magnesium")
    print("   • 6:00 - Snídaně")
    
    print("\n" + "=" * 70)
    print("TÝDENNÍ SHRNUTÍ")
    print("=" * 70)
    
    print("\n📅 PRACOVNÍ DEN")
    print("   5:30  Vstát, suplementy")
    print("   6:00  Snídaně (kaše+ovoce+jogurt, připraveno)")
    print("   10:00 Svačina (ovoce, krabička)")
    print("   12:30 Oběd (menší porce, víc vlákniny)")
    print("   15:30 Svačina (jogurt+ovoce, NE káva!)")
    print("   18:00 Večeře (lehká, sdílená s rodinou)")
    
    print("\n📅 VÍKEND")
    print("   Neděle: 90 min meal prep")
    print("   Sobota: Více času → připravit čerstvé jídlo")
    print("   Roman vaří → komunikace o velikosti porcí")
    
    print("\n🎯 KLÍČOVÉ BODY")
    print("   ✓ Ráno = nejvyšší hlad → vydatná snídaně")
    print("   ✓ 15-16h = kritické okno → připravená svačina")
    print("   ✓ Oběd = riziko přejedení → menší porce")
    print("   ✓ Káva = spouštěč → nahradit vodou/čajem")
    print("   ✓ Meal prep = záchrana → neděle 90 min")
    
    print("\n" + "=" * 70)


def demo_analyza_scenaru():
    """Analýza typického scénáře selhání a prevence."""
    
    print("\n\n" + "=" * 70)
    print("ANALÝZA SCÉNÁŘE SELHÁNÍ & PREVENCE")
    print("=" * 70)
    
    profil = KomplexniProfilPaji()
    
    print("\n🚨 TYPICKÝ SCÉNÁŘ SELHÁNÍ:")
    print(f"   {profil.hlad_chute.get_scenar_selhani()}")
    
    print("\n📊 ROZBOR KROK ZA KROKEM:")
    print("-" * 70)
    
    print("\n1️⃣ 'Jídlo mě neuspokojilo'")
    print("   Důvod: Málo vlákniny, moc tuku, příliš malá porce")
    print("   Prevence:")
    print("     • Jídla zaměřená na vlákninu + objem")
    print("     • Luštěniny, kaše, zelenina")
    print("     • NE tučná masná jídla")
    
    print("\n2️⃣ '→ kafe / automat'")
    print("   Důvod: Hledání rychlého řešení hladu/energie")
    print("   Prevence:")
    print("     • Mít připravenou svačinu v krabičce")
    print("     • Jogurt + ovoce v lednici")
    print("     • Varování: Káva = spouštěč, ne řešení!")
    
    print("\n3️⃣ '→ sladké'")
    print("   Důvod: Káva spustila chutě na sladké")
    print("   Prevence:")
    print("     • Vyhnout se kávě úplně (hlavně 15-16h)")
    print("     • Místo kávy: voda, bylinkový čaj")
    print("     • Pokud hlad: jídlo s vlákninou")
    
    print("\n4️⃣ '→ únava'")
    print("   Důvod: Glykemický výkyv po sladkém")
    print("   Prevence:")
    print("     • Kombinovat sacharidy + protein + vláknina")
    print("     • Nikdy sladké samostatně")
    print("     • Vyhnout se 'hodně sladkému'")
    
    print("\n5️⃣ '→ výčitky'")
    print("   Důvod: Pocit selhání, negativní spiral")
    print("   Prevence:")
    print("     • Rámec, ne disciplína")
    print("     • Jedna špatná volba ≠ selhání")
    print("     • Další jídlo = nová šance")
    
    print("\n💡 STRATEGIE 'ZÁCHRANNÉ BRZDY':")
    print("-" * 70)
    print("\n🔴 KDYŽ SE DĚJE KROK 1 (neuspokojivé jídlo):")
    print("   → Okamžitě sníst ještě něco s vlákninou")
    print("   → Např. jogurt + chia semínka")
    print("   → Radši víc jíst než riskovat scénář")
    
    print("\n🔴 KDYŽ SE DĚJE KROK 2 (chci ke kafe/automatu):")
    print("   → STOP! Zkontrolovat připravenou svačinu")
    print("   → Vypít sklenici vody")
    print("   → Počkat 10 minut")
    
    print("\n🔴 KDYŽ SE STALO (už jsi u sladkého):")
    print("   → Sníst jen trochu, ne celé")
    print("   → Vypít hodně vody")
    print("   → Příští jídlo: extra vláknina")
    print("   → ŽÁDNÉ výčitky, učit se z toho")


if __name__ == "__main__":
    demo_generovani_doporuceni()
    demo_analyza_scenaru()
    
    print("\n\n" + "=" * 70)
    print("✅ DEMO DOKONČENO")
    print("=" * 70)
    print("\nVíce informací:")
    print("  • python osoby/osoba_2/profil_komplexni.py")
    print("  • python osoby/osoba_2/preference.py")
    print("  • osoby/osoba_2/DOPLNUJICI_OTAZKY.md")
    print()
