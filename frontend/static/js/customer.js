// ========================================
// Customer JavaScript Functions
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    initializeCustomerFunctions();
});

// ========================================
// Initialize Customer Functions
// ========================================
function initializeCustomerFunctions() {
    console.log('Customer functions initialized');
    
    // Initialize cart functions
    initializeCartFunctions();
    
    // Initialize search functions
    initializeSearchFunctions();
    
    // Initialize checkout validation
    initializeCheckoutValidation();
    
    // Update cart count on page load
    updateCartCount();
}

// ========================================
// Cart Functions
// ========================================

function initializeCartFunctions() {
    // Add to cart forms
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', handleAddToCart);
    });
    
    // Update cart quantity
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', validateQuantity);
    });
}

async function handleAddToCart(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const button = form.querySelector('button[type="submit"]');
    
    // Show loading
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Adding...';
    button.disabled = true;
    
    try {
        const response = await fetch('/customer/cart/add', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show success message
            showAlert('Book added to cart successfully!', 'success');
            
            // Update cart count
            updateCartCount();
            
            // Reset form
            form.reset();
        } else {
            showAlert(data.message || 'Error adding to cart', 'danger');
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showAlert('Error adding to cart. Please try again.', 'danger');
    } finally {
        // Restore button
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

function validateQuantity(e) {
    const input = e.target;
    const max = parseInt(input.max);
    const value = parseInt(input.value);
    
    if (value < 1) {
        input.value = 1;
        showAlert('Quantity must be at least 1', 'warning');
    } else if (value > max) {
        input.value = max;
        showAlert(`Only ${max} items available in stock`, 'warning');
    }
}

async function updateCartCount() {
    try {
        const response = await fetch('/customer/cart/count');
        const data = await response.json();
        
        const cartBadge = document.getElementById('cart-count');
        if (cartBadge) {
            cartBadge.textContent = data.count || 0;
            
            if (data.count > 0) {
                cartBadge.style.display = 'inline';
            } else {
                cartBadge.style.display = 'none';
            }
        }
    } catch (error) {
        console.error('Error updating cart count:', error);
    }
}

async function removeFromCart(isbn) {
    if (!confirm('Remove this item from your cart?')) {
        return;
    }
    
    try {
        const response = await fetch('/customer/cart/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ isbn: isbn })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Item removed from cart', 'success');
            location.reload();
        } else {
            showAlert(data.message || 'Error removing item', 'danger');
        }
    } catch (error) {
        console.error('Error removing from cart:', error);
        showAlert('Error removing item. Please try again.', 'danger');
    }
}

async function clearCart() {
    if (!confirm('Are you sure you want to clear your entire cart?')) {
        return;
    }
    
    try {
        const response = await fetch('/customer/cart/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Cart cleared successfully', 'success');
            location.reload();
        } else {
            showAlert(data.message || 'Error clearing cart', 'danger');
        }
    } catch (error) {
        console.error('Error clearing cart:', error);
        showAlert('Error clearing cart. Please try again.', 'danger');
    }
}

// ========================================
// Search Functions
// ========================================

function initializeSearchFunctions() {
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        // Add debounced search for title/author fields
        const searchInputs = searchForm.querySelectorAll('input[type="text"]');
        searchInputs.forEach(input => {
            input.addEventListener('input', debounce(function() {
                // Auto-search could be implemented here
            }, 500));
        });
    }
}

function resetSearchForm() {
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.reset();
        window.location.href = '/customer/search';
    }
}

// ========================================
// Checkout Functions
// ========================================

function initializeCheckoutValidation() {
    const checkoutForm = document.getElementById('checkoutForm');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', validateCheckoutForm);
        
        // Format credit card input
        const cardInput = document.getElementById('credit_card_no');
        if (cardInput) {
            cardInput.addEventListener('input', formatCreditCardInput);
        }
        
        // Format CVV input
        const cvvInput = document.getElementById('cvv');
        if (cvvInput) {
            cvvInput.addEventListener('input', formatCVVInput);
        }
    }
}

function validateCheckoutForm(e) {
    const cardNo = document.getElementById('credit_card_no').value;
    const expiryMonth = document.getElementById('expiry_month').value;
    const expiryYear = document.getElementById('expiry_year').value;
    const cvv = document.getElementById('cvv').value;
    const agreeTerms = document.getElementById('agree_terms').checked;
    
    // Card number validation
    if (cardNo.length !== 16 || !/^\d+$/.test(cardNo)) {
        e.preventDefault();
        showAlert('Please enter a valid 16-digit card number', 'danger');
        return false;
    }
    
    // Expiry validation
    if (!expiryMonth || !expiryYear) {
        e.preventDefault();
        showAlert('Please select card expiry date', 'danger');
        return false;
    }
    
    // Check if card is expired
    const today = new Date();
    const expiry = new Date(parseInt(expiryYear), parseInt(expiryMonth) - 1);
    
    if (expiry < today) {
        e.preventDefault();
        showAlert('Your card has expired. Please use a valid card.', 'danger');
        return false;
    }
    
    // CVV validation
    if (cvv.length !== 3 || !/^\d+$/.test(cvv)) {
        e.preventDefault();
        showAlert('Please enter a valid 3-digit CVV', 'danger');
        return false;
    }
    
    // Terms agreement
    if (!agreeTerms) {
        e.preventDefault();
        showAlert('Please agree to the terms and conditions', 'warning');
        return false;
    }
    
    // Final confirmation
    const total = document.querySelector('.alert-info strong').textContent;
    if (!confirm(`Confirm your order of ${total}?`)) {
        e.preventDefault();
        return false;
    }
    
    // Show loading on submit button
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
    submitBtn.disabled = true;
    
    return true;
}

function formatCreditCardInput(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 16) {
        value = value.slice(0, 16);
    }
    e.target.value = value;
}

function formatCVVInput(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 3) {
        value = value.slice(0, 3);
    }
    e.target.value = value;
}

// ========================================
// Profile Functions
// ========================================

function validateProfileForm(e) {
    const currentPassword = document.getElementById('current_password').value;
    const newPassword = document.getElementById('new_password').value;
    const confirmPassword = document.getElementById('confirm_new_password').value;
    
    // If trying to change password
    if (currentPassword || newPassword || confirmPassword) {
        if (!currentPassword) {
            e.preventDefault();
            showAlert('Please enter your current password', 'danger');
            return false;
        }
        
        if (newPassword !== confirmPassword) {
            e.preventDefault();
            showAlert('New passwords do not match', 'danger');
            return false;
        }
        
        if (newPassword.length < 6) {
            e.preventDefault();
            showAlert('Password must be at least 6 characters', 'danger');
            return false;
        }
    }
    
    return true;
}

// ========================================
// Order Functions
// ========================================

function viewOrderDetails(orderId) {
    window.location.href = `/customer/orders?order_id=${orderId}`;
}

function printOrder(orderId) {
    window.print();
}

// ========================================
// Utility Functions
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

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// ========================================
// Make functions globally available
// ========================================
window.customerFunctions = {
    handleAddToCart,
    removeFromCart,
    clearCart,
    validateCheckoutForm,
    validateProfileForm,
    viewOrderDetails,
    printOrder,
    updateCartCount
};