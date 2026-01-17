# Meal Planner Questionnaire and Builder System

This document describes the new meal planning system built into Foodler, which uses questionnaires and fitness functions to create personalized meal plans.

## Overview

The meal planner system consists of three main components:

1. **Questionnaire Module** - Collects user dietary preferences and goals
2. **Day Plan Builder** - Creates optimized daily meal plans using fitness functions
3. **Week Plan Builder** - Combines daily plans into weekly meal plans with variety

## Quick Start

### Running the Interactive Questionnaire

```bash
cd src/planners
python questionnaire.py
```

The questionnaire will ask about:
- Personal information (age, weight, height, activity level)
- Dietary preferences (diet type, meal timing, restrictions)
- Fitness goals (weight loss, muscle gain, maintenance)

### Building a Day Plan

```python
from src.planners import DayPlanBuilder, FitnessThresholds, Meal, MealType

# Define your fitness thresholds
thresholds = FitnessThresholds(
    target_calories=1700,
    target_protein_g=140,
    target_carbs_g=70,
    target_fat_g=92,
    min_fiber_g=25,
    max_daily_cost=400,
    max_daily_prep_time=90
)

# Create builder and set meal database
builder = DayPlanBuilder(thresholds)
builder.set_meal_database(your_meal_list)

# Build optimized plan
plan, score = builder.build_optimized_plan(num_meals=3, iterations=100)

# Check results
print(f"Fitness Score: {score.total_score:.1f}/100")
if score.is_acceptable():
    print("✅ Plan meets requirements!")
```

### Building a Week Plan

```python
from src.planners import WeekPlanBuilder
from datetime import date

# Use the day builder from above
week_builder = WeekPlanBuilder(day_builder)

# Build optimized week plan
week_plan, variety_score = week_builder.build_optimized_week_plan(
    num_days=7,
    meals_per_day=3,
    start_date=date.today()
)

# Get meal prep suggestions
prep_plan = week_builder.generate_meal_prep_plan(week_plan)
print(f"Time savings with batch cooking: {prep_plan['time_savings']:.0f} min")
```

## Fitness Function Framework

The day plan builder uses a fitness function to score meal plans on multiple criteria:

### Scoring Components

1. **Calorie Score** (25% weight) - How close to target calories
2. **Protein Score** (25% weight) - How close to target protein
3. **Carbs Score** (15% weight) - How close to target carbs
4. **Fat Score** (15% weight) - How close to target fat
5. **Fiber Score** (5% weight) - Meeting minimum fiber requirement
6. **Cost Score** (5% weight) - Staying within budget
7. **Time Score** (5% weight) - Keeping prep time reasonable
8. **Distribution Score** (5% weight) - Appropriate number of meals

### Thresholds and Tolerances

Each macro target has a tolerance range:

- **Calories**: ±10% tolerance (default)
- **Protein**: ±15% tolerance
- **Carbs**: ±20% tolerance
- **Fat**: ±20% tolerance

Plans within tolerance score 100 points. Plans beyond 2x tolerance score 0.

### Custom Weights

You can customize the importance of each component:

```python
builder.set_weights({
    "calories": 0.30,  # More important
    "protein": 0.30,
    "carbs": 0.15,
    "fat": 0.15,
    "fiber": 0.05,
    "cost": 0.03,     # Less important
    "time": 0.02,
    "distribution": 0.0  # Not considered
})
```

## Data Models

### UserProfile

Contains biometric data:
- Name, birth date, gender
- Weight (kg), height (cm)
- Activity level
- Optional: body fat %, muscle mass, visceral fat

Calculates:
- BMI
- BMR (Basal Metabolic Rate)
- TDEE (Total Daily Energy Expenditure)

### DietaryPreferences

Contains food preferences:
- Diet type (keto, low-carb, balanced, etc.)
- Allergies and intolerances
- Disliked/preferred foods
- Meal timing (meals per day, intermittent fasting)
- Budget and cooking time constraints

### FitnessGoals

Contains health goals:
- Primary goal (weight loss, muscle gain, maintenance)
- Target weight and date
- Custom macro targets (optional)
- Health conditions and medications

### Meal

Represents a single meal:
- Name and meal type (breakfast, lunch, etc.)
- Macros (calories, protein, carbs, fat, fiber)
- Ingredients list
- Preparation time and cost estimate

### DayPlan

A complete day's meal plan:
- List of meals
- Date and notes
- Methods to calculate totals

### WeekPlan

A weekly meal plan:
- List of day plans
- Week start date
- Methods for totals, averages, shopping lists

## Variety Scoring

The week plan builder evaluates variety using:

1. **Meal Variety** - Ratio of unique meals to total meals
2. **Ingredient Variety** - Number of unique ingredients used
3. **Macro Consistency** - How consistent daily macros are

Target: 60+ variety score for good weekly plans

## Meal Prep Optimization

The week builder identifies:

- Meals that appear multiple times (batch cooking candidates)
- Time savings from batch cooking
- Estimated weekly cooking time vs. meal prep time
- Shopping list consolidation

## Examples

### Example 1: Simple Day Plan

```python
from src.planners import *

# Quick setup
thresholds = FitnessThresholds(
    target_calories=2000,
    target_protein_g=150,
    target_carbs_g=100,
    target_fat_g=100
)

builder = DayPlanBuilder(thresholds)
# ... set meal database ...
plan, score = builder.build_optimized_plan(num_meals=4)
```

### Example 2: Interactive Week Planning

```python
# 1. Run questionnaire
q = interactive_questionnaire()

# 2. Get macro targets
summary = q.get_summary()
macros = summary['macros']

# 3. Create thresholds from questionnaire
thresholds = FitnessThresholds(
    target_calories=macros['calories'],
    target_protein_g=macros['protein'],
    target_carbs_g=macros['carbs'],
    target_fat_g=macros['fat']
)

# 4. Build week plan
day_builder = DayPlanBuilder(thresholds)
week_builder = WeekPlanBuilder(day_builder)
week_plan, score = week_builder.build_optimized_week_plan(num_days=7)
```

### Example 3: Custom Fitness Function

```python
# Prioritize protein and minimize cost
builder.set_weights({
    "calories": 0.20,
    "protein": 0.40,  # Double importance
    "carbs": 0.10,
    "fat": 0.10,
    "fiber": 0.05,
    "cost": 0.10,     # Higher importance
    "time": 0.03,
    "distribution": 0.02
})

plan, score = builder.build_optimized_plan(
    num_meals=3,
    iterations=200,  # More iterations for better optimization
    min_acceptable_score=80.0
)
```

## Integration with Existing Code

The planner system can integrate with:

- **potraviny/databaze.py** - Food database
- **jidla/databaze.py** - Meal recipes database
- **osoby/** - User profiles
- **nakup/seznamy.py** - Shopping lists

Example integration:

```python
from potraviny.databaze import nacist_potraviny
from jidla.databaze import nacist_jidla

# Load existing data
foods = nacist_potraviny()
meals = nacist_jidla()

# Convert to Meal objects for planner
from src.planners import Meal, MealType

planner_meals = []
for jidlo in meals:
    meal = Meal(
        name=jidlo['nazev'],
        meal_type=MealType.LUNCH,  # Map appropriately
        calories=jidlo['kalorie'],
        protein_g=jidlo['bilkoviny'],
        carbs_g=jidlo['sacharidy'],
        fat_g=jidlo['tuky']
    )
    planner_meals.append(meal)

# Use with planner
builder.set_meal_database(planner_meals)
```

## Future Enhancements

Potential improvements:

1. Machine learning for meal preferences
2. Automatic grocery store optimization
3. Recipe scaling for family sizes
4. Seasonal ingredient recommendations
5. Integration with fitness trackers
6. Automatic shopping list generation with Kupi.cz integration

## Troubleshooting

### Issue: Low fitness scores

- Increase tolerance ranges
- Add more meals to the database
- Adjust weights to prioritize achievable metrics

### Issue: Low variety scores

- Add more unique meals to database
- Reduce number of meals per day
- Increase variety_weight in WeekPlanBuilder

### Issue: Slow optimization

- Reduce iterations parameter
- Use smaller meal database
- Pre-filter meals before optimization

## Support

For questions or issues:
- Check existing profiles in `osoby/` for examples
- Review meal data in `jidla/` for format
- See `docs/diet-plans/` for dietary guidance
