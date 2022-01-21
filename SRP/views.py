from datetime import datetime, time
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from SRP.models import aircraft, crew, employee, flight, passenger, pilot, srp_user
from SRP import db
from sqlalchemy.sql import cast
from sqlalchemy.types import String

views = Blueprint("views", __name__)


@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    return render_template('home.html', page="home", user=current_user)


@views.route('/preflight-ac', methods=["GET", "POST"])
@login_required
def preflight():
    if request.method == "GET":
        ac_list = aircraft.query.all()
        return render_template('preflight-ac.html', ac_list=ac_list, user=current_user)
    else:
        ac = request.form.get("aircraft")
        ac_rec = aircraft.query.filter_by(registration=ac).first()
        ac_srp = aircraft.query.filter_by(registration=ac).first().srp
        ac_rec.srp = ac_srp + 1
        db.session.commit()
        return redirect(url_for('views.preflight_ac', ac=ac))


@views.route('/preflight/<ac>', methods=["GET", "POST"])
@login_required
def preflight_ac(ac):
    srp = aircraft.query.filter_by(registration=ac).first().srp
    callsign = aircraft.query.filter_by(registration=ac).first().callsign
    today = datetime.now()
    location = aircraft.query.filter_by(registration=ac).first().location
    pic = employee.query.join(srp_user, employee.email == srp_user.email) \
        .filter_by(email=current_user.email).first()
    pic = pic.name_last if pic else srp_user.query.filter_by(username=current_user.username).first().username
    fuel_bfwd = aircraft.query.filter_by(registration=ac).first().fuel
    oil_dep_l = aircraft.query.filter_by(registration=ac).first().oil_l
    oil_dep_r = aircraft.query.filter_by(registration=ac).first().oil_r
    tks = aircraft.query.filter_by(registration=ac).first().tks
    crew_list = employee.query.join(crew, employee.employee_id == crew.employee_id).all()
    pilot_name = employee.query.join(pilot, employee.employee_id == pilot.employee_id).all()
    if request.method == "GET":
        return render_template("preflight.html",
                               page="preflight",
                               user=current_user,
                               ac=ac,
                               srp=srp,
                               callsign=callsign,
                               location=location,
                               pic=pic,
                               today=today,
                               fuel_bfwd=fuel_bfwd,
                               pilot_name=pilot_name,
                               crew_list=crew_list,
                               oil_dep_l=oil_dep_l,
                               oil_dep_r=oil_dep_r,
                               tks=tks)
    else:
        pax = request.form.get("pax")
        new_pax = passenger(name_first=pax, name_last=pax)
        db.session.add(new_pax)
        db.session.commit()

        aircraft_id = aircraft.query.filter_by(registration=ac).first().aircraft_id
        task = request.form.get("task")
        task_desc = request.form.get("task_desc")
        date = request.form.get("date")
        airport_dep = request.form.get("airport_dep").upper()
        airport_des = request.form.get("airport_des").upper()
        pic = request.form.get("p1")
        p1 = pilot.query.join(employee, pilot.employee_id == employee.employee_id) \
            .filter_by(name_last=pic).first().pilot_id
        pm = request.form.get("p2")
        p2 = pilot.query.join(employee, pilot.employee_id == employee.employee_id) \
            .filter_by(name_last=pm).first().pilot_id if pm else None
        crew_name = request.form.get("crew")
        crew_id = crew.query.join(employee, crew.employee_id == employee.employee_id) \
            .filter_by(name_last=crew_name).first().crew_id if crew_name else None
        takeoff_mass = request.form.get("tom")
        depfuel_total = request.form.get("fuel_dep")
        depfuel_uplift_exp = request.form.get("uplift_exp")
        depfuel_uplift_exp = depfuel_uplift_exp if depfuel_uplift_exp else None
        depfuel_uplift_act = request.form.get("uplift_act")
        depfuel_uplift_act = depfuel_uplift_act if depfuel_uplift_act else None
        oil_dep_l = request.form.get("dep_oil_l")
        oil_dep_r = request.form.get("dep_oil_r")
        oil_uplift_l = request.form.get("oil_up_l")
        oil_uplift_r = request.form.get("oil_up_r")
        tks_preflight = request.form.get("tks")
        anti_ice_type = request.form.get("anti_ice_type")
        temperature = request.form.get("temperature")
        temperature = temperature if temperature else None
        anti_ice_mix = request.form.get("anti_ice_mix")
        anti_ice_time = request.form.get("anti_ice_time")
        anti_ice_time = anti_ice_time if anti_ice_time else None
        holdover_time = request.form.get("holdover_time")
        holdover_time = holdover_time if holdover_time else None

        preflight_signature = True
        preflight_callsign = "x"

        preflight_data = flight(srp=srp,
                                ac=aircraft_id,
                                callsign=callsign,
                                task=task,
                                task_desc=task_desc,
                                date=date,
                                airport_dep=airport_dep,
                                airport_des=airport_des,
                                p1=p1,
                                p2=p2,
                                crew=crew_id,
                                takeoff_mass=takeoff_mass,
                                fuel_bfwd=fuel_bfwd,
                                depfuel_total=depfuel_total,
                                depfuel_uplift_exp=depfuel_uplift_exp,
                                depfuel_uplift_act=depfuel_uplift_act,
                                oil_dep_l=oil_dep_l,
                                oil_dep_r=oil_dep_r,
                                oil_uplift_l=oil_uplift_l,
                                oil_uplift_r=oil_uplift_r,
                                tks_preflight=tks_preflight,
                                deantiice_type=anti_ice_type,
                                deantiice_temp=temperature,
                                deantiice_mix=anti_ice_mix,
                                deantiice_time=anti_ice_time,
                                holdovertime=holdover_time,
                                preflight_signature=preflight_signature,
                                preflight_callsign=preflight_callsign)
        db.session.add(preflight_data)
        db.session.commit()
        return redirect(url_for('views.postflight', ac=ac))


@views.route("/postflight/<ac>", methods=["GET", "POST"])
@login_required
def postflight(ac):
    ac_record = aircraft.query.filter_by(registration=ac).first()
    srp = ac_record.srp
    ac_hrs_bfwd = ac_record.hours
    ac_hrs_bfwd_hrs = '%02d' % int((ac_hrs_bfwd.total_seconds() / 60) // 60)
    ac_hrs_bfwd_min = '%02d' % int((ac_hrs_bfwd.total_seconds() / 60) % 60)
    cycles = ac_record.cycles
    total_day_ldg = ac_record.landing_day_total
    total_night_ldg = ac_record.landing_night_total
    tks_postflight = ac_record.tks
    servicetime = ac_record.servicetime
    service_hrs = int((servicetime.total_seconds() / 60) // 60)
    service_min = int((servicetime.total_seconds() / 60) % 60)
    rem_hrs = int(((servicetime - ac_hrs_bfwd).total_seconds() / 60) // 60)
    rem_min = int(((servicetime - ac_hrs_bfwd).total_seconds() / 60) % 60)

    if request.method == "GET":
        return render_template('postflight.html',
                               user=current_user,
                               srp=srp,
                               ac=ac,
                               ac_hrs_bfwd_hrs=ac_hrs_bfwd_hrs,
                               ac_hrs_bfwd_min=ac_hrs_bfwd_min,
                               cycles=cycles,
                               total_day_ldg=total_day_ldg,
                               total_night_ldg=total_night_ldg,
                               tks=tks_postflight,
                               service_hrs=service_hrs,
                               service_min=service_min,
                               rem_hrs=rem_hrs,
                               rem_min=rem_min
                               )
    else:
        # -----------  update sector record  ---------------------------------
        ac_id = aircraft.query.filter_by(srp=srp).first().aircraft_id
        sector_record = flight.query.filter_by(ac=ac_id, srp=srp).first()
        offhrs = int(request.form.get("offhrs"))
        offmin = int(request.form.get("offmin"))
        tohrs = int(request.form.get("tohrs"))
        tomin = int(request.form.get("tomin"))
        ldghrs = int(request.form.get("ldghrs"))
        ldgmin = int(request.form.get("ldgmin"))
        onhrs = int(request.form.get("onhrs"))
        onmin = int(request.form.get("onmin"))
        blockoff = time(hour=offhrs, minute=offmin)
        takeoff = time(hour=tohrs, minute=tomin)
        landing = time(hour=ldghrs, minute=ldgmin)
        blockon = time(hour=onhrs, minute=onmin)
        sector_record.blockoff = blockoff
        sector_record.takeoff = takeoff
        sector_record.landing = landing
        sector_record.blockon = blockon

        # -------------  update aircraft  ----------------------------------
        ac_hrs = int('%02d' % int(request.form.get("ac_hrs_new")))
        ac_min = int('%02d' % int(request.form.get("ac_min_new")))
        ac_time = f"{ac_hrs}:{ac_min}"
        ac_record.hours = ac_time
        ac_record.fuel = request.form.get("landing_fuel")
        ac_record.cycles = cycles + int(request.form.get("cycles"))
        ac_record.landing_day_total = total_day_ldg + int(request.form.get("landings_day"))
        ac_record.landing_night_total = total_night_ldg + int(request.form.get("landings_night"))
        ac_record.tks = request.form.get("tks")
        ac_record.defect = request.form.get("defect")
        db.session.commit()
        return render_template('home.html',
                               user=current_user)


@views.route("/postflight", methods=["GET", "POST"])
@login_required
def get_postflight():
    return render_template('postflight.html', user=current_user)


@views.route("/records", methods=["GET", "POST"])
@login_required
def records():
    return render_template("records.html",
                           title="Records",
                           page="records",
                           user=current_user
                           )


@views.route("/api/sector_records")
@login_required
def sector_records():
    query = flight.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            cast(flight.flight_id, String).like(f"%{search}%"),
            cast(flight.ac, String).like(f"%{search}%"),
            flight.callsign.like(f"%{search}%"),
            cast(flight.p1, String).like(f"%{search}%"),
            cast(flight.p2, String).like(f"%{search}%"),
            cast(flight.crew, String).like(f"%{search}%"),
            flight.airport_dep.like(f"%{search}%"),
            flight.airport_des.like(f"%{search}%"),
            cast(flight.srp, String).like(f"%{search}%"),
            flight.task.like(f"%{search}%"),
            flight.preflight_signature.like(f"%{search}%"),
            flight.preflight_callsign.like(f"%{search}%"),
            flight.postflight_signature.like(f"%{search}%"),
            flight.postflight_callsign.like(f"%{search}%")
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f"order[{i}][column]")
        if col_index is None:
            break
        col_name = request.args.get(f"columns[{col_index}][data]")
        if col_name not in ["flight_id",
                            "ac",
                            "callsign",
                            "p1",
                            "p2",
                            "crew",
                            "airport_dep",
                            "airport_des",
                            "srp",
                            "date",
                            "task",
                            "preflight_signature",
                            "preflight_callsign",
                            "postflight_signature",
                            "postflight_callsign"]:
            col_name = "flight_id"
        descending = request.args.get(f"order[{i}][dir]") == "desc"
        col = getattr(flight, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    query = query.offset(start).limit(length)

    # response
    return {"data": [sector_data.to_dict() for sector_data in query],
            "recordsFiltered": total_filtered,
            "recordsTotal": flight.query.count(),
            "draw": request.args.get("draw", type=int)
            }


@views.route("/api/aircraft_records")
@login_required
def aircraft_records():
    query = aircraft.query

    # search filter
    search = request.args.get("search[value]")
    if search:
        query = query.filter(db.or_(
            cast(aircraft.aircraft_id, String).like(f"search{search}"),
            aircraft.registration.like(f"search{search}"),
            aircraft.defect.like(f"search{search}"),
            aircraft.status.like(f"search{search}"),
            cast(aircraft.srp, String).like(f"search{search}"),
            aircraft.callsign.like(f"search{search}"),
            aircraft.location.like(f"search{search}")
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f"order[{i}][column]")
        if col_index is None:
            break
        col_name = request.args.get(f"columns[{col_index}][data]")
        if col_name not in ["aircraft_id",
                            "registration",
                            "hours",
                            "landing_day_total",
                            "landing_night_total",
                            "status",
                            "srp",
                            "callsign",
                            "location",
                            "cycles"]:
            col_name = "registration"
        descending = request.args.get(f"order[{i}][dir]") == "desc"
        col = getattr(aircraft, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    query = query.offset(start).limit(length)

    # response
    return {'data': [ac.to_dict() for ac in query],
            "recordsFiltered": total_filtered,
            "recordsTotal": aircraft.query.count(),
            "draw": request.args.get("draw", type=int)
            }


@views.route("/test")
def test():
    return render_template("test.html")
