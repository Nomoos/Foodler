# 🔧 Návod: Aktualizace nutričních hodnot

Tento dokument popisuje proces aktualizace nutričních hodnot v databázi potravin projektu Foodler.

---

## 📋 Přehled

Nutriční hodnoty v databázi potravin (`potraviny/soubory/*.yaml`) potřebují občas aktualizovat, protože:

1. **Nesrovnalosti v kaloriích** - Uvedené kalorie neodpovídají vypočteným z makroživin
2. **Zaokrouhlené hodnoty** - Všechny hodnoty jsou celá čísla (pravděpodobně aproximace)
3. **Neúplná data** - Chybí některé nutriční hodnoty
4. **Zastaralá data** - Data se mohla změnit od poslední aktualizace

---

## 🛠️ Dostupné nástroje

### 1. Seznam produktů k aktualizaci

**Soubor:** `docs/technical/SEZNAM_K_AKTUALIZACI_NUTRICNICH_HODNOT.md`

Obsahuje:
- ✅ Kompletní seznam všech produktů s problémy
- 📊 Detailní analýzu každého produktu
- 🎯 Prioritizaci podle důležitosti
- 📈 Statistiky a přehledy

### 2. Validační report (JSON)

**Soubor:** `nutritional_validation_report.json`

JSON soubor obsahující:
- Metadata o celkovém stavu databáze
- Seznam produktů vyžadujících aktualizaci
- Seznam produktů s menšími problémy
- Seznam produktů v pořádku

### 3. Helper skript pro aktualizaci

**Soubor:** `scripts/update_nutrition_values.py`

Interaktivní nástroj pro:
- 🔍 Vyhledání nutričních hodnot na kaloricketabulky.cz
- 📊 Porovnání současných a nových hodnot
- ✅ Kontrolu konzistence dat
- 💾 Automatické uložení změn

### 4. Prioritní seznam produktů

**Soubor:** `priority_update_list.txt`

Textový soubor s názvy produktů k prioritní aktualizaci.

---

## 🚀 Rychlý start

### Krok 1: Instalace závislostí

```bash
pip install -r requirements.txt
```

Potřebné balíčky:
- `requests` - pro HTTP požadavky
- `beautifulsoup4` - pro parsování HTML
- `pyyaml` - pro práci s YAML soubory

### Krok 2: Aktualizace jednoho produktu

```bash
python scripts/update_nutrition_values.py "Brokolice"
```

Skript:
1. Načte současná data z `potraviny/soubory/brokolice.yaml`
2. Vyhledá produkt na kaloricketabulky.cz
3. Porovná hodnoty
4. Zeptá se, zda chcete použít nová data

### Krok 3: Dávková aktualizace

```bash
python scripts/update_nutrition_values.py --batch priority_update_list.txt
```

Skript projde všechny produkty v seznamu a nabídne aktualizaci každého z nich.

---

## 📖 Detailní návod k použití

### Interaktivní režim (jeden produkt)

```bash
python scripts/update_nutrition_values.py "Název produktu"
```

**Příklady:**
```bash
python scripts/update_nutrition_values.py Brokolice
python scripts/update_nutrition_values.py "Kuřecí prsa"
python scripts/update_nutrition_values.py "Sýr gouda 45%"
```

**Výstup obsahuje:**

1. **Současná data** - aktuální nutriční hodnoty z YAML souboru
2. **Kontrola konzistence** - zda kalorie odpovídají makroživinám
3. **Vyhledání nových dat** - z kaloricketabulky.cz
4. **Porovnání hodnot** - současné vs. nalezené
5. **Volba akce:**
   - `a` (ano) - použít nová data
   - `n` (ne) - zrušit aktualizaci
   - `m` (manuální) - zadat hodnoty ručně

**Příklad výstupu:**

```
📦 AKTUÁLNÍ DATA PRO: Brokolice
============================================================
Kategorie: zelenina
Kalorie: 34.0 kcal
Bílkoviny: 2.8 g
Sacharidy: 7.0 g
Tuky: 0.4 g
Vláknina: 2.6 g

⚠️  VAROVÁNÍ: Současná data nejsou konzistentní
   Vypočtené kalorie: 42.8 kcal
   Rozdíl: 8.8 kcal

🔍 Vyhledávám: Brokolice
------------------------------------------------------------

📊 POROVNÁNÍ:
Hodnota         Současné     Nalezené     Rozdíl      
------------------------------------------------------------
Kalorie         34.0         35.0         +1.0        
Bílkoviny       2.8          2.8          0           
Sacharidy       7.0          6.6          -0.4        
Tuky            0.4          0.4          0           
Vláknina        2.6          2.6          0           

🔍 KONTROLA KONZISTENCE NOVÝCH DAT:
Uvedené kalorie: 35.0 kcal
Vypočtené kalorie: 35.6 kcal
Rozdíl: 0.6 kcal
✅ Data jsou konzistentní

🌐 Zdroj: https://www.kaloricketabulky.cz/potraviny/brokolice

============================================================
Chcete použít nová data? (a=ano, n=ne, m=manuální úprava):
```

### Dávkový režim (více produktů)

```bash
python scripts/update_nutrition_values.py --batch priority_update_list.txt
```

Skript zpracuje každý produkt ze seznamu a po každém se zeptá, zda chcete pokračovat.

**Formát seznamu:**
```
# Komentáře začínají #
Brokolice
Špenát
Cuketa
# další produkty...
```

### Manuální režim

Pokud vyberete možnost `m` (manuální), můžete zadat hodnoty ručně:

```
📝 MANUÁLNÍ ÚPRAVA:
Kalorie (kcal) [34.0]: 35
Bílkoviny (g) [2.8]: 
Sacharidy (g) [7.0]: 6.6
Tuky (g) [0.4]: 
Vláknina (g) [2.6]: 

Vypočtené kalorie: 35.6 kcal
Uvedené kalorie: 35.0 kcal
✅ Data jsou konzistentní

Uložit změny? (a/n):
```

---

## 🔍 Jak kontrolovat konzistenci dat

Kalorie by měly odpovídat vzorci:

```
kalorie = (bílkoviny × 4) + (sacharidy × 4) + (tuky × 9)
```

**Tolerance:** ±15% kvůli:
- Vláknině (má ~2 kcal/g, ne 4)
- Alkoholu (7 kcal/g)
- Rezistentnímu škrobu
- Zaokrouhlování

**Příklad:**

Brokolice má:
- Bílkoviny: 2.8 g → 2.8 × 4 = 11.2 kcal
- Sacharidy: 7.0 g → 7.0 × 4 = 28.0 kcal
- Tuky: 0.4 g → 0.4 × 9 = 3.6 kcal
- **Celkem vypočteno:** 42.8 kcal

Ale uvedeno je: **34 kcal**

**Rozdíl:** 8.8 kcal (26% rozdíl) ❌ Překračuje toleranci

---

## 📝 Manuální aktualizace (bez skriptu)

Pokud nechcete použít skript, můžete aktualizovat hodnoty manuálně:

### 1. Najděte produkt na kaloricketabulky.cz

Otevřete: https://www.kaloricketabulky.cz/  
Vyhledejte produkt (např. "brokolice")

### 2. Otevřete YAML soubor

```bash
nano potraviny/soubory/brokolice.yaml
```

### 3. Aktualizujte hodnoty

```yaml
nazev: Brokolice
kategorie: zelenina
kalorie: 35.0    # ← aktualizujte
bilkoviny: 2.8
sacharidy: 6.6   # ← aktualizujte
tuky: 0.4
vlaknina: 2.6
cena_za_kg: 50.0
sezona:
- '9'
- '10'
# ... atd
```

### 4. Ověřte konzistenci

```bash
python3 << EOF
p, c, f = 2.8, 6.6, 0.4  # bílkoviny, sacharidy, tuky
calc = (p * 4) + (c * 4) + (f * 9)
stated = 35.0
print(f"Vypočteno: {calc:.1f} kcal")
print(f"Uvedeno: {stated:.1f} kcal")
print(f"Rozdíl: {abs(calc - stated):.1f} kcal")
print(f"OK" if abs(calc - stated) <= stated * 0.15 else "CHYBA")
EOF
```

### 5. Commitněte změny

```bash
git add potraviny/soubory/brokolice.yaml
git commit -m "Aktualizace nutričních hodnot: Brokolice"
```

---

## 🎯 Doporučený postup aktualizace

### Fáze 1: Prioritní produkty (zelenina)

Tyto produkty používáme nejčastěji, aktualizujte je jako první:

```bash
python scripts/update_nutrition_values.py Brokolice
python scripts/update_nutrition_values.py Špenát
python scripts/update_nutrition_values.py Cuketa
python scripts/update_nutrition_values.py Rajčata
python scripts/update_nutrition_values.py Okurka
python scripts/update_nutrition_values.py Zelí
```

Nebo dávkově:
```bash
python scripts/update_nutrition_values.py --batch priority_update_list.txt
```

### Fáze 2: Střední priorita

```bash
python scripts/update_nutrition_values.py Květák
python scripts/update_nutrition_values.py Kedlubna
python scripts/update_nutrition_values.py "Ledový salát"
```

### Fáze 3: Ověření zaokrouhlených hodnot

Tyto produkty mají pravděpodobně správné hodnoty, ale jsou zaokrouhlené:

```bash
python scripts/update_nutrition_values.py "Hovězí maso (libové)"
python scripts/update_nutrition_values.py "Krůtí prsa"
python scripts/update_nutrition_values.py Losos
# atd.
```

---

## 🐛 Řešení problémů

### Problem: Skript nenajde modul fetch_nutrition_data

**Řešení:** Ujistěte se, že jste ve správném adresáři projektu:

```bash
cd /path/to/Foodler
python scripts/update_nutrition_values.py Brokolice
```

### Problem: Web scraper nenajde produkt

**Možné důvody:**
1. Název produktu se liší od názvu na kaloricketabulky.cz
2. Produkt není v databázi
3. Síťový problém

**Řešení:** 
- Zkuste hledat ručně na webu a použijte přesný název
- Použijte manuální režim (`m`)

### Problem: Data nejsou konzistentní ani po aktualizaci

**Důvody:**
- Vláknina má jinou energetickou hodnotu (2 kcal/g)
- Alkohol (7 kcal/g)
- Rezistentní škrob

**Řešení:** Pokud je rozdíl malý (<15%), data jsou v pořádku

### Problem: Soubor nenalezen

**Chyba:**
```
❌ Soubor nenalezen: potraviny/soubory/nějaký_produkt.yaml
```

**Řešení:** Zkontrolujte název souboru:
```bash
ls potraviny/soubory/
```

Název souboru musí přesně odpovídat (včetně háčků a čárek).

---

## 📊 Formát YAML souboru

```yaml
nazev: Název produktu
kategorie: kategorie  # bilkoviny, zelenina, tuky, orechy, mlecne_vyrobky, lusteniny
kalorie: 100.0  # kcal na 100g
bilkoviny: 10.0  # g na 100g
sacharidy: 5.0   # g na 100g
tuky: 2.0        # g na 100g
vlaknina: 1.0    # g na 100g
cena_za_kg: 50.0  # volitelné, Kč/kg
sezona:           # volitelné, měsíce dostupnosti
- '6'
- '7'
- '8'
poznamky: "Dodatečné informace"  # volitelné
```

**Pravidla:**
- Všechny číselné hodnoty jsou float (desetinná čísla)
- Kategorie je jedna z: `bilkoviny`, `zelenina`, `tuky`, `orechy`, `mlecne_vyrobky`, `lusteniny`
- Všechny základní nutriční hodnoty (kalorie, bílkoviny, sacharidy, tuky, vláknina) jsou povinné
- Hodnoty jsou na 100g produktu

---

## 📚 Reference

- **Nutriční databáze:** [kaloricketabulky.cz](https://www.kaloricketabulky.cz/)
- **USDA FoodData Central:** [fdc.nal.usda.gov](https://fdc.nal.usda.gov/) (anglicky)
- **Web scraper:** `src/scrapers/fetch_nutrition_data.py`
- **Seznam k aktualizaci:** `docs/technical/SEZNAM_K_AKTUALIZACI_NUTRICNICH_HODNOT.md`
- **Validační report:** `nutritional_validation_report.json`

---

## ✅ Checklist po dokončení aktualizace

Po aktualizaci nutričních hodnot:

- [ ] Všechny prioritní produkty aktualizovány
- [ ] Data jsou konzistentní (kalorie odpovídají makroživinám)
- [ ] Změny commitnuty do gitu
- [ ] Spuštěn validační test
- [ ] Aktualizován SEZNAM_K_AKTUALIZACI_NUTRICNICH_HODNOT.md
- [ ] Vytvořen changelog změn

---

**Vytvořeno:** 19.1.2026  
**Autor:** GitHub Copilot Coding Agent  
**Verze:** 1.0
