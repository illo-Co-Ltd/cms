# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Device(db.Model):
    __tablename__ = 'device'
    __table_args__ = (
        db.UniqueConstraint('serial', name='device_serial_uindex'),
        {'mysql_collate': 'utf8mb4_unicode_ci'}
    )

    _id = db.Column(db.INTEGER, primary_key=True, nullable=False, autoincrement=True, )
    model = db.Column(db.VARCHAR(16), nullable=False)
    serial = db.Column(db.VARCHAR(20), nullable=False)
    owner = db.Column(db.INTEGER, ForeignKey('user.id', onupdate='CASCADE',ondelete='CASCADE'), nullable=False)
    created = db.Column(db.TIMESTAMP)
    created_by = db.Column(db.INTEGER, ForeignKey('user.id',onupdate='CASCADE',ondelete='CASCADE'))
    last_edited = db.Column(db.TIMESTAMP)
    edited_by = db.Column(db.INTEGER, ForeignKey('user.id',onupdate='CASCADE',ondelete='CASCADE'))
    is_deleted = db.Column(db.BOOLEAN)

    def to_dict(self):
        return dict(_id=self._id,
                    model=self.model,
                    serial=self.serial,
                    owner=self.owner,
                    created=self.created,
                    created_by=self.created_by,
                    last_edited=self.last_edited,
                    edited_by=self.edited_by,
                    is_deleted=self.is_deleted)
