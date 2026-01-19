# 📋 Seznam produktů k aktualizaci nutričních hodnot

**Datum vytvoření:** 19.1.2026  
**Účel:** Identifikace a aktualizace nepřesných nebo neúplných nutričních dat v databázi potravin

---

## 📊 Přehled

**Celkový stav databáze:**
- 📦 **Celkem produktů:** 34
- ✅ **Produkty v pořádku:** 15 (44%)
- ⚠️ **Produkty s menšími problémy:** 10 (29%)
- ❌ **Produkty vyžadující aktualizaci:** 9 (26%)

---

## ❌ PRIORITNÍ AKTUALIZACE (9 produktů)

Tyto produkty mají významné nesrovnalosti mezi uvedenými kaloriemi a kaloriemi vypočtenými z makroživin. Kalorie by měly odpovídat vzorci: `kalorie = (bílkoviny × 4) + (sacharidy × 4) + (tuky × 9)` s tolerancí ±15% kvůli alkoholu, vláknině a dalším složkám.

### 1. 🥦 Brokolice

**Soubor:** `potraviny/soubory/brokolice.yaml`  
**Kategorie:** zelenina

**Současné hodnoty (na 100g):**
- Kalorie: 34 kcal
- Bílkoviny: 2.8 g
- Sacharidy: 7.0 g
- Tuky: 0.4 g
- Vláknina: 2.6 g

**Problém:**
- ❌ Kalorie nesedí: uvedeno **34 kcal**, vypočteno z maker **42.8 kcal** (rozdíl 8.8 kcal)

**Doporučená akce:**
- Ověřit hodnoty na [kaloricketabulky.cz](https://www.kaloricketabulky.cz/?s=brokolice)
- Pravděpodobně je potřeba upravit sacharidy nebo kalorie
- Standardní hodnoty pro brokolici: ~34 kcal, 2.8g bílkovin, ~6.6g sacharidů, 0.4g tuků

---

### 2. 🥒 Cuketa

**Soubor:** `potraviny/soubory/cuketa.yaml`  
**Kategorie:** zelenina

**Současné hodnoty (na 100g):**
- Kalorie: 17 kcal
- Bílkoviny: 1.2 g
- Sacharidy: 3.1 g
- Tuky: 0.3 g
- Vláknina: 1.0 g

**Problém:**
- ❌ Kalorie nesedí: uvedeno **17 kcal**, vypočteno z maker **19.9 kcal** (rozdíl 2.9 kcal)

**Doporučená akce:**
- Ověřit na kaloricketabulky.cz
- Rozdíl je relativně malý, ale měl by být korigován

---

### 3. 🥬 Kedlubna

**Soubor:** `potraviny/soubory/kedlubna.yaml`  
**Kategorie:** zelenina

**Současné hodnoty (na 100g):**
- Kalorie: 27 kcal
- Bílkoviny: 1.7 g
- Sacharidy: 6.2 g
- Tuky: 0.1 g
- Vláknina: 3.6 g

**Problém:**
- ❌ Kalorie nesedí: uvedeno **27 kcal**, vypočteno z maker **32.5 kcal** (rozdíl 5.5 kcal)

**Doporučená akce:**
- Ověřit na kaloricketabulky.cz
- Pravděpodobně je potřeba upravit sacharidy nebo kalorie

---

### 4. 🥦 Květák

**Soubor:** `potraviny/soubory/květák.yaml`  
**Kategorie:** zelenina

**Současné hodnoty (na 100g):**
- Kalorie: 25 kcal
- Bílkoviny: 1.9 g
- Sacharidy: 5.0 g
- Tuky: 0.3 g
- Vláknina: 2.0 g

**Problém:**
- ❌ Kalorie nesedí: uvedeno **25 kcal**, vypočteno z maker **30.3 kcal** (rozdíl 5.3 kcal)

**Doporučená akce:**
- Ověřit na kaloricketabulky.cz
- Standardní hodnoty pro květák jsou podobné brokolici

---

### 5. 🥬 Ledový salát

**Soubor:** `potraviny/soubory/ledový_salát.yaml`  
**Kategorie:** zelenina

**Současné hodnoty (na 100g):**
- Kalorie: 16.1 kcal
- Bílkoviny: 0.7 g
- Sacharidy: 2.0 g
- Tuky: 0.14 g
- Vláknina: 1.2 g

**Problém:**
- ❌ Kalorie nesedí: uvedeno **16.1 kcal**, vypočteno z maker **12.1 kcal** (rozdíl 4.0 kcal)
- ℹ️ Tento produkt má vyšší uvedené kalorie než vypočtené - možná obsahuje více vody

**Doporučená akce:**
- Ověřit na kaloricketabulky.cz
- Ledový salát má velmi nízkou kalorickou hodnotu, data jsou pravděpodobně přesná

---

### 6. 🥒 Okurka

**Soubor:** `potraviny/soubory/okurka.yaml`  
**Kategorie:** zelenina

**Současné hodnoty (na 100g):**
- Kalorie: 15 kcal
- Bílkoviny: 0.7 g
- Sacharidy: 3.6 g
- Tuky: 0.1 g
- Vláknina: 0.5 g

**Problémy:**
- ❌ Kalorie nesedí: uvedeno **15 kcal**, vypočteno z maker **18.1 kcal** (rozdíl 3.1 kcal)
- ⚠️ Nízký obsah vlákniny (0.5g) pro zeleninu

**Doporučená akce:**
- Ověřit na kaloricketabulky.cz
- Okurka opravdu má nízký obsah vlákniny (převážně voda)
- Upravit kalorie nebo makroživiny

---

### 7. 🍅 Rajčata

**Soubor:** `potraviny/soubory/rajčata.yaml`  
**Kategorie:** zelenina

**Současné hodnoty (na 100g):**
- Kalorie: 18 kcal
- Bílkoviny: 0.9 g
- Sacharidy: 3.9 g
- Tuky: 0.2 g
- Vláknina: 1.2 g

**Problém:**
- ❌ Kalorie nesedí: uvedeno **18 kcal**, vypočteno z maker **21.0 kcal** (rozdíl 3.0 kcal)

**Doporučená akce:**
- Ověřit na kaloricketabulky.cz
- Standardní hodnoty pro rajčata

---

### 8. 🥬 Zelí

**Soubor:** `potraviny/soubory/zelí.yaml`  
**Kategorie:** zelenina

**Současné hodnoty (na 100g):**
- Kalorie: 25 kcal
- Bílkoviny: 1.3 g
- Sacharidy: 5.8 g
- Tuky: 0.1 g
- Vláknina: 2.5 g

**Problém:**
- ❌ Kalorie nesedí: uvedeno **25 kcal**, vypočteno z maker **29.3 kcal** (rozdíl 4.3 kcal)

**Doporučená akce:**
- Ověřit na kaloricketabulky.cz

---

### 9. 🥬 Špenát

**Soubor:** `potraviny/soubory/špenát.yaml`  
**Kategorie:** zelenina

**Současné hodnoty (na 100g):**
- Kalorie: 23 kcal
- Bílkoviny: 2.9 g
- Sacharidy: 3.6 g
- Tuky: 0.4 g
- Vláknina: 2.2 g

**Problém:**
- ❌ Kalorie nesedí: uvedeno **23 kcal**, vypočteno z maker **29.6 kcal** (rozdíl 6.6 kcal)

**Doporučená akce:**
- Ověřit na kaloricketabulky.cz
- Špenát má vyšší obsah bílkovin, takže by měl mít i více kalorií

---

## ⚠️ MENŠÍ PROBLÉMY K OVĚŘENÍ (10 produktů)

Tyto produkty mají menší problémy - většinou všechny hodnoty jsou celá čísla, což může indikovat aproximaci. Je dobré je ověřit pro větší přesnost.

### 1. Chia semínka ⚠️
**Soubor:** `potraviny/soubory/chia_semínka.yaml`  
**Problém:** Všechny hodnoty jsou celá čísla - možná aproximace  
**Aktuální:** kalorie 486, bílkoviny 17, sacharidy 42, tuky 31, vláknina 34

### 2. Hovězí maso (libové) ⚠️
**Soubor:** `potraviny/soubory/hovězí_maso_libové.yaml`  
**Problém:** Všechny hodnoty jsou celá čísla - možná aproximace  
**Aktuální:** kalorie 250, bílkoviny 26, sacharidy 0, tuky 17, vláknina 0

### 3. Krůtí prsa ⚠️
**Soubor:** `potraviny/soubory/krůtí_prsa.yaml`  
**Problém:** Všechny hodnoty jsou celá čísla - možná aproximace  
**Aktuální:** kalorie 135, bílkoviny 30, sacharidy 0, tuky 1, vláknina 0

### 4. Lněné semínko (mleté) ⚠️
**Soubor:** `potraviny/soubory/lněné_semínko_mleté.yaml`  
**Problém:** Všechny hodnoty jsou celá čísla - možná aproximace  
**Aktuální:** kalorie 534, bílkoviny 18, sacharidy 29, tuky 42, vláknina 27

### 5. Losos ⚠️
**Soubor:** `potraviny/soubory/losos.yaml`  
**Problém:** Všechny hodnoty jsou celá čísla - možná aproximace  
**Aktuální:** kalorie 208, bílkoviny 20, sacharidy 0, tuky 13, vláknina 0

### 6. Mandle ⚠️
**Soubor:** `potraviny/soubory/mandle.yaml`  
**Problém:** Všechny hodnoty jsou celá čísla - možná aproximace  
**Aktuální:** kalorie 579, bílkoviny 21, sacharidy 22, tuky 50, vláknina 12

### 7. Olivový olej ⚠️
**Soubor:** `potraviny/soubory/olivový_olej.yaml`  
**Problém:** Všechny hodnoty jsou celá čísla - možná aproximace  
**Aktuální:** kalorie 884, bílkoviny 0, sacharidy 0, tuky 100, vláknina 0  
**Poznámka:** Tyto hodnoty jsou pravděpodobně správné (čistý tuk)

### 8. Sýr gouda 45% ⚠️
**Soubor:** `potraviny/soubory/sýr_gouda_45%.yaml`  
**Problém:** Všechny hodnoty jsou celá čísla - možná aproximace  
**Aktuální:** kalorie 344, bílkoviny 26, sacharidy 0, tuky 27, vláknina 0

### 9. Tuňák kousky v oleji ⚠️
**Soubor:** `potraviny/soubory/tuňák_kousky_v_oleji.yaml`  
**Problém:** Všechny hodnoty jsou celá čísla - možná aproximace  
**Aktuální:** kalorie 159, bílkoviny 26, sacharidy 0, tuky 6, vláknina 0

### 10. Vejce slepičí M ⚠️
**Soubor:** `potraviny/soubory/vejce_slepičí_m.yaml`  
**Problém:** Nízký obsah bílkovin (12.38g) pro kategorii 'bilkoviny'  
**Aktuální:** kalorie 151, bílkoviny 12.38, sacharidy 0.95, tuky 10.87, vláknina 0  
**Poznámka:** Vejce jsou sice bílkovinová potravina, ale obsahují také hodně tuku. Hodnoty vypadají správně.

---

## ✅ PRODUKTY V POŘÁDKU (15 produktů)

Tyto produkty mají konzistentní a přesné nutriční hodnoty:

1. Avokádo
2. Cottage cheese
3. Fazole barevné pinto
4. Kysané zelí
5. Kuřecí prsa
6. Paprika
7. Sýr eidam
8. Tuňák (konzervovaný)
9. Tvaroh polotučný
10. Vlašské ořechy
11. Řecký jogurt
12. Ředkev bílá
13. Černá čočka
14. Červená čočka
15. Červená řepa

---

## 🔧 NÁSTROJE PRO AKTUALIZACI

### Automatická aktualizace pomocí web scraperu

V projektu máme k dispozici nástroj pro automatické stahování nutričních dat z české databáze [kaloricketabulky.cz](https://www.kaloricketabulky.cz/).

**Soubor:** `src/scrapers/fetch_nutrition_data.py`

#### Použití:

```bash
# Vyhledat produkt podle názvu
python src/scrapers/fetch_nutrition_data.py "Brokolice"

# Nebo použít přímo URL
python src/scrapers/fetch_nutrition_data.py "https://www.kaloricketabulky.cz/potraviny/brokolice"
```

#### Výstup obsahuje:
- Název produktu
- URL zdroje
- Makroživiny (kalorie, bílkoviny, sacharidy, tuky, vláknina, cukry)

### Manuální aktualizace

1. Otevřete příslušný YAML soubor v `potraviny/soubory/`
2. Vyhledejte produkt na [kaloricketabulky.cz](https://www.kaloricketabulky.cz/)
3. Aktualizujte hodnoty v YAML souboru
4. Ověřte, že kalorie odpovídají vzorci: `(bílkoviny × 4) + (sacharidy × 4) + (tuky × 9)`

### Formát YAML souboru

```yaml
nazev: Název produktu
kategorie: kategorie  # bilkoviny, zelenina, tuky, orechy, mlecne_vyrobky, lusteniny
kalorie: 100.0  # kcal na 100g
bilkoviny: 10.0  # g na 100g
sacharidy: 5.0   # g na 100g
tuky: 2.0        # g na 100g
vlaknina: 1.0    # g na 100g
cena_za_kg: 50.0  # volitelné
poznamky: "Dodatečné informace"  # volitelné
```

---

## 📝 POZNÁMKY A DOPORUČENÍ

### Proč jsou nesrovnalosti v kaloriích?

1. **Vláknina:** Vláknina má ~2 kcal/g, ne 4 kcal/g jako ostatní sacharidy
2. **Alkohol:** Některé potraviny obsahují alkohol (7 kcal/g)
3. **Rezistentní škrob:** Ne všechny sacharidy se vstřebají
4. **Zaokrouhlování:** Různé zdroje zaokrouhlují různě
5. **Chyby v datech:** Někdy jsou prostě data špatně

### Doporučený postup aktualizace

1. **Nejprve prioritní aktualizace** - 9 produktů s největšími nesrovnalostmi
2. **Pak menší problémy** - 10 produktů k ověření
3. **Použít web scraper** kde je to možné pro automatickou aktualizaci
4. **Ověřit výsledky** - zkontrolovat, že kalorie odpovídají makroživinám
5. **Commit po každé změně** - pro snadné sledování změn

### Priorita produktů podle frekvence použití

**Vysoká priorita (často používáme):**
- 🥦 Brokolice
- 🥒 Cuketa
- 🥬 Špenát
- 🍅 Rajčata
- 🥒 Okurka
- 🥬 Zelí

**Střední priorita:**
- 🥦 Květák
- 🥬 Kedlubna
- 🥬 Ledový salát

---

## 📊 STATISTIKY

```
Celkem produktů: 34
├── ✅ V pořádku: 15 (44%)
├── ⚠️  Menší problémy: 10 (29%)
└── ❌ Vyžaduje aktualizaci: 9 (26%)

Problémy podle typu:
├── Nesrovnalosti v kaloriích: 9 produktů
├── Zaokrouhlené hodnoty: 9 produktů
└── Nízký obsah vlákniny: 1 produkt

Kategorie s problémy:
├── Zelenina: 9/14 produktů (64% má problémy)
├── Bílkoviny: 4/12 produktů (33% má problémy)
├── Ořechy: 3/4 produktů (75% má problémy)
└── Ostatní: 3/4 produktů (75% má problémy)
```

---

## 🎯 AKČNÍ PLÁN

### Fáze 1: Prioritní aktualizace (1-2 hodiny)
- [ ] Brokolice
- [ ] Cuketa
- [ ] Špenát
- [ ] Rajčata
- [ ] Okurka
- [ ] Zelí
- [ ] Květák
- [ ] Kedlubna
- [ ] Ledový salát

### Fáze 2: Ověření (30 minut)
- [ ] Ověřit bílkovinové produkty (hovězí, krůtí, losos, tuňák)
- [ ] Ověřit ořechy a semínka (chia, lněné semínko, mandle)
- [ ] Ověřit mléčné výrobky (gouda)

### Fáze 3: Dokumentace
- [ ] Aktualizovat tento dokument o výsledky
- [ ] Vytvořit changelog změn
- [ ] Dokumentovat nové hodnoty v gitu

---

## 📚 REFERENCE

- **Nutriční databáze:** [kaloricketabulky.cz](https://www.kaloricketabulky.cz/)
- **USDA FoodData Central:** [fdc.nal.usda.gov](https://fdc.nal.usda.gov/)
- **Web scraper:** `src/scrapers/fetch_nutrition_data.py`
- **Validační skript:** V tomto PR (bude vytvořen)

---

**Vytvořeno:** 19.1.2026  
**Autor:** GitHub Copilot Coding Agent  
**Status:** 🚧 V procesu aktualizace
