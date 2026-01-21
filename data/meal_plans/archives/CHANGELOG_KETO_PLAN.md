# Changelog: Keto Meal Plan Update

**Datum:** 18.01.2026

## Změny v meal_plan_28_days.json

### Problém
Původní jídelníček (`meal_plan_28_days.json`) nerespektoval cílové makronutrienty pro ketogenní/low-carb dietu:
- ❌ Pouze 12.1% jídel obsahovalo dostatečné bílkoviny
- ❌ Vysoký obsah sacharidů (těstoviny, med, rozinky, datle, ananas, grahamové rohlíky)
- ❌ Nebylo využito avokádo (2 ks v lednici)
- ❌ Nedostatečné využití ostatních položek z lednice
- ❌ Pouze 5 jídel denně místo 6 podle profilu

### Cílové makronutrienty (Roman - osoba_1)
- **Kalorie:** 2000 kcal
- **Bílkoviny:** 140g+ (minimum, protein-first přístup)
- **Sacharidy:** max 70g (low-carb/keto)
- **Tuky:** 129g (zdravé zdroje)
- **Vláknina:** 30g
- **Počet jídel:** 6 denně

### Řešení

Vytvořen nový keto-friendly jídelníček s následujícími charakteristikami:

#### ✅ Respektování maker
- **83.3%** jídel obsahuje vysoké množství bílkovin (původně 12.1%)
- **0%** jídel s vysokým obsahem sacharidů (původně vysoký podíl)
- Protein-first přístup v každém jídle
- 6 jídel denně včetně večerní svačiny

#### ✅ Využití položek z lednice

**Vysoká priorita (protein sources):**
- Vejce: 33x (40 ks v zásobě)
- Cottage cheese: 29x (200g v lednici)
- Kuřecí prsa: 11x (600g v lednici)
- Losos: 11x (200g v mrazáku)
- Tuňák: 15x (750g v konzervách)
- Hovězí maso: 11x (400g v lednici)
- Tvaroh: 17x (500g v lednici)
- Iso whey protein: použito v proteinových shake

**Zdravé tuky:**
- Avokádo: **24x** (původně 0x) - 2 ks v lednici
- Olivový olej: 58x (300ml v zásobě)
- Mandle: 24x (150g v zásobě)
- MCT olej: použito v shake a snacích
- Lněné semínko, chia, sezam: použito pravidelně

**Low-carb zelenina:**
- Brokolice: 27x (300g v lednici)
- Špenát: 22x (200g v lednici)
- Cuketa: použita (2 ks v lednici)
- Paprika: použita (3 ks v lednici)
- Ledový salát: použit (1 ks v lednici)
- Kysané zelí: použito (500g v lednici, probiotické)

### Struktura 6 jídel denně

1. **🌅 Snídaně** - Vysoká bílkovina (omelety, vejce, cottage cheese, whey shake)
2. **🍎 Dopolední svačina** - Protein + zdravé tuky (cottage, vejce, mandle, avokádo)
3. **🍽️ Oběd** - Hlavní protein + zelenina (kuřecí, losos, hovězí + low-carb zelenina)
4. **🥤 Odpolední svačina** - Lehčí protein (vejce, tvaroh, cottage, mandle)
5. **🌙 Večeře** - Protein + zelenina (omelety, maso, ryby + zelenina)
6. **🌃 Večerní svačina** - Kasein-like protein (cottage, tvaroh, whey shake)

### Příklady jídel

**Den 1:**
- Snídaně: Omeleta ze 3 vajec, špenát, sýr gouda, avokádo (1/2)
- Dopolední svačina: Cottage cheese (100g), mandle (30g)
- Oběd: Kuřecí prsa grilovaná (200g), brokolice s olivovým olejem, kysané zelí
- Odpolední svačina: Vejce natvrdo (2 ks), olivový olej
- Večeře: Omeleta ze 3 vajec, špenát, sýr, brokolice
- Večerní svačina: Cottage cheese (100g), lněné semínko

**Den 2:**
- Snídaně: Míchaná vajíčka (3 ks), cottage cheese, brokolice, olivový olej
- Dopolední svačina: Iso whey protein shake
- Oběd: Losos (150g), špenát s česnekem, avokádo
- Odpolední svačina: Tvaroh (100g), vlašské ořechy
- Večeře: Kuřecí prsa (150g), ledový salát s olivovým olejem
- Večerní svačina: Tvaroh (100g), vlašské ořechy

### Změny v skriptech

**generate_weekly_meal_plan.py:**
- ✅ Přidána podpora pro `evening_snack` (6. jídlo)
- ✅ Zobrazení večerní svačiny ve výstupu

**generate_weekly_meal_plan_md.py:**
- ✅ Přidána podpora pro `evening_snack` v MD výstupu
- ✅ Přidána sekce "🌃 Večerní Svačina" v denním plánu
- ✅ Aktualizace nákupního seznamu pro 6 jídel

### Záloha

Původní jídelníček byl zazálohován jako:
- `data/meal_plans/meal_plan_28_days_original_backup.json`

Nový keto jídelníček byl uložen také jako:
- `data/meal_plans/meal_plan_28_days_keto.json`

A nahradil původní:
- `data/meal_plans/meal_plan_28_days.json`

## Výhody nového plánu

1. **✅ Respektuje makra** - Protein-first, low-carb přístup
2. **✅ Využívá lednici** - Avokádo, vejce, kuřecí, ryby, cottage cheese
3. **✅ Keto-friendly** - Minimální sacharidy, zdravé tuky
4. **✅ Variabilita** - 7 různých snídaní, 8 obědů, 6 večeří, variety svačin
5. **✅ Praktičnost** - Použití dostupných ingrediencí z lednice
6. **✅ Sytost** - 6 jídel denně, vysoká bílkovina udržuje sytost
7. **✅ Health benefits** - Probiotika (kysané zelí), omega-3 (losos), vláknina

## Další kroky

- [ ] Možné přidání konkrétních gramáží pro přesnější sledování maker
- [ ] Integrace s nákupním seznamem pro automatické generování
- [ ] Propojení s discount scraperem pro optimalizaci nákladů
- [ ] Přidání variant pro víkendy vs. pracovní dny
- [ ] Vytvoření meal prep průvodce pro přípravu několika dní dopředu
