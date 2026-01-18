# Návod k Použití - Týdenní Jídelníčky v Markdown Formátu

## 🎯 Rychlý Start

### Krok 1: Vygeneruj Týdenní Jídelníček

```bash
cd scripts
python3 generate_weekly_meal_plan_md.py 19.1.2026
```

**Výstup:**
```
======================================================================
🍽️  GENEROVÁNÍ TÝDENNÍHO JÍDELNÍČKU
======================================================================

✅ Pondělí 19.01.2026 → day_1_2026-01-19_pondělí.md
✅ Úterý 20.01.2026 → day_2_2026-01-20_úterý.md
✅ Středa 21.01.2026 → day_3_2026-01-21_středa.md
✅ Čtvrtek 22.01.2026 → day_4_2026-01-22_čtvrtek.md
✅ Pátek 23.01.2026 → day_5_2026-01-23_pátek.md
✅ Sobota 24.01.2026 → day_6_2026-01-24_sobota.md
✅ Neděle 25.01.2026 → day_7_2026-01-25_neděle.md

📋 Generuji týdenní souhrn...
✅ Týdenní souhrn → README.md

🛒 Generuji nákupní seznam...
✅ Nákupní seznam → shopping_list.md

✅ HOTOVO!
📁 Všechny soubory uloženy v: ../data/meal_plans/weekly/week_2026-01-19
```

### Krok 2: Zobraz Týdenní Souhrn

```bash
cd ../data/meal_plans/weekly/week_2026-01-19
cat README.md
```

nebo otevři v GitHub/VS Code pro pěkné zobrazení!

### Krok 3: Vytiskni Nákupní Seznam

```bash
cat shopping_list.md
```

Nebo otevři v prohlížeči a vytiskni (Ctrl+P).

---

## 📁 Struktura Souborů

Po spuštění generátoru se vytvoří tato struktura:

```
data/meal_plans/weekly/week_2026-01-19/
├── README.md                        📋 Týdenní souhrn
├── day_1_2026-01-19_pondělí.md      🍽️ Pondělí
├── day_2_2026-01-20_úterý.md        🍽️ Úterý
├── day_3_2026-01-21_středa.md       🍽️ Středa
├── day_4_2026-01-22_čtvrtek.md      🍽️ Čtvrtek
├── day_5_2026-01-23_pátek.md        🍽️ Pátek
├── day_6_2026-01-24_sobota.md       🍽️ Sobota
├── day_7_2026-01-25_neděle.md       🍽️ Neděle
└── shopping_list.md                 🛒 Nákupní seznam
```

---

## 📖 Obsah Souborů

### README.md - Týdenní Souhrn

**Obsahuje:**
- 📅 Přehled celého týdne
- 🔗 Odkazy na jednotlivé dny
- 🔗 Odkaz na nákupní seznam
- 📊 Statistiky (35 jídel, vegetariánské varianty)

**Příklad:**
```markdown
# Týdenní Jídelníček

**Týden: 19.01.2026 - 25.01.2026**

## 📅 Přehled Týdne

### Pondělí 19.01.2026
**Snídaně:** Pohankové vločky, sójové mléko, jablko...
[📄 Celý jídelníček](day_1_2026-01-19_pondělí.md)

### Úterý 20.01.2026
**Snídaně:** Mrkev, jablko, med, rozinky...
[📄 Celý jídelníček](day_2_2026-01-20_úterý.md)
```

### day_X_YYYY-MM-DD_den.md - Jídelníček Dne

**Obsahuje:**
- 🌅 Snídaně
- 🍎 Dopolední svačina
- 🍽️ Oběd (+ vegetariánská varianta)
- 🥤 Odpolední svačina
- 🌙 Večeře
- 💡 Tipy pro přípravu

**Příklad:**
```markdown
# Jídelníček - Pondělí 19.01.2026

**Den 19 z 28denního cyklu**

---

## 🌅 Snídaně
Pohankové vločky, sójové mléko, jablko, vlašské ořechy, med

---

## 🍎 Dopolední Svačina
Ovocný salát

---

## 🍽️ Oběd
Treska na másle, celerové pyré / Vegetarián: Indické tofu, celerové pyré
```

### shopping_list.md - Nákupní Seznam

**Obsahuje:**
- ☑️ Checkboxy pro označení položek
- 📦 Kategorie: Zelenina, Ovoce, Maso, Mléčné produkty, Obiloviny, Ořechy, Koření
- 🔢 Frekvence použití každé ingredience
- 💡 Tipy pro nákup
- 📊 Statistiky

**Příklad:**
```markdown
# Nákupní Seznam

**Týden: 19.01.2026 - 25.01.2026**

## Zelenina
- [ ] **Brokolice s česnekem** (použito 3× během týdne)
- [ ] **Mrkev** (použito 3× během týdne)

## Ovoce
- [ ] **Jablko** (použito 7× během týdne)
- [ ] **Rozinky** (použito 3× během týdne)

## Maso a Ryby
- [ ] **Treska na másle** (použito 2× během týdne)
- [ ] **Tuňák** (použito 2× během týdne)
```

---

## 🎨 Jak Používat MD Soubory

### 1. Zobrazení v Textovém Editoru

```bash
# Nano
nano README.md

# Vim
vim README.md

# VS Code
code README.md
```

### 2. Zobrazení v GitHub/GitLab

Prostě otevři soubor v prohlížeči - GitHub automaticky zobrazí formátovaný Markdown!

### 3. Konverze do HTML

```bash
# Pomocí pandoc
pandoc README.md -o jidelnicek.html

# Pomocí markdown-it
markdown-it README.md > jidelnicek.html
```

### 4. Tisk

**V prohlížeči:**
1. Otevři MD soubor v VS Code nebo GitHub
2. Použij preview mode
3. Stiskni Ctrl+P (Cmd+P na Mac)
4. Vytiskni

**Z příkazové řádky:**
```bash
# Konverze do PDF
pandoc shopping_list.md -o nakupni_seznam.pdf

# Nebo použij wkhtmltopdf
wkhtmltopdf shopping_list.html nakupni_seznam.pdf
```

### 5. Mobilní Telefon

**Varianta A - GitHub:**
1. Pushni soubory do repozitáře
2. Otevři GitHub na mobilu
3. Procházej soubory

**Varianta B - Syncthing:**
1. Synchronizuj složku `week_2026-01-19` do telefonu
2. Použij Markdown viewer app (např. Markor na Android)
3. Otevři soubory offline

**Varianta C - Email:**
1. Pošli si MD soubory emailem
2. Otevři na telefonu
3. Většina emailových klientů zobrazí Markdown správně

---

## 💡 Praktické Tipy

### Meal Prep - Příprava Dopředu

```markdown
NEDĚLE (příprava na týden):
✅ Nakup podle shopping_list.md
✅ Připrav:
   - Pohankové vločky (2× tento týden)
   - Vařené jáhly (2× tento týden)
   - Umyj zeleninu
   - Nakrájej mrkev

BĚHEM TÝDNE:
✅ Pondělí: Připrav na úterý - nakrájej zeleninu na salát
✅ Středa: Připrav na čtvrtek - vař těstoviny
✅ Pátek: Připrav na víkend - nakrájej zeleninu
```

### Editace Checkboxů

V nákupním seznamu můžeš označovat položky:

```markdown
# Před nákupem
- [ ] **Jablko**

# Po koupení
- [x] **Jablko**
```

### Sdílení s Rodinou

```bash
# Pošli celou složku
zip -r jidelnicek_tyden_19.zip week_2026-01-19/
# Pošli emailem nebo přes WhatsApp

# Nebo sdílej přes GitHub
git add .
git commit -m "Jídelníček na týden 19-25.1.2026"
git push
# Pošli odkaz na GitHub
```

---

## 🔄 Generování Dalších Týdnů

```bash
cd scripts

# Další týden
python3 generate_weekly_meal_plan_md.py 26.1.2026

# Únor
python3 generate_weekly_meal_plan_md.py 2.2.2026

# Březen
python3 generate_weekly_meal_plan_md.py 2.3.2026
```

Každý týden se vytvoří do vlastní složky: `week_YYYY-MM-DD/`

---

## 🆘 Řešení Problémů

### "Soubor nenalezen"

```bash
# Ujisti se, že jsi ve složce scripts
cd /home/runner/work/Foodler/Foodler/scripts

# Spusť skript
python3 generate_weekly_meal_plan_md.py 19.1.2026
```

### "Neplatný formát data"

```bash
# Správné formáty
python3 generate_weekly_meal_plan_md.py 19.1.2026    ✅
python3 generate_weekly_meal_plan_md.py 2026-01-19   ✅

# Špatné formáty
python3 generate_weekly_meal_plan_md.py 1/19/2026    ❌
python3 generate_weekly_meal_plan_md.py 19-1-2026    ❌
```

### MD soubory nejsou pěkně formátované

- Použij GitHub/GitLab preview
- Nebo VS Code s Markdown preview (Ctrl+Shift+V)
- Nebo nainstaluj Markdown viewer

---

## 📚 Související Dokumentace

- [scripts/README.md](../scripts/README.md) - Všechny dostupné skripty
- [CHANGELOG_2026-01-18.md](../CHANGELOG_2026-01-18.md) - Historie změn
- [docs/REORGANIZATION.md](../docs/REORGANIZATION.md) - Reorganizace projektu

---

## ✨ Výhody MD Formátu

| Vlastnost | JSON | Markdown |
|-----------|------|----------|
| Čitelnost | ❌ Ne | ✅ Ano |
| Editovatelnost | ❌ Těžké | ✅ Snadné |
| Tisknutelné | ❌ Ne | ✅ Ano |
| Checkboxy | ❌ Ne | ✅ Ano |
| Odkazy | ❌ Ne | ✅ Ano |
| Mobilní zobrazení | ❌ Složité | ✅ Jednoduché |
| GitHub preview | ❌ Ne | ✅ Ano |

---

*Vytvořeno: 18.1.2026*
*Verze: 1.0*
