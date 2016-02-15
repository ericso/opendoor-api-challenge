from server.application import create_app
from server.application import db
from config import BaseConfig


db.create_all(app=create_app(BaseConfig))
