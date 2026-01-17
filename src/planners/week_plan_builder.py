#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Week Plan Builder - builds weekly meal plans from daily plans.

This module combines multiple day plans into optimized weekly meal plans
with variety and meal prep considerations.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import date, timedelta

# Handle both package and standalone execution
if __name__ == "__main__":
    from day_plan_builder import DayPlan, DayPlanBuilder, FitnessThresholds, FitnessScore, Meal
else:
    from .day_plan_builder import DayPlan, DayPlanBuilder, FitnessThresholds, FitnessScore, Meal


@dataclass
class WeekPlan:
    """Represents a weekly meal plan."""
    days: List[DayPlan] = field(default_factory=list)
    week_start_date: Optional[date] = None
    notes: str = ""
    
    def get_week_totals(self) -> Dict[str, float]:
        """Calculate total macros for the week."""
        total = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0,
            "cost": 0,
            "time": 0
        }
        
        for day_plan in self.days:
            macros = day_plan.get_total_macros()
            for key in ["calories", "protein", "carbs", "fat", "fiber"]:
                total[key] += macros[key]
            total["cost"] += day_plan.get_total_cost()
            total["time"] += day_plan.get_total_time()
        
        return total
    
    def get_week_averages(self) -> Dict[str, float]:
        """Calculate average daily values for the week."""
        if not self.days:
            return {}
        
        totals = self.get_week_totals()
        num_days = len(self.days)
        
        return {
            key: value / num_days
            for key, value in totals.items()
        }
    
    def get_shopping_list(self) -> Dict[str, List[str]]:
        """
        Generate a shopping list from all meals in the week.
        
        Returns:
            Dictionary mapping ingredient to list of meals using it
        """
        ingredient_usage = {}
        
        for day_idx, day_plan in enumerate(self.days, 1):
            for meal in day_plan.meals:
                for ingredient in meal.ingredients:
                    if ingredient not in ingredient_usage:
                        ingredient_usage[ingredient] = []
                    ingredient_usage[ingredient].append(
                        f"Day {day_idx}: {meal.name}"
                    )
        
        return ingredient_usage
    
    def get_meal_prep_suggestions(self) -> List[str]:
        """
        Analyze the week and suggest meal prep opportunities.
        
        Returns:
            List of meal prep suggestions
        """
        suggestions = []
        
        # Track recurring meals
        meal_counts = {}
        for day_plan in self.days:
            for meal in day_plan.meals:
                meal_counts[meal.name] = meal_counts.get(meal.name, 0) + 1
        
        # Suggest batch cooking for recurring meals
        for meal_name, count in meal_counts.items():
            if count >= 3:
                suggestions.append(
                    f"Batch cook '{meal_name}' - appears {count} times this week"
                )
        
        # Calculate total prep time and suggest optimization
        total_time = sum(day.get_total_time() for day in self.days)
        if total_time > 600:  # More than 10 hours per week
            suggestions.append(
                f"Consider meal prep - total cooking time: {total_time} min/week"
            )
            suggestions.append(
                "Batch cooking on weekends could reduce daily prep to 5-10 min"
            )
        
        return suggestions


@dataclass
class WeeklyVarietyScore:
    """Scores for weekly variety metrics."""
    meal_variety_score: float  # 0-100, higher = more variety
    ingredient_variety_score: float  # 0-100, higher = more variety
    macro_consistency_score: float  # 0-100, higher = more consistent
    total_score: float  # Average of component scores
    
    feedback: List[str] = field(default_factory=list)


class WeekPlanBuilder:
    """
    Builds optimized weekly meal plans from daily plans.
    
    Ensures variety, consistency, and meal prep efficiency across the week.
    """
    
    def __init__(
        self,
        day_builder: DayPlanBuilder,
        variety_weight: float = 0.3,
        consistency_weight: float = 0.7
    ):
        """
        Initialize week plan builder.
        
        Args:
            day_builder: DayPlanBuilder for creating daily plans
            variety_weight: Weight for variety in optimization (0-1)
            consistency_weight: Weight for macro consistency (0-1)
        """
        self.day_builder = day_builder
        self.variety_weight = variety_weight
        self.consistency_weight = consistency_weight
    
    def _calculate_variety_score(self, week_plan: WeekPlan) -> WeeklyVarietyScore:
        """
        Calculate variety score for a week plan.
        
        Args:
            week_plan: Week plan to evaluate
            
        Returns:
            WeeklyVarietyScore with detailed breakdown
        """
        feedback = []
        
        # 1. Meal variety (unique meals vs total meals)
        all_meals = []
        for day in week_plan.days:
            all_meals.extend([m.name for m in day.meals])
        
        unique_meals = len(set(all_meals))
        total_meals = len(all_meals)
        meal_variety_ratio = unique_meals / total_meals if total_meals > 0 else 0
        meal_variety_score = meal_variety_ratio * 100
        
        if meal_variety_ratio < 0.6:
            feedback.append(
                f"Low meal variety: {unique_meals} unique meals out of {total_meals}"
            )
        
        # 2. Ingredient variety
        all_ingredients = []
        for day in week_plan.days:
            for meal in day.meals:
                all_ingredients.extend(meal.ingredients)
        
        unique_ingredients = len(set(all_ingredients))
        ingredient_variety_score = min(unique_ingredients / 30 * 100, 100)  # 30+ ingredients = max score
        
        if unique_ingredients < 20:
            feedback.append(
                f"Consider more ingredient variety: {unique_ingredients} unique ingredients"
            )
        
        # 3. Macro consistency across days
        daily_macros = []
        for day in week_plan.days:
            daily_macros.append(day.get_total_macros())
        
        if not daily_macros:
            return WeeklyVarietyScore(0, 0, 0, 0, feedback)
        
        # Calculate coefficient of variation for macros
        avg_calories = sum(d["calories"] for d in daily_macros) / len(daily_macros)
        std_calories = (
            sum((d["calories"] - avg_calories) ** 2 for d in daily_macros) / len(daily_macros)
        ) ** 0.5
        cv_calories = (std_calories / avg_calories) if avg_calories > 0 else 0
        
        # Lower CV = more consistent = higher score
        macro_consistency_score = max(0, 100 * (1 - cv_calories))
        
        if cv_calories > 0.15:  # More than 15% variation
            feedback.append(
                f"Daily calorie variation is high: {cv_calories*100:.1f}%"
            )
        
        total_score = (
            meal_variety_score * 0.4 +
            ingredient_variety_score * 0.3 +
            macro_consistency_score * 0.3
        )
        
        return WeeklyVarietyScore(
            meal_variety_score=meal_variety_score,
            ingredient_variety_score=ingredient_variety_score,
            macro_consistency_score=macro_consistency_score,
            total_score=total_score,
            feedback=feedback
        )
    
    def build_week_plan(
        self,
        num_days: int = 7,
        meals_per_day: int = 3,
        start_date: Optional[date] = None
    ) -> WeekPlan:
        """
        Build a basic week plan with daily plans.
        
        Args:
            num_days: Number of days to plan (default 7)
            meals_per_day: Meals per day
            start_date: Start date for the week
            
        Returns:
            WeekPlan with daily plans
        """
        week_plan = WeekPlan(week_start_date=start_date or date.today())
        
        for day_idx in range(num_days):
            day_plan, score = self.day_builder.build_optimized_plan(
                num_meals=meals_per_day,
                iterations=50
            )
            
            if start_date:
                day_plan.date = str(start_date + timedelta(days=day_idx))
            
            week_plan.days.append(day_plan)
        
        return week_plan
    
    def build_optimized_week_plan(
        self,
        num_days: int = 7,
        meals_per_day: int = 3,
        start_date: Optional[date] = None,
        iterations: int = 10,
        min_variety_score: float = 60.0
    ) -> tuple[WeekPlan, WeeklyVarietyScore]:
        """
        Build an optimized week plan with variety consideration.
        
        Args:
            num_days: Number of days to plan
            meals_per_day: Meals per day
            start_date: Start date for the week
            iterations: Number of optimization iterations
            min_variety_score: Minimum acceptable variety score
            
        Returns:
            Tuple of (best week plan, variety score)
        """
        best_plan = None
        best_score = None
        
        for _ in range(iterations):
            plan = self.build_week_plan(num_days, meals_per_day, start_date)
            variety_score = self._calculate_variety_score(plan)
            
            if best_score is None or variety_score.total_score > best_score.total_score:
                best_plan = plan
                best_score = variety_score
                
                if variety_score.total_score >= min_variety_score:
                    break
        
        return best_plan, best_score
    
    def generate_meal_prep_plan(
        self,
        week_plan: WeekPlan
    ) -> Dict[str, any]:
        """
        Generate a meal prep plan for the week.
        
        Args:
            week_plan: Week plan to prep
            
        Returns:
            Dictionary with meal prep instructions
        """
        shopping_list = week_plan.get_shopping_list()
        suggestions = week_plan.get_meal_prep_suggestions()
        
        # Identify meals suitable for batch cooking
        batch_cook_candidates = []
        meal_counts = {}
        for day in week_plan.days:
            for meal in day.meals:
                if meal.name not in meal_counts:
                    meal_counts[meal.name] = {
                        "count": 0,
                        "meal": meal
                    }
                meal_counts[meal.name]["count"] += 1
        
        for meal_name, info in meal_counts.items():
            if info["count"] >= 2:
                batch_cook_candidates.append({
                    "meal": meal_name,
                    "portions": info["count"],
                    "time_per_portion": info["meal"].preparation_time_min,
                    "total_time_if_batch": info["meal"].preparation_time_min * 1.5,
                    "time_saved": info["meal"].preparation_time_min * info["count"] - info["meal"].preparation_time_min * 1.5
                })
        
        # Sort by time saved
        batch_cook_candidates.sort(key=lambda x: x["time_saved"], reverse=True)
        
        return {
            "shopping_list": shopping_list,
            "suggestions": suggestions,
            "batch_cook_opportunities": batch_cook_candidates,
            "total_weekly_time": sum(day.get_total_time() for day in week_plan.days),
            "estimated_batch_cooking_time": sum(
                c["total_time_if_batch"] for c in batch_cook_candidates
            ),
            "time_savings": sum(c["time_saved"] for c in batch_cook_candidates)
        }


if __name__ == "__main__":
    # Example usage
    print("=" * 70)
    print("WEEK PLAN BUILDER - DEMO")
    print("=" * 70)
    
    from day_plan_builder import Meal, MealType
    
    # Create sample meals
    sample_meals = [
        Meal(
            name="Protein Omelette",
            meal_type=MealType.BREAKFAST,
            calories=350,
            protein_g=30,
            carbs_g=5,
            fat_g=23,
            fiber_g=2,
            ingredients=["eggs", "cheese", "spinach"],
            preparation_time_min=15,
            cost_estimate=45
        ),
        Meal(
            name="Greek Yogurt Bowl",
            meal_type=MealType.BREAKFAST,
            calories=280,
            protein_g=25,
            carbs_g=25,
            fat_g=8,
            fiber_g=4,
            ingredients=["greek yogurt", "berries", "nuts"],
            preparation_time_min=5,
            cost_estimate=50
        ),
        Meal(
            name="Grilled Chicken Salad",
            meal_type=MealType.LUNCH,
            calories=450,
            protein_g=40,
            carbs_g=20,
            fat_g=20,
            fiber_g=8,
            ingredients=["chicken breast", "mixed greens", "olive oil", "tomatoes"],
            preparation_time_min=25,
            cost_estimate=85
        ),
        Meal(
            name="Beef Stir-Fry",
            meal_type=MealType.LUNCH,
            calories=480,
            protein_g=38,
            carbs_g=22,
            fat_g=24,
            fiber_g=6,
            ingredients=["beef", "broccoli", "bell peppers", "soy sauce"],
            preparation_time_min=20,
            cost_estimate=95
        ),
        Meal(
            name="Salmon with Vegetables",
            meal_type=MealType.DINNER,
            calories=500,
            protein_g=35,
            carbs_g=15,
            fat_g=32,
            fiber_g=7,
            ingredients=["salmon", "asparagus", "zucchini", "lemon"],
            preparation_time_min=30,
            cost_estimate=120
        ),
        Meal(
            name="Turkey Meatballs",
            meal_type=MealType.DINNER,
            calories=420,
            protein_g=36,
            carbs_g=18,
            fat_g=22,
            fiber_g=5,
            ingredients=["ground turkey", "onion", "garlic", "herbs"],
            preparation_time_min=35,
            cost_estimate=75
        )
    ]
    
    # Set up builder
    thresholds = FitnessThresholds(
        target_calories=1600,
        target_protein_g=130,
        target_carbs_g=65,
        target_fat_g=85,
        min_fiber_g=22,
        max_daily_cost=350,
        max_daily_prep_time=80,
        min_meals=3,
        max_meals=3
    )
    
    day_builder = DayPlanBuilder(thresholds)
    day_builder.set_meal_database(sample_meals)
    
    week_builder = WeekPlanBuilder(day_builder)
    
    print("\nBuilding optimized 7-day meal plan...")
    week_plan, variety_score = week_builder.build_optimized_week_plan(
        num_days=7,
        meals_per_day=3,
        iterations=5
    )
    
    print("\n--- WEEKLY MEAL PLAN ---")
    for day_idx, day_plan in enumerate(week_plan.days, 1):
        print(f"\nDay {day_idx}:")
        for meal in day_plan.meals:
            print(f"  - {meal.name} ({meal.meal_type.value})")
    
    print("\n--- WEEKLY TOTALS ---")
    totals = week_plan.get_week_totals()
    averages = week_plan.get_week_averages()
    
    print(f"Total Calories: {totals['calories']:.0f} kcal")
    print(f"Average/day: {averages['calories']:.0f} kcal")
    print(f"Total Cost: {totals['cost']:.0f} CZK")
    print(f"Average/day: {averages['cost']:.0f} CZK")
    print(f"Total Prep Time: {totals['time']:.0f} min")
    print(f"Average/day: {averages['time']:.0f} min")
    
    print("\n--- VARIETY SCORE ---")
    print(f"Total Score: {variety_score.total_score:.1f}/100")
    print(f"  Meal Variety: {variety_score.meal_variety_score:.1f}")
    print(f"  Ingredient Variety: {variety_score.ingredient_variety_score:.1f}")
    print(f"  Macro Consistency: {variety_score.macro_consistency_score:.1f}")
    
    if variety_score.feedback:
        print("\nFeedback:")
        for item in variety_score.feedback:
            print(f"  - {item}")
    
    print("\n--- MEAL PREP PLAN ---")
    prep_plan = week_builder.generate_meal_prep_plan(week_plan)
    
    print(f"\nTotal weekly cooking time: {prep_plan['total_weekly_time']} min")
    if prep_plan['batch_cook_opportunities']:
        print(f"With batch cooking: {prep_plan['estimated_batch_cooking_time']:.0f} min")
        print(f"Time savings: {prep_plan['time_savings']:.0f} min")
        
        print("\nBatch Cooking Recommendations:")
        for opp in prep_plan['batch_cook_opportunities'][:3]:  # Top 3
            print(f"  - {opp['meal']}: cook {opp['portions']} portions")
            print(f"    Saves {opp['time_saved']:.0f} minutes")
    
    print("\n" + "=" * 70)
