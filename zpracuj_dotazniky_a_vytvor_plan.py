#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hlavní skript pro zpracování dotazníků všech osob a vytvoření komplexního plánu.

Tento skript:
1. Zpracuje dotazníky pro všechny osoby (Roman, Pája, Kubík)
2. Sestaví personalizovaná doporučení
3. Zváží potřeby pro meal prep (potraviny a nádoby)
4. Shrne nákupní plán
5. Vytvoří nákupní seznam do Globusu
6. Poskytne personalizovaná doporučení pro celou rodinu
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Přidat cesty pro importy
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from osoby.osoba_3.profil import DetskyyProfil


class RodinnyPlanSystem:
    """
    Systém pro komplexní plánování stravy a nákupů pro celou rodinu.
    """
    
    def __init__(self):
        self.roman_dotaznik = None
        self.paja_dotaznik = None
        self.kubik_profil = DetskyyProfil()
        self.meal_prep_plan = {}
        self.shopping_plan = {}
        self.output_file_path = None  # Uložíme cestu k výstupnímu souboru
        
    def nacti_dotazniky(self):
        """Načte existující vyplněné dotazníky nebo použije výchozí profily."""
        print("=" * 80)
        print("📋 KROK 1: Načítání profilů osob")
        print("=" * 80)
        print()
        
        # Pro zjednodušení použijeme profily, které jsou definované v README
        # Můžeme později načítat z JSON, pokud existují
        
        # Roman - základní profil
        print("👤 Roman (Romča):")
        print("   ✅ Profil načten z README.md")
        print("   📊 Aktuální váha: 134.2 kg, Cíl: 95 kg")
        print("   🎯 Denní cíl: 2000 kcal | 140g P / 70g C / 129g F")
        print("   📝 Meal prep: Neděle 3 hodiny, batch cooking")
        print("   🛒 Rozpočet: 2500-3000 Kč/týden (rodina)")
        self.roman_dotaznik = {
            "jmeno": "Roman",
            "vaha": 134.2,
            "cilova_vaha": 95.0,
            "kalorie_den": 2000,
            "bilkoviny": 140,
            "sacharidy": 70,
            "tuky": 129,
            "meal_prep_den": "neděle",
            "meal_prep_cas": 180,  # 3 hodiny
            "rozpocet_tyden": 2500
        }
        
        # Pája - základní profil
        print("\n👤 Pája:")
        print("   ✅ Profil načten z README.md")
        print("   📊 Aktuální váha: 77.3 kg, Cíl: 57 kg")
        print("   🎯 Denní cíl: 1508 kcal | 92g P / 60g C")
        print("   📝 Pomáhá: Úklid během meal prepu")
        self.paja_dotaznik = {
            "jmeno": "Pája",
            "vaha": 77.3,
            "cilova_vaha": 57.0,
            "kalorie_den": 1508,
            "bilkoviny": 92,
            "sacharidy": 60,
            "pomaha_s_meal_prep": True
        }
        
        # Kubík - profil je už načtený v __init__
        print("\n👶 Kubík:")
        print("   ✅ Profil načten (předškolní dítě)")
        print(f"   📊 Denní potřeba: {self.kubik_profil.cil_kalorie} kcal, {self.kubik_profil.cil_bilkoviny}g bílkovin")
        print(f"   🎯 Důraz na vitamin A (zrak) a vlákninu (trávení)")
        print()
        
    def sestavit_doporuceni(self):
        """Sestaví personalizovaná doporučení pro každou osobu."""
        print("=" * 80)
        print("🎯 KROK 2: Sestavení personalizovaných doporučení")
        print("=" * 80)
        print()
        
        # Roman - doporučení založené na profilu
        print("👤 ROMAN - Doporučení:")
        print("-" * 80)
        print("1. MEAL PREP: Neděle 14:00-17:00 - 3 hodiny batch cooking")
        print("   • Připrav 14 obědů + 14 večeří na celý týden")
        print("   • Použij tlakový hrnec, troubu a airfryer současně")
        print("   • Vakuuj jídla pro delší trvanlivost")
        print()
        print("2. PROTEINY FIRST: Začni každé jídlo bílkovinou")
        print("   • Cíl: 140g bílkovin denně (32% energie)")
        print("   • Kuřecí prsa, vejce, tvaroh, řecký jogurt")
        print()
        print("3. LOW-CARB: Maximálně 70g sacharidů denně")
        print("   • Eliminuj těstoviny, chléb, brambory, rýži")
        print("   • Zaměř se na nízko-sacharidovou zeleninu")
        print()
        print("4. NÁKUPY: Sobota ráno - kontrola slev na Kupi.cz")
        print("   • Nakup ve 2-3 obchodech podle akcí")
        print("   • Rozpočet: 2500 Kč/týden pro rodinu")
        print()
        print("5. JEDNODUCHOST: Preferuj recepty s 3-5 ingrediencemi")
        print("   • Opakuj osvědčené recepty")
        print("   • Udržitelnost > dokonalost")
        print()
        
        # Pája - doporučení
        print("👤 PÁJA - Doporučení:")
        print("-" * 80)
        print("1. KALORICKÝ DEFICIT: 1508 kcal denně pro hubnutí")
        print("   • Cíl: 77.3 kg → 57 kg (20 kg za 6-12 měsíců)")
        print("   • Tempo: 0.5-1 kg/týden")
        print()
        print("2. PROTEINY: 92g denně pro udržení svalové hmoty")
        print("   • Priorita při každém jídle")
        print("   • Tvaroh, jogurt, kuřecí maso")
        print()
        print("3. EMOČNÍ STRAVOVÁNÍ: Připravené zdravé svačiny")
        print("   • Při stresu mít po ruce zeleninu, ořechy")
        print("   • Žvýkačka jako náhrada")
        print()
        print("4. HORMONÁLNÍ PODPORA: Kvalitní tuky a omega-3")
        print("   • Podpora libida a hormonů")
        print("   • Avokádo, losos, ořechy, olivový olej")
        print()
        print("5. SPOLUPRÁCE: Úklid během meal prepu místo vaření")
        print("   • Společné hubnutí s Romanem = motivace")
        print()
        
        # Kubík - zdravotní priority
        print("👶 KUBÍK - Zdravotní priority:")
        print("-" * 80)
        for poznamka in self.kubik_profil.zdravotni_poznamky[:5]:
            print(f"• {poznamka}")
        print()
        print("DOPORUČENÍ PRO KUBÍKA:")
        print("  • Vitamin A: Mrkev, dýně, sladké brambory, špenát")
        print("  • Omega-3: Losos, makrela (1-2x týdně)")
        print("  • Vláknina: Ovoce, zelenina, celozrnné pečivo")
        print("  • Voda: Minimálně 1.3l denně (důležité!)")
        print()
        
    def zvazit_meal_prep_potreby(self):
        """Zváží potřeby pro meal prep - potraviny a nádoby."""
        print("=" * 80)
        print("🍱 KROK 3: Plánování meal prep potřeb")
        print("=" * 80)
        print()
        
        # Výpočet potřeb na týden - definice konstant pro přehlednost
        ROMAN_KALORIE_DEN = 2000
        PAJA_KALORIE_DEN = 1508
        KUBIK_KALORIE_DEN = 1400
        
        DNI_V_TYDNU = 7
        
        # Kubík jí 2 jídla doma ve všední dny (snídaně + večeře)
        # O víkendu všechna jídla doma
        KUBIK_JIDLA_DOMA_DEN_VSEDNI = 2  # snídaně + večeře
        KUBIK_JIDLA_DOMA_DEN_VIKEND = 5  # všechna jídla
        DNI_VSEDNI = 5
        DNI_VIKEND = 2
        
        kubik_jidla_doma_tyden = (KUBIK_JIDLA_DOMA_DEN_VSEDNI * DNI_VSEDNI) + (KUBIK_JIDLA_DOMA_DEN_VIKEND * DNI_VIKEND)
        
        ROMAN_JIDLA_DEN = 6  # 6 jídel denně
        PAJA_JIDLA_DEN = 5   # 5 jídel denně
        
        roman_jidla_tyden = ROMAN_JIDLA_DEN * DNI_V_TYDNU
        paja_jidla_tyden = PAJA_JIDLA_DEN * DNI_V_TYDNU
        
        print("📊 NUTRIČNÍ POTŘEBY (týdenní):")
        print("-" * 80)
        print(f"Roman:  {ROMAN_KALORIE_DEN * DNI_V_TYDNU:,} kcal/týden | {roman_jidla_tyden} jídel")
        print(f"Pája:   {PAJA_KALORIE_DEN * DNI_V_TYDNU:,} kcal/týden | {paja_jidla_tyden} jídel")
        print(f"Kubík:  {KUBIK_KALORIE_DEN * DNI_V_TYDNU:,} kcal/týden | {kubik_jidla_doma_tyden} jídel doma")
        celkem_kalorie = (ROMAN_KALORIE_DEN + PAJA_KALORIE_DEN + KUBIK_KALORIE_DEN) * DNI_V_TYDNU
        print(f"CELKEM: {celkem_kalorie:,} kcal/týden")
        print()
        
        print("🥘 POTŘEBNÉ POTRAVINY (odhad na týden):")
        print("-" * 80)
        print("PROTEINY:")
        print("  • Kuřecí prsa: 2.5 kg (hlavní zdroj pro Romana a Páju)")
        print("  • Mleté maso: 1.5 kg (obědy, večeře)")
        print("  • Ryby (losos/makrela): 800g (2-3x týdně)")
        print("  • Vejce: 30 ks (snídaně, svačiny)")
        print("  • Tvaroh: 1.5 kg (snídaně, dezerty)")
        print("  • Řecký jogurt: 1 kg (snídaně Páji)")
        print("  • Sýry (eidam, gouda): 600g")
        print()
        
        print("ZELENINA (low-carb pro dospělé, rozmanitá pro Kubíka):")
        print("  • Brokolice: 2 kg")
        print("  • Špenát: 1 kg")
        print("  • Paprika: 1.5 kg")
        print("  • Rajčata: 1 kg")
        print("  • Okurky: 1 kg")
        print("  • Salátová zelenina: 500g")
        print("  • Mrkev (vitamin A pro Kubíka): 1 kg")
        print()
        
        print("PRO KUBÍKA (specifické potřeby):")
        print("  • Ovoce (beta-karoten): banány, pomeranče, mango")
        print("  • Rýže/těstoviny: 500g (přílohy)")
        print("  • Celozrnný chléb: 1 bochník")
        print("  • Jogurty/kefír: 1l")
        print("  • Sýr (oblíbený): 300g")
        print()
        
        print("TUKY A DALŠÍ:")
        print("  • Olivový olej: 500ml")
        print("  • Avokádo: 5 ks")
        print("  • Ořechy (mandle, vlašské): 500g")
        print("  • Semínka (chia, lněná): 200g")
        print()
        
        print("🥡 POTŘEBNÉ NÁDOBY A VYBAVENÍ:")
        print("-" * 80)
        print("MEAL PREP KRABIČKY:")
        print("  • Velké (obědy): 14 ks (7 dní x 2 osoby)")
        print("  • Střední (večeře): 14 ks")
        print("  • Malé (svačiny): 20 ks")
        print("  • Skleničky (chia pudding, jogurt): 10 ks")
        print()
        
        print("VAKUOVACÍ SÁČKY:")
        print("  • Pro maso (před vařením): 10 ks")
        print("  • Pro hotová jídla (mražení): 20 ks")
        print()
        
        print("DALŠÍ VYBAVENÍ:")
        print("  • Pečicí plechy: 2 ks (batch cooking)")
        print("  • Velké hrnce: 2 ks (tlakový hrnec + klasický)")
        print("  • Airfryer (pokud máte)")
        print("  • Mixér (smoothie, polévky)")
        print("  • Kuchyňská váha (přesné dávkování)")
        print()
        
        self.meal_prep_plan = {
            "kalorie_tyden": celkem_kalorie,
            "jidel_celkem": roman_jidla_tyden + paja_jidla_tyden + kubik_jidla_doma_tyden,
            "krabicek_potreba": 14 + 14 + 20,  # velké obědy + střední večeře + malé svačiny
            "cas_pripravy": "3-4 hodiny (neděle)"
        }
        
    def shrnout_nakupni_plan(self):
        """Shrne nákupní plán s odhadem cen a strategií."""
        print("=" * 80)
        print("🛒 KROK 4: Shrnutí nákupního plánu")
        print("=" * 80)
        print()
        
        # Odhad cen podle aktuálních trhových cen v ČR
        plan = {
            "PROTEINY": {
                "položky": [
                    ("Kuřecí prsa (2.5 kg)", 400, "Lidl/Kaufland"),
                    ("Mleté maso (1.5 kg)", 200, "Penny"),
                    ("Losos/makrela (800g)", 250, "Makro/Albert"),
                    ("Vejce (30 ks)", 120, "Lidl"),
                    ("Tvaroh (1.5 kg)", 150, "Kaufland"),
                    ("Řecký jogurt (1 kg)", 100, "Lidl"),
                    ("Sýr (600g)", 150, "Kaufland"),
                ],
                "celkem": 1370
            },
            "ZELENINA": {
                "položky": [
                    ("Brokolice (2 kg)", 120, "Kaufland"),
                    ("Špenát mražený (1 kg)", 80, "Lidl"),
                    ("Paprika (1.5 kg)", 120, "Albert"),
                    ("Rajčata (1 kg)", 70, "Kaufland"),
                    ("Okurky (1 kg)", 50, "Penny"),
                    ("Salát (500g)", 40, "Lidl"),
                    ("Mrkev (1 kg)", 30, "Kaufland"),
                ],
                "celkem": 510
            },
            "KUBÍK_SPECIFIKA": {
                "položky": [
                    ("Ovoce mix", 150, "Kaufland"),
                    ("Rýže/těstoviny (500g)", 50, "Lidl"),
                    ("Celozrnný chléb", 40, "Pekárna"),
                    ("Jogurty dětské (1l)", 60, "Kaufland"),
                    ("Sýr pro děti (300g)", 70, "Lidl"),
                ],
                "celkem": 370
            },
            "TUKY_A_DALŠÍ": {
                "položky": [
                    ("Olivový olej (500ml)", 130, "Kaufland"),
                    ("Avokádo (5 ks)", 100, "Albert"),
                    ("Ořechy (500g)", 150, "Lidl"),
                    ("Semínka (200g)", 80, "DM/Rossmann"),
                ],
                "celkem": 460
            }
        }
        
        celkova_cena = sum(kategorie["celkem"] for kategorie in plan.values())
        
        for kategorie, data in plan.items():
            print(f"{kategorie} ({data['celkem']} Kč):")
            print("-" * 80)
            for polozka, cena, obchod in data["položky"]:
                print(f"  • {polozka:40} {cena:4} Kč  [{obchod}]")
            print()
        
        print("=" * 80)
        print(f"💰 CELKOVÁ ODHADOVANÁ CENA: {celkova_cena} Kč/týden")
        print("=" * 80)
        print()
        
        # Rozpočet podle dotazníku Romana
        rozpocet = 2500  # Z dotazníku: 2500-3000 Kč
        if celkova_cena <= rozpocet:
            print(f"✅ Plán je v rámci rozpočtu! (Rozpočet: {rozpocet} Kč, Plán: {celkova_cena} Kč)")
            print(f"   Úspora: {rozpocet - celkova_cena} Kč")
        else:
            print(f"⚠️  Překročení rozpočtu! (Rozpočet: {rozpocet} Kč, Plán: {celkova_cena} Kč)")
            print(f"   Překročení: {celkova_cena - rozpocet} Kč")
        print()
        
        print("📍 STRATEGIE NÁKUPU:")
        print("-" * 80)
        print("1. SOBOTA ráno - Kontrola letáků na Kupi.cz")
        print("2. SOBOTA dopoledne - Velký nákup:")
        print("   • Lidl (proteiny, vajíčka, jogurty)")
        print("   • Kaufland (zelenina, sýry, maso)")
        print("   • Penny (mleté maso, doplňky)")
        print("3. PODLE POTŘEBY - Makro/Albert (ryby, speciality)")
        print()
        
        self.shopping_plan = {
            "celkova_cena": celkova_cena,
            "plan": plan,
            "rozpocet": rozpocet,
            "v_rozpoctu": celkova_cena <= rozpocet
        }
        
    def vytvorit_seznam_globus(self):
        """Vytvoří specifický nákupní seznam pro Globus."""
        print("=" * 80)
        print("🏪 KROK 5: Nákupní seznam - GLOBUS")
        print("=" * 80)
        print()
        
        print("📝 NÁKUPNÍ SEZNAM PRO GLOBUS")
        print("   (Valašské Meziříčí / nejbližší Globus)")
        print()
        print("=" * 80)
        
        globus_seznam = {
            "MASO A RYBY": [
                "☐ Kuřecí prsa čerstvé - 2.5 kg",
                "☐ Mleté hovězí/vepřové - 1.5 kg",
                "☐ Losos filety - 800g",
                "☐ Kuřecí stehna (pokud sleva) - 1 kg",
            ],
            "MLÉČNÉ VÝROBKY": [
                "☐ Vejce čerstvá - 30 ks (2 kartony)",
                "☐ Tvaroh polotučný - 1.5 kg",
                "☐ Řecký jogurt Globus Premium - 1 kg",
                "☐ Sýr eidam - 600g",
                "☐ Máslo - 250g",
            ],
            "ZELENINA": [
                "☐ Brokolice čerstvá/mražená - 2 kg",
                "☐ Špenát mražený - 1 kg",
                "☐ Paprika červená/žlutá - 1.5 kg",
                "☐ Rajčata - 1 kg",
                "☐ Okurky hadovky - 3 ks",
                "☐ Salátový mix - 500g",
                "☐ Mrkev - 1 kg",
            ],
            "PRO KUBÍKA": [
                "☐ Banány - 1 kg",
                "☐ Pomeranče - 1 kg",
                "☐ Rýže jasmínová - 500g",
                "☐ Těstoviny penne - 500g",
                "☐ Chléb celozrnný - 1 ks",
                "☐ Jogurty Danone dětské - 8 ks",
                "☐ Sýr bloček Globík - 300g",
            ],
            "TUKY A OŘECHY": [
                "☐ Olivový olej extra panenský - 500ml",
                "☐ Avokádo - 5 ks",
                "☐ Mandle natural - 250g",
                "☐ Vlašské ořechy - 250g",
                "☐ Semínka chia - 200g",
            ],
            "KOŘENÍ A DOPLŇKY": [
                "☐ Sůl himálajská",
                "☐ Pepř černý mletý",
                "☐ Česnek čerstvý - 3 hlavičky",
                "☐ Citróny - 4 ks",
                "☐ Zázvor čerstvý - 100g",
            ],
            "DOPLŇKY STRAVY": [
                "☐ Omega-3 kapsle",
                "☐ Vitamin D3",
                "☐ Multivitamin (volitelné)",
            ]
        }
        
        for kategorie, polozky in globus_seznam.items():
            print(f"\n{kategorie}:")
            print("-" * 80)
            for polozka in polozky:
                print(f"  {polozka}")
        
        print()
        print("=" * 80)
        print("💡 TIPY PRO NÁKUP V GLOBUSU:")
        print("=" * 80)
        print("• Nakupujte ve čtvrtek/pátek - čerstvé maso")
        print("• Využijte Globus kartu - sleva 3%")
        print("• Pekárna Globus - čerstvý celozrnný chléb")
        print("• Mrazené zeleniny - často lepší cena než čerstvé")
        print("• Velké balení ořechů - výhodnější cena/kg")
        print()
        
        # Uložit seznam do souboru
        import tempfile
        
        # Použít tempfile pro cross-platform kompatibilitu
        output_dir = tempfile.gettempdir()
        output_path = os.path.join(output_dir, "nakupni_seznam_globus.txt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("NÁKUPNÍ SEZNAM - GLOBUS\n")
            f.write(f"Datum vytvoření: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write("=" * 80 + "\n\n")
            
            for kategorie, polozky in globus_seznam.items():
                f.write(f"{kategorie}:\n")
                f.write("-" * 80 + "\n")
                for polozka in polozky:
                    f.write(f"{polozka}\n")
                f.write("\n")
        
        print(f"💾 Seznam uložen do: {output_path}")
        print()
        
        # Uložit cestu pro použití v závěrečné zprávě
        self.output_file_path = output_path
        
    def shrnout_personalizovana_doporuceni(self):
        """Shrne personalizovaná doporučení pro celou rodinu."""
        print("=" * 80)
        print("🎯 KROK 6: Personalizovaná doporučení pro rodinu")
        print("=" * 80)
        print()
        
        print("👨‍👩‍👦 KOMPLEXNÍ RODINNÝ PLÁN:")
        print("=" * 80)
        print()
        
        print("📅 TÝDENNÍ HARMONOGRAM:")
        print("-" * 80)
        print()
        print("SOBOTA:")
        print("  09:00-10:00 - Kontrola slev na Kupi.cz")
        print("  10:00-12:00 - Velký nákup (Lidl, Kaufland, případně Globus)")
        print("  14:00-15:00 - Plánování jídelníčku na další týden")
        print()
        print("NEDĚLE:")
        print("  09:00-12:00 - VELKÝ MEAL PREP (3 hodiny)")
        print("    • Roman vaří, Pája uklízí a pomáhá")
        print("    • Batch cooking: pečení, tlakový hrnec, airfryer")
        print("    • Příprava 14 obědů + 14 večeří + 20 svačin")
        print("    • Vakuování a organizace do lednice/mrazáku")
        print()
        print("PONDĚLÍ-PÁTEK:")
        print("  06:00-06:30 - Příprava snídaní (10 min)")
        print("  12:00-12:30 - Obědy z meal prep krabiček")
        print("  18:00-18:30 - Večeře (ohřát + čerstvá zelenina)")
        print()
        
        print("\n🎯 INDIVIDUÁLNÍ DOPORUČENÍ:")
        print("=" * 80)
        print()
        
        print("👤 ROMAN (134.2 kg → cíl 95 kg):")
        print("-" * 80)
        print("• Denní příjem: 2000 kcal | 140g P / 70g C / 129g F")
        print("• Strategie: Protein-first, keto/low-carb")
        print("• Důraz na: Batch cooking, jednoduché recepty")
        print("• Meal prep: Neděle odpoledne 3 hodiny")
        print("• Hlavní výzva: Udržet pravidelnost")
        print("• Podpora: Nerušený prostor, čistá kuchyně")
        print()
        
        print("👤 PÁJA (77.3 kg → cíl 57 kg):")
        print("-" * 80)
        print("• Denní příjem: 1508 kcal | 92g P / 60g C / tuky podle potřeby")
        print("• Strategie: Low-carb s hormonální podporou")
        print("• Důraz na: Jednoduché recepty, příprava doma")
        print("• Časová optimalizace: Pomoc s úklidem místo vaření")
        print("• Emoční faktory: Připravené zdravé svačiny proti stresu")
        print("• Podpora: Hubnutí společně s Romanem")
        print()
        
        print("👶 KUBÍK (4.5 let, 17 kg):")
        print("-" * 80)
        print("• Denní příjem: 1400 kcal | 19g P / 130g C / 47g F")
        print("• Priority: Vitamin A (zrak), vláknina (zácpa), omega-3")
        print("• Jídla doma: Snídaně + večeře (všední dny), vše (víkend)")
        print("• Oblíbené: Sýr, mrkev, fíky")
        print("• Specifika: Vyšší podíl sacharidů (přílohy), ovoce")
        print("• Důraz: Oranžová a zelená zelenina pro zrak")
        print()
        
        print("\n💡 KLÍČOVÁ DOPORUČENÍ PRO ÚSPĚCH:")
        print("=" * 80)
        print()
        print("1. PLÁNOVÁNÍ:")
        print("   • Každou sobotu kontrola slev na Kupi.cz")
        print("   • Nákupní seznam podle aktuálních akcí")
        print("   • Předvařit na celý týden = méně stresu")
        print()
        print("2. MEAL PREP:")
        print("   • Neděle = svatý čas na vaření (3 hodiny)")
        print("   • Batch cooking - více jídel najednou")
        print("   • Vakuování pro delší trvanlivost")
        print("   • Organizace: lednice (3-4 dny) + mrazák (zbytek)")
        print()
        print("3. RODINNÁ SPOLUPRÁCE:")
        print("   • Roman vaří, Pája uklízí")
        print("   • Sdílená jídla kde možno (úspora času)")
        print("   • Kubík: přizpůsobené porce + přílohy")
        print()
        print("4. UDRŽITELNOST:")
        print("   • Jednoduché recepty (3-5 ingrediencí)")
        print("   • Opakování osvědčených jídel")
        print("   • Flexibilita při nákupu (slevy)")
        print("   • Pravidelnost > dokonalost")
        print()
        
        print("\n🍽️  UKÁZKOVÝ TÝDENNÍ JÍDELNÍČEK:")
        print("=" * 80)
        print()
        print("OBĚDY (Roman + Pája):")
        print("  • Pondělí: Pečená kuřecí prsa + brokolice + olivový olej")
        print("  • Úterý: Mleté maso s rajčaty + špenát")
        print("  • Středa: Losos + zelenina mix")
        print("  • Čtvrtek: Kuřecí prsa + paprika + cuketa")
        print("  • Pátek: Hovězí mleté + salát")
        print("  • Víkend: Čerstvě vařené podle nálady")
        print()
        print("VEČEŘE (celá rodina):")
        print("  • Proteiny + zelenina pro rodiče")
        print("  • + Příloha pro Kubíka (rýže/těstoviny/brambory)")
        print("  • Jednoduché, rychlé ohřátí")
        print()
        
    def generovat_ai_prompt_templates(self):
        """Vygeneruje prompt templates pro AI generování jídelníčků a jídel."""
        print("=" * 80)
        print("🤖 KROK 7: Generování AI Prompt Templates")
        print("=" * 80)
        print()
        
        # Připravíme 3 typy prompt templates:
        # 1. Template pro generování týdenního jídelníčku
        # 2. Template pro generování jednotlivých receptů
        # 3. Template pro generování meal prep plánu
        
        templates = {}
        
        # Template 1: Generování týdenního jídelníčku
        templates['jidelnicek'] = self._vytvorit_jidelnicek_template()
        
        # Template 2: Generování receptů
        templates['recepty'] = self._vytvorit_recepty_template()
        
        # Template 3: Generování meal prep plánu
        templates['meal_prep'] = self._vytvorit_meal_prep_template()
        
        # Uložit templates do souboru
        import tempfile
        output_dir = tempfile.gettempdir()
        templates_path = os.path.join(output_dir, "ai_prompt_templates.txt")
        
        with open(templates_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("AI PROMPT TEMPLATES - FOODLER MEAL PLANNING SYSTEM\n")
            f.write(f"Vygenerováno: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write("=" * 80 + "\n\n")
            
            for template_name, template_content in templates.items():
                f.write(f"\n{'=' * 80}\n")
                f.write(f"TEMPLATE: {template_name.upper()}\n")
                f.write(f"{'=' * 80}\n\n")
                f.write(template_content)
                f.write("\n\n")
        
        print("✅ AI Prompt Templates vytvořeny:")
        print()
        print("1. 📅 TEMPLATE PRO TÝDENNÍ JÍDELNÍČEK")
        print("   - Personalizovaný pro každého člena rodiny")
        print("   - Zahrnuje nutriční cíle a preference")
        print()
        print("2. 🍳 TEMPLATE PRO GENEROVÁNÍ RECEPTŮ")
        print("   - Keto/low-carb zaměření")
        print("   - Jednoduché recepty (3-5 ingrediencí)")
        print()
        print("3. 📦 TEMPLATE PRO MEAL PREP PLÁN")
        print("   - Batch cooking strategie")
        print("   - Optimalizace pro 3 hodiny přípravy")
        print()
        print(f"💾 Uloženo do: {templates_path}")
        print()
        
        # Zobrazit náhled prvního template
        print("=" * 80)
        print("📋 NÁHLED - Template pro týdenní jídelníček:")
        print("=" * 80)
        print()
        # Zobrazit prvních 30 řádků
        lines = templates['jidelnicek'].split('\n')[:30]
        for line in lines:
            print(line)
        if len(templates['jidelnicek'].split('\n')) > 30:
            print("\n... (zkráceno, úplný obsah v souboru)")
        print()
        
        return templates_path
    
    def _vytvorit_jidelnicek_template(self):
        """Vytvoří prompt template pro generování týdenního jídelníčku."""
        template = f"""# PROMPT TEMPLATE: Generování týdenního jídelníčku

## Kontext

Jsi expert na výživu a keto/low-carb dietu. Tvým úkolem je vytvořit týdenní jídelníček pro českou rodinu se specifickými výživovými potřebami.

## Rodinné profily

### Roman (34 let, muž)
- **Aktuální váha**: {self.roman_dotaznik['vaha']} kg
- **Cílová váha**: {self.roman_dotaznik['cilova_vaha']} kg
- **Denní kalorický cíl**: {self.roman_dotaznik['kalorie_den']} kcal
- **Makra**: {self.roman_dotaznik['bilkoviny']}g bílkovin / {self.roman_dotaznik['sacharidy']}g sacharidů / {self.roman_dotaznik['tuky']}g tuků
- **Dietní přístup**: Protein-first, keto/low-carb
- **Počet jídel denně**: 6 (snídaně, svačina, oběd, svačina, večeře, druhá večeře)

### Pája (žena)
- **Aktuální váha**: {self.paja_dotaznik['vaha']} kg
- **Cílová váha**: {self.paja_dotaznik['cilova_vaha']} kg
- **Denní kalorický cíl**: {self.paja_dotaznik['kalorie_den']} kcal
- **Makra**: {self.paja_dotaznik['bilkoviny']}g bílkovin / {self.paja_dotaznik['sacharidy']}g sacharidů
- **Dietní přístup**: Low-carb s hormonální podporou
- **Počet jídel denně**: 5 (snídaně, svačina, oběd, svačina, večeře)
- **Speciální požadavky**: Podpora libida (avokádo, omega-3, kvalitní tuky)

### Kubík (4.5 let, chlapec)
- **Věk**: 4.5 let
- **Váha**: {self.kubik_profil.vaha} kg
- **Denní kalorický cíl**: {self.kubik_profil.cil_kalorie} kcal
- **Makra**: {self.kubik_profil.cil_bilkoviny}g bílkovin / {self.kubik_profil.cil_sacharidy}g sacharidů / {self.kubik_profil.cil_tuky}g tuků
- **Zdravotní priority**: Vitamin A (zrak - brýle 4 dioptrie), vláknina (problémy s trávením), omega-3
- **Jídla doma**: Snídaně + večeře (všední dny), všechna jídla (víkend)
- **Oblíbené**: Sýr, mrkev, fíky

## Týdenní rozpočet

**Celkem**: 2710 Kč/týden
- Proteiny: 1370 Kč
- Zelenina: 510 Kč
- Pro Kubíka: 370 Kč
- Tuky a další: 460 Kč

## Preference a omezení

### Co ZAHRNOUT:
- **High-protein zdroje**: Kuřecí prsa, krůtí maso, vejce, tvaroh, řecký jogurt, losos
- **Low-carb zelenina**: Brokolice, špenát, paprika, salát, okurky
- **Zdravé tuky**: Olivový olej, avokádo, ořechy, semínka
- **Pro Kubíka**: Ovoce (vitamin A), celozrnné pečivo, rýže/těstoviny jako přílohy

### Co VYNECHAT:
- Cukr a sladkosti (kromě Kubíka)
- Bílé pečivo, těstoviny, rýže pro dospělé
- Brambory pro dospělé
- Cuketu (Roman nemá rád slizkou konzistenci)

### Styl přípravy:
- **Jednoduché recepty**: 3-5 ingrediencí
- **Batch cooking**: Meal prep 1x týdně (neděle)
- **Metody**: Pečení na plechu, tlakový hrnec, dušení
- **Vakuování**: Pro delší trvanlivost

## Úkol

Vytvoř týdenní jídelníček (pondělí-neděle) s následující strukturou:

### Pro každý den specifikuj:

**ROMAN** (6 jídel):
1. Snídaně (370 kcal)
2. Dopolední svačina (370 kcal)
3. Oběd (370 kcal)
4. Odpolední svačina (370 kcal)
5. Večeře (370 kcal)
6. Druhá večeře (158 kcal)

**PÁJA** (5 jídel):
1. Snídaně (~300 kcal)
2. Dopolední svačina (~300 kcal)
3. Oběd (~300 kcal)
4. Odpolední svačina (~300 kcal)
5. Večeře (~300 kcal)

**KUBÍK** (jídla doma):
- Všední dny: Snídaně + večeře
- Víkend: Všechna jídla

### Formát výstupu:

Pro každý den uveď:
- Název jídla
- Hlavní ingredience
- Přibližné makra (P/C/F)
- Kalorie
- Poznámka (sdílené s rodinou / speciální pro osobu)

### Příklad výstupu:

**PONDĚLÍ**

ROMAN - Snídaně (370 kcal):
- Omeleta se špenátem a sýrem
- Ingredience: 3 vejce, 50g špenátu, 30g sýru
- Makra: 28g P / 3g C / 26g F
- Poznámka: Rychlá příprava, vysoký protein

[... pokračuj pro všechna jídla a všechny dny ...]

## Důležité zásady:

1. **Protein first**: Každé jídlo začíná bílkovinou
2. **Varieta**: Neopakuj stejné jídlo více než 2x týdně
3. **Meal prep friendly**: Minimálně 4 jídla by měla být vhodná k předpřipravení
4. **Sdílení**: Kde možno, navrhni jídla, která mohou sdílet (úprava porcí)
5. **Kubík**: Vždy zahrň zdroje vitaminu A (mrkev, dýně, sladké brambory)

Začni generovat jídelníček!"""
        
        return template
    
    def _vytvorit_recepty_template(self):
        """Vytvoří prompt template pro generování receptů."""
        template = f"""# PROMPT TEMPLATE: Generování keto/low-carb receptů

## Kontext

Jsi kuchař specializující se na keto a low-carb recepty vhodné pro českou kuchyni. Tvým úkolem je vytvořit jednoduché recepty pro meal prep.

## Cílová skupina

- **Dospělí**: Keto/low-carb dieta (max {self.roman_dotaznik['sacharidy']}g sacharidů denně)
- **Dítě**: Normální dětská strava s důrazem na vitamin A a vlákninu
- **Časové omezení**: Meal prep 3 hodiny (neděle)
- **Úroveň vaření**: Pokročilý, ale preferuje jednoduché recepty

## Dostupné vybavení

- Tlakový hrnec
- Trouba
- Wok
- Vakuovačka
- Mixér
- Standardní hrnce a pánve

## Požadavky na recepty

### MUST HAVE:
- ✅ Max 5 ingrediencí (kromě koření)
- ✅ Příprava: Max 30 minut aktivního času
- ✅ Vhodné k meal prepu (vydrží 5-7 dní)
- ✅ Vysoký obsah bílkovin (min 25g na porci)
- ✅ Nízké sacharidy (max 15g na porci pro dospělé)
- ✅ Czech-friendly ingredience (dostupné v běžných obchodech)

### PREFEROVANÉ:
- Batch cooking (velké množství najednou)
- Vakuovatelné
- Mrazitelné
- Jednoduché ohřátí

### VYHNĚTE SE:
- Složité techniky (sous-vide, fermentace)
- Exotické ingredience
- Cuketě (slizká textura)
- Cukru a umělým sladidlům

## Kategorie receptů

Vytvoř recepty pro následující kategorie:

1. **SNÍDANĚ** (vysoký protein)
   - Vejce, tvaroh, řecký jogurt
   - Chia pudding
   - Protein smoothie

2. **OBĚDY** (hlavní jídla)
   - Kuřecí prsa (různé způsoby přípravy)
   - Mleté maso s rajčaty
   - Losos se zeleninou

3. **VEČEŘE** (lehčí, sdílené s rodinou)
   - Proteiny + zelenina
   - Příloha separátně pro Kubíka

4. **SVAČINY** (quick & easy)
   - Tvaroh s ořechy
   - Vejce natvrdo
   - Zelenina s dipem

## Formát receptu

Pro každý recept uveď:

**Název receptu**

**Kategorie**: [Snídaně/Oběd/Večeře/Svačina]

**Porce**: [počet] (specifikuj pro koho)

**Čas přípravy**: [X] minut aktivně + [Y] minut vaření

**Nutriční hodnoty (na porci)**:
- Kalorie: [X] kcal
- Bílkoviny: [X]g
- Sacharidy: [X]g
- Tuky: [X]g

**Ingredience**:
1. [množství] [ingredience]
2. [...]

**Postup**:
1. [krok]
2. [...]

**Meal prep tipy**:
- Jak skladovat: [lednice/mrazák/vakuovat]
- Trvanlivost: [X] dní
- Jak ohřát: [mikrovlnka/trouba/studené]

**Variace**:
- [alternativní ingredience nebo úpravy]

## Příklad receptu

**Pečená kuřecí prsa s brokolicí**

**Kategorie**: Oběd

**Porce**: 7 (meal prep na týden)

**Čas přípravy**: 10 minut aktivně + 25 minut pečení

**Nutriční hodnoty (na porci)**:
- Kalorie: 320 kcal
- Bílkoviny: 45g
- Sacharidy: 8g
- Tuky: 12g

**Ingredience**:
1. 2.5 kg kuřecích prsou
2. 1.5 kg brokolice
3. 100ml olivového oleje
4. Sůl, pepř, česnek (koření)

**Postup**:
1. Předehřej troubu na 200°C
2. Kuřecí prsa nakrájej na porce, okořeň
3. Brokolici rozděl na růžičky
4. Polej olejem, rozmísti na 2 plechy
5. Peč 25 minut

**Meal prep tipy**:
- Skladování: Vakuovat nebo meal prep krabičky
- Trvanlivost: 5 dní v lednici, 3 měsíce v mrazáku
- Ohřát: Mikrovlnka 2-3 minuty

**Variace**:
- Místo brokolice: špenát, zelené fazolky, paprika
- Koření: curry, paprika, bylinkové

---

Nyní vytvoř 10 receptů podle výše uvedených pokynů, zaměř se na jednoduchost a meal prep využitelnost!"""
        
        return template
    
    def _vytvorit_meal_prep_template(self):
        """Vytvoří prompt template pro generování meal prep plánu."""
        template = f"""# PROMPT TEMPLATE: Generování meal prep plánu

## Kontext

Jsi expert na meal prep a efektivní organizaci kuchyně. Tvým úkolem je vytvořit detailní 3-hodinový meal prep plán pro neděli.

## Cíl

Připravit **28 jídel** za 3 hodiny:
- 14 obědů (7 pro Romana + 7 pro Páju)
- 14 večeří (7 pro Romana + 7 pro Páju)
- Plus snídaně a svačiny (podle potřeby)

## Dostupné vybavení

- **Trouba**: 2 plechy (lze péct současně)
- **Tlakový hrnec**: 1 velký (6L)
- **Sporáky**: 4 plotýnky
- **Wok**: 1 velký
- **Vakuovačka**: Pro balení hotových jídel
- **Meal prep krabičky**: 58 kusů

## Meal prep strategie

### KROK 1: Příprava (15 minut)
- Rozplánovat timeline
- Připravit všechny ingredience
- Předehřát troubu
- Naplnit tlakový hrnec vodou

### KROK 2: Start vícero procesů současně (2 hodiny)
**Batch cooking princip**:
- Trouba: 2 plechy současně (rotace každých 25 min)
- Tlakový hrnec: Dlouhé vaření (40-60 min)
- Sporáky: 2 hrnce/pánve současně
- Příprava: Krájení zeleniny během vaření

### KROK 3: Balení a organizace (45 minut)
- Vakuování hotových jídel
- Plnění meal prep krabiček
- Označení (datum, obsah)
- Organizace v lednici/mrazáku

## Meal prep timeline template

Vytvoř časový harmonogram ve formátu:

**09:00-09:15 | PŘÍPRAVA**
- [ ] Předehřát troubu na 200°C
- [ ] Připravit 2.5kg kuřecích prsou
- [ ] Nakrájet zeleninu: brokolice, paprika, rajčata
- [ ] Naplnit tlakový hrnec vodou

**09:15-09:40 | START BATCH 1**
- [ ] TROUBA: Plech 1 - Kuřecí prsa (25 min)
- [ ] TROUBA: Plech 2 - Zelenina (25 min)
- [ ] TLAKÁK: Mleté maso + rajčatová omáčka (40 min)
- [ ] SPORÁK 1: Vaření vajec (15 ks, 10 min)

**09:40-10:05 | BATCH 2**
- [ ] TROUBA: Plech 1 - Losos (20 min)
- [ ] TROUBA: Plech 2 - Špenát (15 min)
- [ ] SPORÁK 2: Dušená zelenina (paprika, cuketa)
- [ ] PŘÍPRAVA: Krájení salátu

[... pokračuj až do 12:00 ...]

## Požadavky na plán

1. **Maximální efektivita**: Vždy něco vaří/peče současně
2. **Časová rezerva**: Nepřeplánuj, nech 10% buffer
3. **Logická posloupnost**: Začni tím, co trvá nejdéle
4. **Batch cooking**: Připrav stejné jídlo pro více dní najednou
5. **Rotace**: Míchej metody (pečení/vaření/dušení)

## Poznámky pro optimalizaci

### Časové triky:
- Zatímco něco peče, připravuj další várku
- Využij čekání na tlakový hrnec k přípravě zeleniny
- Vakuuj horká jídla (ale ne pálivá)
- Měření porcí: Použij kuchyňskou váhu

### Organizace:
- **Lednice** (3-4 dny): Jídla na pondělí-čtvrtek
- **Mrazák** (zbytek): Jídla na pátek-neděli
- **Přemístění**: Ve středu večer přesun z mrazáku do lednice

## Výstup

Vytvoř:

1. **Kompletní timeline** (09:00-12:00) s 15-minutovými bloky
2. **Checklist ingrediencí** (co připravit předem)
3. **Finální inventář** (kolik čeho bylo vyrobeno)
4. **Organizační plán** (co kam v lednici/mrazáku)

## Kalkulace času (reference)

Typické časy přípravy:
- Kuřecí prsa pečení: 25 min
- Mleté maso v tlakáči: 40 min
- Losos pečení: 20 min
- Zelenina pečení: 20-25 min
- Zelenina dušení: 15 min
- Vejce vaření: 10 min
- Vakuování 1 porce: 2 min
- Plnění krabičky: 1 min

---

Nyní vytvoř kompletní meal prep plán pro přípravu 28 jídel za 3 hodiny!"""
        
        return template
    
    def spustit_kompletni_zpracovani(self, interactive=True):
        """Spustí kompletní zpracování všech úkolů.
        
        Args:
            interactive: Pokud False, nepřerušuje pro uživatelský vstup
        """
        print("\n")
        print("*" * 80)
        print("*" + " " * 78 + "*")
        print("*" + "     FOODLER - SYSTÉM PRO ZPRACOVÁNÍ DOTAZNÍKŮ A PLÁNOVÁNÍ STRAVY     ".center(78) + "*")
        print("*" + " " * 78 + "*")
        print("*" * 80)
        print("\n")
        
        # Krok 1: Načíst dotazníky
        self.nacti_dotazniky()
        if interactive:
            input("\n⏸️  Stiskněte Enter pro pokračování...")
        
        # Krok 2: Sestavit doporučení
        self.sestavit_doporuceni()
        if interactive:
            input("\n⏸️  Stiskněte Enter pro pokračování...")
        
        # Krok 3: Zvážit meal prep potřeby
        self.zvazit_meal_prep_potreby()
        if interactive:
            input("\n⏸️  Stiskněte Enter pro pokračování...")
        
        # Krok 4: Shrnout nákupní plán
        self.shrnout_nakupni_plan()
        if interactive:
            input("\n⏸️  Stiskněte Enter pro pokračování...")
        
        # Krok 5: Vytvořit seznam pro Globus
        self.vytvorit_seznam_globus()
        if interactive:
            input("\n⏸️  Stiskněte Enter pro pokračování...")
        
        # Krok 6: Personalizovaná doporučení
        self.shrnout_personalizovana_doporuceni()
        if interactive:
            input("\n⏸️  Stiskněte Enter pro pokračování...")
        
        # Krok 7: Generovat AI prompt templates
        templates_path = self.generovat_ai_prompt_templates()
        
        # Závěr
        print()
        print("=" * 80)
        print("✅ KOMPLETNÍ ZPRACOVÁNÍ DOKONČENO")
        print("=" * 80)
        print()
        print("📁 Vytvořené soubory:")
        print(f"  • {self.output_file_path} (Nákupní seznam)")
        print(f"  • {templates_path} (AI Prompt Templates)")
        print()
        print("📚 Další kroky:")
        print("  1. Vytiskněte/stáhněte nákupní seznam pro Globus")
        print("  2. V sobotu zkontrolujte slevy na Kupi.cz")
        print("  3. Naplánujte neděli pro meal prep (3 hodiny)")
        print("  4. Užijte si celý týden bez vaření!")
        print()
        print("🤖 AI Prompt Templates:")
        print("  • Použijte templates s ChatGPT/Claude pro generování:")
        print("    - Týdenního jídelníčku")
        print("    - Detailních receptů")
        print("    - Meal prep plánu")
        print()
        print("🎯 Hodně štěstí na cestě k vašim cílům!")
        print()


def main():
    """Hlavní funkce."""
    # Kontrola, zda spustit interaktivní nebo automatický režim
    interactive = True
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        interactive = False
    
    system = RodinnyPlanSystem()
    system.spustit_kompletni_zpracovani(interactive=interactive)


if __name__ == "__main__":
    main()
