#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sdílená jídla pro celou rodinu
Obsahuje jídla, která mohou sdílet obě osoby s možností úprav porcí
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class SdilenеJidlo:
    """Reprezentuje jídlo, které může být sdíleno mezi osobami."""
    
    nazev: str
    kategorie: str  # "snidane", "obed", "vecere", "svacina"
    ingredience: List[str]
    bilkoviny_na_100g: float
    sacharidy_na_100g: float
    tuky_na_100g: float
    vlaknina_na_100g: float
    kalorie_na_100g: float
    priprava_cas_min: int  # Čas přípravy v minutách
    priprava_popis: str
    vhodne_pro_meal_prep: bool
    poznamky: Optional[str] = None
    
    def vypocitej_makra(self, porce_g: float) -> Dict[str, float]:
        """Vypočítá makronutrienty pro danou porci."""
        koeficient = porce_g / 100
        return {
            "bilkoviny": round(self.bilkoviny_na_100g * koeficient, 1),
            "sacharidy": round(self.sacharidy_na_100g * koeficient, 1),
            "tuky": round(self.tuky_na_100g * koeficient, 1),
            "vlaknina": round(self.vlaknina_na_100g * koeficient, 1),
            "kalorie": round(self.kalorie_na_100g * koeficient, 1)
        }


class SdilenaJidla:
    """Sbírka sdílených jídel vhodných pro celou rodinu."""
    
    JIDLA: List[SdilenеJidlo] = [
        SdilenеJidlo(
            nazev="Kuřecí prsa na grilu s brokolicí",
            kategorie="obed",
            ingredience=["kuřecí prsa", "brokolice", "olivový olej", "česnek", "koření"],
            bilkoviny_na_100g=25.0,
            sacharidy_na_100g=4.0,
            tuky_na_100g=6.0,
            vlaknina_na_100g=2.5,
            kalorie_na_100g=170.0,
            priprava_cas_min=25,
            priprava_popis="Kuřecí prsa naložit v olivovém oleji s kořením, grilovat 6-8 min z každé strany. Brokolici uvařit na páře.",
            vhodne_pro_meal_prep=True,
            poznamky="Ideální pro přípravu dopředu, vydrží 3-4 dny v lednici"
        ),
        SdilenеJidlo(
            nazev="Salát s tuňákem a vejcem",
            kategorie="obed",
            ingredience=["tuňák v konzervě", "vejce", "zelený salát", "okurka", "olivový olej", "citrón"],
            bilkoviny_na_100g=18.0,
            sacharidy_na_100g=3.0,
            tuky_na_100g=8.0,
            vlaknina_na_100g=2.0,
            kalorie_na_100g=155.0,
            priprava_cas_min=15,
            priprava_popis="Vejce uvařit natvrdo (10 min), tuňák smíchat se zeleninou, přidat dressing z oleje a citrónu.",
            vhodne_pro_meal_prep=True,
            poznamky="Rychlá příprava, lze připravit den dopředu"
        ),
        SdilenеJidlo(
            nazev="Hovězí maso s cuketou",
            kategorie="vecere",
            ingredience=["hovězí maso", "cuketa", "cibule", "rajčata", "olivový olej"],
            bilkoviny_na_100g=22.0,
            sacharidy_na_100g=5.0,
            tuky_na_100g=9.0,
            vlaknina_na_100g=2.0,
            kalorie_na_100g=190.0,
            priprava_cas_min=30,
            priprava_popis="Hovězí nakrájet na kostky, opéct na olivovém oleji s cibulí. Přidat cuketu a rajčata, dusit 15 min.",
            vhodne_pro_meal_prep=True,
            poznamky="Výborné pro víkendový meal prep, vydrží 4 dny"
        ),
        SdilenеJidlo(
            nazev="Vaječná omeleta se špenátem",
            kategorie="snidane",
            ingredience=["vejce", "špenát", "sýr", "máslo", "koření"],
            bilkoviny_na_100g=12.0,
            sacharidy_na_100g=2.0,
            tuky_na_100g=10.0,
            vlaknina_na_100g=1.5,
            kalorie_na_100g=150.0,
            priprava_cas_min=10,
            priprava_popis="Vejce rozšlehat, přidat špenát a sýr. Smažit na másle do zlatova.",
            vhodne_pro_meal_prep=False,
            poznamky="Nejlepší čerstvě připravená, ale lze ohřát"
        ),
        SdilenеJidlo(
            nazev="Tvaroh s lněným semínkem",
            kategorie="svacina",
            ingredience=["tvaroh polotučný", "lněné semínko", "skořice"],
            bilkoviny_na_100g=16.0,
            sacharidy_na_100g=3.5,
            tuky_na_100g=4.5,
            vlaknina_na_100g=3.0,
            kalorie_na_100g=120.0,
            priprava_cas_min=2,
            priprava_popis="Tvaroh smíchat s mletým lněným semínkem, posypat skořicí.",
            vhodne_pro_meal_prep=True,
            poznamky="Rychlá svačina, vydrží 2 dny"
        ),
        SdilenеJidlo(
            nazev="Losos s kedlubnou",
            kategorie="vecere",
            ingredience=["lososový filet", "kedlubna", "olivový olej", "citrón", "kopr"],
            bilkoviny_na_100g=20.0,
            sacharidy_na_100g=4.0,
            tuky_na_100g=12.0,
            vlaknina_na_100g=2.0,
            kalorie_na_100g=210.0,
            priprava_cas_min=25,
            priprava_popis="Losos péct v troubě 15 min při 180°C. Kedlubnu nakrájet na plátky, opéct na pánvi s olejem.",
            vhodne_pro_meal_prep=True,
            poznamky="Omega-3, vhodné 2x týdně"
        ),
        SdilenеJidlo(
            nazev="Salát z červené řepy s vejcem",
            kategorie="obed",
            ingredience=["červená řepa", "vejce", "olivový olej", "ocet", "koření"],
            bilkoviny_na_100g=8.0,
            sacharidy_na_100g=9.0,
            tuky_na_100g=7.0,
            vlaknina_na_100g=3.0,
            kalorie_na_100g=130.0,
            priprava_cas_min=45,
            priprava_popis="Řepu uvařit (40 min) nebo použít předvařenou, nakrájet, přidat vajíčko natvrdo, ochutit.",
            vhodne_pro_meal_prep=True,
            poznamky="Klasika z Mačingovky, vydrží 3 dny"
        ),
        SdilenеJidlo(
            nazev="Krůtí maso s paprikou",
            kategorie="obed",
            ingredience=["krůtí prsa", "paprika", "cibule", "rajčata", "olivový olej"],
            bilkoviny_na_100g=24.0,
            sacharidy_na_100g=5.0,
            tuky_na_100g=5.0,
            vlaknina_na_100g=2.0,
            kalorie_na_100g=160.0,
            priprava_cas_min=25,
            priprava_popis="Krůtí nakrájet, opéct s cibulí. Přidat papriku a rajčata, dusit 10 min.",
            vhodne_pro_meal_prep=True,
            poznamky="Lehká varianta, vhodné pro večeři"
        ),
        SdilenеJidlo(
            nazev="Cottage cheese s ořechy",
            kategorie="svacina",
            ingredience=["cottage cheese", "vlašské ořechy", "skořice"],
            bilkoviny_na_100g=14.0,
            sacharidy_na_100g=4.0,
            tuky_na_100g=8.0,
            vlaknina_na_100g=1.5,
            kalorie_na_100g=140.0,
            priprava_cas_min=2,
            priprava_popis="Cottage cheese smíchat s nasekanými ořechy, posypat skořicí.",
            vhodne_pro_meal_prep=True,
            poznamky="Rychlá proteinová svačina"
        ),
        SdilenеJidlo(
            nazev="Zeleninový salát s mandlemi",
            kategorie="svacina",
            ingredience=["zelený salát", "okurka", "rajčata", "mandle", "olivový olej"],
            bilkoviny_na_100g=4.0,
            sacharidy_na_100g=5.0,
            tuky_na_100g=8.0,
            vlaknina_na_100g=3.0,
            kalorie_na_100g=110.0,
            priprava_cas_min=10,
            priprava_popis="Zeleninu nakrájet, přidat opražené mandle, ochutit olejem a citrónem.",
            vhodne_pro_meal_prep=False,
            poznamky="Čerstvé je nejlepší, mandlové výživné"
        )
    ]
    
    @staticmethod
    def najdi_jidla_podle_kategorie(kategorie: str) -> List[SdilenеJidlo]:
        """Najde všechna jídla podle kategorie."""
        return [j for j in SdilenaJidla.JIDLA if j.kategorie == kategorie]
    
    @staticmethod
    def najdi_meal_prep_jidla() -> List[SdilenеJidlo]:
        """Najde jídla vhodná pro meal prep."""
        return [j for j in SdilenaJidla.JIDLA if j.vhodne_pro_meal_prep]
    
    @staticmethod
    def najdi_rychla_jidla(max_minut: int = 15) -> List[SdilenеJidlo]:
        """Najde jídla s krátkou dobou přípravy."""
        return [j for j in SdilenaJidla.JIDLA if j.priprava_cas_min <= max_minut]


class RodinnePlanovani:
    """Nástroje pro plánování sdílených jídel."""
    
    @staticmethod
    def doporuc_tydenni_plan() -> Dict[str, List[str]]:
        """
        Doporučí týdenní plán sdílených jídel pro zjednodušení přípravy.
        """
        plan = {
            "nedele_meal_prep": [
                "Kuřecí prsa na grilu s brokolicí (4 porce)",
                "Hovězí maso s cuketou (4 porce)",
                "Losos s kedlubnou (2 porce)"
            ],
            "streda_meal_prep": [
                "Krůtí maso s paprikou (4 porce)",
                "Salát z červené řepy s vejcem (připravit řepu)"
            ],
            "denne_priprava": [
                "Vaječná omeleta se špenátem (čerstvě ráno)",
                "Svačiny: tvaroh, cottage cheese s ořechy (2 min)"
            ]
        }
        return plan
    
    @staticmethod
    def vypocti_nakupni_seznam_pro_tyden() -> Dict[str, List[str]]:
        """Vygeneruje nákupní seznam pro týdenní meal prep."""
        seznam = {
            "bilkoviny": [
                "Kuřecí prsa 1 kg",
                "Hovězí maso 800g",
                "Lososové filety 400g",
                "Krůtí prsa 800g",
                "Vejce 20 ks",
                "Tvaroh polotučný 1kg",
                "Cottage cheese 500g",
                "Tuňák v konzervě 4 ks"
            ],
            "zelenina": [
                "Brokolice 500g",
                "Cuketa 4 ks",
                "Paprika 4 ks",
                "Kedlubna 2 ks",
                "Červená řepa 4 ks",
                "Zelený salát 2 ks",
                "Špenát čerstvý 300g",
                "Okurky 4 ks",
                "Rajčata 1 kg",
                "Cibule 5 ks",
                "Česnek 1 hlávka"
            ],
            "tuky_a_orechy": [
                "Olivový olej extra virgin 500ml",
                "Máslo 250g",
                "Vlašské ořechy 200g",
                "Mandle 200g",
                "Lněné semínko mleté 250g"
            ],
            "doplnky": [
                "Citrón 3 ks",
                "Koření (sůl, pepř, kopr, skořice)",
                "Ocet 250ml"
            ]
        }
        return seznam


def main():
    """Ukázka použití sdílených jídel."""
    print("=" * 70)
    print("SDÍLENÁ JÍDLA PRO RODINU")
    print("=" * 70)
    
    print("\n🍽️  VŠECHNA SDÍLENÁ JÍDLA:\n")
    for i, jidlo in enumerate(SdilenaJidla.JIDLA, 1):
        print(f"{i}. {jidlo.nazev} ({jidlo.kategorie})")
        print(f"   Čas přípravy: {jidlo.priprava_cas_min} min")
        print(f"   Makra na 100g: B:{jidlo.bilkoviny_na_100g}g, S:{jidlo.sacharidy_na_100g}g, T:{jidlo.tuky_na_100g}g")
        print(f"   Meal prep: {'✓' if jidlo.vhodne_pro_meal_prep else '✗'}")
        print()
    
    print("\n" + "=" * 70)
    print("MEAL PREP JÍDLA (pro přípravu dopředu)")
    print("=" * 70)
    meal_prep = SdilenaJidla.najdi_meal_prep_jidla()
    for jidlo in meal_prep:
        print(f"  ✓ {jidlo.nazev} - {jidlo.poznamky}")
    
    print("\n" + "=" * 70)
    print("RYCHLÁ JÍDLA (≤15 min)")
    print("=" * 70)
    rychla = SdilenaJidla.najdi_rychla_jidla(15)
    for jidlo in rychla:
        print(f"  ⚡ {jidlo.nazev} - {jidlo.priprava_cas_min} min")
    
    print("\n" + "=" * 70)
    print("DOPORUČENÝ TÝDENNÍ PLÁN")
    print("=" * 70)
    plan = RodinnePlanovani.doporuc_tydenni_plan()
    for den, jidla in plan.items():
        print(f"\n{den.upper().replace('_', ' ')}:")
        for jidlo in jidla:
            print(f"  • {jidlo}")
    
    print("\n" + "=" * 70)
    print("NÁKUPNÍ SEZNAM PRO TÝDEN")
    print("=" * 70)
    seznam = RodinnePlanovani.vypocti_nakupni_seznam_pro_tyden()
    for kategorie, polozky in seznam.items():
        print(f"\n{kategorie.upper().replace('_', ' ')}:")
        for polozka in polozky:
            print(f"  □ {polozka}")


if __name__ == "__main__":
    main()
