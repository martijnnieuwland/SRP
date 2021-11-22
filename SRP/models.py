from flask_login import UserMixin
from sqlalchemy.sql import func
from SRP import db


class srp_user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    password = db.Column(db.String)


class aircraft(db.Model):
    aircraft_id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(db.String)
    defect = db.Column(db.Boolean)
    servicetime = db.Column(db.Interval)
    hours = db.Column(db.Interval)
    landing_day_total = db.Column(db.Integer)
    landing_night_total = db.Column(db.Integer)
    status = db.Column(db.String)
    fuel = db.Column(db.Integer)
    oil_l = db.Column(db.Integer)
    oil_r = db.Column(db.Integer)
    tks = db.Column(db.Integer)
    srp = db.Column(db.Integer)
    callsign = db.Column(db.String)
    location = db.Column(db.Integer)


class airport(db.Model):
    icao = db.Column(db.String, primary_key=True)


class crew(db.Model):
    crew_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))


class employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    name_first = db.Column(db.String)
    name_last = db.Column(db.String)
    email = db.Column(db.String)


class flight(db.Model):
    flight_id = db.Column(db.Integer, primary_key=True)
    ac = db.Column(db.Integer, db.ForeignKey('aircraft.aircraft_id'))
    callsign = db.Column(db.String,)
    p1 = db.Column(db.Integer, db.ForeignKey('pilot.pilot_id'))
    p2 = db.Column(db.Integer, db.ForeignKey('pilot.pilot_id'))
    crew = db.Column(db.Integer)
    airport_dep = db.Column(db.String, db.ForeignKey('airport.icao'))
    airport_des = db.Column(db.String, db.ForeignKey('airport.icao'))
    srp = db.Column(db.Integer)
    date = db.Column(db.Date, default=func.now())
    task = db.Column(db.String)
    task_desc = db.Column(db.String)
    fuel_bfwd =  db.Column(db.Integer)
    depfuel_uplift_exp = db.Column(db.Integer)
    depfuel_uplift_act = db.Column(db.Integer)
    depfuel_total = db.Column(db.Integer)
    oil_uplift_l = db.Column(db.Float)
    oil_uplift_r = db.Column(db.Float)
    oil_dep_l = db.Column(db.Float)
    oil_dep_r = db.Column(db.Float)
    tks_preflight = db.Column(db.Integer)
    deantiice_type = db.Column(db.String)
    deantiice_temp = db.Column(db.Integer)
    deantiice_time = db.Column(db.DateTime)
    deantiice_mix = db.Column(db.String)
    holdovertime = db.Column(db.Interval)
    takeoff_mass = db.Column(db.Integer)
    preflight_signature = db.Column(db.Boolean)
    preflight_callsign = db.Column(db.String)
    landfuel_main_l = db.Column(db.Integer)
    landfuel_main_r = db.Column(db.Integer)
    landfuel_aux_l = db.Column(db.Integer)
    landfuel_aux_r = db.Column(db.Integer)
    landfuel_other_l = db.Column(db.Integer)
    landfuel_other_r = db.Column(db.Integer)
    tks_postflight = db.Column(db.Integer)
    blockoff = db.Column(db.DateTime)
    takeoff = db.Column(db.DateTime)
    landing = db.Column(db.DateTime)
    blockon = db.Column(db.DateTime)
    landing_day = db.Column(db.Integer)
    landing_night = db.Column(db.Integer)
    postflight_signature = db.Column(db.Boolean)
    postflight_callsign = db.Column(db.String(5))


operation = db.Table('operation',
                     db.Column('flight', db.Integer, db.ForeignKey('flight.flight_id'), primary_key=True),
                     db.Column('crew', db.Integer, db.ForeignKey('crew.crew_id'), primary_key=True)
                     )


class passenger(db.Model):
    pax_id = db.Column(db.Integer, primary_key=True)
    name_first = db.Column(db.String)
    name_last = db.Column(db.String)


class pilot(db.Model):
    pilot_id = db.Column(db.Integer, primary_key=True)
    call_sign = db.Column(db.String)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))


transport = db.Table('transport',
                     db.Column('flight', db.Integer, db.ForeignKey('flight.flight_id'), primary_key=True),
                     db.Column('pax', db.Integer, db.ForeignKey('passenger.pax_id'), primary_key=True)
                     )
