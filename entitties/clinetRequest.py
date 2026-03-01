from dbOperations.dbConn import get_connection

def create_user_requests_table():
    conn = get_connection()
    if not conn:
        print("❌ Database connection failed")
        return

    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS client_requests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        client_id INT NOT NULL,
        lawyer_id INT NOT NULL,
        case_type_id INT NOT NULL,
        description TEXT,
        status ENUM('Pending', 'Accepted', 'Rejected', 'Closed') DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
        FOREIGN KEY (lawyer_id) REFERENCES lawyers(id) ON DELETE CASCADE,
        FOREIGN KEY (case_type_id) REFERENCES case_types(id) ON DELETE CASCADE
    )
    """

    cursor.execute(create_table_query)
    conn.commit()
    print("✅ User Requests table created successfully!")

    conn.close()
create_user_requests_table()
