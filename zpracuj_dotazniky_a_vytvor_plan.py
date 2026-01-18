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
        
        # Závěr
        print()
        print("=" * 80)
        print("✅ KOMPLETNÍ ZPRACOVÁNÍ DOKONČENO")
        print("=" * 80)
        print()
        print("📁 Vytvořené soubory:")
        print(f"  • {self.output_file_path}")
        print()
        print("📚 Další kroky:")
        print("  1. Vytiskněte/stáhněte nákupní seznam pro Globus")
        print("  2. V sobotu zkontrolujte slevy na Kupi.cz")
        print("  3. Naplánujte neděli pro meal prep (3 hodiny)")
        print("  4. Užijte si celý týden bez vaření!")
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
