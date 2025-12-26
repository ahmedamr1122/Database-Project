import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <div className="hero-section text-center py-5 bg-light rounded mb-5">
        <h1 className="display-4">Welcome to Online Bookstore</h1>
        <p className="lead">Discover your next favorite book</p>
        <div className="mt-4">
          <Link to="/login" className="btn btn-primary btn-lg me-2">
            <i className="fas fa-sign-in-alt"></i> Login
          </Link>
          <Link to="/register" className="btn btn-success btn-lg">
            <i className="fas fa-user-plus"></i> Register
          </Link>
        </div>
      </div>

      <div className="row mb-5">
        <div className="col-md-4">
          <div className="card text-center h-100">
            <div className="card-body">
              <i className="fas fa-book fa-3x text-primary mb-3"></i>
              <h5 className="card-title">Wide Selection</h5>
              <p className="card-text">Browse through thousands of books across multiple categories</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card text-center h-100">
            <div className="card-body">
              <i className="fas fa-shipping-fast fa-3x text-success mb-3"></i>
              <h5 className="card-title">Fast Delivery</h5>
              <p className="card-text">Quick and reliable shipping to your doorstep</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card text-center h-100">
            <div className="card-body">
              <i className="fas fa-lock fa-3x text-warning mb-3"></i>
              <h5 className="card-title">Secure Payment</h5>
              <p className="card-text">Safe and secure checkout process</p>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col-12">
          <h3 className="text-center mb-4">Book Categories</h3>
          <div className="d-flex justify-content-center flex-wrap gap-3">
            <span className="badge bg-primary p-3 fs-6">Science</span>
            <span className="badge bg-success p-3 fs-6">Art</span>
            <span className="badge bg-danger p-3 fs-6">Religion</span>
            <span className="badge bg-warning p-3 fs-6">History</span>
            <span className="badge bg-info p-3 fs-6">Geography</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
