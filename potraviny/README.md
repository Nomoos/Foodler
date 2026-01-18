# Potraviny

Tento modul spravuje **čisté potraviny** (ingredience), které lze použít k přípravě jídel.

## Obsah

- `databaze.py` - Databáze běžných potravin s nutričními hodnotami
- `soubory/` - Adresář s jednotlivými YAML soubory pro každou potravinu
- `JAK_PRIDAT_POTRAVINU.md` - Návod pro přidání nové potraviny

## Struktura databáze

Od verze 2026-01 jsou potraviny ukládány jako **jednotlivé YAML soubory** v adresáři `soubory/`.
To umožňuje:
- ✅ Přidávat nové potraviny bez konfliktů při spolupráci více lidí
- ✅ Snadno spravovat a verzovat jednotlivé potraviny
- ✅ Přehledně organizovat databázi ingrediencí

## Přidání nové potraviny

Viz podrobný návod v souboru [JAK_PRIDAT_POTRAVINU.md](JAK_PRIDAT_POTRAVINU.md).

Stručně: vytvořte nový YAML soubor v adresáři `soubory/` s nutričními hodnotami.

## Použití

```python
from potraviny.databaze import DatabazePotravIn, Potravina

# Najít potravinu podle názvu
kureci = DatabazePotravIn.najdi_podle_nazvu("Kuřecí prsa")

# Vypočítat makra pro 200g
makra = kureci.vypocitej_makra(200)
print(f"Kalorie: {makra['kalorie']} kcal")
print(f"Bílkoviny: {makra['bilkoviny']}g")

# Najít potraviny podle kategorie
zelenina = DatabazePotravIn.najdi_podle_kategorie("zelenina")

# Najít nízkosacharidové potraviny
low_carb = DatabazePotravIn.najdi_low_carb(max_sacharidy=10.0)

# Najít vysokobílkovinové potraviny
high_protein = DatabazePotravIn.najdi_high_protein(min_bilkoviny=15.0)
```

## Kategorie potravin

- **bilkoviny** - Maso, ryby, vejce
- **mlecne_vyrobky** - Tvaroh, jogurt, sýr
- **zelenina** - Brokolice, špenát, cuketa, atd.
- **tuky** - Oleje, avokádo
- **orechy** - Mandle, vlašské ořechy, semínka

## Struktura Potravina

Každá potravina obsahuje:
- Název a kategorie
- Nutriční hodnoty na 100g (kalorie, bílkoviny, sacharidy, tuky, vláknina)
- Cena za kg (volitelné)
- Sezónní dostupnost (volitelné)
- Poznámky (volitelné)
