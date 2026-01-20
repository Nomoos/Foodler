# Strukturované tabulky pro plánování surovin

## Popis změny

Implementace požadavku: "Úprav plánování suroviny pro daný den budou vždy v dobře přehledně strukturované tabulce."

## Před změnou

Ingredience byly zobrazeny jako jednoduchý seznam:

```
🛒 HLAVNÍ INGREDIENCE
======================================================================
   ✓ brokolice
   ✓ cuketa
   ✓ kuřecí prsa
   ✓ vlašské ořechy
======================================================================
```

**Problémy:**
- Žádná kategorizace
- Obtížné vyhledávání specifického typu ingredience
- Méně přehledné pro delší seznamy

## Po změně

Ingredience jsou zobrazeny ve strukturované tabulce s kategoriemi:

```
🛒 HLAVNÍ INGREDIENCE
======================================================================

| Kategorie | Ingredience |
|-----------|-------------|
| **Zelenina** | brokolice |
| | cuketa |
| | papriky |
| | špenát |
| **Maso a Ryby** | hovězí maso |
| | kuřecí prsa |
| **Mléčné Produkty** | tvaroh |
| **Ořechy a Semínka** | chia |
| | mandle |
| | sezam |
| | vlašské ořechy |
| **Ostatní** | iso whey |
| | olivový olej |
| | protein |

======================================================================
```

**Výhody:**
- ✅ Jasná kategorizace podle typu potraviny
- ✅ Snadné vyhledávání konkrétního typu ingredience
- ✅ Přehledná struktura i pro delší seznamy
- ✅ Konzistentní formát pro denní i týdenní plánování
- ✅ Validní markdown tabulka

## Týdenní nákupní seznam

Pro týdenní plánování je navíc přidán sloupec s četností:

```
| Kategorie | Ingredience | Četnost |
|-----------|-------------|---------|
| **Zelenina** | Brokolice | 6× týdně |
| | Špenát | 3× týdně |
| **Maso a Ryby** | Tuňák v oleji | 2× týdně |
| | Kuřecí prsa | 1× týdně |
| **Mléčné Produkty** | Tvaroh | 10× týdně |
| | Sýr gouda | 3× týdně |
```

**Výhody četnosti:**
- Pomáhá odhadnout množství k nákupu
- Identifikuje nejčastěji používané ingredience
- Usnadňuje plánování meal prepu

## Testování

Změny byly otestovány na následujících datech:
- ✅ 20.01.2026 (úterý) - Den 20 z 28denního cyklu
- ✅ 21.01.2026 (středa) - Den 21 z 28denního cyklu
- ✅ 22.01.2026 (čtvrtek) - Den 22 z 28denního cyklu
- ✅ Týdenní plán 26.01-01.02.2026

## Bezpečnost

- ✅ CodeQL security check: 0 alertů
- ✅ Code review: 2 nitpick komentáře (akceptovatelné)

## Upravené soubory

1. `scripts/generate_meal_plan_date.py` - Denní plánování
2. `scripts/generate_weekly_meal_plan_md.py` - Týdenní plánování
3. `.gitignore` - Přidán testovací týden

## Použití

### Denní plán
```bash
python scripts/generate_meal_plan_date.py 2026-01-21
```

### Týdenní plán
```bash
python scripts/generate_weekly_meal_plan_md.py 2026-01-26
```

---

*Implementováno: 20.01.2026*
