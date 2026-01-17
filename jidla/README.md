# Jídla

Tento modul spravuje **hotová jídla** složená z více potravin, připravená ke konzumaci.

## Obsah

- `databaze.py` - Databáze hotových jídel s receptury a nutričními hodnotami

## Použití

```python
from jidla.databaze import DatabzeJidel, Jidlo

# Najít jídlo podle názvu
kureci = DatabzeJidel.najdi_podle_nazvu("Kuřecí prsa s brokolicí a olivovým olejem")

# Vypočítat makra na porci
makra = kureci.vypocitej_makra_na_porci()
print(f"Kalorie na porci: {makra['kalorie']} kcal")
print(f"Bílkoviny: {makra['bilkoviny']}g")

# Najít jídla podle typu
obedy = DatabzeJidel.najdi_podle_typu("obed")

# Najít meal prep jídla
meal_prep = DatabzeJidel.najdi_meal_prep()

# Najít rychlá jídla
rychla = DatabzeJidel.najdi_rychla(max_minut=15)

# Najít nízkosacharidová jídla
low_carb = DatabzeJidel.najdi_low_carb(max_sacharidy=15.0)
```

## Typy jídel

- **snidane** - Snídaně
- **obed** - Oběd
- **vecere** - Večeře
- **svacina** - Svačina

## Struktura Jidlo

Každé jídlo obsahuje:
- Název a typ
- Seznam ingrediencí s množstvím
- Celkové nutriční hodnoty
- Postup přípravy a čas
- Obtížnost (snadná, střední, náročná)
- Vhodnost pro meal prep
- Trvanlivost (vydrží X dní)

## Rozdíl oproti modulu `osoby/sdilena_jidla`

- **`jidla/`** - Komplexní databáze všech jídel s detailními receptury a ingrediencemi
- **`osoby/sdilena_jidla/`** - Vybrané rodinné recepty optimalizované pro sdílené stravování
