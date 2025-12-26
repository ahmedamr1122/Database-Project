from database.connection import get_db_connection

def test_connection():
    conn = get_db_connection()
    if conn:
        print("✅ SUCCESS: Connected to the Docker Database!")
        
        # Try a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        print(f"📂 Current Database: {db_name[0]}")
        
        # Check if tables exist (from your .sql file)
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("📊 Tables found:", [table[0] for table in tables])
        
        conn.close()
    else:
        print("❌ ERROR: Could not connect.")

if __name__ == "__main__":
    test_connection()