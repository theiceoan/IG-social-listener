# Restaurant Instagram Analytics Dashboard 🍽️

A Streamlit-based dashboard for tracking and analyzing Instagram engagement metrics for restaurants. Monitor performance, analyze hashtag trends, and access analytics data through REST API endpoints.

## Features

- 📊 Track multiple restaurant Instagram accounts
- 📈 Real-time engagement analytics
- 🏷️ Hashtag trend analysis
- 📱 Interactive visualization
- 🔄 RESTful API for data access
- 💾 Local SQLite database for data persistence

## Prerequisites

- Python 3.11 or higher
- Required Python packages (automatically installed)

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone <repository-url>
   cd restaurant-instagram-analytics
   ```

2. Install the required Python packages:
   ```bash
   pip install streamlit pandas plotly flask flask-cors
   ```

## Running the Application

1. Start the Streamlit server:
   ```bash
   streamlit run main.py
   ```

2. Start the Flask API server:
   ```bash
   python api.py
   ```

3. The Streamlit dashboard will be available at `http://localhost:5000`
4. The API endpoints will be available at `http://localhost:5001`

## API Documentation

### Available Endpoints

#### 1. Get All Analytics Data
- **Endpoint:** `/api/analytics`
- **Method:** GET
- **Response:** Array of restaurant analytics data including engagement rates, follower counts, and growth metrics
- **Example Response:**
  ```json
  [
    {
      "Restaurant Handle": "@restaurant",
      "Followers": 10000,
      "Total Posts": 50,
      "Average Likes": 500,
      "Average Comments": 25,
      "Engagement Rate (%)": 5.25,
      "Growth Rate (%)": 10.5,
      "Top Hashtags": "#food, #restaurant, #foodie"
    }
  ]
  ```

#### 2. Get All Tracked Restaurants
- **Endpoint:** `/api/restaurants`
- **Method:** GET
- **Response:** Array of restaurant handles
- **Example Response:**
  ```json
  ["@restaurant1", "@restaurant2", "@restaurant3"]
  ```

#### 3. Get Single Restaurant Details
- **Endpoint:** `/api/restaurant/<handle>`
- **Method:** GET
- **Parameters:** `handle` - Restaurant's Instagram handle (with or without @)
- **Response:** Detailed metrics for the specified restaurant
- **Example Response:**
  ```json
  {
    "avg_likes": 500.5,
    "avg_comments": 25.3,
    "followers": 10000,
    "top_hashtags": {
      "#food": 20,
      "#restaurant": 15
    },
    "total_posts": 50
  }
  ```

#### 4. Get Hashtag Analysis
- **Endpoint:** `/api/hashtags`
- **Method:** GET
- **Response:** Object with hashtag frequencies
- **Example Response:**
  ```json
  {
    "#food": 100,
    "#restaurant": 75,
    "#foodie": 50
  }
  ```

### Error Responses
All endpoints return error responses in the following format:
```json
{
  "error": "Error message description"
}
```

## Usage Guide

### Adding Restaurants
1. Navigate to the sidebar
2. Enter the Instagram handle (e.g., @restaurantname)
3. Click "Add Restaurant"

### Viewing Analytics
- Top Performing Restaurants: View engagement rates and growth trends
- Hashtag Analysis: See most used hashtags and their frequency
- Restaurant Detail Analysis: Select specific restaurants for detailed metrics

## Project Structure

- `main.py`: Main Streamlit application
- `api.py`: REST API endpoints
- `analytics.py`: Analytics calculation logic
- `data_handler.py`: Data management and database operations
- `visualization.py`: Data visualization components
- `database.py`: SQLite database connection handling
- `mock_data.py`: Sample data generation for testing
- `instagram_analytics.db`: Local SQLite database file

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.