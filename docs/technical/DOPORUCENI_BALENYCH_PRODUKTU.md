# Doporučení balených mléčných produktů pro keto dietu

## 🎯 Účel

Skript `doporuc_balene_produkty.py` automaticky vyhledává a doporučuje balené mléčné výrobky (jogurty, tvarohy, sýry, smetanové produkty) v akci, které jsou vhodné pro ketogenní/nízkosacharidovou dietu podle požadavků Foodler dietního plánu.

## 📋 Co skript dělá

1. **Vyhledává produkty** v akci z českých supermarketů (Lidl, Kaufland, Albert, Penny, Billa, Tesco, Globus, Makro)
2. **Hodnotí vhodnost** podle ketogenní diety (nízký obsah sacharidů, vysoký obsah bílkovin/tuků)
3. **Filtruje nevhodné produkty** (sladké, s ovocem, s džemem)
4. **Řadí podle skóre vhodnosti** (0-100 bodů)
5. **Zobrazuje doporučení** s cenami, slevami a důvody vhodnosti

## 🚀 Použití

### Základní spuštění

```bash
python doporuc_balene_produkty.py
```

### Co se stane

1. Skript se připojí ke kupi.cz
2. Vyhledá produkty podle kategorií:
   - 🧀 **Tvarohy** - tučné, polotučné, přírodní
   - 🥛 **Jogurty** - řecké, bílé, přírodní
   - 🧀 **Sýry** - tvrdé, polotvrdé, přírodní
   - 🍶 **Smetanové produkty** - zakysaná smetana, mascarpone
3. Zobrazí top 10 produktů z každé kategorie
4. Vygeneruje shrnutí s top 5 doporučeními napříč kategoriemi

## 📊 Výstup

### Příklad výstupu

```
================================================================================
🎯 DOPORUČENÉ BALENÉ PRODUKTY PRO KETO/LOW-CARB DIETU
================================================================================

Tyto produkty jsou aktuálně v akci a jsou vhodné pro dietní plán:
  • Roman: max 70g sacharidů/den
  • Pája: max 60g sacharidů/den
  • Důraz na vysoký obsah bílkovin a zdravých tuků

🥛 Jogurty
================================================================================

1. Bílý jogurt řecký 0% Milko Vše140 g1000 g
   💰 Cena: 120.30 Kč
   🏪 Obchod: Různé obchody
   ⭐ Skóre vhodnosti: 90/100
   📋 Důvod: Obsahuje: řecký, bílý

[... další produkty ...]
```

### Shrnutí obsahuje

- **Celkový počet nalezených produktů** v akci
- **Top 5 doporučení** napříč všemi kategoriemi
- **Tipy pro výběr** jednotlivých kategorií produktů
- **Upozornění** na kontrolu nutričních hodnot

## 🎓 Hodnocení vhodnosti

### Skóre produktu (0-100)

Každý produkt dostává skóre podle následujících kritérií:

| Kritérium | Body | Popis |
|-----------|------|-------|
| Základní skóre | 50 | Všechny produkty začínají na 50 bodech |
| Vhodná klíčová slova | +15 za každé | "tučný", "plnotučný", "řecký", "přírodní", "nesladký" |
| Nevhodná klíčová slova | Vyřazení | "s džemem", "s ovocem", "vanilkový s cukrem" |
| Light/nízkotučný | -20 | Pravděpodobně více sacharidů |
| Vysoká sleva (≥30%) | +10 | Výhodný nákup |
| Dobrá sleva (≥20%) | +5 | Rozumná sleva |
| Priorita kategorie | +0 až +10 | Tvarohy a sýry mají vyšší prioritu |

### Prahová hodnota

- **≥60 bodů** = Produkt je **vhodný** pro keto dietu
- **<60 bodů** = Produkt není zobrazen (není dostatečně vhodný)

## 📦 Kategorie produktů

### 🧀 Tvarohy (Priorita: ⭐⭐⭐)

**Vhodné:**
- Tvaroh tučný
- Tvaroh polotučný
- Tvaroh přírodní
- Tvaroh s cibulkou/bylinkami

**Nevhodné:**
- Tvaroh s džemem
- Tvaroh s ovocem
- Tvaroh vanilkový (sladký)

**Max. sacharidy:** 5g na 100g

### 🥛 Jogurty (Priorita: ⭐⭐)

**Vhodné:**
- Řecký jogurt
- Bílý přírodní jogurt
- Celotučný jogurt
- Jogurt bez přidaného cukru

**Nevhodné:**
- Ovocné jogurty
- Jogurty s příchutí
- Sladké jogurty

**Max. sacharidy:** 6g na 100g

### 🧀 Sýry (Priorita: ⭐⭐⭐)

**Vhodné:**
- Tvrdé sýry (eidam, gouda, čedar)
- Polotvrdé sýry
- Přírodní zrající sýry
- Parmazán, ementál, mozzarella

**Nevhodné:**
- Tavené sýry
- Sýry s příchutí (uzené méně vhodné)

**Max. sacharidy:** 2g na 100g

### 🍶 Smetanové produkty (Priorita: ⭐)

**Vhodné:**
- Zakysaná smetana
- Smetana ke šlehání
- Mascarpone
- Plnotučná smetana

**Nevhodné:**
- Light smetana
- Nízkotučná smetana

**Max. sacharidy:** 5g na 100g

## 🔍 Klíčová slova pro vyhledávání

### Tvarohy
- `tvaroh`
- `tvaroh tučný`
- `cottage cheese`
- `tvaroh měkký`

### Jogurty
- `jogurt`
- `řecký jogurt`
- `bílý jogurt`
- `kysaný výrobek`
- `jogurt řecký`

### Sýry
- `sýr`
- `eidam`
- `gouda`
- `ementál`
- `čedar`
- `parmazán`
- `mozzarella`

### Smetanové produkty
- `zakysaná smetana`
- `smetana`
- `mascarpone`
- `smetanový sýr`

## 💡 Tipy pro použití

### 1. Pravidelné kontroly slev

```bash
# Spustit týdně pro aktuální nabídky
python doporuc_balene_produkty.py > nakup_tyden_$(date +%Y%m%d).txt
```

### 2. Kombinace s nutričními daty

```bash
# Získat nutriční data pro konkrétní produkt
python fetch_nutrition_data.py
# Zadejte název produktu z doporučení
```

### 3. Použití s komplexním asistentem

```bash
# Pro širší výběr všech keto produktů
python src/assistants/keto_shopping_assistant.py
```

## ⚠️ Důležité upozornění

**VŽDY si ověřte nutriční hodnoty na obalu produktu!**

Skript používá heuristiku založenou na názvu produktu a obecných znalostech o kategoriích. Skutečný obsah sacharidů se může lišit podle:
- Výrobce
- Konkrétní receptury
- Přidaných přísad

### Doporučený postup

1. ✅ Použijte skript pro nalezení produktů v akci
2. ✅ Vyberte produkty s vysokým skóre vhodnosti
3. ✅ **V obchodě zkontrolujte nutriční tabulku** na obalu
4. ✅ Ověřte obsah sacharidů, bílkovin a tuků
5. ✅ Kupte pouze produkty odpovídající vašim dietním cílům

## 🎯 Dietní cíle

### Roman (Romča)
- Denní cíl: **2001 kcal**, **140g+ bílkovin**, **max 70g sacharidů**
- Zaměření: Vysoký obsah bílkovin, nízké sacharidy

### Pája (Pavla)
- Denní cíl: **1508 kcal**, **92g bílkovin**, **max 60g sacharidů**
- Zaměření: Vysoký obsah bílkovin, nízké sacharidy

### Příklad denního příjmu z mléčných výrobků

**Snídaně:**
- 250g tučného tvarohu: ~20g bílkovin, ~3g sacharidů
- 150g řeckého jogurtu: ~15g bílkovin, ~5g sacharidů

**Svačina:**
- 50g tvrdého sýru: ~12g bílkovin, ~0.5g sacharidů

**Celkem:** ~47g bílkovin, ~8.5g sacharidů (jen z mléčných výrobků)

To představuje:
- **Roman:** 34% denních bílkovin, 12% denních sacharidů ✅
- **Pája:** 51% denních bílkovin, 14% denních sacharidů ✅

## 🛠️ Technické detaily

### Požadavky

```
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

### Instalace

```bash
pip install -r requirements.txt
```

### Architektura

```
doporuc_balene_produkty.py
├── DAIRY_CATEGORIES         # Definice kategorií a kritérií
├── evaluate_product_suitability()  # Hodnocení vhodnosti
├── search_dairy_products()  # Vyhledávání produktů
├── display_recommendations() # Zobrazení výsledků
└── generate_shopping_summary() # Shrnutí nákupu
```

### Použité moduly

- `src.scrapers.kupi_scraper` - Web scraping z kupi.cz
- `modely.product` - Datový model produktu

## 🔄 Rate Limiting

Skript respektuje etiku web scrapingu:
- **2 sekundy** zpoždění mezi požadavky
- **Realistické User-Agent** hlavičky
- **Respektování robots.txt** webu kupi.cz

## 📈 Výkonnost

- Průměrný čas: **60-90 sekund**
- Vyhledává: **4 kategorie** produktů
- Průměrný počet nalezených produktů: **200-300**
- Zobrazeno: **Top 10 z každé kategorie + Top 5 celkově**

## 🐛 Řešení problémů

### Problém: Žádné produkty nenalezeny

**Možné příčiny:**
1. Problémy s připojením k internetu
2. Web kupi.cz je nedostupný
3. Změna struktury webu

**Řešení:**
```bash
# Zkontrolujte připojení
ping www.kupi.cz

# Zkontrolujte, zda funguje základní scraper
python src/scrapers/kupi_scraper.py
```

### Problém: Nízké skóre vhodnosti

**Řešení:**
- Produkty s nízkým skóre (<60) nejsou vhodné pro keto dietu
- Upravte kritéria v sekci `DAIRY_CATEGORIES` v kódu
- Nebo použijte komplexní asistent pro širší výběr

### Problém: Chybějící ceny

**Vysvětlení:**
- Některé produkty mohou mít `0.00 Kč` - to znamená, že cena nebyla úspěšně extrahována z HTML
- Produkt je stále platný, ale cenu ověřte v obchodě

## 📚 Související dokumentace

- **[KUPI_INTEGRATION.md](KUPI_INTEGRATION.md)** - Integrace s Kupi.cz
- **[DISCOUNT_SCRAPING_GUIDE.md](DISCOUNT_SCRAPING_GUIDE.md)** - Komplexní stahování slev
- **[MEAL_PLANNER_GUIDE.md](MEAL_PLANNER_GUIDE.md)** - Plánovač jídelníčků
- **[PROTEIN_FIRST_PLAN.md](../diet-plans/PROTEIN_FIRST_PLAN.md)** - Dietní plán pro Romana
- **[PAJA_PROTEIN_PLAN.md](../diet-plans/PAJA_PROTEIN_PLAN.md)** - Dietní plán pro Páju

## 🤝 Příklady použití

### Příklad 1: Týdenní nákup

```bash
# Vygenerovat doporučení pro týdenní nákup
python doporuc_balene_produkty.py > doporuceni_$(date +%Y%m%d).txt

# Prohlédnout výsledky
cat doporuceni_$(date +%Y%m%d).txt
```

### Příklad 2: Konkrétní produkt

```python
# Ověření konkrétního produktu
from doporuc_balene_produkty import evaluate_product_suitability, DAIRY_CATEGORIES
from modely.product import Product

product = Product(
    name="Tvaroh tučný Jihočeský Madeta 250g",
    discount_price=31.46,
    discount_percentage=15,
    store="Kaufland",
    # ... další atributy
)

is_suitable, score, reason = evaluate_product_suitability(
    product, 
    DAIRY_CATEGORIES['tvarohy']
)

print(f"Vhodnost: {is_suitable}, Skóre: {score}/100, Důvod: {reason}")
```

### Příklad 3: Export do CSV

```python
# Export výsledků do CSV pro další analýzu
import csv
from src.scrapers.kupi_scraper import KupiCzScraper
from doporuc_balene_produkty import search_dairy_products

with KupiCzScraper() as scraper:
    results = search_dairy_products(scraper)
    
    with open('doporuceni.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Kategorie', 'Název', 'Cena', 'Sleva', 'Obchod', 'Skóre', 'Důvod'])
        
        for category_id, products in results.items():
            for product, score, reason in products[:10]:
                writer.writerow([
                    category_id,
                    product.name,
                    product.discount_price,
                    product.discount_percentage,
                    product.store,
                    score,
                    reason
                ])
```

## 🎓 Výhody tohoto přístupu

✅ **Úspora času** - Automatické vyhledávání namísto ruční kontroly letáků  
✅ **Úspora peněz** - Nalezení produktů v akci  
✅ **Dietní soulad** - Produkty odpovídají keto/low-carb požadavkům  
✅ **Objektivní hodnocení** - Skórovací systém založený na pravidlech  
✅ **Flexibilní** - Snadno rozšiřitelné o další kategorie

## 📝 Změnový log

### v1.0.0 (2026-01-18)
- ✨ První verze skriptu
- ✅ Podpora 4 kategorií produktů (tvarohy, jogurty, sýry, smetanové produkty)
- ✅ Skórovací systém 0-100 bodů
- ✅ Filtrování nevhodných produktů
- ✅ Top doporučení napříč kategoriemi
- ✅ Tipy pro výběr produktů
- ✅ Respektování rate limitingu

## 🔮 Plánované funkce

- [ ] Export do PDF nákupního seznamu
- [ ] Automatické načítání nutričních dat z kaloricketabulky.cz
- [ ] Emailové notifikace o nových slevách
- [ ] Možnost uložení oblíbených produktů
- [ ] Historie cen pro trend analýzu
- [ ] Lokační filtry (jen obchody ve Valašském Meziříčí)
