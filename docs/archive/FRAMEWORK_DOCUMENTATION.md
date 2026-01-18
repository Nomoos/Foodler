# 📚 Modular Meal & Supplement System – Framework Documentation

## Přehled

Tento dokument popisuje kompletní framework pro správu jídel, suplementů a tělesných metrik pro více osob v rodině s různými potřebami.

**Datum vytvoření:** 2026-01-18  
**Verze:** 1.0  
**Autor:** GitHub Copilot pro Foodler

---

## 🎯 Účel Framework

Framework řeší následující problémy:
- **Škálovatelnost** - Snadné přidání nových členů rodiny
- **Flexibilita** - Každý člen má vlastní požadavky
- **Sdílení** - Společná knihovna jídel a suplementů
- **Validace** - Automatická kontrola konzistence
- **Historie** - Sledování tělesných metrik v čase

---

## 🏗️ Architektura

### Základní principy

1. **Každá osoba má vlastní modulární systém**
2. **Rodina je kolekce nezávislých systémů**
3. **Jídla jsou stavěna ze znovupoužitelných modulů**
4. **Suplementy jsou rule-based, ne hardcoded**
5. **Konzistence je validována automaticky**
6. **Tělesné metriky jsou časově ohraničená fakta**

---

## 📦 Hlavní komponenty

### 1. Family Structure

```python
class Family:
    family_id: str
    nazev: str
    members: Dict[str, PersonProfile]
    module_library: ModuleLibrary
    supplement_catalog: SupplementCatalog
    day_templates: Dict[str, DayTemplate]
    kdo_vari: Optional[str]  # ID osoby
    kdo_nakupuje: Optional[str]  # ID osoby
```

**Příklad:**
```python
rodina = Family(
    family_id="foodler_family",
    nazev="Rodina Foodler",
    kdo_vari="roman",
    kdo_nakupuje="roman"
)
```

### 2. Person Profile

```python
class PersonProfile:
    id: str
    jmeno: str
    vek_kategorie: VekKategorie  # DITE / DOSPELY
    daily_targets: DailyTargets
    pocet_jidel: int
    day_template_id: str
    dietni_omezeni: List[str]
    supplement_pack_ids: List[str]
    body_metrics: BodyMetricsHistory
    poznamky: List[str]
```

**Příklad:**
```python
roman = PersonProfile(
    id="roman",
    jmeno="Roman",
    vek_kategorie=VekKategorie.DOSPELY,
    daily_targets=DailyTargets(
        kalorie=2001,
        bilkoviny=140.0,
        sacharidy=70.0,
        tuky=129.0,
        vlaknina=20.0
    ),
    pocet_jidel=6,
    day_template_id="roman_6meals",
    dietni_omezeni=["low-carb", "keto"]
)
```

### 3. Body Metrics (Time-Based)

Tělesné metriky jsou historická fakta, ne předpoklady.

```python
class BodyMetric:
    metric_type: str  # "weight", "height", "body_fat"
    value: float
    unit: str  # "kg", "cm", "%"
    measured_at: date
    poznamka: Optional[str]
```

**Příklad:**
```python
# Přidání měření váhy
profil.body_metrics.pridej_mereni(BodyMetric(
    metric_type="weight",
    value=17.0,
    unit="kg",
    measured_at=date(2026, 1, 18),
    poznamka="Aktuální měření"
))

# Získání poslední váhy
vaha = profil.posledni_vaha()  # 17.0 kg
```

### 4. Day Template System

Definuje, jak je den rozdělen na jídelní sloty.

```python
class DayTemplate:
    template_id: str
    nazev: str
    pocet_jidel: int
    typ_rozlozeni: TypRozlozeni  # ROVNOMERNE / NEROVNOMERNE / SKOLNI_REZIM
    sloty: List[Slot]

class Slot:
    slot_id: str
    slot_type: TypJidla
    vaha: float  # 0-1 podíl denních cílů
    casove_okno: Optional[Tuple[str, str]]
    omezeni_slotu: List[str]
    povolene_tagy: List[str]
    poznamka: Optional[str]
```

**Příklad - Nerovnoměrné rozložení pro Páju:**
```python
template = DayTemplate(
    template_id="paja_5meals",
    nazev="Pája - 5 jídel nerovnoměrně",
    pocet_jidel=5,
    typ_rozlozeni=TypRozlozeni.NEROVNOMERNE
)

# Větší snídaně (27% - nejvyšší hlad ráno)
template.pridej_slot(Slot(
    slot_id="p_snidane",
    slot_type=TypJidla.SNIDANE,
    vaha=0.27,
    casove_okno=("06:00", "06:30"),
    povolene_tagy=["sytici", "vlaknina"],
    poznamka="Nejvyšší hlad ráno - větší porce"
))

# Menší oběd (23% - citlivost na objem)
template.pridej_slot(Slot(
    slot_id="p_obed",
    slot_type=TypJidla.OBED,
    vaha=0.23,
    casove_okno=("12:00", "13:00"),
    povolene_tagy=["lehke", "vlaknina"],
    poznamka="Menší porce - citlivost na objem"
))
```

### 5. Meal Modules

Znovupoužitelné jídelní stavební bloky.

```python
class MealModule:
    id: str
    nazev: str
    makra: Makra  # kalorie, protein, carbs, fats, fiber
    tagy: List[str]
    omezeni: List[str]  # "gluten-free", "lactose-free"
    prep_level: PrepLevel
    zavislosti: List[str]  # ID jiných modulů
    je_addon: bool  # Je to doplněk?
    poznamky: Optional[str]
```

**Příklad:**
```python
# Základní modul
kase = MealModule(
    id="ovsena_kase",
    nazev="Ovesná kaše",
    makra=Makra(
        kalorie=300,
        bilkoviny=10.0,
        sacharidy=50.0,
        tuky=6.0,
        vlaknina=8.0
    ),
    tagy=["sytici", "vlaknina", "meal-prep"],
    prep_level=PrepLevel.MINIMALNI
)

# Add-on modul
protein_addon = MealModule(
    id="protein_powder",
    nazev="Proteinový prášek",
    makra=Makra(
        kalorie=100,
        bilkoviny=20.0,
        sacharidy=2.0,
        tuky=1.0,
        vlaknina=0.0
    ),
    tagy=["protein", "addon"],
    je_addon=True
)
```

### 6. Supplement System

#### 6.1 Supplement Definition

```python
class SupplementDefinition:
    id: str
    nazev: str
    davka: str
    timing_pravidla: List[str]  # "ráno", "s jídlem", "večer"
    podminky: List[str]  # "nalačno", "30min před jídlem"
    konflikty: List[str]  # ID jiných suplementů
    poznamka: Optional[str]
```

**Příklad:**
```python
letrox = SupplementDefinition(
    id="letrox",
    nazev="Letrox",
    davka="dle předpisu",
    timing_pravidla=["ráno", "nalačno"],
    podminky=["5:35", "30 min před jídlem"],
    poznamka="Štítná žláza - DŮLEŽITÉ načasování!"
)
```

#### 6.2 Supplement Packs

Logické seskupení suplementů.

```python
class SupplementPack:
    pack_id: str
    nazev: str
    suplementy: List[str]  # ID suplementů
    povolene_sloty: List[str]  # ID slotů
    pravidla_typu_dne: List[TypDne]
    poznamka: Optional[str]
```

**Příklad:**
```python
paja_am = SupplementPack(
    pack_id="paja_am",
    nazev="Pája - Ranní balíček (5:35!)",
    suplementy=["letrox", "vitamin_d_p", "omega3_p", "magnesium_p"],
    povolene_sloty=["p_snidane"],
    pravidla_typu_dne=[TypDne.PRACOVNI, TypDne.VIKEND],
    poznamka="Letrox v 5:35, ostatní v 5:36!"
)
```

---

## 🔄 Workflow použití

### 1. Vytvoření rodiny

```python
# 1. Vytvoř rodinu
rodina = Family(
    family_id="foodler_family",
    nazev="Rodina Foodler",
    kdo_vari="roman",
    kdo_nakupuje="roman"
)

# 2. Vytvoř templates
rodina.pridej_template(vytvor_template_roman())
rodina.pridej_template(vytvor_template_paja())
rodina.pridej_template(vytvor_template_kubik())

# 3. Naplň supplement catalog
rodina.supplement_catalog = vytvor_supplement_catalog()

# 4. Přidej členy
rodina.pridej_clena(vytvor_profil_roman())
rodina.pridej_clena(vytvor_profil_paja())
rodina.pridej_clena(vytvor_profil_kubik())
```

### 2. Validace

```python
# Validuj všechny členy
validace = rodina.validuj_vsechny_cleny()

for member_id, (je_validni, chyba) in validace.items():
    if not je_validni:
        print(f"❌ {member_id}: {chyba}")
```

### 3. Získání přehledu

```python
# Celková rodina
print(f"Celkové kalorie: {rodina.ziskej_celkove_kalorie()} kcal")
print(f"Celkový počet jídel: {rodina.ziskej_celkovy_pocet_jidel()}")
print(f"Celkový počet suplementů: {rodina.ziskej_celkovy_pocet_suplementu()}")

# Detail člena
for member in rodina.members.values():
    print(member)
    template = rodina.day_templates[member.day_template_id]
    for slot in template.sloty:
        cil_kcal = int(member.daily_targets.kalorie * slot.vaha)
        print(f"  {slot.slot_type.value}: {cil_kcal} kcal")
```

---

## 📊 Implementace pro Foodler Family

### Aktuální stav

```
RODINA: Rodina Foodler
======================================================================
Členové: 3
Celkové kalorie: 4909 kcal/den
Celkový počet jídel: 16 jídel/den
Celkový počet suplementů: 13 suplementů/den
Vaří: Roman (Romča)
Nakupuje: Roman (Romča)
```

### Roman (Romča)
- **6 jídel denně** - rovnoměrné rozložení
- **2001 kcal** | P140g C70g F129g V20g
- **Váha:** 133.6 kg (18.1.2026)
- **Suplementy:** Omeprazol, léky na tlak, multivitamin, omega-3, vitamin D, probiotika
- **Role:** Vaří a nakupuje pro celou rodinu

### Pája (Pavla)
- **5 jídel denně** - nerovnoměrné rozložení
- **1508 kcal** | P92g C60g F100g V20g
- **Váha:** 77.3 kg (22.12.2025)
- **Suplementy:** Letrox (5:35!), antikoncepce, vitamin D, omega-3, magnesium
- **Speciální:** Větší snídaně (27%), menší oběd (23%), kritické okno 15-16h

### Kubík
- **5 jídel denně** - školní režim (2 doma, 3 školka)
- **1400 kcal** | P19g C130g F47g V18g
- **Váha:** 17.0 kg (18.1.2026)
- **Suplementy:** Vitamin A (zrak!), Omega-3 DHA
- **Speciální:** Více sacharidů než dospělí, důraz na vitamin A

---

## ✅ Výhody Framework

### 1. Škálovatelnost
- ✅ Snadné přidání nového člena rodiny
- ✅ Různé počty jídel pro každého
- ✅ Různé kalorie a makro cíle

### 2. Flexibilita
- ✅ Vlastní day templates
- ✅ Individuální supplement packs
- ✅ Vlastní dietní omezení

### 3. Sdílení
- ✅ Společná knihovna meal modulů
- ✅ Společný katalog suplementů
- ✅ Znovupoužitelné komponenty

### 4. Validace
- ✅ Automatická kontrola konzistence
- ✅ Validace day templates (součet vah = 1.0)
- ✅ Detekce konfliktů suplementů

### 5. Historie
- ✅ Časově ohraničené body metrics
- ✅ Sledování váhy v čase
- ✅ Ne hardcoded předpoklady

---

## 🚀 Další kroky

### Fáze 1: Naplnění knihoven ✅
- [x] Framework core implementován
- [x] Person profiles vytvořeny
- [x] Day templates definovány
- [x] Supplement catalog naplněn
- [x] Body metrics implementovány

### Fáze 2: Meal Modules (TODO)
- [ ] Naplnit ModuleLibrary základními jídly
- [ ] Vytvořit add-on moduly
- [ ] Implementovat meal assembly logiku
- [ ] Vytvořit databázi receptů

### Fáze 3: Automatizace (TODO)
- [ ] Automatické generování jídelníčků
- [ ] Target allocation logic
- [ ] Meal assembly logic
- [ ] Supplement assignment logic

### Fáze 4: Integrace (TODO)
- [ ] Integrace s existujícím kódem
- [ ] Migrace starého systému
- [ ] Vytvoření meal prep plánů
- [ ] Generování nákupních seznamů

---

## 📁 Soubory

### Core Framework
- `framework_core.py` - Základní třídy a enums
- `framework_implementation.py` - Implementace pro Foodler family
- `FRAMEWORK_DOCUMENTATION.md` - Tento dokument

### Legacy (k migraci)
- `modularni_system_rodina.py` - Starý systém (nahrazen frameworkem)
- `osoby/osoba_2/modularni_system.py` - Pája-specific (k integraci)

### Související
- `osoby/osoba_*/profil.py` - Původní profily
- `osoby/osoba_2/preference.py` - Preference Páji
- `osoby/osoba_2/profil_komplexni.py` - Komplexní profil Páji

---

## 🔧 Příklady použití

### Přidání nového člena

```python
# 1. Vytvoř day template
novy_template = DayTemplate(
    template_id="new_member_template",
    nazev="Nový člen - 4 jídla",
    pocet_jidel=4,
    typ_rozlozeni=TypRozlozeni.ROVNOMERNE
)
# ... přidej sloty ...

# 2. Vytvoř profil
novy_clen = PersonProfile(
    id="new_member",
    jmeno="Nový člen",
    vek_kategorie=VekKategorie.DOSPELY,
    daily_targets=DailyTargets(kalorie=1800),
    pocet_jidel=4,
    day_template_id="new_member_template"
)

# 3. Přidej do rodiny
rodina.pridej_template(novy_template)
rodina.pridej_clena(novy_clen)

# 4. Validuj
validace = rodina.validuj_vsechny_cleny()
```

### Změna váhy

```python
# Přidej nové měření
kubik = rodina.members["kubik"]
kubik.body_metrics.pridej_mereni(BodyMetric(
    metric_type="weight",
    value=17.5,
    unit="kg",
    measured_at=date(2026, 2, 1)
))

# Získej historii
posledni_vaha = kubik.posledni_vaha()  # 17.5 kg
```

### Vytvoření supplement pack

```python
# Definuj suplementy
catalog.pridej_suplement(SupplementDefinition(
    id="new_supp",
    nazev="Nový suplement",
    davka="1 tableta",
    timing_pravidla=["ráno"]
))

# Vytvoř pack
catalog.pridej_balicek(SupplementPack(
    pack_id="new_pack",
    nazev="Nový balíček",
    suplementy=["new_supp"],
    povolene_sloty=["r_snidane"]
))

# Přiřaď osobě
roman.supplement_pack_ids.append("new_pack")
```

---

## 📞 Support

Pro další informace nebo pomoc:
- Dokumentace: `FRAMEWORK_DOCUMENTATION.md`
- Příklady: `framework_implementation.py`
- Tests: TBD

---

**Vytvořeno:** 2026-01-18  
**Framework Version:** 1.0  
**Status:** ✅ Production Ready (Core)  
**Next:** Meal Assembly Logic
