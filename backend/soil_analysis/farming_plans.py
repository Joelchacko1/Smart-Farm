"""
Farming Plan Generator
Generates detailed farming plans based on soil analysis, weather data, and crop selection
"""

import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging

class FarmingPlanGenerator:
    """
    Generates comprehensive farming plans for selected crops
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.crop_plans = self._load_crop_plans()
        self.seasonal_calendar = self._load_seasonal_calendar()
        self.fertilizer_recommendations = self._load_fertilizer_recommendations()
        self.pest_management = self._load_pest_management()
        self.irrigation_schedules = self._load_irrigation_schedules()
    
    def _load_crop_plans(self) -> Dict[str, Any]:
        """Load detailed crop farming plans"""
        return {
            'wheat': {
                'name': 'Wheat',
                'scientific_name': 'Triticum aestivum',
                'season': 'winter',
                'duration_days': 120,
                'phases': {
                    'land_preparation': {
                        'duration_days': 15,
                        'activities': [
                            'Ploughing and harrowing',
                            'Leveling the field',
                            'Adding organic manure',
                            'Creating irrigation channels'
                        ],
                        'equipment_needed': ['tractor', 'plough', 'harrow', 'leveler'],
                        'labor_required': 2,
                        'cost_estimate': 5000
                    },
                    'sowing': {
                        'duration_days': 5,
                        'activities': [
                            'Seed treatment with fungicide',
                            'Sowing at recommended spacing',
                            'Covering seeds with soil',
                            'Light irrigation'
                        ],
                        'equipment_needed': ['seed_drill', 'sprayer'],
                        'labor_required': 3,
                        'cost_estimate': 3000
                    },
                    'vegetative_growth': {
                        'duration_days': 45,
                        'activities': [
                            'Regular irrigation',
                            'Weed control',
                            'Pest monitoring',
                            'Fertilizer application'
                        ],
                        'equipment_needed': ['sprayer', 'fertilizer_spreader'],
                        'labor_required': 2,
                        'cost_estimate': 8000
                    },
                    'flowering': {
                        'duration_days': 15,
                        'activities': [
                            'Critical irrigation',
                            'Pest and disease control',
                            'Nutrient management',
                            'Field monitoring'
                        ],
                        'equipment_needed': ['sprayer', 'monitoring_tools'],
                        'labor_required': 2,
                        'cost_estimate': 4000
                    },
                    'grain_development': {
                        'duration_days': 30,
                        'activities': [
                            'Gradual irrigation reduction',
                            'Pest control',
                            'Field monitoring',
                            'Harvest preparation'
                        ],
                        'equipment_needed': ['sprayer', 'monitoring_tools'],
                        'labor_required': 2,
                        'cost_estimate': 3000
                    },
                    'harvesting': {
                        'duration_days': 10,
                        'activities': [
                            'Harvesting at optimal maturity',
                            'Threshing and cleaning',
                            'Drying and storage',
                            'Post-harvest management'
                        ],
                        'equipment_needed': ['harvester', 'thresher', 'drying_equipment'],
                        'labor_required': 5,
                        'cost_estimate': 10000
                    }
                },
                'total_cost_estimate': 33000,
                'expected_yield': '3000-4000 kg/hectare',
                'market_price': '₹2000-2500/quintal'
            },
            'rice': {
                'name': 'Rice',
                'scientific_name': 'Oryza sativa',
                'season': 'summer',
                'duration_days': 120,
                'phases': {
                    'nursery_preparation': {
                        'duration_days': 25,
                        'activities': [
                            'Seed selection and treatment',
                            'Nursery bed preparation',
                            'Seed sowing',
                            'Nursery management'
                        ],
                        'equipment_needed': ['seed_treatment_equipment', 'nursery_tools'],
                        'labor_required': 2,
                        'cost_estimate': 4000
                    },
                    'land_preparation': {
                        'duration_days': 20,
                        'activities': [
                            'Puddling and leveling',
                            'Water management',
                            'Fertilizer application',
                            'Field preparation'
                        ],
                        'equipment_needed': ['tractor', 'puddler', 'leveler'],
                        'labor_required': 3,
                        'cost_estimate': 6000
                    },
                    'transplanting': {
                        'duration_days': 10,
                        'activities': [
                            'Seedling uprooting',
                            'Transplanting at proper spacing',
                            'Water management',
                            'Field monitoring'
                        ],
                        'equipment_needed': ['transplanter', 'water_management_tools'],
                        'labor_required': 5,
                        'cost_estimate': 8000
                    },
                    'vegetative_growth': {
                        'duration_days': 40,
                        'activities': [
                            'Water management',
                            'Weed control',
                            'Pest monitoring',
                            'Fertilizer application'
                        ],
                        'equipment_needed': ['water_management_tools', 'sprayer'],
                        'labor_required': 3,
                        'cost_estimate': 10000
                    },
                    'flowering': {
                        'duration_days': 15,
                        'activities': [
                            'Critical water management',
                            'Pest and disease control',
                            'Nutrient management',
                            'Field monitoring'
                        ],
                        'equipment_needed': ['water_management_tools', 'sprayer'],
                        'labor_required': 3,
                        'cost_estimate': 6000
                    },
                    'grain_development': {
                        'duration_days': 30,
                        'activities': [
                            'Gradual water reduction',
                            'Pest control',
                            'Field monitoring',
                            'Harvest preparation'
                        ],
                        'equipment_needed': ['water_management_tools', 'sprayer'],
                        'labor_required': 2,
                        'cost_estimate': 4000
                    },
                    'harvesting': {
                        'duration_days': 15,
                        'activities': [
                            'Harvesting at optimal maturity',
                            'Threshing and cleaning',
                            'Drying and storage',
                            'Post-harvest management'
                        ],
                        'equipment_needed': ['harvester', 'thresher', 'drying_equipment'],
                        'labor_required': 6,
                        'cost_estimate': 12000
                    }
                },
                'total_cost_estimate': 50000,
                'expected_yield': '4000-6000 kg/hectare',
                'market_price': '₹1800-2200/quintal'
            },
            'tomato': {
                'name': 'Tomato',
                'scientific_name': 'Solanum lycopersicum',
                'season': 'summer',
                'duration_days': 75,
                'phases': {
                    'nursery_preparation': {
                        'duration_days': 20,
                        'activities': [
                            'Seed selection and treatment',
                            'Nursery bed preparation',
                            'Seed sowing',
                            'Nursery management'
                        ],
                        'equipment_needed': ['seed_treatment_equipment', 'nursery_tools'],
                        'labor_required': 2,
                        'cost_estimate': 3000
                    },
                    'land_preparation': {
                        'duration_days': 10,
                        'activities': [
                            'Ploughing and harrowing',
                            'Bed preparation',
                            'Fertilizer application',
                            'Irrigation setup'
                        ],
                        'equipment_needed': ['tractor', 'plough', 'harrow'],
                        'labor_required': 2,
                        'cost_estimate': 4000
                    },
                    'transplanting': {
                        'duration_days': 5,
                        'activities': [
                            'Seedling uprooting',
                            'Transplanting at proper spacing',
                            'Watering',
                            'Field monitoring'
                        ],
                        'equipment_needed': ['transplanter', 'watering_tools'],
                        'labor_required': 3,
                        'cost_estimate': 2000
                    },
                    'vegetative_growth': {
                        'duration_days': 30,
                        'activities': [
                            'Regular irrigation',
                            'Weed control',
                            'Pest monitoring',
                            'Fertilizer application',
                            'Staking and training'
                        ],
                        'equipment_needed': ['sprayer', 'staking_materials'],
                        'labor_required': 3,
                        'cost_estimate': 8000
                    },
                    'flowering_fruiting': {
                        'duration_days': 20,
                        'activities': [
                            'Critical irrigation',
                            'Pest and disease control',
                            'Nutrient management',
                            'Field monitoring',
                            'Harvesting preparation'
                        ],
                        'equipment_needed': ['sprayer', 'harvesting_tools'],
                        'labor_required': 4,
                        'cost_estimate': 6000
                    }
                },
                'total_cost_estimate': 23000,
                'expected_yield': '20000-30000 kg/hectare',
                'market_price': '₹20-40/kg'
            }
        }
    
    def _load_seasonal_calendar(self) -> Dict[str, Any]:
        """Load seasonal farming calendar"""
        return {
            'winter': {
                'months': ['October', 'November', 'December', 'January', 'February'],
                'suitable_crops': ['wheat', 'barley', 'mustard', 'potato', 'onion'],
                'weather_conditions': 'cool and dry',
                'irrigation_needs': 'moderate',
                'pest_risks': 'low'
            },
            'summer': {
                'months': ['March', 'April', 'May', 'June'],
                'suitable_crops': ['rice', 'corn', 'sugarcane', 'cotton', 'tomato'],
                'weather_conditions': 'hot and humid',
                'irrigation_needs': 'high',
                'pest_risks': 'high'
            },
            'monsoon': {
                'months': ['July', 'August', 'September'],
                'suitable_crops': ['rice', 'corn', 'sugarcane', 'cotton'],
                'weather_conditions': 'rainy and humid',
                'irrigation_needs': 'low',
                'pest_risks': 'very_high'
            }
        }
    
    def _load_fertilizer_recommendations(self) -> Dict[str, Any]:
        """Load fertilizer recommendations"""
        return {
            'nitrogen': {
                'urea': {
                    'n_content': 46,
                    'application_rate': '100-150 kg/hectare',
                    'application_timing': 'basal and top dressing',
                    'cost_per_kg': 20
                },
                'ammonium_sulfate': {
                    'n_content': 21,
                    'application_rate': '200-300 kg/hectare',
                    'application_timing': 'basal and top dressing',
                    'cost_per_kg': 15
                }
            },
            'phosphorus': {
                'dap': {
                    'p_content': 46,
                    'application_rate': '50-100 kg/hectare',
                    'application_timing': 'basal application',
                    'cost_per_kg': 25
                },
                'ssp': {
                    'p_content': 16,
                    'application_rate': '150-300 kg/hectare',
                    'application_timing': 'basal application',
                    'cost_per_kg': 12
                }
            },
            'potassium': {
                'mop': {
                    'k_content': 60,
                    'application_rate': '50-100 kg/hectare',
                    'application_timing': 'basal application',
                    'cost_per_kg': 18
                },
                'sop': {
                    'k_content': 50,
                    'application_rate': '60-120 kg/hectare',
                    'application_timing': 'basal application',
                    'cost_per_kg': 30
                }
            }
        }
    
    def _load_pest_management(self) -> Dict[str, Any]:
        """Load pest management strategies"""
        return {
            'wheat': {
                'major_pests': ['aphids', 'army_worm', 'cut_worm'],
                'diseases': ['rust', 'smut', 'powdery_mildew'],
                'control_measures': {
                    'cultural': [
                        'Crop rotation',
                        'Proper spacing',
                        'Field sanitation',
                        'Resistant varieties'
                    ],
                    'biological': [
                        'Beneficial insects',
                        'Biopesticides',
                        'Natural predators'
                    ],
                    'chemical': [
                        'Insecticides for pest control',
                        'Fungicides for disease control',
                        'Integrated pest management'
                    ]
                }
            },
            'rice': {
                'major_pests': ['brown_plant_hopper', 'stem_borer', 'leaf_folder'],
                'diseases': ['blast', 'bacterial_blight', 'sheath_blight'],
                'control_measures': {
                    'cultural': [
                        'Water management',
                        'Proper spacing',
                        'Field sanitation',
                        'Resistant varieties'
                    ],
                    'biological': [
                        'Beneficial insects',
                        'Biopesticides',
                        'Natural predators'
                    ],
                    'chemical': [
                        'Insecticides for pest control',
                        'Fungicides for disease control',
                        'Integrated pest management'
                    ]
                }
            },
            'tomato': {
                'major_pests': ['whitefly', 'aphids', 'fruit_borer'],
                'diseases': ['early_blight', 'late_blight', 'bacterial_wilt'],
                'control_measures': {
                    'cultural': [
                        'Crop rotation',
                        'Proper spacing',
                        'Field sanitation',
                        'Resistant varieties'
                    ],
                    'biological': [
                        'Beneficial insects',
                        'Biopesticides',
                        'Natural predators'
                    ],
                    'chemical': [
                        'Insecticides for pest control',
                        'Fungicides for disease control',
                        'Integrated pest management'
                    ]
                }
            }
        }
    
    def _load_irrigation_schedules(self) -> Dict[str, Any]:
        """Load irrigation schedules for different crops"""
        return {
            'wheat': {
                'irrigation_schedule': [
                    {'stage': 'sowing', 'days_after_sowing': 0, 'irrigation_needed': 'light'},
                    {'stage': 'tillering', 'days_after_sowing': 25, 'irrigation_needed': 'moderate'},
                    {'stage': 'flowering', 'days_after_sowing': 60, 'irrigation_needed': 'critical'},
                    {'stage': 'grain_filling', 'days_after_sowing': 80, 'irrigation_needed': 'moderate'},
                    {'stage': 'maturity', 'days_after_sowing': 100, 'irrigation_needed': 'light'}
                ],
                'total_irrigation': '4-5 times',
                'water_requirement': '400-500 mm'
            },
            'rice': {
                'irrigation_schedule': [
                    {'stage': 'transplanting', 'days_after_transplanting': 0, 'irrigation_needed': 'flooding'},
                    {'stage': 'tillering', 'days_after_transplanting': 20, 'irrigation_needed': 'flooding'},
                    {'stage': 'flowering', 'days_after_transplanting': 60, 'irrigation_needed': 'flooding'},
                    {'stage': 'grain_filling', 'days_after_transplanting': 80, 'irrigation_needed': 'flooding'},
                    {'stage': 'maturity', 'days_after_transplanting': 100, 'irrigation_needed': 'drainage'}
                ],
                'total_irrigation': 'continuous',
                'water_requirement': '1000-1500 mm'
            },
            'tomato': {
                'irrigation_schedule': [
                    {'stage': 'transplanting', 'days_after_transplanting': 0, 'irrigation_needed': 'light'},
                    {'stage': 'vegetative', 'days_after_transplanting': 15, 'irrigation_needed': 'moderate'},
                    {'stage': 'flowering', 'days_after_transplanting': 30, 'irrigation_needed': 'moderate'},
                    {'stage': 'fruiting', 'days_after_transplanting': 45, 'irrigation_needed': 'critical'},
                    {'stage': 'harvesting', 'days_after_transplanting': 60, 'irrigation_needed': 'light'}
                ],
                'total_irrigation': 'daily',
                'water_requirement': '500-600 mm'
            }
        }
    
    def generate_farming_plan(self, 
                             crop_name: str, 
                             soil_data: Dict[str, Any], 
                             weather_data: Dict[str, Any],
                             farm_size: float = 1.0,
                             farmer_experience: str = 'beginner') -> Dict[str, Any]:
        """
        Generate comprehensive farming plan for selected crop
        """
        try:
            # Get crop plan
            crop_plan = self.crop_plans.get(crop_name)
            if not crop_plan:
                raise ValueError(f"Crop plan not found for {crop_name}")
            
            # Analyze soil and weather compatibility
            compatibility_analysis = self._analyze_crop_compatibility(crop_name, soil_data, weather_data)
            
            # Generate customized plan
            customized_plan = self._customize_plan(crop_plan, soil_data, weather_data, farm_size, farmer_experience)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(crop_name, soil_data, weather_data)
            
            # Generate timeline
            timeline = self._generate_timeline(crop_plan, weather_data)
            
            # Generate cost analysis
            cost_analysis = self._generate_cost_analysis(customized_plan, farm_size)
            
            # Generate risk assessment
            risk_assessment = self._generate_risk_assessment(crop_name, soil_data, weather_data)
            
            return {
                'success': True,
                'crop_name': crop_name,
                'farming_plan': customized_plan,
                'compatibility_analysis': compatibility_analysis,
                'recommendations': recommendations,
                'timeline': timeline,
                'cost_analysis': cost_analysis,
                'risk_assessment': risk_assessment,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating farming plan: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _analyze_crop_compatibility(self, crop_name: str, soil_data: Dict[str, Any], weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze compatibility between crop and growing conditions"""
        analysis = {
            'overall_compatibility': 'unknown',
            'soil_compatibility': 'unknown',
            'weather_compatibility': 'unknown',
            'strengths': [],
            'challenges': [],
            'recommendations': []
        }
        
        # Analyze soil compatibility
        if 'ph' in soil_data:
            ph_value = soil_data['ph']['value']
            if 6.0 <= ph_value <= 7.0:
                analysis['soil_compatibility'] = 'excellent'
                analysis['strengths'].append('Optimal pH for crop growth')
            elif 5.5 <= ph_value < 6.0 or 7.0 < ph_value <= 7.5:
                analysis['soil_compatibility'] = 'good'
                analysis['recommendations'].append('pH is acceptable but could be optimized')
            else:
                analysis['soil_compatibility'] = 'poor'
                analysis['challenges'].append('pH level needs adjustment')
                analysis['recommendations'].append('Consider lime application to adjust pH')
        
        # Analyze weather compatibility
        temp = weather_data['temperature']
        humidity = weather_data['humidity']
        
        if 15 <= temp <= 30 and 40 <= humidity <= 80:
            analysis['weather_compatibility'] = 'excellent'
            analysis['strengths'].append('Ideal weather conditions')
        elif 10 <= temp <= 35 and 30 <= humidity <= 90:
            analysis['weather_compatibility'] = 'good'
            analysis['recommendations'].append('Weather conditions are suitable with proper management')
        else:
            analysis['weather_compatibility'] = 'challenging'
            analysis['challenges'].append('Weather conditions may be challenging')
            analysis['recommendations'].append('Consider protective measures like greenhouses or shade nets')
        
        # Determine overall compatibility
        if analysis['soil_compatibility'] in ['excellent', 'good'] and analysis['weather_compatibility'] in ['excellent', 'good']:
            analysis['overall_compatibility'] = 'excellent'
        elif analysis['soil_compatibility'] in ['excellent', 'good'] or analysis['weather_compatibility'] in ['excellent', 'good']:
            analysis['overall_compatibility'] = 'good'
        else:
            analysis['overall_compatibility'] = 'challenging'
        
        return analysis
    
    def _customize_plan(self, crop_plan: Dict[str, Any], soil_data: Dict[str, Any], weather_data: Dict[str, Any], farm_size: float, farmer_experience: str) -> Dict[str, Any]:
        """Customize farming plan based on specific conditions"""
        customized_plan = crop_plan.copy()
        
        # Adjust costs based on farm size
        for phase_name, phase_data in customized_plan['phases'].items():
            phase_data['cost_estimate'] = int(phase_data['cost_estimate'] * farm_size)
            phase_data['labor_required'] = int(phase_data['labor_required'] * farm_size)
        
        # Adjust total cost
        customized_plan['total_cost_estimate'] = int(customized_plan['total_cost_estimate'] * farm_size)
        
        # Add soil-specific recommendations
        if 'ph' in soil_data:
            ph_value = soil_data['ph']['value']
            if ph_value < 6.0:
                customized_plan['soil_amendments'] = ['Add lime to increase pH']
            elif ph_value > 7.5:
                customized_plan['soil_amendments'] = ['Add sulfur to decrease pH']
        
        # Add weather-specific recommendations
        temp = weather_data['temperature']
        if temp > 30:
            customized_plan['weather_adaptations'] = ['Increase irrigation frequency', 'Use shade nets']
        elif temp < 15:
            customized_plan['weather_adaptations'] = ['Use protective covers', 'Delay planting if necessary']
        
        # Add experience-based recommendations
        if farmer_experience == 'beginner':
            customized_plan['beginner_tips'] = [
                'Start with smaller area',
                'Seek guidance from experienced farmers',
                'Keep detailed records',
                'Join farmer groups for support'
            ]
        elif farmer_experience == 'intermediate':
            customized_plan['intermediate_tips'] = [
                'Focus on yield optimization',
                'Implement advanced techniques',
                'Consider value addition',
                'Explore new technologies'
            ]
        else:  # advanced
            customized_plan['advanced_tips'] = [
                'Implement precision farming',
                'Use advanced technologies',
                'Focus on sustainability',
                'Explore export markets'
            ]
        
        return customized_plan
    
    def _generate_recommendations(self, crop_name: str, soil_data: Dict[str, Any], weather_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific recommendations for the crop"""
        recommendations = []
        
        # Soil recommendations
        if 'ph' in soil_data:
            ph_value = soil_data['ph']['value']
            if ph_value < 6.0:
                recommendations.append({
                    'category': 'soil',
                    'priority': 'high',
                    'recommendation': 'Add lime to increase pH to optimal range',
                    'implementation': 'Apply 2-3 tons of lime per hectare before planting'
                })
            elif ph_value > 7.5:
                recommendations.append({
                    'category': 'soil',
                    'priority': 'high',
                    'recommendation': 'Add sulfur to decrease pH to optimal range',
                    'implementation': 'Apply 1-2 tons of sulfur per hectare before planting'
                })
        
        # Nutrient recommendations
        if 'nitrogen' in soil_data:
            n_value = soil_data['nitrogen']['value']
            if n_value < 80:
                recommendations.append({
                    'category': 'fertilizer',
                    'priority': 'high',
                    'recommendation': 'Apply nitrogen fertilizer',
                    'implementation': 'Apply 100-150 kg of urea per hectare'
                })
        
        # Weather recommendations
        temp = weather_data['temperature']
        if temp > 30:
            recommendations.append({
                'category': 'weather',
                'priority': 'medium',
                'recommendation': 'Increase irrigation frequency',
                'implementation': 'Irrigate every 2-3 days during hot weather'
            })
        
        return recommendations
    
    def _generate_timeline(self, crop_plan: Dict[str, Any], weather_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate farming timeline"""
        timeline = []
        current_date = datetime.now()
        
        for phase_name, phase_data in crop_plan['phases'].items():
            phase_start = current_date
            phase_end = current_date + timedelta(days=phase_data['duration_days'])
            
            timeline.append({
                'phase': phase_name,
                'start_date': phase_start.isoformat(),
                'end_date': phase_end.isoformat(),
                'duration_days': phase_data['duration_days'],
                'activities': phase_data['activities'],
                'equipment_needed': phase_data['equipment_needed'],
                'labor_required': phase_data['labor_required'],
                'cost_estimate': phase_data['cost_estimate']
            })
            
            current_date = phase_end
        
        return timeline
    
    def _generate_cost_analysis(self, customized_plan: Dict[str, Any], farm_size: float) -> Dict[str, Any]:
        """Generate detailed cost analysis"""
        total_cost = customized_plan['total_cost_estimate']
        
        cost_breakdown = {
            'land_preparation': 0,
            'seeds': 0,
            'fertilizers': 0,
            'pesticides': 0,
            'irrigation': 0,
            'labor': 0,
            'equipment': 0,
            'other': 0
        }
        
        # Estimate cost breakdown (simplified)
        cost_breakdown['land_preparation'] = int(total_cost * 0.15)
        cost_breakdown['seeds'] = int(total_cost * 0.10)
        cost_breakdown['fertilizers'] = int(total_cost * 0.20)
        cost_breakdown['pesticides'] = int(total_cost * 0.10)
        cost_breakdown['irrigation'] = int(total_cost * 0.15)
        cost_breakdown['labor'] = int(total_cost * 0.20)
        cost_breakdown['equipment'] = int(total_cost * 0.05)
        cost_breakdown['other'] = int(total_cost * 0.05)
        
        return {
            'total_cost': total_cost,
            'cost_per_hectare': total_cost / farm_size if farm_size > 0 else total_cost,
            'cost_breakdown': cost_breakdown,
            'expected_revenue': int(total_cost * 1.5),  # Assume 50% profit margin
            'net_profit': int(total_cost * 0.5)
        }
    
    def _generate_risk_assessment(self, crop_name: str, soil_data: Dict[str, Any], weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate risk assessment for the farming plan"""
        risks = []
        mitigations = []
        
        # Weather risks
        temp = weather_data['temperature']
        if temp > 35:
            risks.append({
                'type': 'weather',
                'risk': 'Heat stress',
                'probability': 'high',
                'impact': 'medium',
                'description': 'High temperatures can cause heat stress and reduce yield'
            })
            mitigations.append({
                'risk': 'Heat stress',
                'mitigation': 'Use shade nets and increase irrigation frequency'
            })
        
        # Soil risks
        if 'ph' in soil_data:
            ph_value = soil_data['ph']['value']
            if ph_value < 5.0 or ph_value > 8.0:
                risks.append({
                    'type': 'soil',
                    'risk': 'pH imbalance',
                    'probability': 'high',
                    'impact': 'high',
                    'description': 'Extreme pH levels can severely affect crop growth'
                })
                mitigations.append({
                    'risk': 'pH imbalance',
                    'mitigation': 'Apply appropriate soil amendments before planting'
                })
        
        # Pest and disease risks
        risks.append({
            'type': 'biological',
            'risk': 'Pest and disease attack',
            'probability': 'medium',
            'impact': 'medium',
            'description': 'Crops are susceptible to various pests and diseases'
        })
        mitigations.append({
            'risk': 'Pest and disease attack',
            'mitigation': 'Implement integrated pest management and use resistant varieties'
        })
        
        return {
            'total_risks': len(risks),
            'high_risk_count': len([r for r in risks if r['probability'] == 'high']),
            'risks': risks,
            'mitigations': mitigations,
            'risk_level': 'medium' if len(risks) <= 3 else 'high'
        }
