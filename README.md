# Foodler - Rodinný systém pro hubnutí a dietní plánování

Nástroj pro podporu hubnutí a zdravého stravování pro celou rodinu s důrazem na ketogenní/nízkosacharidovou dietu.

## 👥 Cílová skupina

### Roman (Romča)
- **Váha:** 134.2 kg (měření 9.1.2026)
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
- **[NAVOD_K_POUZITI.md](docs/getting-started/NAVOD_K_POUZITI.md)** - Kompletní návod k použití systému
- **[QUICKSTART.md](docs/getting-started/QUICKSTART.md)** - Rychlý start
- **[RYCHLY_START.md](docs/getting-started/RYCHLY_START.md)** - Začněte tento víkend! (meal prep guide)

### 📋 Dietní plány
- **[PROTEIN_FIRST_PLAN.md](docs/diet-plans/PROTEIN_FIRST_PLAN.md)** - Protein-first low-carb (12:12 IF) - pro Romana
- **[PAJA_PROTEIN_PLAN.md](docs/diet-plans/PAJA_PROTEIN_PLAN.md)** - Protein-first low-carb (12:12 IF) - pro Páju (poměrový přepočet)
- **[KETO_12_12_PLAN.md](docs/diet-plans/KETO_12_12_PLAN.md)** - Keto + časově omezené stravování
- **[NEJLEPSI_DIETY.md](docs/diet-plans/NEJLEPSI_DIETY.md)** - Přehled 15 nejlepších diet na hubnutí
- **[MACINGOVA_DIETA.md](docs/diet-plans/MACINGOVA_DIETA.md)** - Dieta Antonie Mačingové

### 🍽️ Plánování a příprava
- **[TYDENNI_PLANOVANI.md](docs/meal-planning/TYDENNI_PLANOVANI.md)** - Strategie týdenního meal prepu
- **[VYBAVENI_A_TIPY.md](docs/meal-planning/VYBAVENI_A_TIPY.md)** - Využití kuchyňského vybavení
- **[RECEPTY_SALATY.md](docs/meal-planning/RECEPTY_SALATY.md)** - Recepty a saláty
- **[RECEPTY_KETO.md](docs/meal-planning/RECEPTY_KETO.md)** - Keto recepty (chléb, pečivo)

### 📋 Personalizované dotazníky
- **[osoby/osoba_1/README_DOTAZNIK.md](osoby/osoba_1/README_DOTAZNIK.md)** - ⭐ NOVÉ! Dotazník pro Romana - Meal prep a nákupy
  - 67 otázek zaměřených na týdenní přípravu jídel
  - Optimalizace nákupů a využití slev
  - Personalizovaná doporučení pro batch cooking
  - Ukázka: `python demo_dotaznik_roman.py`
- **[osoby/osoba_2/README_DOTAZNIK.md](osoby/osoba_2/README_DOTAZNIK.md)** - Dotazník pro Páju - Jídelní preference
  - 62 otázek pro lepší přizpůsobení jídelníčku
  - Zaměření na emoční stravování a časové preference

### 🏥 Zdraví a metabolismus
- **[TRAVENI_A_METABOLISMUS.md](docs/health/TRAVENI_A_METABOLISMUS.md)** - Trávení a metabolismus
- **[PURPOSE_ANALYSIS.md](docs/health/PURPOSE_ANALYSIS.md)** - Analýza účelu a zdravotního kontextu
- **[TRAVENI_A_METABOLISMUS.md](TRAVENI_A_METABOLISMUS.md)** - Trávení a metabolismus
- **[LOW_CARB_IMPACT.md](LOW_CARB_IMPACT.md)** - Vliv nízkosacharidového/keto stravování na trávení, GERD a psychiku
- **[PURPOSE_ANALYSIS.md](PURPOSE_ANALYSIS.md)** - Analýza účelu a zdravotního kontextu

### 🛒 Nákupy a slevy
- **[KUPI_INTEGRATION.md](docs/technical/KUPI_INTEGRATION.md)** - Integrace s Kupi.cz pro sledování slev
- **[DISCOUNT_SCRAPING_GUIDE.md](docs/technical/DISCOUNT_SCRAPING_GUIDE.md)** - 🆕 Kompletní stahování a ukládání slev ze všech obchodů

**Nové funkce v2.0.0:**
```bash
# Stáhnout a uložit slevy ze všech obchodů (Lidl, Kaufland, Albert, ...)
python scrape_and_save_discounts.py
```
- ✅ Automatická extrakce dat platnosti (od-do)
- ✅ JSON storage s metadaty
- ✅ Srovnání cen napříč obchody
- ✅ Historie cen pro trend analýzu

### 📊 Plánovač jídelníčků
- **[MEAL_PLANNER_GUIDE.md](docs/technical/MEAL_PLANNER_GUIDE.md)** - Interaktivní plánovač s fitness funkcemi
  - Dotazník pro personalizaci
  - Stavitel denního plánu s optimalizací
  - Stavitel týdenního plánu
  - Scoring a threshold systém

### 🔧 Technická dokumentace
- **[GITHUB_COPILOT_WEB_ACCESS.md](docs/technical/GITHUB_COPILOT_WEB_ACCESS.md)** - ⭐ Návod pro GitHub Copilot Pro+ a testování scraperů
- **[LANGUAGE_DECISION.md](LANGUAGE_DECISION.md)** - ⭐ Rozhodnutí o programovacím jazyce (Python vs C# vs TypeScript)
- **[LANGUAGE_EVALUATION.md](docs/technical/LANGUAGE_EVALUATION.md)** - Podrobná analýza jazyků
- **[IMPLEMENTATION_SUMMARY.md](docs/technical/IMPLEMENTATION_SUMMARY.md)** - Shrnutí implementace
- **[REFACTORING_SUMMARY.md](docs/technical/REFACTORING_SUMMARY.md)** - Historie refaktoringu
- **[osoby/README.md](osoby/README.md)** - Práce s profily a preferencemi

---

## 📁 Struktura projektu

```
Foodler/
├── docs/           # 📚 Dokumentace (strukturovaná do kategorií)
│   ├── getting-started/  # Rychlé návody a úvody
│   ├── diet-plans/       # Dietní plány
│   ├── meal-planning/    # Meal prep a plánování
│   ├── health/           # Zdraví a metabolismus
│   └── technical/        # Technická dokumentace
├── osoby/          # 👥 Personalizované profily (Roman, Pája)
├── potraviny/      # 🥩 Databáze potravin a ingrediencí
├── jidla/          # 🍽️  Hotová jídla a recepty
├── nakup/          # 🛒 Nákupní seznamy
├── lednice/        # 🧊 Správa domácích zásob
├── data/           # 📊 Datové soubory a meal plány
├── modely/         # 🔧 Datové modely (SOLID)
└── src/            # 💻 Zdrojový kód
    ├── assistants/       # Nákupní asistenti
    ├── scrapers/         # Web scrapers
    └── planners/         # 🎯 Plánovač jídelníčků (NOVÉ!)
```

Podrobnosti o jednotlivých složkách najdete v **[NAVOD_K_POUZITI.md](docs/getting-started/NAVOD_K_POUZITI.md)**.

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

# Dotazníky pro personalizaci
python osoby/osoba_1/dotaznik_roman.py    # ⭐ Roman - Meal prep a nákupy
python demo_dotaznik_roman.py             # Demo - ukázka pro Romana
python osoby/osoba_2/dotaznik_paja.py     # Pája - Jídelní preference
python demo_dotaznik_paja.py              # Demo - ukázka pro Páju

# Sdílená jídla a meal prep
python osoby/sdilena_jidla/jidla.py

# Databáze potravin
python potraviny/databaze.py

# Databáze jídel
python jidla/databaze.py

# Generátor variací receptů (nové!)
python jidla/variace_receptu.py

# Demo variací receptů (interaktivní)
python demo_variace_receptu.py

# Nákupní seznam
python nakup/seznamy.py

# Keto nákupní asistent
python src/assistants/keto_shopping_assistant.py

# Interaktivní plánovač jídelníčků
python src/planners/questionnaire.py

# Demo denního plánovače
python src/planners/day_plan_builder.py

# Demo týdenního plánovače
python src/planners/week_plan_builder.py

# Generátor jídelníčku na konkrétní datum (z 28denního cyklu)
python generate_meal_plan_date.py tomorrow      # Zítra
python generate_meal_plan_date.py today         # Dnes
python generate_meal_plan_date.py 18.1.2026     # Konkrétní datum

# Jídelníček na zítra (18.1.2026)
python generate_meal_plan_tomorrow.py
```

Více příkladů použití v **[NAVOD_K_POUZITI.md](docs/getting-started/NAVOD_K_POUZITI.md)**.

---

## 📖 English Documentation

See **[README_EN.md](README_EN.md)** for English version.

---

## 📄 Licence

MIT License - volně k použití pro osobní i komerční účely.
