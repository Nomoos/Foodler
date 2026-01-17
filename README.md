# Foodler - 28denní Jídelníček (Mačingovka)

Kompletní jídelní plán na 28 dní pro podporu hubnutí s důrazem na vyváženou stravu.

**Tento jídelníček vychází z diety Antonie Mačingové**, známé jako **"Mačingovka"** - osvědčeného dietního systému zaměřeného na zdravé hubnutí pomocí přirozených potravin.

## Přehled

Tento repozitář obsahuje podrobný 28denní jídelníček s pěti jídly denně:
- **Raňajky** (Snídaně)
- **Desiata** (Dopolední svačina)
- **Obed** (Oběd)
- **Olovrant** (Odpolední svačina)
- **Večera** (Večeře)

## Dostupné formáty

Jídelníček je dostupný ve dvou formátech:

### 1. CSV formát
Soubor: `meal_plan_28_days.csv`

Standardní CSV soubor s čárkovým oddělovačem, kde jednotlivé ingredience v jídle jsou odděleny středníkem. Ideální pro import do tabulkových procesorů (Excel, Google Sheets, LibreOffice Calc).

**Struktura:**
```
Deň,Raňajky,Desiata,Obed,Olovrant,Večera
1,Mrkev; jablko; med; rozinky; vlašské ořechy,Ananas,...
```

### 2. JSON formát
Soubor: `meal_plan_28_days.json`

Strukturovaný JSON soubor s kompletními daty o jídelníčku. Ideální pro programové zpracování a integraci s aplikacemi.

**Struktura:**
```json
{
  "meal_plan": {
    "title": "28-denní jídelníček",
    "description": "Kompletní jídelní plán na 28 dní s 5 jídly denně",
    "days": [
      {
        "day": 1,
        "breakfast": "...",
        "morning_snack": "...",
        "lunch": "...",
        "afternoon_snack": "...",
        "dinner": "..."
      }
    ]
  }
}
```

## Charakteristika jídelníčku

### Hlavní ingredience a jejich frekvence

**Nejčastější snídaně:**
- Mrkev, jablko, med, rozinky, vlašské ořechy (16x)
- Bílý jogurt, vlašské ořechy, med, skořice (4x)
- Vařené jáhly, vlašské ořechy, sušené švestky, med (4x)
- Kiwi, banán, mandle, med, skořice (2x)
- Pohankové vločky, sójové mléko, jablko, vlašské ořechy, med (2x)

**Populární hlavní jídla:**
- Mrkvový perkelt se strouhaným sýrem (6x)
- Brokolice s česnekem (různé varianty)
- Cuketové placky
- Fazolové lusky s česnekem
- Salát z červené řepy (různé varianty)

**Vegetariánské alternativy:**
- Téměř všechna hlavní jídla s masem mají vegetariánskou variantu
- Běžné náhrady: tempeh, tofu, vejce, brokolicové karbanátky

### Nutriční principy

Jídelníček je navržen s důrazem na:
- Vysoký obsah bílkovin (ořechy, vejce, sýry, jogurt, luštěniny)
- Pravidelný příjem vlákniny (zelenina, ovoce, luštěniny)
- Zdravé tuky (ořechy, mandle, med)
- Rozmanitost zeleniny a ovoce
- Možnost vegetariánské varianty

## Použití

### Import do tabulkového procesoru

**Excel / Google Sheets:**
1. Otevřete soubor `meal_plan_28_days.csv`
2. Sloupec "Deň" obsahuje číslo dne (1-28)
3. Každý následující sloupec obsahuje jedno z pěti jídel

**LibreOffice Calc:**
1. Soubor → Otevřít
2. Vyberte `meal_plan_28_days.csv`
3. V dialogu importu nastavte:
   - Kódování: UTF-8
   - Oddělovač: čárka
   - Text delimiter: uvozovky

### Programové zpracování (JSON)

```python
import json

with open('meal_plan_28_days.json', 'r', encoding='utf-8') as f:
    meal_plan = json.load(f)

# Získání jídel pro konkrétní den
day_5 = meal_plan['meal_plan']['days'][4]  # Den 5 (index 4)
print(f"Snídaně: {day_5['breakfast']}")
print(f"Oběd: {day_5['lunch']}")
```

```javascript
const fs = require('fs');

const mealPlan = JSON.parse(
  fs.readFileSync('meal_plan_28_days.json', 'utf-8')
);

// Zobrazení všech snídaní
mealPlan.meal_plan.days.forEach(day => {
  console.log(`Den ${day.day}: ${day.breakfast}`);
});
```

### Použití ukázkového skriptu

V repozitáři je k dispozici Python skript `example_usage.py`, který ukazuje různé způsoby práce s jídelníčkem:

```bash
python3 example_usage.py
```

Skript obsahuje příklady:
- Zobrazení menu pro konkrétní den
- Zobrazení menu na celý týden
- Vyhledávání jídel podle ingredience
- Automatické určení aktuálního dne v cyklu
- Statistiky o jídelníčku

## Poznámky

- Jídelníček je navržen jako flexibilní plán - lze přizpůsobit individuálním potřebám
- Některá jídla se opakují, což usnadňuje nákup a přípravu
- Každý den obsahuje 5 jídel pro optimální rozložení příjmu energie během dne
- Všechna data jsou v UTF-8 kódování pro správné zobrazení českých znaků

## Cílová skupina

Tento jídelníček je určen pro:
- Osoby, které chtějí hubnout zdravým způsobem
- Rodiny hledající vyváženou stravu
- Kohokoliv, kdo hledá inspiraci pro pestrou a zdravou kuchyni

## Další dokumentace

### 📚 Podrobné průvodce:
- **[MACINGOVA_DIETA.md](MACINGOVA_DIETA.md)** - Podrobné informace o dietě Antonie Mačingové
  - Všechna jídla a jejich varianty
  - Principy Mačingovky
  - Nákupní seznamy
  - Tipy na přípravu

- **[RECEPTY_SALATY.md](RECEPTY_SALATY.md)** - Kompletní recepty na saláty z jídelníčku
  - 9 detailních receptů s ingrediencemi
  - Makronutrienty pro každý salát
  - Vegetariánské varianty
  - Tipy na zálivky a dresinky

- **[purpose](purpose)** - Původní dietní cíle a makronutrienty

## Inspirace a použití

Tento jídelníček lze použít jako:
- **Kompletní plán** - následovat celých 28 dní po cyklu
- **Zdroj inspirace** - vybrat si oblíbená jídla a kombinovat je
- **Databáze receptů** - zvláště saláty jsou vhodné pro různé příležitosti
- **Šablona** - upravit podle vlastních preferencí a alergií

Zvláště se doporučuje inspirovat se **saláty**, které jsou pilířem Mačingovky.

## Licence

Tento jídelníček je poskytován jako je, pro osobní použití.
