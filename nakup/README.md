# Nákup

Tento modul spravuje **nákupní seznamy** a plánování nákupů.

## Obsah

- `seznamy.py` - Správa nákupních seznamů a položek

## Použití

```python
from nakup.seznamy import SpravacoNakupu, NakupniSeznam, NakupniPolozka
from datetime import date

# Vytvoření správce nákupů
spravce = SpravacoNakupu()

# Vytvoření týdenního nákupního seznamu
tyden_od = date.today()
seznam = spravce.vytvorit_tydenni_seznam(tyden_od)

print(f"Celková cena: {seznam.celkova_cena:.2f} Kč")
print(f"Počet položek: {len(seznam.polozky)}")

# Zobrazení podle kategorií
kategorie = seznam.ziskej_podle_kategorie()
for kat, polozky in kategorie.items():
    print(f"\n{kat}:")
    for p in polozky:
        print(f"  • {p.nazev} - {p.mnozstvi} {p.jednotka}")

# Zobrazení podle obchodů
obchody = seznam.ziskej_podle_obchodu()
for obchod, polozky in obchody.items():
    print(f"\n{obchod}:")
    for p in polozky:
        print(f"  • {p.nazev}")

# Označení položky jako koupené
seznam.oznacit_koupenou("Kuřecí prsa")

# Kontrola, zda je seznam kompletní
if seznam.je_kompletni():
    print("✅ Vše nakoupeno!")
```

## Funkce

### Vytvoření seznamu
- Automatické vytvoření týdenního nákupního seznamu pro keto dietu
- Odhad cen podle aktuálních tržních cen
- Rozdělení podle obchodů (Lidl, Kaufland)

### Správa položek
- Přidávání/odebírání položek
- Označování jako koupené
- Prioritizace (vysoká, normální, nízká)
- Kategorizace (bílkoviny, zelenina, mléčné výrobky, atd.)

### Zobrazení
- Podle kategorií potravin
- Podle obchodů
- Nekoupené položky
- Celková cena

## Kategorie položek

- **bilkoviny** - Maso, ryby, vejce
- **mlecne_vyrobky** - Tvaroh, jogurt, sýr
- **zelenina** - Brokolice, špenát, cuketa, atd.
- **tuky** - Oleje, máslo
- **orechy** - Mandle, vlašské ořechy, semínka
- **koreni** - Koření, bylinky
