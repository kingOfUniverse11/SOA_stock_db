import psycopg2
import pandas as pd
import os

# Connect to PostgreSQL (replace these values with your actual database credentials)
# connectionToMyLocal = psycopg2.connect(
#     dbname="Stocks_db",
#     user="postgres",
#     password="admin",
#     host="localhost",
#     port="5432"
# )


connectionToAWS = psycopg2.connect(
    dbname="stock_data",
    user="postgres",
    password="nazim4471",
    host="my-db-instance.cxjzjls8ya5o.us-east-2.rds.amazonaws.com",
    port='5432'
)

# conn = connectionToMyLocal
conn = connectionToAWS

# Folder containing CSV files
folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "SP500_Historical_Data")

# Establish connection to the PostgreSQL database
cursor = conn.cursor()

# Function to create tables and insert data
def create_tables_and_insert_data():
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            table_name = os.path.splitext(filename)[0]  # Extract table name from file name (without extension)
            table_name = table_name.upper()
            file_path = os.path.join(folder_path, filename)
          
            # Read CSV file into a DataFrame
            df = pd.read_csv(file_path)
            # print(df['GICS Sector'].iloc[0])
            
            # Create table with the same structure as DataFrame
            stockTableQuery = f"CREATE TABLE IF NOT EXISTS \"STOCKS\" (STOCK_SYMBOL varchar(10) NOT NULL , STOCK_GICS_SECTOR varchar(255) NOT NULL ,PRIMARY KEY(STOCK_SYMBOL));"
            cursor.execute(stockTableQuery)
            insertIntoStocksQuery = f"INSERT INTO \"STOCKS\" VALUES ('{table_name}', '{df['GICS Sector'].iloc[0]}') ON CONFLICT DO NOTHING;"
            cursor.execute(insertIntoStocksQuery)
            create_table_query = f"CREATE TABLE IF NOT EXISTS \"{table_name}\" (DATA_ID SERIAL PRIMARY KEY, TRADE_DATE DATE,OPEN_PRICE float(20), CLOSING_PRICE float(20), DAY_HIGH float(20), DAY_LOW float(20), ADJ_CLOSE_PRICE float(20), VOLUME_TRADED int );"
            cursor.execute(create_table_query)

            column_mapping = {
            'Date': 'TRADE_DATE',
            'Open': 'OPEN_PRICE',
            'Close': 'CLOSING_PRICE',
            'High': 'DAY_HIGH',
            'Low': 'DAY_LOW',
            'Adj Close': 'ADJ_CLOSE_PRICE',
            'Volume': 'VOLUME_TRADED',}

            # Insert data into the table
            for index, row in df.iterrows():
                mapped_values = [row[column] for column in column_mapping.keys()]
                table_columns = [column_mapping[column] for column in column_mapping.keys()]    
                insert_query = f"INSERT INTO \"{table_name}\" ({', '.join(table_columns)}) VALUES ({', '.join(['%s'] * len(mapped_values))}) ON CONFLICT DO NOTHING;"
                cursor.execute(insert_query, mapped_values)

    
    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()

# Call function to create tables and insert data
create_tables_and_insert_data()