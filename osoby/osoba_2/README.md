# 👤 Osoba 2 - Pája (Pavla)

Osobní adresář s profily, jídelními plány a kalkulacemi pro Páju.

## 📁 Struktura Adresáře

### `profil/` - Profilové Soubory
Obsahuje osobní profil, preference a komplexní nastavení.

**Soubory:**
- `profil.py` - Základní profil (váha, výška, cíle)
- `profil_komplexni.py` - Rozšířený profil s detailními údaji
- `preference.py` - Jídelní preference a omezení

**Použití:**
```python
from osoby.osoba_2.profil.profil import PajaProfil

profil = PajaProfil()
print(f"Denní cíl: {profil.denny_cil_kcal} kcal")
print(f"Bílkoviny: {profil.denny_cil_bilkoviny}g")
```

### `meal_plans/` - Jídelníčky
Osobní denní jídelníčky v různých formátech.

**Formáty:**
- **Minimální** - Stručný přehled (pouze jídla a makra)
- **Osobní** - Detailní s poznámkami a tipy
- **Rychlý přehled** - Ultra-kompaktní přehled

**Příklad:**
- `meal_plan_day_3_minimalni.md` - Stručný plán pro den 3
- `meal_plan_day_3_osobni.md` - Detailní plán s tipy
- `meal_plan_day_3_rychly_prehled.md` - Rychlý přehled

### `calculators/` - Kalkulačky
Python skripty pro výpočty makroživin a plánování.

**Soubory:**
- `kalkulacka_den_3.py` - Kalkulace pro konkrétní den
- `kalkulacka_minimalni.py` - Minimalistická kalkulace

**Použití:**
```python
from osoby.osoba_2.calculators.kalkulacka_minimalni import vypocitej_makra

makra = vypocitej_makra(jidla_seznam)
print(f"Celkem: {makra['kalorie']} kcal, {makra['bilkoviny']}g bílkovin")
```

### `shopping_lists/` - Nákupní Seznamy
Nákupní seznamy vygenerované z jídelníčků.

**Soubory:**
- `nakupni_seznam_den_3.md` - Nákup pro den 3
- `nakupni_seznam_minimalni.md` - Minimální nákup

**Formát:**
```markdown
## 🛒 Nákupní Seznam

### Bilkoviny
- [ ] Kuřecí prsa - 500g
- [ ] Vejce - 10 ks

### Zelenina
- [ ] Brokolice - 300g
```

### `documentation/` - Dokumentace
README soubory, návody, dotazníky a souhrny.

**Obsah:**
- `README_DEN_3.md` - Dokumentace plánu pro den 3
- `README_DOTAZNIK.md` - Návod k dotazníku
- `DOTAZNIK_OTAZKY.md` - Seznam otázek dotazníku
- `DOPLNUJICI_OTAZKY.md` - Doplňující dotazník
- `SUMMARY.md` - Celkový souhrn
- `MODULARNI_SYSTEM.md` - Dokumentace modulárního systému
- `PRIKLAD_DOPORUCENI.md` - Příklady doporučení

## 🎯 Profil Páji

**Základní údaje:**
- Váha: 77.3 kg
- Výška: 169 cm
- Věk: ~35 let

**Dietní cíle:**
- 🔥 Denní cíl: **1508 kcal**
- 💪 Bílkoviny: **92g+**
- 🍞 Sacharidy: **max 60g** (keto/low-carb)
- 🥑 Tuky: zbytek kalórií

**Dietní přístup:**
- **Keto/Low-carb** - Minimalizace sacharidů
- **Protein-first** - Priorita bílkovin
- **Healthy fats** - Kvalitní zdroje tuků

## 📊 Aktuální Stav

**Plány:**
- ✅ Den 3 - 3 varianty (minimální, osobní, rychlý)
- ✅ Rychlý přehled (minimální verze)

**Kalkulace:**
- ✅ Kalkulačka den 3
- ✅ Minimální kalkulačka

**Nákup:**
- ✅ Seznam pro den 3
- ✅ Minimální seznam

## 🔧 Použití

### Generování Nového Plánu
```bash
# Použijte generátor osobního plánu
python scripts/generate_personal_meal_plan.py --osoba paja --den 4
```

### Spuštění Kalkulačky
```bash
# Spusťte kalkulačku pro výpočet maker
python osoby/osoba_2/calculators/kalkulacka_minimalni.py
```

### Vytvoření Nákupního Seznamu
```bash
# Vygenerujte nákup z jídelníčku
python scripts/generate_shopping_list.py --meal-plan osoby/osoba_2/meal_plans/meal_plan_day_3_minimalni.md
```

## 🔗 Související Soubory

- `/data/meal_plans/` - Obecné jídelní plány pro celou rodinu
- `/lednice/AKTUALNI_STAV.md` - Co máme doma
- `/docs/diet-plans/` - Dokumentace dietních plánů

## 💡 Tipy

- Prioritně konzumujte potraviny s brzy expirujícím datem (viz `/lednice/AKTUALNI_STAV.md`)
- Používejte kalkulačky pro kontrolu denního příjmu makroživin
- Nákupní seznamy generujte z jídelníčků pro minimalizaci plýtvání

---

*Aktualizováno: 21.01.2026*
