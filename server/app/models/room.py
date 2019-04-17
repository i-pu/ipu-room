from .config import db


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
