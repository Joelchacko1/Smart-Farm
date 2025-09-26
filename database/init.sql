-- Smart Farm Database Initialization Script
-- This script initializes the database with essential data

-- Insert default sensor types
INSERT INTO sensor_types (name, unit, data_type, min_value, max_value, description) VALUES
('Temperature', '°C', 'numeric', -40, 60, 'Air temperature sensor'),
('Humidity', '%', 'numeric', 0, 100, 'Relative humidity sensor'),
('Soil Moisture', '%', 'numeric', 0, 100, 'Soil moisture content sensor'),
('pH Level', 'pH', 'numeric', 0, 14, 'Soil pH level sensor'),
('Light Intensity', 'lux', 'numeric', 0, 100000, 'Light intensity sensor'),
('Wind Speed', 'm/s', 'numeric', 0, 50, 'Wind speed sensor'),
('Rainfall', 'mm', 'numeric', 0, 200, 'Rainfall measurement sensor'),
('Pressure', 'hPa', 'numeric', 800, 1200, 'Atmospheric pressure sensor'),
('CO2 Level', 'ppm', 'numeric', 300, 2000, 'Carbon dioxide level sensor'),
('Nitrogen', 'ppm', 'numeric', 0, 1000, 'Soil nitrogen content sensor'),
('Phosphorus', 'ppm', 'numeric', 0, 1000, 'Soil phosphorus content sensor'),
('Potassium', 'ppm', 'numeric', 0, 1000, 'Soil potassium content sensor');

-- Insert common crop types
INSERT INTO crop_types (name, scientific_name, category, planting_season, harvest_days, water_requirements, temperature_min, temperature_max, ph_min, ph_max) VALUES
('Tomato', 'Solanum lycopersicum', 'vegetable', 'Spring', 75, 2.5, 18, 30, 6.0, 6.8),
('Lettuce', 'Lactuca sativa', 'vegetable', 'Spring/Fall', 45, 1.0, 10, 25, 6.0, 7.0),
('Corn', 'Zea mays', 'grain', 'Spring', 90, 3.0, 15, 35, 5.8, 7.0),
('Wheat', 'Triticum aestivum', 'grain', 'Fall', 120, 2.0, 5, 25, 6.0, 7.5),
('Potato', 'Solanum tuberosum', 'vegetable', 'Spring', 100, 2.5, 10, 25, 4.5, 6.5),
('Carrot', 'Daucus carota', 'vegetable', 'Spring/Fall', 70, 1.5, 10, 25, 5.5, 7.0),
('Strawberry', 'Fragaria × ananassa', 'fruit', 'Spring', 60, 2.0, 15, 25, 5.5, 6.5),
('Basil', 'Ocimum basilicum', 'herb', 'Spring/Summer', 30, 1.0, 20, 30, 6.0, 7.5),
('Bell Pepper', 'Capsicum annuum', 'vegetable', 'Spring', 80, 2.0, 18, 30, 6.0, 6.8),
('Cucumber', 'Cucumis sativus', 'vegetable', 'Spring/Summer', 55, 2.5, 20, 30, 5.5, 7.0);

-- Create a default admin user (password: admin123 - should be changed in production)
INSERT INTO users (username, email, password_hash, first_name, last_name, role) VALUES
('admin', 'admin@smartfarm.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/9.8K.2K', 'System', 'Administrator', 'admin');

-- Create a sample farm
INSERT INTO farms (name, location, latitude, longitude, area_hectares, owner_id) VALUES
('Green Valley Farm', '123 Farm Road, Agricultural District', 40.7128, -74.0060, 25.5, 1);

-- Create sample zones for the farm
INSERT INTO zones (farm_id, name, zone_type, area_square_meters, description) VALUES
(1, 'North Field', 'field', 10000, 'Main crop field for seasonal vegetables'),
(1, 'South Greenhouse', 'greenhouse', 500, 'Controlled environment for year-round growing'),
(1, 'Orchard Section', 'orchard', 2000, 'Fruit trees and berry bushes'),
(1, 'Storage Building', 'storage', 200, 'Equipment and harvest storage');

-- Create sample sensors for the zones
INSERT INTO sensors (zone_id, sensor_type_id, name, serial_number, location_description, installation_date, status) VALUES
(1, 1, 'North Field Temperature', 'TEMP-001', 'Center of North Field', '2024-01-15', 'active'),
(1, 2, 'North Field Humidity', 'HUM-001', 'Center of North Field', '2024-01-15', 'active'),
(1, 3, 'North Field Soil Moisture', 'SM-001', 'North Field Zone A', '2024-01-15', 'active'),
(1, 4, 'North Field pH', 'PH-001', 'North Field Zone A', '2024-01-15', 'active'),
(2, 1, 'Greenhouse Temperature', 'TEMP-002', 'Greenhouse Center', '2024-01-20', 'active'),
(2, 2, 'Greenhouse Humidity', 'HUM-002', 'Greenhouse Center', '2024-01-20', 'active'),
(2, 3, 'Greenhouse Soil Moisture', 'SM-002', 'Greenhouse Zone 1', '2024-01-20', 'active'),
(2, 5, 'Greenhouse Light', 'LIGHT-001', 'Greenhouse Center', '2024-01-20', 'active');

-- Create sample irrigation systems
INSERT INTO irrigation_systems (zone_id, name, system_type, capacity_liters_per_hour, status, installation_date) VALUES
(1, 'North Field Drip System', 'drip', 500, 'active', '2024-01-10'),
(2, 'Greenhouse Sprinkler', 'sprinkler', 200, 'active', '2024-01-15'),
(3, 'Orchard Irrigation', 'drip', 300, 'active', '2024-01-12');

-- Create sample equipment
INSERT INTO equipment (farm_id, name, equipment_type, model, serial_number, purchase_date, status) VALUES
(1, 'Main Tractor', 'tractor', 'John Deere 6120R', 'JD-6120R-001', '2023-06-15', 'active'),
(1, 'Harvest Combine', 'harvester', 'Case IH 2388', 'CI-2388-001', '2023-08-20', 'active'),
(1, 'Irrigation Pump', 'irrigation', 'Grundfos CR 32-4', 'GF-CR32-001', '2023-07-10', 'active'),
(1, 'Weather Station', 'sensor', 'Davis Vantage Pro2', 'DV-VP2-001', '2023-09-01', 'active');

-- Create sample crops
INSERT INTO crops (zone_id, crop_type_id, variety, planting_date, expected_harvest_date, quantity_planted, status) VALUES
(1, 1, 'Roma', '2024-03-15', '2024-06-01', 200, 'growing'),
(1, 2, 'Butterhead', '2024-04-01', '2024-05-15', 500, 'growing'),
(2, 1, 'Cherry', '2024-02-01', '2024-04-15', 100, 'ready_harvest'),
(2, 7, 'Sweet Charlie', '2024-01-15', '2024-03-15', 150, 'harvested'),
(3, 6, 'Nantes', '2024-03-01', '2024-05-15', 300, 'growing');

-- Insert sample weather data (last 7 days)
INSERT INTO weather_data (farm_id, temperature, humidity, pressure, wind_speed, wind_direction, rainfall, uv_index, cloud_cover, source) VALUES
(1, 22.5, 65.2, 1013.2, 3.2, 180, 0.0, 6.5, 25.0, 'station'),
(1, 24.1, 58.7, 1012.8, 4.1, 195, 0.0, 7.2, 15.0, 'station'),
(1, 20.8, 72.3, 1014.1, 2.8, 165, 2.5, 4.8, 80.0, 'station'),
(1, 18.5, 78.9, 1015.3, 1.9, 120, 5.2, 3.1, 95.0, 'station'),
(1, 26.3, 45.2, 1011.5, 5.2, 210, 0.0, 8.1, 5.0, 'station'),
(1, 28.7, 42.1, 1010.8, 6.1, 225, 0.0, 8.9, 0.0, 'station'),
(1, 25.9, 48.6, 1012.2, 4.3, 200, 0.0, 7.8, 10.0, 'station');

-- Create sample sensor data (last 24 hours for active sensors)
INSERT INTO sensor_data (sensor_id, value, quality_score) VALUES
-- Temperature sensor data
(1, 22.3, 0.95), (1, 21.8, 0.97), (1, 20.5, 0.96), (1, 19.2, 0.98),
(1, 18.7, 0.99), (1, 17.9, 0.97), (1, 18.3, 0.96), (1, 19.8, 0.98),
(1, 21.2, 0.97), (1, 22.7, 0.95), (1, 24.1, 0.96), (1, 25.3, 0.94),
(1, 26.8, 0.93), (1, 27.2, 0.92), (1, 26.5, 0.94), (1, 25.1, 0.95),
(1, 23.8, 0.96), (1, 22.4, 0.97), (1, 21.1, 0.98), (1, 20.3, 0.97),
(1, 19.7, 0.98), (1, 19.1, 0.99), (1, 18.8, 0.98), (1, 18.5, 0.97),

-- Humidity sensor data
(2, 65.2, 0.94), (2, 67.8, 0.93), (2, 70.1, 0.95), (2, 72.3, 0.96),
(2, 74.5, 0.97), (2, 76.2, 0.98), (2, 75.8, 0.97), (2, 73.4, 0.96),
(2, 70.9, 0.95), (2, 68.3, 0.94), (2, 65.7, 0.93), (2, 63.2, 0.92),
(2, 60.8, 0.91), (2, 58.4, 0.90), (2, 56.1, 0.89), (2, 54.3, 0.88),
(2, 52.8, 0.87), (2, 51.6, 0.86), (2, 50.9, 0.85), (2, 51.2, 0.86),
(2, 52.1, 0.87), (2, 53.8, 0.88), (2, 56.2, 0.89), (2, 58.7, 0.90);

-- Create sample irrigation events
INSERT INTO irrigation_events (irrigation_system_id, start_time, end_time, duration_minutes, water_used_liters, trigger_type, notes) VALUES
(1, '2024-01-20 06:00:00', '2024-01-20 06:30:00', 30, 250, 'scheduled', 'Morning irrigation for North Field'),
(2, '2024-01-20 07:00:00', '2024-01-20 07:15:00', 15, 50, 'sensor', 'Greenhouse irrigation triggered by low soil moisture'),
(1, '2024-01-21 06:00:00', '2024-01-21 06:45:00', 45, 375, 'scheduled', 'Extended irrigation due to dry conditions'),
(3, '2024-01-21 08:00:00', '2024-01-21 08:20:00', 20, 100, 'manual', 'Manual orchard irrigation');

-- Create sample applications
INSERT INTO applications (zone_id, application_type, product_name, active_ingredient, quantity_applied, unit, application_method, application_date, weather_conditions, notes, created_by) VALUES
(1, 'fertilizer', 'NPK 15-15-15', 'Nitrogen-Phosphorus-Potassium', 50, 'kg', 'spray', '2024-01-15', 'Clear, 22°C, light wind', 'Spring fertilization for North Field', 1),
(2, 'pesticide', 'Neem Oil', 'Azadirachtin', 2, 'liters', 'spray', '2024-01-18', 'Overcast, 18°C, no wind', 'Organic pest control in greenhouse', 1),
(1, 'herbicide', 'Roundup', 'Glyphosate', 1, 'liter', 'spray', '2024-01-10', 'Sunny, 25°C, light wind', 'Pre-planting weed control', 1);

-- Create sample harvest records
INSERT INTO harvests (crop_id, harvest_date, quantity_harvested, unit, quality_grade, price_per_unit, total_value, storage_location, notes) VALUES
(4, '2024-03-15', 45.5, 'kg', 'A', 8.50, 386.75, 'Cold Storage A', 'Excellent quality strawberries'),
(4, '2024-03-20', 12.3, 'kg', 'B', 6.50, 79.95, 'Cold Storage A', 'Second harvest, slightly smaller berries');

-- Create sample maintenance records
INSERT INTO maintenance_records (equipment_id, maintenance_type, description, maintenance_date, cost, technician, notes, created_by) VALUES
(1, 'routine', 'Regular oil change and filter replacement', '2024-01-10', 150.00, 'John Smith', 'Scheduled maintenance completed', 1),
(2, 'repair', 'Combine header adjustment and belt replacement', '2024-01-12', 320.00, 'Mike Johnson', 'Fixed harvesting efficiency issues', 1),
(3, 'calibration', 'Irrigation pump pressure calibration', '2024-01-08', 75.00, 'Sarah Wilson', 'Ensured optimal water distribution', 1);

-- Create sample alerts
INSERT INTO alerts (farm_id, alert_type, severity, title, message, is_read, is_resolved) VALUES
(1, 'sensor', 'medium', 'Low Soil Moisture Alert', 'Soil moisture in North Field Zone A is below 30%. Consider irrigation.', FALSE, FALSE),
(1, 'weather', 'high', 'Frost Warning', 'Temperature expected to drop below 0°C tonight. Protect sensitive crops.', FALSE, FALSE),
(1, 'maintenance', 'low', 'Equipment Service Due', 'Main tractor service is due in 5 days.', FALSE, FALSE),
(1, 'harvest', 'medium', 'Harvest Ready', 'Cherry tomatoes in greenhouse are ready for harvest.', FALSE, FALSE);

COMMIT;
