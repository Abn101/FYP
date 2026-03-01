from dbOperations.dbConn import get_connection

def create_lawyers_table():
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS lawyers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        case_type_id INT NOT NULL,
        verification_code VARCHAR(10),
        is_verified TINYINT(1) DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_type_id) REFERENCES case_types(id)
    )
    """
    
    cursor.execute(create_table_query)
    conn.commit()
    print("✅ Lawyers table created successfully!")
    
    conn.close()
