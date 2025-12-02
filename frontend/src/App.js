import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReviewPredictor from './components/ReviewPredictor';
import CustomerReviews from './components/CustomerReviews';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function App() {
  const [allReviews, setAllReviews] = useState([]);

  const fetchAllReviews = async () => {
    try {
      const response = await axios.get(`${API_URL}/reviews/`);
      if (response.data.success) {
        setAllReviews(response.data.data);
      }
    } catch (err) {
      console.error('Error fetching reviews:', err);
    }
  };

  useEffect(() => {
    fetchAllReviews();
  }, []);

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <div className="header-left">
            <h1 className="app-logo">Automated AI Review Rating </h1>
            <p className="app-tagline">Prediction System</p>
          </div>
          <div className="header-right">
            <div className="header-stats">
              <div className="stat-item">
                <span className="stat-label">Model Used</span>
                <span className="stat-value">Logistic Regression</span>
              </div>
              
            </div>
          </div>
        </div>
      </header>
      
      <div className="content">
        <ReviewPredictor 
          showOnlyForm={true} 
          allReviews={allReviews}
          setAllReviews={setAllReviews}
        />
        <CustomerReviews allReviews={allReviews} />
        <ReviewPredictor 
          showOnlyHistory={true} 
          allReviews={allReviews}
        />
      </div>
    </div>
  );
}

export default App;