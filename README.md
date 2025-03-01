# Restaurant Instagram Analytics Dashboard 🍽️

A Streamlit-based dashboard for tracking and analyzing Instagram engagement metrics for restaurants. Monitor performance, analyze hashtag trends, and export analytics data.

## Features

- 📊 Track multiple restaurant Instagram accounts
- 📈 Real-time engagement analytics
- 🏷️ Hashtag trend analysis
- 📱 Interactive visualization
- 💾 Data export functionality
- 🔄 Persistent storage with PostgreSQL

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- Required Python packages (automatically installed)

## Installation

1. Clone the repository to your local machine or Replit workspace

2. Install the required Python packages:
```bash
pip install streamlit pandas plotly psycopg2-binary
```

3. Set up PostgreSQL database environment variables:
```
DATABASE_URL=postgresql://user:password@host:port/dbname
PGUSER=your_username
PGPASSWORD=your_password
PGHOST=your_host
PGPORT=your_port
PGDATABASE=your_database
```

## Running the Application

1. Start the Streamlit server:
```bash
streamlit run main.py
```

2. The application will be available at `http://localhost:5000` (or your configured port)

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
- `database.py`: Database connection handling
- `mock_data.py`: Sample data generation for testing

## Database Schema

The application uses a PostgreSQL database with the following table:

```sql
CREATE TABLE IF NOT EXISTS restaurants (
    id SERIAL PRIMARY KEY,
    handle VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
