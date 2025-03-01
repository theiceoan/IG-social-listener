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
- PostgreSQL database (local installation)
- Required Python packages (automatically installed)

## Installation

1. Clone the repository to your local machine or Replit workspace

2. Install PostgreSQL locally if not already installed:
   ```bash
   # For Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib

   # For macOS using Homebrew
   brew install postgresql
   ```

3. Start PostgreSQL service:
   ```bash
   # For Ubuntu/Debian
   sudo service postgresql start

   # For macOS
   brew services start postgresql
   ```

4. Create a local database and user:
   ```sql
   sudo -u postgres psql
   CREATE DATABASE instagram_analytics;
   CREATE USER instagram_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE instagram_analytics TO instagram_user;
   ```

5. Install the required Python packages:
   ```bash
   pip install streamlit pandas plotly psycopg2-binary
   ```

6. Set up local environment variables:
   ```bash
   export PGUSER=instagram_user
   export PGPASSWORD=your_password
   export PGHOST=localhost
   export PGPORT=5432
   export PGDATABASE=instagram_analytics
   ```

7. Initialize the database schema:
   ```sql
   psql -U instagram_user -d instagram_analytics
   CREATE TABLE IF NOT EXISTS restaurants (
       id SERIAL PRIMARY KEY,
       handle VARCHAR(255) UNIQUE NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
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