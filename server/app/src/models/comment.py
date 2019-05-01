from .config import db, uuid4_for_str


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.String(36), primary_key=True, default=uuid4_for_str)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'))
    room_id = db.Column(db.String(36), db.ForeignKey('rooms.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.Time)

    room = db.relationship('Room', back_populates='comments')
    user = db.relationship('User', back_populates='comments')

    def __init__(self, user_id, room_id, content, created_at):
        self.user_id = user_id
        self.room_id = room_id
        self.content = content
        self.created_at = created_at

    def __to_dict__(self):
        return {
            'comment': {
                'id': self.id,
                'user_id': self.user_id,
                'room_id': self.room_id,
                'content': self.content,
                'created_at': self.created_at,
            }
        }
