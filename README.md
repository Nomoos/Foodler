# Foodler - Rodinný systém pro hubnutí a dietní plánování

Nástroj pro podporu hubnutí a zdravého stravování pro celou rodinu s důrazem na ketogenní/nízkosacharidovou dietu.

## 🎯 Účel projektu

Tento repozitář slouží jako **rodinný systém pro hubnutí a řízení stravy**. Primárním cílem je poskytnout strukturovanou podporu pro snižování váhy a zlepšení zdraví pro celou rodinu.

## 👥 Cílová skupina

### Osoba 1 (Muž)
- Váha: 135 kg, Výška: 183 cm
- BMI: 40.3, Procento tuku: 41%
- Denní cíl: 2000 kcal, 140g+ bílkovin, max 70g sacharidů

### Osoba 2 (Žena)
- Váha: 80 kg, Výška: 170 cm
- Denní cíl: 1600 kcal, 100g+ bílkovin, max 60g sacharidů

## 📁 Struktura projektu

```
Foodler/
├── potraviny/                    # 🥩 Čisté potraviny/ingredience
│   ├── databaze.py              # Databáze potravin s nutričními hodnotami
│   └── README.md                # Dokumentace
│
├── jidla/                        # 🍽️  Hotová jídla ke konzumaci
│   ├── databaze.py              # Databáze jídel s receptury
│   └── README.md                # Dokumentace
│
├── nakup/                        # 🛒 Nákupní seznamy
│   ├── seznamy.py               # Správa nákupních seznamů
│   └── README.md                # Dokumentace
│
├── lednice/                      # 🧊 Domácí zásoby
│   ├── zasoby.py                # Sledování zásob a expirace
│   └── README.md                # Dokumentace
│
├── osoby/                        # 👥 Personalizované profily
│   ├── osoba_1/                  # Profil muže
│   │   ├── profil.py            # Antropometrie a cíle
│   │   └── preference.py         # Preference a omezení
│   ├── osoba_2/                  # Profil ženy
│   │   ├── profil.py            # Antropometrie a cíle
│   │   └── preference.py         # Preference a omezení
│   └── sdilena_jidla/           # Sdílená jídla pro rodinu
│       └── jidla.py              # Recepty a meal prep
│
├── data/                         # 📊 Datové soubory
│   ├── keto_foods.py            # Keto kategorie potravin
│   └── meal_plans/              # Jídelní plány
│       ├── meal_plan_28_days.json
│       └── meal_plan_28_days.csv
│
├── modely/                       # 🔧 Datové modely (SOLID)
│   └── product.py               # Model produktu
│
├── src/                          # 💻 Zdrojový kód
│   ├── scrapers/                # Web scrapers
│   │   └── kupi_scraper.py      # Kupi.cz scraper
│   └── assistants/              # Asistenti
│       └── keto_shopping_assistant.py
│
└── dokumentace/                  # 📚 Česká dokumentace
    ├── MACINGOVA_DIETA.md       # Info o Mačingovce
    ├── RYCHLY_START.md          # Rychlý start
    └── ...
```

## 🚀 Rychlý start

### Instalace

```bash
# 1. Klonovat repozitář
git clone https://github.com/Nomoos/Foodler.git
cd Foodler

# 2. (Volitelné) Vytvořit virtuální prostředí
python -m venv venv
source venv/bin/activate  # Na Windows: venv\Scripts\activate

# 3. Nainstalovat závislosti
pip install -r requirements.txt
```

### Zobrazení osobního profilu

```bash
# Profil osoby 1
python osoby/osoba_1/profil.py

# Profil osoby 2
python osoby/osoba_2/profil.py

# Preference
python osoby/osoba_1/preference.py
```

### Sdílená jídla a meal prep

```bash
# Zobrazit sdílená jídla a týdenní plán
python osoby/sdilena_jidla/jidla.py
```

### Potraviny a ingredience

```bash
# Zobrazit databázi čistých potravin
python potraviny/databaze.py
```

### Hotová jídla a recepty

```bash
# Zobrazit databázi hotových jídel
python jidla/databaze.py
```

### Nákupní seznamy

```bash
# Vytvořit a zobrazit týdenní nákupní seznam
python nakup/seznamy.py
```

### Domácí zásoby (lednice)

```bash
# Zobrazit inventář zásob a upozornění na expiraci
python lednice/zasoby.py
```

### Příklad použití jídelníčku

```bash
# Zobrazit denní menu a statistiky
python example_usage.py
```

### Keto nákupní asistent

```bash
# Najít zlevněné keto produkty v českých supermarketech
python src/assistants/keto_shopping_assistant.py
```

## 💡 Klíčové funkce

### 🥩 Potraviny (čisté ingredience)
- Databáze 30+ běžných potravin s nutričními hodnotami
- Kategorizace (bílkoviny, zelenina, mléčné výrobky, tuky, ořechy)
- Výpočet makronutrientů pro libovolné množství
- Kontrola low-carb a high-protein potravin
- Informace o cenách a sezónnosti

### 🍽️ Jídla (hotová jídla)
- 7 kompletních receptů s detailními ingrediencemi
- Nutriční hodnoty pro celé jídlo i na porci
- Postup přípravy a časová náročnost
- Vhodnost pro meal prep (3-4 dny trvanlivost)
- Kategorizace podle typu (snídaně, oběd, večeře, svačina)

### 🛒 Nákupní seznamy
- Automatické vytvoření týdenního nákupního seznamu
- Odhad cen (1451 Kč/týden)
- Rozdělení podle obchodů (Lidl, Kaufland)
- Prioritizace položek (vysoká, normální, nízká)
- Sledování koupených položek

### 🧊 Domácí zásoby (lednice)
- Sledování zásob v lednici, mrazáku a spíži
- Automatické upozornění na expiraci
- Kontrola čerstvosti potravin
- Plánování vaření podle dostupných ingrediencí
- Kalkulace hodnoty zásob

### ✅ Personalizované profily
- Individuální cíle pro každou osobu
- Sledování antropometrických dat
- Výpočet BMI a ideální váhy
- Odhad kalorické potřeby

### 🥗 Preference a omezení
- **Bez hub**: Automatické filtrování jídel obsahujících houby
- Preferované bílkoviny, zelenina a tuky
- Dietní omezení (ketogenní/low-carb)
- Doporučené časy jídel

### 🍴 Sdílená jídla pro rodinu
- 10 rodinných receptů s makronutrienty
- Meal prep jídla (vydrží 3-4 dny)
- Rychlá jídla (≤15 minut)
- Týdenní plán přípravy
- Nákupní seznam

### 🏪 Smart nákupní asistent
- Integrace s Kupi.cz
- Hledání slev v českých supermarketech
- Filtrování keto-friendly produktů
- Odhad týdenního rozpočtu

## 📖 Dokumentace

### 🚀 Pro začátečníky:
- **[RYCHLY_START.md](RYCHLY_START.md)** - Začněte tento víkend!
  - Kompletní nákupní seznam
  - 2-hodinový meal prep
  - 3 základní recepty krok za krokem
  - Ideální pro začátečníky

### 📚 Podrobné průvodce meal prepu:
- **[TYDENNI_PLANOVANI.md](TYDENNI_PLANOVANI.md)** - Kompletní strategie týdenního plánování
  - Systém "2+5" (2 vaření za týden, 5 minut denně)
  - Meal prep krok za krokem
  - Top 5 receptů pro přípravu dopředu
  - Nákupní seznamy a časové harmonogramy
  - Strategie mražení a skladování
  - Úspora 50-65% času stráveného vařením

- **[VYBAVENI_A_TIPY.md](VYBAVENI_A_TIPY.md)** - Maximální využití kuchyňského vybavení
  - Jak využít tlakový hrnec pro rychlé vaření
  - Vakuovačka pro prodloužení trvanlivosti 2-3x
  - Mrazák jako váš spojenec (až 3 měsíce zásoby)
  - Trouba pro batch cooking (12 porcí za 1 hodinu)
  - Smoothie meal prep (2minutové snídaně)
  - Praktické kombinované strategie

### 📖 O dietě a receptech:
- **[NEJLEPSI_DIETY.md](NEJLEPSI_DIETY.md)** - ⭐ Přehled 15 nejlepších diet na hubnutí
  - Kompletní shrnutí populárních diet (keto, paleo, středomořská, atd.)
  - Výhody a nevýhody každé diety
  - Jak vybrat správnou dietu pro vás
  - Důležitá doporučení a časté chyby
  - Srovnání diet podle různých kritérií

### 📚 Podrobné průvodce:
- **[TYDENNI_PLANOVANI.md](TYDENNI_PLANOVANI.md)** - Strategie týdenního plánování
- **[VYBAVENI_A_TIPY.md](VYBAVENI_A_TIPY.md)** - Využití kuchyňského vybavení
- **[TRAVENI_A_METABOLISMUS.md](TRAVENI_A_METABOLISMUS.md)** - Jak zlepšit trávení
- **[MACINGOVA_DIETA.md](MACINGOVA_DIETA.md)** - Info o dietě Antonie Mačingové
- **[TRAVENI_A_METABOLISMUS.md](TRAVENI_A_METABOLISMUS.md)** - Jak zlepšit trávení a metabolismus
  - Co reálně pomáhá (bílkoviny, tuky, vláknina)
  - Kdy co jíst pro optimální metabolismus
  - Rychlá orientační tabulka
  - Doporučení pro reflux a trávicí problémy

- **[MACINGOVA_DIETA.md](MACINGOVA_DIETA.md)** - Podrobné informace o dietě Antonie Mačingové
  - Všechna jídla a jejich varianty
  - Principy Mačingovky
  - Nákupní seznamy
  - Tipy na přípravu

- **[KETO_12_12_PLAN.md](KETO_12_12_PLAN.md)** - Keto + časově omezené stravování (12:12)
  - Realistický plán pro ranní vstávání
  - Kombinace keto s 12hodinovým fastingem
  - Časování jídel pro optimální metabolismus
  - Praktické tipy pro GERD a reflux
  - Udržitelný režim bez extrémů

### Use in Python code

### 🔧 Technická dokumentace:
- **[osoby/README.md](osoby/README.md)** - Práce s profily a preferencemi
- **[KUPI_INTEGRATION.md](KUPI_INTEGRATION.md)** - Kupi.cz scraper

## 🏗️ SOLID principy

Projekt je strukturován podle SOLID principů:

- **Single Responsibility**: Každý modul má jediný účel
  - `modely/product.py` - pouze datový model
  - `src/scrapers/kupi_scraper.py` - pouze scrapování
  - `data/keto_foods.py` - pouze data
  - `src/assistants/keto_shopping_assistant.py` - pouze logika asistenta

- **Open/Closed**: Snadné rozšíření o nové osoby nebo jídla
- **Liskov Substitution**: Všechny profily mají stejné rozhraní
- **Interface Segregation**: Oddělení concerns (data vs. logika)
- **Dependency Inversion**: Závislost na abstrakcích

## 🧪 Testování

```bash
# Spustit testy
python test_kupi_scraper.py
python test_mock_data.py
```

## 🥑 Dietní přístup

### Ketogenní/Low-carb dieta
- **Nízké sacharidy**: Max 60-70g denně
- **Vysoké bílkoviny**: Min 100-140g denně
- **Střední až vysoké tuky**: Zdravé zdroje
- **Vláknina**: Min 20g denně

### Společné preference
- ❌ **Bez hub**: Houby, žampiony, hříbky
- ✅ **Preferované bílkoviny**: Kuře, krůta, hovězí, ryby, vejce
- ✅ **Preferovaná zelenina**: Brokolice, špenát, salát, cuketa
- ✅ **Zdravé tuky**: Olivový olej, avokádo, ořechy

## 🔬 Zdravotní kontext

Program je lékařsky sledován a zahrnuje řízení:
- Kardiovaskulárního zdraví (léky na krevní tlak)
- Trávicího zdraví (léčba refluxu)
- Celkové zlepšení metabolického zdraví

Viz [TRAVENI_A_METABOLISMUS.md](TRAVENI_A_METABOLISMUS.md) pro více informací.

## 📊 Příklad použití v kódu

### Práce s profilem

```python
from osoby.osoba_1.profil import OsobniProfil

profil = OsobniProfil()
print(f"BMI: {profil.vypocti_bmi()}")
print(f"Ideální váha: {profil.vypocti_idealniVahu()} kg")

# Získat denní rozložení makronutrientů
makra = profil.ziskej_denni_rozlozeni()
print(f"Denní kalorie: {makra['kalorie']}")
```

### Filtrace jídel podle preferencí

```python
from osoby.osoba_1.preference import PreferenceJidel

jidla = [
    "Kuřecí prsa s brokolicí",
    "Žampionová omáčka",
    "Losos s kedlubnou"
]

# Odfiltruje jídla s houbami
vhodna_jidla = PreferenceJidel.filtruj_jidla(jidla)
print(vhodna_jidla)
# Output: ['Kuřecí prsa s brokolicí', 'Losos s kedlubnou']
```

### Sdílená jídla

```python
from osoby.sdilena_jidla.jidla import SdilenaJidla, RodinnePlanovani

# Najít meal prep jídla
meal_prep_jidla = SdilenaJidla.najdi_meal_prep_jidla()

# Získat týdenní plán
plan = RodinnePlanovani.doporuc_tydenni_plan()

# Vygenerovat nákupní seznam
nakup = RodinnePlanovani.vypocti_nakupni_seznam_pro_tyden()
```

## 🛠️ Požadavky na síť

- Scraper vyžaduje připojení k internetu pro přístup ke kupi.cz
- Pokud běží v omezeném prostředí, selže s chybovou zprávou

## 🤝 Přispívání

Návrhy na vylepšení:
- Další nutriční databáze
- Více datových polí (vitamíny, minerály)
- Export formáty (CSV, Excel)
- Databázové úložiště pro sledované potraviny

## 📝 Licence

Tento projekt je určen pro osobní použití.

## 🔗 Související odkazy

- [Kaloricketabulky.cz](https://www.kaloricketabulky.cz/) - Nutriční data
- [Kupi.cz](https://www.kupi.cz/) - Slevy v supermarketech
- Mačingovka - Dieta Antonie Mačingové

---

**Aktivní vývoj** - Repozitář zahrnuje:
- ✅ Zdokumentovaný dietní plán a zdravotní cíle
- ✅ Personalizované profily a preference
- ✅ Sdílená jídla a meal prep plány
- ✅ Integrace Kupi.cz pro hledání slev
- ✅ Keto dietní nákupní asistent
- 🚧 Budoucnost: Sledování jídel, monitoring pokroku, databáze receptů
