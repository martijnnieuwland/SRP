CREATE TABLE srp_user
  (
     id       SERIAL PRIMARY KEY,
     email    VARCHAR UNIQUE,
     username VARCHAR,
     password VARCHAR
  );

CREATE TABLE aircraft
  (
     aircraft_id                  SERIAL PRIMARY KEY,
     registration        VARCHAR,
     defect              BOOLEAN,
     servicetime         INTERVAL,
     hours               INTERVAL,
     landing_day_total   SMALLINT,
     landing_night_total SMALLINT,
     status              VARCHAR
  );

CREATE TABLE airport
  (
     icao CHAR(4) PRIMARY KEY
  );

CREATE TABLE employee
  (
     employee_id         SERIAL PRIMARY KEY,
     name_first VARCHAR,
     name_last  VARCHAR,
     email      VARCHAR
  );

CREATE TABLE pilot
  (
     pilot_id          SERIAL PRIMARY KEY,
     employee_id INT REFERENCES employee,
     call_sign   VARCHAR
  );

CREATE TABLE crew
  (
     crew_id          SERIAL PRIMARY KEY,
     employee_id INT REFERENCES employee
  );

CREATE TABLE passenger
  (
     passenger_id         SERIAL PRIMARY KEY,
     name_first VARCHAR,
     name_last  VARCHAR
  );

CREATE TABLE flight
  (
     flight_id            SERIAL PRIMARY KEY,
     ac                   INT REFERENCES aircraft,
     p1                   INT REFERENCES pilot,
     p2                   INT REFERENCES pilot,
     airport_dep          VARCHAR REFERENCES airport,
     airport_des          VARCHAR REFERENCES airport,
     srp                  INT,
     DATE                 DATE,
     TASK                 VARCHAR,
     depfuel_uplift_exp   SMALLINT,
     depfuel_uplift_act   SMALLINT,
     depfuel_total        SMALLINT,
     oil_uplift_l         VARCHAR,
     oil_uplift_r         VARCHAR,
     oil_dep_l            VARCHAR,
     oil_dep_r            VARCHAR,
     tks_preflight        SMALLINT,
     deantiice_type       VARCHAR,
     deantiice_temp       SMALLINT,
     deantiice_time       TIME,
     deantiice_mix        VARCHAR,
     holdovertime         INTERVAL,
     takeoff_mass         INT,
     preflight_signature  VARCHAR,
     preflight_callsign   VARCHAR(5),
     landfuel_main_l      SMALLINT,
     landfuel_main_r      SMALLINT,
     landfuel_aux_l       SMALLINT,
     landfuel_aux_r       SMALLINT,
     landfuel_other_l     SMALLINT,
     landfuel_other_r     SMALLINT,
     tks_postflight       SMALLINT,
     blockoff             TIME[0],
     takeoff              TIME[0],
     landing              TIME[0],
     blockon              TIME[0],
     landing_day          SMALLINT,
     landing_night        SMALLINT,
     postflight_signature VARCHAR,
     postflight_callsign  VARCHAR(5)
  );

CREATE TABLE operation
  (
     flight INT REFERENCES flight ON DELETE restrict,
     crew   INT REFERENCES crew,
     PRIMARY KEY (flight, crew)
  );

CREATE TABLE transport
  (
     flight INT REFERENCES flight ON DELETE restrict,
     pax    INT REFERENCES passenger,
     PRIMARY KEY (flight, pax)
  );
