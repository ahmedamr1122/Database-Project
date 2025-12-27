import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import AdminDashboard from './components/admin/Dashboard';
import AddBook from './components/admin/AddBook';
import CustomerDashboard from './components/customer/Dashboard';
import SearchBooks from './components/customer/SearchBooks';
import Cart from './components/customer/Cart';
import Checkout from './components/customer/Checkout';
import Orders from './components/customer/Orders';
import Profile from './components/customer/Profile';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Navbar />
          <div className="container mt-4">
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              {/* Admin Routes */}
              <Route path="/admin/dashboard" element={<AdminDashboard />} />
              <Route path="/admin/add-book" element={<AddBook />} />

              {/* Customer Routes */}
              <Route path="/customer/dashboard" element={<CustomerDashboard />} />
              <Route path="/customer/search" element={<SearchBooks />} />
              <Route path="/customer/cart" element={<Cart />} />
              <Route path="/customer/checkout" element={<Checkout />} />
              <Route path="/customer/orders" element={<Orders />} />
              <Route path="/customer/profile" element={<Profile />} />

              {/* Default redirect */}
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </div>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
