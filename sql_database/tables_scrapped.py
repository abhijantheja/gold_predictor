import mysql.connector
import pandas as pd
import numpy as np

def create_connection():
    return mysql.connector.connect(
        host="ur username", 
        user="root",
        password="ur password to mysql",
        database="ur database name"
        
    )
# Read the new dataset
new_data = pd.read_csv("karan.csv")

# Clean up column names by stripping whitespace
new_data.columns = new_data.columns.str.strip()

# Define column mapping
column_mapping = {
    "Date": "date_id",
    "Adj Close": "adj_close",
    "Close": "close",
    "High": "high",
    "Low": "low",
    "Open": "open",
    "Volume": "volume",
    "SP_Ajclose": "sp_ajclose",
    "SP_close": "sp_close",
    "SP_high": "sp_high",
    "SP_low": "sp_low",
    "SP_open": "sp_open",
    "SP_volume": "sp_volume",
    "DJ_Ajclose": "dj_ajclose",
    "DJ_close": "dj_close",
    "DJ_high": "dj_high",
    "DJ_low": "dj_low",
    "DJ_Open": "dj_open",
    "DJ_volume": "dj_volume",
    "EG_Ajclose": "eg_ajclose",
    "EG_Close": "eg_close",
    "EG_high": "eg_high",
    "EG_Low": "eg_low",
    "EG_open": "eg_open",
    "EG_volume": "eg_volume",
    "EU_Price": "eu_price",
    "EU_high": "eu_high",
    "EU_low": "eu_low",
    "EU_Trend": "eu_trend",
    "EU_open": "eu_open",
    "OF_Price": "of_price",
    "OF_Trend": "of_trend",
    "OF_High": "of_high",
    "OF_Low": "of_low",
    "OF_Open": "of_open",
    "OF_Volume": "of_volume",
    "SF_Trend": "sf_trend",
    "SF_Price": "sf_price",
    "SF_High": "sf_high",
    "SF_Low": "sf_low",
    "SF_Open": "sf_open",
    "SF_Volume": "sf_volume",
    "USB_Price": "usb_price",
    "USB_Trend": "usb_trend",
    "USB_High": "usb_high",
    "USB_Low": "usb_low",
    "USB_Open": "usb_open",
    "PLT_Price": "plt_price",
    "PLT_High": "plt_high",
    "PLT_Low": "plt_low",
    "PLT_Open": "plt_open",
    "PLT_Trend": "plt_trend",
    "PLD_Trend": "pld_trend",
    "PLD_Price": "pld_price",
    "PLD_High": "pld_high",
    "PLD_Low": "pld_low",
    "PLD_Open": "pld_open",
    "RHO_PRICE": "rho_price",
    "USDI_Price": "usdi_price",
    "USDI_Trend": "usdi_trend",
    "USDI_High": "usdi_high",
    "USDI_Low": "usdi_low",
    "USDI_Open": "usdi_open",
    "USDI_Volume": "usdi_volume",
    "GDX_Adj Close": "gdx_adj_close",
    "GDX_Close": "gdx_close",
    "GDX_High": "gdx_high",
    "GDX_Low": "gdx_low",
    "GDX_Open": "gdx_open",
    "GDX_Volume": "gdx_volume",
    "USO_Adj Close": "uso_adj_close",
    "USO_Close": "uso_close",
    "USO_High": "uso_high",
    "USO_Low": "uso_low",
    "USO_Open": "uso_open",
    "USO_Volume": "uso_volume"
}

# Reorder columns based on column_mapping
new_data = new_data[list(column_mapping.keys())]

# Rename columns to match the database table
new_data.rename(columns=column_mapping, inplace=True)

# Clean and replace NaN with None, also strip any unexpected strings like 'Nan' with extra spaces
new_data = new_data.applymap(lambda x: None if isinstance(x, str) and x.strip().lower() == 'nan' else x)
new_data = new_data.where(pd.notnull(new_data), None)

# Connect to the database and append data
connection = create_connection()
cursor = connection.cursor()

# Insert data into the merged_gold_prediction table
for index, row in new_data.iterrows():
    sql_query = """
        INSERT INTO merged_gold_prediction ({columns})
        VALUES ({placeholders})
    """.format(
        columns=", ".join(new_data.columns),
        placeholders=", ".join(["%s"] * len(new_data.columns))
    )
    cursor.execute(sql_query, tuple(row))

connection.commit()
cursor.close()
connection.close()

print("Data added successfully!")
