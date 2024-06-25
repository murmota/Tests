from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StringRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
