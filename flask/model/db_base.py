import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
env = os.getenv('FLASK_ENV')
