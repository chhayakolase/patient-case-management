"""
app.py - Main Flask Web Application
Smart Patient Case Management System
Student: Chhaya Kolase | G H Raisoni University, Amravati
Guide: Sarang Thakare | In-charge: Pranav Dabharde
"""

import os
from functools import wraps
from datetime import datetime, date
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    Response,
    abort,
)

from database import (
    init_db,
    get_db_connection,
    verify_user,
    get_user_by_id,
    generate_patient_id,
    add_patient,
    get_all_patients,
    get_patient_by_id,
    update_patient,
    delete_patient,
    count_patients,
    get_recent_patients,
    add_medical_case,
    get_cases_by_patient,
    get_case_by_id,
    get_all_cases,
    update_medical_case,
    count_cases,
    schedule_appointment,
    check_appointment_conflict,
    get_all_appointments,
    get_today_appointments,
    get_patient_appointments,
    update_appointment_status,
    count_today_appointments,
    get_available_doctors,
)
import analytics

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "smart_patient_case_management_secret_key_2026")


# ==========================================
# AUTHENTICATION & ACCESS CONTROL
# ==========================================

def login_required(f):
    """Decorator to protect routes from unauthorized access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access the Smart Patient Case Management System.", "warning")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.context_processor
def inject_global_data():
    """Inject common project metadata and active session user into all templates."""
    current_user = None
    if "user_id" in session:
        current_user = get_user_by_id(session["user_id"])
    
    return {
        "current_user": current_user,
        "current_year": datetime.now().year,
        "today_str": datetime.now().strftime("%Y-%m-%d"),
        "project_info": {
            "title": "Smart Patient Case Management System",
            "student_name": "Chhaya Kolase",
            "course": "BCA (Bachelor of Computer Applications)",
            "university": "G H Raisoni University, Amravati",
            "semester": "Semester V",
            "session": "2026–27",
            "guide": "Sarang Thakare",
            "incharge": "Pranav Dabharde",
        }
    }


# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():
    """Hospital staff login page."""
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter both username and password.", "danger")
            return render_template("login.html")

        user = verify_user(username, password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["full_name"] = user["full_name"]
            session["role"] = user["role"]
            flash(f"Welcome back, {user['full_name']}! You have successfully signed in.", "success")
            
            next_url = request.args.get("next")
            return redirect(next_url if next_url else url_for("dashboard"))
        else:
            flash("Invalid staff credentials. Please check your username and password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Logout current user and clear session."""
    staff_name = session.get("full_name", "Staff")
    session.clear()
    flash(f"You have been safely logged out, {staff_name}.", "info")
    return redirect(url_for("login"))


# ==========================================
# DASHBOARD ROUTE
# ==========================================

@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    """Main Hospital Case Management Dashboard."""
    total_patients = count_patients()
    total_cases = count_cases()
    today_appts_count = count_today_appointments()
    today_appts = get_today_appointments()
    recent_patients = get_recent_patients(limit=5)
    
    # Analytics summary for quick cards
    summary = analytics.get_analytics_summary()

    return render_template(
        "dashboard.html",
        total_patients=total_patients,
        total_cases=total_cases,
        today_appts_count=today_appts_count,
        today_appts=today_appts,
        recent_patients=recent_patients,
        analytics_summary=summary,
    )


# ==========================================
# PATIENT REGISTRATION & MANAGEMENT
# ==========================================

@app.route("/patients")
@login_required
def patients():
    """View all registered patients with search filtering."""
    query = request.args.get("q", "").strip()
    patient_list = get_all_patients(search_query=query if query else None)
    return render_template("patients.html", patients=patient_list, search_query=query)


@app.route("/patients/add", methods=["GET", "POST"])
@login_required
def add_patient_view():
    """Register a new patient with auto-generated patient ID."""
    if request.method == "POST":
        patient_id = request.form.get("patient_id", "").strip()
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        blood_group = request.form.get("blood_group", "").strip()
        emergency_contact = request.form.get("emergency_contact", "").strip()
        registered_at = request.form.get("registered_at", "").strip()

        # Input Validation
        if not name or not age or not gender or not phone:
            flash("Full Name, Age, Gender, and Phone Number are required fields.", "danger")
            return render_template("add_patient.html", auto_id=patient_id, form_data=request.form)

        try:
            age_int = int(age)
            if age_int < 0 or age_int > 130:
                flash("Please enter a valid age between 0 and 130.", "danger")
                return render_template("add_patient.html", auto_id=patient_id, form_data=request.form)
        except ValueError:
            flash("Age must be a valid integer number.", "danger")
            return render_template("add_patient.html", auto_id=patient_id, form_data=request.form)

        if len(phone) < 7:
            flash("Please enter a valid phone number.", "danger")
            return render_template("add_patient.html", auto_id=patient_id, form_data=request.form)

        if not patient_id:
            patient_id = generate_patient_id()

        try:
            add_patient(
                patient_id=patient_id,
                name=name,
                age=age_int,
                gender=gender,
                phone=phone,
                email=email,
                address=address,
                blood_group=blood_group,
                emergency_contact=emergency_contact,
                registered_at=registered_at if registered_at else None,
            )
            flash(f"Patient {name} registered successfully with ID: {patient_id}!", "success")
            return redirect(url_for("patient_details", patient_id=patient_id))
        except Exception as e:
            flash(f"Could not register patient: {str(e)}", "danger")
            return render_template("add_patient.html", auto_id=patient_id, form_data=request.form)

    auto_id = generate_patient_id()
    return render_template("add_patient.html", auto_id=auto_id, form_data={}, today_str=datetime.now().strftime("%Y-%m-%d"))


@app.route("/patients/<patient_id>")
@login_required
def patient_details(patient_id):
    """View complete patient profile, chronological case history, and appointments."""
    patient = get_patient_by_id(patient_id)
    if not patient:
        flash(f"Patient with ID '{patient_id}' not found.", "danger")
        return redirect(url_for("patients"))

    cases = get_cases_by_patient(patient["patient_id"])
    appointments = get_patient_appointments(patient["patient_id"])
    doctors = get_available_doctors()

    return render_template(
        "patient_details.html",
        patient=patient,
        cases=cases,
        appointments=appointments,
        doctors=doctors,
    )


@app.route("/patients/<patient_id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient_view(patient_id):
    """Edit demographic details of an existing patient."""
    patient = get_patient_by_id(patient_id)
    if not patient:
        flash(f"Patient with ID '{patient_id}' not found.", "danger")
        return redirect(url_for("patients"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        blood_group = request.form.get("blood_group", "").strip()
        emergency_contact = request.form.get("emergency_contact", "").strip()

        if not name or not age or not gender or not phone:
            flash("Full Name, Age, Gender, and Phone Number are required fields.", "danger")
            return render_template("edit_patient.html", patient=patient)

        try:
            age_int = int(age)
            if age_int < 0 or age_int > 130:
                flash("Please enter a valid age between 0 and 130.", "danger")
                return render_template("edit_patient.html", patient=patient)
        except ValueError:
            flash("Age must be a valid number.", "danger")
            return render_template("edit_patient.html", patient=patient)

        try:
            update_patient(
                patient_id=patient["patient_id"],
                name=name,
                age=age_int,
                gender=gender,
                phone=phone,
                email=email,
                address=address,
                blood_group=blood_group,
                emergency_contact=emergency_contact,
            )
            flash(f"Patient record for {name} ({patient['patient_id']}) updated successfully.", "success")
            return redirect(url_for("patient_details", patient_id=patient["patient_id"]))
        except Exception as e:
            flash(f"Update failed: {str(e)}", "danger")

    return render_template("edit_patient.html", patient=patient)


@app.route("/patients/<patient_id>/delete", methods=["POST"])
@login_required
def delete_patient_action(patient_id):
    """Delete a patient record and cascade associated cases/appointments."""
    patient = get_patient_by_id(patient_id)
    if patient:
        p_name = patient["name"]
        delete_patient(patient_id)
        flash(f"Patient record for {p_name} ({patient_id}) and related histories deleted.", "info")
    else:
        flash("Patient not found.", "danger")
    return redirect(url_for("patients"))


# ==========================================
# MEDICAL CASES MANAGEMENT
# ==========================================

@app.route("/cases")
@login_required
def medical_cases():
    """List medical cases with search and filtering by diagnosis/date."""
    search_q = request.args.get("q", "").strip()
    diagnosis_filter = request.args.get("diagnosis", "").strip()
    date_from = request.args.get("date_from", "").strip()
    date_to = request.args.get("date_to", "").strip()

    cases_list = get_all_cases(
        search_query=search_q if search_q else None,
        diagnosis_filter=diagnosis_filter if diagnosis_filter else None,
        date_from=date_from if date_from else None,
        date_to=date_to if date_to else None,
    )

    return render_template(
        "medical_cases.html",
        cases=cases_list,
        search_q=search_q,
        diagnosis_filter=diagnosis_filter,
        date_from=date_from,
        date_to=date_to,
    )


@app.route("/cases/add", methods=["GET", "POST"])
@login_required
def add_case_view():
    """Record a new medical case for a patient."""
    selected_pid = request.args.get("patient_id", "").strip()
    patients_list = get_all_patients()
    doctors = get_available_doctors()

    if request.method == "POST":
        patient_id = request.form.get("patient_id", "").strip()
        case_date = request.form.get("case_date", "").strip()
        chief_complaint = request.form.get("chief_complaint", "").strip()
        symptoms = request.form.get("symptoms", "").strip()
        medical_history = request.form.get("medical_history", "").strip()
        allergies = request.form.get("allergies", "").strip()
        diagnosis = request.form.get("diagnosis", "").strip()
        treatment = request.form.get("treatment", "").strip()
        doctor_notes = request.form.get("doctor_notes", "").strip()
        doctor_name = request.form.get("doctor_name", "").strip()
        follow_up_date = request.form.get("follow_up_date", "").strip()

        if not patient_id or not case_date or not chief_complaint or not symptoms or not diagnosis or not treatment or not doctor_name:
            flash("Patient, Case Date, Chief Complaint, Symptoms, Diagnosis, Treatment, and Doctor are required.", "danger")
            return render_template(
                "add_case.html",
                patients=patients_list,
                doctors=doctors,
                selected_pid=patient_id,
                form_data=request.form,
            )

        try:
            case_id = add_medical_case(
                patient_id=patient_id,
                case_date=case_date,
                chief_complaint=chief_complaint,
                symptoms=symptoms,
                medical_history=medical_history,
                allergies=allergies,
                diagnosis=diagnosis,
                treatment=treatment,
                doctor_notes=doctor_notes,
                doctor_name=doctor_name,
                follow_up_date=follow_up_date if follow_up_date else None,
            )
            flash(f"Medical case #{case_id} recorded successfully for patient {patient_id}!", "success")
            return redirect(url_for("case_details", case_id=case_id))
        except Exception as e:
            flash(f"Failed to record medical case: {str(e)}", "danger")
            return render_template(
                "add_case.html",
                patients=patients_list,
                doctors=doctors,
                selected_pid=patient_id,
                form_data=request.form,
            )

    return render_template(
        "add_case.html",
        patients=patients_list,
        doctors=doctors,
        selected_pid=selected_pid,
        form_data={},
        today_str=datetime.now().strftime("%Y-%m-%d"),
    )


@app.route("/cases/<int:case_id>")
@login_required
def case_details(case_id):
    """View full medical case record and clinical notes (printable)."""
    case = get_case_by_id(case_id)
    if not case:
        flash(f"Medical case record #{case_id} not found.", "danger")
        return redirect(url_for("medical_cases"))

    return render_template("case_details.html", case=case)


@app.route("/cases/<int:case_id>/edit", methods=["GET", "POST"])
@login_required
def edit_case_view(case_id):
    """Update clinical findings and treatment notes of an existing case."""
    case = get_case_by_id(case_id)
    if not case:
        flash(f"Medical case record #{case_id} not found.", "danger")
        return redirect(url_for("medical_cases"))

    doctors = get_available_doctors()

    if request.method == "POST":
        case_date = request.form.get("case_date", "").strip()
        chief_complaint = request.form.get("chief_complaint", "").strip()
        symptoms = request.form.get("symptoms", "").strip()
        medical_history = request.form.get("medical_history", "").strip()
        allergies = request.form.get("allergies", "").strip()
        diagnosis = request.form.get("diagnosis", "").strip()
        treatment = request.form.get("treatment", "").strip()
        doctor_notes = request.form.get("doctor_notes", "").strip()
        doctor_name = request.form.get("doctor_name", "").strip()
        follow_up_date = request.form.get("follow_up_date", "").strip()

        if not case_date or not chief_complaint or not symptoms or not diagnosis or not treatment or not doctor_name:
            flash("All clinical mandatory fields must be completed.", "danger")
            return render_template("edit_case.html", case=case, doctors=doctors)

        try:
            update_medical_case(
                case_id=case_id,
                case_date=case_date,
                chief_complaint=chief_complaint,
                symptoms=symptoms,
                medical_history=medical_history,
                allergies=allergies,
                diagnosis=diagnosis,
                treatment=treatment,
                doctor_notes=doctor_notes,
                doctor_name=doctor_name,
                follow_up_date=follow_up_date if follow_up_date else None,
            )
            flash(f"Medical case #{case_id} updated successfully.", "success")
            return redirect(url_for("case_details", case_id=case_id))
        except Exception as e:
            flash(f"Failed to update case: {str(e)}", "danger")

    return render_template("edit_case.html", case=case, doctors=doctors)


# ==========================================
# APPOINTMENT MANAGEMENT
# ==========================================

@app.route("/appointments")
@login_required
def appointments():
    """List appointments, check upcoming visits, and schedule new ones."""
    status_filter = request.args.get("status", "All").strip()
    date_filter = request.args.get("date", "").strip()

    appts_list = get_all_appointments(
        filter_status=status_filter if status_filter else None,
        filter_date=date_filter if date_filter else None,
    )
    patients_list = get_all_patients()
    doctors = get_available_doctors()

    return render_template(
        "appointments.html",
        appointments=appts_list,
        patients=patients_list,
        doctors=doctors,
        status_filter=status_filter,
        date_filter=date_filter,
        today_str=datetime.now().strftime("%Y-%m-%d"),
    )


@app.route("/appointments/schedule", methods=["POST"])
@login_required
def schedule_appointment_action():
    """Schedule a patient appointment with conflict prevention."""
    patient_id = request.form.get("patient_id", "").strip()
    appointment_date = request.form.get("appointment_date", "").strip()
    appointment_time = request.form.get("appointment_time", "").strip()
    doctor_name = request.form.get("doctor_name", "").strip()
    reason = request.form.get("reason", "").strip()

    if not patient_id or not appointment_date or not appointment_time or not doctor_name or not reason:
        flash("All appointment scheduling fields are required.", "danger")
        return redirect(url_for("appointments"))

    # Conflict Check: Check if doctor is already booked at that date and time slot
    conflict = check_appointment_conflict(doctor_name, appointment_date, appointment_time)
    if conflict:
        flash(
            f"Scheduling Conflict: {doctor_name} already has a scheduled appointment on {appointment_date} at {appointment_time} with {conflict['patient_name']} ({conflict['patient_id']}). Please select another time slot or physician.",
            "danger",
        )
        return redirect(url_for("appointments"))

    try:
        schedule_appointment(
            patient_id=patient_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            doctor_name=doctor_name,
            reason=reason,
            status="Scheduled",
        )
        flash(f"Appointment scheduled successfully for patient {patient_id} with {doctor_name} on {appointment_date} at {appointment_time}.", "success")
    except Exception as e:
        flash(f"Error scheduling appointment: {str(e)}", "danger")

    return redirect(url_for("appointments"))


@app.route("/appointments/<int:appt_id>/status", methods=["POST"])
@login_required
def update_appointment_status_action(appt_id):
    """Update status of an appointment (e.g. Completed or Cancelled)."""
    new_status = request.form.get("status", "").strip()
    if new_status in ["Scheduled", "Completed", "Cancelled"]:
        update_appointment_status(appt_id, new_status)
        flash(f"Appointment #{appt_id} marked as '{new_status}'.", "success")
    else:
        flash("Invalid status selected.", "danger")
    return redirect(url_for("appointments"))


# ==========================================
# REPORTS & DATA ANALYSIS (PANDAS & MATPLOTLIB)
# ==========================================

@app.route("/reports")
@login_required
def reports():
    """Data Analysis and Reports dashboard with embedded Matplotlib visualizations."""
    summary = analytics.get_analytics_summary()

    # Generate charts as base64 images
    monthly_chart = analytics.generate_chart_image("monthly_trend")
    age_chart = analytics.generate_chart_image("age_distribution")
    diag_chart = analytics.generate_chart_image("diagnosis_frequency")
    gender_chart = analytics.generate_chart_image("gender_pie")

    return render_template(
        "reports.html",
        summary=summary,
        monthly_chart=monthly_chart,
        age_chart=age_chart,
        diag_chart=diag_chart,
        gender_chart=gender_chart,
    )


@app.route("/reports/export/<report_type>")
@login_required
def export_csv(report_type):
    """Export dataset to downloadable CSV using Pandas."""
    valid_reports = ["patients", "medical_cases", "appointments"]
    if report_type not in valid_reports:
        flash("Invalid export report type requested.", "danger")
        return redirect(url_for("reports"))

    csv_data = analytics.export_dataframe_to_csv_string(report_type)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{report_type}_report_{timestamp}.csv"

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# ==========================================
# ABOUT & PROJECT METADATA
# ==========================================

@app.route("/about")
@login_required
def about():
    """Academic Final Year Project Details & Educational Notice."""
    return render_template("project_info.html")


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template("base.html", error_title="404 - Page Not Found", error_message="The requested hospital management page could not be located."), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("base.html", error_title="500 - Internal Server Error", error_message="An unexpected system error occurred. Please contact the administrator."), 500


# Auto-initialize database on application startup (essential for cloud deployments like Render)
try:
    init_db()
    conn = get_db_connection()
    user_cnt = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    if user_cnt == 0:
        import seed_data
        seed_data.seed()
except Exception as _e:
    print(f"Startup DB check: {_e}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Smart Patient Case Management System on port {port} ...")
    app.run(debug=True, host="0.0.0.0", port=port)
