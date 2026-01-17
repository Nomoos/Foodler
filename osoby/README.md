# Osoby - Personalizované profily

Tato složka obsahuje osobní profily a preference pro jednotlivé osoby v rodině.

## Struktura

```
osoby/
├── osoba_1/              # Profil muže (135kg, 183cm)
│   ├── profil.py         # Antropometrie a cíle
│   └── preference.py     # Preference jídel a omezení
├── osoba_2/              # Profil ženy (80kg, 170cm)
│   ├── profil.py         # Antropometrie a cíle
│   └── preference.py     # Preference jídel a omezení
└── sdilena_jidla/        # Sdílená jídla pro celou rodinu
    └── jidla.py          # Recepty a meal prep plány
```

## Použití

### Zobrazení profilu

```python
from osoby.osoba_1.profil import OsobniProfil

profil = OsobniProfil()
print(profil)
```

### Kontrola preferencí

```python
from osoby.osoba_1.preference import PreferenceJidel

# Zkontrolovat, zda je jídlo vhodné
vhodne = PreferenceJidel.je_jidlo_vhodne("Kuřecí s brokolicí")

# Filtrovat seznam jídel
jidla = ["Kuřecí prsa", "Žampionová omáčka", "Losos"]
filtrovana = PreferenceJidel.filtruj_jidla(jidla)
```

### Sdílená jídla

```python
from osoby.sdilena_jidla.jidla import SdilenaJidla, RodinnePlanovani

# Najít meal prep jídla
meal_prep = SdilenaJidla.najdi_meal_prep_jidla()

# Získat týdenní plán
plan = RodinnePlanovani.doporuc_tydenni_plan()

# Vygenerovat nákupní seznam
seznam = RodinnePlanovani.vypocti_nakupni_seznam_pro_tyden()
```

## Společné preference

- **Bez hub**: Obě osoby nepreferují houby a produkty z hub
- **Ketogenní dieta**: Nízký příjem sacharidů, vysoký příjem bílkovin a tuků
- **Meal prep**: Zaměření na jídla vhodná pro přípravu dopředu

## Přizpůsobení

Pro přidání nové osoby:

1. Vytvořte novou složku `osoba_X/`
2. Zkopírujte `profil.py` a `preference.py` z existující osoby
3. Upravte hodnoty podle potřeb nové osoby
