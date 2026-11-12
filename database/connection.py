from pathlib import Path
from peewee import SqliteDatabase

# Define the base directory for the database file
BASE_DIR = Path(__file__).resolve().parent

# Define the path to the SQLite database file
DB_PATH = BASE_DIR / "chocan.db"

# Initialize the SQLite database connection with foreign key support
db = SqliteDatabase(
    DB_PATH,
    pragmas={
		'foreign_keys': 1,
		'journal_mode': 'wal',
		}
)