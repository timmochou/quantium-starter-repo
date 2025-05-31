from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
data0 = pd.read_csv('/Users/timmochou/workspace/Quantium_SWE/data/daily_sales_data_0.csv')
data1 = pd.read_csv('/Users/timmochou/workspace/Quantium_SWE/data/daily_sales_data_1.csv')
data2 = pd.read_csv('/Users/timmochou/workspace/Quantium_SWE/data/daily_sales_data_2.csv')
# Concatenate DataFrames
data = pd.concat([data0,data1,data2],ignore_index=True)
# only want to see the product of pink morsel
pink_morsel = data[data['product']=='pink morsel'].copy()

"""
to watch the total sales: multiply the quantity and price groupby given day
"""

#reomve the $ IN THE PRICE COLUMN
pink_morsel.loc[:, 'price'] = pink_morsel['price'].str.replace('$', '')
# Convert the data type to float 
pink_morsel.loc[:, 'price'] = pink_morsel['price'].astype(float)
pink_morsel.loc[:, 'quantity'] = pink_morsel['quantity'].astype(float)
# Calculate sales
pink_morsel.loc[:, 'sales'] = pink_morsel['quantity'] * pink_morsel['price']

# Convert date to datetime
pink_morsel['date'] = pd.to_datetime(pink_morsel['date'])

# Set date as index for resampling
pink_morsel.set_index('date', inplace=True)

# Resample data by 15-day periods for each region
total_sales = pink_morsel.groupby('region').resample('15D')['sales'].sum().reset_index()
total_sales.columns = ['Region', 'Date', 'Sales']

# Sort by date
df = total_sales.sort_values('Date')

app.layout = html.Div([
    html.H1("Pink Morsel Sales Analysis", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[
                {'label': 'All Regions', 'value': 'all'},
                *[{'label': region, 'value': region} for region in df['Region'].unique()]
            ],
            value='all',
            style={'width': '50%'}
        )
    ], style={'margin': '20px'}),
    dcc.Graph(id='graph-with-slider')
])

@callback(
    Output('graph-with-slider', 'figure'),
    Input('region-dropdown', 'value')
)
def update_figure(selected_region):
    if selected_region == 'all':
        filtered_df = df
        title = "Pink Morsel Sales Across All Regions"
    else:
        filtered_df = df[df['Region'] == selected_region]
        title = f"Pink Morsel Sales in {selected_region}"
    
    fig = px.line(filtered_df, 
                  x="Date", 
                  y="Sales",
                  color='Region',
                  title=title,
                  labels={
                      "Date": "Date",
                      "Sales": "Total Sales ($)"
                  })
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        hovermode='x unified'
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)