import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../../context/AuthContext';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [updatingItems, setUpdatingItems] = useState({});

  const { user } = useContext(AuthContext);

  useEffect(() => {
    if (user) {
      fetchCart();
    }
  }, [user]);

  const fetchCart = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/customer/cart', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (response.ok) {
        setCartItems(data.items || []);
        setTotal(data.total || 0);
      } else {
        setError(data.error || 'Failed to load cart');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Cart fetch error:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateQuantity = async (isbn, newQuantity) => {
    if (newQuantity < 1) return;

    setUpdatingItems(prev => ({ ...prev, [isbn]: true }));

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/customer/cart/update', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ isbn, quantity: newQuantity })
      });

      const data = await response.json();

      if (response.ok) {
        await fetchCart(); // Refresh cart
      } else {
        setError(data.error || 'Failed to update quantity');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Update quantity error:', error);
    } finally {
      setUpdatingItems(prev => ({ ...prev, [isbn]: false }));
    }
  };

  const removeItem = async (isbn) => {
    if (!confirm('Remove this item from your cart?')) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/customer/cart/remove', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ isbn })
      });

      const data = await response.json();

      if (response.ok) {
        await fetchCart(); // Refresh cart
      } else {
        setError(data.error || 'Failed to remove item');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Remove item error:', error);
    }
  };

  const clearCart = async () => {
    if (!confirm('Are you sure you want to clear your entire cart?')) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/customer/cart/clear', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (response.ok) {
        setCartItems([]);
        setTotal(0);
      } else {
        setError(data.error || 'Failed to clear cart');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Clear cart error:', error);
    }
  };

  if (!user) {
    return (
      <div className="text-center py-5">
        <h3>Please login to view your cart</h3>
        <Link to="/login" className="btn btn-primary">Login</Link>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h2 className="mb-4">
        <i className="fas fa-shopping-cart"></i> Shopping Cart
      </h2>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {cartItems.length === 0 ? (
        <div className="text-center py-5">
          <i className="fas fa-shopping-cart fa-4x text-muted mb-3"></i>
          <h4>Your cart is empty</h4>
          <p className="text-muted">Add some books to get started!</p>
          <Link to="/customer/search" className="btn btn-primary">
            <i className="fas fa-search"></i> Browse Books
          </Link>
        </div>
      ) : (
        <>
          <div className="card mb-4">
            <div className="card-body">
              <div className="table-responsive">
                <table className="table table-striped">
                  <thead>
                    <tr>
                      <th>Book</th>
                      <th>Author</th>
                      <th>Price</th>
                      <th>Quantity</th>
                      <th>Total</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {cartItems.map((item) => (
                      <tr key={item.isbn}>
                        <td>
                          <strong>{item.title}</strong>
                        </td>
                        <td>{item.authors || 'Unknown'}</td>
                        <td>${item.selling_price.toFixed(2)}</td>
                        <td>
                          <div className="input-group" style={{ width: '120px' }}>
                            <button
                              className="btn btn-outline-secondary btn-sm"
                              type="button"
                              onClick={() => updateQuantity(item.isbn, item.quantity - 1)}
                              disabled={updatingItems[item.isbn]}
                            >
                              -
                            </button>
                            <input
                              type="number"
                              className="form-control text-center"
                              value={item.quantity}
                              onChange={(e) => updateQuantity(item.isbn, parseInt(e.target.value) || 1)}
                              min="1"
                              disabled={updatingItems[item.isbn]}
                            />
                            <button
                              className="btn btn-outline-secondary btn-sm"
                              type="button"
                              onClick={() => updateQuantity(item.isbn, item.quantity + 1)}
                              disabled={updatingItems[item.isbn]}
                            >
                              +
                            </button>
                          </div>
                        </td>
                        <td>${item.total_price.toFixed(2)}</td>
                        <td>
                          <button
                            className="btn btn-danger btn-sm"
                            onClick={() => removeItem(item.isbn)}
                          >
                            <i className="fas fa-trash"></i> Remove
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div className="row">
            <div className="col-md-6">
              <button
                className="btn btn-outline-danger"
                onClick={clearCart}
              >
                <i className="fas fa-trash"></i> Clear Cart
              </button>
            </div>
            <div className="col-md-6">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">Order Summary</h5>
                  <div className="d-flex justify-content-between mb-2">
                    <span>Subtotal:</span>
                    <span>${total.toFixed(2)}</span>
                  </div>
                  <div className="d-flex justify-content-between mb-2">
                    <span>Shipping:</span>
                    <span>$5.00</span>
                  </div>
                  <hr />
                  <div className="d-flex justify-content-between mb-3">
                    <strong>Total:</strong>
                    <strong>${(total + 5.00).toFixed(2)}</strong>
                  </div>
                  <Link to="/customer/checkout" className="btn btn-success w-100">
                    <i className="fas fa-credit-card"></i> Proceed to Checkout
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Cart;
