"""
analytics.py - Pandas and Matplotlib Data Analysis & Reporting
Smart Patient Case Management System
Student: Chhaya Kolase | G H Raisoni University, Amravati
"""

import io
import base64
import os
import matplotlib
matplotlib.use("Agg")  # Use non-GUI Agg backend for web server safety
import matplotlib.pyplot as plt
import pandas as pd
from database import get_db_connection

REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def get_patients_dataframe():
    """Load patients table into a Pandas DataFrame."""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()
    if not df.empty and "registered_at" in df.columns:
        df["registered_at"] = pd.to_datetime(df["registered_at"])
    return df


def get_medical_cases_dataframe():
    """Load medical cases joined with patient details into a Pandas DataFrame."""
    conn = get_db_connection()
    query = """
        SELECT c.*, p.name AS patient_name, p.age, p.gender, p.blood_group
        FROM medical_cases c
        JOIN patients p ON c.patient_id = p.patient_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    if not df.empty and "case_date" in df.columns:
        df["case_date"] = pd.to_datetime(df["case_date"])
    return df


def get_appointments_dataframe():
    """Load appointments joined with patient details into a Pandas DataFrame."""
    conn = get_db_connection()
    query = """
        SELECT a.*, p.name AS patient_name, p.phone
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    if not df.empty and "appointment_date" in df.columns:
        df["appointment_date"] = pd.to_datetime(df["appointment_date"])
    return df


def get_analytics_summary():
    """Compute summary statistics for dashboard and reports using Pandas."""
    patients_df = get_patients_dataframe()
    cases_df = get_medical_cases_dataframe()
    appts_df = get_appointments_dataframe()

    # Age groups categorization using Pandas cut
    age_groups_data = {}
    if not patients_df.empty:
        bins = [0, 12, 19, 39, 59, 120]
        labels = ["0-12 (Child)", "13-19 (Teen)", "20-39 (Young Adult)", "40-59 (Middle Age)", "60+ (Senior)"]
        patients_df["age_group"] = pd.cut(patients_df["age"], bins=bins, labels=labels, right=True)
        age_counts = patients_df["age_group"].value_counts().sort_index()
        age_groups_data = age_counts.to_dict()

    # Top Diagnoses
    diagnoses_data = {}
    if not cases_df.empty:
        diag_counts = cases_df["diagnosis"].value_counts().head(6)
        diagnoses_data = diag_counts.to_dict()

    # Monthly registrations
    monthly_data = {}
    if not patients_df.empty and "registered_at" in patients_df.columns:
        patients_df["year_month"] = patients_df["registered_at"].dt.strftime("%b %Y")
        monthly_counts = patients_df["year_month"].value_counts()
        monthly_data = monthly_counts.to_dict()

    # Gender distribution
    gender_data = {}
    if not patients_df.empty:
        gender_data = patients_df["gender"].value_counts().to_dict()

    # Appointment status
    appt_status_data = {}
    if not appts_df.empty:
        appt_status_data = appts_df["status"].value_counts().to_dict()

    return {
        "total_patients": len(patients_df),
        "total_cases": len(cases_df),
        "total_appointments": len(appts_df),
        "age_groups": age_groups_data,
        "diagnoses": diagnoses_data,
        "monthly": monthly_data,
        "gender": gender_data,
        "appointment_status": appt_status_data,
    }


def generate_chart_image(chart_type):
    """
    Generate professional Matplotlib charts and encode to Base64 string for direct HTML display.
    Styles use medical blue and clean card design aesthetics.
    """
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=110)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f8fbfd")

    # Primary hospital theme colors
    primary_blue = "#1e88e5"
    secondary_blue = "#0f4c81"
    teal_accent = "#00acc1"
    palette = ["#1e88e5", "#00acc1", "#43a047", "#fb8c00", "#e53935", "#8e24aa", "#3949ab"]

    if chart_type == "monthly_trend":
        patients_df = get_patients_dataframe()
        if not patients_df.empty:
            patients_df["month_label"] = patients_df["registered_at"].dt.strftime("%b %Y")
            counts = patients_df["month_label"].value_counts().sort_index()
            bars = ax.bar(counts.index, counts.values, color=primary_blue, edgecolor=secondary_blue, width=0.45, zorder=3)
            ax.set_title("Monthly Patient Registrations Trend", fontsize=12, fontweight="bold", pad=12, color="#1e293b")
            ax.set_ylabel("Number of Patients", fontsize=10, color="#475569")
            ax.set_xlabel("Registration Month", fontsize=10, color="#475569")
            ax.grid(axis="y", linestyle="--", alpha=0.6, zorder=0)
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f"{int(height)}",
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3), textcoords="offset points",
                            ha="center", va="bottom", fontsize=9, fontweight="bold", color="#0f4c81")
        else:
            ax.text(0.5, 0.5, "No Patient Data Available", ha="center", va="center", color="#94a3b8")

    elif chart_type == "age_distribution":
        patients_df = get_patients_dataframe()
        if not patients_df.empty:
            bins = [0, 12, 19, 39, 59, 120]
            labels = ["0-12 (Child)", "13-19 (Teen)", "20-39 (Young)", "40-59 (Mid-Age)", "60+ (Senior)"]
            patients_df["age_group"] = pd.cut(patients_df["age"], bins=bins, labels=labels, right=True)
            counts = patients_df["age_group"].value_counts().reindex(labels, fill_value=0)
            bars = ax.barh(counts.index, counts.values, color=teal_accent, edgecolor="#00838f", height=0.55, zorder=3)
            ax.set_title("Patient Age Group Distribution", fontsize=12, fontweight="bold", pad=12, color="#1e293b")
            ax.set_xlabel("Number of Registered Patients", fontsize=10, color="#475569")
            ax.grid(axis="x", linestyle="--", alpha=0.6, zorder=0)
            for bar in bars:
                width = bar.get_width()
                if width > 0:
                    ax.annotate(f"{int(width)}",
                                xy=(width, bar.get_y() + bar.get_height() / 2),
                                xytext=(4, 0), textcoords="offset points",
                                ha="left", va="center", fontsize=9, fontweight="bold", color="#006064")
        else:
            ax.text(0.5, 0.5, "No Patient Data Available", ha="center", va="center", color="#94a3b8")

    elif chart_type == "diagnosis_frequency":
        cases_df = get_medical_cases_dataframe()
        if not cases_df.empty:
            counts = cases_df["diagnosis"].value_counts().head(6)
            # Truncate long labels for visual cleanliness
            clean_labels = [label[:22] + "..." if len(label) > 22 else label for label in counts.index]
            bars = ax.bar(clean_labels, counts.values, color=palette[:len(counts)], width=0.5, zorder=3)
            ax.set_title("Cases Breakdown by Diagnosis (Top Clinical Conditions)", fontsize=12, fontweight="bold", pad=12, color="#1e293b")
            ax.set_ylabel("Number of Cases", fontsize=10, color="#475569")
            ax.set_xticks(range(len(clean_labels)))
            ax.set_xticklabels(clean_labels, rotation=20, ha="right", fontsize=8.5)
            ax.grid(axis="y", linestyle="--", alpha=0.6, zorder=0)
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f"{int(height)}",
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3), textcoords="offset points",
                            ha="center", va="bottom", fontsize=9, fontweight="bold")
        else:
            ax.text(0.5, 0.5, "No Medical Case Data Available", ha="center", va="center", color="#94a3b8")

    elif chart_type == "gender_pie":
        patients_df = get_patients_dataframe()
        if not patients_df.empty:
            counts = patients_df["gender"].value_counts()
            colors = ["#1e88e5", "#ec407a", "#ab47bc"][:len(counts)]
            wedges, texts, autotexts = ax.pie(
                counts.values,
                labels=counts.index,
                autopct="%1.1f%%",
                startangle=140,
                colors=colors,
                wedgeprops=dict(width=0.6, edgecolor="#ffffff", linewidth=2),
            )
            for t in autotexts:
                t.set_fontsize(9)
                t.set_fontweight("bold")
                t.set_color("#ffffff")
            ax.set_title("Patient Demographics by Gender", fontsize=12, fontweight="bold", pad=12, color="#1e293b")
        else:
            ax.text(0.5, 0.5, "No Gender Data Available", ha="center", va="center", color="#94a3b8")

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return image_base64


def export_dataframe_to_csv_string(report_type):
    """Generate CSV string using Pandas for downloadable reports."""
    if report_type == "patients":
        df = get_patients_dataframe()
        if not df.empty:
            # Reorganize and clean up column names for presentation
            rename_cols = {
                "patient_id": "Patient ID",
                "name": "Full Name",
                "age": "Age",
                "gender": "Gender",
                "phone": "Phone Number",
                "email": "Email Address",
                "blood_group": "Blood Group",
                "address": "Address",
                "emergency_contact": "Emergency Contact",
                "registered_at": "Registration Date",
            }
            existing = {k: v for k, v in rename_cols.items() if k in df.columns}
            export_df = df[list(existing.keys())].rename(columns=existing)
        else:
            export_df = pd.DataFrame(columns=["Patient ID", "Full Name", "Age", "Gender", "Phone Number", "Registration Date"])

    elif report_type == "medical_cases":
        df = get_medical_cases_dataframe()
        if not df.empty:
            rename_cols = {
                "id": "Case No",
                "patient_id": "Patient ID",
                "patient_name": "Patient Name",
                "case_date": "Case Date",
                "chief_complaint": "Chief Complaint",
                "diagnosis": "Diagnosis",
                "treatment": "Prescribed Treatment",
                "doctor_name": "Consulting Doctor",
                "follow_up_date": "Follow-up Date",
            }
            existing = {k: v for k, v in rename_cols.items() if k in df.columns}
            export_df = df[list(existing.keys())].rename(columns=existing)
        else:
            export_df = pd.DataFrame(columns=["Case No", "Patient ID", "Patient Name", "Case Date", "Diagnosis", "Consulting Doctor"])

    elif report_type == "appointments":
        df = get_appointments_dataframe()
        if not df.empty:
            rename_cols = {
                "id": "Appointment ID",
                "patient_id": "Patient ID",
                "patient_name": "Patient Name",
                "appointment_date": "Date",
                "appointment_time": "Time Slot",
                "doctor_name": "Doctor",
                "reason": "Reason for Visit",
                "status": "Status",
            }
            existing = {k: v for k, v in rename_cols.items() if k in df.columns}
            export_df = df[list(existing.keys())].rename(columns=existing)
        else:
            export_df = pd.DataFrame(columns=["Appointment ID", "Patient ID", "Patient Name", "Date", "Time Slot", "Doctor", "Status"])
    else:
        export_df = pd.DataFrame()

    return export_df.to_csv(index=False)
