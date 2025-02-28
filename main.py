import streamlit as st
import pandas as pd
from data_handler import InstagramDataHandler
from analytics import InstagramAnalytics
from visualization import DashboardVisualizer
from datetime import datetime

try:
    # Page config
    st.set_page_config(
        page_title="Restaurant Instagram Analytics",
        page_icon="🍽️",
        layout="wide"
    )

    # Initialize components with error handling
    @st.cache_resource
    def initialize_components():
        try:
            data_handler = InstagramDataHandler()
            analytics = InstagramAnalytics(data_handler)
            visualizer = DashboardVisualizer()
            return data_handler, analytics, visualizer
        except Exception as e:
            st.error(f"Failed to initialize components: {str(e)}")
            return None, None, None

    data_handler, analytics, visualizer = initialize_components()

    if not all([data_handler, analytics, visualizer]):
        st.error("Failed to initialize the application. Please refresh the page.")
        st.stop()

    # Title and description
    st.title("🍽️ Restaurant Instagram Analytics Dashboard")
    st.markdown("""
    This dashboard tracks Instagram engagement and hashtag trends for selected Black-owned restaurants.
    Data is refreshed daily to provide the latest insights on social media performance.
    """)

    # Sidebar for filters and controls
    st.sidebar.title("Dashboard Controls")
    if st.sidebar.button("Refresh Data"):
        try:
            data_handler.refresh_data()
            st.success("Data refreshed successfully!")
        except Exception as e:
            st.error(f"Failed to refresh data: {str(e)}")

    try:
        # Top restaurants by engagement
        st.header("📈 Top Performing Restaurants")
        col1, col2 = st.columns(2)

        with col1:
            top_restaurants = analytics.get_top_restaurants()
            if not top_restaurants.empty:
                st.plotly_chart(
                    visualizer.create_engagement_bar_chart(top_restaurants),
                    use_container_width=True
                )
            else:
                st.info("No engagement data available")

        with col2:
            trending_restaurants = analytics.get_trending_restaurants()
            if not trending_restaurants.empty:
                st.plotly_chart(
                    visualizer.create_trend_line_chart(trending_restaurants),
                    use_container_width=True
                )
            else:
                st.info("No trending data available")

        # Hashtag analysis
        st.header("🏷️ Hashtag Analysis")
        top_hashtags = analytics.get_top_hashtags()
        if not top_hashtags.empty:
            st.plotly_chart(
                visualizer.create_hashtag_bubble_chart(top_hashtags),
                use_container_width=True
            )
        else:
            st.info("No hashtag data available")

        # Restaurant detailed analysis
        st.header("🔍 Restaurant Detail Analysis")
        restaurants = data_handler.data['restaurant'].unique()
        if len(restaurants) > 0:
            selected_restaurant = st.selectbox(
                "Select a restaurant to analyze:",
                restaurants
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
        else:
            st.info("No restaurant data available")

        # Footer with last update time
        st.markdown("---")
        st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        st.error(f"An error occurred while rendering the dashboard: {str(e)}")

except Exception as e:
    st.error(f"Critical error: {str(e)}")