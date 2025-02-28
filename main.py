import streamlit as st
import pandas as pd
from data_handler import InstagramDataHandler
from analytics import InstagramAnalytics
from visualization import DashboardVisualizer
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Restaurant Instagram Analytics",
    page_icon="🍽️",
    layout="wide"
)

# Initialize components
data_handler = InstagramDataHandler()
analytics = InstagramAnalytics(data_handler)
visualizer = DashboardVisualizer()

# Title and description
st.title("🍽️ Restaurant Instagram Analytics Dashboard")
st.markdown("""
This dashboard tracks Instagram engagement and hashtag trends for selected Black-owned restaurants.
Data is refreshed daily to provide the latest insights on social media performance.
""")

# Sidebar for filters and controls
st.sidebar.title("Dashboard Controls")
if st.sidebar.button("Refresh Data"):
    data_handler.refresh_data()
    st.success("Data refreshed successfully!")

# Top restaurants by engagement
st.header("📈 Top Performing Restaurants")
col1, col2 = st.columns(2)

with col1:
    top_restaurants = analytics.get_top_restaurants()
    st.plotly_chart(
        visualizer.create_engagement_bar_chart(top_restaurants),
        use_container_width=True
    )

with col2:
    trending_restaurants = analytics.get_trending_restaurants()
    st.plotly_chart(
        visualizer.create_trend_line_chart(trending_restaurants),
        use_container_width=True
    )

# Hashtag analysis
st.header("🏷️ Hashtag Analysis")
top_hashtags = analytics.get_top_hashtags()
st.plotly_chart(
    visualizer.create_hashtag_bubble_chart(top_hashtags),
    use_container_width=True
)

# Restaurant detailed analysis
st.header("🔍 Restaurant Detail Analysis")
selected_restaurant = st.selectbox(
    "Select a restaurant to analyze:",
    data_handler.data['restaurant'].unique()
)

if selected_restaurant:
    summary = analytics.get_restaurant_summary(selected_restaurant)
    if summary:
        st.plotly_chart(
            visualizer.create_restaurant_summary_cards(summary),
            use_container_width=True
        )
        
        st.subheader("Top Hashtags for " + selected_restaurant)
        st.write(summary['top_hashtags'])
    else:
        st.warning("No data available for selected restaurant")

# Footer with last update time
st.markdown("---")
st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
