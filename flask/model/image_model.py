from .db_base import db, env


class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    if env == 'development':
        cell_id = db.Column(db.ForeignKey('cell.id', onupdate='CASCADE'), index=True)
        path = db.Column(db.String(260, 'utf8mb4_unicode_ci'), unique=True)
        device_id = db.Column(db.ForeignKey('device.id', onupdate='CASCADE'), index=True)
        created = db.Column(db.DateTime)
        created_by_id = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)
        label = db.Column(db.String(20, 'utf8mb4_unicode_ci'))
        offset_x = db.Column(db.Integer)
        offset_y = db.Column(db.Integer)
        offset_z = db.Column(db.Integer)
        pos_x = db.Column(db.Integer)
        pos_y = db.Column(db.Integer)
        pos_z = db.Column(db.Integer)
    else:
        cell_id = db.Column(db.ForeignKey('cell.id', onupdate='CASCADE'), nullable=False, index=True)
        path = db.Column(db.String(260, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
        device_id = db.Column(db.ForeignKey('device.id', onupdate='CASCADE'), nullable=False, index=True)
        created = db.Column(db.DateTime, nullable=False)
        created_by_id = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)
        label = db.Column(db.String(20, 'utf8mb4_unicode_ci'))
        offset_x = db.Column(db.Integer, nullable=False)
        offset_y = db.Column(db.Integer, nullable=False)
        offset_z = db.Column(db.Integer, nullable=False)
        pos_x = db.Column(db.Integer, nullable=False)
        pos_y = db.Column(db.Integer, nullable=False)
        pos_z = db.Column(db.Integer, nullable=False)

    created_by = db.relationship('User', primaryjoin='Image.created_by_id == User.id', backref='images')
    device = db.relationship('Device', primaryjoin='Image.device_id == Device.id', backref='images')
    cell = db.relationship('Cell', primaryjoin='Image.cell_id == Cell.id', backref='images')

    def __repr__(self):
        return f'<Image {self.project} | {self.cell_id} | {self.path}>'

    def to_dict(self):
        return dict(
            id=self.id,
            cell=self.cell,
            path=self.path,
            device=self.device,
            created=self.created,
            created_by=self.created_by,
            label=self.label,
            offset_x=self.offset_x,
            offset_y=self.offset_y,
            offset_z=self.offset_z,
            pos_x=self.pos_x,
            pos_y=self.pos_y,
            pos_z=self.pos_z
        )
