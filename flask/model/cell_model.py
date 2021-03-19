from .db_base import db, env


class Cell(db.Model):
    __tablename__ = 'cell'

    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.ForeignKey('project.id', onupdate='CASCADE'), index=True)
    type = db.Column(db.String(16, 'utf8mb4_unicode_ci'))
    detail = db.Column(db.String(16, 'utf8mb4_unicode_ci'))
    if env == 'development':
        name = db.Column(db.String(16, 'utf8mb4_unicode_ci'), unique=True)
    else:
        name = db.Column(db.String(16, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    description = db.Column(db.String(200, 'utf8mb4_unicode_ci'))

    r_project = db.relationship('Project', primaryjoin='Cell.project == Project.id',
                                backref='cell_project_project_id')

    def __repr__(self):
        return f'<Cell {self.project} | {self.type} | {self.detail} | {self.name}>'

    def to_dict(self):
        return dict(
            id=self.id,
            project=self.project,
            type=self.type,
            detail=self.detail,
            name=self.name,
            description=self.description
        )
