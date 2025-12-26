import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container">
        <Link className="navbar-brand" to="/">
          <i className="fas fa-book-open"></i> Online Bookstore
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            {user ? (
              <>
                {user.role === 'admin' ? (
                  <>
                    <li className="nav-item">
                      <Link className="nav-link" to="/admin/dashboard">
                        <i className="fas fa-tachometer-alt"></i> Dashboard
                      </Link>
                    </li>
                    <li className="nav-item">
                      <Link className="nav-link" to="/admin/add-book">
                        <i className="fas fa-plus-circle"></i> Add Book
                      </Link>
                    </li>
                    <li className="nav-item">
                      <Link className="nav-link" to="/admin/orders">
                        <i className="fas fa-box"></i> Orders
                      </Link>
                    </li>
                    <li className="nav-item">
                      <Link className="nav-link" to="/admin/reports">
                        <i className="fas fa-chart-bar"></i> Reports
                      </Link>
                    </li>
                  </>
                ) : (
                  <>
                    <li className="nav-item">
                      <Link className="nav-link" to="/customer/dashboard">
                        <i className="fas fa-home"></i> Home
                      </Link>
                    </li>
                    <li className="nav-item">
                      <Link className="nav-link" to="/customer/search">
                        <i className="fas fa-search"></i> Search Books
                      </Link>
                    </li>
                    <li className="nav-item">
                      <Link className="nav-link" to="/customer/cart">
                        <i className="fas fa-shopping-cart"></i> Cart
                        <span className="badge bg-danger ms-1" id="cart-count">0</span>
                      </Link>
                    </li>
                    <li className="nav-item">
                      <Link className="nav-link" to="/customer/orders">
                        <i className="fas fa-receipt"></i> My Orders
                      </Link>
                    </li>
                    <li className="nav-item">
                      <Link className="nav-link" to="/customer/profile">
                        <i className="fas fa-user"></i> Profile
                      </Link>
                    </li>
                  </>
                )}
                <li className="nav-item">
                  <button className="btn btn-link nav-link" onClick={handleLogout}>
                    <i className="fas fa-sign-out-alt"></i> Logout ({user.username})
                  </button>
                </li>
              </>
            ) : (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/login">
                    <i className="fas fa-sign-in-alt"></i> Login
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/register">
                    <i className="fas fa-user-plus"></i> Register
                  </Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
