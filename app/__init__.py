from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
with app.app_context():
    db.create_all()

