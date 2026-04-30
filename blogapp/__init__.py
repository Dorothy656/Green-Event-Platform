
from blogapp.config import Config
from flask import Flask
from blogapp.config import Config
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
# migrate = Migrate(app, db)



# Make sure log exists
if not os.path.exists(app.config['LOG_DIR']):
    os.mkdir(app.config['LOG_DIR'])

# set lof formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a file processor
file_handler = RotatingFileHandler(
    os.path.join(app.config['LOG_DIR'], app.config['LOG_FILE']),
    maxBytes=app.config['LOG_MAX_BYTES'],
    backupCount=app.config['LOG_BACKUP_COUNT']
)
file_handler.setFormatter(formatter)
file_handler.setLevel(app.config['LOG_LEVEL'])

# Create console processor
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.ERROR)

# Obtain the application log recorder
logger = logging.getLogger(__name__)
logger.setLevel(app.config['LOG_LEVEL'])
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Record the application startup log
logger.info('Application started')

from blogapp import routes, models