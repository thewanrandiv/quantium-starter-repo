import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Read the processed data
df = pd.read_csv('pink_morsels_sales.csv')

# Convert Date column to datetime for proper sorting
df['Date'] = pd.to_datetime(df['Date'])

# Sort by date
df = df.sort_values('Date')

# Group by date and sum sales across all regions
daily_sales = df.groupby('Date')['Sales'].sum().reset_index()

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the line chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=daily_sales['Date'],
    y=daily_sales['Sales'],
    mode='lines+markers',
    name='Daily Sales',
    line=dict(color='#E91E63', width=2),
    marker=dict(size=6)
))

# Add a vertical line to mark the price increase date (January 15, 2021)
price_increase_date = datetime(2021, 1, 15)

fig.add_vline(
    x=price_increase_date,
    line_dash="dash",
    line_color="red",
    annotation_text="Price Increase (Jan 15, 2021)",
    annotation_position="top"
)

# Update layout with proper labels and styling
fig.update_layout(
    title='Pink Morsels Sales Over Time',
    xaxis_title='Date',
    yaxis_title='Sales ($)',
    hovermode='x unified',
    plot_bgcolor='white',
    height=600,
    font=dict(size=12)
)

# Add gridlines
fig.update_xaxis(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_yaxis(showgrid=True, gridwidth=1, gridcolor='LightGray')

# Define the app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1(
            'Soul Foods: Pink Morsels Sales Analysis',
            style={
                'textAlign': 'center',
                'color': '#2C3E50',
                'marginTop': '20px',
                'marginBottom': '10px',
                'fontFamily': 'Arial, sans-serif'
            }
        ),
        html.H3(
            'Sales Performance Before and After Price Increase',
            style={
                'textAlign': 'center',
                'color': '#7F8C8D',
                'marginBottom': '30px',
                'fontFamily': 'Arial, sans-serif',
                'fontWeight': 'normal'
            }
        )
    ]),
    
    # Line chart
    html.Div([
        dcc.Graph(
            id='sales-chart',
            figure=fig
        )
    ], style={'margin': '0 50px'}),
    
    # Summary statistics
    html.Div([
        html.Div([
            html.H4('Key Insights:', style={'color': '#2C3E50', 'marginBottom': '15px'}),
            html.P([
                html.Strong('Before Price Increase: '),
                f"Average Daily Sales = ${daily_sales[daily_sales['Date'] < price_increase_date]['Sales'].mean():.2f}"
            ], style={'fontSize': '16px', 'marginBottom': '10px'}),
            html.P([
                html.Strong('After Price Increase: '),
                f"Average Daily Sales = ${daily_sales[daily_sales['Date'] >= price_increase_date]['Sales'].mean():.2f}"
            ], style={'fontSize': '16px', 'marginBottom': '10px'}),
        ], style={
            'margin': '30px auto',
            'padding': '20px',
            'maxWidth': '800px',
            'backgroundColor': '#ECF0F1',
            'borderRadius': '10px',
            'fontFamily': 'Arial, sans-serif'
        })
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)