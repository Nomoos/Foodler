# Osoby - Personalizované profily

Tato složka obsahuje osobní profily a preference pro jednotlivé osoby v rodině.

## Struktura

```
osoby/
├── osoba_1/              # Profil muže (135kg, 183cm)
│   ├── profil.py         # Antropometrie a cíle
│   └── preference.py     # Preference jídel a omezení
├── osoba_2/              # Profil ženy (80kg, 170cm)
│   ├── profil.py         # Antropometrie a cíle
│   └── preference.py     # Preference jídel a omezení
├── osoba_3/              # Profil dítěte (Kubík, 4.5 let)
│   ├── profil.py         # Dětské výživové potřeby
│   └── preference.py     # Dětská strava + podpora zraku
└── sdilena_jidla/        # Sdílená jídla pro celou rodinu
    └── jidla.py          # Recepty a meal prep plány
```

## Použití

### Zobrazení profilu

```python
from osoby.osoba_1.profil import OsobniProfil

profil = OsobniProfil()
print(profil)
```

### Kontrola preferencí

```python
from osoby.osoba_1.preference import PreferenceJidel

# Zkontrolovat, zda je jídlo vhodné
vhodne = PreferenceJidel.je_jidlo_vhodne("Kuřecí s brokolicí")

# Filtrovat seznam jídel
jidla = ["Kuřecí prsa", "Žampionová omáčka", "Losos"]
filtrovana = PreferenceJidel.filtruj_jidla(jidla)
```

### 📋 Personalizační dotazník (Pája - osoba_2)

Pro lepší přizpůsobení jídelníčku je k dispozici podrobný dotazník:

```bash
# Zobrazit seznam otázek
python osoby/osoba_2/dotaznik_paja.py --seznam

# Spustit interaktivní dotazník
python osoby/osoba_2/dotaznik_paja.py
```

**Dokumentace dotazníku:**
- `osoby/osoba_2/DOTAZNIK_OTAZKY.md` - 62 otázek v přehledném formátu
- `osoby/osoba_2/README_DOTAZNIK.md` - Návod k použití
- `osoby/osoba_2/PRIKLAD_DOPORUCENI.md` - Ukázka personalizovaných doporučení

**Kategorie otázek:**
- Životní styl a denní rutina (14 otázek)
- Časové preference (5 otázek)
- Jídelní preference (9 otázek)
- Zdravotní cíle (12 otázek)
- Praktická omezení (12 otázek)
- Emoční stravování (9 otázek)

### Sdílená jídla

```python
from osoby.sdilena_jidla.jidla import SdilenaJidla, RodinnePlanovani

# Najít meal prep jídla
meal_prep = SdilenaJidla.najdi_meal_prep_jidla()

# Získat týdenní plán
plan = RodinnePlanovani.doporuc_tydenni_plan()

# Vygenerovat nákupní seznam
seznam = RodinnePlanovani.vypocti_nakupni_seznam_pro_tyden()
```

## Společné preference

- **Bez hub a slizké konzistence**: Obě dospělé osoby nepreferují houby a produkty s kluzkou/slizkou texturou (okra, lilek, řasy, apod.)
- **Ketogenní dieta**: Pro dospělé - nízký příjem sacharidů, vysoký příjem bílkovin a tuků
- **Meal prep**: Zaměření na jídla vhodná pro přípravu dopředu

## Profil dítěte (osoba_3 - Kubík)

Kubík má speciální výživové potřeby:

- **Věk**: 4.5 let (narozen 1.1.2021)
- **Váha**: 18 kg (ideální: 17 kg)
- **Zdravotní specifika**: Brýle 4 dioptrie + astigmatismus
- **Stravovací režim**:
  - Pracovní dny: Snídaně a večeře doma, svačiny a oběd ve školce
  - Víkend: Všechna jídla doma
- **Důraz na podporu zraku**: 
  - Potraviny bohaté na vitamin A (mrkev, sladké brambory, dýně)
  - Beta-karoten z oranžové a zelené zeleniny
  - Omega-3 z ryb (losos, tuňák)
  - Luteín ze špenátu a brokolice

### Použití profilu dítěte

```python
from osoby.osoba_3.profil import DetskyyProfil

# Zobrazit profil
profil = DetskyyProfil()
print(profil)

# Získat rozložení jídel v pracovní den
pracovni_den = profil.ziskej_rozlozeni_pracovni_den()

# Získat rozložení jídel o víkendu
vikend = profil.ziskej_rozlozeni_vikend()
```

```python
from osoby.osoba_3.preference import PreferenceJidel, DietniOmezeni

# Kontrola jídla na podporu zraku
obsahuje_podporu = PreferenceJidel.obsahuje_podporu_zraku("Mrkev s lososem")

# Kontrola jídla s texturovými preferencemi
from osoby.osoba_1.preference import PreferenceJidel as Osoba1Preference
vhodne = Osoba1Preference.je_jidlo_vhodne("Žampionová omáčka")  # False - obsahuje slizkou texturu
vhodne = Osoba1Preference.je_jidlo_vhodne("Žampionová omáčka", kontrolovat_texturu=False)  # False - stále v NEPREFERRED_FOODS

# Získat týdenní plán
tydenni_plan = DietniOmezeni.navrhni_jidla_pro_tyden()

# Vytvořit nákupní seznam
nakup = DietniOmezeni.vytvor_nakupni_seznam()
```

## Přizpůsobení

Pro přidání nové osoby:

1. Vytvořte novou složku `osoba_X/`
2. Zkopírujte `profil.py` a `preference.py` z existující osoby
3. Upravte hodnoty podle potřeb nové osoby
