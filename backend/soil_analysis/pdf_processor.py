"""
Soil Analysis PDF Processor
Extracts soil analysis data from uploaded PDF files
"""

import PyPDF2
import pdfplumber
import re
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

class SoilAnalysisPDFProcessor:
    """
    Processes soil analysis PDF files and extracts relevant data
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.soil_parameters = {
            'ph': ['ph', 'ph level', 'ph value', 'acidity', 'alkalinity'],
            'nitrogen': ['nitrogen', 'n', 'n content', 'total nitrogen'],
            'phosphorus': ['phosphorus', 'p', 'p2o5', 'phosphate'],
            'potassium': ['potassium', 'k', 'k2o', 'potash'],
            'organic_matter': ['organic matter', 'om', 'organic carbon', 'humus'],
            'calcium': ['calcium', 'ca', 'lime'],
            'magnesium': ['magnesium', 'mg'],
            'sulfur': ['sulfur', 's', 'sulphur'],
            'zinc': ['zinc', 'zn'],
            'iron': ['iron', 'fe'],
            'manganese': ['manganese', 'mn'],
            'copper': ['copper', 'cu'],
            'boron': ['boron', 'b'],
            'molybdenum': ['molybdenum', 'mo'],
            'cobalt': ['cobalt', 'co'],
            'nickel': ['nickel', 'ni'],
            'lead': ['lead', 'pb'],
            'cadmium': ['cadmium', 'cd'],
            'chromium': ['chromium', 'cr'],
            'mercury': ['mercury', 'hg'],
            'arsenic': ['arsenic', 'as'],
            'selenium': ['selenium', 'se'],
            'texture': ['texture', 'soil texture', 'clay', 'silt', 'sand'],
            'moisture': ['moisture', 'water content', 'humidity'],
            'bulk_density': ['bulk density', 'bd', 'density'],
            'porosity': ['porosity', 'pore space'],
            'cec': ['cec', 'cation exchange capacity'],
            'base_saturation': ['base saturation', 'bs'],
            'electrical_conductivity': ['ec', 'electrical conductivity', 'salinity']
        }
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process soil analysis PDF and extract data
        """
        try:
            # Extract text from PDF
            text_content = self._extract_text_from_pdf(pdf_path)
            
            # Parse soil parameters
            soil_data = self._parse_soil_parameters(text_content)
            
            # Extract location and date
            location = self._extract_location(text_content)
            analysis_date = self._extract_date(text_content)
            
            # Extract lab information
            lab_info = self._extract_lab_info(text_content)
            
            # Create structured result
            result = {
                'success': True,
                'soil_data': soil_data,
                'location': location,
                'analysis_date': analysis_date,
                'lab_info': lab_info,
                'raw_text': text_content,
                'processed_at': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing PDF: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'processed_at': datetime.now().isoformat()
            }
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF using multiple methods"""
        text_content = ""
        
        try:
            # Method 1: Using pdfplumber (better for tables)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text_content += page.extract_text() or ""
            
            # If pdfplumber fails, try PyPDF2
            if not text_content.strip():
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text()
        
        except Exception as e:
            self.logger.error(f"Error extracting text: {str(e)}")
            raise
        
        return text_content
    
    def _parse_soil_parameters(self, text: str) -> Dict[str, Any]:
        """Parse soil parameters from text"""
        soil_data = {}
        
        for parameter, keywords in self.soil_parameters.items():
            value = self._extract_parameter_value(text, keywords)
            if value is not None:
                soil_data[parameter] = {
                    'value': value['value'],
                    'unit': value['unit'],
                    'status': self._classify_parameter_status(parameter, value['value'])
                }
        
        return soil_data
    
    def _extract_parameter_value(self, text: str, keywords: List[str]) -> Optional[Dict[str, Any]]:
        """Extract parameter value using keyword matching"""
        text_lower = text.lower()
        
        for keyword in keywords:
            # Look for patterns like "pH: 6.5" or "pH = 6.5" or "pH 6.5"
            patterns = [
                rf'{re.escape(keyword)}\s*[:=]\s*([0-9.]+)\s*([a-zA-Z%/%]+)?',
                rf'{re.escape(keyword)}\s+([0-9.]+)\s*([a-zA-Z%/%]+)?',
                rf'([0-9.]+)\s*([a-zA-Z%/%]+)?\s*{re.escape(keyword)}'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    value = float(match.group(1))
                    unit = match.group(2) if match.group(2) else self._get_default_unit(keyword)
                    return {'value': value, 'unit': unit}
        
        return None
    
    def _get_default_unit(self, parameter: str) -> str:
        """Get default unit for parameter"""
        units = {
            'ph': 'pH',
            'nitrogen': 'mg/kg',
            'phosphorus': 'mg/kg',
            'potassium': 'mg/kg',
            'organic_matter': '%',
            'calcium': 'mg/kg',
            'magnesium': 'mg/kg',
            'sulfur': 'mg/kg',
            'zinc': 'mg/kg',
            'iron': 'mg/kg',
            'manganese': 'mg/kg',
            'copper': 'mg/kg',
            'boron': 'mg/kg',
            'molybdenum': 'mg/kg',
            'cobalt': 'mg/kg',
            'nickel': 'mg/kg',
            'lead': 'mg/kg',
            'cadmium': 'mg/kg',
            'chromium': 'mg/kg',
            'mercury': 'mg/kg',
            'arsenic': 'mg/kg',
            'selenium': 'mg/kg',
            'texture': 'texture',
            'moisture': '%',
            'bulk_density': 'g/cm³',
            'porosity': '%',
            'cec': 'cmol/kg',
            'base_saturation': '%',
            'electrical_conductivity': 'dS/m'
        }
        return units.get(parameter, 'unit')
    
    def _classify_parameter_status(self, parameter: str, value: float) -> str:
        """Classify parameter status (low, medium, high, optimal)"""
        classifications = {
            'ph': {
                'optimal': (6.0, 7.5),
                'low': (0, 6.0),
                'high': (7.5, 14)
            },
            'nitrogen': {
                'low': (0, 50),
                'medium': (50, 100),
                'high': (100, 200),
                'very_high': (200, 1000)
            },
            'phosphorus': {
                'low': (0, 15),
                'medium': (15, 30),
                'high': (30, 50),
                'very_high': (50, 1000)
            },
            'potassium': {
                'low': (0, 100),
                'medium': (100, 200),
                'high': (200, 300),
                'very_high': (300, 1000)
            },
            'organic_matter': {
                'low': (0, 2),
                'medium': (2, 4),
                'high': (4, 6),
                'very_high': (6, 100)
            }
        }
        
        if parameter in classifications:
            for status, (min_val, max_val) in classifications[parameter].items():
                if min_val <= value < max_val:
                    return status
        
        return 'unknown'
    
    def _extract_location(self, text: str) -> Optional[Dict[str, str]]:
        """Extract location information from text"""
        location_patterns = [
            r'location\s*[:=]\s*([^\\n]+)',
            r'address\s*[:=]\s*([^\\n]+)',
            r'farm\s*[:=]\s*([^\\n]+)',
            r'field\s*[:=]\s*([^\\n]+)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return {'address': match.group(1).strip()}
        
        return None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """Extract analysis date from text"""
        date_patterns = [
            r'date\s*[:=]\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4})',
            r'analysis\s+date\s*[:=]\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4})',
            r'sample\s+date\s*[:=]\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_lab_info(self, text: str) -> Optional[Dict[str, str]]:
        """Extract laboratory information"""
        lab_info = {}
        
        # Extract lab name
        lab_name_patterns = [
            r'laboratory\s*[:=]\s*([^\\n]+)',
            r'lab\s*[:=]\s*([^\\n]+)',
            r'analyzed\s+by\s*[:=]\s*([^\\n]+)'
        ]
        
        for pattern in lab_name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                lab_info['name'] = match.group(1).strip()
                break
        
        # Extract lab address
        address_patterns = [
            r'address\s*[:=]\s*([^\\n]+)',
            r'location\s*[:=]\s*([^\\n]+)'
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                lab_info['address'] = match.group(1).strip()
                break
        
        return lab_info if lab_info else None
    
    def validate_soil_data(self, soil_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate extracted soil data"""
        validation_result = {
            'is_valid': True,
            'missing_parameters': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Check for essential parameters
        essential_params = ['ph', 'nitrogen', 'phosphorus', 'potassium']
        for param in essential_params:
            if param not in soil_data:
                validation_result['missing_parameters'].append(param)
                validation_result['is_valid'] = False
        
        # Check pH range
        if 'ph' in soil_data:
            ph_value = soil_data['ph']['value']
            if ph_value < 4.0 or ph_value > 9.0:
                validation_result['warnings'].append(f"pH value {ph_value} is outside normal range (4.0-9.0)")
        
        # Check nutrient levels
        if 'nitrogen' in soil_data:
            n_value = soil_data['nitrogen']['value']
            if n_value < 20:
                validation_result['recommendations'].append("Nitrogen levels are very low. Consider adding nitrogen fertilizer.")
            elif n_value > 200:
                validation_result['warnings'].append("Nitrogen levels are very high. Monitor for potential leaching.")
        
        return validation_result
