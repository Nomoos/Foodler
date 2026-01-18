# 🔄 Integrace dat z Kupi.cz a Kalorických tabulek

## 📋 Přehled

Systém má již implementované scrapery pro stahování dat z:
1. **Kupi.cz** - Aktuální slevy ze všech obchodů (Lidl, Kaufland, Albert, Penny, Globus, atd.)
2. **Kaloricketabulky.cz** - Nutriční data pro potraviny

## 🚀 Jak stáhnout data

### 1. Slevy z Kupi.cz

**Existující skript**: `scrape_and_save_discounts.py`

#### Použití:

```bash
# Stáhnout všechny aktuální slevy ze všech obchodů
python scrape_and_save_discounts.py
```

**Co se stane**:
- ✅ Stáhne slevy ze všech obchodů (Lidl, Kaufland, Albert, Penny, Billa, Tesco, Globus, Makro)
- ✅ Extrahuje data platnosti slev
- ✅ Uloží do JSON souboru s timestampem
- ✅ Zobrazí statistiky (kolik produktů z jakého obchodu)

**Výstup**: `data/discounts/discounts_YYYYMMDD_HHMMSS.json`

**Příklad struktury dat**:
```json
{
  "lidl": [
    {
      "name": "Kuřecí prsa",
      "original_price": 150.0,
      "discount_price": 99.90,
      "discount_percentage": 33.4,
      "store": "Lidl",
      "valid_from": "2026-01-20",
      "valid_until": "2026-01-26",
      "image_url": "https://...",
      "product_url": "https://...",
      "category": "Maso"
    }
  ]
}
```

#### Automatizace (doporučeno):

**Každou sobotu ráno** - Před nákupem:

```bash
# Vytvořit cron job (Linux/Mac)
crontab -e

# Přidat řádek (každou sobotu v 8:00)
0 8 * * 6 cd /path/to/Foodler && python scrape_and_save_discounts.py
```

**Windows Task Scheduler**:
- Vytvořit novou úlohu
- Trigger: Každou sobotu v 8:00
- Action: `python C:\path\to\Foodler\scrape_and_save_discounts.py`

---

### 2. Nutriční data z Kaloricketabulky.cz

**Existující skript**: `fetch_nutrition_data.py`

#### Použití:

```bash
# Vyhledat produkt a získat nutriční data
python fetch_nutrition_data.py "Kuřecí prsa"

# Nebo v Python kódu:
from fetch_nutrition_data import fetch_by_product_name

data = fetch_by_product_name("Tvaroh tučný")
print(data)
```

**Příklad výstupu**:
```python
{
    "product_name": "Tvaroh tučný",
    "url": "https://www.kaloricketabulky.cz/...",
    "macros": {
        "calories": "180 kcal",
        "protein": "15 g",
        "carbohydrates": "3 g",
        "fat": "12 g",
        "fiber": "0 g",
        "sugar": "3 g"
    }
}
```

---

## 🔗 Integrace do hlavního systému

### Krok 1: Rozšířit `zpracuj_dotazniky_a_vytvor_plan.py`

Přidáme nový krok pro stahování aktuálních dat:

```python
def stahnout_aktualni_data(self):
    """Stáhne aktuální slevy a nutriční data."""
    print("=" * 80)
    print("📥 KROK 8: Stahování aktuálních dat")
    print("=" * 80)
    print()
    
    # 1. Stáhnout slevy z Kupi.cz
    print("🛒 Stahuji slevy z Kupi.cz...")
    try:
        from src.scrapers.kupi_scraper import KupiCzScraper
        
        with KupiCzScraper() as scraper:
            # Stáhnout slevy relevantní pro nákup
            stores = ['lidl', 'kaufland', 'albert', 'penny', 'globus']
            discounts = {}
            
            for store in stores:
                print(f"  • {store.capitalize()}...", end=" ")
                products = scraper.get_current_discounts(store=store)
                discounts[store] = products
                print(f"✓ ({len(products)} produktů)")
        
        print()
        print("✅ Slevy staženy úspěšně!")
        print(f"   Celkem: {sum(len(p) for p in discounts.values())} produktů v akci")
        print()
        
        # Filtrovat relevantn í produkty pro keto/low-carb
        relevantni_produkty = self._filtruj_keto_produkty(discounts)
        
        print("🥩 TOP 10 SLEV pro keto/low-carb:")
        for i, produkt in enumerate(relevantni_produkty[:10], 1):
            print(f"   {i}. {produkt.name}")
            print(f"      {produkt.discount_price} Kč (-{produkt.discount_percentage}%) @ {produkt.store}")
        print()
        
    except Exception as e:
        print(f"❌ Chyba při stahování slev: {e}")
        print("   Pokračuji bez aktuálních slev...")
    
    # 2. Získat nutriční data pro hlavní ingredience
    print("📊 Aktualizuji nutriční data...")
    try:
        from fetch_nutrition_data import fetch_by_product_name
        
        hlavni_ingredience = [
            "Kuřecí prsa",
            "Mleté maso",
            "Losos",
            "Vejce",
            "Tvaroh",
            "Řecký jogurt"
        ]
        
        nutricni_data = {}
        for ingredience in hlavni_ingredience:
            print(f"  • {ingredience}...", end=" ")
            data = fetch_by_product_name(ingredience)
            if data:
                nutricni_data[ingredience] = data
                print("✓")
            else:
                print("⚠️  (nenalezeno)")
        
        print()
        print(f"✅ Nutriční data aktualizována ({len(nutricni_data)} položek)")
        print()
        
    except Exception as e:
        print(f"❌ Chyba při stahování nutričních dat: {e}")
        print("   Pokračuji s obecnými daty...")
    
    return {
        'discounts': discounts if 'discounts' in locals() else {},
        'nutrition': nutricni_data if 'nutricni_data' in locals() else {}
    }

def _filtruj_keto_produkty(self, discounts):
    """Filtruje produkty vhodné pro keto/low-carb dietu."""
    keto_keywords = [
        'kuřecí', 'krůtí', 'hovězí', 'vepřové', 'losos', 'makrela',
        'vejce', 'tvaroh', 'jogurt', 'sýr', 'máslo',
        'avokádo', 'ořechy', 'olivový olej',
        'brokolice', 'špenát', 'paprika', 'salát'
    ]
    
    relevan tni = []
    for store, products in discounts.items():
        for product in products:
            name_lower = product.name.lower()
            if any(keyword in name_lower for keyword in keto_keywords):
                relevantni.append(product)
    
    # Seřadit podle slevy
    relevantni.sort(key=lambda p: p.discount_percentage or 0, reverse=True)
    return relevantni
```

### Krok 2: Integrovat do hlavního workflow

V metodě `spustit_kompletni_zpracovani()` přidat:

```python
# Krok 8: Stáhnout aktuální data
aktualni_data = self.stahnout_aktualni_data()
if interactive:
    input("\n⏸️  Stiskněte Enter pro pokračování...")
```

---

## 📅 Doporučený workflow

### Sobota ráno (před nákupem):

```bash
# 1. Spustit hlavní systém s automatickým stahováním dat
python zpracuj_dotazniky_a_vytvor_plan.py --auto

# Systém automaticky:
# ✓ Stáhne aktuální slevy z Kupi.cz
# ✓ Aktualizuje nutriční data
# ✓ Vygeneruje nákupní seznam s aktuálními cenami
# ✓ Vytvoří AI prompt templates
# ✓ Zobrazí TOP 10 slev relevantních pro keto
```

### Výstupy:

1. **Nákupní seznam**: `/tmp/nakupni_seznam_globus.txt`
   - Obsahuje aktuální slevy
   - Prioritizuje produkty v akci

2. **AI Templates**: `/tmp/ai_prompt_templates.txt`
   - Zahrnuje aktuální ceny
   - Doporučuje produkty v akci

3. **Report o slevách**: Console output
   - TOP 10 slev pro keto/low-carb
   - Srovnání cen mezi obchody

---

## 🔧 Implementace - Kód

### Soubor: `zpracuj_dotazniky_a_vytvor_plan.py`

Přidat na konec třídy `RodinnyPlanSystem`:

```python
def stahnout_aktualni_data(self):
    """Stáhne aktuální slevy a nutriční data."""
    # Implementace viz výše
    pass

def _filtruj_keto_produkty(self, discounts):
    """Filtruje produkty vhodné pro keto/low-carb dietu."""
    # Implementace viz výše
    pass
```

V metodě `spustit_kompletni_zpracovani()`:

```python
# Po kroku 7 (AI templates) přidat:
if interactive:
    input("\n⏸️  Stiskněte Enter pro pokračování...")

# Krok 8: Stáhnout aktuální data
print()
aktualni_data = self.stahnout_aktualni_data()

# Aktualizovat nákupní seznam s aktuálními cenami
if aktualni_data['discounts']:
    self._aktualizovat_nakupni_seznam(aktualni_data['discounts'])
```

---

## ⚙️ Konfigurace

### Rate Limiting

Scrapery respektují rate limiting:
- **Kupi.cz**: 2-3 sekundy mezi requesty
- **Kaloricketabulky.cz**: 2 sekundy mezi requesty

### Timeout

Nastavení timeoutu pro requesty:
```python
# V kupi_scraper.py a fetch_nutrition_data.py
timeout = 10  # sekund
```

### Chybová zpracování

Systém pokračuje i při selhání stahování:
- ✅ Použije obecná data pokud selže scraping
- ✅ Loguje chyby do konzole
- ✅ Nepřeruší celý proces

---

## 🎯 Výhody integrace

1. **Aktuální ceny** - Vždy nejnovější slevy
2. **Optimalizace rozpočtu** - Automatické doporučení produktů v akci
3. **Přesná nutrice** - Aktuální nutriční data
4. **Časová úspora** - Automatizace ruční kontroly letáků
5. **Lepší rozhodování** - Data-driven nákupy

---

## 📊 Příklad výstupu

```
================================================================================
📥 KROK 8: Stahování aktuálních dat
================================================================================

🛒 Stahuji slevy z Kupi.cz...
  • Lidl... ✓ (234 produktů)
  • Kaufland... ✓ (312 produktů)
  • Albert... ✓ (189 produktů)
  • Penny... ✓ (156 produktů)
  • Globus... ✓ (278 produktů)

✅ Slevy staženy úspěšně!
   Celkem: 1169 produktů v akci

🥩 TOP 10 SLEV pro keto/low-carb:
   1. Kuřecí prsa čerstvé
      89.90 Kč (-40%) @ Lidl
   2. Losos norský filety
      199.00 Kč (-33%) @ Kaufland
   3. Tvaroh Olma 9%
      25.90 Kč (-30%) @ Penny
   4. Vejce čerstvá L (10ks)
      34.90 Kč (-30%) @ Lidl
   5. Olivový olej extra panenský
      119.00 Kč (-25%) @ Albert
   ...

📊 Aktualizuji nutriční data...
  • Kuřecí prsa... ✓
  • Mleté maso... ✓
  • Losos... ✓
  • Vejce... ✓
  • Tvaroh... ✓
  • Řecký jogurt... ✓

✅ Nutriční data aktualizována (6 položek)
```

---

## 🚦 Status implementace

| Komponenta | Status | Poznámka |
|------------|--------|----------|
| Kupi.cz scraper | ✅ Hotovo | `src/scrapers/kupi_scraper.py` |
| Kaloricketabulky scraper | ✅ Hotovo | `fetch_nutrition_data.py` |
| Integrace do hlavního systému | ⏳ K implementaci | Přidat krok 8 |
| Automatizace (cron) | 📝 Dokumentováno | Manuální nastavení |

---

## 📝 TODO - Implementace

- [ ] Přidat metodu `stahnout_aktualni_data()` do `RodinnyPlanSystem`
- [ ] Přidat metodu `_filtruj_keto_produkty()` do `RodinnyPlanSystem`
- [ ] Integrovat krok 8 do `spustit_kompletni_zpracovani()`
- [ ] Aktualizovat nákupní seznam s cenami z Kupi
- [ ] Aktualizovat AI templates s aktuálními cenami
- [ ] Přidat error handling pro síťové chyby
- [ ] Vytvořit cache pro stažená data (platnost 24h)
- [ ] Testovat integraci

---

## 💡 Budoucí vylepšení

1. **Cache systém** - Ukládat stažená data na 24h
2. **Notifikace** - Email/SMS při dobrých slevách
3. **Analýza trendů** - Sledování vývoje cen
4. **AI predikce** - Kdy kupovat co pro nejlepší cenu
5. **Mobilní app** - Nákupní seznam na telefonu

---

**Datum vytvoření**: 18.1.2026  
**Status**: Připraveno k implementaci  
**Priorita**: Vysoká (značně zlepší užitečnost systému)
