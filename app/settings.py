from os import getenv

# Logging
LOG_LEVEL = int(getenv("LOG_LEVEL", "20"))
SERVICE_NAME = "fast-api-squadmakers"

# Third Party API
API_CHUCKNORRIS_URL = "https://api.chucknorris.io/"
API_DADJOKE_URL = "https://icanhazdadjoke.com/"

# Database connection string
DATABASE_URL = getenv('DATABASE_URL', "postgresql://postgres:postgres@localhost:5432/postgres")
