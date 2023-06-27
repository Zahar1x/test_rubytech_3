import app
import config
from app import db
from app import models
with app.app.app_context():
    db.create_all()