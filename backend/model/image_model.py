# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Image(db.Model):
    __tablename__ = 'image'
    __table_args__ = (
        db.UniqueConstraint('path', name='image_path_uindex'),
        {'mysql_collate': 'utf8mb4_unicode_ci'}
    )

    _id = db.Column(db.INTEGER, primary_key=True, nullable=False, autoincrement=True)
    project = db.Column(db.VARCHAR(20), nullable=False)
    target = db.Column(db.VARCHAR(20), nullable=False)
    path = db.Column(db.VARCHAR(260), nullable=False)
    device = db.Column(db.INTEGER, ForeignKey('device.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)
    created_by = db.Column(db.INTEGER, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    label = db.Column(db.VARCHAR(20))
    offset_x = db.Column(db.INTEGER, nullable=False)
    offset_y = db.Column(db.INTEGER, nullable=False)
    offset_z = db.Column(db.INTEGER, nullable=False)
    pos_x = db.Column(db.INTEGER, nullable=False)
    pos_y = db.Column(db.INTEGER, nullable=False)
    pos_z = db.Column(db.INTEGER, nullable=False)

    def to_dict(self):
        return dict(_id=self._id,
                    project=self.project,
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
                    pos_z=self.pos_z)
