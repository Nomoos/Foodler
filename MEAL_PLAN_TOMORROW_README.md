# Plán jídel na zítřek - 21. ledna 2026 🍽️

## Přehled

Tento dokument obsahuje kompletní plán jídel na zítřejší den, vytvořený na základě dostupných surovin:
- 🥔 Brambory
- 🥬 Celer  
- 🥕 Mrkev
- 🥬 Zelí
- 🥒 Naložené okurky (sterilované kyselé)
- 🥛 Mléko
- 🥚 Vejce

## 📋 Rychlý přehled

| Jídlo | Typ | Čas | Kalorie/porci | Protein/porci | Obtížnost |
|-------|-----|-----|---------------|---------------|-----------|
| Zeleninový salát s okurkami a vejci | Oběd | 25 min | 258 kcal | 9.2g | Snadná |
| Bramborová kaše s mlékem a celerem | Příloha | 30 min | 222.5 kcal | 5.7g | Snadná |
| Bramborové placičky se zeleninou | Večeře | 40 min | 193.3 kcal | 5.7g | Střední |
| **Zapékané brambory se zeleninou** 🆕 | Oběd | 50 min | 227.3 kcal | 8.7g | Střední |

**Celkem za den (3 původní jídla):** 674 kcal, 20.6g bílkovin, 101.3g sacharidů  
**Nová varianta (zapékané):** 227.3 kcal, 8.7g bílkovin, 26.8g sacharidů

## 📁 Soubory

### Recepty (YAML)
- `jidla/soubory/zeleninový_salát_s_okurkami_a_vejci.yaml`
- `jidla/soubory/bramborová_kaše_s_mlékem_a_celerem.yaml`
- `jidla/soubory/bramborové_placičky_se_zeleninou.yaml`
- `jidla/soubory/zapékané_brambory_se_zeleninou.yaml` 🆕

### Plány a seznamy
- `data/meal_plans/meal_plan_2026-01-21.md` - Detailní denní plán s postupy
- `data/meal_plans/shopping_list_2026-01-21.md` - Nákupní seznam

### Nové potraviny (YAML)
- `potraviny/soubory/brambory.yaml`
- `potraviny/soubory/celer.yaml`
- `potraviny/soubory/mrkev.yaml`
- `potraviny/soubory/mléko_polotučné.yaml`

## 🛒 Nákupní seznam

### Co potřebujete koupit:
- Brambory: 1 kg (~15 Kč)
- Mrkev: 200g (~4 Kč)
- Celer: 180g (~5.40 Kč)
- Zelí: 180g (~3.60 Kč)
- Mléko polotučné: 100ml (~2.50 Kč)

**Celková cena: ~31 Kč** (pokud už máte vejce, olej a okurky doma)

### Co pravděpodobně už máte:
- Vejce (3 ks)
- Olivový olej (45ml)
- Okurky sterilované kyselé (80g)
- Sůl a koření

## 👨‍🍳 Jak na to

### 1. Příprava předem (večer před)
- Uvařte brambory (pro salát i placičky)
- Uvařte vejce natvrdo
- Nakrájejte zeleninu a uložte do lednice

### 2. Časový harmonogram na zítřek

**Oběd (12:00):**
- 11:35 - Začít s přípravou salátu
- 11:45 - Smíchat ingredience
- 12:00 - Podávat

**Večeře (18:00):**
- 17:20 - Začít s přípravou placičků
- 17:50 - Smažit placičky
- 18:00 - Podávat s bramborovou kaší

## 💡 Tipy a triky

### Pro lepší chuť:
- Do kaše přidejte máslo nebo smetanu (volitelné)
- Salát ochutite citronovou šťávou
- Placičky podávejte s kysanou smetanou

### Pro zvýšení bílkovin:
- Přidejte do salátu kousek kuřecího masa
- Do placičků vmíchejte více vajec
- K bramborové kaši podávejte maso

### Meal prep:
- Všechna jídla vydrží v lednici 1-2 dny
- Placičky lze zmrazit
- Kaši lze ohřát v mikrovlnce

## 🎯 Vhodnost pro rodinu

### Pro Roman (keto dieta):
- ⚠️ Brambory jsou vyšší v sacharidech
- 💡 Doporučuji doplnit více bílkovin (maso, ryby)
- ✅ Přidejte více tuku (olivový olej, máslo)

### Pro Pája:
- ✅ Nízkokalorická jídla
- ✅ Dostatek zeleniny
- ⚠️ Může potřebovat více bílkovin

### Pro Kubíka:
- ✅✅ Ideální! Mrkev je dobrá pro oči
- ✅ Brambory jsou dobrý zdroj energie
- ✅ Vejce pro růst

## 🧪 Testování

Všechny recepty byly otestovány a načítají se správně:

```bash
python -c "from jidla.databaze import DatabzeJidel; print(len(DatabzeJidel.get_all()))"
# Output: 17 receptů (včetně nového zapékaného jídla)
```

## 📊 Nutriční hodnoty (detailní)

### Zeleninový salát s okurkami a vejci (1 porce)
- Kalorie: 258 kcal
- Bílkoviny: 9.2g
- Sacharidy: 26.9g  
- Tuky: 12.8g
- Vláknina: 4.2g

### Bramborová kaše s mlékem a celerem (1 porce)
- Kalorie: 222.5 kcal
- Bílkoviny: 5.7g
- Sacharidy: 42.9g
- Tuky: 5.1g
- Vláknina: 5.3g

### Bramborové placičky se zeleninou (1 porce)
- Kalorie: 193.3 kcal
- Bílkoviny: 5.7g
- Sacharidy: 31.5g
- Tuky: 6.4g
- Vláknina: 4.8g

### Zapékané brambory se zeleninou (1 porce) 🆕
- Kalorie: 227.3 kcal
- Bílkoviny: 8.7g
- Sacharidy: 26.8g
- Tuky: 9.7g
- Vláknina: 5.3g
- **Inspirováno ratatouille** - zapékané jídlo v troubě

## 🔄 Variace receptů

### Alternativy:
1. **Místo brambor:** Batáty (sladké brambory), květák
2. **Místo celeru:** Petržel, pastinák
3. **Místo zelí:** Čínské zelí, kysané zelí
4. **Místo mléka:** Mandlové mléko, smetana

## ✅ Co bylo vytvořeno

- [x] 4 nové potraviny přidány do databáze
- [x] 3 nové recepty vytvořeny
- [x] Denní jídelníček naplánován
- [x] Nákupní seznam vygenerován
- [x] Nutriční hodnoty vypočítány
- [x] Vše otestováno a funkční

## 📞 Další informace

Pro více informací o receptech:
```bash
python jidla/databaze.py
```

Pro zobrazení nákupního seznamu:
```bash
cat data/meal_plans/shopping_list_2026-01-21.md
```

Pro zobrazení detailního plánu:
```bash
cat data/meal_plans/meal_plan_2026-01-21.md
```

---

**Datum vytvoření:** 21. ledna 2026  
**Autor:** Foodler Meal Planning System  
**Verze:** 1.0

Dobrou chuť! 🍽️👨‍🍳
