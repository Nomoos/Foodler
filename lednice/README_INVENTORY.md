# 📦 Správa Zásob - Návod

## 🎯 Účel

Systém pro správu domácích zásob v lednici, mrazáku a spíži. Sleduje:
- Co máte doma
- Množství a umístění
- **Datum expirace** - klíčové pro minimalizaci plýtvání
- Poznámky a detaily

## 📁 Soubory

### `zasoby.py`
Hlavní Python modul s logikou pro správu zásob.

**Klíčové třídy:**
- `ZasobaPolozka` - Jedna položka (vejce, sýr, atd.)
- `Lednice` - Kolekce všech zásob
- `SpravceZasob` - Správce pro práci se zásobami

**Metody:**
```python
from lednice.zasoby import SpravceZasob

# Vytvořit správce
spravce = SpravceZasob()

# Naplnit zásoby z nákupu Globus 18.1.2026
spravce.naplnit_zasoby_z_nakupu_globus_20260118()

# Vypsat inventář
spravce.vypis_inventar()

# Upozornění na expiraci
spravce.upozorneni_expirace()
```

### `INVENTORY.md`
**Human-readable** inventář vygenerovaný automaticky ze `zasoby.py`.

**Sekce:**
1. 🔴 **Prošlé** - vyhodit nebo ihned spotřebovat
2. 🟡 **Brzy vyprší (do 7 dní)** - priorita ke spotřebování
3. 🟢 **Střednědobé (8-30 dní)** - v pořádku
4. 🔵 **Dlouhodobé (nad 30 dní)** - v pořádku
5. ⚪ **Bez expirace** - trvanlivé

**Přehledy:**
- 📍 Podle umístění (lednice, mrazák, spíž, kuchyně)
- 🏷️ Podle kategorie (bilkoviny, mlecne_vyrobky, zelenina, ovoce, atd.)

## 🔄 Jak aktualizovat zásoby

### 1. Po nákupu - Python kód

Přidejte novou metodu do `SpravceZasob`:

```python
def naplnit_zasoby_z_nakupu_DATUM(self):
    """Nákup z datum."""
    dnes = date(2026, 1, 18)  # Datum nákupu
    
    self.lednice.pridat_polozku(ZasobaPolozka(
        "Vejce", 10, "ks", "bilkoviny",
        datum_nakupu=dnes,
        datum_expirace=dnes + timedelta(days=21),
        umisteni="lednice",
        poznamky="Bio vejce z farmy"
    ))
```

### 2. Generovat INVENTORY.md

Spusťte Python skript:

```python
from datetime import date, timedelta
from lednice.zasoby import SpravceZasob

# Načíst zásoby
spravce = SpravceZasob()
spravce.naplnit_zasoby_z_nakupu_globus_20260118()  # Nebo vaše metoda

# Vygenerovat MD soubor (viz script výše)
# ... generate markdown content ...

with open('lednice/INVENTORY.md', 'w', encoding='utf-8') as f:
    f.write(md_content)
```

## 📊 Ukázkové použití

### Kontrola expirace

```python
from lednice.zasoby import SpravceZasob

spravce = SpravceZasob()
spravce.naplnit_zasoby_z_nakupu_globus_20260118()

# Co brzy vyprší?
brzy_expiruji = spravce.lednice.ziskej_brzy_expiruji(dny=7)
for polozka in brzy_expiruji:
    print(f"⏰ {polozka.nazev}: {polozka.dny_do_expirace()} dní")

# Co je prošlé?
prosle = spravce.lednice.ziskej_prosle()
for polozka in prosle:
    print(f"❌ {polozka.nazev}: prošlé!")
```

### Co lze uvařit?

```python
# Mám všechny ingredience?
ingredience = ["Vejce", "Špenát", "Sýr gouda"]
muzu_uvarit = spravce.lednice.co_muzu_uvarit(ingredience)

if muzu_uvarit:
    print("✅ Můžete uvařit omeletu se špenátem!")
else:
    print("❌ Chybí ingredience")
```

### Přehled podle kategorie

```python
kategorie = spravce.lednice.ziskej_podle_kategorie()

for kat, polozky in kategorie.items():
    print(f"\n{kat.upper()}:")
    for p in polozky:
        print(f"  • {p.nazev}: {p.mnozstvi} {p.jednotka}")
```

## 🎨 Kategorie položek

- `bilkoviny` - Maso, ryby, vejce
- `mlecne_vyrobky` - Mléko, sýry, jogurty, tvarohy
- `zelenina` - Čerstvá i konzervovaná zelenina
- `ovoce` - Čerstvé i sušené ovoce
- `orechy` - Ořechy a semínka
- `tuky` - Oleje, máslo
- `sacharidy` - Rýže, těstoviny, mouka (pro Kubíka)
- `koreni` - Koření a bylinky
- `ostatni` - Ostatní položky

## 📍 Umístění

- `lednice` - Chladnička (4-8°C)
- `mrazak` - Mrazák (-18°C)
- `spiz` - Spíž, pokojová teplota
- `kuchyne` - Pracovní plocha, okno

## ⏰ Důležité termíny

### Priorita spotřebování:

1. **🔴 Prošlé** - IHNED spotřebovat nebo vyhodit
2. **🟡 Do 3 dní** - Velmi vysoká priorita
3. **🟡 Do 7 dní** - Vysoká priorita  
4. **🟢 Do 30 dní** - Střední priorita
5. **🔵 Nad 30 dní** - Nízká priorita

### Typické doby trvanlivosti:

| Položka | Trvanlivost | Umístění |
|---------|-------------|----------|
| Vejce | 21-28 dní | Lednice |
| Tvrdý sýr | 14-21 dní | Lednice |
| Cottage cheese | 5-7 dní | Lednice |
| Jogurt | 7-14 dní | Lednice |
| Čerstvá zelenina | 3-10 dní | Lednice |
| Ovoce | 7-14 dní | Lednice |
| Ořechy | 90-180 dní | Spíž |
| Oleje | 365 dní | Spíž |
| Sacharidy (rýže, mouka) | 365 dní | Spíž |

## 🔧 Údržba systému

### Týdenní úkoly:
- ✅ Zkontrolovat `INVENTORY.md` 
- ✅ Spotřebovat položky s 🟡 (do 7 dní)
- ✅ Plánovat jídla podle brzy expirujících položek

### Měsíční úkoly:
- ✅ Aktualizovat `zasoby.py` s novými nákupy
- ✅ Regenerovat `INVENTORY.md`
- ✅ Zkontrolovat prošlé položky

### Po každém nákupu:
- ✅ Přidat novou metodu `naplnit_zasoby_z_nakupu_DATUM()`
- ✅ Zahrnout všechny nakoupené položky
- ✅ Zadat správné datum expirace
- ✅ Regenerovat `INVENTORY.md`

## 💾 Automatizace (budoucnost)

Možná vylepšení:
- [ ] CLI nástroj pro přidání položek
- [ ] Automatické parsování účtenek
- [ ] Notifikace na mobil při expiraci
- [ ] Integrace s jídelníčkem (auto-plánování)
- [ ] API pro sledování spotřeby
- [ ] Dashboard s grafy

## 📝 Changelog

### 18.1.2026
- ✅ Vytvořen systém správy zásob
- ✅ Přidána metoda `naplnit_zasoby_z_nakupu_globus_20260118()`
- ✅ Vygenerován `INVENTORY.md` s 40 položkami
- ✅ Organizace podle expirace a umístění
- ✅ Dokumentace v tomto README

---

**Autor:** GitHub Copilot  
**Datum:** 18. ledna 2026  
**Status:** ✅ Funkční a připraveno k použití
