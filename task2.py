import pandas as pd

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
print(pink_morsel)
pink_morsel['sales'] = pink_morsel['quantity'] * pink_morsel['price']
total_sales = pink_morsel.groupby(['date','region'])['sales'].sum().reset_index()
total_sales.columns = ['Date', 'Region', 'Sales']
print(total_sales)