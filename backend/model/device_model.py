from .db_base import db


class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(16, 'utf8mb4_unicode_ci'), nullable=False)
    serial = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    owner = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), nullable=False, index=True)
    created = db.Column(db.DateTime)
    created_by = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)
    last_edited = db.Column(db.DateTime)
    edited_by = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)
    is_deleted = db.Column(db.Integer)

    r_created_by = db.relationship('User', primaryjoin='Device.created_by == User.id', backref='user_id_device_create_by')
    r_edited_by = db.relationship('User', primaryjoin='Device.edited_by == User.id', backref='user_id_device_edited_by')
    r_owner = db.relationship('User', primaryjoin='Device.owner == User.id', backref='user_id_device_owner')

    def __repr__(self):
        return f'<Device {self.model} | {self.serial}>'

    def to_dict(self):
        return dict(
            id=self.id,
            model=self.model,
            serial=self.serial,
            owner=self.owner,
            created=self.created,
            created_by=self.created_by,
            last_edited=self.last_edited,
            edited_by=self.edited_by,
            is_deleted=self.is_deleted
        )
