import pandas as pd

class InstagramAnalytics:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        
    def get_top_restaurants(self, n=5):
        """Get top n restaurants by engagement rate"""
        engagement_data = self.data_handler.calculate_engagement_rates()
        return engagement_data.nlargest(n, 'engagement_rate')
    
    def get_top_hashtags(self, n=5):
        """Get top n hashtags by frequency"""
        hashtag_counts = self.data_handler.analyze_hashtags()
        return hashtag_counts.head(n)
    
    def get_trending_restaurants(self, n=5):
        """Get top n trending restaurants by growth rate"""
        trends = self.data_handler.get_restaurant_trends()
        return trends.nlargest(n, 'growth_rate')
    
    def get_restaurant_summary(self, restaurant):
        """Get detailed summary for a specific restaurant"""
        restaurant_data = self.data_handler.data[
            self.data_handler.data['restaurant'] == restaurant
        ]
        
        if len(restaurant_data) == 0:
            return None
            
        hashtags = []
        for h in restaurant_data['hashtags']:
            hashtags.extend(h.split(','))
        
        top_hashtags = pd.Series(hashtags).value_counts().head(5)
        
        avg_likes = restaurant_data['likes'].mean()
        avg_comments = restaurant_data['comments'].mean()
        followers = restaurant_data['followers'].iloc[0]
        
        return {
            'avg_likes': avg_likes,
            'avg_comments': avg_comments,
            'followers': followers,
            'top_hashtags': top_hashtags,
            'total_posts': len(restaurant_data)
        }
