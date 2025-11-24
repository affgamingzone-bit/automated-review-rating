import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './CustomerReviews.css';

const API_URL = 'http://localhost:8000/api';

const CustomerReviews = () => {
  const [reviews, setReviews] = useState([]);
  const [stats, setStats] = useState({
    averageRating: 0,
    totalReviews: 0,
    ratingDistribution: {
      5: 0,
      4: 0,
      3: 0,
      2: 0,
      1: 0
    }
  });

  useEffect(() => {
    fetchReviewsData();
  }, []);

  const fetchReviewsData = async () => {
    try {
      const response = await axios.get(`${API_URL}/reviews/`);
      if (response.data.success) {
        const reviewsData = response.data.data;
        setReviews(reviewsData);
        calculateStats(reviewsData);
      }
    } catch (err) {
      console.error('Error fetching reviews:', err);
    }
  };

  const calculateStats = (reviewsData) => {
    const total = reviewsData.length;
    const distribution = {
      5: 0,
      4: 0,
      3: 0,
      2: 0,
      1: 0
    };
    let sum = 0;

    reviewsData.forEach((review) => {
      const score = review.predicted_score;
      distribution[score]++;
      sum += score;
    });

    const average = total > 0 ? (sum / total).toFixed(1) : 0;

    setStats({
      averageRating: average,
      totalReviews: total,
      ratingDistribution: distribution
    });
  };

  const getPercentage = (count) => {
    return stats.totalReviews > 0 ? Math.round((count / stats.totalReviews) * 100) : 0;
  };

  const getRatingColor = (score) => {
    if (score >= 4) return '#FF8C00';
    if (score === 3) return '#FFA500';
    return '#FF6B6B';
  };

  return (
    <div className="customer-reviews-section">
      <div className="reviews-container">
        {/* Header */}
        <div className="reviews-header">
          <h2>Customer Reviews</h2>
        </div>

        {/* Rating Summary */}
        <div className="rating-summary">
          <div className="average-rating">
            <div className="rating-number">{stats.averageRating}</div>
            <div className="rating-stars">
              {[...Array(5)].map((_, i) => (
                <span
                  key={i}
                  className={i < Math.floor(stats.averageRating) ? 'star filled' : 'star'}
                >
                  ★
                </span>
              ))}
            </div>
            <div className="total-count">{stats.totalReviews} global ratings</div>
          </div>

          {/* Rating Distribution */}
          <div className="rating-distribution">
            {[5, 4, 3, 2, 1].map((rating) => (
              <div key={rating} className="rating-bar-row">
                <span className="rating-label">{rating} star</span>
                <div className="bar-container">
                  <div
                    className="bar-fill"
                    style={{
                      width: `${getPercentage(stats.ratingDistribution[rating])}%`,
                      backgroundColor: getRatingColor(rating)
                    }}
                  />
                </div>
                <span className="percentage">{getPercentage(stats.ratingDistribution[rating])}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerReviews;
