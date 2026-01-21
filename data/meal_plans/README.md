# 📅 Meal Plans - Jídelníčky

Tento adresář obsahuje všechny jídelní plány pro rodinu.

## 📁 Struktura Adresářů

### `daily/` - Denní Plány
Denní jídelní plány a nákupní seznamy pro konkrétní dny.

**Formát názvů:** `meal_plan_YYYY-MM-DD.md`, `shopping_list_YYYY-MM-DD.md`

**Příklad:**
- `meal_plan_2026-01-21.md` - Jídelní plán pro 21. ledna 2026
- `shopping_list_2026-01-21.md` - Nákupní seznam pro 21. ledna 2026

### `weekly/` - Týdenní Plány
Týdenní jídelní plány s kompletními jídelníčky pro 7 dní.

**Struktura:**
```
weekly/
├── week_YYYY-MM-DD/           # Složka týdenního plánu
│   ├── README.md              # Přehled týdne
│   ├── day_1_YYYY-MM-DD_pondělí.md
│   ├── day_2_YYYY-MM-DD_úterý.md
│   ├── ...
│   ├── day_7_YYYY-MM-DD_neděle.md
│   ├── shopping_list.md       # Nákupní seznam na celý týden
│   ├── daily_consumption/     # Skutečná spotřeba (tracking)
│   └── archived_duplicates/   # Starší verze a duplikáty
└── weekly_plan_YYYY-MM-DD_to_YYYY-MM-DD.json
```

### `monthly/` - Měsíční Plány
Dlouhodobé plány (28denní, 30denní) v různých formátech.

**Formáty:**
- `.json` - Strukturovaná data pro programy
- `.csv` - Tabulková data pro Excel/Sheets
- `.md` - Human-readable formát

**Příklad:**
- `meal_plan_28_days.json` - 28denní plán (aktuální)
- `meal_plan_28_days_keto.json` - Keto verze 28denního plánu
- `meal_plan_28_days.csv` - CSV export

### `archives/` - Archiv
Starší verze plánů, zálohy a dokumentace změn.

**Obsah:**
- `meal_plan_28_days_original_backup.json` - Originální záloha
- `CHANGELOG_KETO_PLAN.md` - Historie změn keto plánu
- `NUTRITIONAL_OPTIMIZATION.md` - Dokumentace optimalizací
- `SUMMARY_MEAL_PLAN_UPDATE.md` - Souhrny aktualizací

## 🎯 Použití

### Vytvoření Nového Denního Plánu
```bash
# Použijte generátor
python scripts/generate_meal_plan_date.py 2026-01-22
```

### Vytvoření Týdenního Plánu
```bash
# Vygenerujte týdenní plán
python scripts/generate_weekly_meal_plan.py
```

### Export do CSV
```bash
# Exportujte plán do CSV
python scripts/export_meal_plan_csv.py monthly/meal_plan_28_days.json
```

## 📝 Konvence Pojmenování

### Soubory
- **Datum:** Vždy `YYYY-MM-DD` (např. `2026-01-21`)
- **Dny v týdnu:** česky (pondělí, úterý, ...)
- **Typy:** `meal_plan_`, `shopping_list_`, `weekly_plan_`

### Příklady
✅ **Správně:**
- `meal_plan_2026-01-21.md`
- `weekly_plan_2026-01-19_to_2026-01-25.json`
- `day_1_2026-01-19_pondělí.md`

❌ **Špatně:**
- `plan_21-1-2026.md` (nesprávný formát data)
- `meal_plan_monday.md` (chybí datum)
- `PAJA_JIDELNICEK_DEN_2.md` (nekonzistentní)

## 🔄 Údržba

### Co dělat po vytvoření nového plánu:
1. ✅ Uložit do správného adresáře (`daily/`, `weekly/`, `monthly/`)
2. ✅ Použít správné pojmenování
3. ✅ Aktualizovat README pokud přidáváte novou strukturu
4. ✅ Starší verze přesunout do `archives/`

### Pravidelné čištění:
- **Měsíčně:** Přesunout staré denní plány do `archives/`
- **Kvartálně:** Archivovat staré týdenní plány
- **Ročně:** Vyčistit `archives/` (odstranit plány starší 1 roku)

## 📊 Statistiky

Ke dni 21.01.2026:
- **Denní plány:** 2 soubory
- **Týdenní plány:** 1 týden (7 dní)
- **Měsíční plány:** 3 soubory (JSON, CSV, Keto)
- **Archivy:** 4 soubory

## 🔗 Související Dokumentace

- `/osoby/osoba_2/` - Osobní plány pro Páju
- `/lednice/AKTUALNI_STAV.md` - Aktuální stav zásob
- `/docs/meal-planning/` - Dokumentace plánování

---

*Aktualizováno: 21.01.2026*
