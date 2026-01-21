# Jídla

Tento modul spravuje **hotová jídla** složená z více potravin, připravená ke konzumaci.

## Obsah

- `databaze.py` - Databáze hotových jídel s receptury a nutričními hodnotami
- `soubory/` - Adresář s jednotlivými YAML soubory pro každé jídlo organizované do kategorií
- `JAK_PRIDAT_JIDLO.md` - Návod pro přidání nového jídla

## Struktura databáze

Od verze 2026-01 jsou jídla ukládána jako **jednotlivé YAML soubory** v adresáři `soubory/`. 
To umožňuje:
- ✅ Přidávat nová jídla bez konfliktů při spolupráci více lidí
- ✅ Snadno spravovat a verzovat jednotlivá jídla
- ✅ Přehledně organizovat recepty do kategorií

## Organizace receptů

Recepty jsou organizovány do následujících kategorií (podadresářů):

- **polevky/** - Polévky (např. Asijská polévka s bílou ředkví)
- **salaty/** - Saláty (např. Salát s tuňákem, Ředkvičkový salát)
- **hlavni_jidla/** - Hlavní jídla (např. Kuřecí prsa s brokolicí, Hovězí s cuketou)
- **prilohy/** - Přílohy (např. Bramborová kaše, Pečená ředkev)
- **snidane/** - Snídaně (např. Omelety, Vejce)
- **svaciny/** - Svačiny (např. Cottage cheese s ořechy, Tvaroh)

## Přidání nového jídla

Viz podrobný návod v souboru [JAK_PRIDAT_JIDLO.md](JAK_PRIDAT_JIDLO.md).

Stručně: vytvořte nový YAML soubor v adresáři `soubory/` s receptem a nutričními hodnotami.
- `variace_receptu.py` - Generátor variací receptů s různými ingrediencemi

## Použití

### Základní práce s recepty

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

### Generování variací receptů

```python
from jidla.databaze import DatabzeJidel
from jidla.variace_receptu import GeneratorVariaci

# Načti recept
keto_pizza = DatabzeJidel.najdi_podle_nazvu("Keto pizza")

# Vygeneruj varianty s různými sýry
syrove_varianty = GeneratorVariaci.vygeneruj_varianty_syr(
    keto_pizza,
    ingredience_k_nahrade="Sýrařův výběr moravský bochník 45% Madeta",
    alternativni_syry=["Mozzarella", "Parmazán", "Gouda"]
)

# Vygeneruj variantu s vejci
vejce_varianty = GeneratorVariaci.vygeneruj_varianty_s_vejci(
    keto_pizza,
    mnozstvi_vajec_g=50  # cca 1 vejce
)

# Nebo vygeneruj všechny varianty najednou
vsechny_varianty = GeneratorVariaci.vygeneruj_komplexni_varianty(
    keto_pizza,
    syrove_varianty=True,
    vejce_varianta=True
)
```

### Demo skripty

```bash
# Spusť hlavní databázi jídel
python jidla/databaze.py

# Spusť generátor variací
python jidla/variace_receptu.py

# Spusť interaktivní demo
python demo_variace_receptu.py
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

## Generátor variací receptů

Generátor variací umožňuje:
- **Varianty se sýry** - Nahradí jeden sýr různými typy sýrů (Mozzarella, Parmazán, Gouda, Cheddar, atd.)
- **Varianty s vejci** - Přidá vejce do receptu pro zvýšení obsahu bílkovin
- **Automatický výpočet makronutrientů** - Každá variace má přepočítané nutriční hodnoty
- **Výběr nejlepší varianty** - Možnost filtrovat podle makronutrientů

### Příklady použití

**Keto pizza s různými sýry:**
- Varianta s Mozzarellou: 144 kcal, 9.7g bílkovin
- Varianta s Parmazánem: 189 kcal, 16.9g bílkovin (nejvíce protein!)
- Varianta s Eidamem: 166 kcal, 0.3g sacharidů (nejméně carbs!)

**Keto pizza s vejci:**
- + 50g vajec: 250 kcal, 18.2g bílkovin, 0.9g sacharidů

## Rozdíl oproti modulu `osoby/sdilena_jidla`

- **`jidla/`** - Komplexní databáze všech jídel s detailními receptury a ingrediencemi
- **`osoby/sdilena_jidla/`** - Vybrané rodinné recepty optimalizované pro sdílené stravování
