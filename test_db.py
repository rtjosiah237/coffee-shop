from database import Database
import config

# Create database connection
db = Database(
    user=config.USER,
    database=config.DATABASE,
    password=config.PASSWORD,
    host=config.HOST,
    port=config.PORT
)

# Try to connect
db.connect()

# Try a simple query
result = db.run_query("SELECT version()")
print(f"PostgreSQL version: {result}")

# Close connection
db.close()
