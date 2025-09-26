# Smart Farm Database

A comprehensive database system designed for smart farming applications, supporting IoT sensors, crop management, irrigation systems, weather monitoring, and farm operations.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- SQLite (included with Python) or PostgreSQL/MySQL for production

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up the database:**
   ```bash
   python setup.py --db-type sqlite
   ```

3. **Test the connection:**
   ```bash
   python setup.py --test
   ```

## 📊 Database Schema Overview

The Smart Farm database consists of 15 main tables organized into logical groups:

### Core Entities
- **Users** - System users (farmers, technicians, admins)
- **Farms** - Farm locations and properties
- **Zones** - Different areas within farms (fields, greenhouses, orchards)

### Crop Management
- **Crop Types** - Master data for different crop varieties
- **Crops** - Actual plantings and their status
- **Harvests** - Harvest records and yields

### IoT & Sensors
- **Sensor Types** - Types of sensors (temperature, humidity, etc.)
- **Sensors** - Physical sensor devices
- **Sensor Data** - Time-series data from sensors

### Environmental Monitoring
- **Weather Data** - Weather conditions and forecasts
- **Irrigation Systems** - Water management systems
- **Irrigation Events** - Watering schedules and usage

### Farm Operations
- **Applications** - Fertilizer, pesticide applications
- **Equipment** - Farm machinery and tools
- **Maintenance Records** - Equipment maintenance history
- **Alerts** - System notifications and warnings

## 🗄️ Database Tables

### Users & Authentication
```sql
users (id, username, email, password_hash, first_name, last_name, role, created_at, updated_at, is_active)
```

### Farm Management
```sql
farms (id, name, location, latitude, longitude, area_hectares, owner_id, created_at, updated_at)
zones (id, farm_id, name, zone_type, area_square_meters, description, created_at)
```

### Crop Management
```sql
crop_types (id, name, scientific_name, category, planting_season, harvest_days, water_requirements, temperature_min, temperature_max, ph_min, ph_max, created_at)
crops (id, zone_id, crop_type_id, variety, planting_date, expected_harvest_date, actual_harvest_date, quantity_planted, status, notes, created_at, updated_at)
harvests (id, crop_id, harvest_date, quantity_harvested, unit, quality_grade, price_per_unit, total_value, storage_location, notes, created_at)
```

### IoT & Sensors
```sql
sensor_types (id, name, unit, data_type, min_value, max_value, description)
sensors (id, zone_id, sensor_type_id, name, serial_number, location_description, installation_date, last_calibration_date, next_calibration_date, status, battery_level, signal_strength, created_at, updated_at)
sensor_data (id, sensor_id, value, raw_value, timestamp, quality_score)
```

### Environmental Data
```sql
weather_data (id, farm_id, temperature, humidity, pressure, wind_speed, wind_direction, rainfall, uv_index, visibility, cloud_cover, timestamp, source)
```

### Irrigation Systems
```sql
irrigation_systems (id, zone_id, name, system_type, capacity_liters_per_hour, status, installation_date, last_maintenance_date, next_maintenance_date, created_at)
irrigation_events (id, irrigation_system_id, start_time, end_time, duration_minutes, water_used_liters, trigger_type, notes, created_at)
```

### Farm Operations
```sql
applications (id, zone_id, application_type, product_name, active_ingredient, quantity_applied, unit, application_method, application_date, weather_conditions, notes, created_by, created_at)
equipment (id, farm_id, name, equipment_type, model, serial_number, purchase_date, warranty_expiry, status, last_service_date, next_service_date, notes, created_at)
maintenance_records (id, equipment_id, maintenance_type, description, maintenance_date, cost, technician, notes, created_by, created_at)
alerts (id, farm_id, alert_type, severity, title, message, is_read, is_resolved, resolved_at, resolved_by, created_at)
```

## 🔧 Configuration

### Database Types Supported

1. **SQLite** (Default - Development)
   - File-based database
   - No additional setup required
   - Perfect for development and testing

2. **PostgreSQL** (Production)
   - High-performance relational database
   - Better for production environments
   - Requires PostgreSQL server

3. **MySQL** (Production Alternative)
   - Popular open-source database
   - Good for web applications
   - Requires MySQL server

### Environment Variables

For PostgreSQL:
```bash
export POSTGRES_URL="postgresql://username:password@localhost:5432/smart_farm"
export POSTGRES_USER="your_username"
export POSTGRES_PASSWORD="your_password"
export POSTGRES_DB="smart_farm"
```

For MySQL:
```bash
export MYSQL_URL="mysql+pymysql://username:password@localhost:3306/smart_farm"
export MYSQL_USER="your_username"
export MYSQL_PASSWORD="your_password"
export MYSQL_DB="smart_farm"
```

## 🚀 Usage Examples

### Basic Setup
```python
from database.config import DatabaseConfig, get_db

# Initialize database
db_config = DatabaseConfig(db_type='sqlite')

# Get database session
with db_config.get_session() as session:
    # Your database operations here
    pass
```

### Using SQLAlchemy Models
```python
from database.models import User, Farm, Crop, SensorData
from database.config import get_db

# Create a new user
user = User(
    username="farmer1",
    email="farmer@example.com",
    password_hash="hashed_password",
    first_name="John",
    last_name="Doe",
    role=UserRole.farmer
)

# Add to database
session.add(user)
session.commit()
```

### Querying Data
```python
# Get all farms for a user
farms = session.query(Farm).filter(Farm.owner_id == user_id).all()

# Get recent sensor data
recent_data = session.query(SensorData)\
    .filter(SensorData.timestamp >= datetime.now() - timedelta(hours=24))\
    .all()

# Get crops ready for harvest
ready_crops = session.query(Crop)\
    .filter(Crop.status == CropStatus.ready_harvest)\
    .all()
```

## 📈 Performance Optimization

### Indexes
The database includes optimized indexes for common queries:
- Sensor data by sensor and timestamp
- Weather data by farm and timestamp
- Crops by zone and status
- Alerts by farm and read status

### Query Optimization Tips
1. Use specific date ranges for time-series data
2. Filter by farm_id or zone_id when possible
3. Use LIMIT for large result sets
4. Consider data archiving for old sensor data

## 🔒 Security Considerations

1. **Password Hashing**: Use bcrypt or similar for password storage
2. **Input Validation**: Validate all user inputs
3. **SQL Injection**: Use parameterized queries
4. **Access Control**: Implement proper user roles and permissions
5. **Data Encryption**: Consider encrypting sensitive data

## 📊 Sample Data

The database comes with sample data including:
- Default admin user
- Sample farm with multiple zones
- Various sensor types and devices
- Sample crops and harvest records
- Weather data and irrigation events
- Equipment and maintenance records
- System alerts and notifications

## 🛠️ Maintenance

### Database Reset
```bash
python setup.py --reset
```

### Database Information
```bash
python setup.py --info
```

### Connection Test
```bash
python setup.py --test
```

## 📚 API Integration

The database is designed to work with REST APIs. Example endpoints:

- `GET /api/farms` - List all farms
- `GET /api/crops` - List crops with filters
- `POST /api/sensor-data` - Add sensor readings
- `GET /api/weather` - Get weather data
- `POST /api/irrigation` - Trigger irrigation
- `GET /api/alerts` - Get system alerts

## 🔄 Data Migration

For production deployments:

1. **Backup existing data**
2. **Run schema migrations**
3. **Update application code**
4. **Test thoroughly**
5. **Deploy to production**

## 📞 Support

For questions or issues:
1. Check the documentation
2. Review the sample code
3. Test with the provided setup script
4. Check database logs for errors

## 🚀 Next Steps

1. **Set up the database** using the setup script
2. **Explore the sample data** to understand the structure
3. **Integrate with your application** using the provided models
4. **Customize the schema** for your specific needs
5. **Deploy to production** with proper security measures

---

**Happy Farming! 🌱**
