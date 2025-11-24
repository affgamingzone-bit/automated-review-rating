import React from 'react';
import ReviewPredictor from './components/ReviewPredictor';
import CustomerReviews from './components/CustomerReviews';
import './App.css';

function App() {
  return (
    <div className="App">
     
      
      <div className="content">
        <ReviewPredictor showOnlyForm={true} />
        <CustomerReviews />
        <ReviewPredictor showOnlyHistory={true} />
      </div>
    </div>
  );
}

export default App;