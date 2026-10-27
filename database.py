"""
database.py - Database operations and connection management
Smart Patient Case Management System
Student: Chhaya Kolase | G H Raisoni University, Amravati
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "database.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


def get_db_connection():
    """Establish and return a SQLite database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the database schema using schema.sql."""
    conn = get_db_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized successfully.")


# ==========================================
# USER MANAGEMENT & AUTHENTICATION
# ==========================================

def get_user_by_username(username):
    """Retrieve user record by username."""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username.strip(),)
    ).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    """Retrieve user record by user ID."""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return user


def create_user(username, password, full_name, role="Staff", email=None):
    """Create a new user with securely hashed password."""
    conn = get_db_connection()
    password_hash = generate_password_hash(password)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, full_name, role, email)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username.strip(), password_hash, full_name.strip(), role.strip(), email.strip() if email else None),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return new_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def verify_user(username, password):
    """Verify user credentials against stored hash."""
    user = get_user_by_username(username)
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def get_all_users():
    """Retrieve all users."""
    conn = get_db_connection()
    users = conn.execute("SELECT id, username, full_name, role, email, created_at FROM users ORDER BY full_name").fetchall()
    conn.close()
    return users


# ==========================================
# PATIENT MANAGEMENT
# ==========================================

def generate_patient_id():
    """
    Generate the next unique patient ID in format: PAT-YYYY-XXXX
    e.g., PAT-2026-0001
    """
    current_year = datetime.now().year
    prefix = f"PAT-{current_year}-"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT patient_id FROM patients WHERE patient_id LIKE ? ORDER BY id DESC LIMIT 1",
        (f"{prefix}%",),
    )
    last_record = cursor.fetchone()
    conn.close()

    if last_record and last_record["patient_id"]:
        try:
            last_seq = int(last_record["patient_id"].split("-")[-1])
            new_seq = last_seq + 1
        except (ValueError, IndexError):
            new_seq = 1
    else:
        new_seq = 1

    return f"{prefix}{new_seq:04d}"


def add_patient(patient_id, name, age, gender, phone, email, address, blood_group, emergency_contact, registered_at=None):
    """Insert a new patient into the database."""
    if not registered_at:
        registered_at = datetime.now().strftime("%Y-%m-%d")
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO patients (patient_id, name, age, gender, phone, email, address, blood_group, emergency_contact, registered_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (patient_id.strip(), name.strip(), int(age), gender.strip(), phone.strip(), 
         email.strip() if email else None, address.strip() if address else None, 
         blood_group.strip() if blood_group else None, emergency_contact.strip() if emergency_contact else None, 
         registered_at),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_patients(search_query=None):
    """Retrieve all patients, optionally filtered by ID, name, or phone."""
    conn = get_db_connection()
    if search_query:
        pattern = f"%{search_query.strip()}%"
        patients = conn.execute(
            """
            SELECT * FROM patients
            WHERE patient_id LIKE ? OR name LIKE ? OR phone LIKE ?
            ORDER BY id DESC
            """,
            (pattern, pattern, pattern),
        ).fetchall()
    else:
        patients = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    conn.close()
    return patients


def get_patient_by_id(patient_id):
    """Retrieve a single patient by their unique patient_id string or integer id."""
    conn = get_db_connection()
    if isinstance(patient_id, int) or (isinstance(patient_id, str) and patient_id.isdigit()):
        patient = conn.execute("SELECT * FROM patients WHERE id = ?", (int(patient_id),)).fetchone()
    else:
        patient = conn.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id.strip(),)).fetchone()
    conn.close()
    return patient


def update_patient(patient_id, name, age, gender, phone, email, address, blood_group, emergency_contact):
    """Update existing patient details."""
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE patients
        SET name = ?, age = ?, gender = ?, phone = ?, email = ?, address = ?, blood_group = ?, emergency_contact = ?
        WHERE patient_id = ?
        """,
        (name.strip(), int(age), gender.strip(), phone.strip(), 
         email.strip() if email else None, address.strip() if address else None, 
         blood_group.strip() if blood_group else None, emergency_contact.strip() if emergency_contact else None, 
         patient_id.strip()),
    )
    conn.commit()
    conn.close()


def delete_patient(patient_id):
    """Delete a patient and their related records."""
    conn = get_db_connection()
    conn.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id.strip(),))
    conn.commit()
    conn.close()


def count_patients():
    """Return the total count of registered patients."""
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    conn.close()
    return count


def get_recent_patients(limit=5):
    """Return recently registered patients."""
    conn = get_db_connection()
    patients = conn.execute(
        "SELECT * FROM patients ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return patients


# ==========================================
# MEDICAL CASES MANAGEMENT
# ==========================================

def add_medical_case(patient_id, case_date, chief_complaint, symptoms, medical_history,
                     allergies, diagnosis, treatment, doctor_notes, doctor_name, follow_up_date=None):
    """Add a new medical case record for a patient."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO medical_cases (
            patient_id, case_date, chief_complaint, symptoms, medical_history,
            allergies, diagnosis, treatment, doctor_notes, doctor_name, follow_up_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (patient_id.strip(), case_date, chief_complaint.strip(), symptoms.strip(),
         medical_history.strip() if medical_history else None,
         allergies.strip() if allergies else None,
         diagnosis.strip(), treatment.strip(),
         doctor_notes.strip() if doctor_notes else None,
         doctor_name.strip(), follow_up_date if follow_up_date else None),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_cases_by_patient(patient_id):
    """Retrieve chronological case history for a specific patient."""
    conn = get_db_connection()
    cases = conn.execute(
        """
        SELECT * FROM medical_cases
        WHERE patient_id = ?
        ORDER BY case_date DESC, id DESC
        """,
        (patient_id.strip(),),
    ).fetchall()
    conn.close()
    return cases


def get_case_by_id(case_id):
    """Retrieve a single medical case by its primary key with joined patient info."""
    conn = get_db_connection()
    case = conn.execute(
        """
        SELECT c.*, p.name AS patient_name, p.age, p.gender, p.phone, p.blood_group
        FROM medical_cases c
        JOIN patients p ON c.patient_id = p.patient_id
        WHERE c.id = ?
        """,
        (case_id,),
    ).fetchone()
    conn.close()
    return case


def get_all_cases(search_query=None, diagnosis_filter=None, date_from=None, date_to=None):
    """Retrieve all medical cases with search and filter capabilities."""
    conn = get_db_connection()
    query = """
        SELECT c.*, p.name AS patient_name, p.phone
        FROM medical_cases c
        JOIN patients p ON c.patient_id = p.patient_id
        WHERE 1=1
    """
    params = []

    if search_query:
        pattern = f"%{search_query.strip()}%"
        query += " AND (c.patient_id LIKE ? OR p.name LIKE ? OR c.diagnosis LIKE ? OR c.chief_complaint LIKE ?)"
        params.extend([pattern, pattern, pattern, pattern])

    if diagnosis_filter:
        pattern = f"%{diagnosis_filter.strip()}%"
        query += " AND c.diagnosis LIKE ?"
        params.append(pattern)

    if date_from:
        query += " AND c.case_date >= ?"
        params.append(date_from)

    if date_to:
        query += " AND c.case_date <= ?"
        params.append(date_to)

    query += " ORDER BY c.case_date DESC, c.id DESC"
    cases = conn.execute(query, params).fetchall()
    conn.close()
    return cases


def update_medical_case(case_id, case_date, chief_complaint, symptoms, medical_history,
                        allergies, diagnosis, treatment, doctor_notes, doctor_name, follow_up_date=None):
    """Update an existing medical case."""
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE medical_cases
        SET case_date = ?, chief_complaint = ?, symptoms = ?, medical_history = ?,
            allergies = ?, diagnosis = ?, treatment = ?, doctor_notes = ?,
            doctor_name = ?, follow_up_date = ?
        WHERE id = ?
        """,
        (case_date, chief_complaint.strip(), symptoms.strip(),
         medical_history.strip() if medical_history else None,
         allergies.strip() if allergies else None,
         diagnosis.strip(), treatment.strip(),
         doctor_notes.strip() if doctor_notes else None,
         doctor_name.strip(), follow_up_date if follow_up_date else None,
         case_id),
    )
    conn.commit()
    conn.close()


def count_cases():
    """Return the total number of medical cases recorded."""
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(*) FROM medical_cases").fetchone()[0]
    conn.close()
    return count


# ==========================================
# APPOINTMENT MANAGEMENT
# ==========================================

def schedule_appointment(patient_id, appointment_date, appointment_time, doctor_name, reason, status="Scheduled"):
    """Schedule a new patient appointment."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO appointments (patient_id, appointment_date, appointment_time, doctor_name, reason, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (patient_id.strip(), appointment_date, appointment_time.strip(), doctor_name.strip(), reason.strip(), status),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def check_appointment_conflict(doctor_name, appointment_date, appointment_time, exclude_id=None):
    """
    Check if the doctor already has a scheduled appointment on the same date and time.
    Returns the conflicting appointment record if found, else None.
    """
    conn = get_db_connection()
    query = """
        SELECT a.*, p.name AS patient_name
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        WHERE a.doctor_name = ? AND a.appointment_date = ? AND a.appointment_time = ? AND a.status = 'Scheduled'
    """
    params = [doctor_name.strip(), appointment_date, appointment_time.strip()]

    if exclude_id:
        query += " AND a.id != ?"
        params.append(exclude_id)

    conflict = conn.execute(query, params).fetchone()
    conn.close()
    return conflict


def get_all_appointments(filter_status=None, filter_date=None):
    """Retrieve appointments with optional status and date filters."""
    conn = get_db_connection()
    query = """
        SELECT a.*, p.name AS patient_name, p.phone
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        WHERE 1=1
    """
    params = []

    if filter_status and filter_status != "All":
        query += " AND a.status = ?"
        params.append(filter_status)

    if filter_date:
        query += " AND a.appointment_date = ?"
        params.append(filter_date)

    query += " ORDER BY a.appointment_date ASC, a.appointment_time ASC"
    appointments = conn.execute(query, params).fetchall()
    conn.close()
    return appointments


def get_today_appointments():
    """Retrieve all appointments scheduled for today."""
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_db_connection()
    appointments = conn.execute(
        """
        SELECT a.*, p.name AS patient_name, p.phone
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        WHERE a.appointment_date = ?
        ORDER BY a.appointment_time ASC
        """,
        (today,),
    ).fetchall()
    conn.close()
    return appointments


def get_patient_appointments(patient_id):
    """Retrieve all appointments for a specific patient."""
    conn = get_db_connection()
    appointments = conn.execute(
        """
        SELECT * FROM appointments
        WHERE patient_id = ?
        ORDER BY appointment_date DESC, appointment_time DESC
        """,
        (patient_id.strip(),),
    ).fetchall()
    conn.close()
    return appointments


def update_appointment_status(appointment_id, new_status):
    """Update appointment status (Scheduled, Completed, Cancelled)."""
    conn = get_db_connection()
    conn.execute(
        "UPDATE appointments SET status = ? WHERE id = ?",
        (new_status, appointment_id),
    )
    conn.commit()
    conn.close()


def count_today_appointments():
    """Return count of today's appointments."""
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_db_connection()
    count = conn.execute(
        "SELECT COUNT(*) FROM appointments WHERE appointment_date = ?", (today,)
    ).fetchone()[0]
    conn.close()
    return count


def get_available_doctors():
    """Return list of distinct doctors in the system."""
    conn = get_db_connection()
    # Doctors from users table plus any distinct doctors in cases/appointments
    doctors_db = conn.execute(
        "SELECT full_name FROM users WHERE role IN ('Doctor', 'Admin', 'Staff')"
    ).fetchall()
    conn.close()
    
    docs = [d["full_name"] for d in doctors_db]
    default_docs = [
        "Dr. Sarang Thakare (MD, Internal Medicine)",
        "Dr. Pranav Dabharde (MBBS, General Physician)",
        "Dr. Anjali Deshmukh (MD, Cardiology)",
        "Dr. Rajesh Patil (MS, Orthopedics)",
        "Dr. Snehal Kulkarni (MD, Pediatrics)"
    ]
    for d in default_docs:
        if d not in docs:
            docs.append(d)
    return docs
