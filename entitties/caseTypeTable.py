from dbOperations.dbConn import get_connection

def create_case_types_table():
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS case_types (
        id INT AUTO_INCREMENT PRIMARY KEY,
        case_name VARCHAR(100) NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    cursor.execute(create_table_query)
    conn.commit()
    print("✅ Case Types table created successfully!")
    
    conn.close()