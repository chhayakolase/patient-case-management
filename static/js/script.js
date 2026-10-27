/**
 * script.js - Client-Side Interactivity
 * Smart Patient Case Management System
 * Student: Chhaya Kolase | G H Raisoni University, Amravati
 */

document.addEventListener("DOMContentLoaded", function () {
  // 1. Mobile Sidebar Toggle
  const toggleBtn = document.getElementById("sidebarToggleBtn");
  const sidebar = document.getElementById("sidebar");
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", function () {
      sidebar.classList.toggle("show");
    });
  }

  // 2. Alert Dismissal
  const alertCloseButtons = document.querySelectorAll(".alert-close");
  alertCloseButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      const alertBox = this.closest(".alert");
      if (alertBox) {
        alertBox.style.opacity = "0";
        setTimeout(function () {
          alertBox.remove();
        }, 250);
      }
    });
  });

  // Auto-dismiss success and info alerts after 6 seconds
  const autoAlerts = document.querySelectorAll(".alert-success, .alert-info");
  autoAlerts.forEach(function (alertBox) {
    setTimeout(function () {
      alertBox.style.transition = "opacity 0.4s ease";
      alertBox.style.opacity = "0";
      setTimeout(function () {
        alertBox.remove();
      }, 400);
    }, 6000);
  });

  // 3. Quick Table Client Filter (if search input exists with class .live-filter)
  const liveFilterInput = document.getElementById("liveTableSearch");
  if (liveFilterInput) {
    liveFilterInput.addEventListener("keyup", function () {
      const query = this.value.toLowerCase().trim();
      const targetTable = document.querySelector(".filterable-table tbody");
      if (targetTable) {
        const rows = targetTable.querySelectorAll("tr");
        rows.forEach(function (row) {
          const text = row.textContent.toLowerCase();
          row.style.display = text.includes(query) ? "" : "none";
        });
      }
    });
  }
});

// Confirmation helper for deleting patient
function confirmPatientDelete(patientId, patientName) {
  return confirm(
    `Are you sure you want to delete patient "${patientName}" (${patientId})?\n\nWarning: This will permanently remove all associated medical case records and appointments.`
  );
}

// Print trigger for clinical case sheets
function printCaseSheet() {
  window.print();
}

// Helper to fill demo credentials quickly on login page
function fillLogin(username, password) {
  const userInput = document.getElementById("username");
  const passInput = document.getElementById("password");
  if (userInput && passInput) {
    userInput.value = username;
    passInput.value = password;
  }
}
