# Plán pokračování vývoje - Vylepšení analyzátoru masa a nákupních seznamů

## Priorita: Medium
## Typ: Enhancement
## Label: feature, enhancement, keto-diet

---

## Kontext

Po úspěšné implementaci základního analyzátoru masných produktů a generátoru nákupních seznamů byly identifikovány následující oblasti pro vylepšení.

**Související PR**: #[aktuální PR]
**Dokumentace**: `docs/technical/MEAT_ANALYZER_GUIDE.md`

---

## 1. Vylepšení scrapování a parsování ⭐⭐⭐

### 1.1 Lokace a dostupnost
- [ ] **Automatický výběr lokace** na kupi.cz (Valašské Meziříčí)
  - Analýza cookies a session management
  - Implementace lokačního filtru
  - Testování s různými lokacemi
- [ ] **Parsování dostupnosti produktů**
  - Detekce "vyprodáno" / "skladem"
  - Zobrazení stavu ve výstupech
  - Filtrování nedostupných produktů

### 1.2 Rozšířené informace o produktech
- [ ] **Extrakce čárových kódů (EAN)**
  - Implementace parsování EAN z detailních stránek
  - Integrace s `fetch_nutrition_data.py` pro ověření podle EAN
  - Cache nutričních dat podle EAN
- [ ] **Parsování dat platnosti**
  - Extrakce "platí od" a "platí do" z letáků
  - Automatické filtrování vypršených akcí
  - Upozornění na blížící se konec platnosti
- [ ] **Cena za jednotku**
  - Extrakce a parsování ceny/kg, ceny/l
  - Porovnání jednotkových cen mezi produkty
  - Řazení podle nejlepší ceny za jednotku

### 1.3 Další kategorie
- [ ] **Rozšíření na další kategorie masa**
  - Červené maso (hovězí, vepřové)
  - Ryby a mořské plody
  - Zpracované masné výrobky (šunka, klobásy)
- [ ] **Další keto kategorie**
  - Nízkosacharidová zelenina
  - Ořechy a semínka
  - Zdravé tuky (olivový olej, kokosový olej, máslo)

---

## 2. Integrace nutričních databází ⭐⭐⭐

### 2.1 Vylepšení ověřování
- [ ] **Cachování nutričních dat**
  - Lokální databáze SQLite pro cachování
  - Prevence opakovaných dotazů
  - Automatická aktualizace starých dat
- [ ] **Vyhledávání podle EAN**
  - Primární vyhledávání podle čárového kódu
  - Fallback na textové vyhledávání
  - Zvýšení přesnosti shody
- [ ] **Fuzzy matching názvů**
  - Implementace Levenshtein distance
  - Lepší shoda podobných názvů
  - Automatické opravy překlepů

### 2.2 Další nutriční databáze
- [ ] **Podpora více databází**
  - Open Food Facts API
  - USDA FoodData Central
  - Lokální databáze
- [ ] **Agregace dat z více zdrojů**
  - Kombinace dat z různých databází
  - Výběr nejkompletnějších dat
  - Ověření konzistence

---

## 3. Vylepšení analyzátoru a skórování ⭐⭐

### 3.1 Inteligentní skórování
- [ ] **Rozšířené keto skóre**
  - Zahrnutí omega-3/omega-6 poměru
  - Bonus za bio/free-range produkty
  - Penalizace za zpracované maso
- [ ] **Personalizované skóre**
  - Podle individuálních makro cílů (Roman, Pája, Kubík)
  - Zohlednění osobních preferencí
  - Alergeny a nesnášenlivost
- [ ] **Hodnocení kvality**
  - Země původu
  - Způsob chovu (bio, farmářské)
  - Čerstvost vs. zmrazené

### 3.2 Nutriční analýza
- [ ] **Detailní makro rozklad**
  - Složení aminokyselin
  - Typy tuků (nasycené, nenasycené)
  - Obsah vlákniny
- [ ] **Mikronutrienty**
  - Vitaminy (A, D, E, K, B komplex)
  - Minerály (železo, zinek, hořčík)
  - Pro Kubíka - důraz na vitamin A (zrak)

---

## 4. Vylepšení generátoru nákupních seznamů ⭐⭐⭐

### 4.1 Optimalizace nákupu
- [ ] **Cenová optimalizace**
  - Algoritmus pro minimalizaci nákladů
  - Porovnání cen mezi obchody
  - Doporučení nejlepšího obchodu
- [ ] **Automatické plánování**
  - Navržení optimální trasy mezi obchody
  - Zohlednění otevírací doby
  - Minimalizace času stráveného nakupováním
- [ ] **Týdenní plánování**
  - Rozložení nákupu na více dnů
  - Čerstvé produkty vs. trvanlivé
  - Koordinace s jídelníčkem

### 4.2 Rodinné potřeby
- [ ] **Individuální seznamy**
  - Seznam pro každého člena rodiny
  - Zohlednění individuálních makro cílů
  - Speciální požadavky (Kubík - vitamin A)
- [ ] **Množstevní kalkulace**
  - Automatický výpočet množství na týden
  - Zohlednění porce a frekvence jídel
  - Přebytky a zásoby

### 4.3 Export a formáty
- [ ] **Více formátů exportu**
  - PDF (tisknutelný)
  - JSON (pro API)
  - CSV (pro tabulkový procesor)
  - Integrace s Todoist/Notion
- [ ] **QR kódy**
  - QR kód pro mobilní zobrazení
  - QR kódy produktů pro rychlé vyhledání
  - Sdílení seznamů přes QR

---

## 5. Webové rozhraní a API ⭐⭐

### 5.1 REST API
- [ ] **FastAPI backend**
  - `/api/v1/products/search` - vyhledávání produktů
  - `/api/v1/products/analyze` - analýza produktu
  - `/api/v1/shopping-lists/generate` - generování seznamu
  - `/api/v1/nutrition/verify` - ověření nutriční hodnoty
- [ ] **Autentizace**
  - JWT tokeny
  - Uživatelské účty
  - Rate limiting

### 5.2 Webové UI
- [ ] **Frontend (React/Vue)**
  - Dashboard s přehledem akcí
  - Interaktivní nákupní seznam
  - Vizualizace nutriční hodnoty
  - Grafy a statistiky
- [ ] **Mobilní responzivita**
  - Použitelné na telefonu
  - Offline režim
  - PWA podpora

---

## 6. Automatizace a notifikace ⭐

### 6.1 Automatické aktualizace
- [ ] **Scheduled scraping**
  - Denní aktualizace akcí (např. 6:00 ráno)
  - Notifikace o nových slevách
  - Sledování změn cen
- [ ] **Upozornění**
  - Email notifikace o top slevách
  - Push notifikace na mobil
  - Telegram/Discord bot

### 6.2 Historie a trendy
- [ ] **Databáze historie cen**
  - Sledování vývoje cen
  - Predikce budoucích slev
  - Optimální doba nákupu
- [ ] **Statistiky**
  - Průměrné úspory za měsíc
  - Nejčastěji kupované produkty
  - Trendy v keto nakupování

---

## 7. Testování a kvalita ⭐⭐

### 7.1 Rozšíření testů
- [ ] **Integrační testy s reálnými daty**
  - Test s živými daty z kupi.cz
  - Ověření parsování všech obchodů
  - Test nutričního ověřování
- [ ] **End-to-end testy**
  - Kompletní flow: vyhledání → analýza → seznam
  - Test exportů do všech formátů
  - Validace českých datumů
- [ ] **Performance testy**
  - Měření rychlosti scrapování
  - Optimalizace dotazů do databází
  - Load testing API

### 7.2 Error handling
- [ ] **Robustní error handling**
  - Graceful degradation při výpadku webu
  - Retry mechanismy s exponential backoff
  - Detailní logování chyb
- [ ] **Monitoring**
  - Health check endpointy
  - Uptime monitoring
  - Alerting při problémech

---

## 8. Dokumentace ⭐

### 8.1 Uživatelská dokumentace
- [ ] **Quickstart guide**
  - Instalace a setup
  - První spuštění
  - Typické use cases
- [ ] **Video tutoriály**
  - Screencasty základních funkcí
  - Tipy a triky
  - Troubleshooting

### 8.2 Technická dokumentace
- [ ] **API dokumentace**
  - OpenAPI/Swagger specs
  - Příklady použití
  - Authentication guide
- [ ] **Architecture diagram**
  - Vizualizace komponent
  - Data flow diagram
  - Deployment guide

---

## Prioritizace

### High Priority (⭐⭐⭐)
1. Extrakce EAN kódů a lepší nutriční ověření
2. Cenová optimalizace v nákupních seznamech
3. Parsování dat platnosti
4. Automatický výběr lokace

### Medium Priority (⭐⭐)
1. Rozšíření na další kategorie
2. Webové API
3. Cachování nutričních dat
4. Rozšířené testování

### Low Priority (⭐)
1. Webové UI
2. Automatické notifikace
3. Historie a trendy
4. Video dokumentace

---

## Závěr

Tento plán poskytuje komplexní roadmapu pro další vývoj. Doporučuji začít s high priority items, zejména:

1. **EAN a nutriční ověření** - zvýší přesnost doporučení
2. **Cenová optimalizace** - přímý benefit pro uživatele
3. **Parsování dat platnosti** - zlepší relevanci výsledků

---

**Created**: 18.1.2026  
**Status**: Open  
**Estimated effort**: 40-60 hodin (rozloženo na více sprintů)  
**Dependencies**: Aktuální PR musí být merged první
