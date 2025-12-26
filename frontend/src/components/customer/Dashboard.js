import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../../context/AuthContext';

const CustomerDashboard = () => {
  const [cartCount, setCartCount] = useState(0);
  const [recentOrders, setRecentOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const { user } = useContext(AuthContext);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');

      // Fetch cart count
      const cartResponse = await fetch('http://localhost:5000/customer/cart/count', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (cartResponse.ok) {
        const cartData = await cartResponse.json();
        setCartCount(cartData.count || 0);
      }

      // Fetch recent orders
      const ordersResponse = await fetch('http://localhost:5000/customer/orders/recent', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (ordersResponse.ok) {
        const ordersData = await ordersResponse.json();
        setRecentOrders(ordersData.slice(0, 3)); // Show only 3 recent orders
      }

    } catch (error) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', error);
    } finally {
      setLoading(false);
    }
  };

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
      <div className="row mb-4">
        <div className="col-12">
          <div className="card bg-primary text-white">
            <div className="card-body">
              <h4 className="card-title">
                Welcome back, {user?.first_name}!
              </h4>
              <p className="card-text">
                Ready to discover your next favorite book?
              </p>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {/* Quick Actions */}
      <div className="row mb-4">
        <div className="col-md-3 mb-3">
          <Link to="/customer/search" className="text-decoration-none">
            <div className="card h-100 text-center">
              <div className="card-body">
                <i className="fas fa-search fa-3x text-primary mb-3"></i>
                <h5 className="card-title">Search Books</h5>
                <p className="card-text">Browse our extensive collection</p>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-3 mb-3">
          <Link to="/customer/cart" className="text-decoration-none">
            <div className="card h-100 text-center">
              <div className="card-body">
                <i className="fas fa-shopping-cart fa-3x text-success mb-3"></i>
                <h5 className="card-title">Shopping Cart</h5>
                <p className="card-text">
                  {cartCount > 0 ? `${cartCount} items in cart` : 'Your cart is empty'}
                </p>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-3 mb-3">
          <Link to="/customer/orders" className="text-decoration-none">
            <div className="card h-100 text-center">
              <div className="card-body">
                <i className="fas fa-receipt fa-3x text-warning mb-3"></i>
                <h5 className="card-title">My Orders</h5>
                <p className="card-text">View your order history</p>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-3 mb-3">
          <Link to="/customer/profile" className="text-decoration-none">
            <div className="card h-100 text-center">
              <div className="card-body">
                <i className="fas fa-user fa-3x text-info mb-3"></i>
                <h5 className="card-title">My Profile</h5>
                <p className="card-text">Manage your account</p>
              </div>
            </div>
          </Link>
        </div>
      </div>

      {/* Recent Orders */}
      {recentOrders.length > 0 && (
        <div className="row">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h5 className="mb-0">
                  <i className="fas fa-clock"></i> Recent Orders
                </h5>
              </div>
              <div className="card-body">
                <div className="list-group list-group-flush">
                  {recentOrders.map((order) => (
                    <div key={order.order_id} className="list-group-item">
                      <div className="d-flex justify-content-between align-items-center">
                        <div>
                          <h6 className="mb-1">Order #{order.order_id}</h6>
                          <small className="text-muted">
                            {new Date(order.order_date).toLocaleDateString()}
                          </small>
                        </div>
                        <div className="text-end">
                          <div className="fw-bold">${order.total_price.toFixed(2)}</div>
                          <Link to="/customer/orders" className="btn btn-sm btn-outline-primary">
                            View Details
                          </Link>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-3">
                  <Link to="/customer/orders" className="btn btn-primary">
                    View All Orders
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CustomerDashboard;
