# 📝 Analýza Jídelníčku Pája - Den 2 (Úterý 20.01.2026)

## 📂 Soubory v této složce

### 1. **PAJA_DEN_2_RYCHLY_PREHLED.md** ⚡
**Pro koho:** Rychlé použití - chci jen vědět CO přidat  
**Obsah:**
- ✅ Co je už nachystáno
- 🎯 Co přidat (rychlý seznam)
- 🛒 Nákupní seznam
- 📊 Výsledky (stručně)

**→ Doporučeno začít tímto souborem!**

---

### 2. **PAJA_DEN_2_DOPORUCENI.md** 📋
**Pro koho:** Detailní plánování - chci vědět PROČ a JAK  
**Obsah:**
- Kompletní nutriční analýza
- Podrobná tabulka potravin
- Vysvětlení nedostatků
- Dvě varianty jídelníčku:
  - ✅ Oběd doma (ideální)
  - ✅ Oběd v práci (praktická)
- Tipy na meal prep
- Priorita expirujících sýrů

**→ Pro hloubkovou analýzu a plánování**

---

### 3. **analyze_paja_meals.py** 🔧
**Pro koho:** Python skript pro vlastní analýzu  
**Použití:**
```python
from scripts.analyze_paja_meals import MealAnalyzer

analyzer = MealAnalyzer()
analyzer.pridat_potravinu("ledový salát", 100)
analyzer.pridat_potravinu("mandle", 30)
analyzer.pridat_potravinu("avokádo", 80)
# ... přidat další potraviny
analyzer.analyzovat()
```

**→ Pro interaktivní testování vlastních jídelníčků**

---

## 🎯 RYCHLÉ SHRNUTÍ

### ❓ Otázky uživatele:

1. **Co nachystat dále?**
2. **Co vyřadit pokud má oběd v práci?**
3. **Mám ještě něco přidat?**

### ✅ ODPOVĚDI:

#### 1️⃣ CO NACHYSTAT DÁLE?

**UŽ MÁTE DOMA (ze zásob):**
- Paprika červená kapia 100g
- Mandle 20g
- Vlašské ořechy 15g
- Chia semínka 10g
- Lněná semínka 10g
- Tvaroh polotučný 80g
- Olivový olej 15ml
- Gouda Light 25g (❗ vyprší zítra!)

**DOKOUPIT (60-93 Kč):**
- Avokádo 1 ks (80g)
- Tuňák v oleji 1 plechovka
- Rajče 80g
- Ledový salát 100g (další)
- Brokolice 200g (jen pokud oběd doma)

---

#### 2️⃣ CO VYŘADIT POKUD MÁ OBĚD V PRÁCI?

**VYŘADIT:**
- ❌ Brokolice 200g (těžko přenášet)
- ❌ Olivový olej na vaření

**VZÍT DO PRÁCE:**
- ✅ Řecký jogurt 100g + med 14g (v krabičce)
- ✅ Chia semínka 10g (do jogurtu)
- ✅ Mandle 20g (v sáčku)

---

#### 3️⃣ MÁM JEŠTĚ NĚCO PŘIDAT?

**ANO! Tyto položky:**

**Kritické nedostatky v původním plánu:**
- ❌ Vláknina: pouze 1.3g z 20g (6.5%) - VELMI NÍZKÉ!
- ❌ Kalorie: pouze 681 z 1508 kcal (45%) - chybí více než polovina!
- ❌ Bílkoviny: 59g z 92g (64%) - chybí 33g
- ❌ Tuky: 42g z 100g (42%) - chybí 58g

**Řešení - přidat:**
1. **Zeleninu** → vláknina (paprika, avokádo, rajče, salát, brokolice)
2. **Ořechy a semínka** → tuky + vláknina (mandle, vlašské, chia, lněná)
3. **Tvaroh** → bílkoviny (80g)
4. **Tuňák** → bílkoviny (50g další)
5. **Olivový olej** → zdravé tuky (15ml)

---

## 📊 VÝSLEDKY

### ✅ S DOPORUČENÝMI ÚPRAVAMI:

**OBĚD DOMA:**
```
1626 kcal | 104g P | 68g S | 110g T | 26g V
✅ 108% cíle kalorií
✅ 113% cíle bílkovin
⚠️  114% cíle sacharidů (trochu více, ale OK)
✅ 110% cíle tuků
✅ 130% cíle vlákniny
```

**OBĚD V PRÁCI:**
```
1449 kcal | 99g P | 66g S | 86g T | 25g V
✅ 96% cíle kalorií
✅ 108% cíle bílkovin
✅ 110% cíle sacharidů
✅ 86% cíle tuků
✅ 125% cíle vlákniny
```

---

## 🏆 ZÁVĚR

**Původní nachystané jídlo:** Pouze 45% denních kalorií ❌  
**S našimi úpravami:** 96-108% všech cílů ✅

**Hlavní změny:**
1. ✅ Přidána zelenina pro vlákninu
2. ✅ Přidány ořechy a semínka pro tuky
3. ✅ Přidán tvaroh a tuňák pro bílkoviny
4. ✅ Využity zásoby před expirací
5. ✅ Flexibilní varianta pro oběd v práci

---

## 📁 JAK POUŽÍT TYTO SOUBORY?

### Scénář 1: Chci rychlou odpověď
→ Čtěte **PAJA_DEN_2_RYCHLY_PREHLED.md**

### Scénář 2: Chci detailní plán
→ Čtěte **PAJA_DEN_2_DOPORUCENI.md**

### Scénář 3: Chci testovat vlastní varianty
→ Použijte **scripts/analyze_paja_meals.py**

---

## 🔗 Související soubory

- `day_2_2026-01-20_úterý.md` - Původní plánovaný jídelníček
- `SPOTŘEBA_ÚTERÝ_20_01.md` - Sledování spotřeby zásob
- `shopping_list.md` - Týdenní nákupní seznam
- `lednice/AKTUALNI_STAV.md` - Aktuální inventář

---

**Vytvořeno:** 20.01.2026  
**Autor:** GitHub Copilot Assistant  
**Účel:** Pomoc s plánováním jídelníčku pro Páju (Den 2)
