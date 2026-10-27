"""
seed_data.py - Database initialization and realistic fictional seed records.
Smart Patient Case Management System
Student: Chhaya Kolase | G H Raisoni University, Amravati
"""

import os
from datetime import datetime, timedelta
from database import init_db, get_db_connection, create_user, add_patient, add_medical_case, schedule_appointment

def seed():
    print("=" * 60)
    print("Initializing Database & Populating Realistic Demo Data...")
    print("=" * 60)
    
    init_db()
    conn = get_db_connection()
    
    # Check if data already exists
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if user_count > 0:
        print("Database already has records. Clearing existing tables for fresh seed...")
        conn.execute("DELETE FROM appointments")
        conn.execute("DELETE FROM medical_cases")
        conn.execute("DELETE FROM patients")
        conn.execute("DELETE FROM users")
        conn.commit()
    conn.close()

    # 1. Create Staff Users
    print("[1/4] Creating Staff User Accounts...")
    users_data = [
        ("admin", "admin123", "System Administrator", "Admin", "admin@hospital.org"),
        ("chhaya", "chhaya123", "Chhaya Kolase", "Staff", "chhaya.kolase@ghru.edu.in"),
        ("dr_sarang", "doctor123", "Dr. Sarang Thakare", "Doctor", "dr.sarang@hospital.org"),
        ("dr_pranav", "doctor123", "Dr. Pranav Dabharde", "Doctor", "dr.pranav@hospital.org"),
        ("reception", "hospital123", "Aarti Shinde (Desk)", "Receptionist", "reception@hospital.org"),
    ]
    for username, password, full_name, role, email in users_data:
        uid = create_user(username, password, full_name, role, email)
        print(f"  + User created: {username} ({role}) - Pass: {password}")

    # 2. Create Fictional Patients
    print("\n[2/4] Registering Fictional Patients...")
    today = datetime.now()
    
    patients_data = [
        ("PAT-2026-0001", "Rameshwar Deshmukh", 54, "Male", "9823011223", "rameshwar.d@gmail.com", "Rathi Nagar, Amravati", "B+", "Sunita Deshmukh (Wife): 9823011224", (today - timedelta(days=95)).strftime("%Y-%m-%d")),
        ("PAT-2026-0002", "Pooja Santosh Kulkarni", 28, "Female", "9422894561", "pooja.kulkarni@yahoo.com", "Gadge Nagar, Amravati", "O+", "Santosh Kulkarni (Father): 9422894560", (today - timedelta(days=80)).strftime("%Y-%m-%d")),
        ("PAT-2026-0003", "Aarav Nitin Wankhade", 9, "Male", "9890123456", "nitin.wankhade@gmail.com", "Camp Area, Amravati", "A+", "Nitin Wankhade (Father): 9890123456", (today - timedelta(days=65)).strftime("%Y-%m-%d")),
        ("PAT-2026-0004", "Sunita Anand Gawande", 62, "Female", "9765432109", "sunita.g@outlook.com", "Badnera Road, Amravati", "AB+", "Anand Gawande (Husband): 9765432108", (today - timedelta(days=50)).strftime("%Y-%m-%d")),
        ("PAT-2026-0005", "Mohammad Farhan Sheikh", 35, "Male", "9158765432", "farhan.sheikh@gmail.com", "Walgaon Road, Amravati", "O-", "Yasmin Sheikh (Wife): 9158765430", (today - timedelta(days=42)).strftime("%Y-%m-%d")),
        ("PAT-2026-0006", "Sneha Rahul Joshi", 41, "Female", "9822334455", "sneha.joshi@gmail.com", "Dastur Nagar, Amravati", "B+", "Rahul Joshi (Husband): 9822334450", (today - timedelta(days=30)).strftime("%Y-%m-%d")),
        ("PAT-2026-0007", "Kishor Bapurao Tayade", 68, "Male", "9370112233", "kishor.tayade@rediffmail.com", "Sai Nagar, Amravati", "A-", "Sachin Tayade (Son): 9370112234", (today - timedelta(days=20)).strftime("%Y-%m-%d")),
        ("PAT-2026-0008", "Neha Deepak Rathod", 24, "Female", "9970887766", "neha.rathod@gmail.com", "Rajapeth, Amravati", "AB-", "Deepak Rathod (Father): 9970887760", (today - timedelta(days=12)).strftime("%Y-%m-%d")),
        ("PAT-2026-0009", "Vikram Surendra Kale", 47, "Male", "9860223344", "vikram.kale@gmail.com", "Panchavati Square, Amravati", "O+", "Surendra Kale (Father): 9860223340", (today - timedelta(days=5)).strftime("%Y-%m-%d")),
        ("PAT-2026-0010", "Ananya Pravin Jadhav", 16, "Female", "9403445566", "pravin.jadhav@gmail.com", "Tapovan Gate, Amravati", "B+", "Pravin Jadhav (Father): 9403445566", today.strftime("%Y-%m-%d")),
    ]

    for p in patients_data:
        add_patient(*p)
        print(f"  + Patient added: {p[0]} - {p[1]} ({p[2]}y, {p[3]})")

    # 3. Create Medical Case Histories
    print("\n[3/4] Creating Medical Case Histories...")
    cases_data = [
        (
            "PAT-2026-0001",
            (today - timedelta(days=90)).strftime("%Y-%m-%d"),
            "Persistent headache and mild dizziness for 2 weeks",
            "BP 150/95 mmHg, headache in occipital region, occasional fatigue",
            "Known smoker for 10 years, no prior hospital admissions",
            "None reported",
            "Essential Hypertension (Stage 1)",
            "Tab Amlodipine 5mg OD morning, Low sodium diet, 30 min daily brisk walking",
            "Patient advised to monitor blood pressure weekly and avoid salty snacks.",
            "Dr. Sarang Thakare",
            (today - timedelta(days=60)).strftime("%Y-%m-%d"),
        ),
        (
            "PAT-2026-0001",
            (today - timedelta(days=60)).strftime("%Y-%m-%d"),
            "Follow-up for hypertension, feeling significantly better",
            "BP improved to 130/84 mmHg, headaches resolved, sleep pattern normal",
            "Hypertension stage 1 under medication",
            "None reported",
            "Controlled Essential Hypertension",
            "Continue Tab Amlodipine 5mg OD, maintain low sodium dietary regimen",
            "Blood pressure well within target range. Repeat lipid profile next visit.",
            "Dr. Sarang Thakare",
            (today + timedelta(days=30)).strftime("%Y-%m-%d"),
        ),
        (
            "PAT-2026-0002",
            (today - timedelta(days=75)).strftime("%Y-%m-%d"),
            "High fever, body chills, and dry cough for 3 days",
            "Temp 101.5 F, throat congestion, body aches, clear chest sounds",
            "Seasonal allergic rhinitis",
            "Penicillin (mild skin rash)",
            "Acute Viral Pharyngitis & Upper Respiratory Infection",
            "Tab Paracetamol 650mg TDS, Tab Azithromycin 500mg OD for 3 days, Steam inhalation",
            "Adequate hydration and complete bed rest prescribed.",
            "Dr. Pranav Dabharde",
            (today - timedelta(days=68)).strftime("%Y-%m-%d"),
        ),
        (
            "PAT-2026-0003",
            (today - timedelta(days=60)).strftime("%Y-%m-%d"),
            "Wheezing, shortness of breath, and night cough",
            "Bilateral wheezing on auscultation, respiratory rate 26/min, SpO2 96%",
            "Recurrent childhood cough episodes during seasonal transitions",
            "Dust mites, cold air exposure",
            "Mild Persistent Bronchial Asthma",
            "Levosalbutamol + Budesonide inhaler 2 puffs BD, Syrup Montelukast 5mg at bedtime",
            "Parent instructed on proper inhaler spacer technique. Avoid dust exposure.",
            "Dr. Pranav Dabharde",
            (today - timedelta(days=30)).strftime("%Y-%m-%d"),
        ),
        (
            "PAT-2026-0004",
            (today - timedelta(days=48)).strftime("%Y-%m-%d"),
            "Bilateral knee pain and stiffness, difficulty walking downstairs",
            "Crepitus felt on knee flexion, mild swelling, tenderness on joint line",
            "Post-menopausal status, 5 years sedentary lifestyle",
            "Sulfonamides",
            "Bilateral Osteoarthritis of Knees (Grade 2)",
            "Tab Glucosamine + Diacerein OD, Tab Etoricoxib 60mg SOS for pain, Physiotherapy exercises",
            "Quadriceps strengthening exercises recommended. Avoid sitting on the floor.",
            "Dr. Sarang Thakare",
            (today - timedelta(days=15)).strftime("%Y-%m-%d"),
        ),
        (
            "PAT-2026-0005",
            (today - timedelta(days=40)).strftime("%Y-%m-%d"),
            "Severe acidity, epigastric burning pain, and postprandial fullness",
            "Mild epigastric tenderness, negative for Murphy's sign, normal bowel sounds",
            "Irregular meal times, high intake of spicy fried street foods and tea",
            "None",
            "Gastroesophageal Reflux Disease (GERD) with Gastritis",
            "Cap Pantoprazole 40mg + Domperidone 30mg BD before meals, Gelusil syrup 10ml TDS",
            "Advised smaller, frequent meals. Strictly avoid late-night heavy meals and oily items.",
            "Dr. Pranav Dabharde",
            (today - timedelta(days=10)).strftime("%Y-%m-%d"),
        ),
        (
            "PAT-2026-0006",
            (today - timedelta(days=28)).strftime("%Y-%m-%d"),
            "Increased thirst, frequent urination at night, and unexplained fatigue",
            "Fasting blood sugar: 182 mg/dL, Post-prandial: 254 mg/dL, HbA1c 8.2%",
            "Family history of diabetes in mother",
            "None",
            "Type 2 Diabetes Mellitus",
            "Tab Metformin 500mg BD after meals, Diabetic diet plan, 40 min daily exercise",
            "Referred to hospital clinical nutritionist for strict carbohydrate counting.",
            "Dr. Sarang Thakare",
            (today + timedelta(days=14)).strftime("%Y-%m-%d"),
        ),
        (
            "PAT-2026-0007",
            (today - timedelta(days=18)).strftime("%Y-%m-%d"),
            "Chronic cough with morning expectoration and exertional breathlessness",
            "Rhonchi in lower lung fields, SpO2 93% on room air, barrel-shaped chest appearance",
            "Beedi smoker for 35 years (quit 2 years ago)",
            "None",
            "Chronic Obstructive Pulmonary Disease (COPD)",
            "Formoterol + Budesonide inhaler 400mcg BD, Tab Acebrophylline 100mg BD, Breathing exercises",
            "Chest physiotherapy demonstrated. Immediate reporting if sputum changes color.",
            "Dr. Sarang Thakare",
            (today + timedelta(days=7)).strftime("%Y-%m-%d"),
        ),
        (
            "PAT-2026-0008",
            (today - timedelta(days=10)).strftime("%Y-%m-%d"),
            "Throbbing unilateral headache with photophobia and nausea",
            "Pupillary reflexes normal, no focal neurological deficits, sensitivity to bright light",
            "History of exam-related stress headaches since college",
            "Aspirin",
            "Migraine without Aura",
            "Tab Naproxen 500mg + Domperidone 10mg at onset of attack, Tab Propranolol 20mg OD prophylaxis",
            "Advised headache diary maintenance to identify specific triggers.",
            "Dr. Pranav Dabharde",
            (today + timedelta(days=20)).strftime("%Y-%m-%d"),
        ),
        (
            "PAT-2026-0009",
            (today - timedelta(days=4)).strftime("%Y-%m-%d"),
            "Acute back pain after lifting a heavy luggage bag",
            "Paravertebral muscle spasm in lumbar region, straight leg raise test negative",
            "Occasional mild lower back ache",
            "None",
            "Acute Lumbar Muscle Strain",
            "Tab Thiocolchicoside + Aceclofenac BD for 5 days, Hot compression, Lumbar belt support",
            "Strict bed rest for 2 days followed by gentle stretching. Avoid heavy lifting.",
            "Dr. Sarang Thakare",
            (today + timedelta(days=6)).strftime("%Y-%m-%d"),
        ),
    ]

    for c in cases_data:
        add_medical_case(*c)
        print(f"  + Medical case recorded for {c[0]}: {c[6]}")

    # 4. Create Appointments
    print("\n[4/4] Scheduling Appointments (Past, Today, and Upcoming)...")
    appointments_data = [
        ("PAT-2026-0001", (today - timedelta(days=3)).strftime("%Y-%m-%d"), "10:30 AM", "Dr. Sarang Thakare", "Blood pressure checkup", "Completed"),
        ("PAT-2026-0002", (today - timedelta(days=2)).strftime("%Y-%m-%d"), "11:00 AM", "Dr. Pranav Dabharde", "Throat infection follow-up", "Completed"),
        ("PAT-2026-0005", (today - timedelta(days=1)).strftime("%Y-%m-%d"), "02:30 PM", "Dr. Pranav Dabharde", "Hyperacidity follow-up", "Cancelled"),
        # Today's appointments
        ("PAT-2026-0004", today.strftime("%Y-%m-%d"), "09:30 AM", "Dr. Sarang Thakare", "Knee joint pain evaluation", "Scheduled"),
        ("PAT-2026-0006", today.strftime("%Y-%m-%d"), "11:30 AM", "Dr. Sarang Thakare", "Diabetes fasting glucose review", "Scheduled"),
        ("PAT-2026-0010", today.strftime("%Y-%m-%d"), "03:00 PM", "Dr. Pranav Dabharde", "General health checkup and CBC report", "Scheduled"),
        # Upcoming appointments
        ("PAT-2026-0007", (today + timedelta(days=2)).strftime("%Y-%m-%d"), "10:00 AM", "Dr. Sarang Thakare", "COPD spirometry follow-up", "Scheduled"),
        ("PAT-2026-0008", (today + timedelta(days=3)).strftime("%Y-%m-%d"), "04:00 PM", "Dr. Pranav Dabharde", "Migraine prophylaxis review", "Scheduled"),
        ("PAT-2026-0009", (today + timedelta(days=5)).strftime("%Y-%m-%d"), "11:00 AM", "Dr. Sarang Thakare", "Lumbar strain rehabilitation review", "Scheduled"),
    ]

    for a in appointments_data:
        schedule_appointment(*a)
        print(f"  + Appointment: {a[0]} on {a[1]} at {a[2]} with {a[3]} [{a[5]}]")

    print("\n" + "=" * 60)
    print("Database initialization and seed completed successfully!")
    print("Hospital Staff Login Credentials:")
    print("  Username: admin      | Password: admin123")
    print("  Username: chhaya     | Password: chhaya123")
    print("  Username: dr_sarang  | Password: doctor123")
    print("  Username: dr_pranav  | Password: doctor123")
    print("=" * 60)

if __name__ == "__main__":
    seed()
