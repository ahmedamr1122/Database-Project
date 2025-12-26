// ========================================
// Admin JavaScript Functions
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    initializeAdminFunctions();
});

// ========================================
// Initialize Admin Functions
// ========================================
function initializeAdminFunctions() {
    console.log('Admin functions initialized');
    
    // Add Book Form Validation
    const addBookForm = document.getElementById('addBookForm');
    if (addBookForm) {
        addBookForm.addEventListener('submit', validateAddBookForm);
    }
    
    // Modify Book Form Validation
    const modifyBookForm = document.getElementById('modifyBookForm');
    if (modifyBookForm) {
        modifyBookForm.addEventListener('submit', validateModifyBookForm);
    }
    
    // Initialize report date pickers
    initializeDatePickers();
}

// ========================================
// Book Management Functions
// ========================================

function validateAddBookForm(e) {
    const isbn = document.getElementById('isbn').value;
    const title = document.getElementById('title').value;
    const price = parseFloat(document.getElementById('selling_price').value);
    const stock = parseInt(document.getElementById('stock').value);
    const threshold = parseInt(document.getElementById('threshold').value);
    
    // ISBN validation (basic check)
    if (!isValidISBN(isbn)) {
        e.preventDefault();
        alert('Please enter a valid ISBN format (e.g., 978-0-13-468599-1)');
        return false;
    }
    
    // Price validation
    if (price <= 0) {
        e.preventDefault();
        alert('Price must be greater than 0');
        return false;
    }
    
    // Stock validation
    if (stock < 0) {
        e.preventDefault();
        alert('Stock cannot be negative');
        return false;
    }
    
    // Threshold validation
    if (threshold < 1) {
        e.preventDefault();
        alert('Threshold must be at least 1');
        return false;
    }
    
    return true;
}

function validateModifyBookForm(e) {
    const stock = parseInt(document.getElementById('stock').value);
    const threshold = parseInt(document.getElementById('threshold').value);
    
    if (stock < 0) {
        e.preventDefault();
        alert('Stock cannot be negative. This would violate the database constraint.');
        return false;
    }
    
    if (threshold < 1) {
        e.preventDefault();
        alert('Threshold must be at least 1');
        return false;
    }
    
    if (!confirm('Are you sure you want to update this book?')) {
        e.preventDefault();
        return false;
    }
    
    return true;
}

function isValidISBN(isbn) {
    // Basic ISBN format check (allows digits and hyphens)
    const isbnPattern = /^[\d-]{10,17}$/;
    return isbnPattern.test(isbn);
}

// ========================================
// Publisher Management
// ========================================

async function addPublisher() {
    const name = document.getElementById('publisher_name').value;
    const address = document.getElementById('publisher_address').value;
    const phone = document.getElementById('publisher_phone').value;
    
    if (!name || !address || !phone) {
        alert('Please fill in all publisher fields');
        return;
    }
    
    try {
        const response = await fetch('/admin/publishers/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                address: address,
                phone_number: phone
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Publisher added successfully!');
            
            // Add to dropdown
            const publisherSelect = document.getElementById('publisher_id');
            const option = document.createElement('option');
            option.value = data.publisher_id;
            option.text = name;
            publisherSelect.add(option);
            publisherSelect.value = data.publisher_id;
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('addPublisherModal'));
            modal.hide();
            
            // Clear form
            document.getElementById('addPublisherForm').reset();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error adding publisher:', error);
        alert('Error adding publisher. Please try again.');
    }
}

// ========================================
// Order Management
// ========================================

async function confirmOrder(orderId) {
    if (!confirm('Confirm receipt of this order? Stock will be automatically updated.')) {
        return;
    }
    
    const button = event.target.closest('button');
    showLoading(button);
    
    try {
        const response = await fetch(`/admin/orders/${orderId}/confirm`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Order confirmed successfully! Stock has been updated.');
            location.reload();
        } else {
            alert('Error: ' + data.message);
            hideLoading(button);
        }
    } catch (error) {
        console.error('Error confirming order:', error);
        alert('Error confirming order. Please try again.');
        hideLoading(button);
    }
}

// ========================================
// Report Functions
// ========================================

function initializeDatePickers() {
    const dateInput = document.getElementById('sale_date');
    if (dateInput) {
        // Set max date to today
        const today = new Date().toISOString().split('T')[0];
        dateInput.max = today;
    }
}

async function generateReport(reportType, params = {}) {
    const button = event.target.closest('button');
    showLoading(button);
    
    try {
        let url = `/admin/reports/${reportType}`;
        if (Object.keys(params).length > 0) {
            const queryString = new URLSearchParams(params).toString();
            url += `?${queryString}`;
        }
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayReportResults(reportType, data);
        } else {
            alert('Error generating report: ' + data.message);
        }
    } catch (error) {
        console.error('Error generating report:', error);
        alert('Error generating report. Please try again.');
    } finally {
        hideLoading(button);
    }
}

function displayReportResults(reportType, data) {
    // This function would display the report results
    // Implementation depends on report type
    console.log('Report Results:', data);
}

// ========================================
// Search Functions
// ========================================

function searchBooks(searchType) {
    const searchForm = document.getElementById('searchForm');
    if (!searchForm) return;
    
    const formData = new FormData(searchForm);
    let hasSearchCriteria = false;
    
    for (let [key, value] of formData.entries()) {
        if (value.trim() !== '') {
            hasSearchCriteria = true;
            break;
        }
    }
    
    if (!hasSearchCriteria) {
        alert('Please enter at least one search criterion');
        return false;
    }
    
    return true;
}

// ========================================
// Stock Management
// ========================================

function checkStockLevel(currentStock, threshold) {
    if (currentStock < threshold) {
        return {
            status: 'low',
            message: 'Stock below threshold - auto-reorder will trigger',
            class: 'danger'
        };
    } else if (currentStock < threshold * 1.5) {
        return {
            status: 'warning',
            message: 'Stock approaching threshold',
            class: 'warning'
        };
    } else {
        return {
            status: 'good',
            message: 'Stock level good',
            class: 'success'
        };
    }
}

function updateStockIndicator(isbn) {
    const stockInput = document.getElementById('stock');
    const thresholdInput = document.getElementById('threshold');
    
    if (!stockInput || !thresholdInput) return;
    
    const stock = parseInt(stockInput.value);
    const threshold = parseInt(thresholdInput.value);
    
    const status = checkStockLevel(stock, threshold);
    
    // Update UI to show stock status
    const indicator = document.createElement('div');
    indicator.className = `alert alert-${status.class} mt-2`;
    indicator.textContent = status.message;
    
    // Remove old indicator if exists
    const oldIndicator = document.querySelector('.stock-indicator');
    if (oldIndicator) {
        oldIndicator.remove();
    }
    
    indicator.classList.add('stock-indicator');
    stockInput.parentElement.appendChild(indicator);
}

// ========================================
// Export Functions
// ========================================

function exportReportToCSV(reportData, filename) {
    let csv = '';
    
    // Add headers
    if (reportData.length > 0) {
        csv += Object.keys(reportData[0]).join(',') + '\n';
    }
    
    // Add data
    reportData.forEach(row => {
        csv += Object.values(row).join(',') + '\n';
    });
    
    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename + '.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// ========================================
// Helper Functions
// ========================================

function showLoading(element) {
    const spinner = document.createElement('span');
    spinner.className = 'spinner-border spinner-border-sm me-2';
    spinner.setAttribute('role', 'status');
    element.prepend(spinner);
    element.disabled = true;
}

function hideLoading(element) {
    const spinner = element.querySelector('.spinner-border');
    if (spinner) {
        spinner.remove();
    }
    element.disabled = false;
}

// ========================================
// Make functions globally available
// ========================================
window.adminFunctions = {
    addPublisher,
    confirmOrder,
    generateReport,
    searchBooks,
    checkStockLevel,
    updateStockIndicator,
    exportReportToCSV
};