#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Questionnaire module for collecting user dietary preferences and goals.

This module provides data models and questionnaire logic for building
personalized meal plans based on user input.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import date


class ActivityLevel(Enum):
    """Physical activity level categories."""
    SEDENTARY = "sedentary"  # Little or no exercise
    LIGHTLY_ACTIVE = "lightly_active"  # Light exercise 1-3 days/week
    MODERATELY_ACTIVE = "moderately_active"  # Moderate exercise 3-5 days/week
    VERY_ACTIVE = "very_active"  # Hard exercise 6-7 days/week
    EXTREMELY_ACTIVE = "extremely_active"  # Very hard exercise & physical job


class DietType(Enum):
    """Diet type preferences."""
    KETO = "keto"
    LOW_CARB = "low_carb"
    PROTEIN_FIRST = "protein_first"
    BALANCED = "balanced"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    CUSTOM = "custom"


class Goal(Enum):
    """Dietary goals."""
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    MAINTENANCE = "maintenance"
    HEALTH_IMPROVEMENT = "health_improvement"


@dataclass
class UserProfile:
    """User profile with biometric data."""
    name: str
    birth_date: date
    gender: str  # "male", "female", "other"
    weight_kg: float
    height_cm: float
    activity_level: ActivityLevel
    
    # Optional measurements
    body_fat_percentage: Optional[float] = None
    muscle_mass_kg: Optional[float] = None
    visceral_fat_area: Optional[float] = None
    
    @property
    def age(self) -> int:
        """Calculate age from birth date."""
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    
    @property
    def bmi(self) -> float:
        """Calculate Body Mass Index."""
        height_m = self.height_cm / 100
        return self.weight_kg / (height_m ** 2)
    
    def calculate_bmr(self) -> float:
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.
        
        Returns:
            BMR in kcal/day
        """
        if self.gender.lower() == "male":
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age + 5
        else:  # female or other
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age - 161
        return bmr
    
    def calculate_tdee(self) -> float:
        """
        Calculate Total Daily Energy Expenditure based on activity level.
        
        Returns:
            TDEE in kcal/day
        """
        activity_multipliers = {
            ActivityLevel.SEDENTARY: 1.2,
            ActivityLevel.LIGHTLY_ACTIVE: 1.375,
            ActivityLevel.MODERATELY_ACTIVE: 1.55,
            ActivityLevel.VERY_ACTIVE: 1.725,
            ActivityLevel.EXTREMELY_ACTIVE: 1.9
        }
        return self.calculate_bmr() * activity_multipliers[self.activity_level]


@dataclass
class DietaryPreferences:
    """User dietary preferences and restrictions."""
    diet_type: DietType
    
    # Food allergies and intolerances
    allergies: List[str] = field(default_factory=list)
    intolerances: List[str] = field(default_factory=list)
    
    # Foods to avoid or prefer
    disliked_foods: List[str] = field(default_factory=list)
    preferred_foods: List[str] = field(default_factory=list)
    
    # Meal timing preferences
    meals_per_day: int = 3
    intermittent_fasting: bool = False
    fasting_window_hours: int = 12  # e.g., 12:12, 16:8
    
    # Budget and practical constraints
    budget_level: str = "medium"  # "low", "medium", "high"
    cooking_time_available: int = 30  # minutes per day
    meal_prep_friendly: bool = True


@dataclass
class FitnessGoals:
    """User fitness and health goals."""
    primary_goal: Goal
    target_weight_kg: Optional[float] = None
    target_date: Optional[date] = None
    
    # Macro targets (optional custom values)
    daily_calories: Optional[int] = None
    protein_grams: Optional[int] = None
    carbs_grams: Optional[int] = None
    fat_grams: Optional[int] = None
    
    # Health considerations
    health_conditions: List[str] = field(default_factory=list)  # e.g., "diabetes", "high blood pressure"
    medications: List[str] = field(default_factory=list)
    
    def calculate_target_calories(self, tdee: float) -> int:
        """
        Calculate target daily calories based on goal.
        
        Args:
            tdee: Total Daily Energy Expenditure
            
        Returns:
            Target calories in kcal/day
        """
        if self.daily_calories:
            return self.daily_calories
        
        if self.primary_goal == Goal.WEIGHT_LOSS:
            return int(tdee * 0.8)  # 20% deficit
        elif self.primary_goal == Goal.MUSCLE_GAIN:
            return int(tdee * 1.1)  # 10% surplus
        else:  # maintenance or health improvement
            return int(tdee)
    
    def calculate_macro_targets(self, profile: UserProfile, diet_type: DietType) -> Dict[str, int]:
        """
        Calculate macro targets based on diet type and goals.
        
        Args:
            profile: User profile with biometric data
            diet_type: Selected diet type
            
        Returns:
            Dictionary with protein, carbs, and fat targets in grams
        """
        tdee = profile.calculate_tdee()
        target_calories = self.calculate_target_calories(tdee)
        
        # Use custom values if provided
        if self.protein_grams and self.carbs_grams and self.fat_grams:
            return {
                "calories": target_calories,
                "protein": self.protein_grams,
                "carbs": self.carbs_grams,
                "fat": self.fat_grams
            }
        
        # Calculate based on diet type
        if diet_type == DietType.KETO:
            # Keto: 70% fat, 25% protein, 5% carbs
            protein = int(target_calories * 0.25 / 4)
            carbs = int(target_calories * 0.05 / 4)
            fat = int(target_calories * 0.70 / 9)
        elif diet_type == DietType.LOW_CARB or diet_type == DietType.PROTEIN_FIRST:
            # Low carb: 50% fat, 30% protein, 20% carbs
            protein = int(target_calories * 0.30 / 4)
            carbs = int(target_calories * 0.20 / 4)
            fat = int(target_calories * 0.50 / 9)
        elif diet_type == DietType.BALANCED:
            # Balanced: 30% fat, 30% protein, 40% carbs
            protein = int(target_calories * 0.30 / 4)
            carbs = int(target_calories * 0.40 / 4)
            fat = int(target_calories * 0.30 / 9)
        else:
            # Default moderate split
            protein = int(target_calories * 0.25 / 4)
            carbs = int(target_calories * 0.45 / 4)
            fat = int(target_calories * 0.30 / 9)
        
        return {
            "calories": target_calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat
        }


@dataclass
class Questionnaire:
    """Complete questionnaire with all user inputs."""
    profile: UserProfile
    preferences: DietaryPreferences
    goals: FitnessGoals
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the questionnaire responses.
        
        Returns:
            Dictionary with summary information
        """
        tdee = self.profile.calculate_tdee()
        macros = self.goals.calculate_macro_targets(self.profile, self.preferences.diet_type)
        
        return {
            "user": {
                "name": self.profile.name,
                "age": self.profile.age,
                "bmi": round(self.profile.bmi, 1),
                "weight_kg": self.profile.weight_kg,
                "height_cm": self.profile.height_cm
            },
            "metabolism": {
                "bmr": round(self.profile.calculate_bmr(), 0),
                "tdee": round(tdee, 0),
                "activity_level": self.profile.activity_level.value
            },
            "diet": {
                "type": self.preferences.diet_type.value,
                "meals_per_day": self.preferences.meals_per_day,
                "intermittent_fasting": self.preferences.intermittent_fasting,
                "fasting_window": f"{self.preferences.fasting_window_hours}:{24 - self.preferences.fasting_window_hours}"
            },
            "goals": {
                "primary": self.goals.primary_goal.value,
                "target_weight_kg": self.goals.target_weight_kg,
                "target_date": str(self.goals.target_date) if self.goals.target_date else None
            },
            "macros": macros,
            "restrictions": {
                "allergies": self.preferences.allergies,
                "intolerances": self.preferences.intolerances,
                "disliked_foods": self.preferences.disliked_foods
            }
        }
    
    def validate(self) -> List[str]:
        """
        Validate questionnaire responses.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate profile
        if self.profile.weight_kg <= 0:
            errors.append("Weight must be positive")
        if self.profile.height_cm <= 0:
            errors.append("Height must be positive")
        if self.profile.age < 0:
            errors.append("Invalid birth date")
        
        # Validate preferences
        if self.preferences.meals_per_day < 1 or self.preferences.meals_per_day > 8:
            errors.append("Meals per day must be between 1 and 8")
        if self.preferences.fasting_window_hours < 0 or self.preferences.fasting_window_hours > 24:
            errors.append("Fasting window must be between 0 and 24 hours")
        
        # Validate goals
        if self.goals.target_weight_kg and self.goals.target_weight_kg <= 0:
            errors.append("Target weight must be positive")
        
        return errors


def interactive_questionnaire() -> Questionnaire:
    """
    Run an interactive questionnaire to collect user information.
    
    Returns:
        Completed Questionnaire object
    """
    print("=" * 70)
    print("FOODLER MEAL PLANNER - QUESTIONNAIRE")
    print("=" * 70)
    print("\nLet's create your personalized meal plan!")
    print("\n--- PROFILE INFORMATION ---\n")
    
    name = input("Name: ")
    
    # Birth date
    birth_year = int(input("Birth year (YYYY): "))
    birth_month = int(input("Birth month (MM): "))
    birth_day = int(input("Birth day (DD): "))
    birth_date = date(birth_year, birth_month, birth_day)
    
    gender = input("Gender (male/female/other): ").lower()
    weight_kg = float(input("Current weight (kg): "))
    height_cm = float(input("Height (cm): "))
    
    print("\nActivity Level:")
    print("1. Sedentary (little or no exercise)")
    print("2. Lightly Active (light exercise 1-3 days/week)")
    print("3. Moderately Active (moderate exercise 3-5 days/week)")
    print("4. Very Active (hard exercise 6-7 days/week)")
    print("5. Extremely Active (very hard exercise & physical job)")
    activity_choice = int(input("Select (1-5): "))
    activity_levels = [
        ActivityLevel.SEDENTARY,
        ActivityLevel.LIGHTLY_ACTIVE,
        ActivityLevel.MODERATELY_ACTIVE,
        ActivityLevel.VERY_ACTIVE,
        ActivityLevel.EXTREMELY_ACTIVE
    ]
    activity_level = activity_levels[activity_choice - 1]
    
    profile = UserProfile(
        name=name,
        birth_date=birth_date,
        gender=gender,
        weight_kg=weight_kg,
        height_cm=height_cm,
        activity_level=activity_level
    )
    
    print("\n--- DIETARY PREFERENCES ---\n")
    
    print("Diet Type:")
    print("1. Keto")
    print("2. Low Carb")
    print("3. Protein First")
    print("4. Balanced")
    print("5. Vegetarian")
    print("6. Vegan")
    diet_choice = int(input("Select (1-6): "))
    diet_types = [
        DietType.KETO,
        DietType.LOW_CARB,
        DietType.PROTEIN_FIRST,
        DietType.BALANCED,
        DietType.VEGETARIAN,
        DietType.VEGAN
    ]
    diet_type = diet_types[diet_choice - 1]
    
    meals_per_day = int(input("\nMeals per day (1-8): "))
    if_choice = input("Use intermittent fasting? (yes/no): ").lower()
    intermittent_fasting = if_choice in ['yes', 'y']
    
    fasting_window = 12
    if intermittent_fasting:
        fasting_window = int(input("Fasting window (hours, e.g., 12 for 12:12, 16 for 16:8): "))
    
    preferences = DietaryPreferences(
        diet_type=diet_type,
        meals_per_day=meals_per_day,
        intermittent_fasting=intermittent_fasting,
        fasting_window_hours=fasting_window
    )
    
    print("\n--- FITNESS GOALS ---\n")
    
    print("Primary Goal:")
    print("1. Weight Loss")
    print("2. Muscle Gain")
    print("3. Maintenance")
    print("4. Health Improvement")
    goal_choice = int(input("Select (1-4): "))
    goal_types = [
        Goal.WEIGHT_LOSS,
        Goal.MUSCLE_GAIN,
        Goal.MAINTENANCE,
        Goal.HEALTH_IMPROVEMENT
    ]
    primary_goal = goal_types[goal_choice - 1]
    
    target_weight_input = input("\nTarget weight (kg) [press Enter to skip]: ")
    target_weight = float(target_weight_input) if target_weight_input else None
    
    goals = FitnessGoals(
        primary_goal=primary_goal,
        target_weight_kg=target_weight
    )
    
    questionnaire = Questionnaire(
        profile=profile,
        preferences=preferences,
        goals=goals
    )
    
    # Validate
    errors = questionnaire.validate()
    if errors:
        print("\n⚠️  Validation errors:")
        for error in errors:
            print(f"  - {error}")
        return None
    
    print("\n" + "=" * 70)
    print("✅ QUESTIONNAIRE COMPLETE!")
    print("=" * 70)
    
    return questionnaire


if __name__ == "__main__":
    # Run interactive questionnaire
    q = interactive_questionnaire()
    
    if q:
        print("\n--- SUMMARY ---\n")
        summary = q.get_summary()
        
        print(f"👤 {summary['user']['name']}, {summary['user']['age']} years old")
        print(f"   Weight: {summary['user']['weight_kg']} kg, BMI: {summary['user']['bmi']}")
        print(f"\n🔥 Metabolism:")
        print(f"   BMR: {summary['metabolism']['bmr']} kcal/day")
        print(f"   TDEE: {summary['metabolism']['tdee']} kcal/day")
        print(f"\n🍽️  Diet: {summary['diet']['type']}")
        print(f"   {summary['diet']['meals_per_day']} meals/day")
        if summary['diet']['intermittent_fasting']:
            print(f"   IF window: {summary['diet']['fasting_window']}")
        print(f"\n🎯 Goal: {summary['goals']['primary']}")
        if summary['goals']['target_weight_kg']:
            print(f"   Target weight: {summary['goals']['target_weight_kg']} kg")
        print(f"\n📊 Daily Macros:")
        print(f"   Calories: {summary['macros']['calories']} kcal")
        print(f"   Protein: {summary['macros']['protein']} g")
        print(f"   Carbs: {summary['macros']['carbs']} g")
        print(f"   Fat: {summary['macros']['fat']} g")
