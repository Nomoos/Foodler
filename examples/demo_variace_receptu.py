#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo skript pro ukázku použití generátoru variací receptů

Tento skript demonstruje, jak:
1. Najít recept v databázi
2. Vygenerovat varianty s různými sýry
3. Vygenerovat varianty s vejci
4. Uložit si oblíbené varianty
"""

from jidla.databaze import DatabzeJidel
from jidla.variace_receptu import GeneratorVariaci, VariaceReceptu


def zobraz_recept(jidlo, title="RECEPT"):
    """Zobrazí recept v pěkném formátu."""
    print(f"\n{'=' * 80}")
    print(f"{title}: {jidlo.nazev}")
    print('=' * 80)
    
    print("\n📋 INGREDIENCE:")
    for ing in jidlo.ingredience:
        print(f"   • {ing.nazev}: {ing.mnozstvi_g}g")
    
    print("\n👨‍🍳 PŘÍPRAVA:")
    print(f"   Čas: {jidlo.priprava_cas_min} minut")
    print(f"   Obtížnost: {jidlo.obtiznost}")
    print(f"\n   Postup:")
    for i, krok in enumerate(jidlo.priprava_postup.split('. '), 1):
        if krok.strip():
            print(f"   {i}. {krok.strip()}")
    
    makra = jidlo.vypocitej_makra_na_porci()
    print("\n📊 NUTRIČNÍ HODNOTY (na 1 porci):")
    print(f"   • Energie: {makra['kalorie']:.0f} kcal")
    print(f"   • Bílkoviny: {makra['bilkoviny']:.1f}g")
    print(f"   • Sacharidy: {makra['sacharidy']:.1f}g")
    print(f"   • Tuky: {makra['tuky']:.1f}g")
    print(f"   • Vláknina: {makra['vlaknina']:.1f}g")
    
    if jidlo.poznamky:
        print(f"\n💡 POZNÁMKA: {jidlo.poznamky}")


def zobraz_varianty(varianty, typ="VARIANTY"):
    """Zobrazí seznam variant."""
    print(f"\n{'=' * 80}")
    print(f"🔄 {typ}")
    print('=' * 80)
    
    for i, variace in enumerate(varianty, 1):
        makra = variace.jidlo.vypocitej_makra_na_porci()
        print(f"\n{i}. {variace.nazev}")
        
        if variace.zmenene_ingredience:
            zmeny = " → ".join([n for _, n in variace.zmenene_ingredience if n])
            print(f"   🔄 Změna: {zmeny}")
        
        print(f"   📊 Makra: {makra['kalorie']:.0f}kcal | " + 
              f"B:{makra['bilkoviny']:.1f}g | " +
              f"S:{makra['sacharidy']:.1f}g | " +
              f"T:{makra['tuky']:.1f}g")


def main():
    """Hlavní demo funkce."""
    print("=" * 80)
    print("🍕 DEMO: GENERÁTOR VARIACÍ RECEPTŮ - KETO PIZZA")
    print("=" * 80)
    print("\nTento skript ukazuje, jak vygenerovat různé varianty receptu")
    print("s jinými sýry, vejcem a dalšími ingrediencemi.")
    
    # 1. Načteme původní recept
    print("\n\n" + "=" * 80)
    print("KROK 1: NAČTENÍ PŮVODNÍHO RECEPTU")
    print("=" * 80)
    
    keto_pizza = DatabzeJidel.najdi_podle_nazvu("Keto pizza")
    
    if not keto_pizza:
        print("\n❌ Keto pizza nebyla nalezena v databázi!")
        print("   Ujistěte se, že recept byl přidán do jidla/databaze.py")
        return
    
    zobraz_recept(keto_pizza, "PŮVODNÍ RECEPT")
    
    # 2. Vygenerujeme varianty se sýry
    print("\n\n" + "=" * 80)
    print("KROK 2: GENEROVÁNÍ VARIANT S RŮZNÝMI SÝRY")
    print("=" * 80)
    print("\nVygenerujeme varianty, kde nahradíme 'Sýrařův výběr moravský bochník'")
    print("různými typy sýrů (Mozzarella, Parmazán, Gouda, Cheddar, Eidam)")
    
    syrove_varianty = GeneratorVariaci.vygeneruj_varianty_syr(
        keto_pizza,
        ingredience_k_nahrade="Sýrařův výběr moravský bochník 45% Madeta",
        alternativni_syry=["Mozzarella", "Parmazán", "Gouda", "Cheddar", "Sýr eidam"]
    )
    
    zobraz_varianty(syrove_varianty, "VARIANTY S RŮZNÝMI SÝRY")
    
    # 3. Vygenerujeme variantu s vejci
    print("\n\n" + "=" * 80)
    print("KROK 3: GENEROVÁNÍ VARIANTY S PŘIDÁNÍM VAJEC")
    print("=" * 80)
    print("\nPřidáme do receptu vejce pro zvýšení obsahu bílkovin")
    
    vejce_varianty = GeneratorVariaci.vygeneruj_varianty_s_vejci(
        keto_pizza,
        mnozstvi_vajec_g=50  # přibližně 1 vejce
    )
    
    zobraz_varianty(vejce_varianty, "VARIANTA S VEJCI")
    
    # 4. Ukážeme, jak vybrat nejlepší variantu podle makronutrientů
    print("\n\n" + "=" * 80)
    print("KROK 4: VÝBĚR NEJLEPŠÍ VARIANTY PODLE MAKRONUTRIENTŮ")
    print("=" * 80)
    
    vsechny_varianty = syrove_varianty + vejce_varianty
    
    # Najdeme variantu s nejvíce bílkovin
    nejvice_bilkovin = max(
        vsechny_varianty,
        key=lambda v: v.jidlo.vypocitej_makra_na_porci()['bilkoviny']
    )
    
    print("\n🏆 VARIANTA S NEJVÍCE BÍLKOVIN:")
    zobraz_recept(nejvice_bilkovin.jidlo, "NEJLEPŠÍ PRO PROTEINY")
    
    # Najdeme variantu s nejméně sacharidy
    nejmin_sacharidu = min(
        vsechny_varianty,
        key=lambda v: v.jidlo.vypocitej_makra_na_porci()['sacharidy']
    )
    
    print("\n\n🏆 VARIANTA S NEJMÉNĚ SACHARIDY:")
    zobraz_recept(nejmin_sacharidu.jidlo, "NEJLEPŠÍ PRO KETO")
    
    # 5. Ukážeme kompletní generování všech variant najednou
    print("\n\n" + "=" * 80)
    print("KROK 5: KOMPLETNÍ GENEROVÁNÍ VŠECH VARIANT")
    print("=" * 80)
    print("\nMůžeme vygenerovat všechny varianty najednou pomocí jednoho volání:")
    
    komplexni_varianty = GeneratorVariaci.vygeneruj_komplexni_varianty(
        keto_pizza,
        syrove_varianty=True,
        vejce_varianta=True
    )
    
    print(f"\n✅ Vygenerováno celkem {len(komplexni_varianty)} variant receptu!")
    
    # Závěrečné shrnutí
    print("\n\n" + "=" * 80)
    print("📝 SHRNUTÍ")
    print("=" * 80)
    print("\n✅ Naučili jsme se:")
    print("   1. Načíst recept z databáze")
    print("   2. Vygenerovat varianty s různými sýry")
    print("   3. Vygenerovat varianty s vejci")
    print("   4. Vybrat nejlepší variantu podle makronutrientů")
    print("   5. Použít komplexní generování všech variant")
    
    print("\n💡 TIP: Můžete si vytvořit vlastní funkce pro:")
    print("   • Generování variant s různými druhy masa")
    print("   • Generování variant se zeleninou")
    print("   • Kombinování více změn najednou")
    print("   • Ukládání oblíbených variant do databáze")
    
    print("\n" + "=" * 80)
    print("🎉 KONEC DEMO")
    print("=" * 80)


if __name__ == "__main__":
    main()
