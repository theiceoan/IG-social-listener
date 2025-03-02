from flask import Flask, jsonify
from flask_cors import CORS
from data_handler import InstagramDataHandler
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize data handler
data_handler = InstagramDataHandler()

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get all analytics data in JSON format"""
    try:
        analytics_data = data_handler.get_analytics_export_data()
        if analytics_data.empty:
            return jsonify({'error': 'No data available'}), 404

        # Convert DataFrame to dict for JSON serialization
        data = analytics_data.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in analytics endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    """Get list of tracked restaurants"""
    try:
        restaurants = data_handler.get_tracked_restaurants()
        return jsonify(restaurants)
    except Exception as e:
        logger.error(f"Error in restaurants endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/restaurant/<handle>', methods=['GET'])
def get_restaurant_details(handle):
    """Get detailed analytics for a specific restaurant"""
    try:
        if not handle.startswith('@'):
            handle = '@' + handle

        summary = data_handler.get_restaurant_summary(handle)
        if not summary:
            return jsonify({'error': 'Restaurant not found'}), 404

        # Convert NumPy types to native Python types for JSON serialization
        serializable_summary = {
            'avg_likes': float(summary['avg_likes']),
            'avg_comments': float(summary['avg_comments']),
            'followers': int(summary['followers']),
            'top_hashtags': summary['top_hashtags'].to_dict(),
            'total_posts': int(summary['total_posts'])
        }
        return jsonify(serializable_summary)
    except Exception as e:
        logger.error(f"Error in restaurant details endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/hashtags', methods=['GET'])
def get_hashtags():
    """Get hashtag analysis data"""
    try:
        hashtags = data_handler.analyze_hashtags()
        if hashtags.empty:
            return jsonify({'error': 'No hashtag data available'}), 404

        # Convert Series to dict for JSON serialization
        data = {tag: int(count) for tag, count in hashtags.items()}
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in hashtags endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        logger.info("Starting Flask API server on port 5001")
        app.run(host='0.0.0.0', port=5001)
    except Exception as e:
        logger.error(f"Failed to start Flask server: {str(e)}")
        raise