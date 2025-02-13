import sqlite3

def check_db():
    try:
        conn = sqlite3.connect('words.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("Checking groups table:")
        cursor.execute('SELECT * FROM groups')
        groups = cursor.fetchall()
        if not groups:
            print("WARNING: No groups found in database!")
        else:
            for group in groups:
                print(f"Group ID: {group['id']}, Name: {group['name']}")
        
        print("\nChecking study_activities table:")
        cursor.execute('SELECT * FROM study_activities')
        activities = cursor.fetchall()
        if not activities:
            print("WARNING: No study activities found in database!")
        else:
            for activity in activities:
                print(f"Activity ID: {activity['id']}, Name: {activity['name']}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == '__main__':
    check_db() 