from flask_login import UserMixin
from sqlalchemy import exists

from app import db


class Client(UserMixin, db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10), nullable=False, unique=True)
    surname = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    second_name = db.Column(db.String(20))
    email = db.Column(db.String(30))
    is_male = db.Column(db.Boolean, nullable=False)
    photo = db.Column(db.LargeBinary)

    favourite_masters = db.relationship(
        "Master", secondary='favourite_master', back_populates="favourite_clients")
    favourite_procedures = db.relationship(
        "Procedure", secondary='favourite_procedure', back_populates="favourite_clients")
    appointments = db.relationship(
        "Appointment", back_populates="client")
    master_data = db.relationship(
        "Master", back_populates="data")

    def is_master(self):
        return db.session.query(exists().where(Master.id == self.id)).scalar()

    def is_admin(self):
        return db.session.query(exists().where(AdminUser.id == self.id)).scalar()

    def __repr__(self):
        return f'{self.surname} {self.first_name} {self.second_name}, +38{self.phone}'


class Master(db.Model):
    __tablename__ = 'master'
    even_schedule = db.Column(db.Boolean, nullable=False)
    is_hired = db.Column(db.Boolean, nullable=False)

    id = db.Column(
        db.Integer, db.ForeignKey('client.id', onupdate='RESTRICT', ondelete='RESTRICT'),
        nullable=False, primary_key=True)

    favourite_clients = db.relationship(
        "Client", secondary='favourite_master', back_populates="favourite_masters")
    procedures = db.relationship(
        "MasterProcedure", back_populates="master")
    data = db.relationship(
        "Client", back_populates="master_data")
    schedule_changes = db.relationship(
        "ScheduleChange", back_populates="master")
    appointments = db.relationship(
        "Appointment", back_populates="master")

    def __repr__(self):
        return f'{self.data.surname} {self.data.first_name} {self.data.second_name}, +38{self.data.phone}'


class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)


class ScheduleChange(db.Model):
    __tablename__ = 'schedule_change'
    id = db.Column(db.Integer, primary_key=True)
    change_start = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    change_end = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    is_working = db.Column(db.Boolean)

    master_id = db.Column(
        db.Integer, db.ForeignKey('master.id', onupdate='RESTRICT', ondelete='RESTRICT'), nullable=False)

    master = db.relationship(
        "Master", back_populates="schedule_changes")

    __table_args__ = (
        db.CheckConstraint('NOT exists_intersecting_schedule_change'
                           '    (id, master_id, change_start, change_end)', name='change_intersects'),
        db.CheckConstraint('change_start < change_end', name='change_start_less_end'),
    )

    def __repr__(self):
        return f'{self.master}, ' \
               f'{self.start_time.strftime("%h:%m")} - {self.end_time.strftime("%h:%m")}'


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False, unique=True)

    procedures = db.relationship("Procedure", back_populates="category")

    def __repr__(self):
        return f'{self.name}'


class Procedure(db.Model):
    __tablename__ = 'procedure'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False, unique=True)
    price_min = db.Column(db.Numeric(precision=14, scale=2), nullable=False)
    price_max = db.Column(db.Numeric(precision=14, scale=2))
    info = db.Column(db.String(300))

    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id', onupdate='RESTRICT', ondelete='RESTRICT'), nullable=False)

    category = db.relationship(
        "Category", back_populates="procedures")
    favourite_clients = db.relationship(
        "Client", secondary='favourite_procedure', back_populates="favourite_procedures")
    masters = db.relationship(
        "MasterProcedure", back_populates="procedure")
    appointments = db.relationship(
        "Appointment", back_populates="procedure")

    __table_args__ = (
        db.CheckConstraint('price_max IS NULL OR price_max > price_min', name='price_max_greater_min'),
    )

    def __repr__(self):
        return f'{self.name}'


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    appoint_start = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    appoint_end = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    preferences = db.Column(db.String(300))
    status = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Numeric(precision=14, scale=2), nullable=False)

    client_id = db.Column(
        db.Integer, db.ForeignKey('client.id', onupdate='RESTRICT', ondelete='RESTRICT'), nullable=False)
    master_id = db.Column(
        db.Integer, db.ForeignKey('master.id', onupdate='RESTRICT', ondelete='RESTRICT'), nullable=False)
    procedure_id = db.Column(
        db.Integer, db.ForeignKey('procedure.id', onupdate='RESTRICT', ondelete='RESTRICT'), nullable=False)

    client = db.relationship(
        "Client", back_populates="appointments")
    master = db.relationship(
        "Master", back_populates="appointments")
    procedure = db.relationship(
        "Procedure", back_populates="appointments")
    paints = db.relationship(
        "AppointmentPaint", back_populates="appointment")

    __table_args__ = (
        db.UniqueConstraint('appoint_start', 'client_id', name='unique_client_time'),
        db.UniqueConstraint('appoint_start', 'master_id', name='unique_master_time')
    )

    def __repr__(self):
        return f'{self.appoint_start} - {self.master} - {self.procedure} - {self.client}'


class Paint(db.Model):
    __tablename__ = 'paint'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(75), nullable=False)
    left_ml = db.Column(db.Integer, nullable=False, default=0)

    paint_supplies = db.relationship(
        "PaintSupply", back_populates="paint")
    appointments = db.relationship(
        "AppointmentPaint", back_populates="paint")

    def __repr__(self):
        return f'{self.code} - {self.name}'


class PaintSupply(db.Model):
    __tablename__ = 'paint_supply'
    id = db.Column(db.Integer, primary_key=True)
    supply_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    paint_id = db.Column(
        db.Integer, db.ForeignKey('paint.id', onupdate='RESTRICT', ondelete='RESTRICT'), nullable=False)

    paint = db.relationship(
        "Paint", back_populates="paint_supplies")

    def __repr__(self):
        return f'{self.supply_date} - {self.paint}'


class AppointmentPaint(db.Model):
    __tablename__ = 'appointment_paint'
    volume_ml = db.Column(db.Integer, nullable=False)

    paint_id = db.Column(
        db.Integer, db.ForeignKey('paint.id', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True)
    appointment_id = db.Column(
        db.Integer, db.ForeignKey('appointment.id', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True)

    paint = db.relationship(
        "Paint", back_populates="appointments")
    appointment = db.relationship(
        "Appointment", back_populates="paints")

    def __repr__(self):
        return f'{self.volume_ml}ml {self.paint} {self.appointment}'


db.Table('favourite_master',
         db.Column('client_id', db.Integer,
                   db.ForeignKey('client.id', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True),
         db.Column('master_id', db.Integer,
                   db.ForeignKey('master.id', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True)
         )

db.Table('favourite_procedure',
         db.Column('client_id', db.Integer,
                   db.ForeignKey('client.id', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True),
         db.Column('procedure_id', db.Integer,
                   db.ForeignKey('procedure.id', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True)
         )


class MasterProcedure(db.Model):
    __tablename__ = 'master_procedure'
    duration = db.Column(db.Integer, nullable=False)

    master_id = db.Column(
        db.Integer, db.ForeignKey('master.id', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True)
    procedure_id = db.Column(
        db.Integer, db.ForeignKey('procedure.id', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True)

    master = db.relationship(
        "Master", back_populates="procedures")
    procedure = db.relationship(
        "Procedure", back_populates="masters")

    def __repr__(self):
        return f'{self.master} - {self.procedure}: {self.duration}min'

# exists_intersecting_schedule_change = ReplaceableObject(
#     'exists_intersecting_schedule_change(param_change_id integer, param_master_id integer, '
#     'param_change_start timestamp, param_change_end timestamp)',
#     """
#    RETURNS boolean AS $$
#    BEGIN
#        RETURN EXISTS (SELECT *
#                       FROM Schedule_Change
#                       WHERE Schedule_Change.master_id = param_master_id AND
#                             Schedule_Change.id <> param_change_id AND
#                             Schedule_Change.change_start < param_change_end AND
#                             Schedule_Change.change_end > param_change_start);
#    END;
#    $$ LANGUAGE plpgsql;
#    """
# )
