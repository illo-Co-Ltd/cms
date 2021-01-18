from .db_base import db


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    shorthand = db.Column(db.String(5, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    description = db.Column(db.String(200, 'utf8mb4_unicode_ci'))

    def __repr__(self):
        return f'<Project {self.name} | {self.shorthand}>'

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            shorthand=self.shorthand,
            description=self.description
        )
