#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for texture-based food preferences.
Tests that slimy/slippery foods are correctly filtered.
"""

from osoby.osoba_1.preference import PreferenceJidel as Osoba1Preference
from osoby.osoba_2.preference import PreferenceJidel as Osoba2Preference


def test_slimy_food_filtering():
    """Test that slimy textured foods are correctly identified and filtered."""
    
    # Test meals that should be REJECTED (contain slimy foods)
    rejected_meals = [
        "Žampionová omáčka s hovězím",
        "Smažené houby s rýží",
        "Lilek na grilu",
        "Okra s kuřecím",
        "Hovězí steak s řasami",
        "Kuřecí s chobotnicí",
        "Rosolová polévka",
        "Hříbková omáčka",
        "Hlívová polévka"
    ]
    
    # Test meals that should be ACCEPTED (no slimy foods)
    accepted_meals = [
        "Kuřecí prsa s brokolicí",
        "Losos s kedlubnou",
        "Hovězí steak s paprikou",
        "Salát s tuňákem",
        "Grilované kuře s cuketou"
    ]
    
    print("=" * 70)
    print("TEST FILTRACE SLIZKÉ/KLUZKÉ KONZISTENCE")
    print("=" * 70)
    
    # Test osoba_1
    print("\n🧪 Testing Osoba 1 (Roman):")
    print("-" * 70)
    
    all_passed = True
    
    print("\n❌ Should be REJECTED (contain slimy foods):")
    for meal in rejected_meals:
        is_suitable = Osoba1Preference.je_jidlo_vhodne(meal)
        status = "PASS" if not is_suitable else "FAIL"
        symbol = "✓" if not is_suitable else "✗"
        if is_suitable:
            all_passed = False
        print(f"  [{status}] {symbol} {meal}")
    
    print("\n✅ Should be ACCEPTED (no slimy foods):")
    for meal in accepted_meals:
        is_suitable = Osoba1Preference.je_jidlo_vhodne(meal)
        status = "PASS" if is_suitable else "FAIL"
        symbol = "✓" if is_suitable else "✗"
        if not is_suitable:
            all_passed = False
        print(f"  [{status}] {symbol} {meal}")
    
    # Test osoba_2
    print("\n" + "=" * 70)
    print("🧪 Testing Osoba 2 (Pája):")
    print("-" * 70)
    
    print("\n❌ Should be REJECTED (contain slimy foods):")
    for meal in rejected_meals:
        is_suitable = Osoba2Preference.je_jidlo_vhodne(meal)
        status = "PASS" if not is_suitable else "FAIL"
        symbol = "✓" if not is_suitable else "✗"
        if is_suitable:
            all_passed = False
        print(f"  [{status}] {symbol} {meal}")
    
    print("\n✅ Should be ACCEPTED (no slimy foods):")
    for meal in accepted_meals:
        is_suitable = Osoba2Preference.je_jidlo_vhodne(meal)
        status = "PASS" if is_suitable else "FAIL"
        symbol = "✓" if is_suitable else "✗"
        if not is_suitable:
            all_passed = False
        print(f"  [{status}] {symbol} {meal}")
    
    # Test with texture checking disabled
    print("\n" + "=" * 70)
    print("🧪 Testing with texture checking DISABLED:")
    print("-" * 70)
    
    print("\nNote: With texture checking disabled, only items in NEPREFERRED_FOODS")
    print("are filtered (i.e., mushroom types: houby, hříbky, žampiony, hlíva, shiitake).")
    print()
    
    for meal in rejected_meals[:3]:  # Test a few examples
        is_suitable = Osoba1Preference.je_jidlo_vhodne(meal, kontrolovat_texturu=False)
        print(f"  {meal}: {'ACCEPTED' if is_suitable else 'REJECTED'}")
    
    for meal in accepted_meals[:3]:
        is_suitable = Osoba1Preference.je_jidlo_vhodne(meal, kontrolovat_texturu=False)
        print(f"  {meal}: {'ACCEPTED' if is_suitable else 'REJECTED'}")
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED!")
    print("=" * 70)
    
    return all_passed


def test_preference_summary():
    """Test that preference summary includes texture information."""
    
    print("\n" + "=" * 70)
    print("TEST PREFERENCE SUMMARY")
    print("=" * 70)
    
    summary = Osoba1Preference.ziskej_preference_summary()
    
    print("\n✓ Available preference categories:")
    for key in summary.keys():
        print(f"  - {key}: {len(summary[key])} items")
    
    assert "slizke_textury" in summary, "Missing 'slizke_textury' in summary"
    assert len(summary["slizke_textury"]) > 0, "Empty 'slizke_textury' list"
    
    print("\n✓ Sample slimy textured foods to avoid:")
    for item in summary["slizke_textury"][:5]:
        print(f"  - {item}")
    
    print("\n✅ Preference summary test PASSED!")


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "TEXTURE PREFERENCE TEST SUITE" + " " * 24 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_passed = test_slimy_food_filtering()
    test_preference_summary()
    
    print("\n")
    if test_passed:
        print("🎉 All texture preference tests completed successfully!")
        exit(0)
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        exit(1)
