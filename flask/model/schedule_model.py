from .db_base import db


class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16, 'utf8mb4_unicode_ci'), unique=True)
    start_x = db.Column(db.Integer)
    start_y = db.Column(db.Integer)
    end_x = db.Column(db.Integer)
    end_y = db.Column(db.Integer)
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    interval = db.Column(db.Interval)
    last_executed = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    created_by_id = db.Column(db.ForeignKey('user.id', onupdate='CASCADE'), index=True)

    created_by = db.relationship('User', primaryjoin='Schedule.created_by_id == User.id', backref='schedules')

    def __repr__(self):
        return f'<Schedule{self.name} | {self.start_datetime} ~ {self.end_datetime} | {self.interval}>'

    def to_dict(self):
        return dict(
            id=self.id,
            start_x=self.start_x,
            start_y=self.start_y,
            end_x=self.end_x,
            end_y=self.end_y,
            name=self.name,
            start_datetime=self.start_datetime,
            end_datetime=self.end_datetime,
            interval=self.interval,
            last_executed=self.last_executed,
            created=self.created,
            created_by=self.created_by
        )
