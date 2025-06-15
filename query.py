import sqlite3

def run_query(query, params=()):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

# 1. count total patients by gender.
query1 = """
SELECT gender, COUNT(*) AS count
FROM patients
GROUP BY gender;
"""

# 2. Number of appointmens per doctor
query2 = """
SELECT d.name, d.specialty, COUNT(a.id) AS total_appointments 
FROM doctors d
LEFT JOIN appointments a ON d.id = a.doctor_id
GROUP BY d.id
ORDER BY total_appointments DESC;
"""

# 3. List patients with their age (approximate)
query3 = """
SELECT name,
        (strftime('%Y', 'now') - strftime('%Y', birthdate)) AS age
FROM patients;
"""

print("Patients by Gender:")
print(f"{'Gender':<10} | {'Count':>5}")
print("-" * 18)
for row in run_query(query1):
    print(f"{row[0]:<10} | {row[1]:>5}")

print("\nAppointments per Doctor:")
print(f"{'Doctor':<20} | {'Specialty':<15} | {'Appointments':>12}")
print("-" * 53)
for row in run_query(query2):
    print(f"Dr. {row[0]:<17} | {row[1]:<15} | {row[2]:>12}")

print("\nPatients and Their Approximate Ages:")
print(f"{'Patient':<20} | {'Age':>3}")
print("-" * 26)
for row in run_query(query3):
    print(f"{row[0]:<20} | {row[1]:>3}")
