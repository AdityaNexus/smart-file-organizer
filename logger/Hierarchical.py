import logging

# Configure the root logger
logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")

# Create child loggers
db_logger = logging.getLogger("app.database")
ui_logger = logging.getLogger("app.user_interface")

def connect_db():
    db_logger.info("Connecting to PostgreSQL...")
    db_logger.error("Connection timeout.")

def render_screen():
    ui_logger.info("Drawing main menu.")

connect_db()
render_screen()