"""
SQLAlchemy models for Smart Farm database
These models represent the database tables and relationships
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

# Enums for better type safety
class UserRole(enum.Enum):
    admin = "admin"
    farmer = "farmer"
    technician = "technician"
    viewer = "viewer"

class ZoneType(enum.Enum):
    field = "field"
    greenhouse = "greenhouse"
    orchard = "orchard"
    livestock = "livestock"
    storage = "storage"

class CropCategory(enum.Enum):
    vegetable = "vegetable"
    fruit = "fruit"
    grain = "grain"
    herb = "herb"
    flower = "flower"
    other = "other"

class CropStatus(enum.Enum):
    planted = "planted"
    growing = "growing"
    ready_harvest = "ready_harvest"
    harvested = "harvested"
    failed = "failed"

class SensorStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"
    error = "error"

class DataType(enum.Enum):
    numeric = "numeric"
    boolean = "boolean"
    text = "text"

class IrrigationType(enum.Enum):
    drip = "drip"
    sprinkler = "sprinkler"
    flood = "flood"
    manual = "manual"

class ApplicationType(enum.Enum):
    fertilizer = "fertilizer"
    pesticide = "pesticide"
    herbicide = "herbicide"
    fungicide = "fungicide"
    other = "other"

class ApplicationMethod(enum.Enum):
    spray = "spray"
    soil = "soil"
    foliar = "foliar"
    injection = "injection"
    other = "other"

class QualityGrade(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

class EquipmentType(enum.Enum):
    tractor = "tractor"
    harvester = "harvester"
    irrigation = "irrigation"
    sensor = "sensor"
    other = "other"

class MaintenanceType(enum.Enum):
    routine = "routine"
    repair = "repair"
    calibration = "calibration"
    cleaning = "cleaning"
    other = "other"

class AlertType(enum.Enum):
    sensor = "sensor"
    weather = "weather"
    irrigation = "irrigation"
    maintenance = "maintenance"
    harvest = "harvest"
    other = "other"

class AlertSeverity(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class TriggerType(enum.Enum):
    manual = "manual"
    scheduled = "scheduled"
    sensor = "sensor"
    weather = "weather"

# User and Authentication Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.farmer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    farms = relationship("Farm", back_populates="owner")
    applications = relationship("Application", back_populates="creator")
    maintenance_records = relationship("MaintenanceRecord", back_populates="creator")
    resolved_alerts = relationship("Alert", back_populates="resolver")

class Farm(Base):
    __tablename__ = "farms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    area_hectares = Column(DECIMAL(10, 2))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="farms")
    zones = relationship("Zone", back_populates="farm", cascade="all, delete-orphan")
    weather_data = relationship("WeatherData", back_populates="farm", cascade="all, delete-orphan")
    equipment = relationship("Equipment", back_populates="farm", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="farm", cascade="all, delete-orphan")

class Zone(Base):
    __tablename__ = "zones"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    name = Column(String(100), nullable=False)
    zone_type = Column(Enum(ZoneType), nullable=False)
    area_square_meters = Column(DECIMAL(10, 2))
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    farm = relationship("Farm", back_populates="zones")
    crops = relationship("Crop", back_populates="zone", cascade="all, delete-orphan")
    sensors = relationship("Sensor", back_populates="zone", cascade="all, delete-orphan")
    irrigation_systems = relationship("IrrigationSystem", back_populates="zone", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="zone", cascade="all, delete-orphan")

# Crop Models
class CropType(Base):
    __tablename__ = "crop_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    scientific_name = Column(String(150))
    category = Column(Enum(CropCategory), nullable=False)
    planting_season = Column(String(50))
    harvest_days = Column(Integer)
    water_requirements = Column(DECIMAL(5, 2))  # liters per day
    temperature_min = Column(DECIMAL(5, 2))
    temperature_max = Column(DECIMAL(5, 2))
    ph_min = Column(DECIMAL(3, 1))
    ph_max = Column(DECIMAL(3, 1))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    crops = relationship("Crop", back_populates="crop_type")

class Crop(Base):
    __tablename__ = "crops"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    crop_type_id = Column(Integer, ForeignKey("crop_types.id"), nullable=False)
    variety = Column(String(100))
    planting_date = Column(Date, nullable=False)
    expected_harvest_date = Column(Date)
    actual_harvest_date = Column(Date)
    quantity_planted = Column(Integer)
    status = Column(Enum(CropStatus), default=CropStatus.planted)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    zone = relationship("Zone", back_populates="crops")
    crop_type = relationship("CropType", back_populates="crops")
    harvests = relationship("Harvest", back_populates="crop", cascade="all, delete-orphan")

# Sensor Models
class SensorType(Base):
    __tablename__ = "sensor_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)
    data_type = Column(Enum(DataType), default=DataType.numeric)
    min_value = Column(DECIMAL(10, 3))
    max_value = Column(DECIMAL(10, 3))
    description = Column(Text)
    
    # Relationships
    sensors = relationship("Sensor", back_populates="sensor_type")

class Sensor(Base):
    __tablename__ = "sensors"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    sensor_type_id = Column(Integer, ForeignKey("sensor_types.id"), nullable=False)
    name = Column(String(100), nullable=False)
    serial_number = Column(String(100), unique=True)
    location_description = Column(String(200))
    installation_date = Column(Date)
    last_calibration_date = Column(Date)
    next_calibration_date = Column(Date)
    status = Column(Enum(SensorStatus), default=SensorStatus.active)
    battery_level = Column(Integer)  # percentage
    signal_strength = Column(Integer)  # percentage
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    zone = relationship("Zone", back_populates="sensors")
    sensor_type = relationship("SensorType", back_populates="sensors")
    sensor_data = relationship("SensorData", back_populates="sensor", cascade="all, delete-orphan")

class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    value = Column(DECIMAL(10, 3), nullable=False)
    raw_value = Column(Text)
    timestamp = Column(DateTime, default=func.now(), index=True)
    quality_score = Column(DECIMAL(3, 2))  # 0.00 to 1.00
    
    # Relationships
    sensor = relationship("Sensor", back_populates="sensor_data")

# Weather Model
class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    temperature = Column(DECIMAL(5, 2))
    humidity = Column(DECIMAL(5, 2))
    pressure = Column(DECIMAL(7, 2))
    wind_speed = Column(DECIMAL(5, 2))
    wind_direction = Column(Integer)  # degrees
    rainfall = Column(DECIMAL(5, 2))
    uv_index = Column(DECIMAL(4, 2))
    visibility = Column(DECIMAL(5, 2))
    cloud_cover = Column(DECIMAL(5, 2))
    timestamp = Column(DateTime, default=func.now(), index=True)
    source = Column(String(50))  # 'station', 'api', 'manual'
    
    # Relationships
    farm = relationship("Farm", back_populates="weather_data")

# Irrigation Models
class IrrigationSystem(Base):
    __tablename__ = "irrigation_systems"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    name = Column(String(100), nullable=False)
    system_type = Column(Enum(IrrigationType), nullable=False)
    capacity_liters_per_hour = Column(DECIMAL(8, 2))
    status = Column(Enum(SensorStatus), default=SensorStatus.active)
    installation_date = Column(Date)
    last_maintenance_date = Column(Date)
    next_maintenance_date = Column(Date)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    zone = relationship("Zone", back_populates="irrigation_systems")
    irrigation_events = relationship("IrrigationEvent", back_populates="irrigation_system", cascade="all, delete-orphan")

class IrrigationEvent(Base):
    __tablename__ = "irrigation_events"
    
    id = Column(Integer, primary_key=True, index=True)
    irrigation_system_id = Column(Integer, ForeignKey("irrigation_systems.id"), nullable=False)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer)
    water_used_liters = Column(DECIMAL(8, 2))
    trigger_type = Column(Enum(TriggerType), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    irrigation_system = relationship("IrrigationSystem", back_populates="irrigation_events")

# Application Models
class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    application_type = Column(Enum(ApplicationType), nullable=False)
    product_name = Column(String(100), nullable=False)
    active_ingredient = Column(String(100))
    quantity_applied = Column(DECIMAL(8, 2))
    unit = Column(String(20), nullable=False)
    application_method = Column(Enum(ApplicationMethod), nullable=False)
    application_date = Column(Date, nullable=False)
    weather_conditions = Column(String(200))
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    zone = relationship("Zone", back_populates="applications")
    creator = relationship("User", back_populates="applications")

# Harvest Model
class Harvest(Base):
    __tablename__ = "harvests"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    harvest_date = Column(Date, nullable=False)
    quantity_harvested = Column(DECIMAL(10, 2), nullable=False)
    unit = Column(String(20), nullable=False)
    quality_grade = Column(Enum(QualityGrade), nullable=False)
    price_per_unit = Column(DECIMAL(8, 2))
    total_value = Column(DECIMAL(10, 2))
    storage_location = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    crop = relationship("Crop", back_populates="harvests")

# Equipment Models
class Equipment(Base):
    __tablename__ = "equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    name = Column(String(100), nullable=False)
    equipment_type = Column(Enum(EquipmentType), nullable=False)
    model = Column(String(100))
    serial_number = Column(String(100))
    purchase_date = Column(Date)
    warranty_expiry = Column(Date)
    status = Column(Enum(SensorStatus), default=SensorStatus.active)
    last_service_date = Column(Date)
    next_service_date = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    farm = relationship("Farm", back_populates="equipment")
    maintenance_records = relationship("MaintenanceRecord", back_populates="equipment", cascade="all, delete-orphan")

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    maintenance_type = Column(Enum(MaintenanceType), nullable=False)
    description = Column(Text, nullable=False)
    maintenance_date = Column(Date, nullable=False)
    cost = Column(DECIMAL(10, 2))
    technician = Column(String(100))
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_records")
    creator = relationship("User", back_populates="maintenance_records")

# Alert Model
class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    alert_type = Column(Enum(AlertType), nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime)
    resolved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now(), index=True)
    
    # Relationships
    farm = relationship("Farm", back_populates="alerts")
    resolver = relationship("User", back_populates="resolved_alerts")
