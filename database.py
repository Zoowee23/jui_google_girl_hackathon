import sqlite3

def create_database():
    print("🔄 Creating database and tables...")

    conn = sqlite3.connect("electronics_company.db")
    cursor = conn.cursor()

    # ✅ Create Products Table
    print("🛠 Creating 'products' table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL CHECK (category = 'Refrigerator'),
        warranty_period INTEGER NOT NULL,  -- Months
        price REAL NOT NULL
    )
    """)

    # ✅ Create Users Table
    print("🛠 Creating 'users' table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        product_id INTEGER NOT NULL,
        warranty_expiry DATE NOT NULL,
        last_service_date DATE,
        maintenance_plan TEXT DEFAULT 'Standard',
        sentiment TEXT DEFAULT 'Neutral',
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)

    # ✅ Create Agents Table
    print("🛠 Creating 'agents' table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    # ✅ Create Feedback Table (To Log Customer Feedback)
    print("🛠 Creating 'feedback' table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        feedback_text TEXT NOT NULL,
        sentiment TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # ✅ Create Offers Table (To Store Available Offers)
    print("🛠 Creating 'offers' table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS offers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        offer_details TEXT NOT NULL,
        valid_until DATE NOT NULL
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Database and tables created successfully!")

if __name__ == "__main__":
    create_database()
