from .config import db, uuid4_for_str


class Plugin(db.Model):
    __tablename__ = 'plugins'

    id = db.Column(db.String(36), primary_key=True, default=uuid4_for_str)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    python = db.Column(db.Text)
    html = db.Column(db.Text)

    def __repr__(self):
        return 'Plugin(id: {}, name: {}, description: {})' \
            .format(self.id, self.name, self.description)

    def __to_dict__(self):
        return {
            'plugin': {
                'id': self.id,
                'name': self.name,
                'description': self.description
            }
        }
