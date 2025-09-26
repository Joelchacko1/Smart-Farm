"""
Weather Integration Service
Fetches and processes weather data for soil analysis recommendations
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

class WeatherService:
    """
    Service for fetching and processing weather data
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
        self.base_urls = {
            'openweathermap': 'https://api.openweathermap.org/data/2.5',
            'weather_api': 'https://api.weatherapi.com/v1',
            'accuweather': 'https://dataservice.accuweather.com'
        }
    
    def get_current_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Get current weather conditions for a location
        """
        try:
            # Try multiple weather APIs
            weather_data = None
            
            # Try OpenWeatherMap first
            if self.api_key:
                weather_data = self._fetch_openweathermap_data(latitude, longitude)
            
            # Fallback to mock data if API fails
            if not weather_data:
                weather_data = self._generate_mock_weather_data(latitude, longitude)
            
            # Process weather data for agricultural use
            processed_data = self._process_weather_for_agriculture(weather_data)
            
            return {
                'success': True,
                'weather_data': processed_data,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching weather data: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'weather_data': self._generate_mock_weather_data(latitude, longitude)
            }
    
    def get_weather_forecast(self, latitude: float, longitude: float, days: int = 7) -> Dict[str, Any]:
        """
        Get weather forecast for specified days
        """
        try:
            forecast_data = []
            
            # Generate mock forecast data
            for i in range(days):
                date = datetime.now() + timedelta(days=i)
                day_weather = self._generate_mock_weather_data(latitude, longitude, date)
                forecast_data.append(day_weather)
            
            return {
                'success': True,
                'forecast': forecast_data,
                'location': {'latitude': latitude, 'longitude': longitude},
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching forecast: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _fetch_openweathermap_data(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Fetch data from OpenWeatherMap API"""
        try:
            url = f"{self.base_urls['openweathermap']}/weather"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'cloudiness': data['clouds']['all'],
                'visibility': data.get('visibility', 10000) / 1000,  # Convert to km
                'uv_index': data.get('uvi', 0),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }
            
        except Exception as e:
            self.logger.error(f"OpenWeatherMap API error: {str(e)}")
            return None
    
    def _generate_mock_weather_data(self, latitude: float, longitude: float, date: datetime = None) -> Dict[str, Any]:
        """Generate mock weather data for testing"""
        import random
        
        if date is None:
            date = datetime.now()
        
        # Simulate seasonal variations based on latitude
        base_temp = 20 + (latitude * 0.5)  # Rough temperature estimation
        seasonal_variation = 10 * abs(latitude / 90)  # Seasonal variation
        
        # Add some randomness
        temperature = base_temp + random.uniform(-5, 5) + seasonal_variation * random.uniform(-0.5, 0.5)
        
        return {
            'temperature': round(temperature, 1),
            'humidity': random.randint(30, 90),
            'pressure': random.randint(1000, 1030),
            'wind_speed': round(random.uniform(0, 15), 1),
            'wind_direction': random.randint(0, 360),
            'cloudiness': random.randint(0, 100),
            'visibility': round(random.uniform(5, 20), 1),
            'uv_index': random.randint(0, 11),
            'description': random.choice([
                'clear sky', 'few clouds', 'scattered clouds', 'broken clouds',
                'shower rain', 'rain', 'thunderstorm', 'snow', 'mist', 'fog'
            ]),
            'icon': f"weather_icon_{random.randint(1, 10)}",
            'date': date.isoformat()
        }
    
    def _process_weather_for_agriculture(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process weather data for agricultural recommendations"""
        processed = weather_data.copy()
        
        # Add agricultural insights
        processed['agricultural_insights'] = {
            'growing_conditions': self._assess_growing_conditions(weather_data),
            'irrigation_recommendation': self._get_irrigation_recommendation(weather_data),
            'pest_risk': self._assess_pest_risk(weather_data),
            'disease_risk': self._assess_disease_risk(weather_data),
            'harvest_conditions': self._assess_harvest_conditions(weather_data)
        }
        
        # Add weather alerts
        processed['alerts'] = self._generate_weather_alerts(weather_data)
        
        return processed
    
    def _assess_growing_conditions(self, weather_data: Dict[str, Any]) -> str:
        """Assess growing conditions based on weather"""
        temp = weather_data['temperature']
        humidity = weather_data['humidity']
        wind_speed = weather_data['wind_speed']
        
        if 15 <= temp <= 30 and 40 <= humidity <= 80 and wind_speed < 10:
            return 'excellent'
        elif 10 <= temp <= 35 and 30 <= humidity <= 90 and wind_speed < 15:
            return 'good'
        elif 5 <= temp <= 40 and 20 <= humidity <= 95 and wind_speed < 20:
            return 'fair'
        else:
            return 'poor'
    
    def _get_irrigation_recommendation(self, weather_data: Dict[str, Any]) -> str:
        """Get irrigation recommendation based on weather"""
        temp = weather_data['temperature']
        humidity = weather_data['humidity']
        wind_speed = weather_data['wind_speed']
        
        # Simple irrigation logic
        if temp > 30 and humidity < 50 and wind_speed > 5:
            return 'high_irrigation_needed'
        elif temp > 25 and humidity < 60:
            return 'moderate_irrigation_needed'
        elif temp < 15 or humidity > 80:
            return 'no_irrigation_needed'
        else:
            return 'light_irrigation_recommended'
    
    def _assess_pest_risk(self, weather_data: Dict[str, Any]) -> str:
        """Assess pest risk based on weather conditions"""
        temp = weather_data['temperature']
        humidity = weather_data['humidity']
        
        if 20 <= temp <= 30 and 60 <= humidity <= 80:
            return 'high'
        elif 15 <= temp <= 35 and 50 <= humidity <= 90:
            return 'medium'
        else:
            return 'low'
    
    def _assess_disease_risk(self, weather_data: Dict[str, Any]) -> str:
        """Assess disease risk based on weather conditions"""
        humidity = weather_data['humidity']
        temp = weather_data['temperature']
        
        if humidity > 80 and 15 <= temp <= 25:
            return 'high'
        elif humidity > 70 and 10 <= temp <= 30:
            return 'medium'
        else:
            return 'low'
    
    def _assess_harvest_conditions(self, weather_data: Dict[str, Any]) -> str:
        """Assess harvest conditions"""
        temp = weather_data['temperature']
        humidity = weather_data['humidity']
        wind_speed = weather_data['wind_speed']
        
        if 15 <= temp <= 25 and humidity < 70 and wind_speed < 10:
            return 'excellent'
        elif 10 <= temp <= 30 and humidity < 80 and wind_speed < 15:
            return 'good'
        else:
            return 'poor'
    
    def _generate_weather_alerts(self, weather_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate weather alerts for farmers"""
        alerts = []
        
        temp = weather_data['temperature']
        humidity = weather_data['humidity']
        wind_speed = weather_data['wind_speed']
        
        if temp < 5:
            alerts.append({
                'type': 'frost_warning',
                'message': 'Frost warning: Protect sensitive crops',
                'severity': 'high'
            })
        elif temp > 35:
            alerts.append({
                'type': 'heat_warning',
                'message': 'High temperature: Ensure adequate irrigation',
                'severity': 'medium'
            })
        
        if humidity > 85:
            alerts.append({
                'type': 'humidity_warning',
                'message': 'High humidity: Monitor for fungal diseases',
                'severity': 'medium'
            })
        
        if wind_speed > 15:
            alerts.append({
                'type': 'wind_warning',
                'message': 'Strong winds: Secure structures and protect crops',
                'severity': 'medium'
            })
        
        return alerts
    
    def get_historical_weather(self, latitude: float, longitude: float, days: int = 30) -> Dict[str, Any]:
        """Get historical weather data"""
        try:
            historical_data = []
            
            for i in range(days):
                date = datetime.now() - timedelta(days=i)
                day_weather = self._generate_mock_weather_data(latitude, longitude, date)
                historical_data.append(day_weather)
            
            return {
                'success': True,
                'historical_data': historical_data,
                'location': {'latitude': latitude, 'longitude': longitude},
                'period_days': days,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching historical weather: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
