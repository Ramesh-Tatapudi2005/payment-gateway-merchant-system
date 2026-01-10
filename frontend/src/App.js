import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Pages
import Dashboard from './pages/Dashboard';
import Transactions from './pages/Transactions';
import Orders from './pages/Orders'; 
import CreateOrder from './pages/CreateOrder';
import Login from './pages/Login';

// Components
import Sidebar from './components/Sidebar'; 

function App() {
  // Requirement: Authentication check
  // We check localStorage for the flag set by your Login.jsx component
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

  return (
    <Router>
      <div className="flex min-h-screen bg-gray-50">
        {/* Requirement: Dashboard should only display after successful login */}
        {isAuthenticated && <Sidebar />}
        
        <main className="flex-1">
          <div className="max-w-7xl mx-auto">
            <Routes>
              {/* AUTH ROUTE - Accessible always, but redirects if already logged in */}
              <Route 
                path="/login" 
                element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" replace />} 
              />

              {/* PROTECTED ROUTES - Redirect to /login if not authenticated */}
              <Route 
                path="/dashboard" 
                element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" replace />} 
              />
              
              <Route 
                path="/transactions" 
                element={isAuthenticated ? <Transactions /> : <Navigate to="/login" replace />} 
              />
              
              <Route 
                path="/orders" 
                element={isAuthenticated ? <Orders /> : <Navigate to="/login" replace />} 
              />
              
              <Route 
                path="/create-order" 
                element={isAuthenticated ? <CreateOrder /> : <Navigate to="/login" replace />} 
              />

              {/* DEFAULT NAVIGATION */}
              <Route 
                path="/" 
                element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />} 
              />
              
              {/* CATCH-ALL REDIRECT */}
              <Route 
                path="*" 
                element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />} 
              />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;