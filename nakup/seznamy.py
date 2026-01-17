#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nákup - Modul pro správu nákupních seznamů a plánování nákupů

Tento modul pomáhá vytvářet a spravovat nákupní seznamy
na základě jídelníčků a aktuálních zásob.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, date


@dataclass
class NakupniPolozka:
    """Reprezentuje jednu položku v nákupním seznamu."""
    nazev: str
    mnozstvi: float  # v gramech nebo kusech
    jednotka: str  # "g", "kg", "ks", "l", "ml"
    kategorie: str  # "bilkoviny", "zelenina", "mlecne_vyrobky", atd.
    priorita: str = "normalni"  # "vysoka", "normalni", "nizka"
    odhadovana_cena: Optional[float] = None  # Kč
    koupeno: bool = False
    obchod: Optional[str] = None  # "Lidl", "Kaufland", atd.
    poznamky: Optional[str] = None


@dataclass
class NakupniSeznam:
    """Reprezentuje kompletní nákupní seznam."""
    nazev: str
    datum_vytvoreni: datetime = field(default_factory=datetime.now)
    platnost_do: Optional[date] = None
    polozky: List[NakupniPolozka] = field(default_factory=list)
    celkova_cena: float = 0.0
    dokonceno: bool = False
    
    def pridat_polozku(self, polozka: NakupniPolozka):
        """Přidá položku do seznamu."""
        self.polozky.append(polozka)
        if polozka.odhadovana_cena:
            self.celkova_cena += polozka.odhadovana_cena
    
    def odebrat_polozku(self, nazev: str):
        """Odebere položku ze seznamu."""
        for polozka in self.polozky:
            if polozka.nazev == nazev:
                if polozka.odhadovana_cena:
                    self.celkova_cena -= polozka.odhadovana_cena
                self.polozky.remove(polozka)
                break
    
    def oznacit_koupenou(self, nazev: str):
        """Označí položku jako koupenou."""
        for polozka in self.polozky:
            if polozka.nazev == nazev:
                polozka.koupeno = True
                break
    
    def ziskej_nekoupene(self) -> List[NakupniPolozka]:
        """Vrátí nekoupené položky."""
        return [p for p in self.polozky if not p.koupeno]
    
    def ziskej_podle_kategorie(self) -> Dict[str, List[NakupniPolozka]]:
        """Seskupí položky podle kategorie."""
        kategorie = {}
        for polozka in self.polozky:
            if polozka.kategorie not in kategorie:
                kategorie[polozka.kategorie] = []
            kategorie[polozka.kategorie].append(polozka)
        return kategorie
    
    def ziskej_podle_obchodu(self) -> Dict[str, List[NakupniPolozka]]:
        """Seskupí položky podle obchodu."""
        obchody = {}
        for polozka in self.polozky:
            obchod = polozka.obchod or "Neurčeno"
            if obchod not in obchody:
                obchody[obchod] = []
            obchody[obchod].append(polozka)
        return obchody
    
    def je_kompletni(self) -> bool:
        """Kontroluje, zda jsou všechny položky koupeny."""
        return all(p.koupeno for p in self.polozky)


class SpravacoNakupu:
    """Správce nákupních seznamů."""
    
    def __init__(self):
        self.seznamy: List[NakupniSeznam] = []
    
    def vytvorit_tydenni_seznam(self, tyden_od: date) -> NakupniSeznam:
        """Vytvoří základní týdenní nákupní seznam pro keto dietu."""
        seznam = NakupniSeznam(
            nazev=f"Týdenní nákup od {tyden_od.strftime('%d.%m.%Y')}",
            platnost_do=tyden_od
        )
        
        # Bílkoviny
        seznam.pridat_polozku(NakupniPolozka(
            "Kuřecí prsa", 1000, "g", "bilkoviny",
            priorita="vysoka", odhadovana_cena=150.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Hovězí maso libové", 800, "g", "bilkoviny",
            priorita="normalni", odhadovana_cena=176.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Losos čerstvý", 400, "g", "bilkoviny",
            priorita="normalni", odhadovana_cena=140.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Tuňák v konzervě", 4, "ks", "bilkoviny",
            priorita="normalni", odhadovana_cena=120.0, obchod="Lidl"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Vejce", 20, "ks", "bilkoviny",
            priorita="vysoka", odhadovana_cena=80.0, obchod="Lidl"
        ))
        
        # Mléčné výrobky
        seznam.pridat_polozku(NakupniPolozka(
            "Tvaroh polotučný", 1000, "g", "mlecne_vyrobky",
            priorita="vysoka", odhadovana_cena=45.0, obchod="Lidl"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Cottage cheese", 500, "g", "mlecne_vyrobky",
            priorita="normalni", odhadovana_cena=50.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Řecký jogurt", 500, "g", "mlecne_vyrobky",
            priorita="normalni", odhadovana_cena=30.0, obchod="Lidl"
        ))
        
        # Zelenina
        seznam.pridat_polozku(NakupniPolozka(
            "Brokolice", 500, "g", "zelenina",
            priorita="vysoka", odhadovana_cena=25.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Špenát čerstvý", 300, "g", "zelenina",
            priorita="normalni", odhadovana_cena=24.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Cuketa", 4, "ks", "zelenina",
            priorita="normalni", odhadovana_cena=60.0, obchod="Lidl"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Paprika", 4, "ks", "zelenina",
            priorita="normalni", odhadovana_cena=60.0, obchod="Lidl"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Rajčata", 1000, "g", "zelenina",
            priorita="normalni", odhadovana_cena=45.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Okurky", 4, "ks", "zelenina",
            priorita="normalni", odhadovana_cena=35.0, obchod="Lidl"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Zelený salát", 2, "ks", "zelenina",
            priorita="normalni", odhadovana_cena=40.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Kedlubna", 2, "ks", "zelenina",
            priorita="nizka", odhadovana_cena=20.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Červená řepa", 4, "ks", "zelenina",
            priorita="nizka", odhadovana_cena=20.0, obchod="Lidl"
        ))
        
        # Tuky a ořechy
        seznam.pridat_polozku(NakupniPolozka(
            "Olivový olej extra virgin", 500, "ml", "tuky",
            priorita="vysoka", odhadovana_cena=90.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Máslo", 250, "g", "tuky",
            priorita="normalni", odhadovana_cena=40.0, obchod="Lidl"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Mandle", 200, "g", "orechy",
            priorita="normalni", odhadovana_cena=56.0, obchod="Lidl"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Vlašské ořechy", 200, "g", "orechy",
            priorita="normalni", odhadovana_cena=50.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Lněné semínko mleté", 250, "g", "orechy",
            priorita="vysoka", odhadovana_cena=30.0, obchod="Kaufland"
        ))
        
        # Koření a doplňky
        seznam.pridat_polozku(NakupniPolozka(
            "Česnek", 1, "ks", "koreni",
            priorita="normalni", odhadovana_cena=10.0, obchod="Lidl"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Citrony", 3, "ks", "koreni",
            priorita="normalni", odhadovana_cena=30.0, obchod="Kaufland"
        ))
        seznam.pridat_polozku(NakupniPolozka(
            "Skořice", 1, "ks", "koreni",
            priorita="nizka", odhadovana_cena=25.0, obchod="Kaufland"
        ))
        
        self.seznamy.append(seznam)
        return seznam
    
    def najdi_seznam(self, nazev: str) -> Optional[NakupniSeznam]:
        """Najde seznam podle názvu."""
        for seznam in self.seznamy:
            if seznam.nazev == nazev:
                return seznam
        return None
    
    def ziskej_aktivni_seznamy(self) -> List[NakupniSeznam]:
        """Vrátí nedokončené seznamy."""
        return [s for s in self.seznamy if not s.dokonceno]


def main():
    """Ukázka použití modulu nákupu."""
    print("=" * 70)
    print("SPRÁVA NÁKUPNÍCH SEZNAMŮ")
    print("=" * 70)
    
    # Vytvoření týdenního seznamu
    spravce = SpravacoNakupu()
    tyden_od = date.today()
    seznam = spravce.vytvorit_tydenni_seznam(tyden_od)
    
    print(f"\n📋 {seznam.nazev}")
    print(f"Datum vytvoření: {seznam.datum_vytvoreni.strftime('%d.%m.%Y %H:%M')}")
    print(f"Celková cena: {seznam.celkova_cena:.2f} Kč")
    print(f"Počet položek: {len(seznam.polozky)}")
    
    # Zobrazení podle kategorií
    print("\n" + "=" * 70)
    print("NÁKUPNÍ SEZNAM PODLE KATEGORIÍ")
    print("=" * 70)
    
    kategorie = seznam.ziskej_podle_kategorie()
    for kat, polozky in sorted(kategorie.items()):
        print(f"\n{kat.upper().replace('_', ' ')}:")
        for p in polozky:
            priorita_znak = "🔴" if p.priorita == "vysoka" else "🟡" if p.priorita == "normalni" else "🟢"
            print(f"  {priorita_znak} □ {p.nazev} - {p.mnozstvi} {p.jednotka} ({p.odhadovana_cena:.0f} Kč)")
    
    # Zobrazení podle obchodů
    print("\n" + "=" * 70)
    print("NÁKUP PODLE OBCHODŮ")
    print("=" * 70)
    
    obchody = seznam.ziskej_podle_obchodu()
    for obchod, polozky in sorted(obchody.items()):
        cena_celkem = sum(p.odhadovana_cena or 0 for p in polozky)
        print(f"\n🏪 {obchod.upper()} - {cena_celkem:.2f} Kč:")
        for p in polozky:
            print(f"  □ {p.nazev} - {p.mnozstvi} {p.jednotka}")
    
    print("\n" + "=" * 70)
    print("✅ Nákupní seznam připraven!")
    print("=" * 70)


if __name__ == "__main__":
    main()
