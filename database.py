import pg8000.native as pg

class Database:
    def __init__(self, user, database, password, host, port):
        self.user = user
        self.database = database
        self.password = password
        self.host = host
        self.port = port
        self.con = None

    def connect(self):
        try:
            self.con = pg.Connection(
                user=self.user,
                database=self.database,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connected to database successfully!")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise  # Stop the program if we can't connect

    def close(self):
        if self.con:
            self.con.close()
            print("Database connection closed.")

    def begin(self):
        self.con.run("BEGIN")
    
    def commit(self):
        self.con.run("COMMIT")
    
    def rollback(self):
        self.con.run("ROLLBACK")
    
    def run_query(self, query, **params):
        """Run a SQL query with parameters"""
        return self.con.run(query, **params)


