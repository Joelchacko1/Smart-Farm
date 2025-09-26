"""
Government Scheme Matcher
Matches farmers with relevant government schemes and subsidies
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

class GovernmentSchemeMatcher:
    """
    Matches farmers with relevant government schemes and subsidies
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.schemes_database = self._load_schemes_database()
        self.eligibility_criteria = self._load_eligibility_criteria()
    
    def _load_schemes_database(self) -> Dict[str, Any]:
        """Load government schemes database"""
        return {
            'pm_kisan': {
                'name': 'PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)',
                'description': 'Direct income support of ₹6,000 per year to small and marginal farmers',
                'benefit_amount': 6000,
                'currency': 'INR',
                'duration': 'annual',
                'category': 'income_support',
                'eligibility_criteria': {
                    'land_holding': 'up_to_2_hectares',
                    'farmer_type': ['small', 'marginal'],
                    'income_limit': 100000,
                    'age_limit': 18
                },
                'application_process': 'online_application',
                'required_documents': ['aadhaar_card', 'bank_account', 'land_documents'],
                'contact_info': {
                    'website': 'https://pmkisan.gov.in',
                    'helpline': '1800-180-1551'
                },
                'status': 'active'
            },
            'soil_health_card': {
                'name': 'Soil Health Card Scheme',
                'description': 'Free soil testing and health cards for farmers',
                'benefit_amount': 0,
                'currency': 'INR',
                'duration': 'one_time',
                'category': 'soil_health',
                'eligibility_criteria': {
                    'farmer_type': ['all'],
                    'land_holding': 'any',
                    'soil_testing': 'required'
                },
                'application_process': 'online_application',
                'required_documents': ['aadhaar_card', 'land_documents'],
                'contact_info': {
                    'website': 'https://soilhealth.dac.gov.in',
                    'helpline': '1800-180-1551'
                },
                'status': 'active'
            },
            'pradhan_mantri_fasal_bima': {
                'name': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
                'description': 'Crop insurance scheme with premium subsidy',
                'benefit_amount': 'variable',
                'currency': 'INR',
                'duration': 'seasonal',
                'category': 'crop_insurance',
                'eligibility_criteria': {
                    'farmer_type': ['all'],
                    'crop_type': ['food_crops', 'commercial_crops', 'horticultural_crops'],
                    'land_holding': 'any'
                },
                'application_process': 'online_application',
                'required_documents': ['aadhaar_card', 'land_documents', 'bank_account'],
                'contact_info': {
                    'website': 'https://pmfby.gov.in',
                    'helpline': '1800-180-1551'
                },
                'status': 'active'
            },
            'kisan_credit_card': {
                'name': 'Kisan Credit Card (KCC)',
                'description': 'Credit facility for farmers with interest subvention',
                'benefit_amount': 'variable',
                'currency': 'INR',
                'duration': 'annual',
                'category': 'credit_facility',
                'eligibility_criteria': {
                    'farmer_type': ['all'],
                    'land_holding': 'any',
                    'credit_history': 'required'
                },
                'application_process': 'bank_application',
                'required_documents': ['aadhaar_card', 'land_documents', 'income_certificate'],
                'contact_info': {
                    'website': 'https://kcc.gov.in',
                    'helpline': '1800-180-1551'
                },
                'status': 'active'
            },
            'pradhan_mantri_kisan_sampada': {
                'name': 'PM Kisan SAMPADA Yojana',
                'description': 'Scheme for Agro-Marine Processing and Development of Agro-Processing Clusters',
                'benefit_amount': 'variable',
                'currency': 'INR',
                'duration': 'project_based',
                'category': 'processing_development',
                'eligibility_criteria': {
                    'farmer_type': ['all'],
                    'business_type': ['processing', 'value_addition'],
                    'investment_amount': 1000000
                },
                'application_process': 'online_application',
                'required_documents': ['aadhaar_card', 'business_plan', 'financial_documents'],
                'contact_info': {
                    'website': 'https://mofpi.gov.in',
                    'helpline': '1800-180-1551'
                },
                'status': 'active'
            },
            'pradhan_mantri_kisan_urja_suraksha': {
                'name': 'PM KUSUM (Kisan Urja Suraksha evam Utthaan Mahabhiyan)',
                'description': 'Scheme for solar power generation and irrigation',
                'benefit_amount': 'variable',
                'currency': 'INR',
                'duration': 'project_based',
                'category': 'renewable_energy',
                'eligibility_criteria': {
                    'farmer_type': ['all'],
                    'land_holding': 'any',
                    'solar_potential': 'required'
                },
                'application_process': 'online_application',
                'required_documents': ['aadhaar_card', 'land_documents', 'technical_feasibility'],
                'contact_info': {
                    'website': 'https://kusum.gov.in',
                    'helpline': '1800-180-1551'
                },
                'status': 'active'
            },
            'pradhan_mantri_kisan_maan_dhan': {
                'name': 'PM Kisan Maan Dhan Yojana',
                'description': 'Pension scheme for small and marginal farmers',
                'benefit_amount': 3000,
                'currency': 'INR',
                'duration': 'monthly',
                'category': 'pension',
                'eligibility_criteria': {
                    'farmer_type': ['small', 'marginal'],
                    'age_range': [18, 40],
                    'land_holding': 'up_to_2_hectares'
                },
                'application_process': 'online_application',
                'required_documents': ['aadhaar_card', 'land_documents', 'age_proof'],
                'contact_info': {
                    'website': 'https://pmkmy.gov.in',
                    'helpline': '1800-180-1551'
                },
                'status': 'active'
            },
            'pradhan_mantri_kisan_sampada_yojana': {
                'name': 'PM Kisan SAMPADA Yojana',
                'description': 'Scheme for Agro-Marine Processing and Development of Agro-Processing Clusters',
                'benefit_amount': 'variable',
                'currency': 'INR',
                'duration': 'project_based',
                'category': 'processing_development',
                'eligibility_criteria': {
                    'farmer_type': ['all'],
                    'business_type': ['processing', 'value_addition'],
                    'investment_amount': 1000000
                },
                'application_process': 'online_application',
                'required_documents': ['aadhaar_card', 'business_plan', 'financial_documents'],
                'contact_info': {
                    'website': 'https://mofpi.gov.in',
                    'helpline': '1800-180-1551'
                },
                'status': 'active'
            }
        }
    
    def _load_eligibility_criteria(self) -> Dict[str, Any]:
        """Load eligibility criteria for different farmer types"""
        return {
            'small_farmer': {
                'land_holding': 'up_to_2_hectares',
                'income_limit': 100000,
                'priority_schemes': ['pm_kisan', 'soil_health_card', 'pradhan_mantri_fasal_bima']
            },
            'marginal_farmer': {
                'land_holding': 'up_to_1_hectare',
                'income_limit': 50000,
                'priority_schemes': ['pm_kisan', 'soil_health_card', 'pradhan_mantri_fasal_bima', 'kisan_credit_card']
            },
            'medium_farmer': {
                'land_holding': '2_to_10_hectares',
                'income_limit': 200000,
                'priority_schemes': ['soil_health_card', 'pradhan_mantri_fasal_bima', 'kisan_credit_card']
            },
            'large_farmer': {
                'land_holding': 'above_10_hectares',
                'income_limit': 500000,
                'priority_schemes': ['soil_health_card', 'pradhan_mantri_fasal_bima', 'kisan_credit_card']
            }
        }
    
    def match_schemes(self, 
                     farmer_profile: Dict[str, Any], 
                     soil_data: Dict[str, Any] = None,
                     crop_preferences: List[str] = None) -> Dict[str, Any]:
        """
        Match farmer with relevant government schemes
        """
        try:
            # Analyze farmer profile
            farmer_analysis = self._analyze_farmer_profile(farmer_profile)
            
            # Get eligible schemes
            eligible_schemes = self._get_eligible_schemes(farmer_analysis, soil_data, crop_preferences)
            
            # Score and rank schemes
            ranked_schemes = self._rank_schemes(eligible_schemes, farmer_analysis, soil_data)
            
            # Generate recommendations
            recommendations = self._generate_scheme_recommendations(ranked_schemes, farmer_analysis)
            
            return {
                'success': True,
                'farmer_analysis': farmer_analysis,
                'eligible_schemes': eligible_schemes,
                'recommendations': recommendations,
                'total_schemes': len(eligible_schemes),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error matching schemes: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _analyze_farmer_profile(self, farmer_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze farmer profile for scheme eligibility"""
        analysis = {
            'farmer_type': 'unknown',
            'land_holding_category': 'unknown',
            'income_category': 'unknown',
            'priority_level': 'unknown',
            'eligible_categories': [],
            'limitations': [],
            'opportunities': []
        }
        
        # Determine farmer type based on land holding
        land_holding = farmer_profile.get('land_holding_hectares', 0)
        if land_holding <= 1:
            analysis['farmer_type'] = 'marginal'
            analysis['land_holding_category'] = 'up_to_1_hectare'
        elif land_holding <= 2:
            analysis['farmer_type'] = 'small'
            analysis['land_holding_category'] = 'up_to_2_hectares'
        elif land_holding <= 10:
            analysis['farmer_type'] = 'medium'
            analysis['land_holding_category'] = '2_to_10_hectares'
        else:
            analysis['farmer_type'] = 'large'
            analysis['land_holding_category'] = 'above_10_hectares'
        
        # Determine income category
        annual_income = farmer_profile.get('annual_income', 0)
        if annual_income <= 50000:
            analysis['income_category'] = 'low'
        elif annual_income <= 100000:
            analysis['income_category'] = 'medium'
        else:
            analysis['income_category'] = 'high'
        
        # Determine priority level
        if analysis['farmer_type'] in ['marginal', 'small']:
            analysis['priority_level'] = 'high'
            analysis['opportunities'].append('Eligible for priority schemes')
        elif analysis['farmer_type'] == 'medium':
            analysis['priority_level'] = 'medium'
        else:
            analysis['priority_level'] = 'low'
        
        # Determine eligible categories
        if analysis['farmer_type'] in ['marginal', 'small']:
            analysis['eligible_categories'].extend(['income_support', 'pension', 'credit_facility'])
        
        if land_holding > 0:
            analysis['eligible_categories'].extend(['soil_health', 'crop_insurance'])
        
        if annual_income > 100000:
            analysis['eligible_categories'].extend(['processing_development', 'renewable_energy'])
        
        return analysis
    
    def _get_eligible_schemes(self, farmer_analysis: Dict[str, Any], soil_data: Dict[str, Any] = None, crop_preferences: List[str] = None) -> List[Dict[str, Any]]:
        """Get eligible schemes based on farmer analysis"""
        eligible_schemes = []
        
        for scheme_id, scheme_data in self.schemes_database.items():
            if self._is_scheme_eligible(scheme_data, farmer_analysis, soil_data, crop_preferences):
                eligible_schemes.append({
                    'scheme_id': scheme_id,
                    **scheme_data
                })
        
        return eligible_schemes
    
    def _is_scheme_eligible(self, scheme_data: Dict[str, Any], farmer_analysis: Dict[str, Any], soil_data: Dict[str, Any] = None, crop_preferences: List[str] = None) -> bool:
        """Check if farmer is eligible for a specific scheme"""
        eligibility = scheme_data.get('eligibility_criteria', {})
        
        # Check land holding eligibility
        if 'land_holding' in eligibility:
            required_holding = eligibility['land_holding']
            farmer_holding = farmer_analysis['land_holding_category']
            
            if required_holding == 'up_to_2_hectares' and farmer_holding not in ['up_to_1_hectare', 'up_to_2_hectares']:
                return False
            elif required_holding == 'up_to_1_hectare' and farmer_holding != 'up_to_1_hectare':
                return False
        
        # Check farmer type eligibility
        if 'farmer_type' in eligibility:
            required_types = eligibility['farmer_type']
            if isinstance(required_types, str):
                required_types = [required_types]
            
            if farmer_analysis['farmer_type'] not in required_types and 'all' not in required_types:
                return False
        
        # Check income limit
        if 'income_limit' in eligibility:
            income_limit = eligibility['income_limit']
            farmer_income = farmer_analysis.get('annual_income', 0)
            if farmer_income > income_limit:
                return False
        
        # Check age limit
        if 'age_limit' in eligibility:
            age_limit = eligibility['age_limit']
            farmer_age = farmer_analysis.get('age', 0)
            if farmer_age < age_limit:
                return False
        
        return True
    
    def _rank_schemes(self, eligible_schemes: List[Dict[str, Any]], farmer_analysis: Dict[str, Any], soil_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Rank schemes based on relevance and benefits"""
        ranked_schemes = []
        
        for scheme in eligible_schemes:
            score = self._calculate_scheme_score(scheme, farmer_analysis, soil_data)
            ranked_schemes.append({
                **scheme,
                'relevance_score': score,
                'priority_level': self._get_priority_level(score)
            })
        
        # Sort by relevance score
        ranked_schemes.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return ranked_schemes
    
    def _calculate_scheme_score(self, scheme: Dict[str, Any], farmer_analysis: Dict[str, Any], soil_data: Dict[str, Any] = None) -> float:
        """Calculate relevance score for a scheme"""
        score = 0.0
        
        # Base score based on farmer type
        if farmer_analysis['farmer_type'] in ['marginal', 'small']:
            if scheme['category'] in ['income_support', 'pension']:
                score += 40
            elif scheme['category'] in ['soil_health', 'crop_insurance']:
                score += 30
            else:
                score += 20
        else:
            if scheme['category'] in ['soil_health', 'crop_insurance']:
                score += 35
            elif scheme['category'] in ['credit_facility', 'processing_development']:
                score += 25
            else:
                score += 15
        
        # Bonus for high priority schemes
        if scheme['category'] in ['income_support', 'soil_health']:
            score += 20
        
        # Bonus for active schemes
        if scheme.get('status') == 'active':
            score += 10
        
        # Bonus for schemes with higher benefits
        if scheme.get('benefit_amount', 0) > 0:
            score += min(scheme['benefit_amount'] / 1000, 20)
        
        return min(score, 100)
    
    def _get_priority_level(self, score: float) -> str:
        """Get priority level based on score"""
        if score >= 80:
            return 'high'
        elif score >= 60:
            return 'medium'
        else:
            return 'low'
    
    def _generate_scheme_recommendations(self, ranked_schemes: List[Dict[str, Any]], farmer_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate scheme recommendations"""
        recommendations = []
        
        for scheme in ranked_schemes[:5]:  # Top 5 recommendations
            recommendation = {
                'scheme_name': scheme['name'],
                'description': scheme['description'],
                'benefit_amount': scheme['benefit_amount'],
                'currency': scheme['currency'],
                'category': scheme['category'],
                'relevance_score': scheme['relevance_score'],
                'priority_level': scheme['priority_level'],
                'eligibility_status': 'eligible',
                'application_process': scheme['application_process'],
                'required_documents': scheme['required_documents'],
                'contact_info': scheme['contact_info'],
                'application_deadline': self._get_application_deadline(scheme),
                'benefits_summary': self._get_benefits_summary(scheme),
                'application_tips': self._get_application_tips(scheme, farmer_analysis)
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _get_application_deadline(self, scheme: Dict[str, Any]) -> str:
        """Get application deadline for a scheme"""
        if scheme['duration'] == 'annual':
            return 'December 31, 2024'
        elif scheme['duration'] == 'seasonal':
            return 'Varies by season'
        elif scheme['duration'] == 'project_based':
            return 'Ongoing'
        else:
            return 'No specific deadline'
    
    def _get_benefits_summary(self, scheme: Dict[str, Any]) -> List[str]:
        """Get benefits summary for a scheme"""
        benefits = []
        
        if scheme['benefit_amount'] > 0:
            benefits.append(f"Direct benefit of ₹{scheme['benefit_amount']:,} per {scheme['duration']}")
        
        if scheme['category'] == 'income_support':
            benefits.append('Regular income support')
        elif scheme['category'] == 'crop_insurance':
            benefits.append('Crop loss protection')
        elif scheme['category'] == 'soil_health':
            benefits.append('Free soil testing and recommendations')
        elif scheme['category'] == 'credit_facility':
            benefits.append('Easy credit access with interest subvention')
        elif scheme['category'] == 'pension':
            benefits.append('Monthly pension after retirement age')
        
        return benefits
    
    def _get_application_tips(self, scheme: Dict[str, Any], farmer_analysis: Dict[str, Any]) -> List[str]:
        """Get application tips for a scheme"""
        tips = []
        
        tips.append('Ensure all required documents are ready')
        tips.append('Apply online for faster processing')
        tips.append('Keep copies of all submitted documents')
        
        if scheme['category'] == 'income_support':
            tips.append('Ensure bank account is linked with Aadhaar')
            tips.append('Keep land documents updated')
        elif scheme['category'] == 'crop_insurance':
            tips.append('Apply before sowing season')
            tips.append('Keep crop records for claim processing')
        elif scheme['category'] == 'soil_health':
            tips.append('Apply for soil testing before planting season')
            tips.append('Follow up on soil test results')
        
        return tips
