import pandas as pd
import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="ur username", 
        user="root",
        password="ur password to mysql",
        database="ur database name"
        
    )

def fetch_table_data(connection, table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, connection)

def merge_tables():
    connection = create_connection()
    try:
        # Fetch data from all tables
        gold_prices = fetch_table_data(connection, 'gold_prices')
        stock_indices = fetch_table_data(connection, 'stock_indices')
        etf_data = fetch_table_data(connection, 'etf_data')
        exchange_rates = fetch_table_data(connection, 'exchange_rates')
        futures_data = fetch_table_data(connection, 'futures_data')
        other_metals = fetch_table_data(connection, 'other_metals')
        eg_usb_data = fetch_table_data(connection, 'eg_usb_data')

        # Merge all tables on date_id
        merged_data = gold_prices.merge(
            stock_indices, on='date_id', how='left'
        ).merge(
            etf_data, on='date_id', how='left'
        ).merge(
            exchange_rates, on='date_id', how='left'
        ).merge(
            futures_data, on='date_id', how='left'
        ).merge(
            other_metals, on='date_id', how='left'
        ).merge(
            eg_usb_data, on='date_id', how='left'
        )

        return merged_data

    finally:
        connection.close()

def create_merged_table(connection):
    cursor = connection.cursor()
    
    # Create the merged table with all columns
    create_table_query = """
    CREATE TABLE IF NOT EXISTS merged_gold_prediction (
        date_id DATE PRIMARY KEY,
        
        -- Gold Prices
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        adj_close FLOAT,
        volume BIGINT,
        
        -- Stock Indices
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
        dj_volume BIGINT,
        
        -- ETF Data
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
        uso_volume BIGINT,
        
        -- Exchange Rates
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
        usdi_trend VARCHAR(10),
        
        -- Futures Data
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
        sf_trend VARCHAR(10),
        
        -- Other Metals
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
        rho_price FLOAT,
        
        -- EG and USB Data
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
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()

def insert_merged_data(connection, merged_data):
    cursor = connection.cursor()
    
    # Prepare columns and placeholders for the INSERT query
    columns = merged_data.columns.tolist()
    placeholders = ', '.join(['%s'] * len(columns))
    
    # Create the INSERT query
    insert_query = f"""
    INSERT INTO merged_gold_prediction ({', '.join(columns)})
    VALUES ({placeholders})
    """
    
    # Convert DataFrame to list of tuples for insertion
    values = [tuple(row) for row in merged_data.values]
    
    # Execute the insert
    cursor.executemany(insert_query, values)
    connection.commit()
    cursor.close()

def main():
    # Create connection
    connection = create_connection()
    
    try:
        # Create the merged table
        print("Creating merged table structure...")
        create_merged_table(connection)
        
        # Merge data from all tables
        print("Merging data from all tables...")
        merged_data = merge_tables()
        
        # Insert merged data into the new table
        print("Inserting merged data...")
        insert_merged_data(connection, merged_data)
        
        print("Data successfully merged and stored in merged_gold_prediction table!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()