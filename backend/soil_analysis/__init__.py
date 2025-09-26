"""
Smart Farm Soil Analysis Backend
Handles soil analysis PDF processing, weather integration, and crop recommendations
"""

__version__ = "1.0.0"
__author__ = "Smart Farm Team"

from .pdf_processor import SoilAnalysisPDFProcessor
from .weather_integration import WeatherService
from .crop_recommendations import CropRecommendationEngine
from .government_schemes import GovernmentSchemeMatcher
from .farming_plans import FarmingPlanGenerator

__all__ = [
    'SoilAnalysisPDFProcessor',
    'WeatherService', 
    'CropRecommendationEngine',
    'GovernmentSchemeMatcher',
    'FarmingPlanGenerator'
]
