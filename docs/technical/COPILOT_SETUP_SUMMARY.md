# Přehled: GitHub Copilot Pro+ Konfigurace

## ✅ Co bylo vytvořeno

Tento dokument shrnuje změny provedené pro povolení GitHub Copilot Pro+ přístupu k webovým datům pro testování scraperů.

---

## 📄 Vytvořené soubory

### 1. **docs/technical/GITHUB_COPILOT_WEB_ACCESS.md**
**Hlavní návod v češtině** (530 řádků)

Kompletní průvodce obsahující:
- ✅ Požadavky pro GitHub Copilot Pro+
- ✅ Krok-za-krokem konfigurace repozitáře
- ✅ Povolení přístupu k webovým stránkám (kaloricketabulky.cz, kupi.cz)
- ✅ Vytvoření Copilot instrukcí
- ✅ Testovací příklady
- ✅ Řešení problémů (troubleshooting)
- ✅ Best practices a doporučení
- ✅ Pokročilé použití

**Klíčové sekce:**
- Přehled GitHub Copilot Pro+ funkcí
- Konfigurace přístupu na úrovni účtu/organizace
- Testování scraperů s reálnými daty
- Automatické monitoring a aktualizace
- Etické použití scraperů

### 2. **.github/copilot-instructions.md**
**Copilot instrukce pro projekt** (399 řádků)

Tento soubor říká GitHub Copilotu:
- ✅ Co je účel projektu (keto/low-carb diet planning)
- ✅ Jak fungují oba scrapery (kaloricketabulky.cz, kupi.cz)
- ✅ Jaké jsou testovací postupy
- ✅ Jak psát kód (konvence, style guide)
- ✅ Kontext dietního plánu (makra, cíle)
- ✅ Etické pravidla pro scraping

**Copilot díky tomuto bude:**
- Rozumět kontextu projektu
- Navrhovat konzistentní kód
- Testovat s reálnými daty (když má web access)
- Respektovat české konvence (komentáře v češtině)

### 3. **test_scrapers_integration.py**
**Integrační testy s reálnými daty** (286 řádků)

Spustitelný Python skript demonstrující:
- ✅ Test nutrition scraperu (kaloricketabulky.cz)
- ✅ Test discount scraperu (kupi.cz)
- ✅ Hledání keto-friendly produktů
- ✅ Kombinovaný workflow (nutriční data + ceny)

**Použití:**
```bash
python test_scrapers_integration.py
```

**Funkce:**
- Testuje vyhledávání produktů
- Získává nutriční data
- Hledá aktuální slevy
- Kombinuje oba scrapery pro komplexní use case
- Respektuje rate limiting (2s prodleva)

### 4. **Aktualizované soubory**

**README.md** - Přidán odkaz na nový návod:
```markdown
### 🔧 Technická dokumentace
- **[GITHUB_COPILOT_WEB_ACCESS.md]** - ⭐ Návod pro GitHub Copilot Pro+ a testování scraperů
```

**README_EN.md** - Přidán odkaz na nový návod (anglická verze)

---

## 🎯 Jak to použít

### Krok 1: Povolit GitHub Copilot Pro+ web access

1. Přejděte na https://github.com/settings/copilot
2. Povolte **"Allow GitHub Copilot to access the web"**
3. Pro organizační repo: administrátor musí povolit v org settings

### Krok 2: Přidat povolené domény

V nastavení přidejte:
```
www.kaloricketabulky.cz
kaloricketabulky.cz
www.kupi.cz
kupi.cz
```

### Krok 3: Používat Copilot pro testování

V GitHub Copilot Chat (VS Code):

```
@workspace Otestuj fetch_nutrition_data.py s reálným produktem 
"Kuřecí prsa" z kaloricketabulky.cz
```

Copilot teď:
- ✅ Přistoupí na web
- ✅ Načte reálná data
- ✅ Porovná se scraperem
- ✅ Ohlásí, jestli funguje

### Krok 4: Spustit integrační testy

```bash
# Lokálně s reálnými daty
python test_scrapers_integration.py

# Nebo požádejte Copilot:
@workspace Spusť test_scrapers_integration.py a analyzuj výsledky
```

---

## 📚 Dokumentace

### Pro uživatele:
👉 **Čtěte:** `docs/technical/GITHUB_COPILOT_WEB_ACCESS.md`
- Kompletní návod v češtině
- Krok-za-krokem instrukce
- Troubleshooting
- Best practices

### Pro vývojáře:
👉 **Čtěte:** `.github/copilot-instructions.md`
- Kontext projektu pro AI
- Coding conventions
- Testing guidelines
- Ethical rules

### Pro testování:
👉 **Spusťte:** `test_scrapers_integration.py`
- Ověří, že scrapery fungují
- Testuje s reálnými daty
- Respektuje rate limiting

---

## 🔑 Klíčové přínosy

### 1. **Automatické testování s reálnými daty**
Copilot teď může:
- Načítat data přímo z webů
- Ověřovat, že scrapery fungují správně
- Detekovat změny ve struktuře HTML
- Navrhovat opravy, když se web změní

### 2. **Lepší code suggestions**
Díky `.github/copilot-instructions.md`:
- Copilot rozumí kontextu projektu
- Navrhuje kód konzistentní se stávajícím
- Respektuje české konvence
- Zná dietní cíle a makra

### 3. **Usnadnění údržby**
Když se web změní:
```
@workspace Web kaloricketabulky.cz změnil HTML strukturu.
Načti aktuální stránku a uprav scraper.
```
Copilot načte novou strukturu a opraví kód.

### 4. **Etické použití**
Návod obsahuje:
- Rate limiting (2s mezi požadavky)
- Respekt k robots.txt
- Reálné User-Agent headers
- Caching pro minimalizaci requestů

---

## 🚀 Příklady použití s Copilotem

### Příklad 1: Test scraperu
```
@workspace Otestuj nutrition scraper s produktem "Tvaroh". 
Načti reálná data z kaloricketabulky.cz a ověř, že protein je správně parsován.
```

### Příklad 2: Najít keto slevy
```
@workspace Použij kupi_scraper a najdi TOP 10 keto-friendly produktů ve slevě.
Hledej: kuřecí prsa, vejce, sýr, tvaroh, losos. Seřaď podle slevy.
```

### Příklad 3: Automatická oprava
```
@workspace Scraper nefunguje. Načti HTML z kaloricketabulky.cz, 
porovnej se současnými CSS selektory a oprav je.
```

### Příklad 4: Vytvoření testu
```
@workspace Vytvoř pytest testy pro oba scrapery. 
Použij mock data z reálných webů, které právě načteš.
```

---

## ⚠️ Důležité poznámky

### Rate Limiting
- ✅ Vždy počkejte 2+ sekundy mezi požadavky
- ✅ Používejte caching kde je to možné
- ❌ Nespouštějte desítky požadavků za sekundu

### Robots.txt
- ✅ Respektujte pravidla obou webů
- ✅ Zkontrolujte: `/robots.txt` na každém webu
- ❌ Neobcházejte anti-scraping opatření

### Změny struktury
- ⚠️ Webové stránky mění HTML pravidelně
- ✅ Testujte scrapery pravidelně
- ✅ Používejte Copilot pro rychlé opravy

---

## 📊 Statistiky

| Soubor | Řádky | Účel |
|--------|-------|------|
| GITHUB_COPILOT_WEB_ACCESS.md | 530 | Hlavní návod |
| copilot-instructions.md | 399 | AI kontext |
| test_scrapers_integration.py | 286 | Testy |
| **Celkem** | **1,215** | **Kompletní řešení** |

---

## 🎓 Další kroky

### 1. Přečtěte dokumentaci
```bash
# Otevřete hlavní návod
code docs/technical/GITHUB_COPILOT_WEB_ACCESS.md
```

### 2. Nakonfigurujte Copilot
- Povolte web access v GitHub settings
- Přidejte povolené domény
- Restartujte VS Code

### 3. Vyzkoušejte
```bash
# Spusťte integrační testy
python test_scrapers_integration.py

# Nebo použijte Copilot Chat
@workspace Test the scrapers with real data
```

### 4. Začněte používat
```
# V Copilot Chat:
@workspace Najdi nejlevnější kuřecí prsa ve slevě
@workspace Získej nutriční data pro "Losos"
@workspace Vytvoř týdenní nákupní seznam s keto produkty ve slevě
```

---

## 📞 Podpora

- **Dokumentace**: `docs/technical/GITHUB_COPILOT_WEB_ACCESS.md`
- **GitHub Issues**: Otevřete issue v repozitáři
- **GitHub Support**: Pro problémy s předplatným

---

## 📝 Licence

Tento návod je součástí Foodler projektu - MIT License

---

**Vytvořeno:** 18. ledna 2026  
**Autor:** Foodler Project Team  
**Verze:** 1.0
