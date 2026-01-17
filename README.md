# Foodler - Rodinný systém pro hubnutí a dietní plánování

Nástroj pro podporu hubnutí a zdravého stravování pro celou rodinu s důrazem na ketogenní/nízkosacharidovou dietu.

## 👥 Cílová skupina

### Roman (Romča)
- **Váha:** 134.2 kg (měření 1.9.2026)
- **Výška:** 183 cm
- **Věk:** 34 let
- **BMI:** 40.1
- **Procento tuku:** 46%
- **Svalová hmota:** 72.5 kg
- **Úroveň aktivity:** Sedavá (mostly sedentary)
- **Denní cíl:** 2001 kcal (20% deficit), 140g+ bílkovin, max 70g sacharidů

### Pája (Pavla)
- **Váha:** 77.3 kg (měření 22.12.2025)
- **Výška:** 169 cm
- **BMI:** 27.1
- **Procento tuku:** 39.6% (měření)
- **Svalová hmota (SMM):** 25.6 kg (měření)
- **VFA:** 147.2 cm²/level (měření)
- **Denní cíl:** 1508 kcal, 92g bílkovin, max 60g sacharidů (Ankerl Keto Calculator)

### Kubík
- **Datum narození:** 1.1.2021
- **Věk:** 4.5 let
- **Váha:** 18 kg (průměr pro věk)
- **Výška:** 106 cm
- **Zdraví:** Brýle 4 dioptrie, astigmatismus
- **Denní cíl:** 1400 kcal, 19g bílkovin, 130g sacharidů, důraz na vitamin A pro podporu zraku
- **Stravování:** Pracovní den: snídaně a večeře doma, svačiny a oběd ve školce; Víkend: všechna jídla doma

---

## 📚 Dokumentace

### 🚀 Začínáme
- **[NAVOD_K_POUZITI.md](NAVOD_K_POUZITI.md)** - Kompletní návod k použití systému
- **[QUICKSTART.md](QUICKSTART.md)** - Rychlý start
- **[RYCHLY_START.md](RYCHLY_START.md)** - Začněte tento víkend! (meal prep guide)

### 📋 Dietní plány
- **[PROTEIN_FIRST_PLAN.md](PROTEIN_FIRST_PLAN.md)** - Protein-first low-carb (12:12 IF) - pro Romana
- **[PAJA_PROTEIN_PLAN.md](PAJA_PROTEIN_PLAN.md)** - Protein-first low-carb (12:12 IF) - pro Páju (poměrový přepočet)
- **[KETO_12_12_PLAN.md](KETO_12_12_PLAN.md)** - Keto + časově omezené stravování
- **[NEJLEPSI_DIETY.md](NEJLEPSI_DIETY.md)** - Přehled 15 nejlepších diet na hubnutí
- **[MACINGOVA_DIETA.md](MACINGOVA_DIETA.md)** - Dieta Antonie Mačingové

### 🍽️ Plánování a příprava
- **[TYDENNI_PLANOVANI.md](TYDENNI_PLANOVANI.md)** - Strategie týdenního meal prepu
- **[VYBAVENI_A_TIPY.md](VYBAVENI_A_TIPY.md)** - Využití kuchyňského vybavení
- **[RECEPTY_SALATY.md](RECEPTY_SALATY.md)** - Recepty a saláty

### 🏥 Zdraví a metabolismus
- **[TRAVENI_A_METABOLISMUS.md](TRAVENI_A_METABOLISMUS.md)** - Trávení a metabolismus
- **[PURPOSE_ANALYSIS.md](PURPOSE_ANALYSIS.md)** - Analýza účelu a zdravotního kontextu

### 🛒 Nákupy a slevy
- **[KUPI_INTEGRATION.md](KUPI_INTEGRATION.md)** - Integrace s Kupi.cz pro sledování slev

### 🔧 Technická dokumentace
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Shrnutí implementace
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - Historie refaktoringu
- **[osoby/README.md](osoby/README.md)** - Práce s profily a preferencemi

---

## 📁 Struktura projektu

```
Foodler/
├── osoby/          # 👥 Personalizované profily (Roman, Pája)
├── potraviny/      # 🥩 Databáze potravin a ingrediencí
├── jidla/          # 🍽️  Hotová jídla a recepty
├── nakup/          # 🛒 Nákupní seznamy
├── lednice/        # 🧊 Správa domácích zásob
├── data/           # 📊 Datové soubory a meal plány
├── modely/         # 🔧 Datové modely (SOLID)
└── src/            # 💻 Zdrojový kód (scrapers, assistants)
```

Podrobnosti o jednotlivých složkách najdete v **[NAVOD_K_POUZITI.md](NAVOD_K_POUZITI.md)**.

---

## 🚀 Instalace

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

---

## 💡 Rychlé příkazy

```bash
# Zobrazit profily
python osoby/osoba_1/profil.py    # Roman
python osoby/osoba_2/profil.py    # Pája
python osoby/osoba_3/profil.py    # Kubík

# Zobrazit preference
python osoby/osoba_1/preference.py
python osoby/osoba_3/preference.py  # Kubík - potraviny pro podporu zraku

# Sdílená jídla a meal prep
python osoby/sdilena_jidla/jidla.py

# Databáze potravin
python potraviny/databaze.py

# Nákupní seznam
python nakup/seznamy.py

# Keto nákupní asistent
python src/assistants/keto_shopping_assistant.py
```

Více příkladů použití v **[NAVOD_K_POUZITI.md](NAVOD_K_POUZITI.md)**.

---

## 📖 English Documentation

See **[README_EN.md](README_EN.md)** for English version.

---

## 📄 Licence

MIT License - volně k použití pro osobní i komerční účely.
