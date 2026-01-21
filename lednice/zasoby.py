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
        # NÁKUP 18.1.2026 - Vejce M30 (2x balení)
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Vejce slepičí M", 60, "ks", "bilkoviny",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 5),
            umisteni="lednice",
            poznamky="Velikost M30, 2x balení po 30 ks, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Utopenci
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Utopenci", 1550, "g", "bilkoviny",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 15),
            umisteni="lednice",
            poznamky="Delikatesní 1550g, nakládané"
        ))
        
        # Mléčné výrobky
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Tvaroh polotučný", 500, "g", "mlecne_vyrobky",
            datum_nakupu=dnes - timedelta(days=1),
            datum_expirace=dnes + timedelta(days=4),
            umisteni="lednice",
            otevreno=True
        ))
        # NÁKUP 18.1.2026 - Cottage cheese s pažitkou
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Cottage cheese pažitka", 180, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 1, 28),
            umisteni="lednice",
            poznamky="Meggle cottage s pažitkou, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Sýr Gouda Light (4 kusy)
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Sýr gouda light", 867, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 15),
            umisteni="lednice",
            poznamky="4 kusy: 249g + 232g + 200g + 186g, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Sýr Císařský 45%
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Sýr císařský 45%", 343, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 8),
            umisteni="lednice",
            poznamky="2 kusy: 173g + 170g, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Král sýrů přírodní
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Král sýrů přírodní", 480, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 15),
            umisteni="lednice",
            poznamky="4x 120g, Président, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Král sýrů pepř
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Král sýrů pepř", 240, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 15),
            umisteni="lednice",
            poznamky="2x 120g, Président s pepřem, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Mascarpone
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Mascarpone", 500, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 8),
            umisteni="lednice",
            poznamky="2x 250g, italský smetanový sýr, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Řecký jogurt 5% (2x 1kg)
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Řecký jogurt 5%", 2000, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 1),
            umisteni="lednice",
            poznamky="2x 1kg, řecký jogurt 5% tuku, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Řecký jogurt natural 1kg
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Řecký jogurt natural", 1000, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 1),
            umisteni="lednice",
            poznamky="1x 1kg, řecký jogurt natural, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Mozzarella
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Mozzarella", 250, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 5),
            umisteni="lednice",
            poznamky="2x 125g, italská mozzarella, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Řecké jogurty ochucené (různé příchutě)
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Řecký jogurt malinový", 280, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 1, 30),
            umisteni="lednice",
            poznamky="2x 140g, řecký jogurt malinový, Globus nákup"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Řecký jogurt hruška", 280, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 1, 30),
            umisteni="lednice",
            poznamky="2x 140g, řecký jogurt hruškový, Globus nákup"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Řecký jogurt meruňka", 140, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 1, 30),
            umisteni="lednice",
            poznamky="1x 140g, řecký jogurt meruňkový, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Ostatní jogurty
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Jogurt nugát", 150, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 1, 28),
            umisteni="lednice",
            poznamky="Ochucený jogurt, Globus nákup"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Jogurt borůvka", 150, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 1, 28),
            umisteni="lednice",
            poznamky="Ochucený jogurt, Globus nákup"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "BIO jogurt jahoda", 180, "g", "mlecne_vyrobky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 1, 30),
            umisteni="lednice",
            poznamky="Hollandia BIO jahodový, Globus nákup"
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
        # NÁKUP 18.1.2026 - Celer bulvový
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Celer bulvový", 2930, "g", "zelenina",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 8),
            umisteni="lednice",
            poznamky="2.93 kg, čerstvý, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Pažitka v květináči
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Pažitka v květináči", 1, "ks", "zelenina",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 28),
            umisteni="lednice",
            poznamky="Živá bylinková rostlina, Globus nákup"
        ))
        # Bílá redkev - potřebuje spotřebovat
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Bílá redkev", 1, "ks", "zelenina",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=2),
            umisteni="lednice",
            poznamky="Potřebuje rychle spotřebovat"
        ))
        
        # Tuky a ořechy
        # NÁKUP 18.1.2026 - Olivový olej 1L
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Olivový olej", 1000, "ml", "tuky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2027, 1, 18),
            umisteni="spiz",
            poznamky="Gusto Andalusia 1L, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Rýžový olej
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Rýžový olej", 750, "ml", "tuky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2027, 1, 18),
            umisteni="spiz",
            poznamky="750 ml, pro smažení a pečení, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Dýňový olej
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Dýňový olej", 250, "ml", "tuky",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2027, 1, 18),
            umisteni="spiz",
            poznamky="Gusto Andalusia 250ml, pro saláty, Globus nákup"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "MCT olej v prášku", 250, "g", "tuky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz",
            poznamky="Keto doplněk stravy"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Mandle", 150, "g", "orechy",
            datum_nakupu=dnes - timedelta(days=10),
            datum_expirace=dnes + timedelta(days=80),
            umisteni="spiz"
        ))
        # NÁKUP 18.1.2026 - Kešu ořechy
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Kešu ořechy pražené", 200, "g", "orechy",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 7, 18),
            umisteni="spiz",
            poznamky="200g, pražené nesolené, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Pekanové ořechy
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Pekanové ořechy", 200, "g", "orechy",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 7, 18),
            umisteni="spiz",
            poznamky="200g, premium ořechy, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Dýňová semínka
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Dýňová semínka", 200, "g", "orechy",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 7, 18),
            umisteni="spiz",
            poznamky="200g, bohaté na zinek a hořčík, Globus nákup"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Lněné semínko", 100, "g", "orechy",
            datum_nakupu=dnes - timedelta(days=5),
            datum_expirace=dnes + timedelta(days=25),
            umisteni="spiz",
            otevreno=True
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Chia semínka", 200, "g", "orechy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz",
            poznamky="Bohaté na omega-3 a vlákninu"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Sezam bílý", 150, "g", "orechy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=90),
            umisteni="spiz",
            poznamky="Zdroj vápníku"
        ))
        
        # Mléčné výrobky a ostatní
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Mléko polotučné", 1000, "ml", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=5),
            umisteni="lednice",
            poznamky="1.5% tuku"
        ))
        
        # Ovoce
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Mango", 1, "ks", "ovoce",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=5),
            umisteni="lednice",
            poznamky="~300g"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Avokádo", 2, "ks", "ovoce",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=4),
            umisteni="lednice",
            poznamky="Zdroj zdravých tuků"
        ))
        # NÁKUP 18.1.2026 - Jablka červená
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Jablka červená", 1290, "g", "ovoce",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 8),
            umisteni="lednice",
            poznamky="1.29 kg, čerstvá, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Borůvky
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Borůvky", 125, "g", "ovoce",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 1, 25),
            umisteni="lednice",
            poznamky="125g, čerstvé, bohaté na antioxidanty, Globus nákup"
        ))
        
        # Sacharidy a ostatní
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Těstoviny", 500, "g", "sacharidy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Brambory", 2000, "g", "sacharidy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=14),
            umisteni="spiz",
            poznamky="Pro Kubíka"
        ))
        # NÁKUP 18.1.2026 - Rýže basmati 5kg
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Rýže basmati", 5000, "g", "sacharidy",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2027, 1, 18),
            umisteni="spiz",
            poznamky="5 kg balení, pro Kubíka, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Čočka velkozrnná
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Čočka velkozrnná", 500, "g", "sacharidy",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2027, 1, 18),
            umisteni="spiz",
            poznamky="500g, bohatá na bílkoviny, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - BIO pohankové vločky
        self.lednice.pridat_polozku(ZasobaPolozka(
            "BIO pohankové vločky", 500, "g", "sacharidy",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 7, 18),
            umisteni="spiz",
            poznamky="2x 250g, BIO kvalita, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - BIO ovesné vločky
        self.lednice.pridat_polozku(ZasobaPolozka(
            "BIO ovesné vločky", 1000, "g", "sacharidy",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 7, 18),
            umisteni="spiz",
            poznamky="2x 500g, BIO kvalita, Globus nákup"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Krupice", 500, "g", "sacharidy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Mouka hladká", 1000, "g", "sacharidy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz"
        ))
        
        # Ostatní
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Med", 500, "g", "ostatni",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz",
            poznamky="Přírodní sladidlo"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Drožní čerstvé", 84, "g", "ostatni",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=14),
            umisteni="lednice",
            poznamky="2 ks x 42g"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Cukr", 1000, "g", "ostatni",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Iso whey prozero Nutrend", 1000, "g", "bilkoviny",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz",
            poznamky="Chocolate brownies, proteinový prášek"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Mana", 400, "g", "ostatni",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz",
            poznamky="Kompletní jídlo v prášku"
        ))
        # NÁKUP 18.1.2026 - BIO goji
        self.lednice.pridat_polozku(ZasobaPolozka(
            "BIO goji", 100, "g", "ostatni",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 7, 18),
            umisteni="spiz",
            poznamky="2x balení, BIO superfoods, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Švestky půlené
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Švestky půlené", 660, "g", "ovoce",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 7, 18),
            umisteni="spiz",
            poznamky="660g konzervované, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Fíky sušené
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Fíky sušené kolečka", 600, "g", "ovoce",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 7, 18),
            umisteni="spiz",
            poznamky="3x 200g, sušené fíky, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Jedlá soda
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Jedlá soda", 2000, "g", "ostatni",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2028, 1, 18),
            umisteni="spiz",
            poznamky="2x 1kg, bikarbona, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Olivy zelené
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Olivy zelené", 880, "g", "ostatni",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2027, 1, 18),
            umisteni="spiz",
            poznamky="Gusto Andalusia 880g, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Koření
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Kmín celý", 30, "g", "ostatni",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2027, 1, 18),
            umisteni="spiz",
            poznamky="30g, Globus nákup"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Nové koření celé", 12, "g", "ostatni",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2027, 1, 18),
            umisteni="spiz",
            poznamky="12g, piment, Globus nákup"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Petržel sušená", 7, "g", "ostatni",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2027, 1, 18),
            umisteni="spiz",
            poznamky="7g, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Pečicí papír
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Pečicí papír", 20, "m", "ostatni",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2028, 1, 18),
            umisteni="spiz",
            poznamky="20 metrů, Globus nákup"
        ))
        # NÁKUP 18.1.2026 - Vitamíny/šťávy pro děti
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Vitamínová šťáva jablko-jahoda", 150, "ml", "ostatni",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 18),
            umisteni="lednice",
            poznamky="150ml, Vitar, pro Kubíka, Globus nákup"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Vitamínová šťáva jablko-rakytník", 150, "ml", "ostatni",
            datum_nakupu=date(2026, 1, 18),
            datum_expirace=date(2026, 2, 18),
            umisteni="lednice",
            poznamky="150ml, Vitar, pro Kubíka, Globus nákup"
        ))
    
    def naplnit_zasoby_z_nakupu_globus_20260118(self):
        """
        Naplní lednici položkami z nákupu Globus z 18.1.2026.
        Kompletní nákup za 3708 Kč s 40 položkami.
        """
        datum_nakupu = date(2026, 1, 18)
        dnes = datum_nakupu
        
        # Mléčné výrobky a vejce
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Vejce M30 podestýlkové", 60, "ks", "bilkoviny",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=21),
            umisteni="lednice",
            poznamky="2 balení po 30 ks, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Sýr Císařský 45%", 173, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=14),
            umisteni="lednice",
            poznamky="Polotvrdý sýr, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Sýr Císařský uzený 44%", 170, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=14),
            umisteni="lednice",
            poznamky="Uzený polotvrdý, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Sýr Gouda Light", 867, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=14),
            umisteni="lednice",
            poznamky="4 kusy (249g+232g+200g+186g), Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Král sýrů přírodní", 480, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=10),
            umisteni="lednice",
            poznamky="4x 120g, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Král sýrů s pepřem", 240, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=10),
            umisteni="lednice",
            poznamky="2x 120g, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Mascarpone", 500, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=7),
            umisteni="lednice",
            poznamky="2x 250g, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Cottage cheese s pažitkou", 180, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=5),
            umisteni="lednice",
            poznamky="180g, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Řecký jogurt 5%", 2000, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=10),
            umisteni="lednice",
            poznamky="2x 1kg, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Řecký jogurt natural", 1000, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=10),
            umisteni="lednice",
            poznamky="1kg, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Mozzarella", 250, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=14),
            umisteni="lednice",
            poznamky="2x 125g, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Jogurt nugát", 150, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=7),
            umisteni="lednice",
            poznamky="Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Jogurt borůvka", 150, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=7),
            umisteni="lednice",
            poznamky="Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Bio jogurt jahoda", 180, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=7),
            umisteni="lednice",
            poznamky="Bio, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Řecký jogurt malina", 280, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=7),
            umisteni="lednice",
            poznamky="2x 140g, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Řecký jogurt hruška", 280, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=7),
            umisteni="lednice",
            poznamky="2x 140g, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Řecký jogurt meruňka", 140, "g", "mlecne_vyrobky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=7),
            umisteni="lednice",
            poznamky="140g, Globus 18.1.2026"
        ))
        
        # Zelenina a ovoce
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Jablka červená", 1290, "g", "ovoce",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=14),
            umisteni="lednice",
            poznamky="Čerstvá, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Celer bulvový", 2930, "g", "zelenina",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=10),
            umisteni="lednice",
            poznamky="2.93 kg, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Borůvky", 125, "g", "ovoce",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=3),
            umisteni="lednice",
            poznamky="Rychle spotřebovat, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Pažitka v květináči", 1, "ks", "zelenina",
            datum_nakupu=dnes,
            datum_expirace=None,
            umisteni="kuchyne",
            poznamky="Živá rostlina, Globus 18.1.2026"
        ))
        
        # Ořechy a semínka
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Kešu ořechy pražené", 200, "g", "orechy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=90),
            umisteni="spiz",
            poznamky="200g nesolené, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Pekanové ořechy", 200, "g", "orechy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=90),
            umisteni="spiz",
            poznamky="200g premium, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Dýňová semínka", 200, "g", "orechy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz",
            poznamky="200g, zinek a hořčík, Globus 18.1.2026"
        ))
        
        # Tuky a oleje
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Olivový olej", 1000, "ml", "tuky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz",
            poznamky="1L, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Rýžový olej", 750, "ml", "tuky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz",
            poznamky="750ml, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Dýňový olej", 250, "ml", "tuky",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz",
            poznamky="250ml styrijský, Globus 18.1.2026"
        ))
        
        # Sacharidy (pro Kubíka)
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Rýže basmati", 5000, "g", "sacharidy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz",
            poznamky="5kg pro Kubíka, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Bio pohankové vločky", 500, "g", "sacharidy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz",
            poznamky="2x 250g, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Bio ovesné vločky", 1000, "g", "sacharidy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz",
            poznamky="2x 500g, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Čočka velkozrnná", 500, "g", "sacharidy",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz",
            poznamky="500g, Globus 18.1.2026"
        ))
        
        # Ostatní
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Bio Goji", 100, "g", "ovoce",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=90),
            umisteni="spiz",
            poznamky="Sušené bobule, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Utopenci", 1550, "g", "ostatni",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=30),
            umisteni="lednice",
            poznamky="Nakládaná klobása, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Olivy zelené", 880, "g", "zelenina",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz",
            poznamky="Konzervované, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Švestky půlené sušené", 660, "g", "ovoce",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz",
            poznamky="Sušené, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Fíky sušené", 600, "g", "ovoce",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=180),
            umisteni="spiz",
            poznamky="3x 200g, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Kmín celý", 30, "g", "koreni",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz",
            poznamky="Koření, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Nové koření", 12, "g", "koreni",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz",
            poznamky="Koření, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Petržel sušená", 7, "g", "koreni",
            datum_nakupu=dnes,
            datum_expirace=dnes + timedelta(days=365),
            umisteni="spiz",
            poznamky="Koření, Globus 18.1.2026"
        ))
        self.lednice.pridat_polozku(ZasobaPolozka(
            "Jedlá soda", 1000, "g", "ostatni",
            datum_nakupu=dnes,
            datum_expirace=None,
            umisteni="spiz",
            poznamky="Kypřící prášek, Globus 18.1.2026"
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
