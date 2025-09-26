#!/usr/bin/env python3
"""
Smart Farm Database Setup Script
This script helps you set up and manage the Smart Farm database
"""

import os
import sys
import sqlite3
import argparse
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import DatabaseConfig, initialize_database, test_connection

def create_database_directory():
    """Create database directory if it doesn't exist"""
    db_dir = Path("database")
    db_dir.mkdir(exist_ok=True)
    return db_dir

def setup_sqlite_database():
    """Set up SQLite database with schema and sample data"""
    print("Setting up SQLite database...")
    
    # Create database directory
    create_database_directory()
    
    # Initialize database configuration
    db_config = DatabaseConfig(db_type='sqlite', environment='default')
    
    # Test connection
    success, message = test_connection()
    print(f"Connection test: {message}")
    
    if not success:
        print("Failed to connect to database. Exiting.")
        return False
    
    # Initialize database with schema and data
    success, message = initialize_database()
    print(f"Database initialization: {message}")
    
    if success:
        print("✅ SQLite database setup completed successfully!")
        print(f"Database file: {db_config.database_url}")
        return True
    else:
        print("❌ Database setup failed!")
        return False

def setup_postgresql_database():
    """Set up PostgreSQL database"""
    print("Setting up PostgreSQL database...")
    print("Please ensure PostgreSQL is running and you have the necessary credentials.")
    
    # Check for required environment variables
    required_vars = ['POSTGRES_URL', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables and try again.")
        return False
    
    db_config = DatabaseConfig(db_type='postgresql', environment='default')
    
    # Test connection
    success, message = test_connection()
    print(f"Connection test: {message}")
    
    if success:
        print("✅ PostgreSQL database setup completed successfully!")
        return True
    else:
        print("❌ PostgreSQL setup failed!")
        return False

def setup_mysql_database():
    """Set up MySQL database"""
    print("Setting up MySQL database...")
    print("Please ensure MySQL is running and you have the necessary credentials.")
    
    # Check for required environment variables
    required_vars = ['MYSQL_URL', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DB']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables and try again.")
        return False
    
    db_config = DatabaseConfig(db_type='mysql', environment='default')
    
    # Test connection
    success, message = test_connection()
    print(f"Connection test: {message}")
    
    if success:
        print("✅ MySQL database setup completed successfully!")
        return True
    else:
        print("❌ MySQL setup failed!")
        return False

def reset_database():
    """Reset database (drop and recreate)"""
    print("Resetting database...")
    
    db_config = DatabaseConfig()
    
    try:
        # Drop all tables
        db_config.drop_tables()
        print("✅ All tables dropped successfully!")
        
        # Recreate tables and data
        success, message = initialize_database()
        if success:
            print("✅ Database reset completed successfully!")
        else:
            print(f"❌ Database reset failed: {message}")
        
        return success
    except Exception as e:
        print(f"❌ Database reset failed: {str(e)}")
        return False

def show_database_info():
    """Show database information and statistics"""
    print("Smart Farm Database Information")
    print("=" * 40)
    
    db_config = DatabaseConfig()
    
    # Test connection
    success, message = test_connection()
    print(f"Connection Status: {'✅ Connected' if success else '❌ Failed'}")
    print(f"Database URL: {db_config.database_url}")
    print(f"Database Type: {db_config.db_type}")
    
    if success:
        try:
            with db_config.engine.connect() as connection:
                # Get table information
                if db_config.db_type == 'sqlite':
                    result = connection.execute("""
                        SELECT name FROM sqlite_master 
                        WHERE type='table' AND name NOT LIKE 'sqlite_%'
                        ORDER BY name
                    """)
                    tables = [row[0] for row in result.fetchall()]
                else:
                    # For PostgreSQL/MySQL, you'd need different queries
                    tables = ["Tables not queried for non-SQLite databases"]
                
                print(f"Tables: {', '.join(tables)}")
                
                # Get record counts for main tables
                main_tables = ['users', 'farms', 'zones', 'crops', 'sensors', 'sensor_data']
                for table in main_tables:
                    if table in tables:
                        try:
                            result = connection.execute(f"SELECT COUNT(*) FROM {table}")
                            count = result.fetchone()[0]
                            print(f"{table}: {count} records")
                        except:
                            print(f"{table}: Unable to count records")
        
        except Exception as e:
            print(f"Error getting database info: {str(e)}")

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Smart Farm Database Setup')
    parser.add_argument('--db-type', choices=['sqlite', 'postgresql', 'mysql'], 
                       default='sqlite', help='Database type to use')
    parser.add_argument('--reset', action='store_true', 
                       help='Reset database (drop and recreate)')
    parser.add_argument('--info', action='store_true', 
                       help='Show database information')
    parser.add_argument('--test', action='store_true', 
                       help='Test database connection')
    
    args = parser.parse_args()
    
    if args.test:
        db_config = DatabaseConfig(db_type=args.db_type)
        success, message = test_connection()
        print(f"Connection test: {message}")
        return
    
    if args.info:
        show_database_info()
        return
    
    if args.reset:
        reset_database()
        return
    
    # Setup database based on type
    if args.db_type == 'sqlite':
        setup_sqlite_database()
    elif args.db_type == 'postgresql':
        setup_postgresql_database()
    elif args.db_type == 'mysql':
        setup_mysql_database()
    else:
        print(f"Unsupported database type: {args.db_type}")
        sys.exit(1)

if __name__ == "__main__":
    main()
