from .config import db


class Plugin(db.Model):
    __tablename__ = 'plugins'
    # todo: room と relation を持つようにする
    # todo: 名前が一意になるべきかも知れないので name が primary key でもいいかも

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return 'id: {}, name: {}' \
            .format(self.id, self.name)

    def __to_dict__(self):
        return {
            'plugin': {
                'id': self.id,
                'name': self.name,
                'user_id': self.user_id,
            }
        }
