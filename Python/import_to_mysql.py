import pandas as pd
import mysql.connector
from getpass import getpass

# Ask for MySQL password securely
password = getpass("Enter your MySQL password: ")

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="ola_project"
)

cursor = connection.cursor()

# Read the complete cleaned CSV
df = pd.read_csv("Dataset/ola_cleaned.csv")

# Create a new table without disturbing old tables
cursor.execute("DROP TABLE IF EXISTS ola_rides_full")

cursor.execute("""
CREATE TABLE ola_rides_full (
    `Date` TEXT,
    `Time` TEXT,
    `Booking_ID` TEXT,
    `Booking_Status` TEXT,
    `Customer_ID` TEXT,
    `Vehicle_Type` TEXT,
    `Pickup_Location` TEXT,
    `Drop_Location` TEXT,
    `V_TAT` DOUBLE,
    `C_TAT` DOUBLE,
    `Canceled_Rides_by_Customer` TEXT,
    `Canceled_Rides_by_Driver` TEXT,
    `Incomplete_Rides` TEXT,
    `Incomplete_Rides_Reason` TEXT,
    `Booking_Value` DOUBLE,
    `Payment_Method` TEXT,
    `Ride_Distance` DOUBLE,
    `Driver_Ratings` DOUBLE,
    `Customer_Rating` DOUBLE,
    `Vehicle Images` TEXT
)
""")

# Convert missing values to SQL NULL
df = df.astype(object).where(pd.notna(df), None)

columns = ", ".join(f"`{col}`" for col in df.columns)
placeholders = ", ".join(["%s"] * len(df.columns))

query = f"INSERT INTO ola_rides_full ({columns}) VALUES ({placeholders})"

# Insert in batches
batch_size = 1000

for start in range(0, len(df), batch_size):
    batch = df.iloc[start:start + batch_size]
    cursor.executemany(query, batch.values.tolist())
    connection.commit()
    print(f"Imported {min(start + batch_size, len(df))} / {len(df)} rows")

print("Import completed successfully!")

cursor.close()
connection.close()