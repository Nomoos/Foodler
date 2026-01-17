#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Osobní preference a omezení pro Osobu 3 - Kubík
Důraz na podporu zraku a dětské stravování
"""

from typing import List, Dict


class PreferenceJidel:
    """Preference a omezení týkající se jídel pro předškolní dítě."""
    
    # Potraviny podporující zrak (vitamin A, beta-karoten, luteín)
    POTRAVINY_PRO_ZRAK: List[str] = [
        "mrkev",
        "sladké brambory",
        "dýně",
        "meruňky",
        "špenát",
        "brokolice",
        "vajíčka",
        "losos",
        "tuňák",
        "borůvky",
        "pomeranče"
    ]
    
    # Potraviny pomáhající při zácpě (vysoký obsah vlákniny)
    POTRAVINY_PROTI_ZACPE: List[str] = [
        "fíky (oblíbené! 2-3 denně)",  # DietniOmezeni.FIKY_DENNE_MIN-MAX
        "švestky",
        "sušené meruňky",
        "hrušky",
        "jablka",
        "brokolice",
        "hrášek",
        "ovesné vločky",
        "celozrnné těstoviny",
        "celozrnný chléb",
        "jogurt s probiotiky",
        "kefír",
        "voda (dostatek tekutin!)",
        "lněné semínko",
        "chia semínka"
    ]
    
    # Oblíbené dětské zdroje bílkovin
    PREFERRED_PROTEINS: List[str] = [
        "kuřecí maso",
        "krůtí maso",
        "ryby (losos, treska)",
        "vajíčka",
        "jogurt s probiotiky",
        "tvaroh",
        "sýr",
        "mléko",
        "kefír"
    ]
    
    # Dětská zelenina (sladší, měkčí chutě)
    PREFERRED_VEGETABLES: List[str] = [
        "mrkev",
        "sladké brambory",
        "kukuřice",
        "hrášek",
        "rajčata",
        "okurka",
        "paprika (sladká)",
        "brokolice (malé porcí)",
        "cuketa",
        "dýně"
    ]
    
    # Ovoce vhodné pro děti (důraz na vlákninu proti zácpě)
    PREFERRED_FRUITS: List[str] = [
        "fíky (oblíbené! 2-3 denně)",
        "švestky (čerstvé i sušené)",
        "hrušky",
        "jablka (se slupkou)",
        "meruňky",
        "broskve",
        "banány (zralé)",
        "jahody",
        "borůvky",
        "maliny",
        "pomeranče",
        "mandarinky"
    ]
    
    # Zdravé tuky pro děti
    PREFERRED_FATS: List[str] = [
        "avokádo",
        "lososový olej",
        "olivový olej",
        "ořechy (drcené, pozor na alergeny)",
        "mandlové máslo",
        "lněné semínko (mleté)"
    ]
    
    # Potraviny k omezení/vyhnutí
    NEPREFERRED_FOODS: List[str] = [
        "zpracované potraviny",
        "sladkosti",
        "chipsy",
        "slazené nápoje",
        "rychlé občerstvení",
        "příliš kořeněná jídla"
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
    def obsahuje_podporu_zraku(jidlo: str) -> bool:
        """
        Zkontroluje, zda jídlo obsahuje ingredience podporující zrak.
        
        Args:
            jidlo: Název nebo popis jídla
            
        Returns:
            True pokud jídlo obsahuje ingredience pro zrak
        """
        jidlo_lower = jidlo.lower()
        for potravina in PreferenceJidel.POTRAVINY_PRO_ZRAK:
            if potravina in jidlo_lower:
                return True
        return False
    
    @staticmethod
    def pomaha_proti_zacpe(jidlo: str) -> bool:
        """
        Zkontroluje, zda jídlo obsahuje ingredience pomáhající při zácpě.
        
        Args:
            jidlo: Název nebo popis jídla
            
        Returns:
            True pokud jídlo obsahuje ingredience proti zácpě
        """
        jidlo_lower = jidlo.lower()
        for potravina in PreferenceJidel.POTRAVINY_PROTI_ZACPE:
            if potravina.lower() in jidlo_lower:
                return True
        return False
    
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
            "potraviny_pro_zrak": PreferenceJidel.POTRAVINY_PRO_ZRAK,
            "potraviny_proti_zacpe": PreferenceJidel.POTRAVINY_PROTI_ZACPE,
            "nepreferovane": PreferenceJidel.NEPREFERRED_FOODS,
            "preferovane_bilkoviny": PreferenceJidel.PREFERRED_PROTEINS,
            "preferovana_zelenina": PreferenceJidel.PREFERRED_VEGETABLES,
            "preferovane_ovoce": PreferenceJidel.PREFERRED_FRUITS,
            "preferovane_tuky": PreferenceJidel.PREFERRED_FATS
        }


class DietniOmezeni:
    """Dietní omezení a doporučení pro předškolní dítě."""
    
    # Typ stravy
    TYP_STRAVY: str = "vyvážená dětská strava s podporou zraku a trávení"
    
    # Doporučené množství fíků
    FIKY_DENNE_MIN: int = 2  # fíky denně (minimum)
    FIKY_DENNE_MAX: int = 3  # fíky denně (maximum)
    
    # Omezení na jedno jídlo
    KALORIE_NA_JIDLO_VIKEND: int = 280  # cca 1400 / 5
    KALORIE_SNIDANE: int = 350  # 25% denní potřeby
    KALORIE_VECERE: int = 350  # 25% denní potřeby
    
    # Časy jídel
    CASY_JIDEL_PRACOVNI_DEN: Dict[str, str] = {
        "snidane_doma": "07:00",
        "dopoledni_svacina_skolka": "09:30",
        "obed_skolka": "12:00",
        "odpoledni_svacina_skolka": "15:00",
        "vecere_doma": "18:00"
    }
    
    CASY_JIDEL_VIKEND: Dict[str, str] = {
        "snidane": "08:00",
        "dopoledni_svacina": "10:00",
        "obed": "12:30",
        "odpoledni_svacina": "15:30",
        "vecere": "18:00"
    }
    
    # Příklady jídel podporujících zrak
    PRIKLADOVA_JIDLA_PRO_ZRAK: List[Dict[str, str]] = [
        {
            "nazev": "Mrkvový salát s jablkem",
            "ingredience": "mrkev, jablko, olivový olej, citron",
            "vitamin_a": "vysoký obsah beta-karotenu"
        },
        {
            "nazev": "Omeletka se špenátem",
            "ingredience": "vejce, špenát, sýr",
            "vitamin_a": "luteín ze špenátu + vitamin A z vajec"
        },
        {
            "nazev": "Losos s brokolicí a sladkými brambory",
            "ingredience": "losos, brokolice, sladké brambory",
            "vitamin_a": "omega-3 z lososa + beta-karoten"
        },
        {
            "nazev": "Jogurt s borůvkami",
            "ingredience": "přirozený jogurt, borůvky, med",
            "vitamin_a": "antioxidanty pro oči"
        },
        {
            "nazev": "Dýňová polévka",
            "ingredience": "dýně, mrkev, kokosové mléko",
            "vitamin_a": "velmi vysoký obsah beta-karotenu"
        },
        {
            "nazev": "Kuřecí prsa s kukuřicí a hráškem",
            "ingredience": "kuřecí maso, kukuřice, hrášek, mrkev",
            "vitamin_a": "luteín z kukuřice a hrášku"
        }
    ]
    
    # Příklady jídel pomáhajících při zácpě
    PRIKLADOVA_JIDLA_PROTI_ZACPE: List[Dict[str, str]] = [
        {
            "nazev": "Ovesná kaše s fíky a hruškou",
            "ingredience": "ovesné vločky, fíky (2-3 ks), hruška, voda",
            "benefit": "vysoká vláknina + oblíbené fíky"
        },
        {
            "nazev": "Jogurt s probiotiky, švestkami a chia",
            "ingredience": "jogurt, švestky, chia semínka",
            "benefit": "probiotika + vláknina"
        },
        {
            "nazev": "Celozrnný chléb s tvarohem a fíky",
            "ingredience": "celozrnný chléb, tvaroh, fíky (2-3 ks)",
            "benefit": "vláknina + oblíbené fíky"
        },
        {
            "nazev": "Hrušková svačinka s mandlovým máslem",
            "ingredience": "hruška, mandlové máslo",
            "benefit": "přírodní vláknina"
        },
        {
            "nazev": "Brokolice s celozrnnými těstovinami",
            "ingredience": "brokolice, celozrnné těstoviny, olivový olej",
            "benefit": "zelenina + vláknina"
        }
    ]
    
    @staticmethod
    def navrhni_jidla_pro_tyden() -> Dict[str, Dict[str, str]]:
        """
        Navrhne jídla na týden s důrazem na podporu zraku.
        Pracovní dny: snídaně a večeře doma
        Víkend: všechna jídla doma
        """
        return {
            "pondeli": {
                "snidane_doma": "Ovesná kaše s banánem a borůvkami",
                "vecere_doma": "Kuřecí nugety s mrkvovým salátem"
            },
            "utery": {
                "snidane_doma": "Jogurt s granolou a meruňkami",
                "vecere_doma": "Rybí prsty s brokolicí a sladkými brambory"
            },
            "streda": {
                "snidane_doma": "Vajíčková omeleta se špenátem",
                "vecere_doma": "Kuřecí polévka s mrkví a hráškem"
            },
            "ctvrtek": {
                "snidane_doma": "Tvarohový dezert s jahodami",
                "vecere_doma": "Špagety s rajčatovou omáčkou"
            },
            "patek": {
                "snidane_doma": "Palačinky s jablečným pyré",
                "vecere_doma": "Losos s cuketou a kukuřicí"
            },
            "sobota": {
                "snidane": "Francouzské toasty s borůvkami",
                "svacina": "Mrkev s hummusem",
                "obed": "Kuřecí řízek s bramborovou kaší a okurkou",
                "svacina": "Jablko s mandlovým máslem",
                "vecere": "Dýňová polévka s krutony"
            },
            "nedele": {
                "snidane": "Míchaná vejce s rajčaty",
                "svacina": "Jogurt s granolou",
                "obed": "Pečené kuře s mrkví a brokolicí",
                "svacina": "Borůvky s tvarohem",
                "vecere": "Zeleninová fritata"
            }
        }
    
    @staticmethod
    def vytvor_nakupni_seznam() -> Dict[str, List[str]]:
        """Vytvoří nákupní seznam s důrazem na potraviny pro zrak a trávení."""
        return {
            "zelenina": [
                "mrkev (1 kg)",
                "brokolice (2 ks)",
                "špenát (1 balení)",
                "sladké brambory (500g)",
                "dýně (1 ks)",
                "okurka (2 ks)",
                "rajčata (500g)",
                "paprika (3 ks)",
                "hrášek (300g)"
            ],
            "ovoce": [
                f"fíky ({DietniOmezeni.FIKY_DENNE_MIN * 7}-{DietniOmezeni.FIKY_DENNE_MAX * 7} ks pro týden) - PRIORITA!",
                "švestky (500g)",
                "hrušky (5 ks)",
                "jablka (1 kg)",
                "borůvky (250g)",
                "jahody (250g)",
                "meruňky (300g)",
                "pomeranče (4 ks)"
            ],
            "bilkoviny": [
                "kuřecí prsa (500g)",
                "losos (300g)",
                "vejce (10 ks)",
                "jogurt s probiotiky (4 ks)",
                "kefír (1 l)",
                "tvaroh (2 ks)",
                "sýr (200g)"
            ],
            "ostatni": [
                "olivový olej",
                "kokosové mléko",
                "ovesné vločky",
                "celozrnné těstoviny",
                "celozrnný chléb",
                "hummus",
                "mandlové máslo",
                "chia semínka",
                "lněné semínko (mleté)"
            ]
        }


def main():
    """Ukázka použití preferencí."""
    print("=" * 60)
    print("PREFERENCE JÍDEL - KUBÍK (4.5 let)")
    print("=" * 60)
    
    preference = PreferenceJidel.ziskej_preference_summary()
    
    print("\n🥕 POTRAVINY PODPORUJÍCÍ ZRAK (priorita!):")
    for item in preference["potraviny_pro_zrak"]:
        print(f"  ✓ {item}")
    
    print("\n🌾 POTRAVINY PROTI ZÁCPĚ (důležité!):")
    for item in preference["potraviny_proti_zacpe"]:
        print(f"  ✓ {item}")
    
    print("\n🍗 Preferované bílkoviny:")
    for item in preference["preferovane_bilkoviny"]:
        print(f"  ✓ {item}")
    
    print("\n🥦 Preferovaná zelenina:")
    for item in preference["preferovana_zelenina"]:
        print(f"  ✓ {item}")
    
    print("\n🍎 Preferované ovoce:")
    for item in preference["preferovane_ovoce"]:
        print(f"  ✓ {item}")
    
    print("\n" + "=" * 60)
    print("PŘÍKLADOVÁ JÍDLA PRO PODPORU ZRAKU")
    print("=" * 60)
    for jidlo in DietniOmezeni.PRIKLADOVA_JIDLA_PRO_ZRAK:
        print(f"\n📍 {jidlo['nazev']}")
        print(f"   Ingredience: {jidlo['ingredience']}")
        print(f"   Benefit: {jidlo['vitamin_a']}")
    
    print("\n" + "=" * 60)
    print("PŘÍKLADOVÁ JÍDLA PROTI ZÁCPĚ")
    print("=" * 60)
    for jidlo in DietniOmezeni.PRIKLADOVA_JIDLA_PROTI_ZACPE:
        print(f"\n📍 {jidlo['nazev']}")
        print(f"   Ingredience: {jidlo['ingredience']}")
        print(f"   Benefit: {jidlo['benefit']}")
    
    print("\n" + "=" * 60)
    print("NÁVRH JÍDEL NA TÝDEN")
    print("=" * 60)
    tydenni_plan = DietniOmezeni.navrhni_jidla_pro_tyden()
    for den, jidla in tydenni_plan.items():
        print(f"\n{den.upper()}:")
        for typ_jidla, jidlo in jidla.items():
            print(f"  • {typ_jidla.replace('_', ' ').title()}: {jidlo}")
    
    print("\n" + "=" * 60)
    print("NÁKUPNÍ SEZNAM")
    print("=" * 60)
    nakup = DietniOmezeni.vytvor_nakupni_seznam()
    for kategorie, polozky in nakup.items():
        print(f"\n{kategorie.upper()}:")
        for polozka in polozky:
            print(f"  □ {polozka}")


if __name__ == "__main__":
    main()
