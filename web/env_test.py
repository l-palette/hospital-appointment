import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
db_url = os.getenv("DATABASE_URL")
print(type(db_url))