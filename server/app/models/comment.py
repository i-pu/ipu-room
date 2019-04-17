from .config import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.String, db.ForeignKey('rooms.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.Time)
