# 🧩 Modulární systém jídel

## 📋 Koncept

Modulární systém umožňuje **snadnou výměnu jídel** v jídelníčku, protože každé jídlo má standardizovanou kalorickou hodnotu podle typu.

### Základní princip

```
Typ jídla → Kalorický modul → Konkrétní jídla s podobnou kalorickou hodnotou
```

**Výhody:**
- ✅ Snadná výměna jídel stejného typu
- ✅ Automatická kontrola kalorií
- ✅ Flexibilní plánování
- ✅ Databáze alternativ
- ✅ Zachování celkového denního příjmu

## 🎯 Kalorie moduly pro Páju

Celkem: **1500 kcal/den** (rozděleno nerovnoměrně podle preferencí)

| Typ jídla | Cílové kcal | Rozmezí | Důvod |
|-----------|-------------|---------|-------|
| **Snídaně** | 400 | 350-450 | Nejvyšší hlad ráno |
| **Malá svačina** | 150 | 120-180 | Prevence hladu |
| **Oběd** | 350 | 300-400 | Menší (problém s objemem) |
| **Velká svačina** | 250 | 220-280 | Kritické okno 15-16h |
| **Večeře** | 350 | 300-400 | Sdílená s rodinou |

### Proč nerovnoměrné rozložení?

1. **Snídaně větší (400 kcal)** - Pája má nejvyšší hlad ráno
2. **Oběd menší (350 kcal)** - Problém s přejedením při velkých porcích
3. **Velká svačina (250 kcal)** - Kritické okno 15-16h vyžaduje sytící jídlo
4. **Malá svačina (150 kcal)** - Jen prevence hladu mezi jídly

## 🔧 Jak to funguje

### 1. Definice modulu

```python
from osoby.osoba_2.modularni_system import MODULY_PAJA, TypJidla

# Získat modul pro snídani
modul_snidane = MODULY_PAJA[TypJidla.SNIDANE]
print(modul_snidane)
# snídaně: 400 kcal (350-450 kcal)
```

### 2. Vytvoření jídla

```python
from osoby.osoba_2.modularni_system import ModularniJidlo, TypJidla

snidane = ModularniJidlo(
    nazev="Ovesná kaše s ovocem",
    typ=TypJidla.SNIDANE,
    kalorie=400,
    bilkoviny=25,
    sacharidy=45,
    tuky=12,
    vlaknina=8,
    syti_dobre=True,
    meal_prep_vhodne=True,
    ingredience=["ovesné vločky", "banán", "jogurt"]
)
```

### 3. Kontrola kompatibility

```python
# Je jídlo kompatibilní s modulem?
if snidane.je_kompatibilni_s_modulem(modul_snidane):
    print("✅ Jídlo odpovídá modulu snídaně")
    
# O kolik se liší od cílových kalorií?
odchylka = snidane.vypocti_odchylku_od_modulu(modul_snidane)
print(f"Odchylka: {odchylka} kcal")
```

### 4. Sestavení jídelníčku

```python
from osoby.osoba_2.modularni_system import ModularniJidelnicek

jidelnicek = ModularniJidelnicek(datum="2026-01-20")
jidelnicek.pridej_jidlo(snidane)
jidelnicek.pridej_jidlo(svacina)
jidelnicek.pridej_jidlo(obed)
jidelnicek.pridej_jidlo(svacina2)
jidelnicek.pridej_jidlo(vecere)

print(jidelnicek)
# Zobrazí kompletní jídelníček s makry
```

### 5. Výměna jídla

```python
# Vytvoř alternativní snídani
alt_snidane = ModularniJidlo(
    nazev="Vejce s avokádem",
    typ=TypJidla.SNIDANE,
    kalorie=420,
    ...
)

# Vyměň snídani
jidelnicek.vymenit_jidlo(TypJidla.SNIDANE, alt_snidane)

# Kontrola celkových kalorií
if jidelnicek.je_v_cili():
    print("✅ Stále v cíli!")
```

## 📚 Databáze jídel podle modulů

### Snídaně (400 kcal, 350-450)

| Jídlo | kcal | P | C | F | V | Tagy |
|-------|------|---|---|---|---|------|
| Ovesná kaše + ovoce + jogurt | 400 | 25 | 45 | 12 | 8 | sytící, meal_prep |
| Vejce (3ks) + avokádo + chléb | 420 | 28 | 22 | 25 | 10 | protein, rychlé |
| Proteinové palačinky + borůvky | 380 | 30 | 40 | 10 | 6 | sytící, sladké |
| Tvaroh + ovoce + ořechy | 410 | 28 | 35 | 18 | 7 | protein, meal_prep |

### Malá svačina (150 kcal, 120-180)

| Jídlo | kcal | P | C | F | V | Tagy |
|-------|------|---|---|---|---|------|
| Jablko + hrst mandlí | 150 | 4 | 18 | 8 | 4 | rychlé, přenosné |
| Jogurt + chia semínka | 160 | 12 | 15 | 6 | 5 | protein, krabička |
| Mrkev + hummus | 140 | 5 | 20 | 5 | 6 | zelenina, dip |
| Tvarohová pomazánka + zelenina | 130 | 15 | 8 | 4 | 3 | protein, lehké |

### Oběd (350 kcal, 300-400)

| Jídlo | kcal | P | C | F | V | Tagy |
|-------|------|---|---|---|---|------|
| Luštěniny + cuketa + semínka | 350 | 20 | 40 | 10 | 12 | sytící, vláknina |
| Kuřecí salát s quinoou | 380 | 35 | 30 | 12 | 6 | protein, lehké |
| Čočková polévka + celozrnný chléb | 320 | 18 | 45 | 8 | 10 | teplé, sytící |
| Rybí filé + zelenina | 340 | 38 | 20 | 12 | 5 | protein, omega-3 |

### Velká svačina (250 kcal, 220-280)

| Jídlo | kcal | P | C | F | V | Tagy |
|-------|------|---|---|---|---|------|
| Řecký jogurt + ovoce | 250 | 20 | 25 | 8 | 3 | protein, rychlé |
| Ovesné vločky + ořechy | 260 | 12 | 35 | 10 | 7 | vláknina, sytící |
| Tvaroh + ovoce | 240 | 22 | 28 | 5 | 4 | protein, sladké |
| Proteinový smoothie | 270 | 25 | 30 | 8 | 5 | tekuté, rychlé |

### Večeře (350 kcal, 300-400)

| Jídlo | kcal | P | C | F | V | Tagy |
|-------|------|---|---|---|---|------|
| Kuřecí prsa + brokolice | 350 | 45 | 15 | 12 | 5 | protein, lehké |
| Losos + zelená fazolka | 380 | 38 | 18 | 16 | 6 | omega-3, rodinné |
| Krůtí maso + květák | 340 | 42 | 20 | 10 | 6 | protein, meal_prep |
| Tofu + zelenina wok | 320 | 25 | 28 | 12 | 7 | vegetariánské |

## 🔄 Praktické použití

### Scénář 1: Změna preference

**Situace:** Pája už nechce ovesnou kaši  
**Řešení:** Vyměň za jiné jídlo typu SNIDANE (400 kcal)

```python
# Místo kaše dej vejce s avokádem
jidelnicek.vymenit_jidlo(
    TypJidla.SNIDANE,
    vejce_s_avokadem  # 420 kcal - stále v rozmezí 350-450
)
```

### Scénář 2: Meal prep na týden

**Cíl:** Připravit 4 snídaně dopředu

```python
# Vyfiltruj jídla vhodná pro meal prep
meal_prep_snidane = [
    j for j in databaze_jidel 
    if j.typ == TypJidla.SNIDANE 
    and j.meal_prep_vhodne
    and j.je_kompatibilni_s_modulem(MODULY_PAJA[TypJidla.SNIDANE])
]

# Vyber jedno a použij 4x
```

### Scénář 3: Automatické generování jídelníčku

```python
def vygeneruj_tydenni_jidelnicek(databaze):
    """Vygeneruje týdenní jídelníček s různými jídly."""
    
    tyden = []
    for den in range(7):
        jidelnicek = ModularniJidelnicek(datum=f"Den {den+1}")
        
        # Pro každý typ jídla vyber náhodně z databáze
        for typ in TypJidla:
            # Vyfiltruj kompatibilní jídla
            kompatibilni = [
                j for j in databaze[typ]
                if j.je_kompatibilni_s_modulem(MODULY_PAJA[typ])
            ]
            
            # Vyber náhodně (nebo podle preferencí)
            jidlo = random.choice(kompatibilni)
            jidelnicek.pridej_jidlo(jidlo)
        
        # Kontrola cíle
        if jidelnicek.je_v_cili():
            tyden.append(jidelnicek)
    
    return tyden
```

## ⚙️ Integrace s existujícím systémem

### S preference.py

```python
from osoby.osoba_2.preference import SyticiJidla, ProblematickaJidla

# Při vytváření jídla nastav značky
jidlo = ModularniJidlo(
    nazev="Kaše s ovocem",
    ...
    syti_dobre=SyticiJidla.je_jidlo_sytici("kaše s ovocem"),
    problematicke=ProblematickaJidla.je_jidlo_problematicke("kaše s ovocem")
)
```

### S profil_komplexni.py

```python
from osoby.osoba_2.profil_komplexni import KomplexniProfilPaji

profil = KomplexniProfilPaji()

# Kalorie moduly podle profilu
# - Snídaně větší (nejvyšší hlad ráno)
# - Oběd menší (problém s objemem)
# - Velká svačina (kritické okno 15-16h)
```

## 🎨 Možná rozšíření

### 1. Automatické doporučení

```python
def doporuc_jidlo(typ: TypJidla, preference: List[str]) -> ModularniJidlo:
    """
    Doporučí jídlo podle preferencí.
    
    Args:
        typ: Typ jídla (SNIDANE, OBED, ...)
        preference: Seznam tagů ("sytící", "rychlé", "meal_prep")
    """
    pass
```

### 2. Nákupní seznam

```python
def vytvor_nakupni_seznam(jidelnicek: ModularniJidelnicek) -> List[str]:
    """Vytvoří nákupní seznam ze všech ingrediencí."""
    ingredience = set()
    for jidlo in jidelnicek.jidla.values():
        ingredience.update(jidlo.ingredience)
    return sorted(ingredience)
```

### 3. Rozpočtová optimalizace

```python
@dataclass
class ModularniJidlo:
    ...
    cena_pripravy: float = 0.0  # Kč
    
def optimalizuj_podle_rozpoctu(databaze, max_cena_den: float):
    """Vybere nejlevnější jídla v rámci modulů."""
    pass
```

### 4. Týdenní rotace

```python
def vytvor_tydenni_rotaci(databaze, preferuj_varietu=True):
    """
    Vytvoří týdenní jídelníček s různými jídly.
    Žádné jídlo se neopakuje 2x za týden.
    """
    pass
```

## 📝 Shrnutí

### Co máš teď:

✅ Systém modulárních jídel  
✅ Standardizované kalorické hodnoty  
✅ Snadná výměna jídel  
✅ Automatická kontrola kalorií  
✅ Ukázková databáze jídel  

### Jak používat:

1. **Vytvoř jídla** podle modulů (snídaně 400 kcal, svačina 150 kcal, atd.)
2. **Sestav jídelníček** z modulárních jídel
3. **Vyměň jídla** podle potřeby (únava, preference, dostupnost)
4. **Systém automaticky kontroluje** celkové kalorie

### Příklady:

```bash
# Spusť demo
python osoby/osoba_2/modularni_system.py

# Zobrazí:
# - Kalorie moduly
# - Ukázkový jídelníček
# - Výměnu jídla
# - Kontrolu kalorií
```

---

**Vytvořeno:** 2026-01-18  
**Pro:** Pája (osoba_2)  
**Cílové kalorie:** 1508 kcal/den (zaokrouhleno na 1500)
