# Foodler - Rodinný systém pro hubnutí a dietní plánování

Nástroj pro podporu hubnutí a zdravého stravování pro celou rodinu s důrazem na ketogenní/nízkosacharidovou dietu.

## 👥 Cílová skupina

### Roman (Romča)
- **Váha:** 135.5 kg (měření)
- **Výška:** 183 cm
- **BMI:** 40.5
- **Procento tuku:** 37.5% (měření)
- **Svalová hmota (SMM):** 45.3 kg (měření)
- **Denní cíl:** 2000 kcal, 140g+ bílkovin, max 70g sacharidů

### Pája (Pavla)
- **Váha:** 77.3 kg (měření 22.12.2025)
- **Výška:** 170 cm
- **BMI:** 26.7
- **Procento tuku:** 39.6% (měření)
- **Svalová hmota (SMM):** 25.6 kg (měření)
- **VFA:** 147.2 cm²/level (měření)
- **Denní cíl:** 1600 kcal, 100g+ bílkovin, max 60g sacharidů

---

## 📚 Dokumentace

### 🚀 Začínáme
- **[NAVOD_K_POUZITI.md](NAVOD_K_POUZITI.md)** - Kompletní návod k použití systému
- **[QUICKSTART.md](QUICKSTART.md)** - Rychlý start
- **[RYCHLY_START.md](RYCHLY_START.md)** - Začněte tento víkend! (meal prep guide)

### 📋 Dietní plány
- **[PROTEIN_FIRST_PLAN.md](PROTEIN_FIRST_PLAN.md)** - Protein-first low-carb (12:12 IF)
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

# Zobrazit preference
python osoby/osoba_1/preference.py

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
