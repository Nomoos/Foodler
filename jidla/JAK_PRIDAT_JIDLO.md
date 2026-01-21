# Přidání nového jídla

Pro přidání nového jídla do databáze, vytvořte nový YAML soubor v příslušné kategorii v adresáři `jidla/soubory/`.

## Kategorie

Recepty jsou organizovány do následujících podadresářů:

- **polevky/** - Polévky
- **salaty/** - Saláty a studená jídla
- **hlavni_jidla/** - Hlavní jídla (maso, ryby)
- **prilohy/** - Přílohy
- **snidane/** - Snídaně
- **svaciny/** - Svačiny a lehké pokrmy

Vyberte kategorii, do které vaše jídlo patří, a vytvořte tam nový YAML soubor.

## Formát souboru

Název souboru by měl být tvořen z názvu jídla (malými písmeny, mezery nahrazeny podtržítky), např. `grilované_kure_s_ryzí.yaml`.

Uložte soubor do příslušného podadresáře, např. `jidla/soubory/hlavni_jidla/grilované_kure_s_ryzí.yaml`.

### Příklad:

```yaml
nazev: Grilované kuře s rýží
typ: obed  # snidane, obed, vecere, svacina
ingredience:
- nazev: Kuřecí prsa
  mnozstvi_g: 200
  kategorie: hlavni
- nazev: Rýže bílá
  mnozstvi_g: 100
  kategorie: priloha
- nazev: Olivový olej
  mnozstvi_g: 10
  kategorie: omacka
kalorie_celkem: 500
bilkoviny_celkem: 45.0
sacharidy_celkem: 55.0
tuky_celkem: 12.0
vlaknina_celkem: 2.0
priprava_cas_min: 30
priprava_postup: |
  1. Kuřecí prsa nakrájet a osolit.
  2. Opéct na grilu 15 minut.
  3. Rýži uvařit podle návodu.
obtiznost: snadna  # snadna, stredni, narocna
porce: 1
vhodne_pro_meal_prep: true
vydrzi_dni: 3
poznamky: Ideální pro meal prep na celý týden
```

## Povinná pole

- `nazev`: Název jídla
- `typ`: Typ jídla (snidane, obed, vecere, svacina)
- `ingredience`: Seznam ingrediencí (každá má nazev, mnozstvi_g, kategorie)
- `kalorie_celkem`: Celkový počet kalorií
- `bilkoviny_celkem`: Celkové množství bílkovin v gramech
- `sacharidy_celkem`: Celkové množství sacharidů v gramech
- `tuky_celkem`: Celkové množství tuků v gramech
- `vlaknina_celkem`: Celkové množství vlákniny v gramech
- `priprava_cas_min`: Čas přípravy v minutách
- `priprava_postup`: Postup přípravy
- `obtiznost`: Obtížnost přípravy (snadna, stredni, narocna)

## Volitelná pole

- `porce`: Počet porcí (výchozí: 1)
- `vhodne_pro_meal_prep`: true/false (výchozí: false)
- `vydrzi_dni`: Počet dní, které jídlo vydrží v lednici
- `poznamky`: Další poznámky k jídlu

## Po přidání souboru

Po uložení nového YAML souboru bude jídlo automaticky načteno při příštím spuštění aplikace. Není potřeba měnit žádný další kód.

## Výhody tohoto přístupu

- **Bez konfliktů**: Každý může přidat nové jídlo bez konfliktu s ostatními
- **Snadná údržba**: Každé jídlo je samostatný soubor, lze snadno upravovat
- **Přehlednost**: YAML formát je čitelný pro lidi i stroje
- **Verzování**: Git efektivně sleduje změny v jednotlivých souborech
