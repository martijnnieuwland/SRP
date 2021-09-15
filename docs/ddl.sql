CREATE TABLE aircraft (
  id SERIAL PRIMARY KEY, registration VARCHAR NOT NULL,
  defect BOOLEAN, servicetime INTERVAL,
  hours INTERVAL NOT NULL, landing_day_total SMALLINT,
  landing_night_total SMALLINT
);
CREATE TABLE airport (
  icao CHAR(4) PRIMARY KEY
);
CREATE TABLE pilot (
  id SERIAL PRIMARY KEY, call_sign VARCHAR,
  name_first VARCHAR, name_last VARCHAR
);
CREATE TABLE crew (
  id SERIAL PRIMARY KEY, name_first VARCHAR,
  name_last VARCHAR
);
CREATE TABLE passenger (
  id SERIAL PRIMARY KEY, name_first VARCHAR,
  name_last VARCHAR
);
CREATE TABLE operation (
  flight INT REFERENCES flight ON DELETE RESTRICT,
  crew INT REFERENCES crew,
  PRIMARY KEY (flight, crew)
);
CREATE TABLE transport (
  flight INT REFERENCES flight ON DELETE RESTRICT,
  pax INT REFERENCES passenger,
  PRIMARY KEY (flight, pax)
);
CREATE TABLE flight (
  id SERIAL PRIMARY KEY,
  ac INT REFERENCES aircraft,
  p1 INT REFERENCES pilot,
  p2 INT REFERENCES pilot,
  airport_dep VARCHAR REFERENCES airport,
  airport_des VARCHAR REFERENCES airport,
  srp INT,
  date DATE NOT NULL,
  task VARCHAR,
  depfuel_uplift_exp SMALLINT,
  depfuel_uplift_act SMALLINT,
  depfuel_total SMALLINT NOT NULL,
  oil_uplift_l VARCHAR,
  oil_uplift_r VARCHAR,
  oil_dep_l VARCHAR,
  oil_dep_r VARCHAR,
  tks_preflight SMALLINT,
  deantiice_type VARCHAR,
  deantiice_temp SMALLINT,
  deantiice_time TIME,
  deantiice_mix VARCHAR,
  holdovertime INTERVAL,
  takeoff_mass INT NOT NULL,
  preflight_signature VARCHAR,
  preflight_callsign VARCHAR(5),
  landfuel_main_l SMALLINT NOT NULL,
  landfuel_main_r SMALLINT NOT NULL,
  landfuel_aux_l SMALLINT NOT NULL,
  landfuel_aux_r SMALLINT NOT NULL,
  landfuel_other_l SMALLINT NOT NULL,
  landfuel_other_r SMALLINT NOT NULL,
  tks_postflight SMALLINT,
  blockoff TIME[0] NOT NULL,
  takeoff TIME[0] NOT NULL,
  landing TIME[0] NOT NULL,
  blockon TIME[0] NOT NULL,
  landing_day SMALLINT NOT NULL,
  landing_night SMALLINT NOT NULL,
  postflight_signature VARCHAR NOT NULL,
  postflight_callsign VARCHAR(5) NOT NULL
);
