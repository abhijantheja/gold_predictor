import mysql.connector
from mysql.connector import Error



 
host="ur username" 
user="root"
password="ur password to mysql"
database="ur database name"



# Query to create tables
create_tables_query = """
CREATE TABLE IF NOT EXISTS gold_prices (
    date_id DATE NOT NULL PRIMARY KEY,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    adj_close FLOAT,
    volume BIGINT
);

CREATE TABLE IF NOT EXISTS stock_indices (
    date_id DATE NOT NULL PRIMARY KEY,
    sp_open FLOAT,
    sp_high FLOAT,
    sp_low FLOAT,
    sp_close FLOAT,
    sp_ajclose FLOAT,
    sp_volume BIGINT,
    dj_open FLOAT,
    dj_high FLOAT,
    dj_low FLOAT,
    dj_close FLOAT,
    dj_ajclose FLOAT,
    dj_volume BIGINT
);

CREATE TABLE IF NOT EXISTS etf_data (
    date_id DATE NOT NULL PRIMARY KEY,
    gdx_open FLOAT,
    gdx_high FLOAT,
    gdx_low FLOAT,
    gdx_close FLOAT,
    gdx_adj_close FLOAT,
    gdx_volume BIGINT,
    uso_open FLOAT,
    uso_high FLOAT,
    uso_low FLOAT,
    uso_close FLOAT,
    uso_adj_close FLOAT,
    uso_volume BIGINT
);

CREATE TABLE IF NOT EXISTS exchange_rates (
    date_id DATE NOT NULL PRIMARY KEY,
    eu_price FLOAT,
    eu_open FLOAT,
    eu_high FLOAT,
    eu_low FLOAT,
    eu_trend VARCHAR(10),
    usdi_price FLOAT,
    usdi_open FLOAT,
    usdi_high FLOAT,
    usdi_low FLOAT,
    usdi_volume BIGINT,
    usdi_trend VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS futures_data (
    date_id DATE NOT NULL PRIMARY KEY,
    of_price FLOAT,
    of_open FLOAT,
    of_high FLOAT,
    of_low FLOAT,
    of_volume BIGINT,
    of_trend VARCHAR(10),
    sf_price FLOAT,
    sf_open FLOAT,
    sf_high FLOAT,
    sf_low FLOAT,
    sf_volume BIGINT,
    sf_trend VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS other_metals (
    date_id DATE NOT NULL PRIMARY KEY,
    plt_price FLOAT,
    plt_open FLOAT,
    plt_high FLOAT,
    plt_low FLOAT,
    plt_trend VARCHAR(10),
    pld_price FLOAT,
    pld_open FLOAT,
    pld_high FLOAT,
    pld_low FLOAT,
    pld_trend VARCHAR(10),
    rho_price FLOAT
);

CREATE TABLE IF NOT EXISTS eg_usb_data (
    date_id DATE NOT NULL PRIMARY KEY,
    eg_open FLOAT,
    eg_high FLOAT,
    eg_low FLOAT,
    eg_close FLOAT,
    eg_ajclose FLOAT,
    eg_volume BIGINT,
    usb_price FLOAT,
    usb_open FLOAT,
    usb_high FLOAT,
    usb_low FLOAT,
    usb_trend VARCHAR(10)
);
"""

# Connect to the database and execute the query
try:
    connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    # Execute queries and handle multi=True properly
    if connection.is_connected():
      cursor = connection.cursor()
      for result in cursor.execute(create_tables_query, multi=True):
        try:
            print(f"Running query: {result.statement}")
            print(f"Affected rows: {result.rowcount}")
        except Exception as e:
            print(f"Error processing query: {e}")
      connection.commit()
      print("Tables created successfully.")


except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection closed.")
