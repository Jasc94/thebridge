import pymysql

class MySQL:

    def __init__(self, IP_DNS, USER, PASSWORD, DB_NAME, PORT):
        self.IP_DNS = IP_DNS
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.DB_NAME = DB_NAME
        self.PORT = PORT
        self.SQL_ALCHEMY = 'mysql+pymysql://' + self.USER + ':' + self.PASSWORD + '@' + self.IP_DNS + ':' + str(self.PORT) + '/' + self.DB_NAME

    # ### To connect with the database
    def connect(self):
        # Open database connection
        self.db = pymysql.connect(host = self.IP_DNS,
                                  user = self.USER,
                                  password = self.PASSWORD,
                                  database = self.DB_NAME,
                                  port = self.PORT)

        # Create a cursor object using cursor method
        self.cursor = self.db.cursor()
        print("Connected to MySQL server [" + self.DB_NAME + "]")
        return self.db

    # ### To close the database
    def close(self):
        # Disconnect from server
        self.db.close()
        print("Close connection with MySQL server [" + self.DB_NAME + "]")

    # ### To execute SQL commands
    def execute_interactive_sql(self, sql, delete = False):
        ''' NO SELECT '''

        result = 0

        try:
            # Execute SQL command
            self.cursor.execute(sql)

            # Commit your changes in the database
            self.db.commit()
            print("Executed \n\n" + str(sql) + "\n\n succesfully")
            result = 1
        
        except Exception as error:
            print(error)
            # Rollback in case there is an error
            self.db.rollback()

        return result

    # ### To execute SQL queries
    def execute_get_sql(self, sql):
        '''SELECT'''
        
        results = None
        print("Executing:\n", sql)

        try:
            # Execute the SQL command
            self.cursor.execute(sql)

            # Fetch all the rows in a list of lists and save it in results
            results = self.cursor.fetchall()

        except Exception as error:
            print(error)
            print("Error: unable to fetch the data")

        # return the list of lists
        return results

    # ### To insert values in the daily intakes dataframe
    def generate_insert_into_dailyintakes_sql(self, to_insert):
        '''
        This must be modified according to the table structure
        '''

        gender, age, url = to_insert

        sql = """INSERT INTO dailyintakes
                (GENDER, AGE, URL)
                VALUES
                ('""" + gender + """', '""" + age + """', '""" + url + """')"""

        sql = sql.replace("\n", "").replace("            ", " ")

        #self.cursor.execute(sql, to_insert)

        return sql


    # ### To insert values in the dataframe
    def generate_insert_into_resources_sql(self, to_insert):
        '''
        This must be modified according to the table structure
        '''

        food, total_emissions, land_1000kcal, land_kg, land_100gprotein, water_1000kcal, water_kg, water_100g_protein, origin = to_insert

        sql = """INSERT INTO resources
                (FOOD, TOTAL_EMISSIONS, LAND_USE_PER_1000KCAL, LAND_USE_PER_KG, LAND_USE_PER_100G_PROTEIN, FRESHWATER_WITHDRAWLS_PER_1000KCAL, FRESHWATER_WITHDRAWLS_PER_KG, FRESHWATER_WITHDRAWLS_PER_100G_PROTEIN, ORIGIN)
                VALUES
                ('""" + food + """', '""" + total_emissions + """', '""" + land_1000kcal + """',
                '""" + land_kg + """', '""" + land_100gprotein + """', '""" + water_1000kcal + """',
                '""" + water_kg + """', '""" + water_100g_protein + """', '""" + origin + """')"""

        sql = sql.replace("\n", "").replace("            ", " ")

        #self.cursor.execute(sql, to_insert)

        return sql