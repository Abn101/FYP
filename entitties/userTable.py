from dbOperations.dbConn import get_connection

def create_clients_table():
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    create_table_query =  """
    CREATE TABLE IF NOT EXISTS clients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        special_code VARCHAR(4), -- 4-digit code for email verification
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    
    cursor.execute(create_table_query)
    conn.commit()
    print("✅ Clients table created successfully!")
    
    conn.close()