"""
Soil Analysis API Endpoints
RESTful API for soil analysis, weather integration, and farming recommendations
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
from typing import Dict, Any
import logging

# Import our modules
from pdf_processor import SoilAnalysisPDFProcessor
from weather_integration import WeatherService
from crop_recommendations import CropRecommendationEngine
from government_schemes import GovernmentSchemeMatcher
from farming_plans import FarmingPlanGenerator

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
pdf_processor = SoilAnalysisPDFProcessor()
weather_service = WeatherService()
crop_engine = CropRecommendationEngine()
scheme_matcher = GovernmentSchemeMatcher()
plan_generator = FarmingPlanGenerator()

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/soil-analysis/upload', methods=['POST'])
def upload_soil_analysis():
    """Upload and process soil analysis PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if file and allowed_file(file.filename):
            # Save uploaded file
            filename = f"soil_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process PDF
            result = pdf_processor.process_pdf(filepath)
            
            if result['success']:
                # Validate soil data
                validation = pdf_processor.validate_soil_data(result['soil_data'])
                result['validation'] = validation
                
                return jsonify({
                    'success': True,
                    'message': 'Soil analysis processed successfully',
                    'data': result
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': result['error']
                }), 500
        
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Only PDF files are allowed.'
            }), 400
    
    except Exception as e:
        logger.error(f"Error processing soil analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/weather/current', methods=['GET'])
def get_current_weather():
    """Get current weather conditions"""
    try:
        latitude = float(request.args.get('lat', 0))
        longitude = float(request.args.get('lon', 0))
        
        if latitude == 0 and longitude == 0:
            return jsonify({
                'success': False,
                'error': 'Latitude and longitude are required'
            }), 400
        
        weather_data = weather_service.get_current_weather(latitude, longitude)
        
        return jsonify({
            'success': True,
            'data': weather_data
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/weather/forecast', methods=['GET'])
def get_weather_forecast():
    """Get weather forecast"""
    try:
        latitude = float(request.args.get('lat', 0))
        longitude = float(request.args.get('lon', 0))
        days = int(request.args.get('days', 7))
        
        if latitude == 0 and longitude == 0:
            return jsonify({
                'success': False,
                'error': 'Latitude and longitude are required'
            }), 400
        
        forecast_data = weather_service.get_weather_forecast(latitude, longitude, days)
        
        return jsonify({
            'success': True,
            'data': forecast_data
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching weather forecast: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/crop-recommendations', methods=['POST'])
def get_crop_recommendations():
    """Get crop recommendations based on soil and weather data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request data is required'
            }), 400
        
        soil_data = data.get('soil_data', {})
        weather_data = data.get('weather_data', {})
        user_preferences = data.get('user_preferences', {})
        
        if not soil_data or not weather_data:
            return jsonify({
                'success': False,
                'error': 'Soil data and weather data are required'
            }), 400
        
        recommendations = crop_engine.get_crop_recommendations(
            soil_data, weather_data, user_preferences
        )
        
        return jsonify({
            'success': True,
            'data': recommendations
        }), 200
    
    except Exception as e:
        logger.error(f"Error generating crop recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/government-schemes', methods=['POST'])
def get_government_schemes():
    """Get matching government schemes"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request data is required'
            }), 400
        
        farmer_profile = data.get('farmer_profile', {})
        soil_data = data.get('soil_data', {})
        crop_preferences = data.get('crop_preferences', [])
        
        if not farmer_profile:
            return jsonify({
                'success': False,
                'error': 'Farmer profile is required'
            }), 400
        
        schemes = scheme_matcher.match_schemes(farmer_profile, soil_data, crop_preferences)
        
        return jsonify({
            'success': True,
            'data': schemes
        }), 200
    
    except Exception as e:
        logger.error(f"Error matching government schemes: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/farming-plan', methods=['POST'])
def generate_farming_plan():
    """Generate detailed farming plan for selected crop"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request data is required'
            }), 400
        
        crop_name = data.get('crop_name')
        soil_data = data.get('soil_data', {})
        weather_data = data.get('weather_data', {})
        farm_size = float(data.get('farm_size', 1.0))
        farmer_experience = data.get('farmer_experience', 'beginner')
        
        if not crop_name:
            return jsonify({
                'success': False,
                'error': 'Crop name is required'
            }), 400
        
        farming_plan = plan_generator.generate_farming_plan(
            crop_name, soil_data, weather_data, farm_size, farmer_experience
        )
        
        return jsonify({
            'success': True,
            'data': farming_plan
        }), 200
    
    except Exception as e:
        logger.error(f"Error generating farming plan: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/farming-plan/pdf', methods=['POST'])
def generate_farming_plan_pdf():
    """Generate PDF of farming plan"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request data is required'
            }), 400
        
        crop_name = data.get('crop_name')
        soil_data = data.get('soil_data', {})
        weather_data = data.get('weather_data', {})
        farm_size = float(data.get('farm_size', 1.0))
        farmer_experience = data.get('farmer_experience', 'beginner')
        
        if not crop_name:
            return jsonify({
                'success': False,
                'error': 'Crop name is required'
            }), 400
        
        # Generate farming plan
        farming_plan = plan_generator.generate_farming_plan(
            crop_name, soil_data, weather_data, farm_size, farmer_experience
        )
        
        if not farming_plan['success']:
            return jsonify({
                'success': False,
                'error': farming_plan['error']
            }), 500
        
        # Generate PDF (simplified - in real implementation, use reportlab or similar)
        pdf_filename = f"farming_plan_{crop_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        
        # Create a simple text-based PDF content (in real implementation, use proper PDF library)
        pdf_content = f"""
        FARMING PLAN FOR {crop_name.upper()}
        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        FARMING PLAN DETAILS:
        {json.dumps(farming_plan, indent=2)}
        """
        
        with open(pdf_path, 'w') as f:
            f.write(pdf_content)
        
        return jsonify({
            'success': True,
            'message': 'Farming plan PDF generated successfully',
            'pdf_url': f'/api/download/{pdf_filename}',
            'data': farming_plan
        }), 200
    
    except Exception as e:
        logger.error(f"Error generating farming plan PDF: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download generated files"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
    
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/soil-analysis/validate', methods=['POST'])
def validate_soil_analysis():
    """Validate soil analysis data"""
    try:
        data = request.get_json()
        
        if not data or 'soil_data' not in data:
            return jsonify({
                'success': False,
                'error': 'Soil data is required'
            }), 400
        
        soil_data = data['soil_data']
        validation = pdf_processor.validate_soil_data(soil_data)
        
        return jsonify({
            'success': True,
            'validation': validation
        }), 200
    
    except Exception as e:
        logger.error(f"Error validating soil analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/crops/list', methods=['GET'])
def get_crops_list():
    """Get list of available crops"""
    try:
        crops = [
            {'name': 'Wheat', 'scientific_name': 'Triticum aestivum', 'category': 'cereal'},
            {'name': 'Rice', 'scientific_name': 'Oryza sativa', 'category': 'cereal'},
            {'name': 'Corn', 'scientific_name': 'Zea mays', 'category': 'cereal'},
            {'name': 'Tomato', 'scientific_name': 'Solanum lycopersicum', 'category': 'vegetable'},
            {'name': 'Potato', 'scientific_name': 'Solanum tuberosum', 'category': 'vegetable'},
            {'name': 'Soybean', 'scientific_name': 'Glycine max', 'category': 'legume'},
            {'name': 'Cotton', 'scientific_name': 'Gossypium hirsutum', 'category': 'fiber'},
            {'name': 'Sugarcane', 'scientific_name': 'Saccharum officinarum', 'category': 'cash_crop'}
        ]
        
        return jsonify({
            'success': True,
            'crops': crops
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting crops list: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'soil-analysis-api'
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
