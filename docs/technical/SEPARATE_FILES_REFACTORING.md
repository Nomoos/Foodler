# Refactoring: Separate Files for Dishes and Ingredients

## Problem Statement

Previously, all dishes were stored in a single Python file (`jidla/databaze.py`) as a hardcoded list, and all ingredients were stored similarly in `potraviny/databaze.py`. This created merge conflicts when multiple people tried to add new dishes or ingredients simultaneously.

**Czech problem statement (original):**
> Drž jednotlivá jídla jako separátní soubory to samé potraviny vyhneme se tak konfliktům.
>
> Translation: "Keep individual dishes as separate files, same for ingredients - we'll avoid conflicts this way."

## Solution

We refactored the system to store each dish and each ingredient as a **separate YAML file**:

- **Dishes**: `jidla/soubory/*.yaml` (13 files)
- **Ingredients**: `potraviny/soubory/*.yaml` (30 files)

### Architecture Changes

1. **Data Storage**:
   - Before: Single `databaze.py` file with Python list
   - After: Directory with individual YAML files

2. **Loading Mechanism**:
   - The `DatabzeJidel` and `DatabazePotravIn` classes now dynamically load data from YAML files
   - Caching is implemented for performance
   - Backward compatibility is maintained

3. **File Format**:
   ```yaml
   # Example: jidla/soubory/kuřecí_prsa_s_brokolicí.yaml
   nazev: Kuřecí prsa s brokolicí a olivovým olejem
   typ: obed
   ingredience:
   - nazev: Kuřecí prsa
     mnozstvi_g: 200
     kategorie: hlavni
   kalorie_celkem: 428
   bilkoviny_celkem: 67.6
   # ... more fields
   ```

## Benefits

✅ **No Merge Conflicts**: Multiple people can add dishes/ingredients simultaneously without conflicts

✅ **Easy to Add**: Just create a new YAML file - no code changes needed

✅ **Better Organization**: Each item is a separate, readable file

✅ **Git-Friendly**: Changes to individual items are tracked separately

✅ **Backward Compatible**: All existing code continues to work without changes

## How to Add New Items

### Adding a New Dish

1. Create a new YAML file in `jidla/soubory/`
2. Follow the format in `jidla/JAK_PRIDAT_JIDLO.md`
3. The dish will be automatically loaded on next run

### Adding a New Ingredient

1. Create a new YAML file in `potraviny/soubory/`
2. Follow the format in `potraviny/JAK_PRIDAT_POTRAVINU.md`
3. The ingredient will be automatically loaded on next run

## Files Changed

### Core Files
- `jidla/databaze.py` - Refactored to load from YAML files
- `potraviny/databaze.py` - Refactored to load from YAML files
- `requirements.txt` - Added PyYAML dependency

### Documentation
- `jidla/README.md` - Updated with new structure
- `potraviny/README.md` - Updated with new structure
- `jidla/JAK_PRIDAT_JIDLO.md` - New guide for adding dishes
- `potraviny/JAK_PRIDAT_POTRAVINU.md` - New guide for adding ingredients

### Data Files
- `jidla/soubory/*.yaml` - 13 dish files
- `potraviny/soubory/*.yaml` - 30 ingredient files

## Testing

All existing functionality was tested and works correctly:

✅ `jidla/databaze.py` - Direct module execution
✅ `potraviny/databaze.py` - Direct module execution  
✅ `generate_optimized_plan.py` - Meal plan generation
✅ Dynamic loading of new files
✅ Backward compatibility

## Migration

The migration was done using a script that:
1. Read all existing dishes/ingredients from the old Python lists
2. Converted each item to YAML format
3. Wrote each item to a separate file
4. Updated the loading code to read from files

No data was lost, and all 13 dishes and 30 ingredients were successfully migrated.

## Future Improvements

Potential enhancements:
- Add validation schema for YAML files
- Create a CLI tool for adding new dishes/ingredients
- Add support for recipe variations
- Enable user-specific overrides
