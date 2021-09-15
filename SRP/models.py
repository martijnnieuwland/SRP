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
    registration = db.Column(db.String, nullable=False)
    defect = db.Column(db.Boolean)
    servicetime = db.Column(db.Interval)
    hours = db.Column(db.Interval, nullable=False)
    landing_day_total = db.Column(db.Integer)
    landing_night_total = db.Column(db.Integer)
    fuel = db.Column(db.Integer)


class airport(db.Model):
    icao = db.Column(db.String, primary_key=True)


class crew(db.Model):
    crew_id = db.Column(db.Integer, primary_key=True)
    name_first = db.Column(db.String)
    name_last = db.Column(db.String)


class flight(db.Model):
    flight_id = db.Column(db.Integer, primary_key=True)
    aircraft = db.Column(db.Integer, db.ForeignKey('aircraft.aircraft_id'), nullable=False)
    pilot1 = db.Column(db.Integer, db.ForeignKey('pilot.pilot_id'), nullable=False)
    pilot2 = db.Column(db.Integer, db.ForeignKey('pilot.pilot_id'))
    airport_dep = db.Column(db.String, db.ForeignKey('airport.icao'), nullable=False)
    airport_des = db.Column(db.String, db.ForeignKey('airport.icao'), nullable=False)
    srp = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=func.now())
    task = db.Column(db.String)
    depfuel_uplift_exp = db.Column(db.Integer)
    depfuel_uplift_act = db.Column(db.Integer)
    depfuel_total = db.Column(db.Integer, nullable=False)
    oil_uplift_l = db.Column(db.Float)
    oil_uplift_r = db.Column(db.Float)
    oil_dep_l = db.Column(db.Float, nullable=False)
    oil_dep_r = db.Column(db.Float, nullable=False)
    tks_preflight = db.Column(db.Integer, nullable=False)
    deantiice_type = db.Column(db.String)
    deantiice_temp = db.Column(db.Integer)
    deantiice_time = db.Column(db.DateTime)
    deantiice_mix = db.Column(db.String)
    holdovertime = db.Column(db.Interval)
    takeoff_mass = db.Column(db.Integer, nullable=False)
    preflight_signature = db.Column(db.Boolean, nullable=False)
    preflight_callsign = db.Column(db.String(5), nullable=False)
    landfuel_main_l = db.Column(db.Integer, nullable=False)
    landfuel_main_r = db.Column(db.Integer, nullable=False)
    landfuel_aux_l = db.Column(db.Integer, nullable=False)
    landfuel_aux_r = db.Column(db.Integer, nullable=False)
    landfuel_other_l = db.Column(db.Integer, nullable=False)
    landfuel_other_r = db.Column(db.Integer, nullable=False)
    tks_postflight = db.Column(db.Integer, nullable=False)
    blockoff = db.Column(db.DateTime, nullable=False)
    takeoff = db.Column(db.DateTime, nullable=False)
    landing = db.Column(db.DateTime, nullable=False)
    blockon = db.Column(db.DateTime, nullable=False)
    landing_day = db.Column(db.Integer, nullable=False)
    landing_night = db.Column(db.Integer, nullable=False)
    postflight_signature = db.Column(db.Boolean, nullable=False)
    postflight_callsign = db.Column(db.String(5), nullable=False)


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
    callsign = db.Column(db.String, nullable=False)
    name_first = db.Column(db.String)
    name_last = db.Column(db.String)


transport = db.Table('transport',
                     db.Column('flight', db.Integer, db.ForeignKey('flight.flight_id'), primary_key=True),
                     db.Column('pax', db.Integer, db.ForeignKey('passenger.pax_id'), primary_key=True)
                     )
