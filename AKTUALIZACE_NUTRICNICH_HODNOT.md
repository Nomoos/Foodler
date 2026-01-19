# 📋 Aktualizace nutričních hodnot - Souhrn

**Datum:** 19.1.2026  
**Status:** ✅ Analýza dokončena, nástroje připraveny  
**Další krok:** Aktualizace prioritních produktů (volitelné)

---

## 🎯 Rychlý přehled

Z **34 produktů** v databázi:
- ✅ **15 produktů** (44%) - v pořádku
- ⚠️ **10 produktů** (29%) - menší problémy (zaokrouhlené hodnoty)
- ❌ **9 produktů** (26%) - **vyžadují aktualizaci** (nesrovnalosti v kaloriích)

---

## 📚 Dokumentace

### 1. Detailní seznam k aktualizaci
**Soubor:** [`docs/technical/SEZNAM_K_AKTUALIZACI_NUTRICNICH_HODNOT.md`](docs/technical/SEZNAM_K_AKTUALIZACI_NUTRICNICH_HODNOT.md)

Obsahuje:
- Kompletní seznam všech 9 produktů s prioritní potřebou aktualizace
- Detailní analýzu každého produktu (současné hodnoty, problémy, doporučení)
- Seznam 10 produktů s menšími problémy
- Statistiky a přehledy

### 2. Návod k použití nástrojů
**Soubor:** [`docs/technical/NAVOD_AKTUALIZACE_NUTRICNICH_HODNOT.md`](docs/technical/NAVOD_AKTUALIZACE_NUTRICNICH_HODNOT.md)

Obsahuje:
- Kompletní návod k použití helper skriptu
- Příklady použití
- Řešení problémů
- Checklist po dokončení

### 3. Validační report (JSON)
**Soubor:** `nutritional_validation_report.json`

JSON soubor s kompletními výsledky analýzy pro další zpracování.

---

## 🛠️ Nástroje

### Helper skript pro aktualizaci
**Soubor:** `scripts/update_nutrition_values.py`

```bash
# Nápověda
python scripts/update_nutrition_values.py

# Aktualizovat jeden produkt
python scripts/update_nutrition_values.py Brokolice

# Dávková aktualizace
python scripts/update_nutrition_values.py --batch priority_update_list.txt
```

### Prioritní seznam
**Soubor:** `priority_update_list.txt`

Seznam 9 prioritních produktů k aktualizaci, připravený pro dávkové zpracování.

---

## ❌ Produkty vyžadující aktualizaci (prioritní)

### Vysoká priorita (často používáme):
1. **Brokolice** - rozdíl 8.8 kcal (26%)
2. **Špenát** - rozdíl 6.6 kcal (29%)
3. **Cuketa** - rozdíl 2.9 kcal (17%)
4. **Rajčata** - rozdíl 3.0 kcal (17%)
5. **Okurka** - rozdíl 3.1 kcal (21%) + nízká vláknina
6. **Zelí** - rozdíl 4.3 kcal (17%)

### Střední priorita:
7. **Květák** - rozdíl 5.3 kcal (21%)
8. **Kedlubna** - rozdíl 5.5 kcal (20%)
9. **Ledový salát** - rozdíl 4.0 kcal (25%)

**Poznámka:** Všechny produkty jsou zelenina, což naznačuje systematický problém s vlákninou v kalkulaci kalorií.

---

## ⚠️ Produkty s menšími problémy

Tyto produkty mají zaokrouhlené hodnoty (všechna celá čísla), což může indikovat aproximaci:

- Chia semínka
- Hovězí maso (libové)
- Krůtí prsa
- Lněné semínko (mleté)
- Losos
- Mandle
- Olivový olej (pravděpodobně v pořádku - čistý tuk)
- Sýr gouda 45%
- Tuňák kousky v oleji
- Vejce slepičí M (bílkoviny 12.38g jsou v pořádku pro vejce)

---

## 🚀 Jak začít

### Instalace závislostí
```bash
pip install -r requirements.txt
```

### Aktualizace prioritních produktů

**Doporučený postup:**

1. **Dávková aktualizace** všech prioritních produktů:
   ```bash
   python scripts/update_nutrition_values.py --batch priority_update_list.txt
   ```

2. **Nebo postupně** jeden po druhém:
   ```bash
   python scripts/update_nutrition_values.py Brokolice
   python scripts/update_nutrition_values.py Špenát
   python scripts/update_nutrition_values.py Cuketa
   # ... atd
   ```

3. **Po každé aktualizaci** commit změn:
   ```bash
   git add potraviny/soubory/*.yaml
   git commit -m "Aktualizace nutričních hodnot: <názvy produktů>"
   ```

---

## 🔍 Proč je potřeba aktualizovat?

**Problém:** Kalorie uvedené v databázi neodpovídají kaloriím vypočteným z makroživin.

**Vzorec:** `kalorie = (bílkoviny × 4) + (sacharidy × 4) + (tuky × 9)`

**Příklad - Brokolice:**
- **Uvedeno:** 34 kcal
- **Vypočteno:** 42.8 kcal (2.8×4 + 7.0×4 + 0.4×9)
- **Rozdíl:** 8.8 kcal (26% chyba)

**Důvody nesrovnalostí:**
1. Vláknina má ~2 kcal/g, ne 4 kcal/g jako ostatní sacharidy
2. Různé zdroje dat používají různé metody výpočtu
3. Zaokrouhlování
4. Rezistentní škrob

---

## 📊 Statistiky

```
Problémy podle kategorie:
├── Zelenina: 9/14 produktů (64% má problémy) ← největší problém
├── Bílkoviny: 4/12 produktů (33% má problémy)
├── Ořechy: 3/4 produktů (75% má problémy)
└── Ostatní: 3/4 produktů (75% má problémy)

Typy problémů:
├── Nesrovnalosti v kaloriích: 9 produktů ← priorita
├── Zaokrouhlené hodnoty: 9 produktů
└── Nízký obsah vlákniny: 1 produkt
```

---

## 📞 Reference

- **Web scraper:** `src/scrapers/fetch_nutrition_data.py`
- **Nutriční databáze:** [kaloricketabulky.cz](https://www.kaloricketabulky.cz/)
- **USDA databáze:** [fdc.nal.usda.gov](https://fdc.nal.usda.gov/)

---

## ✅ Další kroky

- [ ] Přečíst dokumentaci: `docs/technical/NAVOD_AKTUALIZACE_NUTRICNICH_HODNOT.md`
- [ ] Aktualizovat 9 prioritních produktů
- [ ] Ověřit 10 produktů s menšími problémy
- [ ] Commit změn do gitu
- [ ] Aktualizovat tento dokument o výsledky

---

**Vytvořeno:** GitHub Copilot Coding Agent  
**Verze:** 1.0
