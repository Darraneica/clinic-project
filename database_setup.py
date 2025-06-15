import sqlite3

# connect to the database - creates the file if it doesn't exist.
conn = sqlite3.connect('clinic.db')
cursor = conn.cursor()

# create patients table
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
gender TEXT,
birthdate DATE,
contact TEXT
)
''')

# create doctors table
cursor.execute('''
CREATE TABLE IF NOT EXISTS doctors (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
specialty TEXT
)
''')

# create appointments table
cursor.execute('''
CREATE TABLE IF NOT EXISTS appointments (
id INTEGER PRIMARY KEY AUTOINCREMENT,
patient_id INTEGER,
doctor_id, INTEGER,
appointment_date TEXT,
reason TEXT,
FOREIGN KEY (patient_id) REFERENCES patients(id),
FOREIGN KEY (doctor_id) REFERENCES doctors(id)
)
''')

# sample doctors

cursor.execute("INSERT INTO doctors (name, specialty) VALUES ('Dr. Smith', 'Cardiology')")
cursor.execute("INSERT INTO doctors (name, specialty) VALUES ('Dr. Patel', 'Pulmonology')")
cursor.execute("INSERT INTO doctors (name, specialty) VALUES ('Dr. Johnson', 'Dermatology')")

# sample patients

cursor.execute("INSERT INTO patients (name, gender, birthdate, contact) VALUES ('Allison Johnson', 'Female', '1990-05-12', '555-1234')")
cursor.execute("INSERT INTO patients (name, gender, birthdate, contact) VALUES ('Bob Lee', 'Male', '1985-09-22', '555-5678')")
cursor.execute("INSERT INTO patients (name, gender, birthdate, contact) VALUES ('Maria Lopez', 'Female', '1978-11-03', '555-9876')")

# sample appointments

cursor.execute("INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason) VALUES (1, 1, '2025-06-15', 'Chest pain')")
cursor.execute("INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason) VALUES (2, 2, '2025-06-16', 'Cough')")
cursor.execute("INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason) VALUES (3, 3, '2025-06-17', 'Check up')")

conn.commit()
conn.close()

print("Database and tables created successfully.")