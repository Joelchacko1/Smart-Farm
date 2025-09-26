-- Smart Farm Database Schema
-- This database is designed for a comprehensive smart farming system

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Users and Authentication
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role ENUM('admin', 'farmer', 'technician', 'viewer') DEFAULT 'farmer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Farm Locations
CREATE TABLE farms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    area_hectares DECIMAL(10, 2),
    owner_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Farm Zones (different areas within a farm)
CREATE TABLE zones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    zone_type ENUM('field', 'greenhouse', 'orchard', 'livestock', 'storage') NOT NULL,
    area_square_meters DECIMAL(10, 2),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE CASCADE
);

-- Crop Types
CREATE TABLE crop_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150),
    category ENUM('vegetable', 'fruit', 'grain', 'herb', 'flower', 'other') NOT NULL,
    planting_season VARCHAR(50),
    harvest_days INTEGER,
    water_requirements DECIMAL(5, 2), -- liters per day
    temperature_min DECIMAL(5, 2),
    temperature_max DECIMAL(5, 2),
    ph_min DECIMAL(3, 1),
    ph_max DECIMAL(3, 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crops (actual plantings)
CREATE TABLE crops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL,
    crop_type_id INTEGER NOT NULL,
    variety VARCHAR(100),
    planting_date DATE NOT NULL,
    expected_harvest_date DATE,
    actual_harvest_date DATE,
    quantity_planted INTEGER,
    status ENUM('planted', 'growing', 'ready_harvest', 'harvested', 'failed') DEFAULT 'planted',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE,
    FOREIGN KEY (crop_type_id) REFERENCES crop_types(id)
);

-- Sensor Types
CREATE TABLE sensor_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    data_type ENUM('numeric', 'boolean', 'text') DEFAULT 'numeric',
    min_value DECIMAL(10, 3),
    max_value DECIMAL(10, 3),
    description TEXT
);

-- Sensors
CREATE TABLE sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL,
    sensor_type_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    serial_number VARCHAR(100) UNIQUE,
    location_description VARCHAR(200),
    installation_date DATE,
    last_calibration_date DATE,
    next_calibration_date DATE,
    status ENUM('active', 'inactive', 'maintenance', 'error') DEFAULT 'active',
    battery_level INTEGER, -- percentage
    signal_strength INTEGER, -- percentage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE,
    FOREIGN KEY (sensor_type_id) REFERENCES sensor_types(id)
);

-- Sensor Data
CREATE TABLE sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    value DECIMAL(10, 3) NOT NULL,
    raw_value TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quality_score DECIMAL(3, 2), -- 0.00 to 1.00
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
);

-- Weather Data
CREATE TABLE weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_id INTEGER NOT NULL,
    temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    pressure DECIMAL(7, 2),
    wind_speed DECIMAL(5, 2),
    wind_direction INTEGER, -- degrees
    rainfall DECIMAL(5, 2),
    uv_index DECIMAL(4, 2),
    visibility DECIMAL(5, 2),
    cloud_cover DECIMAL(5, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50), -- 'station', 'api', 'manual'
    FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE CASCADE
);

-- Irrigation Systems
CREATE TABLE irrigation_systems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    system_type ENUM('drip', 'sprinkler', 'flood', 'manual') NOT NULL,
    capacity_liters_per_hour DECIMAL(8, 2),
    status ENUM('active', 'inactive', 'maintenance') DEFAULT 'active',
    installation_date DATE,
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE
);

-- Irrigation Events
CREATE TABLE irrigation_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    irrigation_system_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration_minutes INTEGER,
    water_used_liters DECIMAL(8, 2),
    trigger_type ENUM('manual', 'scheduled', 'sensor', 'weather') NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (irrigation_system_id) REFERENCES irrigation_systems(id) ON DELETE CASCADE
);

-- Fertilizer/Pesticide Applications
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL,
    application_type ENUM('fertilizer', 'pesticide', 'herbicide', 'fungicide', 'other') NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    active_ingredient VARCHAR(100),
    quantity_applied DECIMAL(8, 2),
    unit VARCHAR(20) NOT NULL,
    application_method ENUM('spray', 'soil', 'foliar', 'injection', 'other') NOT NULL,
    application_date DATE NOT NULL,
    weather_conditions VARCHAR(200),
    notes TEXT,
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Harvest Records
CREATE TABLE harvests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_id INTEGER NOT NULL,
    harvest_date DATE NOT NULL,
    quantity_harvested DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    quality_grade ENUM('A', 'B', 'C', 'D') NOT NULL,
    price_per_unit DECIMAL(8, 2),
    total_value DECIMAL(10, 2),
    storage_location VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE
);

-- Equipment
CREATE TABLE equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    equipment_type ENUM('tractor', 'harvester', 'irrigation', 'sensor', 'other') NOT NULL,
    model VARCHAR(100),
    serial_number VARCHAR(100),
    purchase_date DATE,
    warranty_expiry DATE,
    status ENUM('active', 'maintenance', 'retired') DEFAULT 'active',
    last_service_date DATE,
    next_service_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE CASCADE
);

-- Maintenance Records
CREATE TABLE maintenance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER NOT NULL,
    maintenance_type ENUM('routine', 'repair', 'calibration', 'cleaning', 'other') NOT NULL,
    description TEXT NOT NULL,
    maintenance_date DATE NOT NULL,
    cost DECIMAL(10, 2),
    technician VARCHAR(100),
    notes TEXT,
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Alerts and Notifications
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_id INTEGER NOT NULL,
    alert_type ENUM('sensor', 'weather', 'irrigation', 'maintenance', 'harvest', 'other') NOT NULL,
    severity ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    resolved_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE CASCADE,
    FOREIGN KEY (resolved_by) REFERENCES users(id)
);

-- Create indexes for better performance
CREATE INDEX idx_sensor_data_sensor_timestamp ON sensor_data(sensor_id, timestamp);
CREATE INDEX idx_sensor_data_timestamp ON sensor_data(timestamp);
CREATE INDEX idx_weather_data_farm_timestamp ON weather_data(farm_id, timestamp);
CREATE INDEX idx_crops_zone_status ON crops(zone_id, status);
CREATE INDEX idx_alerts_farm_unread ON alerts(farm_id, is_read);
CREATE INDEX idx_irrigation_events_system_time ON irrigation_events(irrigation_system_id, start_time);

-- Create triggers for updated_at timestamps
CREATE TRIGGER update_users_timestamp 
    AFTER UPDATE ON users
    FOR EACH ROW
    BEGIN
        UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER update_farms_timestamp 
    AFTER UPDATE ON farms
    FOR EACH ROW
    BEGIN
        UPDATE farms SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER update_crops_timestamp 
    AFTER UPDATE ON crops
    FOR EACH ROW
    BEGIN
        UPDATE crops SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER update_sensors_timestamp 
    AFTER UPDATE ON sensors
    FOR EACH ROW
    BEGIN
        UPDATE sensors SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
