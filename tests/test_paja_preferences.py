#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pro nové preference Páji (osoba_2) - zaznamenané odpovědi část 1.
"""

import sys
import os

# Přidání cesty k modulu
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from osoby.osoba_2.preference import (
    PreferenceJidel,
    DietniOmezeni,
    HladAEnergie,
    StrukturaJidel,
    SyticiJidla,
    ProblematickaJidla,
    ReakceTela
)


def test_hlad_a_energie():
    """Test vzorců hladu a energie."""
    print("Test: HladAEnergie")
    prehled = HladAEnergie.ziskej_prehled()
    
    assert prehled['nejvyssi_hlad'] == "ráno", "Nejvyšší hlad by měl být ráno"
    assert prehled['pocit_bez_energie'] == False, "Pocit bez energie by měl být False"
    assert prehled['prejedeni_bez_hladu'] == True, "Přejedení bez hladu by mělo být True"
    assert prehled['horsi_pocit'] == "plnost/těžkost", "Horší pocit by měl být plnost/těžkost"
    assert len(prehled['poznamky']) > 0, "Měly by existovat poznámky"
    
    print("  ✓ HladAEnergie funguje správně")


def test_struktura_jidel():
    """Test struktury jídel a doporučení porcí."""
    print("Test: StrukturaJidel")
    doporuceni = StrukturaJidel.ziskej_doporuceni_porci()
    
    assert doporuceni['problematicke_jidlo'] == "oběd", "Problematické jídlo by měl být oběd"
    assert "velké porce" in doporuceni['duvod'], "Důvod by měl zmínit velké porce"
    assert len(doporuceni['doporuceni']) > 0, "Měla by existovat doporučení"
    
    print("  ✓ StrukturaJidel funguje správně")


def test_sytici_jidla():
    """Test sytících jídel."""
    print("Test: SyticiJidla")
    
    # Test funkce je_jidlo_sytici
    assert SyticiJidla.je_jidlo_sytici("ovesná kaše"), "Kaše by měla být sytící"
    assert SyticiJidla.je_jidlo_sytici("jogurt s ovocem"), "Jogurt s ovocem by měl být sytící"
    assert SyticiJidla.je_jidlo_sytici("luštěniny"), "Luštěniny by měly být sytící"
    assert not SyticiJidla.je_jidlo_sytici("steak s máslem"), "Steak s máslem by neměl být sytící"
    
    # Test přehledu
    prehled = SyticiJidla.ziskej_prehled()
    assert "vláknina" in prehled['faktory_sytosti'], "Vláknina by měla být faktor sytosti"
    assert "tuk" in prehled['nesyti'], "Tuk by neměl být sytící"
    
    print("  ✓ SyticiJidla fungují správně")


def test_problematicka_jidla():
    """Test problematických jídel."""
    print("Test: ProblematickaJidla")
    
    # Test funkce je_jidlo_problematicke
    assert ProblematickaJidla.je_jidlo_problematicke("káva"), "Káva by měla být problematická"
    assert ProblematickaJidla.je_jidlo_problematicke("čokoláda"), "Čokoláda by měla být problematická"
    assert ProblematickaJidla.je_jidlo_problematicke("knedlíky"), "Knedlíky by měly být problematické"
    assert not ProblematickaJidla.je_jidlo_problematicke("kuřecí prsa"), "Kuřecí prsa by neměla být problematická"
    
    # Test získání důvodu problému
    duvod_kava = ProblematickaJidla.ziskej_duvod_problemu("káva")
    assert duvod_kava is not None, "Káva by měla mít důvod problému"
    assert "spouštěč" in duvod_kava, "Důvod kávy by měl zmínit spouštěč"
    
    duvod_coko = ProblematickaJidla.ziskej_duvod_problemu("čokoláda")
    assert duvod_coko is not None, "Čokoláda by měla mít důvod problému"
    
    print("  ✓ ProblematickaJidla fungují správně")


def test_reakce_tela():
    """Test tělesných reakcí."""
    print("Test: ReakceTela")
    
    # Test nadýmání
    assert ReakceTela.muze_zpusobit_nadymani("kaše"), "Kaše by mohla způsobit nadýmání"
    assert ReakceTela.muze_zpusobit_nadymani("knedlíky"), "Knedlíky by mohly způsobit nadýmání"
    
    # Test únavy
    assert ReakceTela.muze_zpusobit_unavu("káva"), "Káva by mohla způsobit únavu"
    assert ReakceTela.muze_zpusobit_unavu("masné jídlo"), "Masné jídlo by mohlo způsobit únavu"
    assert ReakceTela.muze_zpusobit_unavu("sladký dezert"), "Sladký dezert by mohl způsobit únavu"
    
    # Test chutí na sladké
    assert ReakceTela.muze_spustit_chute_na_sladke("čokoláda"), "Čokoláda by měla spustit chutě"
    assert ReakceTela.muze_spustit_chute_na_sladke("káva"), "Káva by měla spustit chutě"
    assert not ReakceTela.muze_spustit_chute_na_sladke("brokolice"), "Brokolice by neměla spustit chutě"
    
    # Test přehledu
    prehled = ReakceTela.ziskej_prehled()
    assert len(prehled['nadymani']) > 0, "Měly by existovat spouštěče nadýmání"
    assert len(prehled['unava']) > 0, "Měly by existovat spouštěče únavy"
    assert len(prehled['chute_na_sladke']) > 0, "Měly by existovat spouštěče chutí"
    
    print("  ✓ ReakceTela fungují správně")


def test_integrace_s_preferencemi():
    """Test integrace s existujícími preferencemi."""
    print("Test: Integrace s PreferenceJidel")
    
    # Stávající funkce by měly stále fungovat
    assert not PreferenceJidel.je_jidlo_vhodne("žampionová omáčka"), "Žampiony by neměly být vhodné"
    assert PreferenceJidel.je_jidlo_vhodne("kuřecí s brokolicí"), "Kuřecí s brokolicí by mělo být vhodné"
    
    # Test filtrace
    jidla = ["káva", "kaše", "kuřecí prsa", "houby"]
    filtrovana = PreferenceJidel.filtruj_jidla(jidla)
    assert "houby" not in filtrovana, "Houby by neměly projít filtrací"
    assert "kuřecí prsa" in filtrovana, "Kuřecí prsa by měla projít filtrací"
    
    print("  ✓ Integrace s PreferenceJidel funguje správně")


def main():
    """Spustí všechny testy."""
    print("=" * 60)
    print("TESTY NOVÝCH PREFERENCÍ PÁJI (ČÁST 1)")
    print("=" * 60)
    print()
    
    try:
        test_hlad_a_energie()
        test_struktura_jidel()
        test_sytici_jidla()
        test_problematicka_jidla()
        test_reakce_tela()
        test_integrace_s_preferencemi()
        
        print()
        print("=" * 60)
        print("✅ VŠECHNY TESTY PROŠLY")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"❌ TEST SELHAL: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ CHYBA: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
