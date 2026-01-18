# Pája - Zaznamenané odpovědi (část 1) - Implementační dokumentace

## 📋 Přehled

Tento dokument popisuje implementaci zaznamenaných odpovědí z dotazníku o stravě pro Páju (osoba_2). Změny jsou založeny na problem statement "Pája – zaznamenané odpovědi (část 1)".

## 🎯 Cíl

Zaznamenat a strukturovat kvalitativní data o:
- Vzorcích hladu a energie
- Preferované struktuře jídel
- Jídlech, která dobře sytí
- Problematických jídlech
- Tělesných reakcích na jídlo

## 📁 Změněné soubory

### 1. `osoby/osoba_2/preference.py` ⭐ Hlavní změna

Přidáno **5 nových tříd**:

#### `HladAEnergie`
Zaznamenává vzorce hladu a energetických úrovní.

**Klíčová data:**
- Nejvyšší hlad: ráno
- Pocit bez energie při správném jídle: spíše ne
- Přejedení bez hladu: ano
- Horší pocit: plnost/těžkost (vs. hlad)
- **Důležité zjištění**: Citlivost na objem jídla, NE na kalorickou hodnotu

**Použití:**
```python
from osoby.osoba_2.preference import HladAEnergie

prehled = HladAEnergie.ziskej_prehled()
print(f"Nejvyšší hlad: {prehled['nejvyssi_hlad']}")  # "ráno"
```

#### `StrukturaJidel`
Preference ohledně struktury dne a velikosti porcí.

**Klíčová data:**
- Nejproblematičtější jídlo: oběd
- Důvod: moc velké porce
- Preference: rovnoměrnější porce během dne

**Doporučení:**
- Zmenšit porce u oběda
- Rozdělit kalorie rovnoměrněji mezi všechna jídla
- Více menších jídel místo jednoho velkého oběda

**Použití:**
```python
from osoby.osoba_2.preference import StrukturaJidel

doporuceni = StrukturaJidel.ziskej_doporuceni_porci()
print(f"Problém: {doporuceni['duvod']}")
```

#### `SyticiJidla`
Jídla, která dobře sytí.

**Klíčová data:**
- Jídla: kaše, ovoce, jogurt, kombinace, luštěniny se semínky
- **Faktory sytosti**: vláknina + objem + jemná sladkost
- **Co NESYTÍ**: tuk ⚠️

**⚠️ DŮLEŽITÉ ZJIŠTĚNÍ:**
Tuk není faktor sytosti pro Páju! To je zásadní rozdíl oproti standardní keto dietě, kde je tuk primární faktor sytosti.

**Použití:**
```python
from osoby.osoba_2.preference import SyticiJidla

# Kontrola, zda je jídlo sytící
if SyticiJidla.je_jidlo_sytici("ovesná kaše"):
    print("✅ Toto jídlo dobře sytí")

# Získat přehled
prehled = SyticiJidla.ziskej_prehled()
print("Faktory sytosti:", prehled['faktory_sytosti'])
```

#### `ProblematickaJidla`
Jídla, která chutnají, ale způsobují problémy.

**Klíčová data:**
- Káva: spouštěč chutí i propadu energie
- Pečené brambory: pravděpodobně problém s tukem
- Čokoláda: spouští chutě na sladké
- Kakao ve větším množství: v malém OK (v buchtě)
- Cibule: spíš v malém množství
- Knedlíky: způsobují nadýmání

**⚠️ Speciální upozornění o kávě:**
- Káva je SPOUŠTĚČ chutí, NE pomocník
- Způsobuje 'dojezd' (propad energie) po ~3 hodinách
- Kombinace káva + kaše = nadýmání

**Použití:**
```python
from osoby.osoba_2.preference import ProblematickaJidla

if ProblematickaJidla.je_jidlo_problematicke("káva"):
    duvod = ProblematickaJidla.ziskej_duvod_problemu("káva")
    print(f"⚠️ {duvod}")
```

#### `ReakceTela`
Tělesné reakce na různé typy jídel.

**Klíčová data:**

**Nadýmání - spouštěče:**
- Kaše + káva (hlavně při velkém množství)
- Špatný odhad porce (obecně)
- Knedlíky

**Únava - spouštěče:**
- Dojezd po kávě (~3 hodiny)
- Masná jídla
- Přejedení
- Hodně sladké jídlo

**Chutě na sladké - spouštěče:**
- Po čokoládě
- Po kávě
- Když jídlo neuspokojí → řeší to sladkým/kafem z automatu

**Použití:**
```python
from osoby.osoba_2.preference import ReakceTela

# Kontroly
if ReakceTela.muze_zpusobit_nadymani("kaše"):
    print("⚠️ Může způsobit nadýmání")

if ReakceTela.muze_zpusobit_unavu("káva"):
    print("⚠️ Může způsobit únavu")

if ReakceTela.muze_spustit_chute_na_sladke("čokoláda"):
    print("⚠️ Může spustit chutě na sladké")
```

### 2. `test_paja_preferences.py` ✅ Nový testovací soubor

Kompletní testovací suite pro všechny nové třídy.

**Testy:**
- `test_hlad_a_energie()` - Vzorce hladu a energie
- `test_struktura_jidel()` - Struktura jídel a doporučení
- `test_sytici_jidla()` - Sytící jídla a faktory
- `test_problematicka_jidla()` - Problematická jídla
- `test_reakce_tela()` - Tělesné reakce
- `test_integrace_s_preferencemi()` - Integrace s existujícími preferencemi

**Spuštění:**
```bash
python test_paja_preferences.py
```

### 3. `demo_paja_responses.py` 📚 Demo skript

Praktická ukázka použití všech nových tříd.

**Obsahuje:**
- Analýzu 6 různých jídel
- Plánování jídel s ohledem na preference
- Důležité upozornění o kávě

**Spuštění:**
```bash
python demo_paja_responses.py
```

## 🔑 Klíčová zjištění

### 1. Sytost ≠ Tuk
Pro Páju **tuk není faktor sytosti**. Místo toho funguje:
- Vláknina
- Objem jídla
- Jemná sladkost

To je zásadní rozdíl oproti standardní keto dietě!

### 2. Objem > Kalorie
Pája je citlivá na **objem jídla**, ne na kalorickou hodnotu. Pocit plnosti a těžkosti je horší než hlad.

### 3. Káva jako spouštěč
Káva není pomocník, ale **spouštěč**:
- Chutí na sladké
- Propadu energie (~3h)
- Nadýmání (v kombinaci s kaší)

### 4. Struktura jídel
- Oběd je problematický (příliš velké porce)
- Preference: rovnoměrnější rozložení porcí během dne
- Nejvyšší hlad je ráno → vydatnější snídaně

## 📊 Testování

### Nové testy
```bash
python test_paja_preferences.py
# Výsledek: ✅ 6/6 testů prošlo
```

### Existující testy (regrese)
```bash
python test_texture_preferences.py
# Výsledek: ✅ Všechny testy prošly (žádná regrese)
```

### Demo
```bash
python demo_paja_responses.py
# Výsledek: ✅ Funguje správně
```

## 🔧 Technické detaily

### Type hints
Všechny funkce mají správné type hinty:
```python
def ziskej_prehled() -> Dict[str, Any]: ...
def je_jidlo_sytici(jidlo: str) -> bool: ...
def ziskej_duvod_problemu(jidlo: str) -> Optional[str]: ...
```

### Dokumentace
Všechny třídy a metody mají české docstringy podle PEP 257.

### Integrace
Nové třídy jsou plně kompatibilní s existujícími třídami `PreferenceJidel` a `DietniOmezeni`.

## 💡 Použití v praxi

### Příklad: Plánování snídaně
```python
from osoby.osoba_2.preference import (
    HladAEnergie, SyticiJidla, ReakceTela
)

# Zjistit, kdy je největší hlad
if HladAEnergie.NEJVYSSI_HLAD == "ráno":
    # Plánovat vydatnější snídani
    
    # Co bude sytit?
    if SyticiJidla.je_jidlo_sytici("ovesná kaše s ovocem"):
        print("✅ Dobrá volba pro snídani")
    
    # Zkontrolovat reakce
    if not ReakceTela.muze_spustit_chute_na_sladke("ovesná kaše"):
        print("✅ Nebude spouštět chutě")
```

### Příklad: Kontrola problematických kombinací
```python
from osoby.osoba_2.preference import ProblematickaJidla, ReakceTela

# Snídaně: kaše + káva
if "káva" in "kaše + káva" and "kaše" in "kaše + káva":
    print("⚠️ VAROVÁNÍ: Tato kombinace způsobuje nadýmání!")
    print(ProblematickaJidla.UPOZORNENI_KAVA)
```

## 📝 Poznámky pro další vývoj

1. **Meal planning algoritmy** by měly zohlednit:
   - Větší snídani (nejvyšší hlad ráno)
   - Menší oběd (problematické velké porce)
   - Preferenci vlákniny a objemu nad tuk

2. **Nákupní seznamy** by měly prioritizovat:
   - Kaši, ovoce, jogurt
   - Luštěniny se semínky
   - Potraviny bohaté na vlákninu

3. **Varování** by měla být zobrazena při:
   - Plánování kávy (spouštěč chutí/únavy)
   - Velkých porcích (nadýmání)
   - Čokoládě (spouští chutě)

## 🚀 Další kroky

Pro "část 2" by mohly být přidány:
- Časové preference jídel
- Sociální aspekty stravování
- Sezónní preference
- Další tělesné reakce
- Integrace s meal planning systémem

## 📚 Reference

- Problem statement: "Pája – zaznamenané odpovědi (část 1)"
- Existující preference: `osoby/osoba_2/preference.py` (původní verze)
- Testovací vzor: `test_texture_preferences.py`
