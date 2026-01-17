# Návod k použití - Foodler

## 🚀 Rychlý start (5 minut)

### 1. Instalace

```bash
# Klonovat repozitář
git clone https://github.com/Nomoos/Foodler.git
cd Foodler

# Nainstalovat závislosti
pip install -r requirements.txt
```

### 2. Zobrazení osobního profilu

```bash
# Profil osoby 1 (muž)
python osoby/osoba_1/profil.py

# Profil osoby 2 (žena)
python osoby/osoba_2/profil.py
```

**Výstup:**
```
Profil: Osoba 1
==================================================
Antropometrie:
  Váha: 135.0 kg
  Výška: 183 cm
  BMI: 40.3
  Ideální váha (BMI 25): 83.7 kg
  
Denní cíle:
  Kalorie: 2000 kcal (6 jídel)
  Bílkoviny: min 140g
  Sacharidy: max 70g
```

### 3. Zobrazení preferencí a omezení

```bash
python osoby/osoba_1/preference.py
```

**Automaticky vyloučí:**
- ❌ Houby, žampiony, hříbky

**Preferuje:**
- ✅ Kuřecí, krůtí, hovězí, ryby, vejce
- ✅ Brokolice, špenát, salát, cuketa
- ✅ Olivový olej, avokádo, ořechy

### 4. Sdílená jídla pro celou rodinu

```bash
python osoby/sdilena_jidla/jidla.py
```

**Ukáže:**
- 10 rodinných receptů
- Meal prep jídla (vydrží 3-4 dny)
- Rychlá jídla (≤15 minut)
- Týdenní plán přípravy
- Nákupní seznam

### 5. Týdenní jídelníček (28 dní)

```bash
python example_usage.py
```

## 💡 Použití v kódu

### Práce s profilem

```python
from osoby.osoba_1.profil import OsobniProfil

# Vytvořit profil
profil = OsobniProfil()

# Vypočítat BMI
bmi = profil.vypocti_bmi()
print(f"Vaše BMI: {bmi}")

# Ideální váha
idealni = profil.vypocti_idealniVahu()
print(f"Ideální váha: {idealni} kg")

# Denní makronutrienty
makra = profil.ziskej_denni_rozlozeni()
print(f"Denní kalorie: {makra['kalorie']}")
print(f"Bílkoviny: {makra['bilkoviny_g']}g")
```

### Filtrování jídel podle preferencí

```python
from osoby.osoba_1.preference import PreferenceJidel

# Seznam jídel
jidla = [
    "Kuřecí prsa s brokolicí",
    "Žampionová omáčka s hovězím",
    "Losos s kedlubnou",
    "Smažené houby"
]

# Filtrovat (automaticky odstraní houby)
vhodna = PreferenceJidel.filtruj_jidla(jidla)

print("Vhodná jídla:")
for jidlo in vhodna:
    print(f"  ✓ {jidlo}")

# Výstup:
#   ✓ Kuřecí prsa s brokolicí
#   ✓ Losos s kedlubnou
```

### Kontrola makronutrientů

```python
from osoby.osoba_1.preference import DietniOmezeni

# Kontrola, zda jídlo splňuje limity
sacharidy = 10  # g
bilkoviny = 25   # g

if DietniOmezeni.je_jidlo_v_ramci_limitu(sacharidy, bilkoviny):
    print("✓ Jídlo je v rámci limitů!")
else:
    print("✗ Jídlo nesplňuje limity")
```

### Sdílená jídla - meal prep

```python
from osoby.sdilena_jidla.jidla import SdilenaJidla, RodinnePlanovani

# Najít jídla vhodná pro meal prep
meal_prep = SdilenaJidla.najdi_meal_prep_jidla()

print("Meal prep jídla:")
for jidlo in meal_prep:
    print(f"  • {jidlo.nazev} - {jidlo.priprava_cas_min} min")
    print(f"    {jidlo.poznamky}")

# Týdenní plán
plan = RodinnePlanovani.doporuc_tydenni_plan()

print("\nNEDĚLE - Meal prep:")
for jidlo in plan['nedele_meal_prep']:
    print(f"  □ {jidlo}")

# Nákupní seznam
nakup = RodinnePlanovani.vypocti_nakupni_seznam_pro_tyden()

print("\nNÁKUPNÍ SEZNAM - Bílkoviny:")
for polozka in nakup['bilkoviny']:
    print(f"  □ {polozka}")
```

### Rychlá jídla

```python
from osoby.sdilena_jidla.jidla import SdilenaJidla

# Najít jídla do 15 minut
rychla = SdilenaJidla.najdi_rychla_jidla(max_minut=15)

print("Rychlá jídla (≤15 min):")
for jidlo in rychla:
    print(f"  ⚡ {jidlo.nazev} - {jidlo.priprava_cas_min} min")
```

## 📁 Struktura souborů

```
osoby/
├── osoba_1/           # Profil muže
│   ├── profil.py      # Antropometrie, BMI, cíle
│   └── preference.py  # Preference a omezení
├── osoba_2/           # Profil ženy
│   ├── profil.py      # Antropometrie, BMI, cíle
│   └── preference.py  # Preference a omezení
└── sdilena_jidla/     # Sdílená jídla
    └── jidla.py       # Recepty, meal prep, plány
```

## 🥗 Příklady receptů

### 1. Kuřecí prsa na grilu s brokolicí (25 min)
- Makra na 100g: B:25g, S:4g, T:6g
- Meal prep: ✓ (vydrží 3-4 dny)
- Příprava: Kuřecí prsa naložit, grilovat 6-8 min z každé strany

### 2. Salát s tuňákem a vejcem (15 min)
- Makra na 100g: B:18g, S:3g, T:8g
- Meal prep: ✓ (den dopředu)
- Příprava: Vejce uvařit, tuňák smíchat se zeleninou

### 3. Tvaroh s lněným semínkem (2 min)
- Makra na 100g: B:16g, S:3.5g, T:4.5g
- Rychlá svačina
- Příprava: Tvaroh + lněné semínko + skořice

## 🛒 Nákupní asistent

```bash
# Najít slevy v českých supermarketech
python src/assistants/keto_shopping_assistant.py
```

**Zobrazí:**
- Aktuální slevy na keto produkty
- Porovnání cen v Lidl, Kaufland, Albert atd.
- Týdenní rozpočet
- Doporučený nákupní seznam

## ❓ FAQ

### Jak přidat novou osobu?
1. Vytvořte složku `osoby/osoba_3/`
2. Zkopírujte `profil.py` a `preference.py` z osoba_1
3. Upravte hodnoty podle potřeb

### Jak přidat nové jídlo?
Otevřete `osoby/sdilena_jidla/jidla.py` a přidejte do seznamu `JIDLA`:

```python
SdileneJidlo(
    nazev="Vaše jídlo",
    kategorie="obed",
    ingredience=["..."],
    bilkoviny_na_100g=20.0,
    sacharidy_na_100g=5.0,
    tuky_na_100g=10.0,
    vlaknina_na_100g=2.0,
    kalorie_na_100g=200.0,
    priprava_cas_min=20,
    priprava_popis="...",
    vhodne_pro_meal_prep=True,
    poznamky="..."
)
```

### Jak změnit preference?
Upravte soubor `osoby/osoba_X/preference.py`:

```python
NEPREFERRED_FOODS: List[str] = [
    "houby",
    "hříbky",
    # přidejte další...
]
```

## 📚 Další dokumentace

- [README.md](README.md) - Hlavní dokumentace
- [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) - Technické detaily
- [osoby/README.md](osoby/README.md) - Práce s profily
- [RYCHLY_START.md](RYCHLY_START.md) - Meal prep guide
- [TYDENNI_PLANOVANI.md](TYDENNI_PLANOVANI.md) - Týdenní plánování

## 🆘 Podpora

Při problémech:
1. Zkontrolujte instalaci závislostí: `pip install -r requirements.txt`
2. Spusťte testy: `python test_kupi_scraper.py`
3. Prohlédněte dokumentaci v repozitáři

---

**Užijte si zdravé hubnutí! 🥑💪**
