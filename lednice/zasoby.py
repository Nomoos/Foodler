#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lednice - Modul pro správu zásob potravin doma

Tento modul sleduje, jaké potraviny máte doma, jejich množství
a datum expirace.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta


@dataclass
class ZasobaPolozka:
    """Reprezentuje jednu položku v zásobách."""
    nazev: str
    mnozstvi: float  # v gramech nebo kusech
    jednotka: str  # "g", "kg", "ks", "l", "ml"
    kategorie: str  # "bilkoviny", "zelenina", "mlecne_vyrobky", atd.
    datum_nakupu: date
    datum_expirace: Optional[date] = None
    umisteni: str = "lednice"  # "lednice", "mrazak", "spiz"
    otevreno: bool = False
    poznamky: Optional[str] = None
    
    def je_cerstva(self) -> bool:
        """Kontroluje, zda položka není prošlá."""
        if not self.datum_expirace:
            return True
        return date.today() <= self.datum_expirace
    
    def dny_do_expirace(self) -> Optional[int]:
        """Vrátí počet dní do expirace."""
        if not self.datum_expirace:
            return None
        delta = self.datum_expirace - date.today()
        return delta.days
    
    def je_na_dohled_expirace(self, dny: int = 3) -> bool:
        """Kontroluje, zda položka brzy vyprší."""
        dny_do_exp = self.dny_do_expirace()
        if dny_do_exp is None:
            return False
        return 0 <= dny_do_exp <= dny


@dataclass
class Lednice:
    """Reprezentuje zásoby v lednici/domácnosti."""
    nazev: str = "Domácí zásoby"
    polozky: List[ZasobaPolozka] = field(default_factory=list)
    
    def pridat_polozku(self, polozka: ZasobaPolozka):
        """Přidá položku do zásob."""
        # Zkontrolovat, zda položka již existuje
        existujici = self.najdi_polozku(polozka.nazev, polozka.umisteni)
        if existujici:
            # Přidat k existujícímu množství
            existujici.mnozstvi += polozka.mnozstvi
        else:
            self.polozky.append(polozka)
    
    def odebrat_polozku(self, nazev: str, mnozstvi: float, umisteni: str = "lednice"):
        """Odebere množství z položky."""
        polozka = self.najdi_polozku(nazev, umisteni)
        if polozka:
            polozka.mnozstvi -= mnozstvi
            if polozka.mnozstvi <= 0:
                self.polozky.remove(polozka)
    
    def najdi_polozku(self, nazev: str, umisteni: str = "lednice") -> Optional[ZasobaPolozka]:
        """Najde položku podle názvu a umístění."""
        for polozka in self.polozky:
            if polozka.nazev.lower() == nazev.lower() and polozka.umisteni == umisteni:
                return polozka
        return None
    
    def ziskej_podle_umisteni(self, umisteni: str) -> List[ZasobaPolozka]:
        """Vrátí položky podle umístění."""
        return [p for p in self.polozky if p.umisteni == umisteni]
    
    def ziskej_podle_kategorie(self) -> Dict[str, List[ZasobaPolozka]]:
        """Seskupí položky podle kategorie."""
        kategorie = {}
        for polozka in self.polozky:
            if polozka.kategorie not in kategorie:
                kategorie[polozka.kategorie] = []
            kategorie[polozka.kategorie].append(polozka)
        return kategorie
    
    def ziskej_brzy_expiruji(self, dny: int = 3) -> List[ZasobaPolozka]:
        """Vrátí položky, které brzy vyprší."""
        return [p for p in self.polozky if p.je_na_dohled_expirace(dny)]
    
    def ziskej_prosle(self) -> List[ZasobaPolozka]:
        """Vrátí prošlé položky."""
        return [p for p in self.polozky if not p.je_cerstva()]
    
    def co_muzu_uvarit(self, potrebne_ingredience: List[str]) -> bool:
        """Zkontroluje, zda máte všechny ingredience."""
        for ingredience in potrebne_ingredience:
            if not any(p.nazev.lower() == ingredience.lower() for p in self.polozky):
                return False
        return True
    
    def celkova_hodnota(self, ceny: Dict[str, float]) -> float:
        """Vypočítá celkovou hodnotu zásob podle cen za kg."""
        celkem = 0.0
        for polozka in self.polozky:
            if polozka.nazev in ceny:
                # Převést na kg
                mnozstvi_kg = polozka.mnozstvi / 1000 if polozka.jednotka == "g" else polozka.mnozstvi
                celkem += mnozstvi_kg * ceny[polozka.nazev]
        return celkem


class SpravceZasob:
    """Správce domácích zásob."""
    
    def __init__(self):
        self.lednice = Lednice()
    
    def naplnit_prikladove_zasoby(self):
        """Naplní lednici příkladovými zásobami."""
        dnes = date.today()
        
        # Bílkoviny
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Kuřecí prsa", 600, "g", "bilkoviny",
            datum_nakupu=dnes - timedelta(days=1),
            datum_expirace=dnes + timedelta(days=3),
            umisteni="lednice"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Hovězí maso", 400, "g", "bilkoviny",
            datum_nakupu=dnes - timedelta(days=2),
            datum_expirace=dnes + timedelta(days=2),
            umisteni="lednice"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Losos", 200, "g", "bilkoviny",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=2),
            umisteni="mrazak"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Tuňák kousky v oleji", 750, "g", "bilkoviny",
            datum_nakupu=dnes - timedelta(days=5),
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz",
            poznamky="Sun&Sea 750g, konzervovaný"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Vejce slepičí M", 40, "ks", "bilkoviny",
            datum_nakupu=dnes - timedelta(days=3),
            datum_expirace=dnes + timedelta(days=18),
            umisteni="lednice",
            poznamky="Velikost M (55g/ks), celkem 2200g"
        ))
        
        # Mléčné výrobky
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Tvaroh polotučný", 500, "g", "mlecne_vyrobky",
            datum_nakupu=dnes - timedelta(days=1),
            datum_expirace=dnes + timedelta(days=4),
            umisteni="lednice",
            otevreno=True
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Cottage cheese", 200, "g", "mlecne_vyrobky",
            datum_nakupu=dnes - timedelta(days=2),
            datum_expirace=dnes + timedelta(days=3),
            umisteni="lednice",
            otevreno=True
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Sýr gouda 45%", 300, "g", "mlecne_vyrobky",
            datum_nakupu=dnes - timedelta(days=2),
            datum_expirace=dnes + timedelta(days=14),
            umisteni="lednice",
            poznamky="Polotvrdý sýr"
        ))
        
        # Zelenina
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Brokolice", 300, "g", "zelenina",
            datum_nakupu=dnes - timedelta(days=1),
            datum_expirace=dnes + timedelta(days=4),
            umisteni="lednice"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Špenát", 200, "g", "zelenina",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=3),
            umisteni="lednice"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Cuketa", 2, "ks", "zelenina",
            datum_nakupu=dnes - timedelta(days=2),
            datum_expirace=dnes + timedelta(days=5),
            umisteni="lednice"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Paprika", 3, "ks", "zelenina",
            datum_nakupu=dnes - timedelta(days=1),
            datum_expirace=dnes + timedelta(days=6),
            umisteni="lednice"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Ledový salát", 1, "ks", "zelenina",
            datum_nakupu=dnes - timedelta(days=1),
            datum_expirace=dnes + timedelta(days=4),
            umisteni="lednice",
            poznamky="Hlávka (~500g)"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Kysané zelí", 500, "g", "zelenina",
            datum_nakupu=dnes - timedelta(days=3),
            datum_expirace=dnes + timedelta(days=30),
            umisteni="lednice",
            poznamky="Fermentované, probiotické"
        ))
        
        # Tuky a ořechy
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Olivový olej", 300, "ml", "tuky",
            datum_nakupu=dnes - timedelta(days=30),
            datum_expirace=dnes + timedelta(days=335),
            umisteni="spiz",
            otevreno=True
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Mandle", 150, "g", "orechy",
            datum_nakupu=dnes - timedelta(days=10),
            datum_expirace=dnes + timedelta(days=80),
            umisteni="spiz"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Lněné semínko", 100, "g", "orechy",
            datum_nakupu=dnes - timedelta(days=5),
            datum_expirace=dnes + timedelta(days=25),
            umisteni="spiz",
            otevreno=True
        ))
    
    def vypis_inventar(self):
        """Vypíše kompletní inventář."""
        print("=" * 70)
        print("DOMÁCÍ ZÁSOBY - INVENTÁŘ")
        print("=" * 70)
        
        umisteni_map = {
            "lednice": "🧊 LEDNICE",
            "mrazak": "❄️  MRAZÁK",
            "spiz": "🏠 SPÍŽ"
        }
        
        for umisteni, nazev in umisteni_map.items():
            polozky = self.lednice.ziskej_podle_umisteni(umisteni)
            if polozky:
                print(f"\n{nazev}:")
                for p in polozky:
                    dny_exp = p.dny_do_expirace()
                    exp_text = f"(vyprší za {dny_exp} dní)" if dny_exp is not None else ""
                    otevreno_text = " [OTEVŘENO]" if p.otevreno else ""
                    print(f"  • {p.nazev} - {p.mnozstvi} {p.jednotka} {exp_text}{otevreno_text}")
    
    def upozorneni_expirace(self):
        """Zobrazí upozornění na expiraci."""
        print("\n" + "=" * 70)
        print("⚠️  UPOZORNĚNÍ NA EXPIRACI")
        print("=" * 70)
        
        brzy_expiruji = self.lednice.ziskej_brzy_expiruji(3)
        if brzy_expiruji:
            print("\n🟡 Brzy vyprší (do 3 dnů):")
            for p in brzy_expiruji:
                dny = p.dny_do_expirace()
                print(f"  • {p.nazev} - zbývá {dny} dní")
        
        prosle = self.lednice.ziskej_prosle()
        if prosle:
            print("\n🔴 Prošlé položky:")
            for p in prosle:
                dny = abs(p.dny_do_expirace()) if p.dny_do_expirace() else 0
                print(f"  • {p.nazev} - prošlé o {dny} dní")
        
        if not brzy_expiruji and not prosle:
            print("\n✅ Vše je v pořádku, žádné položky brzy nevyprší.")


def main():
    """Ukázka použití modulu lednice."""
    print("=" * 70)
    print("SPRÁVA DOMÁCÍCH ZÁSOB")
    print("=" * 70)
    
    # Vytvoření správce a naplnění příkladovými zásobami
    spravce = SpravceZasob()
    spravce.naplnit_prikladove_zasoby()
    
    # Výpis inventáře
    spravce.vypis_inventar()
    
    # Upozornění na expiraci
    spravce.upozorneni_expirace()
    
    # Test, co lze uvařit
    print("\n" + "=" * 70)
    print("CO MOHU UVAŘIT?")
    print("=" * 70)
    
    recepty = [
        ("Kuřecí prsa s brokolicí", ["Kuřecí prsa", "Brokolice", "Olivový olej"]),
        ("Losos s kedlubnou", ["Losos", "Kedlubna", "Olivový olej"]),
        ("Omeleta se špenátem", ["Vejce", "Špenát"]),
    ]
    
    for nazev, ingredience in recepty:
        muzu = spravce.lednice.co_muzu_uvarit(ingredience)
        status = "✅" if muzu else "❌"
        print(f"{status} {nazev}")
        if not muzu:
            chybi = [i for i in ingredience if not any(p.nazev.lower() == i.lower() for p in spravce.lednice.polozky)]
            print(f"   Chybí: {', '.join(chybi)}")


if __name__ == "__main__":
    main()
