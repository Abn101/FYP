from dbOperations.dbConn import get_connection

def create_chat_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            request_id INT NOT NULL,
            sender_type ENUM('client','lawyer') NOT NULL,
            sender_id INT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (request_id) REFERENCES client_requests(id)
            ON DELETE CASCADE
        );
        """

        cursor.execute(create_table_query)
        conn.commit()

        print("✅ chat_messages table created successfully!")

    except Exception as e:
        print("❌ Error creating table:", e)

    finally:
        conn.close()

create_chat_table()