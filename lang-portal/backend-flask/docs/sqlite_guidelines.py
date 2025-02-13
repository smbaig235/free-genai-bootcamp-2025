"""
SQLite3 Best Practices and Guidelines
-----------------------------------

This document outlines critical rules and best practices for working with SQLite3
in our application. Following these guidelines is mandatory for all database operations.

1. ALWAYS USE PARAMETERIZED QUERIES
---------------------------------
Parameterized queries prevent SQL injection attacks and handle data typing correctly.

Good:
    cursor.execute("SELECT * FROM words WHERE id = ?", (word_id,))
    cursor.execute("INSERT INTO words (name, value) VALUES (?, ?)", (name, value))

Bad (NEVER DO THIS):
    cursor.execute(f"SELECT * FROM words WHERE id = {word_id}")  # VULNERABLE!
    cursor.execute("SELECT * FROM words WHERE name = '" + name + "'")  # VULNERABLE!


2. PROPER CONNECTION AND CURSOR MANAGEMENT
----------------------------------------
Always properly manage database resources to prevent leaks and ensure cleanup.

Good Pattern:
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM words")
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        cursor.close()  # Always close cursor
        db.close()      # Always close connection when done


3. USE TRANSACTIONS FOR MULTIPLE OPERATIONS
-----------------------------------------
When performing multiple related database operations, use transactions to ensure
data consistency.

Good Pattern:
    try:
        with db:  # Creates a transaction
            cursor = db.cursor()
            # All these operations will be rolled back if any fails
            cursor.execute("UPDATE words SET count = count + 1 WHERE id = ?", (word_id,))
            cursor.execute("INSERT INTO history (word_id) VALUES (?)", (word_id,))
    except sqlite3.Error as e:
        print(f"Transaction failed: {e}")
        raise


IMPORTANT NOTES
--------------
1. SQLite Limitations:
   - Not suitable for high concurrency (writes lock the entire database)
   - Not recommended for large-scale applications
   - Better suited for development and smaller applications

2. Performance Considerations:
   - Use indexes for frequently queried columns
   - Avoid large transactions that could lock the database for too long
   - Consider using batch operations for bulk updates

3. Security:
   - Always validate and sanitize input data
   - Use appropriate file permissions for the database file
   - Regularly backup the database file

4. Error Handling:
   - Always catch and handle sqlite3.Error exceptions
   - Log database errors appropriately
   - Consider implementing retry logic for transient errors
"""

# Example Implementation Pattern
def example_safe_query(db, query, params=None):
    """
    Example of a safe database query implementation.
    
    Args:
        db: Database connection object
        query: SQL query string with parameter placeholders
        params: Tuple of parameters to bind to the query
    """
    if params is None:
        params = ()
    
    try:
        with db:  # Start transaction
            cursor = db.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        cursor.close()

# Usage Example
"""
# Example usage of the safe query pattern:
try:
    results = example_safe_query(
        db,
        "SELECT * FROM words WHERE category = ? AND difficulty <= ?",
        ("verbs", 3)
    )
except sqlite3.Error as e:
    # Handle error appropriately
    pass
""" 