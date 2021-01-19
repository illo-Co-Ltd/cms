from .db_base import db


class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.ForeignKey('target.id', onupdate='CASCADE'), nullable=False, index=True)
    path = db.Column(db.String(260, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    device = db.Column(db.ForeignKey('device.id', onupdate='CASCADE'), nullable=False, index=True)
    created = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)
    label = db.Column(db.String(20, 'utf8mb4_unicode_ci'))
    offset_x = db.Column(db.Integer, nullable=False)
    offset_y = db.Column(db.Integer, nullable=False)
    offset_z = db.Column(db.Integer, nullable=False)
    pos_x = db.Column(db.Integer, nullable=False)
    pos_y = db.Column(db.Integer, nullable=False)
    pos_z = db.Column(db.Integer, nullable=False)

    r_created_by = db.relationship('User', primaryjoin='Image.created_by == User.id', backref='image_create_by_user_id')
    r_device = db.relationship('Device', primaryjoin='Image.device == Device.id', backref='image_device_device_id')
    r_target = db.relationship('Target', primaryjoin='Image.target == Target.id', backref='image_target_target_id')

    def __repr__(self):
        return f'<Image {self.project} | {self.target} | {self.path}>'

    def to_dict(self):
        return dict(
            id=self.id,
            target=self.target,
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
