import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../../context/AuthContext';

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    total_books: 0,
    total_customers: 0,
    pending_orders: 0,
    monthly_sales: 0
  });
  const [lowStockBooks, setLowStockBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const { user } = useContext(AuthContext);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');

      // Fetch stats (you'll need to implement these endpoints)
      const statsResponse = await fetch('http://localhost:5000/admin/stats', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData);
      }

      // Fetch low stock books
      const lowStockResponse = await fetch('http://localhost:5000/admin/low-stock', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (lowStockResponse.ok) {
        const lowStockData = await lowStockResponse.json();
        setLowStockBooks(lowStockData);
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
      <h2 className="mb-4">
        <i className="fas fa-tachometer-alt"></i> Admin Dashboard
      </h2>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {/* Statistics Cards */}
      <div className="row mb-4">
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <i className="fas fa-book fa-2x text-primary mb-2"></i>
              <h4 className="card-title">{stats.total_books}</h4>
              <p className="card-text">Total Books</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <i className="fas fa-users fa-2x text-success mb-2"></i>
              <h4 className="card-title">{stats.total_customers}</h4>
              <p className="card-text">Total Customers</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <i className="fas fa-box fa-2x text-warning mb-2"></i>
              <h4 className="card-title">{stats.pending_orders}</h4>
              <p className="card-text">Pending Orders</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <i className="fas fa-dollar-sign fa-2x text-info mb-2"></i>
              <h4 className="card-title">${stats.monthly_sales.toFixed(2)}</h4>
              <p className="card-text">Monthly Sales</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Quick Actions</h5>
            </div>
            <div className="card-body">
              <div className="d-flex flex-wrap gap-2">
                <a href="/admin/add-book" className="btn btn-primary">
                  <i className="fas fa-plus-circle"></i> Add New Book
                </a>
                <button className="btn btn-secondary" disabled>
                  <i className="fas fa-edit"></i> Modify Books (Coming Soon)
                </button>
                <button className="btn btn-warning" disabled>
                  <i className="fas fa-box"></i> Manage Orders (Coming Soon)
                </button>
                <button className="btn btn-info" disabled>
                  <i className="fas fa-chart-bar"></i> View Reports (Coming Soon)
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Low Stock Alert */}
      {lowStockBooks.length > 0 && (
        <div className="row">
          <div className="col-12">
            <div className="card">
              <div className="card-header bg-warning">
                <h5 className="mb-0">
                  <i className="fas fa-exclamation-triangle"></i> Low Stock Alert
                </h5>
              </div>
              <div className="card-body">
                <div className="table-responsive">
                  <table className="table table-striped">
                    <thead>
                      <tr>
                        <th>ISBN</th>
                        <th>Title</th>
                        <th>Current Stock</th>
                        <th>Threshold</th>
                      </tr>
                    </thead>
                    <tbody>
                      {lowStockBooks.map((book) => (
                        <tr key={book.isbn}>
                          <td>{book.isbn}</td>
                          <td>{book.title}</td>
                          <td>
                            <span className="badge bg-danger">{book.stock}</span>
                          </td>
                          <td>{book.threshold}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
