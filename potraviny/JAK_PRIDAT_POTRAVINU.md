# Přidání nové potraviny

Pro přidání nové potraviny do databáze, vytvořte nový YAML soubor v adresáři `potraviny/soubory/`.

## Formát souboru

Název souboru by měl být tvořen z názvu potraviny (malými písmeny, mezery nahrazeny podtržítky), např. `fazole_cerná.yaml`.

### Příklad:

```yaml
nazev: Fazole černá
kategorie: luštěniny  # bilkoviny, zelenina, tuky, orechy, mlecne_vyrobky, lusteniny, atd.
kalorie: 132
bilkoviny: 8.9
sacharidy: 23.7
tuky: 0.5
vlaknina: 8.7
cena_za_kg: 45.0
sezona:
- '1'
- '2'
- '3'
- '4'
- '5'
- '6'
- '7'
- '8'
- '9'
- '10'
- '11'
- '12'
poznamky: Skvělý zdroj bílkovin a vlákniny, dostupné celoročně
```

## Povinná pole

- `nazev`: Název potraviny
- `kategorie`: Kategorie potraviny (bilkoviny, zelenina, tuky, orechy, mlecne_vyrobky, lusteniny, atd.)
- `kalorie`: Kalorie na 100g
- `bilkoviny`: Bílkoviny v gramech na 100g
- `sacharidy`: Sacharidy v gramech na 100g
- `tuky`: Tuky v gramech na 100g
- `vlaknina`: Vláknina v gramech na 100g

## Volitelná pole

- `cena_za_kg`: Průměrná cena za kilogram v Kč
- `sezona`: Seznam měsíců, kdy je potravina v sezóně (1-12)
- `poznamky`: Další poznámky k potravině

## Po přidání souboru

Po uložení nového YAML souboru bude potravina automaticky načtena při příštím spuštění aplikace. Není potřeba měnit žádný další kód.

## Výhody tohoto přístupu

- **Bez konfliktů**: Každý může přidat novou potravinu bez konfliktu s ostatními
- **Snadná údržba**: Každá potravina je samostatný soubor, lze snadno upravovat
- **Přehlednost**: YAML formát je čitelný pro lidi i stroje
- **Verzování**: Git efektivně sleduje změny v jednotlivých souborech

## Kategorie potravin

Běžně používané kategorie:
- `bilkoviny` - maso, ryby, vejce
- `zelenina` - všechna zelenina
- `tuky` - oleje, avokádo
- `orechy` - ořechy a semínka
- `mlecne_vyrobky` - mléko, sýry, jogurty
- `lusteniny` - fazole, čočka, cizrna
- `obiloviny` - rýže, ovesné vločky
- `ovoce` - všechno ovoce
