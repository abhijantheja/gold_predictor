import pandas as pd
import mysql.connector
from mysql.connector import Error

# Step 1: Load data from CSV
data = pd.read_csv("FINAL_USO.csv")
data.columns = data.columns.str.strip()  # Remove spaces from column names

# Step 2: Validate the required columns
required_columns = {
    'gold_prices': ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'],
    'stock_indices': ['Date', 'SP_open', 'SP_high', 'SP_low', 'SP_close', 'SP_Ajclose', 'SP_volume', 
                      'DJ_open', 'DJ_high', 'DJ_low', 'DJ_close', 'DJ_Ajclose', 'DJ_volume'],
    'etf_data': ['Date', 'GDX_Open', 'GDX_High', 'GDX_Low', 'GDX_Close', 'GDX_Adj Close', 'GDX_Volume',
                 'USO_Open', 'USO_High', 'USO_Low', 'USO_Close', 'USO_Adj Close', 'USO_Volume'],
    'exchange_rates': ['Date', 'EU_Price', 'EU_open', 'EU_high', 'EU_low', 'EU_Trend', 
                       'USDI_Price', 'USDI_Open', 'USDI_High', 'USDI_Low', 'USDI_Volume', 'USDI_Trend'],
    'futures_data': ['Date', 'OF_Price', 'OF_Open', 'OF_High', 'OF_Low', 'OF_Volume', 'OF_Trend', 
                     'SF_Price', 'SF_Open', 'SF_High', 'SF_Low', 'SF_Volume', 'SF_Trend'],
    'other_metals': ['Date', 'PLT_Price', 'PLT_Open', 'PLT_High', 'PLT_Low', 'PLT_Trend', 
                     'PLD_Price', 'PLD_Open', 'PLD_High', 'PLD_Low', 'PLD_Trend', 'RHO_PRICE'],
    'eg_usb_data': ['Date', 'EG_open', 'EG_high', 'EG_low', 'EG_close', 'EG_Ajclose', 'EG_volume',
                    'USB_Price', 'USB_Open', 'USB_High', 'USB_Low', 'USB_Trend']
}



# Step 3: Process data subsets
gold_prices_data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].copy()
gold_prices_data.columns = ['date_id', 'open', 'high', 'low', 'close', 'adj_close', 'volume']

stock_indices_data = data[['Date', 'SP_open', 'SP_high', 'SP_low', 'SP_close', 'SP_Ajclose', 'SP_volume',
                           'DJ_open', 'DJ_high', 'DJ_low', 'DJ_close', 'DJ_Ajclose', 'DJ_volume']].copy()
stock_indices_data.columns = ['date_id', 'sp_open', 'sp_high', 'sp_low', 'sp_close', 'sp_ajclose', 'sp_volume',
                              'dj_open', 'dj_high', 'dj_low', 'dj_close', 'dj_ajclose', 'dj_volume']

etf_data = data[['Date', 'GDX_Open', 'GDX_High', 'GDX_Low', 'GDX_Close', 'GDX_Adj Close', 'GDX_Volume',
                 'USO_Open', 'USO_High', 'USO_Low', 'USO_Close', 'USO_Adj Close', 'USO_Volume']].copy()
etf_data.columns = ['date_id', 'gdx_open', 'gdx_high', 'gdx_low', 'gdx_close', 'gdx_adj_close', 'gdx_volume',
                    'uso_open', 'uso_high', 'uso_low', 'uso_close', 'uso_adj_close', 'uso_volume']

exchange_rates_data = data[['Date', 'EU_Price', 'EU_open', 'EU_high', 'EU_low', 'EU_Trend', 
                            'USDI_Price', 'USDI_Open', 'USDI_High', 'USDI_Low', 'USDI_Volume', 'USDI_Trend']].copy()
exchange_rates_data.columns = ['date_id', 'eu_price', 'eu_open', 'eu_high', 'eu_low', 'eu_trend', 
                               'usdi_price', 'usdi_open', 'usdi_high', 'usdi_low', 'usdi_volume', 'usdi_trend']

futures_data = data[['Date', 'OF_Price', 'OF_Open', 'OF_High', 'OF_Low', 'OF_Volume', 'OF_Trend', 
                     'SF_Price', 'SF_Open', 'SF_High', 'SF_Low', 'SF_Volume', 'SF_Trend']].copy()
futures_data.columns = ['date_id', 'of_price', 'of_open', 'of_high', 'of_low', 'of_volume', 'of_trend', 
                        'sf_price', 'sf_open', 'sf_high', 'sf_low', 'sf_volume', 'sf_trend']

other_metals_data = data[['Date', 'PLT_Price', 'PLT_Open', 'PLT_High', 'PLT_Low', 'PLT_Trend', 
                          'PLD_Price', 'PLD_Open', 'PLD_High', 'PLD_Low', 'PLD_Trend', 'RHO_PRICE']].copy()
other_metals_data.columns = ['date_id', 'plt_price', 'plt_open', 'plt_high', 'plt_low', 'plt_trend', 
                             'pld_price', 'pld_open', 'pld_high', 'pld_low', 'pld_trend', 'rho_price']

eg_usb_data = data[['Date', 'EG_open', 'EG_high', 'EG_low', 'EG_close', 'EG_Ajclose', 'EG_volume',
                    'USB_Price', 'USB_Open', 'USB_High', 'USB_Low', 'USB_Trend']].copy()
eg_usb_data.columns = ['date_id', 'eg_open', 'eg_high', 'eg_low', 'eg_close', 'eg_ajclose', 'eg_volume',
                       'usb_price', 'usb_open', 'usb_high', 'usb_low', 'usb_trend']

# Step 4: Insert data into MySQL database
def create_connection():
    return mysql.connector.connect(
        host="ur username", 
        user="root",
        password="ur password to mysql",
        database="ur database name"
        
    )

def insert_data(connection, table_name, dataframe):
    cursor = connection.cursor()
    cols = ", ".join(dataframe.columns)
    placeholders = ", ".join(["%s"] * len(dataframe.columns))
    sql_query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
    data = [tuple(row) for row in dataframe.to_numpy()]
    cursor.executemany(sql_query, data)
    connection.commit()
    cursor.close()

connection = create_connection()

try:
    insert_data(connection, 'gold_prices', gold_prices_data)
    insert_data(connection, 'stock_indices', stock_indices_data)
    insert_data(connection, 'etf_data', etf_data)
    insert_data(connection, 'exchange_rates', exchange_rates_data)
    insert_data(connection, 'futures_data', futures_data)
    insert_data(connection, 'other_metals', other_metals_data)
    insert_data(connection, 'eg_usb_data', eg_usb_data)
    print("Data inserted successfully into all tables.")
finally:
    connection.close()
