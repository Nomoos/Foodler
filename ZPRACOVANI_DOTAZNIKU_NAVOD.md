# 📋 Zpracování dotazníků a vytvoření komplexního plánu

## 🎯 Účel

Tento skript (`zpracuj_dotazniky_a_vytvor_plan.py`) zpracovává dotazníky pro všechny členy rodiny a vytváří komplexní plán zahrnující:

1. ✅ **Zpracování dotazníků** pro všechny osoby (Roman, Pája, Kubík)
2. ✅ **Sestavení personalizovaných doporučení** pro každého
3. ✅ **Plánování meal prep potřeb** (potraviny a nádoby)
4. ✅ **Shrnutí nákupního plánu** s odhadem cen
5. ✅ **Vytvoření nákupního seznamu pro Globus**
6. ✅ **Získání personalizovaných doporučení** pro celou rodinu

## 📖 Použití

### Interaktivní režim (s pauzami)

```bash
python zpracuj_dotazniky_a_vytvor_plan.py
```

Tento režim zobrazuje výstup postupně a čeká na stisknutí Enter mezi jednotlivými kroky.

### Automatický režim (bez pauzy)

```bash
python zpracuj_dotazniky_a_vytvor_plan.py --auto
```

Tento režim spustí všechny kroky automaticky bez čekání na uživatelský vstup.

## 📊 Co skript dělá

### KROK 1: Načítání profilů osob

Načte profily všech členů rodiny:
- **Roman**: 134.2 kg → cíl 95 kg | 2000 kcal/den | 140g P / 70g C / 129g F
- **Pája**: 77.3 kg → cíl 57 kg | 1508 kcal/den | 92g P / 60g C
- **Kubík**: 17 kg | 1400 kcal/den | Důraz na vitamin A a vlákninu

### KROK 2: Personalizovaná doporučení

Vytvoří specifická doporučení pro každou osobu:
- **Roman**: Meal prep strategie, protein-first přístup, low-carb
- **Pája**: Kalorický deficit, hormonální podpora, emoční stravování
- **Kubík**: Vitamin A pro zrak, vláknina pro trávení, omega-3

### KROK 3: Meal prep potřeby

Vypočítá:
- Týdenní nutriční potřeby (34,356 kcal/týden)
- Potřebné potraviny (2.5 kg kuřecích prsou, 1.5 kg mletého masa, atd.)
- Potřebné nádoby (48 meal prep krabiček + 30 vakuovacích sáčků)

### KROK 4: Nákupní plán

Shrne nákupní plán s rozpisem podle kategorií:
- **PROTEINY**: 1370 Kč
- **ZELENINA**: 510 Kč
- **PRO KUBÍKA**: 370 Kč
- **TUKY A DALŠÍ**: 460 Kč
- **CELKEM**: 2710 Kč/týden

### KROK 5: Seznam pro Globus

Vytvoří strukturovaný nákupní seznam specificky pro Globus s checkboxy:
- Maso a ryby
- Mléčné výrobky
- Zelenina
- Položky pro Kubíka
- Tuky a ořechy
- Koření a doplňky
- Doplňky stravy

**Výstup**: Nákupní seznam je uložen v dočasném adresáři systému:
- **Linux/Mac**: `/tmp/nakupni_seznam_globus.txt`
- **Windows**: `%TEMP%\nakupni_seznam_globus.txt`

### KROK 6: Komplexní rodinný plán

Poskytne:
- Týdenní harmonogram (sobota = nákup, neděle = meal prep)
- Individuální doporučení pro každého
- Klíčová doporučení pro úspěch
- Ukázkový týdenní jídelníček

## 📁 Výstupy

### Soubory vytvořené skriptem:

1. **Nákupní seznam pro Globus** - Tisknutelný nákupní seznam
   - **Lokace**: Dočasný adresář systému
     - Linux/Mac: `/tmp/nakupni_seznam_globus.txt`
     - Windows: `%TEMP%\nakupni_seznam_globus.txt`
   - Strukturováno podle kategorií
   - Checkbox formát (☐) pro zaškrtávání
   - Datum vytvoření

## 🎯 Příklad použití

```bash
# Spustit automaticky
python zpracuj_dotazniky_a_vytvor_plan.py --auto > output.txt

# Zobrazit vytvořený seznam
cat /tmp/nakupni_seznam_globus.txt

# Vytisknout seznam
lp /tmp/nakupni_seznam_globus.txt
```

## 📊 Ukázka výstupu

```
********************************************************************************
*         FOODLER - SYSTÉM PRO ZPRACOVÁNÍ DOTAZNÍKŮ A PLÁNOVÁNÍ STRAVY         *
********************************************************************************

================================================================================
📋 KROK 1: Načítání profilů osob
================================================================================

👤 Roman (Romča):
   ✅ Profil načten z README.md
   📊 Aktuální váha: 134.2 kg, Cíl: 95 kg
   🎯 Denní cíl: 2000 kcal | 140g P / 70g C / 129g F

...
```

## 🔧 Technické detaily

### Závislosti

```python
- osoby.osoba_3.profil.DetskyyProfil
```

### Struktura

```
RodinnyPlanSystem:
  ├── nacti_dotazniky()          # Načte profily všech osob
  ├── sestavit_doporuceni()      # Vytvoří doporučení
  ├── zvazit_meal_prep_potreby() # Spočítá potřeby
  ├── shrnout_nakupni_plan()     # Shrne nákup s cenami
  ├── vytvorit_seznam_globus()   # Vytvoří seznam pro Globus
  └── shrnout_personalizovana_doporuceni() # Komplexní plán
```

## 💡 Tipy

### Pro tisk nákupního seznamu:

```bash
# Linux
lp /tmp/nakupni_seznam_globus.txt

# macOS
lpr /tmp/nakupni_seznam_globus.txt

# Nebo otevřít v editoru a vytisknout
gedit /tmp/nakupni_seznam_globus.txt
```

### Pro pravidelné použití:

1. **Každou sobotu ráno** - Spustit skript
2. **Vytisknout seznam** - Vzít s sebou do obchodu
3. **Nakoupit podle seznamu** - Lidl, Kaufland, Globus
4. **Neděle** - Meal prep podle plánu

## 🎓 Související dokumentace

- **[DOTAZNIK_OTAZKY.md](osoby/osoba_1/DOTAZNIK_OTAZKY.md)** - Dotazník pro Romana
- **[DOTAZNIK_OTAZKY.md](osoby/osoba_2/DOTAZNIK_OTAZKY.md)** - Dotazník pro Páju
- **[profil.py](osoby/osoba_3/profil.py)** - Profil Kubíka
- **[README.md](README.md)** - Hlavní dokumentace projektu

## 📝 Poznámky

- Skript používá data z README.md pro profily (aktuální váha, cíle)
- Ceny jsou odhadované podle aktuálních tržních cen v ČR (2026)
- Seznam je optimalizovaný pro keto/low-carb dietu pro dospělé
- Pro Kubíka zahrnuje vyšší podíl sacharidů a vitamin A pro zrak

## 🚀 Další vývoj

Plánované vylepšení:
- [ ] Načítání skutečných slev z Kupi.cz API
- [ ] Automatická optimalizace podle aktuálních akcí
- [ ] Export do mobilní aplikace (iOS/Android)
- [ ] Integrace s Google Keep / Todoist
- [ ] QR kód pro rychlý přístup k seznamu v obchodě

## ⚠️ Důležité upozornění

**Rozpočet**: Odhadovaná cena 2710 Kč/týden překračuje původní rozpočet 2500 Kč o 210 Kč.

**Cenová aktualizace**: Ceny byly naposledy aktualizovány 18.1.2026 a jsou založené na aktuálních tržních cenách v ČR. Pro nejaktuálnější ceny doporučujeme zkontrolovat letáky nebo použít Kupi.cz.

**Možnosti úspory**:
1. Nakupovat mleté maso místo části kuřecích prsou (-100 Kč)
2. Použít mražený losos místo čerstvého (-80 Kč)
3. Sledovat akce na Kupi.cz před nákupem (-50-100 Kč)
4. Nakupovat ve více obchodech podle slev

## 📞 Podpora

Pokud máte otázky nebo problémy:
1. Zkontrolujte, zda máte nainstalované všechny závislosti
2. Spusťte v automatickém režimu pro ladění: `--auto > log.txt`
3. Kontaktujte správce projektu

---

**Autor**: Foodler System  
**Poslední aktualizace**: 18.1.2026  
**Verze**: 1.0.0
