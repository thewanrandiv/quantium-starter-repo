import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Read the processed data
df = pd.read_csv('pink_morsels_sales.csv')

# Convert Date column to datetime for proper sorting
df['Date'] = pd.to_datetime(df['Date'])

# Sort by date
df = df.sort_values('Date')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    # Main container
    html.Div([
        # Header section with gradient background
        html.Div([
            html.H1(
                '🍬 Soul Foods: Pink Morsels Sales Analysis',
                style={
                    'textAlign': 'center',
                    'color': '#FFFFFF',
                    'marginBottom': '10px',
                    'fontFamily': 'Helvetica, Arial, sans-serif',
                    'fontWeight': 'bold',
                    'fontSize': '42px',
                    'textShadow': '2px 2px 4px rgba(0,0,0,0.3)'
                }
            ),
            html.P(
                'Sales Performance Before and After Price Increase',
                style={
                    'textAlign': 'center',
                    'color': '#FFE5EC',
                    'fontSize': '18px',
                    'fontFamily': 'Helvetica, Arial, sans-serif',
                    'marginBottom': '0'
                }
            )
        ], style={
            'background': 'linear-gradient(135deg, #E91E63 0%, #F06292 50%, #F48FB1 100%)',
            'padding': '40px 20px',
            'borderRadius': '0 0 30px 30px',
            'boxShadow': '0 4px 15px rgba(0,0,0,0.2)',
            'marginBottom': '40px'
        }),
        
        # Control panel for region filter
        html.Div([
            html.Div([
                html.Label(
                    '📍 Select Region:',
                    style={
                        'fontSize': '20px',
                        'fontWeight': 'bold',
                        'color': '#2C3E50',
                        'marginBottom': '15px',
                        'display': 'block',
                        'fontFamily': 'Helvetica, Arial, sans-serif'
                    }
                ),
                dcc.RadioItems(
                    id='region-filter',
                    options=[
                        {'label': ' All Regions', 'value': 'all'},
                        {'label': ' North', 'value': 'north'},
                        {'label': ' East', 'value': 'east'},
                        {'label': ' South', 'value': 'south'},
                        {'label': ' West', 'value': 'west'}
                    ],
                    value='all',
                    inline=True,
                    style={
                        'fontSize': '16px',
                        'fontFamily': 'Helvetica, Arial, sans-serif'
                    },
                    labelStyle={
                        'display': 'inline-block',
                        'marginRight': '25px',
                        'cursor': 'pointer',
                        'padding': '8px 15px',
                        'backgroundColor': '#FFF',
                        'borderRadius': '20px',
                        'border': '2px solid #E91E63',
                        'transition': 'all 0.3s ease'
                    }
                )
            ], style={
                'backgroundColor': '#FFFFFF',
                'padding': '25px',
                'borderRadius': '15px',
                'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
                'marginBottom': '30px'
            })
        ], style={'margin': '0 50px'}),
        
        # Line chart container
        html.Div([
            dcc.Graph(
                id='sales-chart',
                config={'displayModeBar': True, 'displaylogo': False}
            )
        ], style={
            'margin': '0 50px',
            'backgroundColor': '#FFFFFF',
            'padding': '20px',
            'borderRadius': '15px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
        }),
        
        # Summary statistics
        html.Div([
            html.Div(id='insights-panel')
        ], style={'margin': '30px 50px'})
        
    ], style={
        'backgroundColor': '#F8F9FA',
        'minHeight': '100vh',
        'paddingBottom': '50px'
    })
])

# Callback to update chart and insights based on region selection
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('insights-panel', 'children')],
    [Input('region-filter', 'value')]
)
def update_chart(selected_region):
    # Filter data based on selected region
    if selected_region == 'all':
        filtered_df = df.copy()
        region_label = 'All Regions'
    else:
        filtered_df = df[df['Region'].str.lower() == selected_region].copy()
        region_label = selected_region.capitalize()
    
    # Group by date and sum sales
    daily_sales = filtered_df.groupby('Date')['Sales'].sum().reset_index()
    
    # Create the line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_sales['Date'],
        y=daily_sales['Sales'],
        mode='lines+markers',
        name='Daily Sales',
        line=dict(color='#E91E63', width=3),
        marker=dict(size=7, color='#C2185B', line=dict(color='#FFFFFF', width=2)),
        fill='tozeroy',
        fillcolor='rgba(233, 30, 99, 0.1)'
    ))
    
    # Add a vertical line to mark the price increase date
    price_increase_date = datetime(2021, 1, 15)
    
    fig.add_vline(
        x=price_increase_date,
        line_dash="dash",
        line_color="#D32F2F",
        line_width=3,
        annotation_text="💰 Price Increase<br>Jan 15, 2021",
        annotation_position="top",
        annotation_font_size=13,
        annotation_font_color="#D32F2F",
        annotation_font_family="Helvetica, Arial, sans-serif"
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': f'Pink Morsels Sales Over Time - {region_label}',
            'font': {'size': 24, 'color': '#2C3E50', 'family': 'Helvetica, Arial, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Date',
        yaxis_title='Sales ($)',
        hovermode='x unified',
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='#FFFFFF',
        height=550,
        font=dict(size=13, family='Helvetica, Arial, sans-serif'),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#E0E0E0',
            title_font=dict(size=16, color='#2C3E50')
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#E0E0E0',
            title_font=dict(size=16, color='#2C3E50')
        )
    )
    
    # Calculate insights
    sales_before = daily_sales[daily_sales['Date'] < price_increase_date]['Sales'].mean()
    sales_after = daily_sales[daily_sales['Date'] >= price_increase_date]['Sales'].mean()
    
    # Handle case where there's no data
    if pd.isna(sales_before):
        sales_before = 0
    if pd.isna(sales_after):
        sales_after = 0
    
    change_percent = ((sales_after - sales_before) / sales_before * 100) if sales_before > 0 else 0
    
    # Determine trend
    if change_percent > 0:
        trend_icon = '📈'
        trend_color = '#4CAF50'
        trend_text = 'Increase'
    else:
        trend_icon = '📉'
        trend_color = '#F44336'
        trend_text = 'Decrease'
    
    # Create insights panel
    insights = html.Div([
        html.H3(
            f'📊 Key Insights for {region_label}',
            style={
                'color': '#2C3E50',
                'marginBottom': '20px',
                'fontFamily': 'Helvetica, Arial, sans-serif',
                'textAlign': 'center'
            }
        ),
        html.Div([
            # Before card
            html.Div([
                html.Div('Before Price Increase', style={
                    'fontSize': '16px',
                    'color': '#7F8C8D',
                    'marginBottom': '10px',
                    'fontWeight': '600'
                }),
                html.Div(f'${sales_before:,.2f}', style={
                    'fontSize': '32px',
                    'color': '#2C3E50',
                    'fontWeight': 'bold'
                }),
                html.Div('Average Daily Sales', style={
                    'fontSize': '14px',
                    'color': '#95A5A6',
                    'marginTop': '5px'
                })
            ], style={
                'flex': '1',
                'backgroundColor': '#E3F2FD',
                'padding': '25px',
                'borderRadius': '12px',
                'textAlign': 'center',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'margin': '0 10px'
            }),
            
            # Arrow
            html.Div([
                html.Div(trend_icon, style={'fontSize': '48px'})
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'padding': '0 20px'
            }),
            
            # After card
            html.Div([
                html.Div('After Price Increase', style={
                    'fontSize': '16px',
                    'color': '#7F8C8D',
                    'marginBottom': '10px',
                    'fontWeight': '600'
                }),
                html.Div(f'${sales_after:,.2f}', style={
                    'fontSize': '32px',
                    'color': '#2C3E50',
                    'fontWeight': 'bold'
                }),
                html.Div('Average Daily Sales', style={
                    'fontSize': '14px',
                    'color': '#95A5A6',
                    'marginTop': '5px'
                })
            ], style={
                'flex': '1',
                'backgroundColor': '#FCE4EC',
                'padding': '25px',
                'borderRadius': '12px',
                'textAlign': 'center',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'margin': '0 10px'
            })
        ], style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'marginBottom': '25px',
            'flexWrap': 'wrap'
        }),
        
        # Change summary
        html.Div([
            html.Span(f'{trend_text}: ', style={'fontWeight': '600', 'color': '#2C3E50'}),
            html.Span(f'{abs(change_percent):.1f}%', style={
                'fontWeight': 'bold',
                'color': trend_color,
                'fontSize': '20px'
            }),
            html.Span(f' change in average daily sales after price increase', style={'color': '#2C3E50'})
        ], style={
            'textAlign': 'center',
            'fontSize': '18px',
            'padding': '20px',
            'backgroundColor': '#FFFFFF',
            'borderRadius': '12px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'fontFamily': 'Helvetica, Arial, sans-serif'
        })
    ], style={
        'backgroundColor': '#FFFFFF',
        'padding': '30px',
        'borderRadius': '15px',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
        'fontFamily': 'Helvetica, Arial, sans-serif'
    })
    
    return fig, insights

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)