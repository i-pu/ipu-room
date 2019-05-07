from .config import db, uuid4_for_str


class Plugin(db.Model):
    __tablename__ = 'plugins'

    name = db.Column(db.String(255), primary_key=True)
    description = db.Column(db.String(255))
    python_code = db.Column(db.Text)
    html_code = db.Column(db.Text)

    def __repr__(self):
        return 'Plugin(name: {}, description: {})' \
            .format(self.name, self.description)

    def __to_dict__(self):
        return {
            'plugin': {
                'name': self.name,
                'description': self.description
            }
        }
