#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor variací receptů - modul pro vytváření variant receptů s různými ingrediencemi

Tento modul umožňuje:
- Vygenerovat varianty receptu s různými sýry
- Vygenerovat varianty receptu s vejci
- Automaticky vypočítat nutriční hodnoty pro každou variaci
"""

from dataclasses import dataclass, replace
from typing import List, Dict, Optional
import sys
import os

# Přidání rodičovského adresáře do cesty pro import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jidla.databaze import Jidlo, Ingredience
from potraviny.databaze import DatabazePotravIn, Potravina


@dataclass
class VariaceReceptu:
    """Reprezentuje jednu variaci receptu."""
    nazev: str
    puvodni_recept: str
    zmenene_ingredience: List[tuple]  # [(puvodni, nova), ...]
    jidlo: Jidlo
    
    def __str__(self):
        """Formátovaný výstup variace."""
        makra = self.jidlo.vypocitej_makra_na_porci()
        zmeny = ", ".join([f"{p} → {n}" for p, n in self.zmenene_ingredience])
        return f"{self.nazev}\n  Změny: {zmeny}\n  Makra: {makra['kalorie']}kcal | B:{makra['bilkoviny']}g S:{makra['sacharidy']}g T:{makra['tuky']}g"


class GeneratorVariaci:
    """Generátor variací receptů."""
    
    @staticmethod
    def _vypocitej_nutrici_ingredience(nazev: str, mnozstvi_g: float) -> Dict[str, float]:
        """Vypočítá nutriční hodnoty pro danou ingredienci."""
        potravina = DatabazePotravIn.najdi_podle_nazvu(nazev)
        if not potravina:
            # Pokud ingredience není v databázi, vrátíme nulové hodnoty
            return {
                "kalorie": 0,
                "bilkoviny": 0,
                "sacharidy": 0,
                "tuky": 0,
                "vlaknina": 0
            }
        return potravina.vypocitej_makra(mnozstvi_g)
    
    @staticmethod
    def _vypocitej_celkovou_nutrici(ingredience: List[Ingredience]) -> Dict[str, float]:
        """Vypočítá celkovou nutrici z ingrediencí."""
        celkem = {
            "kalorie": 0.0,
            "bilkoviny": 0.0,
            "sacharidy": 0.0,
            "tuky": 0.0,
            "vlaknina": 0.0
        }
        
        for ing in ingredience:
            nutrice = GeneratorVariaci._vypocitej_nutrici_ingredience(ing.nazev, ing.mnozstvi_g)
            for key in celkem:
                celkem[key] += nutrice[key]
        
        return celkem
    
    @classmethod
    def vygeneruj_varianty_syr(
        cls, 
        puvodni_jidlo: Jidlo, 
        ingredience_k_nahrade: str,
        alternativni_syry: Optional[List[str]] = None
    ) -> List[VariaceReceptu]:
        """
        Vygeneruje varianty receptu s různými sýry.
        
        Args:
            puvodni_jidlo: Původní recept
            ingredience_k_nahrade: Název ingredience, která se má nahradit
            alternativni_syry: Seznam názvů alternativních sýrů (pokud None, použijí se běžné sýry)
        
        Returns:
            Seznam variant receptu
        """
        if alternativni_syry is None:
            alternativni_syry = [
                "Mozzarella",
                "Parmazán",
                "Gouda",
                "Cheddar",
                "Sýr eidam",
            ]
        
        varianty = []
        
        # Najdeme ingredienci k náhradě a její množství
        puvodni_ingredience = None
        for ing in puvodni_jidlo.ingredience:
            if ingredience_k_nahrade.lower() in ing.nazev.lower():
                puvodni_ingredience = ing
                break
        
        if not puvodni_ingredience:
            return varianty
        
        # Vytvoříme variantu pro každý alternativní sýr
        for syr in alternativni_syry:
            # Zkontrolujeme, že sýr existuje v databázi
            potravina = DatabazePotravIn.najdi_podle_nazvu(syr)
            if not potravina:
                continue
            
            # Vytvoříme novou sadu ingrediencí
            nove_ingredience = []
            for ing in puvodni_jidlo.ingredience:
                if ing.nazev == puvodni_ingredience.nazev:
                    nove_ingredience.append(
                        Ingredience(syr, ing.mnozstvi_g, ing.kategorie)
                    )
                else:
                    nove_ingredience.append(ing)
            
            # Vypočítáme novou nutrici
            nutrice = cls._vypocitej_celkovou_nutrici(nove_ingredience)
            
            # Vytvoříme nové jídlo
            nove_jidlo = replace(
                puvodni_jidlo,
                nazev=f"{puvodni_jidlo.nazev} (varianta s {syr})",
                ingredience=nove_ingredience,
                kalorie_celkem=nutrice["kalorie"],
                bilkoviny_celkem=nutrice["bilkoviny"],
                sacharidy_celkem=nutrice["sacharidy"],
                tuky_celkem=nutrice["tuky"],
                vlaknina_celkem=nutrice["vlaknina"],
            )
            
            # Vytvoříme variaci
            variace = VariaceReceptu(
                nazev=nove_jidlo.nazev,
                puvodni_recept=puvodni_jidlo.nazev,
                zmenene_ingredience=[(puvodni_ingredience.nazev, syr)],
                jidlo=nove_jidlo
            )
            
            varianty.append(variace)
        
        return varianty
    
    @classmethod
    def vygeneruj_varianty_s_vejci(
        cls,
        puvodni_jidlo: Jidlo,
        mnozstvi_vajec_g: float = 50
    ) -> List[VariaceReceptu]:
        """
        Vygeneruje varianty receptu s přidáním vajec.
        
        Args:
            puvodni_jidlo: Původní recept
            mnozstvi_vajec_g: Množství vajec v gramech (50g = cca 1 vejce)
        
        Returns:
            Seznam variant receptu
        """
        varianty = []
        
        # Vytvoříme variantu s přidáním vajec
        nove_ingredience = list(puvodni_jidlo.ingredience)
        nove_ingredience.append(
            Ingredience("Vejce", mnozstvi_vajec_g, "hlavni")
        )
        
        # Vypočítáme novou nutrici
        nutrice = cls._vypocitej_celkovou_nutrici(nove_ingredience)
        
        # Vytvoříme nové jídlo
        nove_jidlo = replace(
            puvodni_jidlo,
            nazev=f"{puvodni_jidlo.nazev} + vejce",
            ingredience=nove_ingredience,
            kalorie_celkem=nutrice["kalorie"],
            bilkoviny_celkem=nutrice["bilkoviny"],
            sacharidy_celkem=nutrice["sacharidy"],
            tuky_celkem=nutrice["tuky"],
            vlaknina_celkem=nutrice["vlaknina"],
        )
        
        # Vytvoříme variaci
        variace = VariaceReceptu(
            nazev=nove_jidlo.nazev,
            puvodni_recept=puvodni_jidlo.nazev,
            zmenene_ingredience=[("žádné", f"+ {mnozstvi_vajec_g}g vajec")],
            jidlo=nove_jidlo
        )
        
        varianty.append(variace)
        
        return varianty
    
    @classmethod
    def vygeneruj_komplexni_varianty(
        cls,
        puvodni_jidlo: Jidlo,
        syrove_varianty: bool = True,
        vejce_varianta: bool = True,
        syr_k_nahrade: Optional[str] = None,
        alternativni_syry: Optional[List[str]] = None
    ) -> List[VariaceReceptu]:
        """
        Vygeneruje kompletní sadu variant receptu.
        
        Args:
            puvodni_jidlo: Původní recept
            syrove_varianty: Zda generovat varianty s různými sýry
            vejce_varianta: Zda generovat variantu s vejci
            syr_k_nahrade: Název sýru k náhradě (pokud None, hledá automaticky)
            alternativni_syry: Seznam alternativních sýrů
        
        Returns:
            Seznam všech variant receptu
        """
        vsechny_varianty = []
        
        # Varianty se sýry
        if syrove_varianty:
            # Pokud není specifikován sýr k náhradě, najdeme první sýr v ingrediencích
            if syr_k_nahrade is None:
                for ing in puvodni_jidlo.ingredience:
                    if any(keyword in ing.nazev.lower() for keyword in ["sýr", "cheese", "bochník", "klásek", "eidam", "gouda", "cheddar"]):
                        syr_k_nahrade = ing.nazev
                        break
            
            if syr_k_nahrade:
                varianty_syr = cls.vygeneruj_varianty_syr(
                    puvodni_jidlo, 
                    syr_k_nahrade,
                    alternativni_syry
                )
                vsechny_varianty.extend(varianty_syr)
        
        # Varianta s vejci
        if vejce_varianta:
            varianty_vejce = cls.vygeneruj_varianty_s_vejci(puvodni_jidlo)
            vsechny_varianty.extend(varianty_vejce)
        
        return vsechny_varianty


def main():
    """Ukázka použití generátoru variací."""
    from jidla.databaze import DatabzeJidel
    
    print("=" * 80)
    print("GENERÁTOR VARIACÍ RECEPTŮ")
    print("=" * 80)
    
    # Najdeme Keto pizzu
    keto_pizza = DatabzeJidel.najdi_podle_nazvu("Keto pizza")
    
    if not keto_pizza:
        print("\n❌ Keto pizza nebyla nalezena v databázi!")
        return
    
    print(f"\n📋 PŮVODNÍ RECEPT: {keto_pizza.nazev}")
    print(f"   Ingredience:")
    for ing in keto_pizza.ingredience:
        print(f"     • {ing.nazev}: {ing.mnozstvi_g}g")
    
    makra = keto_pizza.vypocitej_makra_na_porci()
    print(f"\n   Nutriční hodnoty na porci:")
    print(f"     • Kalorie: {makra['kalorie']} kcal")
    print(f"     • Bílkoviny: {makra['bilkoviny']}g")
    print(f"     • Sacharidy: {makra['sacharidy']}g")
    print(f"     • Tuky: {makra['tuky']}g")
    print(f"     • Vláknina: {makra['vlaknina']}g")
    
    # Vygenerujeme kompletní varianty
    print("\n" + "=" * 80)
    print("VYGENEROVANÉ VARIANTY")
    print("=" * 80)
    
    varianty = GeneratorVariaci.vygeneruj_komplexni_varianty(
        keto_pizza,
        syrove_varianty=True,
        vejce_varianta=True,
        syr_k_nahrade="Sýrařův výběr moravský bochník 45% Madeta"
    )
    
    # Sýrové varianty
    print("\n🧀 VARIANTY S RŮZNÝMI SÝRY:\n")
    syrove = [v for v in varianty if "vejce" not in v.nazev.lower()]
    for i, variace in enumerate(syrove, 1):
        print(f"{i}. {variace}")
        print()
    
    # Varianta s vejci
    print("=" * 80)
    print("🥚 VARIANTA S VEJCI:\n")
    vejce_varianty = [v for v in varianty if "vejce" in v.nazev.lower()]
    for variace in vejce_varianty:
        print(f"• {variace}")
        print()
    
    # Podrobný výpis jedné varianty
    if varianty:
        print("=" * 80)
        print("DETAILNÍ POHLED NA JEDNU VARIANTU")
        print("=" * 80)
        
        variace = varianty[0]
        print(f"\n📋 {variace.nazev}")
        print(f"\nIngrediencé:")
        for ing in variace.jidlo.ingredience:
            print(f"  • {ing.nazev}: {ing.mnozstvi_g}g")
        
        print(f"\nPostup přípravy:")
        print(f"  {variace.jidlo.priprava_postup}")
        
        print(f"\nObtížnost: {variace.jidlo.obtiznost}")
        print(f"Čas přípravy: {variace.jidlo.priprava_cas_min} min")


if __name__ == "__main__":
    main()
