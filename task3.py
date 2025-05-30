# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash()

# assume you have a "long-form" data frame
data0 = pd.read_csv('/Users/timmochou/workspace/Quantium_SWE/data/daily_sales_data_0.csv')
data1 = pd.read_csv('/Users/timmochou/workspace/Quantium_SWE/data/daily_sales_data_1.csv')
data2 = pd.read_csv('/Users/timmochou/workspace/Quantium_SWE/data/daily_sales_data_2.csv')
# Concatenate DataFrames
data = pd.concat([data0,data1,data2],ignore_index=True)
# only want to see the product of pink morsel
pink_morsel = data[data['product']=='pink morsel']

"""
to watch the total sales: multiply the quantity and price groupby given day
"""

#reomve the $ IN THE PRICE COLUMN
pink_morsel['price'] = pink_morsel['price'].str.replace('$', '')
# Convert the data type to float 
pink_morsel['price'] = pink_morsel['price'].astype(float)
pink_morsel['quantity'] = pink_morsel['quantity'].astype(float)
# Calculate sales
pink_morsel['sales'] = pink_morsel['quantity'] * pink_morsel['price']

# Convert date to datetime
pink_morsel['date'] = pd.to_datetime(pink_morsel['date'])

# Set date as index for resampling
pink_morsel.set_index('date', inplace=True)

# Resample data by 15-day periods for each region
total_sales = pink_morsel.groupby('region').resample('15D')['sales'].sum().reset_index()
total_sales.columns = ['Region', 'Date', 'Sales']

# Sort by date
total_sales = total_sales.sort_values('Date')

fig = px.line(total_sales, x="Date", y="Sales", 
              title="Pink Morsel Sales Before and After Price Increase (Jan 15, 2021)",
              labels={
                  "Date": "Date",
                  "Sales": "Total Sales ($)",
                  "Region": "Region"
              },
              color='Region')

fig.update_layout(
    title_x=0.5,
    title_font_size=20,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
    showlegend=True
)

fig.show()