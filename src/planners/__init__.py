"""
Meal planning module with questionnaire-based builders.
"""

from .questionnaire import (
    UserProfile,
    DietaryPreferences,
    FitnessGoals,
    Questionnaire,
    ActivityLevel,
    DietType,
    Goal,
    interactive_questionnaire
)
from .day_plan_builder import (
    DayPlanBuilder,
    DayPlan,
    Meal,
    MealType,
    FitnessThresholds,
    FitnessScore
)
from .week_plan_builder import (
    WeekPlanBuilder,
    WeekPlan,
    WeeklyVarietyScore
)

__all__ = [
    # Questionnaire
    'UserProfile',
    'DietaryPreferences',
    'FitnessGoals',
    'Questionnaire',
    'ActivityLevel',
    'DietType',
    'Goal',
    'interactive_questionnaire',
    # Day planning
    'DayPlanBuilder',
    'DayPlan',
    'Meal',
    'MealType',
    'FitnessThresholds',
    'FitnessScore',
    # Week planning
    'WeekPlanBuilder',
    'WeekPlan',
    'WeeklyVarietyScore'
]
