-- Smart Patient Case Management System
-- Database Schema for SQLite3
-- Student: Chhaya Kolase (BCA Final Year)
-- University: G H Raisoni University, Amravati

-- 1. Users Table (Hospital Staff Authentication)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'Staff',
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Patients Table (Demographics and Contact Details)
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT,
    blood_group TEXT,
    emergency_contact TEXT,
    registered_at DATE NOT NULL DEFAULT (CURRENT_DATE),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Medical Cases Table (Medical Histories & Diagnoses)
CREATE TABLE IF NOT EXISTS medical_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    case_date DATE NOT NULL,
    chief_complaint TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    medical_history TEXT,
    allergies TEXT,
    diagnosis TEXT NOT NULL,
    treatment TEXT NOT NULL,
    doctor_notes TEXT,
    doctor_name TEXT NOT NULL,
    follow_up_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- 4. Appointments Table (Scheduling & Status Tracking)
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- Indices for fast searching
CREATE INDEX IF NOT EXISTS idx_patients_pid ON patients(patient_id);
CREATE INDEX IF NOT EXISTS idx_patients_name ON patients(name);
CREATE INDEX IF NOT EXISTS idx_cases_pid ON medical_cases(patient_id);
CREATE INDEX IF NOT EXISTS idx_cases_date ON medical_cases(case_date);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date);
