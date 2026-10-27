"""
test_app.py - Automated Test Suite
Smart Patient Case Management System
Student: Chhaya Kolase | G H Raisoni University, Amravati
"""

import unittest
import os
from datetime import datetime
from app import app
from database import (
    get_db_connection,
    init_db,
    verify_user,
    generate_patient_id,
    add_patient,
    get_patient_by_id,
    add_medical_case,
    get_cases_by_patient,
    schedule_appointment,
    check_appointment_conflict,
)
import analytics

class PatientCaseManagementTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment and test client."""
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_01_database_tables_exist(self):
        """Verify that SQLite tables are created properly."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row["name"] for row in cursor.fetchall()]
        conn.close()

        expected = ["users", "patients", "medical_cases", "appointments"]
        for tbl in expected:
            self.assertIn(tbl, tables, f"Expected table '{tbl}' was not found in database.")
        print("  [PASS] Test 1: Database schema and all tables verified.")

    def test_02_authentication(self):
        """Verify password hashing and user credential verification."""
        # Valid staff login
        user = verify_user("admin", "admin123")
        self.assertIsNotNone(user, "Valid user verification failed.")
        self.assertEqual(user["username"], "admin")

        # Invalid password
        invalid_user = verify_user("admin", "wrongpassword")
        self.assertIsNone(invalid_user, "Invalid password was incorrectly verified.")
        print("  [PASS] Test 2: Password hashing & credential verification verified.")

    def test_03_login_and_protected_routes(self):
        """Verify that unauthenticated access redirects to /login and authorized session works."""
        # Unauthenticated request to /dashboard should redirect
        response = self.client.get("/dashboard", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

        # Authenticate session
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["username"] = "admin"
            sess["full_name"] = "System Administrator"
            sess["role"] = "Admin"

        # Now dashboard should return HTTP 200
        dash_response = self.client.get("/dashboard")
        self.assertEqual(dash_response.status_code, 200)
        self.assertIn(b"Hospital Overview", dash_response.data)
        print("  [PASS] Test 3: Session authentication & route protection verified.")

    def test_04_patient_id_generation_and_crud(self):
        """Verify unique sequential patient ID generation and registration."""
        auto_id = generate_patient_id()
        self.assertTrue(auto_id.startswith(f"PAT-{datetime.now().year}-"))

        test_pid = f"PAT-TEST-{int(datetime.now().timestamp())}"
        add_patient(
            patient_id=test_pid,
            name="Test Patient Aarti",
            age=32,
            gender="Female",
            phone="9876543210",
            email="aarti.test@hospital.org",
            address="Camp Road, Amravati",
            blood_group="O+",
            emergency_contact="Father: 9876543211",
        )

        patient = get_patient_by_id(test_pid)
        self.assertIsNotNone(patient)
        self.assertEqual(patient["name"], "Test Patient Aarti")
        self.assertEqual(patient["age"], 32)
        print("  [PASS] Test 4: Patient ID generation & record storage verified.")

    def test_05_medical_case_history_preservation(self):
        """Verify adding multiple cases preserves history without overwriting."""
        test_pid = "PAT-2026-0001"
        initial_cases = get_cases_by_patient(test_pid)
        count_before = len(initial_cases)

        # Add a new follow-up case
        add_medical_case(
            patient_id=test_pid,
            case_date=datetime.now().strftime("%Y-%m-%d"),
            chief_complaint="Unit test follow-up visit for routine BP monitoring",
            symptoms="Normal vitals, BP 124/80 mmHg",
            medical_history="Hypertension",
            allergies="None",
            diagnosis="Routine Hypertension Checkup",
            treatment="Continue current dosage",
            doctor_notes="Patient compliant with regimen",
            doctor_name="Dr. Sarang Thakare",
        )

        updated_cases = get_cases_by_patient(test_pid)
        self.assertEqual(len(updated_cases), count_before + 1, "Case history was not appended properly.")
        print("  [PASS] Test 5: Medical case history multi-case preservation verified.")

    def test_06_appointment_conflict_prevention(self):
        """Verify that overlapping doctor bookings on the same date/time are detected."""
        test_date = "2026-11-15"
        test_time = "10:00 AM"
        test_doc = "Dr. Sarang Thakare"

        # Book an appointment
        schedule_appointment(
            patient_id="PAT-2026-0001",
            appointment_date=test_date,
            appointment_time=test_time,
            doctor_name=test_doc,
            reason="Cardio evaluation",
            status="Scheduled",
        )

        # Attempt to book another patient with the same doctor at the same slot
        conflict = check_appointment_conflict(test_doc, test_date, test_time)
        self.assertIsNotNone(conflict, "Conflict guard failed to detect overlapping booking.")
        print("  [PASS] Test 6: Doctor appointment scheduling conflict guard verified.")

    def test_07_analytics_and_pandas_dataframe(self):
        """Verify Pandas calculations and statistical aggregation."""
        summary = analytics.get_analytics_summary()
        self.assertIn("total_patients", summary)
        self.assertIn("age_groups", summary)
        self.assertIn("diagnoses", summary)
        self.assertGreaterEqual(summary["total_patients"], 10)
        print("  [PASS] Test 7: Pandas DataFrame summary analytics verified.")

    def test_08_matplotlib_charts_generation(self):
        """Verify that Matplotlib charts render clean Base64 images."""
        chart_types = ["monthly_trend", "age_distribution", "diagnosis_frequency", "gender_pie"]
        for ctype in chart_types:
            img_b64 = analytics.generate_chart_image(ctype)
            self.assertTrue(len(img_b64) > 1000, f"Chart image generation failed for {ctype}")
        print("  [PASS] Test 8: Matplotlib 4-chart rendering verified.")

    def test_09_csv_export_generation(self):
        """Verify that Pandas exports valid CSV string data."""
        for rtype in ["patients", "medical_cases", "appointments"]:
            csv_str = analytics.export_dataframe_to_csv_string(rtype)
            self.assertTrue(len(csv_str) > 0, f"CSV export failed for {rtype}")
            self.assertIn(",", csv_str, f"CSV delimiters missing in {rtype}")
        print("  [PASS] Test 9: Pandas CSV export pipeline verified.")

if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING AUTOMATED TEST SUITE: SMART PATIENT CASE MANAGEMENT")
    print("=" * 60)
    unittest.main()
