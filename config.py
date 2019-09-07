# Create dummy secrey key so we can use sessions
SECRET_KEY = 'PUT_YOUR_RANDOM_KEY_HERE'

# Create in-memory database
DATABASE_FILE = 'YOUR_DB_NAME.sqlite'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
SQLALCHEMY_ECHO = True