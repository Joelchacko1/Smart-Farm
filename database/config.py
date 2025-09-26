"""
Database configuration for Smart Farm system
Supports multiple database backends: SQLite, PostgreSQL, MySQL
"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Database configuration
DATABASE_CONFIG = {
    'sqlite': {
        'default': 'sqlite:///smart_farm.db',
        'test': 'sqlite:///:memory:',
        'production': 'sqlite:///production_farm.db'
    },
    'postgresql': {
        'default': 'postgresql://username:password@localhost:5432/smart_farm',
        'test': 'postgresql://username:password@localhost:5432/smart_farm_test',
        'production': 'postgresql://username:password@localhost:5432/smart_farm_prod'
    },
    'mysql': {
        'default': 'mysql+pymysql://username:password@localhost:3306/smart_farm',
        'test': 'mysql+pymysql://username:password@localhost:3306/smart_farm_test',
        'production': 'mysql+pymysql://username:password@localhost:3306/smart_farm_prod'
    }
}

class DatabaseConfig:
    def __init__(self, db_type='sqlite', environment='default'):
        self.db_type = db_type
        self.environment = environment
        self.database_url = self._get_database_url()
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()
        self.metadata = MetaData()
    
    def _get_database_url(self):
        """Get database URL based on environment variables or defaults"""
        # Check for environment variables first
        if os.getenv('DATABASE_URL'):
            return os.getenv('DATABASE_URL')
        
        # Check for specific database type environment variables
        if self.db_type == 'postgresql':
            if os.getenv('POSTGRES_URL'):
                return os.getenv('POSTGRES_URL')
        elif self.db_type == 'mysql':
            if os.getenv('MYSQL_URL'):
                return os.getenv('MYSQL_URL')
        elif self.db_type == 'sqlite':
            if os.getenv('SQLITE_URL'):
                return os.getenv('SQLITE_URL')
        
        # Use default configuration
        return DATABASE_CONFIG[self.db_type][self.environment]
    
    def _create_engine(self):
        """Create database engine with appropriate settings"""
        if self.db_type == 'sqlite':
            return create_engine(
                self.database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=False  # Set to True for SQL query logging
            )
        else:
            return create_engine(
                self.database_url,
                echo=False,  # Set to True for SQL query logging
                pool_pre_ping=True,
                pool_recycle=300
            )
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def create_tables(self):
        """Create all tables"""
        self.Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all tables"""
        self.Base.metadata.drop_all(bind=self.engine)

# Global database configuration instance
db_config = DatabaseConfig()

# Dependency for FastAPI or similar frameworks
def get_db():
    """Database dependency for dependency injection"""
    db = db_config.get_session()
    try:
        yield db
    finally:
        db.close()

# Database connection test
def test_connection():
    """Test database connection"""
    try:
        with db_config.engine.connect() as connection:
            result = connection.execute("SELECT 1")
            return True, "Database connection successful"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

# Environment-specific configurations
def get_production_config():
    """Get production database configuration"""
    return DatabaseConfig(db_type='postgresql', environment='production')

def get_development_config():
    """Get development database configuration"""
    return DatabaseConfig(db_type='sqlite', environment='default')

def get_test_config():
    """Get test database configuration"""
    return DatabaseConfig(db_type='sqlite', environment='test')

# Database initialization functions
def initialize_database():
    """Initialize database with schema and sample data"""
    try:
        # Create tables
        db_config.create_tables()
        
        # Load initial data if using SQLite
        if db_config.db_type == 'sqlite':
            with open('database/init.sql', 'r') as f:
                init_sql = f.read()
            
            with db_config.engine.connect() as connection:
                # Split SQL commands and execute them
                commands = init_sql.split(';')
                for command in commands:
                    command = command.strip()
                    if command:
                        connection.execute(command)
                connection.commit()
        
        return True, "Database initialized successfully"
    except Exception as e:
        return False, f"Database initialization failed: {str(e)}"

if __name__ == "__main__":
    # Test database connection and initialization
    success, message = test_connection()
    print(f"Connection test: {message}")
    
    if success:
        success, message = initialize_database()
        print(f"Initialization: {message}")
