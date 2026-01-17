# Foodler - 28denní Jídelníček

Kompletní jídelní plán na 28 dní pro podporu hubnutí s důrazem na vyváženou stravu.

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

## Další informace

Pro více informací o dietních cílech a makronutrientech viz soubor `purpose`.

## Licence

Tento jídelníček je poskytován jako je, pro osobní použití.
