#!/usr/bin/env python3
"""
Smart PostgreSQL database setup for chatbot project.
Automatically detects if database exists and either creates it or accesses it.
"""

import os
import json
import sys
from pathlib import Path
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Add src to path so we can import our modules
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Database configuration
DB_USER = "chatbot_user"
DB_PASSWORD = "chatbot_user"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "digital_twin"

# Admin credentials (change if different)
ADMIN_USER = "postgres"
ADMIN_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")  # Replace YOUR_ACTUAL_PASSWORD_HERE with your pgAdmin password

def check_database_exists():
    """Check if the database and user already exist"""
    try:
        # Try to connect directly to the target database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        conn.close()
        return True, "Database and user exist and are accessible"
    
    except psycopg2.OperationalError as e:
        error_msg = str(e).lower()
        
        if "database" in error_msg and "does not exist" in error_msg:
            return False, "Database does not exist"
        elif "authentication failed" in error_msg or "role" in error_msg:
            return False, "User does not exist or password incorrect"
        else:
            return False, f"Connection failed: {e}"

def create_user_and_database():
    """Create PostgreSQL user and database"""
    print("🔧 Creating PostgreSQL user and database...")
    
    try:
        # Connect as admin user
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=ADMIN_USER,
            password=ADMIN_PASSWORD,
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute(
            "SELECT 1 FROM pg_roles WHERE rolname = %s",
            (DB_USER,)
        )
        
        if not cursor.fetchone():
            # Create user
            cursor.execute(
                sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
                    sql.Identifier(DB_USER)
                ),
                (DB_PASSWORD,)
            )
            print(f"✓ User '{DB_USER}' created")
        else:
            print(f"✓ User '{DB_USER}' already exists")
        
        # Grant privileges to user
        cursor.execute(
            sql.SQL("ALTER USER {} CREATEDB").format(
                sql.Identifier(DB_USER)
            )
        )
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_NAME,)
        )
        
        if not cursor.fetchone():
            # Create database
            cursor.execute(
                sql.SQL("CREATE DATABASE {} OWNER {}").format(
                    sql.Identifier(DB_NAME),
                    sql.Identifier(DB_USER)
                )
            )
            print(f"✓ Database '{DB_NAME}' created")
        else:
            print(f"✓ Database '{DB_NAME}' already exists")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def check_tables_exist():
    """Check if tables already exist in the database"""
    try:
        from src.app.database.db import engine
        from sqlalchemy import text
        
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'profiles'
            """))
            
            tables = result.fetchall()
            return len(tables) > 0
            
    except Exception as e:
        print(f"Warning: Could not check existing tables: {e}")
        return False

def create_tables():
    """Create all tables using SQLAlchemy"""
    print("📋 Setting up database tables...")
    
    try:
        from src.app.database.db import engine, Base
        from src.app.models.profile import Profile  # Import to register the model
        from sqlalchemy import text
        
        print("   • Importing models...")
        
        # Ensure the Profile model is registered with Base
        print(f"   • Registered tables: {list(Base.metadata.tables.keys())}")
        
        # Create all tables
        print("   • Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        # Verify tables were created
        print("   • Verifying tables...")
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result.fetchall()]
            
        if not tables:
            # Try alternative table creation method
            print("   • No tables found, trying direct SQL creation...")
            with engine.connect() as connection:
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS profiles (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(100) UNIQUE NOT NULL,
                        idade INTEGER,
                        formacao JSONB,
                        experiencia JSONB,
                        habilidades JSONB,
                        objetivos TEXT,
                        hobbies JSONB
                    );
                """))
                connection.commit()
                
            # Check again
            with engine.connect() as connection:
                result = connection.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """))
                tables = [row[0] for row in result.fetchall()]
            
        print(f"✓ Tables ready: {', '.join(tables) if tables else 'none'}")
        return len(tables) > 0
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_profiles_exist():
    """Check if profiles are already loaded in the database"""
    try:
        from src.app.database.db import SessionLocal
        from src.app.models.profile import Profile
        
        db = SessionLocal()
        profile_count = db.query(Profile).count()
        db.close()
        
        return profile_count > 0, profile_count
        
    except Exception as e:
        return False, 0

def load_profiles():
    """Load profile data from JSON files"""
    print("👥 Loading profile data...")
    
    try:
        from src.app.database.db import SessionLocal
        from src.app.models.profile import Profile
        
        db = SessionLocal()
        
        # Path to profiles directory
        profiles_dir = Path("src/profiles")
        
        if not profiles_dir.exists():
            print(f"⚠️  Profiles directory not found: {profiles_dir}")
            return True  # Not an error, just no profiles to load
        
        json_files = list(profiles_dir.glob("*.json"))
        if not json_files:
            print("⚠️  No profile JSON files found")
            return True
        
        loaded_count = 0
        skipped_count = 0
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                
                # Check if profile already exists
                existing = db.query(Profile).filter(
                    Profile.nome.ilike(profile_data["nome"])
                ).first()
                
                if existing:
                    skipped_count += 1
                    continue
                
                # Create new profile
                new_profile = Profile(**profile_data)
                db.add(new_profile)
                db.commit()
                
                loaded_count += 1
                
            except Exception as e:
                print(f"  ⚠️  Error processing {json_file.name}: {e}")
        
        db.close()
        
        if loaded_count > 0:
            print(f"✓ Loaded {loaded_count} new profiles")
        if skipped_count > 0:
            print(f"⚠️  Skipped {skipped_count} existing profiles")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading profiles: {e}")
        return False

def show_database_status():
    """Show current database status and contents"""
    print("\n📊 Database Status:")
    
    try:
        from src.app.database.db import SessionLocal, engine
        from src.app.models.profile import Profile
        
        # Show connection info
        print(f"   🔗 Connection: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        # Show tables
        from sqlalchemy import text
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"   📋 Tables: {', '.join(tables) if tables else 'none'}")
        
        # Show profile count
        db = SessionLocal()
        profile_count = db.query(Profile).count()
        print(f"   👥 Profiles: {profile_count}")
        
        if profile_count > 0:
            profiles = db.query(Profile).limit(5).all()
            print(f"   📝 Sample profiles:")
            for profile in profiles:
                print(f"      • {profile.nome}")
            if profile_count > 5:
                print(f"      ... and {profile_count - 5} more")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking status: {e}")
        return False

def main():
    """Main setup function with smart detection"""
    print("🐘 Smart PostgreSQL Setup for Chatbot")
    print("=" * 45)
    
    # Step 1: Check if database exists and is accessible
    db_exists, reason = check_database_exists()
    
    if db_exists:
        print(f"✓ Database is accessible: {reason}")
        
        # Check if tables exist
        tables_exist = check_tables_exist()
        if tables_exist:
            print("✓ Tables already exist")
        else:
            print("⚠️  Tables missing, creating them...")
            if not create_tables():
                print("❌ Failed to create tables")
                sys.exit(1)
        
        # Check if profiles exist
        profiles_exist, count = check_profiles_exist()
        if profiles_exist:
            print(f"✓ Database already contains {count} profiles")
        else:
            print("📥 No profiles found, loading from JSON files...")
            load_profiles()
    
    else:
        print(f"🔧 First time setup needed: {reason}")
        
        # First time setup
        print("\n🚀 Performing first-time database setup...")
        
        if not create_user_and_database():
            print("❌ Failed to create database")
            sys.exit(1)
        
        if not create_tables():
            print("❌ Failed to create tables")
            sys.exit(1)
        
        if not load_profiles():
            print("❌ Failed to load profiles")
            sys.exit(1)
        
        print("✅ First-time setup completed successfully!")
    
    # Final status check
    if show_database_status():
        print("\n🎉 Database is ready!")
        print("\n🚀 You can now:")
        print("   • Start your FastAPI application")
        print("   • Use all API endpoints")
        print("   • Add more profiles in src/profiles/")
    else:
        print("\n⚠️  Setup completed but status check failed")
        sys.exit(1)

if __name__ == "__main__":
    main()