import sqlite3
import os
import time
from app import create_app

def init_db():
    # Try to delete existing database if it exists
    if os.path.exists('words.db'):
        try:
            os.remove('words.db')
            print("Removed existing database")
        except PermissionError:
            print("Please stop the Flask server first (Ctrl+C)")
            print("Then try running this script again")
            return
        except Exception as e:
            print(f"Error removing database: {e}")
            return

    # Create new database and initialize it
    app = create_app()
    
    with app.app_context():
        try:
            # Get database connection
            conn = sqlite3.connect('words.db')
            cursor = conn.cursor()
            
            # Read and execute schema.sql
            with open('schema.sql', 'r') as f:
                cursor.executescript(f.read())
                
            # Commit changes
            conn.commit()
            print("Database initialized with schema")
            
            # Verify the data was inserted
            cursor.execute('SELECT * FROM groups')
            groups = cursor.fetchall()
            print("\nGroups in database:", groups)
            
            cursor.execute('SELECT * FROM study_activities')
            activities = cursor.fetchall()
            print("\nStudy activities in database:", activities)
            
        finally:
            conn.close()
            if hasattr(app, 'db'):
                app.db.close()

if __name__ == '__main__':
    init_db()
    print("\nDatabase initialization complete!") 