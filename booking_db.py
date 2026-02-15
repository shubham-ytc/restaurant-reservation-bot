import sqlite3
from datetime import datetime

DB_NAME = "booking.db"


def get_connection():
    """Create and return database connection"""
    return sqlite3.connect(DB_NAME)


def create_booking_table():
    """Create booking table if not exists"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS booking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
             
            time_slot TEXT NOT NULL,
            date TEXT NOT NULL,
            party_size INTEGER NOT NULL
        )
     """) # WE'LL ADD user_id INTEGER IN FUTURE, FOR ASSOCIATION OF USER ID WITH BOOKING REQUEST 

    conn.commit()
    conn.close()
    print(" Booking table ready.")


def insert_booking(time_slot: str, date: str, party_size: int):
    """
    Insert booking record into database

    Args:
        time_slot (str): Example: '7:00 PM - 9:00 PM'
        date (str): Example: '2026-02-14'
        party_size (int): Number of people
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO booking (time_slot, date, party_size)
        VALUES (?, ?, ?)
    """, (time_slot, date, party_size))

    conn.commit()
    conn.close()

    print("Booking inserted successfully!")


def fetch_all_bookings():
    """Fetch all booking records"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM booking")
    rows = cursor.fetchall()

    conn.close()
    return rows



if __name__ == "__main__":
    create_booking_table()

    # # Test Insert
    # insert_booking("7:00 PM - 9:00 PM", "2026-02-14", 4)
    # insert_booking("7:00 PM - 9:00 PM", "2026-02-14", 2)
    # insert_booking("7:00 PM - 9:00 PM", "2026-02-14", 3)
    # insert_booking("7:00 PM - 9:00 PM", "2026-02-14", 4)

    bookings = fetch_all_bookings()
    print("\n Current Bookings:")
    for b in bookings:
        print(b)
