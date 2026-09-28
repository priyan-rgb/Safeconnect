import sqlite3

conn = sqlite3.connect("safeconnect.db")
cursor = conn.cursor()

tables = [
    "users",
    "complaints",
    "emergency_contacts",
    "emergency_alerts",
    "notifications"
]

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]

    print(f"{table}: {count} records")

conn.close()