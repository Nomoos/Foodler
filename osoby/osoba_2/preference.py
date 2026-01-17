#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Osobní preference a omezení pro Osobu 2
"""

from typing import List, Dict


class PreferenceJidel:
    """Preference a omezení týkající se jídel."""
    
    # Potraviny, které je třeba omezit nebo vyloučit
    NEPREFERRED_FOODS: List[str] = [
        "houby",
        "hříbky",
        "žampiony",
        "hlíva",
        "shiitake"
    ]
    
    # Oblíbené zdroje bílkovin
    PREFERRED_PROTEINS: List[str] = [
        "kuřecí prsa",
        "krůtí maso",
        "ryby (losos, tuňák)",
        "vejce",
        "tvaroh",
        "řecký jogurt",
        "cottage cheese",
        "tofu (občas)"
    ]
    
    # Oblíbená zelenina (low-carb)
    PREFERRED_VEGETABLES: List[str] = [
        "brokolice",
        "špenát",
        "salát",
        "rajčata",
        "okurka",
        "paprika",
        "cuketa",
        "zelí",
        "květák",
        "rukola",
        "baby špenát"
    ]
    
    # Zdravé tuky
    PREFERRED_FATS: List[str] = [
        "olivový olej",
        "avokádo",
        "mandle",
        "vlašské ořechy",
        "lněné semínko",
        "chia semínka"
    ]
    
    @staticmethod
    def je_jidlo_vhodne(jidlo: str) -> bool:
        """
        Zkontroluje, zda jídlo neobsahuje nepreferované ingredience.
        
        Args:
            jidlo: Název nebo popis jídla
            
        Returns:
            True pokud je jídlo vhodné, False pokud obsahuje nepreferované složky
        """
        jidlo_lower = jidlo.lower()
        for nepref in PreferenceJidel.NEPREFERRED_FOODS:
            if nepref in jidlo_lower:
                return False
        return True
    
    @staticmethod
    def filtruj_jidla(jidla: List[str]) -> List[str]:
        """
        Filtruje seznam jídel a odstraní ta s nepreferovanými ingrediencemi.
        
        Args:
            jidla: Seznam názvů jídel
            
        Returns:
            Filtrovaný seznam jídel
        """
        return [j for j in jidla if PreferenceJidel.je_jidlo_vhodne(j)]
    
    @staticmethod
    def ziskej_preference_summary() -> Dict[str, List[str]]:
        """Vrátí kompletní přehled preferencí."""
        return {
            "nepreferovane": PreferenceJidel.NEPREFERRED_FOODS,
            "preferovane_bilkoviny": PreferenceJidel.PREFERRED_PROTEINS,
            "preferovana_zelenina": PreferenceJidel.PREFERRED_VEGETABLES,
            "preferovane_tuky": PreferenceJidel.PREFERRED_FATS
        }


class DietniOmezeni:
    """Dietní omezení a doporučení."""
    
    # Typ diety
    TYP_DIETY: str = "ketogenní/low-carb"
    
    # Omezení
    MAX_SACHARIDY_NA_JIDLO: int = 12  # g (60g / 5 jídel = 12g)
    MIN_BILKOVINY_NA_JIDLO: int = 20  # g (100g / 5 jídel = 20g)
    
    # Časy jídel (preferované)
    CASY_JIDEL: Dict[str, str] = {
        "snidane": "07:30",
        "dopoledni_svacina": "10:00",
        "obed": "12:30",
        "odpoledni_svacina": "15:30",
        "vecere": "18:30"
    }
    
    # Doplňky stravy
    DOPLNKY: List[str] = [
        "Multivitamin",
        "Omega-3",
        "Vitamin D",
        "Probiotika"
    ]
    
    @staticmethod
    def je_jidlo_v_ramci_limitu(sacharidy: float, bilkoviny: float) -> bool:
        """
        Kontroluje, zda jídlo spadá do denních limitů makronutrientů.
        
        Args:
            sacharidy: Množství sacharidů v gramech
            bilkoviny: Množství bílkovin v gramech
            
        Returns:
            True pokud je jídlo v rámci limitů
        """
        return (sacharidy <= DietniOmezeni.MAX_SACHARIDY_NA_JIDLO and 
                bilkoviny >= DietniOmezeni.MIN_BILKOVINY_NA_JIDLO)


def main():
    """Ukázka použití preferencí."""
    print("=" * 60)
    print("PREFERENCE JÍDEL - OSOBA 2")
    print("=" * 60)
    
    preference = PreferenceJidel.ziskej_preference_summary()
    
    print("\nNepreferované potraviny:")
    for item in preference["nepreferovane"]:
        print(f"  ✗ {item}")
    
    print("\nPreferované bílkoviny:")
    for item in preference["preferovane_bilkoviny"]:
        print(f"  ✓ {item}")
    
    print("\nPreferovaná zelenina:")
    for item in preference["preferovana_zelenina"]:
        print(f"  ✓ {item}")
    
    print("\nPreferované zdravé tuky:")
    for item in preference["preferovane_tuky"]:
        print(f"  ✓ {item}")
    
    print("\n" + "=" * 60)
    print("DIETNÍ OMEZENÍ")
    print("=" * 60)
    print(f"Typ diety: {DietniOmezeni.TYP_DIETY}")
    print(f"Max sacharidy na jídlo: {DietniOmezeni.MAX_SACHARIDY_NA_JIDLO}g")
    print(f"Min bílkoviny na jídlo: {DietniOmezeni.MIN_BILKOVINY_NA_JIDLO}g")
    
    print("\nDoporučené časy jídel:")
    for jidlo, cas in DietniOmezeni.CASY_JIDEL.items():
        print(f"  {jidlo}: {cas}")


if __name__ == "__main__":
    main()
