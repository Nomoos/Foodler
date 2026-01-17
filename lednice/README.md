# Lednice

Tento modul spravuje **domácí zásoby** - sleduje potraviny v lednici, mrazáku a spíži.

## Obsah

- `zasoby.py` - Správa zásob, sledování expirace a inventář

## Použití

```python
from lednice.zasoby import SpravceZasob, ZasobaPolozka
from datetime import date, timedelta

# Vytvoření správce zásob
spravce = SpravceZasob()

# Přidání položky do lednice
dnes = date.today()
spravce.lednice.pridat_polozku(ZasobaPolozka(
    nazev="Kuřecí prsa",
    mnozstvi=500,
    jednotka="g",
    kategorie="bilkoviny",
    datum_nakupu=dnes,
    datum_expirace=dnes + timedelta(days=3),
    umisteni="lednice"
))

# Výpis inventáře
spravce.vypis_inventar()

# Upozornění na expiraci
spravce.upozorneni_expirace()

# Kontrola, zda lze uvařit jídlo
ingredience = ["Kuřecí prsa", "Brokolice", "Olivový olej"]
muzu_uvarit = spravce.lednice.co_muzu_uvarit(ingredience)

if muzu_uvarit:
    print("✅ Můžete uvařit!")
else:
    print("❌ Chybí ingredience")

# Odebrání použité potraviny
spravce.lednice.odebrat_polozku("Kuřecí prsa", 200, "lednice")
```

## Funkce

### Správa zásob
- Přidávání/odebírání položek
- Sledování množství
- Aktualizace stavu (otevřeno/neotevřeno)

### Umístění
- **lednice** - Čerstvé potraviny
- **mrazak** - Zmrazené potraviny
- **spiz** - Trvanlivé potraviny

### Sledování expirace
- Automatická kontrola čerstvosti
- Upozornění na blížící se expiraci (3 dny)
- Seznam prošlých položek

### Inventář
- Zobrazení podle umístění
- Zobrazení podle kategorií
- Celková hodnota zásob

### Plánování vaření
- Kontrola dostupnosti ingrediencí
- Návrhy na jídla podle dostupných surovin

## Kategorie položek

- **bilkoviny** - Maso, ryby, vejce
- **mlecne_vyrobky** - Tvaroh, jogurt, sýr
- **zelenina** - Brokolice, špenát, cuketa, atd.
- **tuky** - Oleje, máslo
- **orechy** - Mandle, vlašské ořechy, semínka
- **koreni** - Koření, bylinky

## Upozornění

⚠️ **Expirační datum** - Systém automaticky upozorní na položky, které brzy vyprší nebo již prošly.

🟡 **Brzy vyprší** - Položky, které vyprší do 3 dnů  
🔴 **Prošlé** - Položky s prošlým datem expirace
