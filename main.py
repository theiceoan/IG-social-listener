import streamlit as st
import pandas as pd
from data_handler import InstagramDataHandler
from analytics import InstagramAnalytics
from visualization import DashboardVisualizer
from datetime import datetime
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

try:
    # Page config
    st.set_page_config(
        page_title="Restaurant Instagram Analytics",
        page_icon="🍽️",
        layout="wide"
    )
    logger.info("Page configuration set successfully")

    # Initialize components with error handling
    @st.cache_resource
    def initialize_components():
        try:
            logger.info("Initializing application components")
            data_handler = InstagramDataHandler()
            analytics = InstagramAnalytics(data_handler)
            visualizer = DashboardVisualizer()
            logger.info("Components initialized successfully")
            return data_handler, analytics, visualizer
        except Exception as e:
            logger.error(f"Failed to initialize components: {str(e)}", exc_info=True)
            st.error(f"Failed to initialize components: {str(e)}")
            return None, None, None

    data_handler, analytics, visualizer = initialize_components()

    if not all([data_handler, analytics, visualizer]):
        logger.error("Failed to initialize one or more components")
        st.error("Failed to initialize the application. Please refresh the page.")
        st.stop()

    # Title and description
    st.title("🍽️ Restaurant Instagram Analytics Dashboard")
    st.markdown("""
    This dashboard tracks Instagram engagement and hashtag trends for restaurants.
    Add Instagram handles to analyze their social media performance.
    """)

    # Sidebar for restaurant management and controls
    st.sidebar.title("Dashboard Controls")

    # Restaurant Input Section
    st.sidebar.header("Add Restaurants")
    new_restaurant = st.sidebar.text_input(
        "Enter Instagram handle (e.g., @restaurantname)",
        key="new_restaurant"
    )

    if st.sidebar.button("Add Restaurant"):
        if new_restaurant:
            if not new_restaurant.startswith('@'):
                new_restaurant = '@' + new_restaurant
            try:
                data_handler.add_restaurant(new_restaurant)
                st.sidebar.success(f"Added {new_restaurant}")
            except Exception as e:
                logger.error(f"Failed to add restaurant: {str(e)}", exc_info=True)
                st.sidebar.error(f"Failed to add restaurant: {str(e)}")

    # Show current restaurants
    current_restaurants = data_handler.get_tracked_restaurants()
    if current_restaurants:
        st.sidebar.header("Tracked Restaurants")
        for restaurant in current_restaurants:
            col1, col2 = st.sidebar.columns([3, 1])
            col1.write(restaurant)
            if col2.button("Remove", key=f"remove_{restaurant}"):
                data_handler.remove_restaurant(restaurant)
                st.rerun()

    # Refresh Data Button
    if st.sidebar.button("Refresh Data"):
        try:
            data_handler.refresh_data()
            st.success("Data refreshed successfully!")
        except Exception as e:
            logger.error(f"Failed to refresh data: {str(e)}", exc_info=True)
            st.error(f"Failed to refresh data: {str(e)}")

    # Export Data Button
    if current_restaurants:
        st.sidebar.markdown("---")
        st.sidebar.header("Export Data")
        if st.sidebar.button("Export Analytics to CSV"):
            try:
                export_data = data_handler.get_analytics_export_data()
                if not export_data.empty:
                    csv = export_data.to_csv(index=False)
                    st.sidebar.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"restaurant_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    st.sidebar.success("Data ready for download!")
                else:
                    st.sidebar.warning("No data available to export")
            except Exception as e:
                logger.error(f"Failed to export data: {str(e)}", exc_info=True)
                st.sidebar.error(f"Failed to export data: {str(e)}")

    try:
        # Only show analytics if there are restaurants being tracked
        if current_restaurants:
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
            restaurants = data_handler.get_tracked_restaurants()
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
        else:
            st.info("👈 Start by adding restaurants in the sidebar")

    except Exception as e:
        logger.error(f"An error occurred while rendering the dashboard: {str(e)}", exc_info=True)
        st.error(f"An error occurred while rendering the dashboard: {str(e)}")

except Exception as e:
    logger.error(f"Critical error: {str(e)}", exc_info=True)
    st.error(f"Critical error: {str(e)}")