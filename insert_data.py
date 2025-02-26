import sqlite3

def insert_data():
    conn = sqlite3.connect("electronics_company.db")
    cursor = conn.cursor()

    # ✅ Insert Products Data (Only Refrigerators)
    print("🔄 Inserting sample products...")
    products_data = [
        ("LG Smart Fridge", "Refrigerator", 12, 699.99),
        ("Samsung Double Door", "Refrigerator", 24, 1299.99),
        ("Whirlpool Compact", "Refrigerator", 18, 299.99)
    ]
    cursor.executemany("INSERT INTO products (name, category, warranty_period, price) VALUES (?, ?, ?, ?)", products_data)

    # ✅ Insert Users Data (Linked to Products) - Avoid Duplicate Emails
    print("🔄 Inserting sample users...")
    users_data = [
        ("Alice Johnson", "alice@example.com", 1, "2025-06-15", "2024-06-01", "Premium", "Neutral"),
        ("Bob Smith", "bob@example.com", 2, "2024-01-10", "2026-11-05", "Standard", "Positive")
    ]
    for user in users_data:
        cursor.execute("SELECT email FROM users WHERE email = ?", (user[1],))
        if cursor.fetchone() is None:  # Insert only if email doesn't exist
            cursor.execute("INSERT INTO users (name, email, product_id, warranty_expiry, last_service_date, maintenance_plan, sentiment) VALUES (?, ?, ?, ?, ?, ?, ?)", user)
        else:
            print(f"⚠️ User with email {user[1]} already exists. Skipping.")

    # ✅ Insert Agents Data - Avoid Duplicate Emails
    print("🔄 Inserting sample agents...")
    agents_data = [
        ("John Agent", "john.agent@example.com", "+123456789"),
        ("Sarah Help", "sarah.help@example.com", "+987654321")
    ]
    for agent in agents_data:
        cursor.execute("SELECT email FROM agents WHERE email = ?", (agent[1],))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO agents (name, email, phone) VALUES (?, ?, ?)", agent)
        else:
            print(f"⚠️ Agent with email {agent[1]} already exists. Skipping.")

    # ✅ Insert Sample Feedback Data
    print("🔄 Inserting sample feedback...")
    feedback_data = [
        (1, "I love my refrigerator, works great!", "Positive"),
        (2, "Cooling issue detected, needs repair!", "Negative")
    ]
    cursor.executemany("INSERT INTO feedback (user_id, feedback_text, sentiment) VALUES (?, ?, ?)", feedback_data)

    # ✅ Insert Sample Offers Data - Avoid Duplicate Offers
    print("🔄 Inserting sample offers...")
    offers_data = [
        ("10% off on refrigerator maintenance plans!", "2025-12-31"),
        ("Free servicing for first-year customers!", "2025-06-30"),
        ("Exclusive cashback on refrigerator upgrades!", "2025-08-15")
    ]
    for offer in offers_data:
        cursor.execute("SELECT offer_details FROM offers WHERE offer_details = ?", (offer[0],))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO offers (offer_details, valid_until) VALUES (?, ?)", offer)
        else:
            print(f"⚠️ Offer '{offer[0]}' already exists. Skipping.")

    conn.commit()
    conn.close()
    print("✅ Sample data inserted successfully!")

if __name__ == "__main__":
    insert_data()
