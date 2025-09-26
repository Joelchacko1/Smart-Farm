#!/usr/bin/env python3
"""
Smart Farm Backend Demo
Demonstrates the soil analysis and government scheme features
"""

import json
from datetime import datetime
from typing import Dict, Any

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library not found.")
    print("Please install it using: pip install requests")
    exit(1)

# Demo configuration
BASE_URL = "http://localhost:5001"
DEMO_DATA = {
    "soil_analysis": {
        "ph": {"value": 6.5, "unit": "pH", "status": "optimal"},
        "nitrogen": {"value": 80, "unit": "mg/kg", "status": "medium"},
        "phosphorus": {"value": 25, "unit": "mg/kg", "status": "medium"},
        "potassium": {"value": 150, "unit": "mg/kg", "status": "medium"},
        "organic_matter": {"value": 3.2, "unit": "%", "status": "good"}
    },
    "weather_data": {
        "temperature": 25.5,
        "humidity": 65.2,
        "pressure": 1013.2,
        "wind_speed": 3.2,
        "wind_direction": 180,
        "rainfall": 0.0,
        "uv_index": 6.5,
        "cloudiness": 25.0
    },
    "farmer_profile": {
        "land_holding_hectares": 2.5,
        "annual_income": 80000,
        "age": 35,
        "experience": "intermediate",
        "location": {
            "latitude": 28.6139,
            "longitude": 77.2090
        }
    }
}

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_weather_integration():
    """Test weather integration"""
    print("\n🌤️ Testing Weather Integration...")
    try:
        # Test current weather
        response = requests.get(f"{BASE_URL}/api/weather/current?lat=28.6139&lon=77.2090")
        if response.status_code == 200:
            data = response.json()
            print("✅ Current weather fetched successfully")
            print(f"   Temperature: {data['data']['weather_data']['temperature']}°C")
            print(f"   Humidity: {data['data']['weather_data']['humidity']}%")
        else:
            print(f"❌ Weather API failed: {response.status_code}")
            return False
        
        # Test weather forecast
        response = requests.get(f"{BASE_URL}/api/weather/forecast?lat=28.6139&lon=77.2090&days=7")
        if response.status_code == 200:
            data = response.json()
            print("✅ Weather forecast fetched successfully")
            print(f"   Forecast days: {len(data['data']['forecast'])}")
        else:
            print(f"❌ Weather forecast failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Weather integration error: {str(e)}")
        return False

def test_crop_recommendations():
    """Test crop recommendations"""
    print("\n🌾 Testing Crop Recommendations...")
    try:
        payload = {
            "soil_data": DEMO_DATA["soil_analysis"],
            "weather_data": DEMO_DATA["weather_data"],
            "user_preferences": {
                "preferred_categories": ["cereal", "vegetable"],
                "preferred_seasons": ["winter", "summer"]
            }
        }
        
        response = requests.post(f"{BASE_URL}/api/crop-recommendations", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Crop recommendations generated successfully")
            recommendations = data['data']['recommendations']
            print(f"   Found {len(recommendations)} crop recommendations")
            
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec['crop_name']} - Score: {rec['score']} - Suitability: {rec['suitability']}")
        else:
            print(f"❌ Crop recommendations failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Crop recommendations error: {str(e)}")
        return False

def test_government_schemes():
    """Test government scheme matching"""
    print("\n🏛️ Testing Government Scheme Matching...")
    try:
        payload = {
            "farmer_profile": DEMO_DATA["farmer_profile"],
            "soil_data": DEMO_DATA["soil_analysis"],
            "crop_preferences": ["wheat", "rice", "tomato"]
        }
        
        response = requests.post(f"{BASE_URL}/api/government-schemes", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Government schemes matched successfully")
            recommendations = data['data']['recommendations']
            print(f"   Found {len(recommendations)} eligible schemes")
            
            for i, scheme in enumerate(recommendations[:3], 1):
                print(f"   {i}. {scheme['scheme_name']} - Priority: {scheme['priority_level']}")
                print(f"      Benefit: ₹{scheme['benefit_amount']:,} - Category: {scheme['category']}")
        else:
            print(f"❌ Government schemes failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Government schemes error: {str(e)}")
        return False

def test_farming_plan():
    """Test farming plan generation"""
    print("\n📋 Testing Farming Plan Generation...")
    try:
        payload = {
            "crop_name": "wheat",
            "soil_data": DEMO_DATA["soil_analysis"],
            "weather_data": DEMO_DATA["weather_data"],
            "farm_size": 2.0,
            "farmer_experience": "intermediate"
        }
        
        response = requests.post(f"{BASE_URL}/api/farming-plan", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Farming plan generated successfully")
            plan = data['data']['farming_plan']
            print(f"   Crop: {plan['name']}")
            print(f"   Duration: {plan['duration_days']} days")
            print(f"   Total Cost: ₹{plan['total_cost_estimate']:,}")
            print(f"   Expected Yield: {plan['expected_yield']}")
            print(f"   Market Price: {plan['market_price']}")
            
            # Show phases
            phases = plan['phases']
            print(f"   Farming Phases: {len(phases)}")
            for phase_name, phase_data in phases.items():
                print(f"     - {phase_name}: {phase_data['duration_days']} days, ₹{phase_data['cost_estimate']:,}")
        else:
            print(f"❌ Farming plan failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Farming plan error: {str(e)}")
        return False

def test_farming_plan_pdf():
    """Test farming plan PDF generation"""
    print("\n📄 Testing Farming Plan PDF Generation...")
    try:
        payload = {
            "crop_name": "wheat",
            "soil_data": DEMO_DATA["soil_analysis"],
            "weather_data": DEMO_DATA["weather_data"],
            "farm_size": 2.0,
            "farmer_experience": "intermediate"
        }
        
        response = requests.post(f"{BASE_URL}/api/farming-plan/pdf", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Farming plan PDF generated successfully")
            print(f"   PDF URL: {data['pdf_url']}")
            print("   You can download the PDF using the provided URL")
        else:
            print(f"❌ Farming plan PDF failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Farming plan PDF error: {str(e)}")
        return False

def test_crops_list():
    """Test crops list endpoint"""
    print("\n🌱 Testing Crops List...")
    try:
        response = requests.get(f"{BASE_URL}/api/crops/list")
        if response.status_code == 200:
            data = response.json()
            print("✅ Crops list fetched successfully")
            crops = data['crops']
            print(f"   Available crops: {len(crops)}")
            
            for crop in crops[:5]:
                print(f"   - {crop['name']} ({crop['scientific_name']}) - {crop['category']}")
        else:
            print(f"❌ Crops list failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Crops list error: {str(e)}")
        return False

def test_soil_analysis_validation():
    """Test soil analysis validation"""
    print("\n🧪 Testing Soil Analysis Validation...")
    try:
        payload = {
            "soil_data": DEMO_DATA["soil_analysis"]
        }
        
        response = requests.post(f"{BASE_URL}/api/soil-analysis/validate", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Soil analysis validation completed")
            validation = data['validation']
            print(f"   Overall Health: {validation['overall_health']}")
            print(f"   Missing Parameters: {len(validation['missing_parameters'])}")
            print(f"   Warnings: {len(validation['warnings'])}")
            print(f"   Recommendations: {len(validation['recommendations'])}")
        else:
            print(f"❌ Soil analysis validation failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Soil analysis validation error: {str(e)}")
        return False

def run_comprehensive_demo():
    """Run comprehensive demo of all features"""
    print("🚀 Smart Farm Backend Demo")
    print("=" * 50)
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    print()
    
    # Test results
    results = {}
    
    # Run all tests
    results['health_check'] = test_health_check()
    results['weather_integration'] = test_weather_integration()
    results['crop_recommendations'] = test_crop_recommendations()
    results['government_schemes'] = test_government_schemes()
    results['farming_plan'] = test_farming_plan()
    results['farming_plan_pdf'] = test_farming_plan_pdf()
    results['crops_list'] = test_crops_list()
    results['soil_analysis_validation'] = test_soil_analysis_validation()
    
    # Summary
    print("\n📊 Demo Summary")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\nTest Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    if failed_tests > 0:
        print(f"\n⚠️  {failed_tests} test(s) failed. Please check the server logs.")
    else:
        print("\n🎉 All tests passed! The backend is working perfectly.")
    
    print(f"\nDemo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main function"""
    try:
        run_comprehensive_demo()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo error: {str(e)}")

if __name__ == "__main__":
    main()
