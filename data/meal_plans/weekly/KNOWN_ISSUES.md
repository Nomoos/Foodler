# Known Issues - Weekly Meal Plans

## Shopping List Ingredient Parsing

**Status:** Pre-existing issue (not introduced by keto meal plan update)

**Issue:** The `generate_weekly_meal_plan_md.py` script has ingredient parsing issues when generating shopping lists. It sometimes:
- Breaks on parentheses: "Avokádo (1" instead of "Avokádo (1/2)"
- Creates incomplete entries: "2) s olivovým olejem a solí"
- Duplicates similar items: "Cuketa" and "Cuketa s česnekem"

**Location:** `scripts/generate_weekly_meal_plan_md.py`, function `generate_shopping_list()`

**Impact:** Low - Shopping lists are generated but need manual review

**Workaround:** Review generated shopping list and manually consolidate items

**Future Fix:** Update the ingredient extraction regex to handle:
1. Parentheses with fractions (1/2, 1/4)
2. Portion sizes in parentheses
3. Full meal names vs. individual ingredients
4. Better deduplication of similar items

**Example Issues:**
```markdown
- [ ] **Avokádo (1** (použito 5× během týdne)  
      Should be: Avokádo (celkem 5x jako 1/2 kusu)

- [ ] **2) s olivovým olejem a solí** (použito 1× během týdne)
      Should be: Avokádo s olivovým olejem a solí

- [ ] **Omeleta ze 3 vajec** vs **Vejce natvrdo** vs **Vejce na měkko**
      Should consolidate: Vejce (celkem X ks)
```

## Note

This issue exists in the original codebase and is not related to the keto meal plan update. The core meal plan data is correct and all scripts display meals properly. Only the shopping list generation has parsing issues.
