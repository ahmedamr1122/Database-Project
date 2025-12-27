import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../../context/AuthContext';

const Checkout = () => {
  const [cartItems, setCartItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');
  const [creditCard, setCreditCard] = useState({
    number: '',
    expiry: '',
    cvv: ''
  });

  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      fetchCart();
    }
  }, [user]);

  const fetchCart = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/customer/cart', {
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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCreditCard(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateCreditCard = () => {
    const { number, expiry, cvv } = creditCard;

    // Basic validation
    if (!number || number.length < 13 || number.length > 19) {
      return 'Invalid credit card number';
    }

    if (!expiry || !/^\d{2}\/\d{2}$/.test(expiry)) {
      return 'Invalid expiry date (MM/YY)';
    }

    if (!cvv || cvv.length < 3 || cvv.length > 4) {
      return 'Invalid CVV';
    }

    // Check expiry date is in future
    const [month, year] = expiry.split('/');
    const expiryDate = new Date(2000 + parseInt(year), parseInt(month) - 1);
    const now = new Date();

    if (expiryDate <= now) {
      return 'Credit card has expired';
    }

    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationError = validateCreditCard();
    if (validationError) {
      setError(validationError);
      return;
    }

    if (cartItems.length === 0) {
      setError('Your cart is empty');
      return;
    }

    setProcessing(true);
    setError('');

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/customer/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          credit_card_no: creditCard.number.replace(/\s/g, ''),
          expiry_date: creditCard.expiry
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Clear cart and redirect to orders
        navigate('/customer/orders', {
          state: { message: 'Order placed successfully!' }
        });
      } else {
        setError(data.error || 'Failed to place order');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Checkout error:', error);
    } finally {
      setProcessing(false);
    }
  };

  if (!user) {
    return (
      <div className="text-center py-5">
        <h3>Please login to checkout</h3>
        <button onClick={() => navigate('/login')} className="btn btn-primary">Login</button>
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

  if (cartItems.length === 0) {
    return (
      <div className="text-center py-5">
        <h3>Your cart is empty</h3>
        <button onClick={() => navigate('/customer/search')} className="btn btn-primary">Browse Books</button>
      </div>
    );
  }

  return (
    <div>
      <h2 className="mb-4">
        <i className="fas fa-credit-card"></i> Checkout
      </h2>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      <div className="row">
        <div className="col-md-8">
          <div className="card mb-4">
            <div className="card-header">
              <h5>Order Summary</h5>
            </div>
            <div className="card-body">
              <div className="table-responsive">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Book</th>
                      <th>Author</th>
                      <th>Price</th>
                      <th>Quantity</th>
                      <th>Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    {cartItems.map((item) => (
                      <tr key={item.isbn}>
                        <td><strong>{item.title}</strong></td>
                        <td>{item.authors || 'Unknown'}</td>
                        <td>${item.selling_price.toFixed(2)}</td>
                        <td>{item.quantity}</td>
                        <td>${item.total_price.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <hr />
              <div className="d-flex justify-content-between">
                <strong>Total:</strong>
                <strong>${total.toFixed(2)}</strong>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card">
            <div className="card-header">
              <h5>Payment Information</h5>
            </div>
            <div className="card-body">
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="cardNumber" className="form-label">Credit Card Number</label>
                  <input
                    type="text"
                    className="form-control"
                    id="cardNumber"
                    name="number"
                    value={creditCard.number}
                    onChange={handleInputChange}
                    placeholder="1234 5678 9012 3456"
                    maxLength="19"
                    required
                  />
                </div>

                <div className="row">
                  <div className="col-6">
                    <div className="mb-3">
                      <label htmlFor="expiry" className="form-label">Expiry Date</label>
                      <input
                        type="text"
                        className="form-control"
                        id="expiry"
                        name="expiry"
                        value={creditCard.expiry}
                        onChange={handleInputChange}
                        placeholder="MM/YY"
                        maxLength="5"
                        required
                      />
                    </div>
                  </div>
                  <div className="col-6">
                    <div className="mb-3">
                      <label htmlFor="cvv" className="form-label">CVV</label>
                      <input
                        type="text"
                        className="form-control"
                        id="cvv"
                        name="cvv"
                        value={creditCard.cvv}
                        onChange={handleInputChange}
                        placeholder="123"
                        maxLength="4"
                        required
                      />
                    </div>
                  </div>
                </div>

                <button
                  type="submit"
                  className="btn btn-success w-100"
                  disabled={processing}
                >
                  {processing ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Processing...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-lock"></i> Place Order
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;
