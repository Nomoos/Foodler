# ✅ Kompletní vyřešení úkolů z dotazníků

## 📋 Původní zadání

```
[] Zpracuj DOTAZNIK_OTAZKY.md pro všechny osoby
[] Sestav doporučení
[] Zkus zvážit co budeme potřebovat za potraviny a nádoby na meal prep
[] Shrň mi nákupní plán
[] Vytvoř nákupní seznam do Globusu
[] Získej personalizovaná doporučení
```

## ✅ Status všech úkolů

### ✅ 1. Zpracování DOTAZNIK_OTAZKY.md pro všechny osoby

**Stav**: HOTOVO

**Co bylo zpracováno**:

#### 👤 Roman (Romča)
- **Dotazník**: `osoby/osoba_1/DOTAZNIK_OTAZKY.md` (67 otázek)
- **Python verze**: `osoby/osoba_1/dotaznik_roman.py`
- **Demo**: `demo_dotaznik_roman.py`
- **Status**: ✅ Kompletně vyplněný a zpracovaný
- **Profil**:
  - Váha: 134.2 kg → Cíl: 95 kg
  - Denní potřeba: 2000 kcal | 140g P / 70g C / 129g F
  - Meal prep: Neděle 3 hodiny
  - Rozpočet: 2500-3000 Kč/týden

#### 👤 Pája
- **Dotazník**: `osoby/osoba_2/DOTAZNIK_OTAZKY.md` (62 otázek)
- **Python verze**: `osoby/osoba_2/dotaznik_paja.py`
- **Demo**: `demo_dotaznik_paja.py`
- **Status**: ✅ Kompletně vyplněný a zpracovaný
- **Profil**:
  - Váha: 77.3 kg → Cíl: 57 kg
  - Denní potřeba: 1508 kcal | 92g P / 60g C
  - Role: Pomáhá s úklidem během meal prepu
  - Emoční faktory: Stress eating, preferuje připravené svačiny

#### 👶 Kubík
- **Profil**: `osoby/osoba_3/profil.py` (DetskyyProfil class)
- **Status**: ✅ Profil existuje a je kompletní
- **Poznámka**: Pro předškolní dítě není potřeba klasický dotazník, ale profil s výživovými potřebami
- **Profil**:
  - Věk: 4.5 let, Váha: 17 kg
  - Denní potřeba: 1400 kcal | 19g P / 130g C / 47g F
  - Specifika: Brýle (4 dioptrie), potřeba vitamin A pro zrak, vláknina pro trávení
  - Oblíbené: Sýr, mrkev, fíky

---

### ✅ 2. Sestavení doporučení

**Stav**: HOTOVO

**Vytvořeno**: Personalizovaná doporučení pro každou osobu v `zpracuj_dotazniky_a_vytvor_plan.py`

#### 👤 Roman - Top 5 doporučení:

1. **MEAL PREP**: Neděle 14:00-17:00 - 3 hodiny batch cooking
   - Připrav 14 obědů + 14 večeří na celý týden
   - Použij tlakový hrnec, troubu a airfryer současně

2. **PROTEINY FIRST**: Začni každé jídlo bílkovinou
   - Cíl: 140g bílkovin denně (32% energie)

3. **LOW-CARB**: Maximálně 70g sacharidů denně
   - Eliminuj těstoviny, chléb, brambory, rýži

4. **NÁKUPY**: Sobota ráno - kontrola slev na Kupi.cz
   - Nakup ve 2-3 obchodech podle akcí

5. **JEDNODUCHOST**: Preferuj recepty s 3-5 ingrediencemi
   - Udržitelnost > dokonalost

#### 👤 Pája - Top 5 doporučení:

1. **KALORICKÝ DEFICIT**: 1508 kcal denně
   - Cíl: 77.3 kg → 57 kg za 6-12 měsíců

2. **PROTEINY**: 92g denně pro udržení svalové hmoty

3. **EMOČNÍ STRAVOVÁNÍ**: Připravené zdravé svačiny
   - Při stresu mít po ruce zeleninu, ořechy

4. **HORMONÁLNÍ PODPORA**: Kvalitní tuky a omega-3
   - Avokádo, losos, ořechy, olivový olej (podpora libida)

5. **SPOLUPRÁCE**: Úklid během meal prepu
   - Společné hubnutí s Romanem = motivace

#### 👶 Kubík - Zdravotní priority:

1. **VITAMIN A**: Mrkev, dýně, sladké brambory, špenát (pro zrak)
2. **OMEGA-3**: Losos, makrela 1-2x týdně (mozek a oči)
3. **VLÁKNINA**: Ovoce, zelenina, celozrnné pečivo (trávení, zácpa)
4. **VODA**: Minimálně 1.3l denně

---

### ✅ 3. Plánování potravin a nádob na meal prep

**Stav**: HOTOVO

**Výstup**: Kompletní analýza v `zpracuj_dotazniky_a_vytvor_plan.py` (KROK 3)

#### 📊 Týdenní nutriční potřeby:

| Osoba | Kalorie/týden | Jídel týdně | Poznámka |
|-------|---------------|-------------|----------|
| Roman | 14,000 kcal | 42 jídel | 6 jídel denně |
| Pája | 10,556 kcal | 35 jídel | 5 jídel denně |
| Kubík | 9,800 kcal | 20 jídel | Pouze doma (snídaně + večeře všední den, vše víkend) |
| **CELKEM** | **34,356 kcal** | **97 jídel** | |

#### 🥘 Potřebné potraviny (týdenní):

**PROTEINY**:
- Kuřecí prsa: 2.5 kg
- Mleté maso: 1.5 kg
- Ryby (losos/makrela): 800g
- Vejce: 30 ks
- Tvaroh: 1.5 kg
- Řecký jogurt: 1 kg
- Sýry: 600g

**ZELENINA**:
- Brokolice: 2 kg
- Špenát: 1 kg
- Paprika: 1.5 kg
- Rajčata: 1 kg
- Okurky: 1 kg
- Salát: 500g
- Mrkev (vitamin A pro Kubíka): 1 kg

**PRO KUBÍKA**:
- Ovoce mix (banány, pomeranče, mango)
- Rýže/těstoviny: 500g
- Celozrnný chléb: 1 bochník
- Jogurty/kefír: 1l
- Sýr: 300g

**TUKY**:
- Olivový olej: 500ml
- Avokádo: 5 ks
- Ořechy: 500g
- Semínka: 200g

#### 🥡 Potřebné nádoby:

**MEAL PREP KRABIČKY**:
- Velké (obědy): **14 ks** (7 dní x 2 osoby)
- Střední (večeře): **14 ks**
- Malé (svačiny): **20 ks**
- Skleničky (chia pudding, jogurt): **10 ks**
- **CELKEM**: **58 nádob**

**VAKUOVACÍ SÁČKY**:
- Pro maso (před vařením): **10 ks**
- Pro hotová jídla (mražení): **20 ks**
- **CELKEM**: **30 sáčků**

**DALŠÍ VYBAVENÍ**:
- Pečicí plechy: 2 ks (batch cooking)
- Velké hrnce: 2 ks (tlakový + klasický)
- Airfryer
- Mixér
- Kuchyňská váha

---

### ✅ 4. Shrnutí nákupního plánu

**Stav**: HOTOVO

**Výstup**: Detailní rozpis v `zpracuj_dotazniky_a_vytvor_plan.py` (KROK 4)

#### 💰 Rozpis podle kategorií:

| Kategorie | Cena | Obchod |
|-----------|------|--------|
| **PROTEINY** | 1370 Kč | Lidl, Kaufland, Penny, Makro |
| Kuřecí prsa (2.5 kg) | 400 Kč | Lidl/Kaufland |
| Mleté maso (1.5 kg) | 200 Kč | Penny |
| Losos/makrela (800g) | 250 Kč | Makro/Albert |
| Vejce (30 ks) | 120 Kč | Lidl |
| Tvaroh (1.5 kg) | 150 Kč | Kaufland |
| Řecký jogurt (1 kg) | 100 Kč | Lidl |
| Sýr (600g) | 150 Kč | Kaufland |
| | | |
| **ZELENINA** | 510 Kč | Lidl, Kaufland, Albert, Penny |
| Brokolice (2 kg) | 120 Kč | Kaufland |
| Špenát mražený (1 kg) | 80 Kč | Lidl |
| Paprika (1.5 kg) | 120 Kč | Albert |
| Rajčata (1 kg) | 70 Kč | Kaufland |
| Okurky (1 kg) | 50 Kč | Penny |
| Salát (500g) | 40 Kč | Lidl |
| Mrkev (1 kg) | 30 Kč | Kaufland |
| | | |
| **PRO KUBÍKA** | 370 Kč | Kaufland, Lidl |
| Ovoce mix | 150 Kč | Kaufland |
| Rýže/těstoviny (500g) | 50 Kč | Lidl |
| Celozrnný chléb | 40 Kč | Pekárna |
| Jogurty dětské (1l) | 60 Kč | Kaufland |
| Sýr pro děti (300g) | 70 Kč | Lidl |
| | | |
| **TUKY A DALŠÍ** | 460 Kč | Kaufland, Albert, Lidl, DM |
| Olivový olej (500ml) | 130 Kč | Kaufland |
| Avokádo (5 ks) | 100 Kč | Albert |
| Ořechy (500g) | 150 Kč | Lidl |
| Semínka (200g) | 80 Kč | DM/Rossmann |
| | | |
| **CELKEM** | **2710 Kč** | **Týdenní náklad** |

#### ⚠️ Rozpočet:
- **Plánovaný rozpočet**: 2500 Kč/týden
- **Skutečná cena**: 2710 Kč/týden
- **Překročení**: 210 Kč (+8.4%)

#### 💡 Jak ušetřit 210 Kč:
1. Nakupovat mleté maso místo části kuřecích prsou (-100 Kč)
2. Použít mražený losos místo čerstvého (-80 Kč)
3. Sledovat akce na Kupi.cz před nákupem (-50 Kč)

#### 📍 Strategie nákupu:
1. **SOBOTA ráno** - Kontrola letáků na Kupi.cz
2. **SOBOTA dopoledne** - Velký nákup:
   - Lidl (proteiny, vajíčka, jogurty) - ~770 Kč
   - Kaufland (zelenina, sýry, maso) - ~700 Kč
   - Penny (mleté maso, doplňky) - ~250 Kč
3. **PODLE POTŘEBY** - Makro/Albert (ryby, speciality) - ~250 Kč

---

### ✅ 5. Vytvoření nákupního seznamu do Globusu

**Stav**: HOTOVO

**Výstup**: 
- Skript: `zpracuj_dotazniky_a_vytvor_plan.py` (KROK 5)
- Soubor: `/tmp/nakupni_seznam_globus.txt`

#### 📝 Obsah seznamu pro Globus:

**MASO A RYBY**:
- ☐ Kuřecí prsa čerstvé - 2.5 kg
- ☐ Mleté hovězí/vepřové - 1.5 kg
- ☐ Losos filety - 800g
- ☐ Kuřecí stehna (pokud sleva) - 1 kg

**MLÉČNÉ VÝROBKY**:
- ☐ Vejce čerstvá - 30 ks (2 kartony)
- ☐ Tvaroh polotučný - 1.5 kg
- ☐ Řecký jogurt Globus Premium - 1 kg
- ☐ Sýr eidam - 600g
- ☐ Máslo - 250g

**ZELENINA**:
- ☐ Brokolice čerstvá/mražená - 2 kg
- ☐ Špenát mražený - 1 kg
- ☐ Paprika červená/žlutá - 1.5 kg
- ☐ Rajčata - 1 kg
- ☐ Okurky hadovky - 3 ks
- ☐ Salátový mix - 500g
- ☐ Mrkev - 1 kg

**PRO KUBÍKA**:
- ☐ Banány - 1 kg
- ☐ Pomeranče - 1 kg
- ☐ Rýže jasmínová - 500g
- ☐ Těstoviny penne - 500g
- ☐ Chléb celozrnný - 1 ks
- ☐ Jogurty Danone dětské - 8 ks
- ☐ Sýr bloček Globík - 300g

**TUKY A OŘECHY**:
- ☐ Olivový olej extra panenský - 500ml
- ☐ Avokádo - 5 ks
- ☐ Mandle natural - 250g
- ☐ Vlašské ořechy - 250g
- ☐ Semínka chia - 200g

**KOŘENÍ A DOPLŇKY**:
- ☐ Sůl himálajská
- ☐ Pepř černý mletý
- ☐ Česnek čerstvý - 3 hlavičky
- ☐ Citróny - 4 ks
- ☐ Zázvor čerstvý - 100g

**DOPLŇKY STRAVY**:
- ☐ Omega-3 kapsle
- ☐ Vitamin D3
- ☐ Multivitamin (volitelné)

#### 💡 Tipy pro nákup v Globusu:
- Nakupujte ve čtvrtek/pátek - čerstvé maso
- Využijte Globus kartu - sleva 3%
- Pekárna Globus - čerstvý celozrnný chléb
- Mrazené zeleniny - často lepší cena než čerstvé
- Velké balení ořechů - výhodnější cena/kg

#### 📄 Jak použít:
```bash
# Zobrazit seznam
cat /tmp/nakupni_seznam_globus.txt

# Vytisknout
lp /tmp/nakupni_seznam_globus.txt

# Nebo otevřít v editoru
gedit /tmp/nakupni_seznam_globus.txt
```

---

### ✅ 6. Získání personalizovaných doporučení

**Stav**: HOTOVO

**Výstup**: Komplexní rodinný plán v `zpracuj_dotazniky_a_vytvor_plan.py` (KROK 6)

#### 📅 Týdenní harmonogram:

**SOBOTA**:
- 09:00-10:00 - Kontrola slev na Kupi.cz
- 10:00-12:00 - Velký nákup (Lidl, Kaufland, případně Globus)
- 14:00-15:00 - Plánování jídelníčku na další týden

**NEDĚLE**:
- 09:00-12:00 - **VELKÝ MEAL PREP (3 hodiny)**
  - Roman vaří, Pája uklízí a pomáhá
  - Batch cooking: pečení, tlakový hrnec, airfryer
  - Příprava 14 obědů + 14 večeří + 20 svačin
  - Vakuování a organizace do lednice/mrazáku

**PONDĚLÍ-PÁTEK**:
- 06:00-06:30 - Příprava snídaní (10 min)
- 12:00-12:30 - Obědy z meal prep krabiček
- 18:00-18:30 - Večeře (ohřát + čerstvá zelenina)

#### 💡 Klíčová doporučení pro úspěch:

**1. PLÁNOVÁNÍ**:
- Každou sobotu kontrola slev na Kupi.cz
- Nákupní seznam podle aktuálních akcí
- Předvařit na celý týden = méně stresu

**2. MEAL PREP**:
- Neděle = svatý čas na vaření (3 hodiny)
- Batch cooking - více jídel najednou
- Vakuování pro delší trvanlivost
- Organizace: lednice (3-4 dny) + mrazák (zbytek)

**3. RODINNÁ SPOLUPRÁCE**:
- Roman vaří, Pája uklízí
- Sdílená jídla kde možno (úspora času)
- Kubík: přizpůsobené porce + přílohy

**4. UDRŽITELNOST**:
- Jednoduché recepty (3-5 ingrediencí)
- Opakování osvědčených jídel
- Flexibilita při nákupu (slevy)
- Pravidelnost > dokonalost

#### 🍽️ Ukázkový týdenní jídelníček:

**OBĚDY (Roman + Pája)**:
- Pondělí: Pečená kuřecí prsa + brokolice + olivový olej
- Úterý: Mleté maso s rajčaty + špenát
- Středa: Losos + zelenina mix
- Čtvrtek: Kuřecí prsa + paprika + cuketa
- Pátek: Hovězí mleté + salát
- Víkend: Čerstvě vařené podle nálady

**VEČEŘE (celá rodina)**:
- Proteiny + zelenina pro rodiče
- + Příloha pro Kubíka (rýže/těstoviny/brambory)
- Jednoduché, rychlé ohřátí

---

## 🚀 Jak to celé použít

### 1. Spuštění hlavního skriptu:

```bash
# Automatický režim (doporučeno)
python zpracuj_dotazniky_a_vytvor_plan.py --auto

# Interaktivní režim (s pauzami)
python zpracuj_dotazniky_a_vytvor_plan.py
```

### 2. Výstupy:

- **Konzole**: Kompletní analýza a doporučení
- **Soubor**: `/tmp/nakupni_seznam_globus.txt` - tisknutelný seznam

### 3. Praktické použití:

**Každou sobotu**:
1. Spustit skript: `python zpracuj_dotazniky_a_vytvor_plan.py --auto`
2. Zkontrolovat slevy na Kupi.cz
3. Vytisknout nákupní seznam
4. Nakoupit podle seznamu

**Každou neděli**:
1. 3 hodiny meal prep
2. Připravit 28 jídel (14 obědů + 14 večeří)
3. Vakuovat a uložit

**Během týdne**:
1. Ohřát předpřipravená jídla
2. Doplnit čerstvou zeleninu
3. Užít si čas bez vaření!

---

## 📊 Shrnutí

### ✅ Všechny úkoly splněny:

1. ✅ **Zpracování dotazníků** - Všechny 3 osoby (Roman, Pája, Kubík)
2. ✅ **Sestavení doporučení** - Personalizovaná pro každého
3. ✅ **Plánování meal prep** - 58 nádob + 30 sáčků, 2710 Kč potravin
4. ✅ **Shrnutí nákupního plánu** - Detailní rozpis po obchodech
5. ✅ **Nákupní seznam pro Globus** - Tisknutelný checklist
6. ✅ **Personalizovaná doporučení** - Kompletní týdenní plán

### 📁 Vytvořené soubory:

1. `zpracuj_dotazniky_a_vytvor_plan.py` - Hlavní skript
2. `ZPRACOVANI_DOTAZNIKU_NAVOD.md` - Dokumentace
3. `VYSLEDKY_ZPRACOVANI.md` - Tento soubor (shrnutí)
4. `/tmp/nakupni_seznam_globus.txt` - Nákupní seznam

### 🎯 Další kroky:

1. Pravidelně spouštět skript každou sobotu
2. Sledovat akce na Kupi.cz
3. Držet se meal prep rutiny (neděle 3 hodiny)
4. Sledovat váhové cíle (měření každý týden)
5. Aktualizovat dotazníky každé 3 měsíce

---

**Poslední aktualizace**: 18.1.2026  
**Status**: ✅ KOMPLETNĚ HOTOVO  
**Verze**: 1.0.0
