import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()#engine_options={"init_command": "SET SESSION time_zone='+09:00'"})
env = os.getenv('FLASK_ENV')
