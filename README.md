# Restaurant Instagram Analytics Dashboard 🍽️

A Streamlit-based dashboard for tracking and analyzing Instagram engagement metrics for restaurants. Monitor performance, analyze hashtag trends, and export analytics data.

## Features

- 📊 Track multiple restaurant Instagram accounts
- 📈 Real-time engagement analytics
- 🏷️ Hashtag trend analysis
- 📱 Interactive visualization
- 💾 Data export functionality
- 🔄 Local SQLite database for data persistence

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
   pip install streamlit pandas plotly
   ```

## Running the Application

1. Start the Streamlit server:
   ```bash
   streamlit run main.py
   ```

2. The application will be available at `http://localhost:5000`

## Usage Guide

### Adding Restaurants
1. Navigate to the sidebar
2. Enter the Instagram handle (e.g., @restaurantname)
3. Click "Add Restaurant"

### Viewing Analytics
- Top Performing Restaurants: View engagement rates and growth trends
- Hashtag Analysis: See most used hashtags and their frequency
- Restaurant Detail Analysis: Select specific restaurants for detailed metrics

### Exporting Data
1. Click "Export Analytics to CSV" in the sidebar
2. Download the generated CSV file containing all metrics

## Project Structure

- `main.py`: Main Streamlit application
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