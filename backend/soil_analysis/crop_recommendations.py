"""
Crop Recommendation Engine
Provides intelligent crop recommendations based on soil analysis and weather data
"""

import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging

class CropRecommendationEngine:
    """
    Engine for generating crop recommendations based on soil and weather data
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.crop_database = self._load_crop_database()
        self.soil_requirements = self._load_soil_requirements()
        self.weather_requirements = self._load_weather_requirements()
    
    def _load_crop_database(self) -> Dict[str, Any]:
        """Load crop database with requirements and characteristics"""
        return {
            'wheat': {
                'name': 'Wheat',
                'scientific_name': 'Triticum aestivum',
                'category': 'cereal',
                'season': 'winter',
                'duration_days': 120,
                'water_requirements': 'moderate',
                'soil_ph_range': (6.0, 7.5),
                'soil_nitrogen_range': (50, 150),
                'soil_phosphorus_range': (15, 50),
                'soil_potassium_range': (100, 300),
                'temperature_range': (15, 25),
                'humidity_range': (40, 70),
                'yield_potential': 'high',
                'market_value': 'high',
                'disease_resistance': 'medium',
                'pest_resistance': 'medium'
            },
            'rice': {
                'name': 'Rice',
                'scientific_name': 'Oryza sativa',
                'category': 'cereal',
                'season': 'summer',
                'duration_days': 120,
                'water_requirements': 'high',
                'soil_ph_range': (5.5, 7.0),
                'soil_nitrogen_range': (80, 200),
                'soil_phosphorus_range': (20, 60),
                'soil_potassium_range': (120, 400),
                'temperature_range': (20, 30),
                'humidity_range': (60, 90),
                'yield_potential': 'very_high',
                'market_value': 'high',
                'disease_resistance': 'low',
                'pest_resistance': 'low'
            },
            'corn': {
                'name': 'Corn',
                'scientific_name': 'Zea mays',
                'category': 'cereal',
                'season': 'summer',
                'duration_days': 90,
                'water_requirements': 'moderate',
                'soil_ph_range': (6.0, 7.0),
                'soil_nitrogen_range': (100, 250),
                'soil_phosphorus_range': (20, 80),
                'soil_potassium_range': (150, 400),
                'temperature_range': (18, 28),
                'humidity_range': (50, 80),
                'yield_potential': 'high',
                'market_value': 'medium',
                'disease_resistance': 'medium',
                'pest_resistance': 'medium'
            },
            'tomato': {
                'name': 'Tomato',
                'scientific_name': 'Solanum lycopersicum',
                'category': 'vegetable',
                'season': 'summer',
                'duration_days': 75,
                'water_requirements': 'moderate',
                'soil_ph_range': (6.0, 6.8),
                'soil_nitrogen_range': (80, 200),
                'soil_phosphorus_range': (25, 100),
                'soil_potassium_range': (150, 500),
                'temperature_range': (20, 30),
                'humidity_range': (50, 70),
                'yield_potential': 'high',
                'market_value': 'high',
                'disease_resistance': 'low',
                'pest_resistance': 'low'
            },
            'potato': {
                'name': 'Potato',
                'scientific_name': 'Solanum tuberosum',
                'category': 'vegetable',
                'season': 'spring',
                'duration_days': 100,
                'water_requirements': 'moderate',
                'soil_ph_range': (5.0, 6.5),
                'soil_nitrogen_range': (60, 150),
                'soil_phosphorus_range': (20, 80),
                'soil_potassium_range': (200, 600),
                'temperature_range': (15, 25),
                'humidity_range': (60, 80),
                'yield_potential': 'medium',
                'market_value': 'medium',
                'disease_resistance': 'low',
                'pest_resistance': 'low'
            },
            'soybean': {
                'name': 'Soybean',
                'scientific_name': 'Glycine max',
                'category': 'legume',
                'season': 'summer',
                'duration_days': 110,
                'water_requirements': 'moderate',
                'soil_ph_range': (6.0, 7.0),
                'soil_nitrogen_range': (50, 120),
                'soil_phosphorus_range': (15, 60),
                'soil_potassium_range': (100, 300),
                'temperature_range': (20, 30),
                'humidity_range': (50, 80),
                'yield_potential': 'medium',
                'market_value': 'high',
                'disease_resistance': 'medium',
                'pest_resistance': 'medium'
            },
            'cotton': {
                'name': 'Cotton',
                'scientific_name': 'Gossypium hirsutum',
                'category': 'fiber',
                'season': 'summer',
                'duration_days': 150,
                'water_requirements': 'high',
                'soil_ph_range': (6.0, 8.0),
                'soil_nitrogen_range': (80, 200),
                'soil_phosphorus_range': (20, 80),
                'soil_potassium_range': (150, 400),
                'temperature_range': (25, 35),
                'humidity_range': (40, 70),
                'yield_potential': 'medium',
                'market_value': 'high',
                'disease_resistance': 'low',
                'pest_resistance': 'low'
            },
            'sugarcane': {
                'name': 'Sugarcane',
                'scientific_name': 'Saccharum officinarum',
                'category': 'cash_crop',
                'season': 'year_round',
                'duration_days': 365,
                'water_requirements': 'very_high',
                'soil_ph_range': (6.0, 7.5),
                'soil_nitrogen_range': (100, 300),
                'soil_phosphorus_range': (30, 100),
                'soil_potassium_range': (200, 600),
                'temperature_range': (25, 35),
                'humidity_range': (60, 90),
                'yield_potential': 'very_high',
                'market_value': 'high',
                'disease_resistance': 'medium',
                'pest_resistance': 'medium'
            }
        }
    
    def _load_soil_requirements(self) -> Dict[str, Any]:
        """Load soil requirement specifications"""
        return {
            'ph_optimal': (6.0, 7.0),
            'nitrogen_optimal': (80, 150),
            'phosphorus_optimal': (20, 60),
            'potassium_optimal': (150, 300),
            'organic_matter_optimal': (2.0, 4.0),
            'cec_optimal': (15, 25)
        }
    
    def _load_weather_requirements(self) -> Dict[str, Any]:
        """Load weather requirement specifications"""
        return {
            'optimal_temperature': (20, 28),
            'optimal_humidity': (50, 80),
            'optimal_rainfall': (500, 1500),  # mm per year
            'optimal_sunlight': (6, 8)  # hours per day
        }
    
    def get_crop_recommendations(self, 
                                soil_data: Dict[str, Any], 
                                weather_data: Dict[str, Any],
                                user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get crop recommendations based on soil and weather data
        """
        try:
            # Analyze soil conditions
            soil_analysis = self._analyze_soil_conditions(soil_data)
            
            # Analyze weather conditions
            weather_analysis = self._analyze_weather_conditions(weather_data)
            
            # Score crops based on compatibility
            crop_scores = self._score_crops(soil_analysis, weather_analysis, user_preferences)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(crop_scores, soil_analysis, weather_analysis)
            
            return {
                'success': True,
                'recommendations': recommendations,
                'soil_analysis': soil_analysis,
                'weather_analysis': weather_analysis,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating crop recommendations: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _analyze_soil_conditions(self, soil_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze soil conditions and provide insights"""
        analysis = {
            'overall_health': 'unknown',
            'nutrient_balance': 'unknown',
            'ph_status': 'unknown',
            'recommendations': [],
            'limitations': [],
            'strengths': []
        }
        
        # Analyze pH
        if 'ph' in soil_data:
            ph_value = soil_data['ph']['value']
            if 6.0 <= ph_value <= 7.0:
                analysis['ph_status'] = 'optimal'
                analysis['strengths'].append('Optimal pH level')
            elif 5.5 <= ph_value < 6.0 or 7.0 < ph_value <= 7.5:
                analysis['ph_status'] = 'acceptable'
                analysis['recommendations'].append('pH is acceptable but could be optimized')
            else:
                analysis['ph_status'] = 'poor'
                analysis['limitations'].append('pH level needs adjustment')
                analysis['recommendations'].append('Consider lime application to adjust pH')
        
        # Analyze nutrients
        nutrient_scores = []
        if 'nitrogen' in soil_data:
            n_value = soil_data['nitrogen']['value']
            if 80 <= n_value <= 150:
                nutrient_scores.append('nitrogen_optimal')
            elif n_value < 80:
                analysis['limitations'].append('Low nitrogen levels')
                analysis['recommendations'].append('Add nitrogen fertilizer')
            else:
                analysis['limitations'].append('High nitrogen levels')
                analysis['recommendations'].append('Monitor for nitrogen leaching')
        
        if 'phosphorus' in soil_data:
            p_value = soil_data['phosphorus']['value']
            if 20 <= p_value <= 60:
                nutrient_scores.append('phosphorus_optimal')
            elif p_value < 20:
                analysis['limitations'].append('Low phosphorus levels')
                analysis['recommendations'].append('Add phosphorus fertilizer')
            else:
                analysis['limitations'].append('High phosphorus levels')
                analysis['recommendations'].append('Monitor for phosphorus runoff')
        
        if 'potassium' in soil_data:
            k_value = soil_data['potassium']['value']
            if 150 <= k_value <= 300:
                nutrient_scores.append('potassium_optimal')
            elif k_value < 150:
                analysis['limitations'].append('Low potassium levels')
                analysis['recommendations'].append('Add potassium fertilizer')
            else:
                analysis['limitations'].append('High potassium levels')
                analysis['recommendations'].append('Monitor for potassium excess')
        
        # Determine overall health
        if len(nutrient_scores) >= 2 and analysis['ph_status'] in ['optimal', 'acceptable']:
            analysis['overall_health'] = 'good'
        elif len(nutrient_scores) >= 1:
            analysis['overall_health'] = 'fair'
        else:
            analysis['overall_health'] = 'poor'
        
        return analysis
    
    def _analyze_weather_conditions(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze weather conditions for crop suitability"""
        analysis = {
            'growing_conditions': 'unknown',
            'season_suitability': 'unknown',
            'irrigation_needs': 'unknown',
            'risk_factors': [],
            'opportunities': []
        }
        
        temp = weather_data['temperature']
        humidity = weather_data['humidity']
        wind_speed = weather_data['wind_speed']
        
        # Assess growing conditions
        if 15 <= temp <= 30 and 40 <= humidity <= 80 and wind_speed < 15:
            analysis['growing_conditions'] = 'excellent'
            analysis['opportunities'].append('Ideal growing conditions')
        elif 10 <= temp <= 35 and 30 <= humidity <= 90 and wind_speed < 20:
            analysis['growing_conditions'] = 'good'
            analysis['opportunities'].append('Good growing conditions')
        elif 5 <= temp <= 40 and 20 <= humidity <= 95:
            analysis['growing_conditions'] = 'fair'
            analysis['risk_factors'].append('Suboptimal growing conditions')
        else:
            analysis['growing_conditions'] = 'poor'
            analysis['risk_factors'].append('Challenging growing conditions')
        
        # Assess irrigation needs
        if temp > 30 and humidity < 50:
            analysis['irrigation_needs'] = 'high'
            analysis['risk_factors'].append('High irrigation requirements')
        elif temp > 25 and humidity < 60:
            analysis['irrigation_needs'] = 'moderate'
        else:
            analysis['irrigation_needs'] = 'low'
            analysis['opportunities'].append('Low irrigation requirements')
        
        # Assess risk factors
        if temp < 5:
            analysis['risk_factors'].append('Frost risk')
        elif temp > 35:
            analysis['risk_factors'].append('Heat stress risk')
        
        if humidity > 85:
            analysis['risk_factors'].append('High disease risk due to humidity')
        
        if wind_speed > 15:
            analysis['risk_factors'].append('Wind damage risk')
        
        return analysis
    
    def _score_crops(self, soil_analysis: Dict[str, Any], weather_analysis: Dict[str, Any], user_preferences: Dict[str, Any] = None) -> Dict[str, float]:
        """Score crops based on compatibility with soil and weather conditions"""
        crop_scores = {}
        
        for crop_name, crop_data in self.crop_database.items():
            score = 0.0
            max_score = 100.0
            
            # Soil compatibility (40% weight)
            soil_score = self._calculate_soil_compatibility(crop_data, soil_analysis)
            score += soil_score * 0.4
            
            # Weather compatibility (30% weight)
            weather_score = self._calculate_weather_compatibility(crop_data, weather_analysis)
            score += weather_score * 0.3
            
            # Market value (20% weight)
            market_score = self._calculate_market_score(crop_data)
            score += market_score * 0.2
            
            # User preferences (10% weight)
            if user_preferences:
                preference_score = self._calculate_preference_score(crop_data, user_preferences)
                score += preference_score * 0.1
            else:
                score += 50 * 0.1  # Neutral preference score
            
            crop_scores[crop_name] = min(score, max_score)
        
        return crop_scores
    
    def _calculate_soil_compatibility(self, crop_data: Dict[str, Any], soil_analysis: Dict[str, Any]) -> float:
        """Calculate soil compatibility score for a crop"""
        score = 0.0
        
        # pH compatibility
        if 'ph' in soil_analysis and 'ph_status' in soil_analysis:
            if soil_analysis['ph_status'] == 'optimal':
                score += 25
            elif soil_analysis['ph_status'] == 'acceptable':
                score += 15
            else:
                score += 5
        
        # Nutrient compatibility
        nutrient_score = 0
        if 'nitrogen' in soil_analysis:
            nutrient_score += 10
        if 'phosphorus' in soil_analysis:
            nutrient_score += 10
        if 'potassium' in soil_analysis:
            nutrient_score += 10
        
        score += min(nutrient_score, 25)
        
        # Overall soil health
        if soil_analysis['overall_health'] == 'good':
            score += 25
        elif soil_analysis['overall_health'] == 'fair':
            score += 15
        else:
            score += 5
        
        return min(score, 100)
    
    def _calculate_weather_compatibility(self, crop_data: Dict[str, Any], weather_analysis: Dict[str, Any]) -> float:
        """Calculate weather compatibility score for a crop"""
        score = 0.0
        
        # Growing conditions
        if weather_analysis['growing_conditions'] == 'excellent':
            score += 40
        elif weather_analysis['growing_conditions'] == 'good':
            score += 30
        elif weather_analysis['growing_conditions'] == 'fair':
            score += 20
        else:
            score += 10
        
        # Irrigation needs compatibility
        if weather_analysis['irrigation_needs'] == 'low':
            score += 30
        elif weather_analysis['irrigation_needs'] == 'moderate':
            score += 20
        else:
            score += 10
        
        # Risk factors
        risk_penalty = len(weather_analysis['risk_factors']) * 5
        score = max(score - risk_penalty, 0)
        
        return min(score, 100)
    
    def _calculate_market_score(self, crop_data: Dict[str, Any]) -> float:
        """Calculate market value score for a crop"""
        market_values = {
            'very_high': 100,
            'high': 80,
            'medium': 60,
            'low': 40
        }
        
        return market_values.get(crop_data['market_value'], 50)
    
    def _calculate_preference_score(self, crop_data: Dict[str, Any], user_preferences: Dict[str, Any]) -> float:
        """Calculate user preference score for a crop"""
        score = 50  # Base score
        
        if 'preferred_categories' in user_preferences:
            if crop_data['category'] in user_preferences['preferred_categories']:
                score += 30
        
        if 'preferred_seasons' in user_preferences:
            if crop_data['season'] in user_preferences['preferred_seasons']:
                score += 20
        
        return min(score, 100)
    
    def _generate_recommendations(self, crop_scores: Dict[str, float], soil_analysis: Dict[str, Any], weather_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate final crop recommendations"""
        # Sort crops by score
        sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        
        for crop_name, score in sorted_crops[:5]:  # Top 5 recommendations
            crop_data = self.crop_database[crop_name]
            
            recommendation = {
                'crop_name': crop_data['name'],
                'scientific_name': crop_data['scientific_name'],
                'category': crop_data['category'],
                'score': round(score, 1),
                'suitability': self._get_suitability_level(score),
                'duration_days': crop_data['duration_days'],
                'water_requirements': crop_data['water_requirements'],
                'yield_potential': crop_data['yield_potential'],
                'market_value': crop_data['market_value'],
                'advantages': self._get_crop_advantages(crop_name, soil_analysis, weather_analysis),
                'considerations': self._get_crop_considerations(crop_name, soil_analysis, weather_analysis),
                'farming_tips': self._get_farming_tips(crop_name, soil_analysis, weather_analysis)
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _get_suitability_level(self, score: float) -> str:
        """Get suitability level based on score"""
        if score >= 80:
            return 'excellent'
        elif score >= 60:
            return 'good'
        elif score >= 40:
            return 'fair'
        else:
            return 'poor'
    
    def _get_crop_advantages(self, crop_name: str, soil_analysis: Dict[str, Any], weather_analysis: Dict[str, Any]) -> List[str]:
        """Get advantages for growing a specific crop"""
        advantages = []
        
        if soil_analysis['overall_health'] == 'good':
            advantages.append('Soil conditions are suitable for this crop')
        
        if weather_analysis['growing_conditions'] in ['excellent', 'good']:
            advantages.append('Weather conditions are favorable')
        
        if weather_analysis['irrigation_needs'] == 'low':
            advantages.append('Low irrigation requirements')
        
        return advantages
    
    def _get_crop_considerations(self, crop_name: str, soil_analysis: Dict[str, Any], weather_analysis: Dict[str, Any]) -> List[str]:
        """Get considerations for growing a specific crop"""
        considerations = []
        
        if soil_analysis['overall_health'] == 'poor':
            considerations.append('Soil conditions may need improvement')
        
        if weather_analysis['growing_conditions'] == 'poor':
            considerations.append('Weather conditions may be challenging')
        
        if weather_analysis['irrigation_needs'] == 'high':
            considerations.append('High irrigation requirements')
        
        if weather_analysis['risk_factors']:
            considerations.extend(weather_analysis['risk_factors'])
        
        return considerations
    
    def _get_farming_tips(self, crop_name: str, soil_analysis: Dict[str, Any], weather_analysis: Dict[str, Any]) -> List[str]:
        """Get farming tips for a specific crop"""
        tips = []
        
        # Soil improvement tips
        if soil_analysis['overall_health'] != 'good':
            tips.append('Consider soil amendments before planting')
        
        # Weather adaptation tips
        if weather_analysis['risk_factors']:
            tips.append('Monitor weather conditions closely')
        
        # General farming tips
        tips.extend([
            'Follow proper crop rotation practices',
            'Monitor for pests and diseases regularly',
            'Maintain proper irrigation schedule',
            'Harvest at optimal maturity for best quality'
        ])
        
        return tips
