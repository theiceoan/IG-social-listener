import pandas as pd
from datetime import datetime, timedelta
from mock_data import get_restaurant_data

class InstagramDataHandler:
    def __init__(self):
        self.data = None
        self.refresh_data()
    
    def refresh_data(self):
        """Fetch fresh data"""
        self.data = get_restaurant_data()
    
    def calculate_engagement_rates(self):
        """Calculate engagement rates for each restaurant"""
        engagement_data = []
        
        for restaurant in self.data['restaurant'].unique():
            restaurant_posts = self.data[self.data['restaurant'] == restaurant]
            
            if len(restaurant_posts) == 0:
                continue
                
            total_likes = restaurant_posts['likes'].sum()
            total_comments = restaurant_posts['comments'].sum()
            followers = restaurant_posts['followers'].iloc[0]
            
            avg_engagement = ((total_likes + total_comments) / 
                            (len(restaurant_posts) * followers)) * 100
            
            engagement_data.append({
                'restaurant': restaurant,
                'engagement_rate': avg_engagement,
                'followers': followers,
                'total_posts': len(restaurant_posts)
            })
        
        return pd.DataFrame(engagement_data)
    
    def analyze_hashtags(self):
        """Analyze hashtag usage and trends"""
        all_hashtags = []
        for hashtags in self.data['hashtags']:
            all_hashtags.extend(hashtags.split(','))
            
        hashtag_counts = pd.Series(all_hashtags).value_counts()
        
        return hashtag_counts
    
    def get_restaurant_trends(self):
        """Calculate restaurant trends over the past month"""
        now = datetime.now()
        two_weeks_ago = now - timedelta(days=14)
        
        recent_data = self.data[self.data['post_date'] >= two_weeks_ago]
        old_data = self.data[self.data['post_date'] < two_weeks_ago]
        
        trends = []
        
        for restaurant in self.data['restaurant'].unique():
            recent_engagement = recent_data[recent_data['restaurant'] == restaurant]
            old_engagement = old_data[old_data['restaurant'] == restaurant]
            
            if len(recent_engagement) == 0 or len(old_engagement) == 0:
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
            
        return pd.DataFrame(trends)
