import sqlite3

def run_query(query, params=()):
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def add_patient():
    name = input("Enter patient name: ")
    gender = input("Enter gender (Male/Female): ")
    birthdate = input("Enter birthdate (YYYY-MM-DD): ")
    contact = input("Enter contact info: ")
    run_query(
        "INSERT INTO patients (name, gender, birthdate, contact) VALUES (?, ?, ?, ?)",
        (name, gender, birthdate, contact)
    )
    print("Patient added successfully!")

def update_patient():
    list_patients()
    patient_id = input("Enter the ID of the patient you want to update: ")
    updated_name = input("Enter new name (leave blank to keep current.): ")
    updated_birthdate = input("Enter new birthdate (YYYY-MM-DD, leave blank to keep current.): ")
    updated_contact = input("Enter new contact info (leave blank to keep current.): ")
    
    # get current values
    current = run_query("SELECT name, gender, birthdate, contact FROM patients WHERE id = ?", (patient_id))
    if not current:
        print("Patient not found.\n")
        return
    current = current[0]

    # replaces blanks with current values

    name = updated_name if updated_name else current[0]
    birthdate = updated_birthdate if updated_birthdate  else current[2]
    contact = updated_contact if updated_contact else current[3]

    run_query(
        "UPDATE patients SET name = ?, birthdate = ?, contact = ? WHERE id = ?", 
        (name, birthdate, contact, patient_id)
    )
    print("Patient record updated. \n")
    
def delete_patient():
    list_patients()
    patient_id = input ("Enter the ID of the patient to delete: ")
    confirm = input("Are you sure you want to delete this patient? (Y/N): ")
    if confirm.lower() == "yes" or "Y":
        run_query("DELETE FROM patients WHERE id = ?", (patient_id))
        print("Patient delete.\n")
    else:
        print("Delete canclled.\n")

def list_patients():
    patients = run_query("SELECT id, name, gender, birthdate FROM patients")
    print("\nPatients:")
    for p in patients:
        print(f"{p[0]}: {p[1]} ({p[2]}, born {p[3]})")
        print()

def list_doctors():
    doctors = run_query("SELECT id, name, specialty FROM doctors")
    print("\nDoctors:")
    for d in doctors:
        print(f"{d[0]}:{d[1]} ({d[2]})")
        print()

def add_appointment():
    list_patients()
    patient_id = input("Enter patient ID for appointment.")
    list_doctors()
    doctor_id = input("Enter doctor ID for appointment: ")
    date = input("Enter appointment date (YYYY-MM-DD): ")
    reason = input("Enter reason for appointment: ")
    run_query(
        "INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason) VALUES (?, ?, ?, ?)",
        (patient_id, doctor_id, date, reason)
    )
    print("Appointment added successfully!")

def list_appointments():
    query = """
    SELECT a.id, p.name, d.name, a.appointment_date, a.reason
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors D ON a.doctor_id = d.id
    ORDER BY a.appointment_date
    """
    appointments = run_query(query)
    print("\nAppointments:")
    for a in appointments:
        print(f"{a[0]}: with Dr. {a[2]} - {a[4]}")
        print()

def search_appointments_by_patient():
    name_query = input("Enter the patient's name to search: ").strip()

    query = """
    SELECT a.id, p.name, d.name, a.appointment_date, a.reason
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors d ON a.doctor_id = d.id
    WHERE p.name LIKE ?
    ORDER BY a.appointment_date
    """
    results = run_query(query, (f"%{name_query}%",))

    if results:
        print("\nMatching Appointments:")
        for a in results:
            print(f"{a[0]}: {a[1]} with {a[2]} on {a[3]} - {a[4]}")
            print()
        else:
            print("No appointments found for that name.\n.")

def report_appointments_per_doctor():
    query="""
    SELECT d.name, COUNT(a.id) as total_appointments
    FROM doctors d
    LEFT JOIN appointments a ON d.id = a.doctor_id
    GROUP BY d.name
    ORDER BY total_appointments DESC
    """

    results = run_query(query)

    print("\nAppointments per Doctor:")
    print("-" * 35)
    for row in results:
        print(f"{row[0]: <20} | {row[1]} appointments")
    print()

def monthly_report():
    query = """
    SELECT
        strftime('%Y-%m', appointment_date) AS month,
        COUNT(*) as total_appointments
    FROM appointments
    GROUP BY month
    ORDER BY month
    """

    results = run_query(query)

    print("\nMonthly Appointment Trends:")
    print("-" * 35)
    for row in results:
        print(f"{row[0]} | {row[1]} appointments")
    print()

def menu():
    while True:
        print("""
    --- Clinic Appointment System
    1. List Patients
    2. Add Patient
    3. Update Patient
    4. Delete Patient
    5. List doctors
    6. List appointments
    7. Add appointments
    8. Search Appointments
    9. View Appointments Per Doctor
    10. Monthly Appointment Trends
    11. Exit
    """)
        choice = input("Choose an option (1-9):")
        if choice == '1':
            list_patients()
        elif choice == '2':
            add_patient()
        elif choice == '3':
            update_patient()
        elif choice == '4':
            delete_patient()
        elif choice == '5':
            list_doctors()
        elif choice == '6':
         list_appointments()
        elif choice == '7':
         add_appointment()
        elif choice == '8':
            search_appointments_by_patient()
        elif choice == '9':
            report_appointments_per_doctor()
        elif choice == '10':
            monthly_report()
        elif choice == '11':
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    menu()