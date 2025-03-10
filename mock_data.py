import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Common hashtags that might be used
HASHTAGS = [
    "#foodie", "#foodporn", "#instafood", "#yummy", "#delicious",
    "#dinner", "#lunch", "#breakfast", "#foodstagram", "#foodphotography",
    "#blackownedrestaurants", "#soulfood", "#caribbeanfood"
]

def generate_mock_data(restaurants):
    """Generate mock Instagram data for specified restaurants"""
    if not restaurants:
        return pd.DataFrame()

    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    for restaurant in restaurants:
        followers = random.randint(1000, 50000)
        for _ in range(random.randint(10, 30)):  # Posts per restaurant
            post_date = start_date + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )

            likes = random.randint(50, int(followers * 0.1))
            comments = random.randint(5, int(likes * 0.1))

            # Generate random hashtags for each post
            post_hashtags = random.sample(HASHTAGS, random.randint(3, 7))

            data.append({
                'restaurant': restaurant,
                'followers': followers,
                'post_date': pd.Timestamp(post_date),  # Ensure proper datetime format
                'likes': likes,
                'comments': comments,
                'hashtags': ','.join(post_hashtags)
            })

    df = pd.DataFrame(data)
    df['post_date'] = pd.to_datetime(df['post_date'])  # Convert to pandas datetime
    return df

def get_restaurant_data(restaurants=None):
    """Return mock Instagram data for specified restaurants"""
    try:
        return generate_mock_data(restaurants)
    except Exception as e:
        print(f"Error generating mock data: {str(e)}")
        return None