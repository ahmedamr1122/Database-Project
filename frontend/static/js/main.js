// ========================================
// Main JavaScript - Common Functions
// ========================================

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  initializeApp();
  updateCartCount();
  autoCloseAlerts();
});

// ========================================
// Initialize Application
// ========================================
function initializeApp() {
  console.log("Online Bookstore initialized");

  // Add fade-in animation to main content
  const mainContent = document.querySelector("main");
  if (mainContent) {
    mainContent.classList.add("fade-in");
  }

  // Initialize tooltips (if Bootstrap 5 is loaded)
  if (typeof bootstrap !== "undefined") {
    const tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
}

// ========================================
// Cart Functions
// ========================================
function updateCartCount() {
  fetch("/customer/cart/count")
    .then((response) => response.json())
    .then((data) => {
      const cartBadge = document.getElementById("cart-count");
      if (cartBadge) {
        cartBadge.textContent = data.count || 0;
        if (data.count > 0) {
          cartBadge.classList.remove("d-none");
          cartBadge.style.display = "inline"; // Ensure it takes up space
        } else {
          cartBadge.classList.add("d-none");
          cartBadge.style.display = "none";
        }
      }
    })
    .catch((error) => console.error("Error updating cart count:", error));
}

// ========================================
// Alert Functions
// ========================================
function autoCloseAlerts() {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    if (!alert.classList.contains("alert-permanent")) {
      setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      }, 5000);
    }
  });
}

function showAlert(message, type = "info") {
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
  alertDiv.role = "alert";
  alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  const container = document.querySelector(".container");
  if (container) {
    container.insertBefore(alertDiv, container.firstChild);

    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alertDiv);
      bsAlert.close();
    }, 5000);
  }
}

// ========================================
// Form Validation
// ========================================
function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return false;

  let isValid = true;
  const inputs = form.querySelectorAll(
    "input[required], select[required], textarea[required]"
  );

  inputs.forEach((input) => {
    if (!input.value.trim()) {
      input.classList.add("is-invalid");
      isValid = false;
    } else {
      input.classList.remove("is-invalid");
      input.classList.add("is-valid");
    }
  });

  return isValid;
}

// Clear validation states
function clearValidation(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  const inputs = form.querySelectorAll(".is-invalid, .is-valid");
  inputs.forEach((input) => {
    input.classList.remove("is-invalid", "is-valid");
  });
}

// ========================================
// Loading Functions
// ========================================
function showLoading(element) {
  const spinner = document.createElement("span");
  spinner.className = "spinner-border spinner-border-sm me-2";
  spinner.setAttribute("role", "status");
  spinner.setAttribute("aria-hidden", "true");
  element.prepend(spinner);
  element.disabled = true;
}

function hideLoading(element) {
  const spinner = element.querySelector(".spinner-border");
  if (spinner) {
    spinner.remove();
  }
  element.disabled = false;
}

// ========================================
// Confirmation Dialogs
// ========================================
function confirmAction(message, callback) {
  if (confirm(message)) {
    callback();
  }
}

// ========================================
// Format Functions
// ========================================
function formatCurrency(amount) {
  return "$" + parseFloat(amount).toFixed(2);
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

// ========================================
// Search Functions
// ========================================
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ========================================
// Local Storage Helper (for non-sensitive data)
// ========================================
function saveToLocalStorage(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {
    console.error("Error saving to localStorage:", e);
  }
}

function getFromLocalStorage(key) {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
  } catch (e) {
    console.error("Error reading from localStorage:", e);
    return null;
  }
}

// ========================================
// Scroll Functions
// ========================================
function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}

function scrollToElement(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }
}

// ========================================
// API Helper Functions
// ========================================
async function fetchAPI(url, options = {}) {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    showAlert("An error occurred. Please try again.", "danger");
    throw error;
  }
}

// ========================================
// Input Formatting
// ========================================

// Format phone number input
function formatPhoneNumber(input) {
  let phone = input.value.replace(/\D/g, "");
  if (phone.length > 10) {
    phone = phone.slice(0, 10);
  }
  input.value = phone;
}

// Format credit card number
function formatCreditCard(input) {
  let card = input.value.replace(/\D/g, "");
  if (card.length > 16) {
    card = card.slice(0, 16);
  }
  input.value = card;
}

// ========================================
// Copy to Clipboard
// ========================================
function copyToClipboard(text) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      showAlert("Copied to clipboard!", "success");
    })
    .catch((err) => {
      console.error("Failed to copy:", err);
      showAlert("Failed to copy to clipboard", "danger");
    });
}

// ========================================
// Print Function
// ========================================
function printPage() {
  window.print();
}

// ========================================
// Export for use in other files
// ========================================
window.bookstoreUtils = {
  updateCartCount,
  showAlert,
  validateForm,
  clearValidation,
  showLoading,
  hideLoading,
  confirmAction,
  formatCurrency,
  formatDate,
  debounce,
  scrollToTop,
  scrollToElement,
  fetchAPI,
  copyToClipboard,
  printPage,
};
