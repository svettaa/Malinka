from app import db


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10), nullable=False, unique=True)
    surname = db.Column(db.String(20), nullable=False)
    fist_name = db.Column(db.String(20), nullable=False)
    second_name = db.Column(db.String(20))
    email = db.Column(db.String(30))
    is_male = db.Column(db.Boolean, nullable=False)
    photo = db.Column(db.LargeBinary)

    favourite_masters = db.relationship("Master", secondary='favourite_master', back_populates="favourite_clients")

    def __repr__(self):
        return f'{self.surname} {self.fist_name} {self.second_name}, +38{self.phone}'


class Master(db.Model):
    __tablename__ = 'master'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10), nullable=False, unique=True)
    surname = db.Column(db.String(20), nullable=False)
    fist_name = db.Column(db.String(20), nullable=False)
    second_name = db.Column(db.String(20))
    email = db.Column(db.String(30))
    even_schedule = db.Column(db.Boolean, nullable=False)
    is_hired = db.Column(db.Boolean, nullable=False)
    photo = db.Column(db.LargeBinary)

    favourite_clients = db.relationship("Client", secondary='favourite_master', back_populates="favourite_masters")
    schedule_changes = db.relationship("ScheduleChange", back_populates="master")

    def __repr__(self):
        return f'{self.surname} {self.fist_name} {self.second_name}, +38{self.phone}'


class ScheduleChange(db.Model):
    __tablename__ = 'schedule_change'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_working = db.Column(db.Boolean)

    master_id = db.Column(db.Integer,
                          db.ForeignKey('master.id', onupdate='RESTRICT', ondelete='RESTRICT'), nullable=False)
    master = db.relationship("Master", back_populates="schedule_changes")

    def __repr__(self):
        return f'{self.master}, ' \
               f'{self.start_time.strftime("%h:%m")} - {self.end_time.strftime("%h:%m")}'


db.Table('favourite_master',
         db.Column('client_id', db.Integer,
                   db.ForeignKey('client.id', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True),
         db.Column('master_id', db.Integer,
                   db.ForeignKey('master.id', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True)
         )
