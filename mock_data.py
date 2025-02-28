import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

RESTAURANTS = [
    "@deosaevents", "@deluxe_manna", "@chukusldn", "@thegoldcoastlondon",
    "@ekorestaurant", "@ssweet1ne", "@280degreesbar", "@akokorestaurant",
    "@maubybrockley", "@fishwingsandtings", "@jamdelish", "@bustermantis",
    "@bokitla", "@fenchurchrestaurant", "@jaybabas_kitchen", "@yayaskitchenldnont"
]

HASHTAGS = [
    "#foodie", "#foodporn", "#instafood", "#yummy", "#delicious",
    "#dinner", "#lunch", "#breakfast", "#foodstagram", "#foodphotography",
    "#blackownedrestaurants", "#soulfood", "#caribbeanfood"
]

def generate_mock_data():
    """Generate mock Instagram data for restaurants"""
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    for restaurant in RESTAURANTS:
        followers = random.randint(1000, 50000)
        for _ in range(random.randint(10, 30)):  # Posts per restaurant
            post_date = start_date + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23)
            )
            
            likes = random.randint(50, int(followers * 0.1))
            comments = random.randint(5, int(likes * 0.1))
            
            # Generate random hashtags for each post
            post_hashtags = random.sample(HASHTAGS, random.randint(3, 7))
            
            data.append({
                'restaurant': restaurant,
                'followers': followers,
                'post_date': post_date,
                'likes': likes,
                'comments': comments,
                'hashtags': ','.join(post_hashtags)
            })
    
    return pd.DataFrame(data)

def get_restaurant_data():
    """Return mock Instagram data"""
    return generate_mock_data()
