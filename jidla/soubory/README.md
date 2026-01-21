# Struktura složky s recepty

Tato složka obsahuje všechny recepty organizované do kategorií pro snadnou orientaci.

## Poznámka k organizaci

**Důležité:** Složková struktura (polevky, salaty, atd.) je **organizační kategorie** podle typu pokrmu, 
zatímco pole `typ` v receptu (snidane, obed, vecere, svacina) označuje **kdy se jídlo typicky konzumuje**.

Například:
- Omeleta může být ve složce `snidane/` (je to vaječný pokrm), ale mít `typ: vecere` (pokud se jí na večeři)
- Polévka může být ve složce `polevky/`, ale mít `typ: vecere` (pokud je to večeře)
- Salát může být ve složce `salaty/`, ale mít `typ: obed` (pokud je to oběd)

## Kategorie

### 🍲 polevky/
Polévky a teplé tekuté pokrmy
- Asijská polévka s bílou ředkví

### 🥗 salaty/
Saláty a studená jídla
- Salát s tuňákem, vejcem a zeleninou
- Salát z bílé ředkve s mrkví
- Ředkvičkový salát s tuňákem
- Vaječný salát s cottage cheese
- Zeleninový salát s okurkami a vejci
- RaPaCiSo salát (zeleninový mix)

### 🍗 hlavni_jidla/
Hlavní jídla (maso, ryby, zapékané pokrmy)
- Kuřecí prsa s brokolicí a olivovým olejem
- Hovězí maso s cuketou
- Losos s kedlubnou a koprem
- Bramborovo-celerový nákyp s vejci a sýrem

### 🥔 prilohy/
Přílohy
- Bramborová kaše s mlékem a celerem
- Bramborové placičky se zeleninou
- Zapékané brambory se zeleninou
- Pečená bílá ředkev s bylinkami

### 🍳 snidane/
Snídaně
- Omeleta se zeleninou (3 vejce)
- Vaječná omeleta se špenátem a sýrem
- Míchaná vejce se sýrem (4 vejce)
- Vajíčka v kapustě (3 vejce)
- Vařená vejce na tvrd (3 ks)

### 🥜 svaciny/
Svačiny a lehké pokrmy
- Cottage cheese s vlašskými ořechy
- Tvaroh s lněným semínkem a skořicí

## Přidání nového receptu

Chcete-li přidat nový recept:

1. Vyberte vhodnou kategorii (podadresář)
2. Vytvořte nový YAML soubor s názvem receptu (malými písmeny, mezery nahrazeny podtržítky)
3. Postupujte podle návodu v souboru `JAK_PRIDAT_JIDLO.md`

## Recepty s bílou ředkví

Bílá ředkev je zdravá a chutná zelenina bohatá na vitamín C a vlákninu. V této databázi najdete:

- **Salát z bílé ředkve s mrkví** (salaty/) - osvěžující a křupavý
- **Ředkvičkový salát s tuňákem** (salaty/) - vysokobílkovinový, nízko sacharidový
- **Asijská polévka s bílou ředkví** (polevky/) - lehká a sytá polévka
- **Pečená bílá ředkev s bylinkami** (prilohy/) - sladká a křupavá příloha

Všechny recepty jsou vhodné pro keto/low-carb dietu a jsou bohaté na bílkoviny.
