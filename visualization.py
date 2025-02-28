import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class DashboardVisualizer:
    def create_engagement_bar_chart(self, engagement_data):
        """Create bar chart for engagement rates"""
        fig = px.bar(
            engagement_data,
            x='restaurant',
            y='engagement_rate',
            title='Restaurant Engagement Rates',
            labels={'restaurant': 'Restaurant', 'engagement_rate': 'Engagement Rate (%)'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig
    
    def create_hashtag_bubble_chart(self, hashtag_counts):
        """Create bubble chart for hashtag frequency"""
        df = pd.DataFrame({
            'hashtag': hashtag_counts.index,
            'count': hashtag_counts.values
        })
        
        fig = px.scatter(
            df,
            x='hashtag',
            y='count',
            size='count',
            title='Hashtag Usage Frequency',
            labels={'hashtag': 'Hashtag', 'count': 'Frequency'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig
    
    def create_trend_line_chart(self, trend_data):
        """Create line chart for growth trends"""
        fig = px.line(
            trend_data,
            x='restaurant',
            y='growth_rate',
            title='Restaurant Growth Trends',
            labels={'restaurant': 'Restaurant', 'growth_rate': 'Growth Rate (%)'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig
    
    def create_restaurant_summary_cards(self, summary):
        """Create summary metrics cards"""
        metrics = go.Figure()
        
        metrics.add_trace(go.Indicator(
            mode="number",
            value=summary['avg_likes'],
            title="Average Likes",
            domain={'row': 0, 'column': 0}
        ))
        
        metrics.add_trace(go.Indicator(
            mode="number",
            value=summary['avg_comments'],
            title="Average Comments",
            domain={'row': 0, 'column': 1}
        ))
        
        metrics.add_trace(go.Indicator(
            mode="number",
            value=summary['followers'],
            title="Followers",
            domain={'row': 1, 'column': 0}
        ))
        
        metrics.add_trace(go.Indicator(
            mode="number",
            value=summary['total_posts'],
            title="Total Posts",
            domain={'row': 1, 'column': 1}
        ))
        
        metrics.update_layout(
            grid={'rows': 2, 'columns': 2},
            height=400
        )
        
        return metrics
