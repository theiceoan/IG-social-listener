import pandas as pd
from datetime import datetime, timedelta
from mock_data import get_restaurant_data
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstagramDataHandler:
    def __init__(self):
        """Initialize with empty data and tracked restaurants list"""
        logger.info("Initializing InstagramDataHandler")
        self.data = pd.DataFrame()
        self.tracked_restaurants = set()

    def add_restaurant(self, restaurant_handle):
        """Add a restaurant to track"""
        if not restaurant_handle.startswith('@'):
            restaurant_handle = '@' + restaurant_handle

        logger.info(f"Adding restaurant: {restaurant_handle}")
        self.tracked_restaurants.add(restaurant_handle)
        self.refresh_data()

    def remove_restaurant(self, restaurant_handle):
        """Remove a restaurant from tracking"""
        logger.info(f"Removing restaurant: {restaurant_handle}")
        self.tracked_restaurants.discard(restaurant_handle)
        self.refresh_data()

    def get_tracked_restaurants(self):
        """Get list of currently tracked restaurants"""
        return sorted(list(self.tracked_restaurants))

    def refresh_data(self):
        """Fetch fresh data with error handling"""
        try:
            logger.info("Attempting to fetch fresh data")
            if not self.tracked_restaurants:
                logger.info("No restaurants to track")
                self.data = pd.DataFrame()
                return

            new_data = get_restaurant_data(list(self.tracked_restaurants))

            if new_data is None:
                logger.error("get_restaurant_data returned None")
                raise ValueError("No data received from get_restaurant_data")

            if new_data.empty:
                logger.error("get_restaurant_data returned empty DataFrame")
                raise ValueError("Empty DataFrame received from get_restaurant_data")

            # Verify datetime format
            if not pd.api.types.is_datetime64_any_dtype(new_data['post_date']):
                logger.warning("Converting post_date to datetime")
                new_data['post_date'] = pd.to_datetime(new_data['post_date'])

            logger.info(f"Successfully loaded data with {len(new_data)} rows")
            self.data = new_data

        except Exception as e:
            logger.error(f"Error refreshing data: {str(e)}")
            # Initialize with empty DataFrame if data loading fails
            self.data = pd.DataFrame(columns=['restaurant', 'followers', 'post_date', 
                                            'likes', 'comments', 'hashtags'])
            raise Exception(f"Failed to load data: {str(e)}")

    def calculate_engagement_rates(self):
        """Calculate engagement rates for each restaurant"""
        try:
            if self.data.empty:
                logger.warning("No data available for engagement calculation")
                return pd.DataFrame(columns=['restaurant', 'engagement_rate', 
                                        'followers', 'total_posts'])

            engagement_data = []

            for restaurant in self.tracked_restaurants:
                restaurant_posts = self.data[self.data['restaurant'] == restaurant]

                if len(restaurant_posts) == 0:
                    continue

                total_likes = restaurant_posts['likes'].sum()
                total_comments = restaurant_posts['comments'].sum()
                followers = restaurant_posts['followers'].iloc[0]

                # Avoid division by zero
                if followers == 0:
                    logger.warning(f"Zero followers for restaurant: {restaurant}")
                    continue

                avg_engagement = ((total_likes + total_comments) / 
                                (len(restaurant_posts) * followers)) * 100

                engagement_data.append({
                    'restaurant': restaurant,
                    'engagement_rate': avg_engagement,
                    'followers': followers,
                    'total_posts': len(restaurant_posts)
                })

            return pd.DataFrame(engagement_data)
        except Exception as e:
            logger.error(f"Error calculating engagement rates: {str(e)}")
            raise

    def analyze_hashtags(self):
        """Analyze hashtag usage and trends"""
        try:
            if self.data.empty:
                logger.warning("No data available for hashtag analysis")
                return pd.Series(dtype=float)

            all_hashtags = []
            for hashtags in self.data['hashtags']:
                if pd.notna(hashtags):  # Check for NaN/None values
                    all_hashtags.extend(hashtags.split(','))

            if not all_hashtags:
                logger.warning("No hashtags found in data")
                return pd.Series(dtype=float)

            logger.info(f"Analyzed {len(all_hashtags)} hashtags")
            return pd.Series(all_hashtags).value_counts()
        except Exception as e:
            logger.error(f"Error analyzing hashtags: {str(e)}")
            raise

    def get_restaurant_trends(self):
        """Calculate restaurant trends over the past month"""
        try:
            if self.data.empty:
                logger.warning("No data available for trend analysis")
                return pd.DataFrame(columns=['restaurant', 'growth_rate'])

            now = datetime.now()
            two_weeks_ago = now - timedelta(days=14)

            recent_data = self.data[self.data['post_date'] >= two_weeks_ago]
            old_data = self.data[self.data['post_date'] < two_weeks_ago]

            trends = []

            for restaurant in self.tracked_restaurants:
                recent_engagement = recent_data[recent_data['restaurant'] == restaurant]
                old_engagement = old_data[old_data['restaurant'] == restaurant]

                if len(recent_engagement) == 0 or len(old_engagement) == 0:
                    logger.warning(f"Insufficient data for trend analysis: {restaurant}")
                    continue

                recent_rate = ((recent_engagement['likes'].mean() + 
                            recent_engagement['comments'].mean()) / 
                            recent_engagement['followers'].iloc[0] * 100)

                old_rate = ((old_engagement['likes'].mean() + 
                            old_engagement['comments'].mean()) / 
                            old_engagement['followers'].iloc[0] * 100)

                growth = ((recent_rate - old_rate) / old_rate) * 100 if old_rate > 0 else 0

                trends.append({
                    'restaurant': restaurant,
                    'growth_rate': growth
                })

            logger.info(f"Calculated trends for {len(trends)} restaurants")
            return pd.DataFrame(trends)
        except Exception as e:
            logger.error(f"Error calculating restaurant trends: {str(e)}")
            raise