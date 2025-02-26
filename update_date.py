import sqlite3

# Connect to the database
conn = sqlite3.connect("electronics_company.db")
cursor = conn.cursor()

# Update last service date for Bob Smith
cursor.execute("UPDATE users SET last_service_date = ? WHERE email = ?", ('2024-05-07', 'bob@example.com'))

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Last service date updated successfully!")
