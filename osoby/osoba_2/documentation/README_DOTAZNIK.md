# 📋 Dotazník pro Páju - Návod k použití

Tento adresář obsahuje personalizovaný dotazník pro lepší přizpůsobení jídelníčku Páji.

## 📁 Soubory

### 1. `DOTAZNIK_OTAZKY.md` ⭐ ZAČNI TADY
**Kompletní seznam 62 otázek** v přehledném markdown formátu.

- ✅ **Nejlepší pro vyplnění rukou** - vytiskni nebo otevři v editoru
- ✅ **Přehledné kategorie** - životní styl, časy, preference, cíle, praktické věci
- ✅ **Checkboxy** - snadno vyber odpovědi
- ✅ **Můžeš sdílet** - pošli Páji k vyplnění

### 2. `dotaznik_paja.py`
**Interaktivní Python verze** dotazníku.

Obsahuje:
- Automatické vyplnění s průvodcem
- Validaci odpovědí
- Uložení do JSON souboru
- **Generování personalizovaných doporučení** na základě odpovědí

## 🚀 Jak použít

### Varianta A: Markdown dotazník (doporučeno)

1. Otevři soubor `DOTAZNIK_OTAZKY.md`
2. Vyplň odpovědi (můžeš upravit přímo v souboru nebo vytisknout)
3. Ulož poznámky

### Varianta B: Interaktivní Python dotazník

```bash
# Základní použití - interaktivní vyplnění
python osoby/osoba_2/dotaznik_paja.py

# Zobrazit pouze seznam otázek
python osoby/osoba_2/dotaznik_paja.py --seznam
```

Po vyplnění dostaneš:
- ✅ Personalizovaná doporučení
- ✅ Uložené odpovědi v JSON formátu
- ✅ Konkrétní tipy na meal planning

### Varianta C: Kombinace obou

1. Nejprve si projdi otázky v `DOTAZNIK_OTAZKY.md`
2. Rozmysli si odpovědi
3. Spusť Python verzi pro automatické doporučení

## 📊 Kategorie otázek

### 1️⃣ Životní styl a denní rutina (14 otázek)
- Pracovní režim
- Spánek a energie
- Hlad během dne
- Stres a trávení

### 2️⃣ Časové preference (5 otázek)
- Čas na meal prep
- Preferované časy jídel
- Víkend vs. všední den

### 3️⃣ Jídelní preference (9 otázek)
- TOP oblíbená jídla
- Jídla, která chceš častěji
- Studená vs. teplá jídla
- Jednoduché vs. složité recepty

### 4️⃣ Zdravotní cíle (12 otázek)
- Hlavní cíle (váha, energie, trávení...)
- Váhové cíle (1/3/6 měsíců)
- Problémové oblasti
- Zdravotní problémy
- Menstruační cyklus

### 5️⃣ Praktická omezení (12 otázek)
- Rozpočet na potraviny
- Nákupní návyky a obchody
- Kuchyňské vybavení
- Skladovací prostor
- Rodinná situace

### 6️⃣ Emoční stravování (9 otázek)
- Spouštěče přejídání (stres, nuda)
- Strategie zvládání
- Obtížné situace
- Podpora rodiny

### 7️⃣ Další poznámky (1 otázka)
- Jakékoli speciální požadavky

## 🎯 Co získáš vyplněním?

### Okamžitá doporučení:
- 🌅 Optimální složení snídaně podle energie
- 🌙 Strategie pro večerní hlad
- ⏰ Meal prep plán podle času
- 📝 Recepty podle preferencí
- 💰 Nákupní optimalizace podle rozpočtu
- 🧘 Řešení emočního stravování

### Dlouhodobě:
- 📋 Jídelníček šitý na míru
- 🛒 Personalizované nákupní seznamy
- 📅 Týdenní meal prep plány
- 📊 Sledování pokroku směrem k cílům

## 💡 Příklad použití

```python
# Spusť interaktivní dotazník
python osoby/osoba_2/dotaznik_paja.py

# Příklad výstupu:
"""
📋 DOPORUČENÍ NA ZÁKLADĚ TVÝCH ODPOVĚDÍ:
1. 🌙 Večerní hlad: Naplánuj větší večeři s 30-35g bílkovin pro sytost
2. ⏰ Meal prep: Víkendový meal prep pro 3-4 dny dopředu
3. 📝 Jednoduché recepty: Zaměř se na recepty do 5 ingrediencí
4. 📉 Úbytek váhy: Udržuj 1508 kcal, 90g+ bílkovin, <60g sacharidů
5. 💰 Rozpočet: Využij slevy z Kupi.cz, vejce a tvaroh jsou cenově výhodné
"""
```

## 🔄 Aktualizace

Dotazník můžeš vyplnit znovu:
- **Po měsíci** - zkontroluj změny v preferencích
- **Když se změní situace** - nová práce, jiný režim
- **Když narazíš na problém** - např. večerní hlad, únava
- **Pro fine-tuning** - jemné doladění jídelníčku

## 📞 Další kroky

Po vyplnění dotazníku:

1. **Ulož odpovědi** - do JSON nebo poznámek
2. **Přečti si doporučení** - konkrétní tipy
3. **Vytvoř akční plán** - co změnit tento týden
4. **Uprav profil** - aktualizuj `profil.py` a `preference.py`
5. **Vygeneruj jídelníček** - použij meal planner s novými preferencemi

---

## 📚 Související soubory

- `profil.py` - Základní antropometrické údaje a cíle
- `preference.py` - Aktuální preference jídel a omezení
- `../README.md` - Obecný návod k profilům

---

**Vytvořeno:** 2026-01-18  
**Počet otázek:** 62  
**Čas vyplnění:** 15-20 minut  
**Platnost:** Doporučujeme aktualizovat každý měsíc
