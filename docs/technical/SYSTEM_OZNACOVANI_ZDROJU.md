# 📋 Systém označování zdrojů nutričních dat

**Datum vytvoření:** 19.1.2026  
**Účel:** Transparentní tracking zdrojů všech nutričních hodnot pro budoucí korekce a aktualizace

---

## 🎯 Proč označujeme zdroje?

1. **Transparentnost** - Jasné určení, odkud data pocházejí
2. **Aktualizace** - Snadná identifikace dat, která je třeba aktualizovat
3. **Důvěryhodnost** - Rozlišení mezi ověřenými a odhadovanými hodnotami
4. **Tracking** - Možnost sledovat, kdy byla data naposledy aktualizována

---

## 📊 Struktura označení

Každý produkt v `potraviny/soubory/*.yaml` by měl obsahovat:

```yaml
nazev: Název produktu
kategorie: kategorie
kalorie: 100
bilkoviny: 10
sacharidy: 5
tuky: 2
vlaknina: 1
# ... další pole ...

# POVINNÉ pole pro tracking zdrojů
zdroj: "kaloricketabulky.cz"        # Odkud data pocházejí
datum_aktualizace: "2026-01-19"     # Kdy byla data aktualizována (YYYY-MM-DD)
```

---

## 🏷️ Typy zdrojů

### 1. `kaloricketabulky.cz`
**Popis:** Data stažena z oficiální české databáze kaloricketabulky.cz  
**Důvěryhodnost:** ⭐⭐⭐⭐⭐ Vysoká - ověřená databáze  
**Použití:** Preferovaný zdroj pro české potraviny  
**Počet produktů:** 16

**Poznámka:** V kaloricketabulky.cz platí:
- "Sacharidy" = NET carbs (bez vlákniny)
- "Vláknina" = uvedena samostatně, ~2 kcal/g

**Příklad produktů:**
- Brokolice, Špenát, Květák, Okurka, Rajčata
- Vejce na tvrdo, Tuňák v slunečnicovém oleji
- Eidam 30% plátky, Jihočeský eidam 20%

---

### 2. `původní databáze`
**Popis:** Data byla v databázi před 19.1.2026, zdroj není dokumentován  
**Důvěryhodnost:** ⭐⭐⭐ Střední - pravděpodobně správné, ale neověřené  
**Použití:** Starší data čekající na ověření  
**Počet produktů:** 25

**Doporučení:** Tyto produkty by měly být postupně ověřeny a přesunuty na konkrétní zdroj.

**Příklad produktů:**
- Chia semínka, Mandle, Vlašské ořechy
- Kuřecí prsa, Hovězí maso, Losos
- Cottage cheese, Tvaroh polotučný
- Cuketa, Zelí, Paprika

---

### 3. `manuální`
**Popis:** Data zadána manuálně uživatelem nebo z nespecifikovaného zdroje  
**Důvěryhodnost:** ⭐⭐⭐ Střední až vysoká - závisí na zdroji  
**Použití:** Data bez konkrétní databáze jako zdroje  
**Počet produktů:** 1

**Příklad produktů:**
- Sýr eidam (45%)

---

### 4. `AI-generováno: <model>` ⚠️
**Popis:** Hodnoty vygenerovány AI modelem (např. GPT-4, Claude)  
**Důvěryhodnost:** ⭐ Nízká - pouze odhad, **VYŽADUJE OVĚŘENÍ**  
**Použití:** Pouze dočasně, dokud nejsou nahrazeny ověřenými daty  
**Počet produktů:** 0 (aktuálně žádné)

**DŮLEŽITÉ:**
- ❌ Nikdy nepoužívat pro production výpočty
- ⚠️ Označit červeně ve všech výstupech
- 🔄 Co nejdříve nahradit ověřenými daty

**Formát:**
```yaml
zdroj: "AI-generováno: GPT-4"
datum_aktualizace: "2026-01-19"
poznamky: "⚠️ NEOVĚŘENÉ - pouze odhad AI, vyžaduje ověření z oficiálního zdroje"
```

---

### 5. `USDA`
**Popis:** Data z americké databáze USDA FoodData Central  
**Důvěryhodnost:** ⭐⭐⭐⭐⭐ Velmi vysoká - oficálně ověřená databáze  
**Použití:** Pro potraviny bez českého ekvivalentu  
**Počet produktů:** 0 (aktuálně žádné)

**Poznámka:** USDA používá "Total Carbohydrates" (včetně vlákniny), na rozdíl od kaloricketabulky.cz

---

### 6. `obalová informace`
**Popis:** Data z nutričního štítku na obalu produktu  
**Důvěryhodnost:** ⭐⭐⭐⭐ Vysoká - oficiální údaje výrobce  
**Použití:** Pro specifické značkové produkty  
**Počet produktů:** 0 (aktuálně žádné)

**Formát:**
```yaml
zdroj: "obalová informace"
poznamky: "Značka XY, výrobce ABC, výrobní číslo 123"
```

---

## 🔄 Proces aktualizace zdrojů

### Krok 1: Identifikace produktů k ověření

```bash
# Zobraz produkty podle zdroje
python scripts/validate_nutrition_data.py --show-sources
```

### Krok 2: Ověření hodnot

1. Najdi produkt na [kaloricketabulky.cz](https://www.kaloricketabulky.cz/)
2. Porovnej hodnoty
3. Pokud se liší > 10%, aktualizuj

### Krok 3: Aktualizace YAML

```bash
# Použij helper
python scripts/update_nutrition_values.py "Název produktu"
```

Nebo manuálně:
```yaml
nazev: Produkt
# ... nutriční hodnoty ...
zdroj: "kaloricketabulky.cz"          # ← Aktualizuj
datum_aktualizace: "2026-01-19"       # ← Aktualizuj na dnešní datum
poznamky: "Původní zdroj: původní databáze, ověřeno 19.1.2026"
```

---

## ⚠️ DŮLEŽITÁ PRAVIDLA

### ✅ CO DĚLAT:
1. **Vždy označit zdroj** při přidání nového produktu
2. **Aktualizovat datum** při změně hodnot
3. **Používat ověřené zdroje** (kaloricketabulky.cz, USDA, obalová informace)
4. **Dokumentovat změny** v commit message

### ❌ CO NEDĚLAT:
1. **Nikdy nepoužívat AI-generované hodnoty** bez označení
2. **Neměnit hodnoty bez ověření** ze zdroje
3. **Nemíchat zdroje** - pokud měníš hodnotu, změň i zdroj
4. **Nepřidávat produkty bez zdroje**

---

## 📈 Statistiky zdrojů (aktuální stav)

```
Zdroj                      Počet    %      Důvěryhodnost
─────────────────────────────────────────────────────────
kaloricketabulky.cz          16    38%    ⭐⭐⭐⭐⭐
původní databáze             25    60%    ⭐⭐⭐ (čeká na ověření)
manuální                      1     2%    ⭐⭐⭐
AI-generováno                 0     0%    ⚠️ NEPOVOLENO bez označení
─────────────────────────────────────────────────────────
CELKEM                       42   100%
```

**Cíl:** 100% produktů s ověřeným zdrojem (kaloricketabulky.cz nebo USDA)

---

## 🔧 Nástroje pro práci se zdroji

### Validační skript
```bash
# Zobraz produkty podle zdroje
python scripts/validate_nutrition_data.py --group-by-source

# Zobraz produkty vyžadující ověření
python scripts/validate_nutrition_data.py --unverified
```

### Update helper
```bash
# Automaticky stáhne data z kaloricketabulky.cz
python scripts/update_nutrition_values.py "Brokolice"
# Automaticky nastaví: zdroj="kaloricketabulky.cz", datum=dnes
```

---

## 📝 Příklady správného označení

### ✅ SPRÁVNĚ - Ověřený produkt z kaloricketabulky.cz

```yaml
nazev: Brokolice
kategorie: zelenina
kalorie: 43.4
bilkoviny: 3.3
sacharidy: 5.7
tuky: 0.2
vlaknina: 3.0
poznamky: "Vysoký obsah vápníku (105mg/100g), cukry 2.49g"
zdroj: "kaloricketabulky.cz"
datum_aktualizace: "2026-01-19"
```

### ⚠️ DOČASNĚ PŘIJATELNÉ - Původní databáze

```yaml
nazev: Chia semínka
kategorie: orechy
kalorie: 486
bilkoviny: 17.0
sacharidy: 42.0
tuky: 31.0
vlaknina: 34.0
zdroj: "původní databáze"
datum_aktualizace: "2025-01-01"
# TODO: Ověřit z kaloricketabulky.cz
```

### ❌ ŠPATNĚ - AI generované bez označení

```yaml
nazev: Nějaký produkt
kalorie: 150
# ... hodnoty ...
# CHYBÍ zdroj a datum! ❌
```

### ✅ VÝJIMEČNĚ POVOLENO - AI s jasným označením

```yaml
nazev: Exotický produkt XYZ
kalorie: 200
bilkoviny: 15
sacharidy: 10
tuky: 5
vlaknina: 3
zdroj: "AI-generováno: GPT-4"
datum_aktualizace: "2026-01-19"
poznamky: "⚠️ NEOVĚŘENÉ - pouze odhad AI na základě podobných produktů. VYŽADUJE OVĚŘENÍ z oficiálního zdroje!"
```

---

## 🎯 Priorita ověření

**Vysoká priorita** (často používané):
1. Produkty se zdrojem "původní databáze" a vysokou frekvencí použití
2. Produkty s "AI-generováno"
3. Produkty s velkými nesrovnalostmi v kaloriích

**Střední priorita:**
4. Ostatní "původní databáze" produkty
5. Produkty "manuální" bez detailního zdroje

**Nízká priorita:**
6. Produkty již ověřené z kaloricketabulky.cz nebo USDA

---

## 📞 Kontakt

Pokud najdete produkt bez správného označení zdroje nebo s podezřelými hodnotami, prosím:
1. Vytvořte issue v GitHubu
2. Označte produkt a uveďte důvod
3. Pokud máte ověřená data, navrhněte opravu

---

**Poslední aktualizace:** 19.1.2026  
**Verze:** 1.0  
**Autor:** GitHub Copilot Coding Agent
