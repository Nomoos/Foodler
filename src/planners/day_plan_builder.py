#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day Plan Builder with fitness function and scoring framework.

This module builds daily meal plans optimized using fitness functions
with configurable thresholds and scoring.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Tuple
from enum import Enum
import random


class MealType(Enum):
    """Types of meals in a day."""
    BREAKFAST = "breakfast"
    MORNING_SNACK = "morning_snack"
    LUNCH = "lunch"
    AFTERNOON_SNACK = "afternoon_snack"
    DINNER = "dinner"
    EVENING_SNACK = "evening_snack"


@dataclass
class Meal:
    """Represents a single meal."""
    name: str
    meal_type: MealType
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float = 0
    ingredients: List[str] = field(default_factory=list)
    preparation_time_min: int = 30
    cost_estimate: float = 0.0
    
    def get_macros(self) -> Dict[str, float]:
        """Get macro breakdown."""
        return {
            "calories": self.calories,
            "protein": self.protein_g,
            "carbs": self.carbs_g,
            "fat": self.fat_g,
            "fiber": self.fiber_g
        }


@dataclass
class DayPlan:
    """Represents a complete day meal plan."""
    meals: List[Meal] = field(default_factory=list)
    date: Optional[str] = None
    notes: str = ""
    
    def get_total_macros(self) -> Dict[str, float]:
        """Calculate total macros for the day."""
        total = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0
        }
        for meal in self.meals:
            macros = meal.get_macros()
            for key in total:
                total[key] += macros[key]
        return total
    
    def get_total_cost(self) -> float:
        """Calculate total cost estimate."""
        return sum(meal.cost_estimate for meal in self.meals)
    
    def get_total_time(self) -> int:
        """Calculate total preparation time."""
        return sum(meal.preparation_time_min for meal in self.meals)


@dataclass
class FitnessThresholds:
    """Thresholds for fitness function evaluation."""
    # Macro targets (required)
    target_calories: int
    target_protein_g: int
    target_carbs_g: int
    target_fat_g: int
    
    # Tolerances
    calorie_tolerance: float = 0.1  # ±10%
    protein_tolerance: float = 0.15  # ±15%
    carbs_tolerance: float = 0.2  # ±20%
    fat_tolerance: float = 0.2  # ±20%
    
    # Minimum fiber
    min_fiber_g: float = 25
    
    # Practical constraints
    max_daily_cost: float = 500  # CZK
    max_daily_prep_time: int = 120  # minutes
    
    # Meal distribution (optional)
    min_meals: int = 2
    max_meals: int = 6


@dataclass
class FitnessScore:
    """Detailed fitness score breakdown."""
    total_score: float  # 0-100, higher is better
    
    # Component scores (0-100 each)
    calorie_score: float
    protein_score: float
    carbs_score: float
    fat_score: float
    fiber_score: float
    cost_score: float
    time_score: float
    meal_distribution_score: float
    
    # Constraint violations
    violations: List[str] = field(default_factory=list)
    
    def is_acceptable(self, min_score: float = 70.0) -> bool:
        """Check if score meets minimum threshold."""
        return self.total_score >= min_score and len(self.violations) == 0


class DayPlanBuilder:
    """
    Builds optimal day meal plans using fitness functions.
    
    Uses genetic algorithm-inspired optimization with fitness scoring
    to find meal combinations that best meet nutritional targets.
    """
    
    def __init__(self, thresholds: FitnessThresholds):
        """
        Initialize builder with fitness thresholds.
        
        Args:
            thresholds: Fitness thresholds for evaluation
        """
        self.thresholds = thresholds
        self.meal_database: List[Meal] = []
        
        # Fitness function weights (sum to 1.0)
        self.weights = {
            "calories": 0.25,
            "protein": 0.25,
            "carbs": 0.15,
            "fat": 0.15,
            "fiber": 0.05,
            "cost": 0.05,
            "time": 0.05,
            "distribution": 0.05
        }
    
    def set_meal_database(self, meals: List[Meal]):
        """Set available meals for planning."""
        self.meal_database = meals
    
    def set_weights(self, weights: Dict[str, float]):
        """
        Set custom weights for fitness components.
        
        Args:
            weights: Dictionary of component weights (should sum to 1.0)
        """
        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total}")
        self.weights = weights
    
    def _score_macro_target(
        self,
        actual: float,
        target: float,
        tolerance: float
    ) -> float:
        """
        Score a macro against its target with tolerance.
        
        Args:
            actual: Actual value
            target: Target value
            tolerance: Tolerance as fraction (e.g., 0.1 = ±10%)
            
        Returns:
            Score from 0-100
        """
        if target == 0:
            return 100 if actual == 0 else 0
        
        diff_ratio = abs(actual - target) / target
        
        if diff_ratio <= tolerance:
            # Within tolerance: score 100
            return 100.0
        elif diff_ratio <= tolerance * 2:
            # Within 2x tolerance: linear decay
            return 100.0 - (diff_ratio - tolerance) * (100.0 / tolerance)
        else:
            # Beyond 2x tolerance: score 0
            return 0.0
    
    def _score_minimum_target(
        self,
        actual: float,
        minimum: float,
        optimal: float
    ) -> float:
        """
        Score against a minimum threshold with optimal target.
        
        Args:
            actual: Actual value
            target: Minimum acceptable value
            optimal: Optimal value
            
        Returns:
            Score from 0-100
        """
        if actual >= optimal:
            return 100.0
        elif actual >= minimum:
            return 50.0 + 50.0 * (actual - minimum) / (optimal - minimum)
        else:
            return 50.0 * (actual / minimum) if minimum > 0 else 0.0
    
    def _score_maximum_constraint(
        self,
        actual: float,
        maximum: float
    ) -> float:
        """
        Score against a maximum constraint.
        
        Args:
            actual: Actual value
            maximum: Maximum allowed value
            
        Returns:
            Score from 0-100
        """
        if actual <= maximum:
            return 100.0
        elif actual <= maximum * 1.5:
            # Up to 50% over: linear penalty
            return 100.0 - 100.0 * (actual - maximum) / (maximum * 0.5)
        else:
            # More than 50% over: score 0
            return 0.0
    
    def evaluate_fitness(self, plan: DayPlan) -> FitnessScore:
        """
        Evaluate fitness of a day plan.
        
        Args:
            plan: Day plan to evaluate
            
        Returns:
            FitnessScore with detailed breakdown
        """
        macros = plan.get_total_macros()
        violations = []
        
        # Score macros
        calorie_score = self._score_macro_target(
            macros["calories"],
            self.thresholds.target_calories,
            self.thresholds.calorie_tolerance
        )
        
        protein_score = self._score_macro_target(
            macros["protein"],
            self.thresholds.target_protein_g,
            self.thresholds.protein_tolerance
        )
        
        carbs_score = self._score_macro_target(
            macros["carbs"],
            self.thresholds.target_carbs_g,
            self.thresholds.carbs_tolerance
        )
        
        fat_score = self._score_macro_target(
            macros["fat"],
            self.thresholds.target_fat_g,
            self.thresholds.fat_tolerance
        )
        
        # Score fiber (minimum target)
        fiber_score = self._score_minimum_target(
            macros["fiber"],
            self.thresholds.min_fiber_g,
            self.thresholds.min_fiber_g * 1.5
        )
        
        # Score cost and time (maximum constraints)
        cost_score = self._score_maximum_constraint(
            plan.get_total_cost(),
            self.thresholds.max_daily_cost
        )
        
        time_score = self._score_maximum_constraint(
            plan.get_total_time(),
            self.thresholds.max_daily_prep_time
        )
        
        # Score meal distribution
        num_meals = len(plan.meals)
        if self.thresholds.min_meals <= num_meals <= self.thresholds.max_meals:
            distribution_score = 100.0
        else:
            distribution_score = 0.0
            violations.append(
                f"Meal count {num_meals} outside range "
                f"[{self.thresholds.min_meals}, {self.thresholds.max_meals}]"
            )
        
        # Check for violations
        if macros["calories"] < self.thresholds.target_calories * (1 - self.thresholds.calorie_tolerance * 2):
            violations.append(f"Calories too low: {macros['calories']:.0f}")
        if macros["calories"] > self.thresholds.target_calories * (1 + self.thresholds.calorie_tolerance * 2):
            violations.append(f"Calories too high: {macros['calories']:.0f}")
        
        if macros["protein"] < self.thresholds.target_protein_g * (1 - self.thresholds.protein_tolerance * 2):
            violations.append(f"Protein too low: {macros['protein']:.0f}g")
        
        # Calculate weighted total score
        total_score = (
            self.weights["calories"] * calorie_score +
            self.weights["protein"] * protein_score +
            self.weights["carbs"] * carbs_score +
            self.weights["fat"] * fat_score +
            self.weights["fiber"] * fiber_score +
            self.weights["cost"] * cost_score +
            self.weights["time"] * time_score +
            self.weights["distribution"] * distribution_score
        )
        
        return FitnessScore(
            total_score=total_score,
            calorie_score=calorie_score,
            protein_score=protein_score,
            carbs_score=carbs_score,
            fat_score=fat_score,
            fiber_score=fiber_score,
            cost_score=cost_score,
            time_score=time_score,
            meal_distribution_score=distribution_score,
            violations=violations
        )
    
    def build_random_plan(self, num_meals: int = 3) -> DayPlan:
        """
        Build a random day plan.
        
        Args:
            num_meals: Number of meals to include
            
        Returns:
            Random day plan
        """
        if not self.meal_database:
            raise ValueError("Meal database is empty")
        
        meals = random.sample(self.meal_database, min(num_meals, len(self.meal_database)))
        return DayPlan(meals=meals)
    
    def build_optimized_plan(
        self,
        num_meals: int = 3,
        iterations: int = 100,
        min_acceptable_score: float = 70.0
    ) -> Tuple[DayPlan, FitnessScore]:
        """
        Build an optimized day plan using iterative improvement.
        
        Args:
            num_meals: Target number of meals
            iterations: Number of optimization iterations
            min_acceptable_score: Minimum acceptable fitness score
            
        Returns:
            Tuple of (best day plan, fitness score)
        """
        best_plan = None
        best_score = None
        
        for _ in range(iterations):
            plan = self.build_random_plan(num_meals)
            score = self.evaluate_fitness(plan)
            
            if best_score is None or score.total_score > best_score.total_score:
                best_plan = plan
                best_score = score
                
                # Early exit if we found an acceptable plan
                if score.is_acceptable(min_acceptable_score):
                    break
        
        return best_plan, best_score


if __name__ == "__main__":
    # Example usage
    print("=" * 70)
    print("DAY PLAN BUILDER - DEMO")
    print("=" * 70)
    
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
            preparation_time_min=15,
            cost_estimate=45
        ),
        Meal(
            name="Grilled Chicken Salad",
            meal_type=MealType.LUNCH,
            calories=450,
            protein_g=40,
            carbs_g=20,
            fat_g=20,
            fiber_g=8,
            preparation_time_min=25,
            cost_estimate=85
        ),
        Meal(
            name="Salmon with Vegetables",
            meal_type=MealType.DINNER,
            calories=500,
            protein_g=35,
            carbs_g=15,
            fat_g=32,
            fiber_g=7,
            preparation_time_min=30,
            cost_estimate=120
        ),
        Meal(
            name="Greek Yogurt with Berries",
            meal_type=MealType.MORNING_SNACK,
            calories=180,
            protein_g=15,
            carbs_g=20,
            fat_g=5,
            fiber_g=4,
            preparation_time_min=5,
            cost_estimate=35
        ),
        Meal(
            name="Cottage Cheese with Nuts",
            meal_type=MealType.AFTERNOON_SNACK,
            calories=220,
            protein_g=20,
            carbs_g=10,
            fat_g=12,
            fiber_g=3,
            preparation_time_min=5,
            cost_estimate=40
        )
    ]
    
    # Set up thresholds
    thresholds = FitnessThresholds(
        target_calories=1700,
        target_protein_g=140,
        target_carbs_g=70,
        target_fat_g=92,
        min_fiber_g=25,
        max_daily_cost=400,
        max_daily_prep_time=90,
        min_meals=3,
        max_meals=5
    )
    
    # Build optimized plan
    builder = DayPlanBuilder(thresholds)
    builder.set_meal_database(sample_meals)
    
    print("\nBuilding optimized day plan...")
    plan, score = builder.build_optimized_plan(num_meals=5, iterations=50)
    
    print("\n--- MEAL PLAN ---")
    for i, meal in enumerate(plan.meals, 1):
        print(f"\n{i}. {meal.name} ({meal.meal_type.value})")
        print(f"   {meal.calories:.0f} kcal | P: {meal.protein_g}g | C: {meal.carbs_g}g | F: {meal.fat_g}g")
        print(f"   Time: {meal.preparation_time_min} min | Cost: {meal.cost_estimate:.0f} CZK")
    
    macros = plan.get_total_macros()
    print("\n--- DAILY TOTALS ---")
    print(f"Calories: {macros['calories']:.0f} kcal (target: {thresholds.target_calories})")
    print(f"Protein: {macros['protein']:.0f}g (target: {thresholds.target_protein_g}g)")
    print(f"Carbs: {macros['carbs']:.0f}g (target: {thresholds.target_carbs_g}g)")
    print(f"Fat: {macros['fat']:.0f}g (target: {thresholds.target_fat_g}g)")
    print(f"Fiber: {macros['fiber']:.0f}g (min: {thresholds.min_fiber_g}g)")
    print(f"Total Cost: {plan.get_total_cost():.0f} CZK")
    print(f"Total Time: {plan.get_total_time()} min")
    
    print("\n--- FITNESS SCORE ---")
    print(f"Total Score: {score.total_score:.1f}/100")
    print(f"  Calories: {score.calorie_score:.1f}")
    print(f"  Protein: {score.protein_score:.1f}")
    print(f"  Carbs: {score.carbs_score:.1f}")
    print(f"  Fat: {score.fat_score:.1f}")
    print(f"  Fiber: {score.fiber_score:.1f}")
    print(f"  Cost: {score.cost_score:.1f}")
    print(f"  Time: {score.time_score:.1f}")
    print(f"  Distribution: {score.meal_distribution_score:.1f}")
    
    if score.violations:
        print("\n⚠️  Violations:")
        for violation in score.violations:
            print(f"  - {violation}")
    
    if score.is_acceptable():
        print("\n✅ Plan meets acceptable fitness threshold!")
    else:
        print("\n⚠️  Plan does not meet acceptable fitness threshold.")
