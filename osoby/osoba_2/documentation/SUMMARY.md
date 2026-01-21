# 🎯 Dotazník pro Páju - Rychlý přehled

## ✅ Co bylo vytvořeno

### 1. Kompletní dotazník - 62 otázek
Rozděleno do 7 kategorií:
- 🏃 **Životní styl** (14 otázek) - práce, spánek, energie, stres
- ⏰ **Časové preference** (5 otázek) - meal prep, časy jídel
- 🍽️ **Jídelní preference** (9 otázek) - oblíbená jídla, recepty
- 🎯 **Zdravotní cíle** (12 otázek) - váha, energie, problémy
- 💰 **Praktická omezení** (12 otázek) - rozpočet, vybavení, rodina
- 🧘 **Emoční faktory** (9 otázek) - stres, nuda, podpora
- 📝 **Poznámky** (1 otázka) - speciální požadavky

### 2. Dva formáty dotazníku

#### A) Markdown verze (pro tisk)
📄 `osoby/osoba_2/DOTAZNIK_OTAZKY.md`
- Přehledný formát s checkboxy
- Můžeš vytisknout nebo vyplnit v editoru
- 10 stran, ~11 KB

#### B) Python interaktivní verze
💻 `osoby/osoba_2/dotaznik_paja.py`
- Průvodce vyplněním krok za krokem
- Automatická validace odpovědí
- **Generuje personalizovaná doporučení**
- Ukládá do JSON pro další použití
- ~23 KB, 600+ řádků

### 3. Dokumentace

📚 **Návod k použití**
- `osoby/osoba_2/README_DOTAZNIK.md` (4.6 KB)
- Jak používat oba formáty
- Jak často aktualizovat
- Co dělat s výsledky

📊 **Ukázka doporučení**
- `osoby/osoba_2/PRIKLAD_DOPORUCENI.md` (9.5 KB)
- Konkrétní příklad vyplněného dotazníku
- 9 kategorií personalizovaných doporučení
- Konkrétní recepty a meal prep plány
- Týdenní plán, nákupní seznam

🎬 **Demo script**
- `demo_dotaznik_paja.py` (7.3 KB)
- Spustitelný příklad použití
- Ukazuje všechny funkce systému

### 4. Integrace

✅ Aktualizován hlavní README (`osoby/README.md`)
- Přidána sekce o dotazníku
- Instrukce k použití
- Odkazy na všechny soubory

## 🚀 Jak použít

### Varianta 1: Rychlé seznámení
```bash
# Zobraz seznam všech otázek
python osoby/osoba_2/dotaznik_paja.py --seznam

# Spusť demo s ukázkou
python demo_dotaznik_paja.py
```

### Varianta 2: Vyplnění dotazníku

**Markdown (doporučeno pro první vyplnění):**
1. Otevři `osoby/osoba_2/DOTAZNIK_OTAZKY.md`
2. Projdi otázky a zaškrtni/vyplň odpovědi
3. Poznamenej si odpovědi

**Python (pro automatická doporučení):**
```bash
python osoby/osoba_2/dotaznik_paja.py
```
- Odpovídej na otázky
- Systém vygeneruje personalizovaná doporučení
- Odpovědi se uloží do JSON

### Varianta 3: Studium ukázky
1. Přečti si `PRIKLAD_DOPORUCENI.md`
2. Prohlédni si konkrétní recepty a plány
3. Inspiruj se pro vlastní jídelníček

## 📊 Co získáš vyplněním

### Okamžitá doporučení (9 kategorií):

1. **🌅 Ranní energie** - jak optimalizovat snídani podle energie
2. **🌙 Večerní hlad** - strategie pro největší hlad
3. **⏰ Meal prep** - plán podle dostupného času
4. **📝 Recepty** - jednoduché vs. složité podle preferencí
5. **🥗 Studená jídla** - využití meal prep krabiček
6. **📉 Úbytek váhy** - realistické cíle a makra
7. **⚡ Více energie** - nutrienty a suplementy
8. **🧘 Emoce** - strategie proti emočnímu stravování
9. **💰 Rozpočet** - optimalizace nákupů a výběr potravin

### Konkrétní výstupy:

- ✅ Personalizované denní makro rozložení
- ✅ Konkrétní recepty (3-5 ingrediencí)
- ✅ Meal prep plán (90 min v neděli = 4 dny jídel)
- ✅ Nákupní seznam podle rozpočtu a obchodů
- ✅ Týdenní jídelníček
- ✅ Strategie pro obtížné situace

## 📈 Příklad výstupu

### Ukázkové odpovědi
- Nízká energie ráno
- Největší hlad večer
- 20 min čas všední den, 90 min o víkendu
- Preferuje jednoduché recepty
- Rozpočet 700 Kč/týden
- Jí při nudě

### Vygenerovaná doporučení
```
🌅 Ranní jídlo: Vejce (3) + avokádo (50g) = 350 kcal, 25g protein
🌙 Večerní jídlo: Kuřecí (180g) + brokolice (200g) = 420 kcal, 55g protein
⏰ Meal prep: Neděle 90 min → 4 dny obědů + večeří připraveno
📝 Recepty: Kuřecí + brokolice + sýr (3 ingredience, 15 min)
💰 Nákup: Vejce 20ks (70 Kč), kuřecí 1kg (160 Kč), tvaroh 3x (90 Kč)
```

## 🔄 Aktualizace

Doporučujeme vyplnit dotazník znovu:
- **Po měsíci** - zkontrolovat změny
- **Když se změní situace** - nová práce, jiný režim
- **Při problému** - např. večerní hlad, únava
- **Pro fine-tuning** - jemné doladění

## 📞 Další kroky

1. ✅ **Vyplň dotazník** (15-20 minut)
2. ✅ **Přečti doporučení** - konkrétní tipy
3. ✅ **Vytvoř akční plán** - co změnit tento týden
4. ✅ **Uprav profil** - `profil.py` a `preference.py`
5. ✅ **Vygeneruj jídelníček** - použij meal planner

## 📁 Všechny soubory

```
Foodler/
├── osoby/osoba_2/
│   ├── DOTAZNIK_OTAZKY.md        # 62 otázek (markdown)
│   ├── dotaznik_paja.py          # Python dotazník
│   ├── README_DOTAZNIK.md        # Návod
│   ├── PRIKLAD_DOPORUCENI.md     # Ukázka výstupů
│   ├── profil.py                 # Současný profil
│   └── preference.py             # Současné preference
├── demo_dotaznik_paja.py         # Demo script
└── osoby/README.md               # Hlavní README (aktualizováno)
```

## 🎯 Shrnutí

**Vytvořeno:** Kompletní dotazníkový systém pro personalizaci jídelníčku Páji

**Otázky:** 62 otázek v 7 kategoriích

**Formáty:** 2 (markdown pro tisk, Python pro auto-doporučení)

**Výstupy:** Personalizovaná doporučení, recepty, meal prep plány, nákupní seznamy

**Čas vyplnění:** 15-20 minut

**Benefit:** Jídelníček přesně šitý na míru potřebám, preferencím a životnímu stylu

---

**Status:** ✅ Hotovo a otestováno  
**Datum:** 2026-01-18  
**Autor:** GitHub Copilot pro projekt Foodler
