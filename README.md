# Smart Patient Case Management System
### BCA Final Year Project (Session 2026–27)
**Department of Computer Applications**  
**G H Raisoni University, Amravati, Maharashtra**

---

## Academic Project Details
- **Project Title:** Smart Patient Case Management System
- **Student Name:** Chhaya Kolase
- **Course:** Bachelor of Computer Applications (BCA)
- **Semester:** Semester V
- **Session:** 2026–27
- **Project Guide:** Sarang Thakare
- **Project In-Charge:** Pranav Dabharde

---

## 1. Project Abstract
The **Smart Patient Case Management System** is an electronic medical records (EMR) and hospital clinical case management web application designed and implemented using Python, Flask, SQLite, Pandas, and Matplotlib. 

Traditional clinics and peripheral hospitals often maintain patient histories in manual, paper-based case registers or physical case files. This manual approach is vulnerable to physical record loss, time-consuming file retrievals, uncoordinated follow-ups, and inadvertent overwriting of past clinical diagnoses. 

The Smart Patient Case Management System solves these problems by providing a secure, centralized digital repository. Medical staff can register patients with auto-generated unique identifiers (`PAT-YYYY-XXXX`), maintain an immutable chronological history of medical cases, schedule consultations with automated doctor-time conflict prevention, and generate analytical statistical reports and data visualizations powered by Python Pandas and Matplotlib.

---

## 2. Project Objectives & Scope

### Objectives:
1. **Centralized Patient Record Management:** Eliminate physical register files with persistent SQLite database storage.
2. **Historical Case Integrity:** Maintain a normalized 1-to-Many case history where follow-up consultations and past diagnoses are preserved without overwriting historical medical data.
3. **Role-Based Access Control & Security:** Restrict medical records to authorized hospital staff with secure password hashing via Werkzeug.
4. **Intelligent Scheduling & Conflict Prevention:** Allow patient appointments to be booked while automatically preventing overlapping bookings for the same doctor and time slot.
5. **Healthcare Analytics & Reporting:** Ingest database records into Pandas DataFrames to perform demographic segmentation, track disease frequencies, render Matplotlib visualizations, and export datasets to CSV format.

### Scope:
- Designed specifically for multi-doctor clinics, nursing homes, and university hospital departments.
- Provides accessible, clean hospital UI with a medical blue and white aesthetic responsive on laptops, tablets, and smartphones.
- **Educational Notice:** Intended for record management, case documentation, and educational demonstration; not intended for real-time automated clinical diagnostic decisions.

---

## 3. Technology Stack

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Backend Language** | Python | 3.10+ / 3.14 | Core business logic, routing, data processing |
| **Web Framework** | Flask | 3.1+ | WSGI application routing, session handling, view controllers |
| **Authentication** | Werkzeug Security | 3.1+ | SHA-256 password hashing (`generate_password_hash`, `check_password_hash`) |
| **Database** | SQLite3 | 3.x | Lightweight, relational database with foreign key support |
| **Data Analysis** | Pandas | 2.2+ / 3.0+ | SQL-to-DataFrame transformation, `.cut()`, `.value_counts()`, CSV exporting |
| **Visualization** | Matplotlib | 3.8+ / 3.11+ | Headless Agg rendering, generation of Base64 chart graphics |
| **Frontend Structure** | HTML5 / Jinja2 | 3.1+ | Server-side template rendering, modular layout inheritance |
| **Frontend Styling** | CSS3 & FontAwesome | 6.4 | Responsive blue/white hospital theme, printable prescription layout |
| **Frontend Interactivity** | Vanilla JavaScript | ES6 | Mobile sidebar drawer, dynamic alerts, client-side table search |

---

## 4. Hardware & Software Requirements

### Minimum Software Requirements:
- **Operating System:** Windows 10/11, macOS 10.15+, or Ubuntu Linux 20.04+
- **Python Runtime:** Python 3.10 or higher
- **Web Browser:** Google Chrome, Microsoft Edge, Mozilla Firefox, or Apple Safari
- **Terminal / Shell:** PowerShell, Command Prompt, or Bash

### Minimum Hardware Requirements:
- **Processor:** Intel Core i3 / AMD Ryzen 3 or higher
- **RAM:** 4 GB minimum (8 GB recommended)
- **Disk Storage:** At least 250 MB free disk space for Python virtual environment and database

---

## 5. System Architecture & Database Design

### System Architecture Flow:
```
[ Web Browser / Client ]
         │ (HTTP GET/POST)
         ▼
[ Flask Application (app.py) ] ── (Session Authentication Guard)
         │
    ┌────┴─────────────────────────┐
    ▼                              ▼
[ Database Layer (database.py) ]   [ Analytics Engine (analytics.py) ]
    │ (Parameterized SQL)              │ (Pandas DataFrames)
    ▼                                  ▼
[ SQLite DB (database.db) ]        [ Matplotlib Base64 Charts & CSV Exports ]
```

### Database Schema (ER Structure):
The system utilizes 4 relational tables in `database.db`:

1. **`users` Table (Staff Authentication):**
   - `id` (INTEGER, PK, AUTOINCREMENT)
   - `username` (TEXT, UNIQUE, NOT NULL)
   - `password_hash` (TEXT, NOT NULL)
   - `full_name` (TEXT, NOT NULL)
   - `role` (TEXT, NOT NULL) &mdash; e.g. `'Admin'`, `'Doctor'`, `'Staff'`, `'Receptionist'`
   - `email` (TEXT)
   - `created_at` (TIMESTAMP)

2. **`patients` Table (Demographics & Contacts):**
   - `id` (INTEGER, PK, AUTOINCREMENT)
   - `patient_id` (TEXT, UNIQUE, NOT NULL) &mdash; Format: `PAT-2026-XXXX`
   - `name` (TEXT, NOT NULL)
   - `age` (INTEGER, NOT NULL)
   - `gender` (TEXT, NOT NULL)
   - `phone` (TEXT, NOT NULL)
   - `email` (TEXT)
   - `address` (TEXT)
   - `blood_group` (TEXT)
   - `emergency_contact` (TEXT)
   - `registered_at` (DATE, NOT NULL)

3. **`medical_cases` Table (Clinical Encounter Records):**
   - `id` (INTEGER, PK, AUTOINCREMENT)
   - `patient_id` (TEXT, NOT NULL, FK &rarr; `patients(patient_id)`)
   - `case_date` (DATE, NOT NULL)
   - `chief_complaint` (TEXT, NOT NULL)
   - `symptoms` (TEXT, NOT NULL)
   - `medical_history` (TEXT)
   - `allergies` (TEXT)
   - `diagnosis` (TEXT, NOT NULL)
   - `treatment` (TEXT, NOT NULL)
   - `doctor_notes` (TEXT)
   - `doctor_name` (TEXT, NOT NULL)
   - `follow_up_date` (DATE)

4. **`appointments` Table (Consultation Visits):**
   - `id` (INTEGER, PK, AUTOINCREMENT)
   - `patient_id` (TEXT, NOT NULL, FK &rarr; `patients(patient_id)`)
   - `appointment_date` (DATE, NOT NULL)
   - `appointment_time` (TEXT, NOT NULL)
   - `doctor_name` (TEXT, NOT NULL)
   - `reason` (TEXT, NOT NULL)
   - `status` (TEXT, NOT NULL) &mdash; `'Scheduled'`, `'Completed'`, `'Cancelled'`

---

## 6. Project Directory Structure

```
patient_case_management/
│
├── app.py                      # Core Flask web application and HTTP routing
├── database.py                 # SQLite database query wrappers & CRUD logic
├── analytics.py                # Pandas data analysis and Matplotlib charts engine
├── schema.sql                  # Database table definitions and indexing
├── seed_data.py                # Realistic demo dataset generator script
├── test_app.py                 # Automated unit test suite (9 test cases)
├── requirements.txt            # Python package dependencies
├── README.md                   # Project documentation and student guide
├── database.db                 # SQLite database file (created automatically)
│
├── static/
│   ├── css/
│   │   └── style.css           # Clean hospital theme (medical blue & white)
│   └── js/
│       └── script.js           # Client-side validation, alerts, and print triggers
│
├── templates/
│   ├── base.html               # Main master layout (sidebar, topbar, alert flashes)
│   ├── login.html              # Hospital staff login portal with demo credentials
│   ├── dashboard.html          # Clinical statistics cards, today's appointments, intake
│   ├── patients.html           # Patients table with server/client search filters
│   ├── add_patient.html        # Patient registration form with auto-generated ID
│   ├── edit_patient.html       # Edit patient demographic information
│   ├── patient_details.html    # Patient profile, case history timeline, appointments
│   ├── medical_cases.html      # Cases directory with diagnosis and date filtering
│   ├── add_case.html           # New medical case diagnosis & prescription form
│   ├── case_details.html       # Printable clinical case sheet with signature block
│   ├── edit_case.html          # Edit existing case notes and findings
│   ├── appointments.html       # Appointment scheduler with conflict guard
│   ├── reports.html            # Pandas analytics summary & Matplotlib visual charts
│   └── project_info.html       # Academic viva questions, student & mentor credits
│
└── reports/                    # Local reports directory for data exports
```

---

## 7. Installation & Running Instructions

### Step 1: Open Terminal / PowerShell
Open Windows PowerShell or Command Prompt and navigate to the project directory:
```powershell
cd c:\Users\chhay\OneDrive\Desktop\patient_case_management
```

### Step 2: Install Python Dependencies
Install required packages using pip:
```powershell
pip install -r requirements.txt
```
*(Dependencies: Flask, Werkzeug, Pandas, Matplotlib)*

### Step 3: Initialize Database & Populate Demo Data
Run the seed script to create all tables and populate realistic patients, cases, and appointments:
```powershell
python seed_data.py
```

### Step 4: Run the Automated Test Suite (Optional)
Verify that all 9 unit test cases pass:
```powershell
python test_app.py
```

### Step 5: Start the Flask Web Server
Run the Flask server:
```powershell
python app.py
```

### Step 6: Access the Application in Your Web Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 8. Hospital Staff Demo Credentials

| Username | Password | Full Name | Role | Access Level |
| :--- | :--- | :--- | :--- | :--- |
| `admin` | `admin123` | System Administrator | Admin | Full Access |
| `chhaya` | `chhaya123` | Chhaya Kolase | Staff / Project Lead | Full Staff Access |
| `dr_sarang` | `doctor123` | Dr. Sarang Thakare | Doctor | Clinical & Prescriptions |
| `dr_pranav` | `doctor123` | Dr. Pranav Dabharde | Doctor | Clinical & Prescriptions |
| `reception` | `hospital123` | Aarti Shinde | Receptionist | Front-desk & Registration |

---

## 9. Module-by-Module Description

### 1. Authentication & Security Module (`app.py`, `database.py`)
- Restricts patient records behind session-based login.
- `@login_required` decorator validates active user session before allowing access to any medical routes.
- Employs PBKDF2/SHA-256 cryptographic password hashing via `werkzeug.security`.

### 2. Dashboard Module (`templates/dashboard.html`)
- Displays real-time metric counters: Total Patients, Total Cases, Today's Scheduled Appointments, Active Doctors.
- Displays Today's Appointments with one-click status updates (`Mark as Completed`).
- Lists Recently Registered Patients with quick links to their medical folders.
- Displays quick Pandas analytical summaries.

### 3. Patient Registration Module (`templates/add_patient.html`, `templates/patients.html`)
- Auto-generates unique sequential identifiers (e.g. `PAT-2026-0001`).
- Validates mandatory fields: Name, Age (0–125), Gender, and Phone Number.
- Provides search filters by Patient ID, Name, or Phone number.

### 4. Medical Case History Module (`templates/add_case.html`, `templates/case_details.html`)
- Maintains a sequential, multi-case medical history per patient without overwriting past clinical data.
- Records Chief Complaint, Symptoms, Medical History, Allergies, Diagnosis, Prescribed Treatment & Medications, Doctor Notes, and Follow-up Date.
- Provides a **Printable Clinical Case Sheet** with official hospital header, patient demographic box, and doctor signature block.

### 5. Appointment Scheduling & Conflict Guard (`templates/appointments.html`)
- Schedules visits with Date, Time Slot, Doctor, and Reason for Visit.
- **Conflict Guard:** Validates whether the designated doctor already has an overlapping appointment scheduled for that exact time slot and alerts staff to select another time or physician.
- Tracks statuses: `Scheduled`, `Completed`, and `Cancelled`.

### 6. Analytics & Reports Module (`analytics.py`, `templates/reports.html`)
- **Pandas Data Analysis:** Reads SQLite tables into DataFrames to calculate age cohorts (`0-12 Child`, `13-19 Teen`, `20-39 Young Adult`, `40-59 Middle-Aged`, `60+ Senior`), monthly trends, and diagnosis frequencies.
- **Matplotlib Visualization:** Generates 4 clean charts (Monthly Trend, Age Distribution, Top Diagnoses, Gender Ratio) encoded to Base64 strings.
- **CSV Data Export:** Allows authorized staff to export patients, medical cases, and appointments into downloadable CSV files.

---

## 10. Test Cases & Verification Matrix

| Test ID | Module Tested | Input / Condition | Expected Result | Status |
| :---: | :--- | :--- | :--- | :---: |
| **TC-01** | Database Setup | Run `init_db()` and table query | All 4 tables (`users`, `patients`, `medical_cases`, `appointments`) created | **PASS** |
| **TC-02** | Staff Login | Valid credentials (`admin`/`admin123`) | Authenticated session created, redirected to Dashboard | **PASS** |
| **TC-03** | Auth Rejection | Wrong password (`admin`/`wrongpass`) | Access denied, flash alert displayed | **PASS** |
| **TC-04** | Route Guard | Access `/dashboard` without session | Redirected to `/login` | **PASS** |
| **TC-05** | ID Generation | Register new patient | Generated ID follows `PAT-2026-XXXX` format | **PASS** |
| **TC-06** | Case History | Add second case for existing patient | Case appended to timeline; previous case preserved | **PASS** |
| **TC-07** | Conflict Guard | Book duplicate doctor + date + time | Conflict detected, appointment rejected with alert | **PASS** |
| **TC-08** | Visual Charts | Ingest database into `analytics.py` | 4 Matplotlib Base64 images generated successfully | **PASS** |
| **TC-09** | CSV Export | Click "Export Patients CSV" | Downloadable CSV file generated via Pandas | **PASS** |

---

## 11. Viva Voce Questions & Answers (Student Preparation)

**Q1: What is the main objective of your BCA final-year project?**  
*Answer:* The objective of the Smart Patient Case Management System is to build a modern, secure, and digitized electronic healthcare record system for clinics and hospitals. It replaces manual paper registers with an SQLite database, preserves multi-case clinical histories per patient, prevents appointment scheduling conflicts, and provides analytical reporting using Python Pandas and Matplotlib.

**Q2: Why did you choose SQLite instead of MySQL or PostgreSQL?**  
*Answer:* SQLite is a serverless, self-contained, zero-configuration relational database engine. It stores data in a single file (`database.db`), supports standard SQL with foreign key constraints, and requires no external server daemon, making it lightweight, robust, and ideal for single-clinic management and educational demonstration.

**Q3: How did you implement security and protect user passwords?**  
*Answer:* Passwords are never stored in plain text. We utilize Werkzeug's cryptographic hashing algorithms (`generate_password_hash` and `check_password_hash`). Even if the SQLite file is inspected directly, the passwords cannot be reversed. Furthermore, all SQL queries strictly use parameterized statements (`?` placeholders) to prevent SQL injection attacks.

**Q4: How does your system ensure previous medical cases are not overwritten?**  
*Answer:* We implemented a normalized 1-to-Many relational database model. One patient in the `patients` table can have multiple corresponding rows in the `medical_cases` table linked by the foreign key `patient_id`. Each doctor consultation is appended as a new record, allowing the patient details page to render a complete chronological clinical history.

**Q5: What role does Pandas play in your project?**  
*Answer:* Pandas is used in the data analytics and reporting engine (`analytics.py`). It ingests SQL tables into DataFrames using `pd.read_sql_query()`. We use Pandas functions like `pd.cut()` to classify patients into distinct age cohorts and `.value_counts()` to compute disease frequencies and appointment statuses, as well as `DataFrame.to_csv()` for automated CSV report downloads.

**Q6: How are Matplotlib charts displayed on the web page?**  
*Answer:* To avoid saving temporary image files to the server disk and risking cache synchronization issues, we use Matplotlib with the non-GUI `Agg` backend. The chart is rendered directly to an in-memory byte buffer (`io.BytesIO`), encoded into a Base64 string, and passed directly into the Jinja2 HTML template (`<img src="data:image/png;base64,...">`).

---

## 12. Academic Declaration

> **Project Title:** Smart Patient Case Management System  
> **Student:** Chhaya Kolase  
> **Degree:** Bachelor of Computer Applications (BCA)  
> **Institution:** G H Raisoni University, Amravati  
> **Academic Session:** 2026–27  
> **Project Guide:** Sarang Thakare  
> **Project In-Charge:** Pranav Dabharde  
>
> *This application has been designed, implemented, and documented as a practical final-year project demonstrating full-stack software development with Python, Flask, SQLite, Pandas, and Matplotlib.*
