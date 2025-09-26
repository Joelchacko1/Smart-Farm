# Smart Farm Backend - Soil Analysis & Government Schemes

A comprehensive backend system for soil analysis, weather integration, crop recommendations, government scheme matching, and farming plan generation.

## 🚀 Features

### 🌱 Soil Analysis
- **PDF Processing** - Extract soil data from uploaded PDF files
- **Data Validation** - Validate extracted soil parameters
- **Parameter Analysis** - Analyze pH, nutrients, and soil health
- **Recommendations** - Generate soil improvement suggestions

### 🌤️ Weather Integration
- **Current Weather** - Real-time weather conditions
- **Weather Forecast** - 7-day weather predictions
- **Agricultural Insights** - Weather-based farming recommendations
- **Risk Assessment** - Weather-related risk analysis

### 🌾 Crop Recommendations
- **Intelligent Matching** - Match crops with soil and weather conditions
- **Compatibility Analysis** - Analyze crop-soil-weather compatibility
- **Scoring System** - Rank crops by suitability
- **Detailed Insights** - Provide advantages and considerations

### 🏛️ Government Schemes
- **Scheme Matching** - Match farmers with relevant schemes
- **Eligibility Analysis** - Check scheme eligibility criteria
- **Priority Ranking** - Rank schemes by relevance
- **Application Guidance** - Provide application tips and requirements

### 📋 Farming Plans
- **Detailed Plans** - Generate comprehensive farming plans
- **Phase-wise Activities** - Break down farming into phases
- **Cost Analysis** - Estimate costs and profits
- **Timeline Generation** - Create farming timelines
- **Risk Assessment** - Identify and mitigate risks

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd Smart-Farm/backend

# Install dependencies
pip install -r requirements.txt

# Create uploads directory
mkdir uploads

# Set environment variables
export FLASK_APP=soil_analysis/api.py
export FLASK_ENV=development
```

### Running the Server
```bash
# Development server
python soil_analysis/api.py

# Production server
gunicorn -w 4 -b 0.0.0.0:5001 soil_analysis.api:app
```

## 📡 API Endpoints

### Soil Analysis
- `POST /api/soil-analysis/upload` - Upload and process soil analysis PDF
- `POST /api/soil-analysis/validate` - Validate soil analysis data

### Weather Integration
- `GET /api/weather/current?lat=<latitude>&lon=<longitude>` - Get current weather
- `GET /api/weather/forecast?lat=<latitude>&lon=<longitude>&days=<days>` - Get weather forecast

### Crop Recommendations
- `POST /api/crop-recommendations` - Get crop recommendations based on soil and weather

### Government Schemes
- `POST /api/government-schemes` - Get matching government schemes

### Farming Plans
- `POST /api/farming-plan` - Generate detailed farming plan
- `POST /api/farming-plan/pdf` - Generate PDF of farming plan

### Utility Endpoints
- `GET /api/crops/list` - Get list of available crops
- `GET /api/download/<filename>` - Download generated files
- `GET /api/health` - Health check

## 💡 Usage Examples

### 1. Upload Soil Analysis PDF
```bash
curl -X POST http://localhost:5001/api/soil-analysis/upload \
  -F "file=@soil_analysis.pdf"
```

### 2. Get Current Weather
```bash
curl "http://localhost:5001/api/weather/current?lat=28.6139&lon=77.2090"
```

### 3. Get Crop Recommendations
```bash
curl -X POST http://localhost:5001/api/crop-recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "soil_data": {
      "ph": {"value": 6.5, "unit": "pH"},
      "nitrogen": {"value": 80, "unit": "mg/kg"},
      "phosphorus": {"value": 25, "unit": "mg/kg"},
      "potassium": {"value": 150, "unit": "mg/kg"}
    },
    "weather_data": {
      "temperature": 25,
      "humidity": 65,
      "wind_speed": 5
    }
  }'
```

### 4. Get Government Schemes
```bash
curl -X POST http://localhost:5001/api/government-schemes \
  -H "Content-Type: application/json" \
  -d '{
    "farmer_profile": {
      "land_holding_hectares": 2.5,
      "annual_income": 80000,
      "age": 35,
      "experience": "intermediate"
    }
  }'
```

### 5. Generate Farming Plan
```bash
curl -X POST http://localhost:5001/api/farming-plan \
  -H "Content-Type: application/json" \
  -d '{
    "crop_name": "wheat",
    "soil_data": {...},
    "weather_data": {...},
    "farm_size": 2.0,
    "farmer_experience": "intermediate"
  }'
```

## 🔧 Configuration

### Environment Variables
```bash
# Flask configuration
export FLASK_APP=soil_analysis/api.py
export FLASK_ENV=development

# Weather API (optional)
export WEATHER_API_KEY=your_api_key

# File upload
export MAX_CONTENT_LENGTH=16777216  # 16MB
export UPLOAD_FOLDER=uploads
```

### Database Configuration
The system uses SQLite by default. For production, configure PostgreSQL or MySQL:
```bash
export DATABASE_URL=postgresql://user:password@localhost/smartfarm
```

## 📊 Data Models

### Soil Analysis Data
```json
{
  "ph": {"value": 6.5, "unit": "pH", "status": "optimal"},
  "nitrogen": {"value": 80, "unit": "mg/kg", "status": "medium"},
  "phosphorus": {"value": 25, "unit": "mg/kg", "status": "medium"},
  "potassium": {"value": 150, "unit": "mg/kg", "status": "medium"}
}
```

### Weather Data
```json
{
  "temperature": 25.5,
  "humidity": 65.2,
  "pressure": 1013.2,
  "wind_speed": 3.2,
  "wind_direction": 180,
  "rainfall": 0.0,
  "uv_index": 6.5,
  "cloudiness": 25.0
}
```

### Farmer Profile
```json
{
  "land_holding_hectares": 2.5,
  "annual_income": 80000,
  "age": 35,
  "experience": "intermediate",
  "location": {
    "latitude": 28.6139,
    "longitude": 77.2090
  }
}
```

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/

# Run with coverage
pytest --cov=soil_analysis tests/
```

### Test Data
The system includes mock data for testing:
- Mock weather data for various locations
- Sample soil analysis data
- Test farmer profiles
- Mock government schemes

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "soil_analysis.api:app"]
```

### Production Configuration
```bash
# Use production WSGI server
gunicorn -w 4 -b 0.0.0.0:5001 soil_analysis.api:app

# With environment variables
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:password@localhost/smartfarm
```

## 📈 Performance

### Optimization Tips
1. **File Upload Limits** - Set appropriate file size limits
2. **Caching** - Implement Redis caching for weather data
3. **Database Indexing** - Add indexes for frequently queried fields
4. **Async Processing** - Use Celery for heavy processing tasks

### Monitoring
- Health check endpoint: `/api/health`
- Logging configuration in `api.py`
- Error handling and reporting

## 🔒 Security

### Security Measures
1. **File Upload Validation** - Validate file types and sizes
2. **Input Sanitization** - Sanitize all user inputs
3. **Rate Limiting** - Implement rate limiting for API endpoints
4. **CORS Configuration** - Configure CORS properly
5. **Error Handling** - Don't expose sensitive information in errors

## 📞 Support

### Common Issues
1. **File Upload Fails** - Check file size and type
2. **Weather API Errors** - Verify API key and network connection
3. **PDF Processing Errors** - Ensure PDF is not corrupted
4. **Database Connection** - Check database configuration

### Debugging
```bash
# Enable debug mode
export FLASK_DEBUG=1

# Check logs
tail -f logs/app.log

# Test endpoints
curl -X GET http://localhost:5001/api/health
```

## 🔄 Integration

### Frontend Integration
The backend is designed to work with the Smart Farm frontend. Key integration points:

1. **File Upload** - Use multipart/form-data for PDF uploads
2. **API Responses** - All responses follow consistent JSON format
3. **Error Handling** - Proper HTTP status codes and error messages
4. **CORS** - Configured for frontend domain

### Third-party Integrations
- **Weather APIs** - OpenWeatherMap, WeatherAPI
- **Government Databases** - Scheme information and eligibility
- **PDF Processing** - PyPDF2, pdfplumber
- **File Storage** - Local filesystem (configurable for cloud storage)

---

**Happy Farming! 🌱**
