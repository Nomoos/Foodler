#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Osobní preference a omezení pro Osobu 2 - Pája (Pavla)

Obsahuje:
- PreferenceJidel: základní preference a texturové preference
- DietniOmezeni: dietní limity a doporučení
- HladAEnergie: vzorce hladu a energetických úrovní
- StrukturaJidel: preference ohledně časování a velikosti porcí
- SyticiJidla: jídla, která dobře sytí
- ProblematickaJidla: jídla, která chutnají, ale nesedí
- ReakceTela: tělesné reakce na jídlo (nadýmání, únava, chutě)
"""

from typing import List, Dict, Optional, Any, Union


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
    
    # Potraviny se slizkou/kluzkou konzistencí (texture preference)
    # Note: Includes items from NEPREFERRED_FOODS plus additional slimy-textured foods
    # This allows for granular control via the kontrolovat_texturu parameter
    SLIMY_TEXTURED_FOODS: List[str] = [
        "houby",           # všechny druhy hub
        "houb",            # variace (houbová omáčka)
        "hříbky",
        "hříbk",           # variace (hříbková polévka)
        "žampiony",
        "žampion",         # variace (žampionová omáčka)
        "hlíva",
        "hlív",            # variace (hlívová polévka)
        "shiitake",
        "lilek",           # může být slizký po vaření
        "okra",            # velmi slizká zelenina
        "okr",             # variace
        "ustřice",         # slizká textura
        "ústřice",
        "slimáci",         # velmi slizká textura
        "slimák",
        "žabí stehýnka",   # slizká textura
        "mořské řasy",     # mohou být slizké
        "řasy",
        "řas",             # variace (s řasami)
        "aloe vera",       # slizká konzistence
        "chobotnice",      # může mít slizkou texturu
        "chobotnic",       # variace
        "syrová vejce",    # slizká konzistence
        "syrové vejce",
        "rosolovité pokrmy",
        "rosol"
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
    def je_jidlo_vhodne(jidlo: str, kontrolovat_texturu: bool = True) -> bool:
        """
        Zkontroluje, zda jídlo neobsahuje nepreferované ingredience.
        
        Args:
            jidlo: Název nebo popis jídla
            kontrolovat_texturu: Pokud True, kontroluje i slizké textury
            
        Returns:
            True pokud je jídlo vhodné, False pokud obsahuje nepreferované složky
        """
        jidlo_lower = jidlo.lower()
        
        # Kontrola běžných nepreferovaných potravin
        for nepref in PreferenceJidel.NEPREFERRED_FOODS:
            if nepref in jidlo_lower:
                return False
        
        # Kontrola slizké/kluzké konzistence
        if kontrolovat_texturu:
            for slimy in PreferenceJidel.SLIMY_TEXTURED_FOODS:
                if slimy in jidlo_lower:
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
            "slizke_textury": PreferenceJidel.SLIMY_TEXTURED_FOODS,
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


class HladAEnergie:
    """
    Vzorce hladu a energetických úrovní.
    
    Na základě osobních odpovědí o hladu, energii a pocitových stavech.
    """
    
    # Denní vzorce hladu
    NEJVYSSI_HLAD: str = "ráno"
    
    # Energetické stavy
    POCIT_BEZ_ENERGIE_PRI_SPRAVNEM_JIDLE: bool = False  # "spíše ne"
    
    # Přejedení
    PREJEDENI_BEZ_HLADU: bool = True  # "ano"
    
    # Co je horší
    HORSI_POCIT: str = "plnost/těžkost"  # vs. hlad
    
    # Klíčové poznámky
    POZNAMKY: List[str] = [
        "Citlivost na objem jídla, ne na kalorickou hodnotu",
        "Pocit plnosti a těžkosti je horší než hlad",
        "Přejedení se děje i bez pocitu hladu"
    ]
    
    @staticmethod
    def ziskej_prehled() -> Dict[str, Any]:
        """Vrátí přehled vzorců hladu a energie."""
        return {
            "nejvyssi_hlad": HladAEnergie.NEJVYSSI_HLAD,
            "pocit_bez_energie": HladAEnergie.POCIT_BEZ_ENERGIE_PRI_SPRAVNEM_JIDLE,
            "prejedeni_bez_hladu": HladAEnergie.PREJEDENI_BEZ_HLADU,
            "horsi_pocit": HladAEnergie.HORSI_POCIT,
            "poznamky": HladAEnergie.POZNAMKY
        }


class StrukturaJidel:
    """
    Preference ohledně struktury dne a velikosti porcí.
    
    Identifikuje problematická jídla a preferované rozložení jídel během dne.
    """
    
    # Problematické jídlo
    NEJPROBLEMATICTEJSI_JIDLO: str = "oběd"
    DUVOD_PROBLEMU: str = "moc velké porce"
    
    # Preference
    PREFERENCE_PORCI: str = "rovnoměrnější porce během dne"
    
    # Doporučení
    DOPORUCENI: List[str] = [
        "Zmenšit porce u oběda",
        "Rozdělit kalorie rovnoměrněji mezi všechna jídla",
        "Více menších jídel místo jednoho velkého oběda"
    ]
    
    @staticmethod
    def ziskej_doporuceni_porci() -> Dict[str, Union[str, List[str]]]:
        """Vrátí doporučení pro velikost porcí."""
        return {
            "problematicke_jidlo": StrukturaJidel.NEJPROBLEMATICTEJSI_JIDLO,
            "duvod": StrukturaJidel.DUVOD_PROBLEMU,
            "preference": StrukturaJidel.PREFERENCE_PORCI,
            "doporuceni": StrukturaJidel.DOPORUCENI
        }


class SyticiJidla:
    """
    Jídla, která dobře sytí.
    
    Klíčové zjištění: funguje vláknina + objem + jemná sladkost, NE tuk.
    """
    
    # Jídla, která dobře sytí
    DOBRE_SYTI: List[str] = [
        "kaše",
        "ovoce",
        "jogurt",
        "kombinace: kaše + ovoce + jogurt",
        "luštěniny (hlavně se semínky)"
    ]
    
    # Klíčové faktory sytosti
    FAKTORY_SYTOSTI: List[str] = [
        "vláknina",
        "objem",
        "jemná sladkost"
    ]
    
    # Co NESYTÍ (důležitá poznámka)
    NESYTI: List[str] = [
        "tuk"  # Důležité: tuk není faktor sytosti pro Páju
    ]
    
    # Poznámky
    POZNAMKY: List[str] = [
        "Velmi silná odpověď na vlákninu + objem + jemnou sladkost",
        "Tuk není faktor sytosti (na rozdíl od standardní keto diety)",
        "Luštěniny se semínky fungují velmi dobře"
    ]
    
    @staticmethod
    def je_jidlo_sytici(jidlo: str) -> bool:
        """
        Zkontroluje, zda jídlo patří mezi sytící.
        
        Args:
            jidlo: Název jídla
            
        Returns:
            True pokud je jídlo mezi doporučenými sytícími
        """
        jidlo_lower = jidlo.lower()
        for sytici in SyticiJidla.DOBRE_SYTI:
            if any(kw in jidlo_lower for kw in sytici.split()):
                return True
        return False
    
    @staticmethod
    def ziskej_prehled() -> Dict[str, List[str]]:
        """Vrátí přehled sytících jídel a faktorů."""
        return {
            "dobre_syti": SyticiJidla.DOBRE_SYTI,
            "faktory_sytosti": SyticiJidla.FAKTORY_SYTOSTI,
            "nesyti": SyticiJidla.NESYTI,
            "poznamky": SyticiJidla.POZNAMKY
        }


class ProblematickaJidla:
    """
    Jídla, která chutnají, ale nesedí (způsobují problémy).
    """
    
    # Jídla s problémy
    JIDLA_CO_NESEDI: Dict[str, Optional[str]] = {
        "káva": "spouštěč chutí i propadu energie",
        "pečené brambory": "pravděpodobně problém s tukem",
        "čokoláda": "spouští chutě na sladké",
        "kakao ve větším množství": "v malém množství (v buchtě) OK",
        "cibule": "spíš v malém množství",
        "knedlíky": "způsobují nadýmání"
    }
    
    # Specifická upozornění
    UPOZORNENI_KAVA: List[str] = [
        "Káva je SPOUŠTĚČ chutí, ne pomocník",
        "Způsobuje 'dojezd' (propad energie) po ~3 hodinách",
        "Kombinace káva + kaše = nadýmání"
    ]
    
    @staticmethod
    def je_jidlo_problematicke(jidlo: str) -> bool:
        """
        Zkontroluje, zda jídlo patří mezi problematická.
        
        Args:
            jidlo: Název jídla
            
        Returns:
            True pokud je jídlo mezi problematickými
        """
        jidlo_lower = jidlo.lower()
        for problematicke in ProblematickaJidla.JIDLA_CO_NESEDI.keys():
            if problematicke in jidlo_lower:
                return True
        return False
    
    @staticmethod
    def ziskej_duvod_problemu(jidlo: str) -> Optional[str]:
        """
        Vrátí důvod, proč je jídlo problematické.
        
        Args:
            jidlo: Název jídla
            
        Returns:
            Popis problému nebo None
        """
        jidlo_lower = jidlo.lower()
        for problematicke, duvod in ProblematickaJidla.JIDLA_CO_NESEDI.items():
            if problematicke in jidlo_lower:
                return duvod
        return None


class ReakceTela:
    """
    Tělesné reakce na různé typy jídel.
    
    Zahrnuje nadýmání, únavu a chutě na sladké.
    """
    
    # Spouštěče nadýmání
    NADYMANI_SPOUSTECE: List[str] = [
        "kaše + káva (hlavně při velkém množství)",
        "špatný odhad porce (obecně)",
        "knedlíky"
    ]
    
    # Spouštěče únavy
    UNAVA_SPOUSTECE: List[str] = [
        "dojezd po kávě (~3 hodiny)",
        "masná jídla",
        "přejedení",
        "hodně sladké jídlo"
    ]
    
    # Spouštěče chutí na sladké
    CHUTE_NA_SLADKE_SPOUSTECE: List[str] = [
        "po čokoládě",
        "po kávě",
        "když jídlo neuspokojí → řeší to sladkým/kafem z automatu"
    ]
    
    # Poznámky
    POZNAMKY: List[str] = [
        "Nadýmání: citlivost na objem jídla a kombinace kaše + káva",
        "Únava: hlavně po kávě (3h dojezd), masných jídlech, přejedení",
        "Chutě: káva a čokoláda jako spouštěče, neuspokojivá jídla vedou k automatu"
    ]
    
    @staticmethod
    def muze_zpusobit_nadymani(jidlo: str) -> bool:
        """
        Zkontroluje, zda jídlo může způsobit nadýmání.
        
        Args:
            jidlo: Název jídla
            
        Returns:
            True pokud jídlo může způsobit nadýmání
        """
        jidlo_lower = jidlo.lower()
        return any(
            kw in jidlo_lower 
            for spoustec in ReakceTela.NADYMANI_SPOUSTECE
            for kw in spoustec.lower().split()
            if kw not in ["hlavně", "při", "velkém", "množství", "(obecně)", "špatný", "odhad"]
        )
    
    @staticmethod
    def muze_zpusobit_unavu(jidlo: str) -> bool:
        """
        Zkontroluje, zda jídlo může způsobit únavu.
        
        Args:
            jidlo: Název jídla
            
        Returns:
            True pokud jídlo může způsobit únavu
        """
        jidlo_lower = jidlo.lower()
        klicova_slova = ["káva", "kafe", "maso", "masn", "sladké", "sladký", "čokoláda"]
        return any(kw in jidlo_lower for kw in klicova_slova)
    
    @staticmethod
    def muze_spustit_chute_na_sladke(jidlo: str) -> bool:
        """
        Zkontroluje, zda jídlo může spustit chutě na sladké.
        
        Args:
            jidlo: Název jídla
            
        Returns:
            True pokud jídlo může spustit chutě na sladké
        """
        jidlo_lower = jidlo.lower()
        spoustece = ["čokoláda", "čokolád", "káva", "kafe"]
        return any(sp in jidlo_lower for sp in spoustece)
    
    @staticmethod
    def ziskej_prehled() -> Dict[str, List[str]]:
        """Vrátí přehled tělesných reakcí."""
        return {
            "nadymani": ReakceTela.NADYMANI_SPOUSTECE,
            "unava": ReakceTela.UNAVA_SPOUSTECE,
            "chute_na_sladke": ReakceTela.CHUTE_NA_SLADKE_SPOUSTECE,
            "poznamky": ReakceTela.POZNAMKY
        }


def main():
    """Ukázka použití preferencí."""
    print("=" * 60)
    print("PREFERENCE JÍDEL - OSOBA 2 (PÁJA)")
    print("=" * 60)
    
    preference = PreferenceJidel.ziskej_preference_summary()
    
    print("\nNepreferované potraviny:")
    for item in preference["nepreferovane"]:
        print(f"  ✗ {item}")
    
    print("\n🚫 Slizké/kluzké textury (vyhýbat se):")
    for item in preference["slizke_textury"]:
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
    
    # Nové sekce - zaznamenané odpovědi (část 1)
    print("\n" + "=" * 60)
    print("🧠 HLAD A ENERGIE")
    print("=" * 60)
    hlad_info = HladAEnergie.ziskej_prehled()
    print(f"Nejvyšší hlad: {hlad_info['nejvyssi_hlad']}")
    print(f"Pocit bez energie při správném jídle: {'ano' if hlad_info['pocit_bez_energie'] else 'spíše ne'}")
    print(f"Přejedení bez hladu: {'ano' if hlad_info['prejedeni_bez_hladu'] else 'ne'}")
    print(f"Horší pocit: {hlad_info['horsi_pocit']}")
    print("\n📝 Poznámky:")
    for poznamka in hlad_info['poznamky']:
        print(f"  • {poznamka}")
    
    print("\n" + "=" * 60)
    print("🍽️ STRUKTURA JÍDEL")
    print("=" * 60)
    struktura = StrukturaJidel.ziskej_doporuceni_porci()
    print(f"Nejproblematičtější jídlo: {struktura['problematicke_jidlo']}")
    print(f"Důvod: {struktura['duvod']}")
    print(f"Preference: {struktura['preference']}")
    print("\nDoporučení:")
    for dop in struktura['doporuceni']:
        print(f"  • {dop}")
    
    print("\n" + "=" * 60)
    print("🥣 CO SYTÍ DOBŘE")
    print("=" * 60)
    sytici = SyticiJidla.ziskej_prehled()
    print("Jídla, která dobře sytí:")
    for jidlo in sytici['dobre_syti']:
        print(f"  ✓ {jidlo}")
    print("\nFaktory sytosti:")
    for faktor in sytici['faktory_sytosti']:
        print(f"  • {faktor}")
    print("\nCo NESYTÍ:")
    for item in sytici['nesyti']:
        print(f"  ✗ {item}")
    print("\n📝 Poznámky:")
    for poznamka in sytici['poznamky']:
        print(f"  • {poznamka}")
    
    print("\n" + "=" * 60)
    print("⚠️ JÍDLA, KTERÁ CHUTNAJÍ, ALE NESEDÍ")
    print("=" * 60)
    for jidlo, duvod in ProblematickaJidla.JIDLA_CO_NESEDI.items():
        print(f"  ⚠️ {jidlo}")
        if duvod:
            print(f"     → {duvod}")
    print("\n📝 Specificky o kávě:")
    for upozorneni in ProblematickaJidla.UPOZORNENI_KAVA:
        print(f"  • {upozorneni}")
    
    print("\n" + "=" * 60)
    print("🚨 REAKCE TĚLA")
    print("=" * 60)
    reakce = ReakceTela.ziskej_prehled()
    print("Nadýmání - spouštěče:")
    for spoustec in reakce['nadymani']:
        print(f"  • {spoustec}")
    print("\nÚnava - spouštěče:")
    for spoustec in reakce['unava']:
        print(f"  • {spoustec}")
    print("\nChutě na sladké - spouštěče:")
    for spoustec in reakce['chute_na_sladke']:
        print(f"  • {spoustec}")
    print("\n📝 Poznámky:")
    for poznamka in reakce['poznamky']:
        print(f"  • {poznamka}")


if __name__ == "__main__":
    main()
