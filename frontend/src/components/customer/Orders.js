import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../../context/AuthContext';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedOrder, setSelectedOrder] = useState(null);

  const { user } = useContext(AuthContext);

  useEffect(() => {
    if (user) {
      fetchOrders();
    }
  }, [user]);

  const fetchOrders = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/customer/orders', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (response.ok) {
        setOrders(data.orders || []);
      } else {
        setError(data.error || 'Failed to load orders');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Orders fetch error:', error);
    } finally {
      setLoading(false);
    }
  };

  const viewOrderDetails = (order) => {
    setSelectedOrder(order);
  };

  const closeOrderDetails = () => {
    setSelectedOrder(null);
  };

  if (!user) {
    return (
      <div className="text-center py-5">
        <h3>Please login to view your orders</h3>
        <a href="/login" className="btn btn-primary">Login</a>
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
        <i className="fas fa-receipt"></i> My Orders
      </h2>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {orders.length === 0 ? (
        <div className="text-center py-5">
          <i className="fas fa-receipt fa-4x text-muted mb-3"></i>
          <h4>No orders yet</h4>
          <p className="text-muted">Your order history will appear here</p>
          <a href="/customer/search" className="btn btn-primary">
            <i className="fas fa-search"></i> Start Shopping
          </a>
        </div>
      ) : (
        <>
          <div className="card">
            <div className="card-body">
              <div className="table-responsive">
                <table className="table table-striped">
                  <thead>
                    <tr>
                      <th>Order ID</th>
                      <th>Date</th>
                      <th>Total</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orders.map((order) => (
                      <tr key={order.order_id}>
                        <td>#{order.order_id}</td>
                        <td>{new Date(order.order_date).toLocaleDateString()}</td>
                        <td>${order.total_price.toFixed(2)}</td>
                        <td>
                          <span className="badge bg-success">Completed</span>
                        </td>
                        <td>
                          <button
                            className="btn btn-sm btn-outline-primary"
                            onClick={() => viewOrderDetails(order)}
                          >
                            <i className="fas fa-eye"></i> View Details
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Order Details Modal */}
          {selectedOrder && (
            <div className="modal show d-block" tabIndex="-1">
              <div className="modal-dialog modal-lg">
                <div className="modal-content">
                  <div className="modal-header">
                    <h5 className="modal-title">Order #{selectedOrder.order_id}</h5>
                    <button
                      type="button"
                      className="btn-close"
                      onClick={closeOrderDetails}
                    ></button>
                  </div>
                  <div className="modal-body">
                    <div className="row mb-3">
                      <div className="col-md-6">
                        <strong>Order Date:</strong> {new Date(selectedOrder.order_date).toLocaleDateString()}
                      </div>
                      <div className="col-md-6">
                        <strong>Total:</strong> ${selectedOrder.total_price.toFixed(2)}
                      </div>
                    </div>

                    <h6>Items:</h6>
                    <div className="table-responsive">
                      <table className="table table-sm">
                        <thead>
                          <tr>
                            <th>ISBN</th>
                            <th>Title</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Total</th>
                          </tr>
                        </thead>
                        <tbody>
                          {selectedOrder.items?.map((item) => (
                            <tr key={item.isbn}>
                              <td>{item.isbn}</td>
                              <td>{item.title}</td>
                              <td>{item.quantity}</td>
                              <td>${item.selling_price.toFixed(2)}</td>
                              <td>${item.total_price.toFixed(2)}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>

                    {selectedOrder.credit_card_no && (
                      <div className="mt-3">
                        <strong>Payment Method:</strong> **** **** **** {selectedOrder.credit_card_no.slice(-4)}
                      </div>
                    )}
                  </div>
                  <div className="modal-footer">
                    <button
                      type="button"
                      className="btn btn-secondary"
                      onClick={closeOrderDetails}
                    >
                      Close
                    </button>
                    <button
                      type="button"
                      className="btn btn-primary"
                      onClick={() => window.print()}
                    >
                      <i className="fas fa-print"></i> Print
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Modal Backdrop */}
          {selectedOrder && (
            <div className="modal-backdrop show" onClick={closeOrderDetails}></div>
          )}
        </>
      )}
    </div>
  );
};

export default Orders;
