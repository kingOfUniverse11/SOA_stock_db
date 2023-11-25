import psycopg2

class PostgresAPI:
    def __init__(self):
        awsConnectionParamaters = {
            'dbname': 'stock_data',
            'user':'postgres',
            'password':'nazim4471',
            'host':'my-db-instance.cxjzjls8ya5o.us-east-2.rds.amazonaws.com',
            'port':'5432' }
        self.connection_params = awsConnectionParamaters

    def fetchDataFromDatabase(self, query):
        conn = psycopg2.connect(**self.connection_params)
        cursor = conn.cursor()

        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()
        return data
    
