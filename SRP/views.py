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
    if request.method == "GET":
        ac_list = aircraft.query.all()
        user_employee = employee.query.filter_by(email=current_user.email).first()
        user_name_first = user_employee.name_first
        user_name_last = user_employee.name_last
        active_preflights = flight.query.filter_by(postflight_signature=None).all()
        signed_ac = {}
        for pf in active_preflights:
            signed_ac.update({pf.preflight_signature: pf.ac})
        prefl_ac = aircraft.query.filter(aircraft.aircraft_id.in_(signed_ac.values())).all()
        if user_name_last in signed_ac:
            postflight_ac = aircraft.query.filter_by(aircraft_id=signed_ac[user_name_last]).first().registration
        else:
            postflight_ac = ""
        username = current_user.username
        return render_template('home.html',
                               ac_list=ac_list,
                               user=current_user,
                               user_name_last=user_name_last,
                               user_name_first=user_name_first,
                               preflight_ac=prefl_ac,
                               preflight_names=signed_ac.keys(),
                               postflight_ac=postflight_ac,
                               username=username
                               )
    else:
        ac = request.form.get("aircraft")
        return redirect(url_for('views.preflight_ac',
                                ac=ac,
                                ))


@views.route('/preflight-ac', methods=["GET", "POST"])
@login_required
def preflight():
    ac = request.form.get("aircraft")
    if request.method == "GET":
        ac_list = aircraft.query.all()
        return render_template('preflight-ac.html',
                               ac=ac,
                               ac_list=ac_list,
                               user=current_user)
    else:
        return redirect(url_for('views.preflight_ac',
                                ac=ac,
                                user=current_user
                                ))


@views.route('/preflight/<ac>', methods=["GET", "POST"])
@login_required
def preflight_ac(ac):

    #   ---------------- aircraft data  -----------------------------
    ac_list = aircraft.query.all()
    ac_rec = aircraft.query.filter_by(registration=ac).first()
    srp_current = ac_rec.srp
    ac_id = ac_rec.aircraft_id

    # ----------------------- user data --------------------------
    userdata = employee.query.filter_by(email=current_user.email).first()
    user_name_last = userdata.name_last
    current_srp_user = employee.query.filter_by(email=current_user.email).first()
    current_srp_user_name = current_srp_user.name_last
    current_srp_user_initial = current_srp_user.name_first[0]
    current_srp_user_callsign = pilot.query.filter_by(employee_id=current_srp_user.employee_id).first().call_sign
    crew_list = employee.query.join(crew, employee.employee_id == crew.employee_id).all()
    pilot_name = employee.query.join(pilot, employee.employee_id == pilot.employee_id).all()
    username = current_user.username

    # ----------------------- preflight data  --------------------------
    active_preflights = flight.query.filter_by(postflight_signature=None).all()
    signed_ac = {}
    active_preflight_ids = signed_ac.keys()
    active_preflight_regs = []

    for pf in active_preflights:
        signed_ac.update({pf.ac: pf.preflight_signature})

    for i in active_preflight_ids:
        reg = aircraft.query.filter_by(aircraft_id=i).first().registration
        active_preflight_regs.append(reg)

    # -----------------  In case the chosen aircraft has an existing preflight performed  ------------
    if ac_id in signed_ac:
        preflight_rec = flight.query.filter_by(postflight_signature=None, ac=ac_id).first()

        # srp = preflight_rec.srp
        callsign = preflight_rec.callsign
        location = preflight_rec.airport_dep
        destination = preflight_rec.airport_des
        pic_name = employee.query.join(pilot, employee.employee_id == pilot.employee_id).filter_by(
            pilot_id=preflight_rec.p1).first().name_last
        p2 = employee.query.join(pilot, employee.employee_id == pilot.employee_id).filter_by(
            pilot_id=preflight_rec.p2).first().name_last
        crew_name = preflight_rec.crew
        dof = preflight_rec.date
        fuel_bfwd = preflight_rec.depfuel_total
        tom = preflight_rec.takeoff_mass
        oil_dep_l = preflight_rec.oil_dep_l
        oil_dep_r = preflight_rec.oil_dep_r
        tks = preflight_rec.tks_preflight
        task_desc = preflight_rec.task_desc
        if request.method == "GET":

            if user_name_last == signed_ac[ac_id]:
                preflight_signee = "yourself"
                preflight_signee_first = ""
            else:
                preflight_signee = signed_ac[ac_id]
                preflight_signee_first = employee.query.filter_by(name_last=preflight_signee).first().name_first

            return render_template('preflight.html',
                                   page="preflight",
                                   user=current_user,
                                   preflight_signee=preflight_signee,
                                   preflight_signee_first=preflight_signee_first,
                                   active_preflight_regs=active_preflight_regs,
                                   ac=ac,
                                   srp=srp_current,
                                   task_desc=task_desc,
                                   callsign=callsign,
                                   location=location,
                                   destination=destination,
                                   pic_name=pic_name,
                                   p2=p2,
                                   crew_name=crew_name,
                                   # pax=pax,
                                   current_srp_user_name=current_srp_user_name,
                                   dof=dof,
                                   fuel_bfwd=fuel_bfwd,
                                   pilot_name=pilot_name,
                                   crew_list=crew_list,
                                   tom=tom,
                                   oil_dep_l=oil_dep_l,
                                   oil_dep_r=oil_dep_r,
                                   tks=tks,
                                   current_srp_user_initial=current_srp_user_initial,
                                   current_srp_user_callsign=current_srp_user_callsign,
                                   # date=dof,
                                   username=username,
                                   ac_list=ac_list,
                                   )
        else:
            preflight_rec.callsign = request.form.get("callsign") if request.form.get("callsign") else "-"
            preflight_rec.task = request.form.get("task")
            preflight_rec.task_desc = request.form.get("task_desc")
            preflight_rec.date = request.form.get("date")
            preflight_rec.airport_dep = request.form.get("airport_dep").upper()
            preflight_rec.airport_des = request.form.get("airport_des").upper()
            preflight_rec.pic_name = request.form.get("p1")
            preflight_rec.p1 = pilot.query.join(employee, pilot.employee_id == employee.employee_id) \
                .filter_by(name_last=pic_name).first().pilot_id
            pm = request.form.get("p2")
            preflight_rec.p2 = pilot.query.join(employee, pilot.employee_id == employee.employee_id) \
                .filter_by(name_last=pm).first().pilot_id if pm else 0
            preflight_rec.crew_name = request.form.get("crew")
            preflight_rec.crew_id = crew.query.join(employee, crew.employee_id == employee.employee_id) \
                .filter_by(name_last=crew_name).first().crew_id if crew_name else None
            preflight_rec.takeoff_mass = request.form.get("tom")
            preflight_rec.fuel_bfwd = request.form.get("fuel_bfwd") if request.form.get("fuel_bfwd") else 0
            preflight_rec.depfuel_total = request.form.get("fuel_dep")
            preflight_rec.depfuel_uplift_exp = request.form.get("uplift_exp") if request.form.get("uplift_exp") else 0
            preflight_rec.depfuel_uplift_act = request.form.get("uplift_act") if request.form.get("uplift_act") else 0
            preflight_rec.oil_dep_l = request.form.get("dep_oil_l")
            preflight_rec.oil_dep_r = request.form.get("dep_oil_r")
            preflight_rec.oil_uplift_l = request.form.get("oil_up_l") if request.form.get("oil_up_l") else 0
            preflight_rec.oil_uplift_r = request.form.get("oil_up_l") if request.form.get("oil_up_l") else 0
            preflight_rec.tks_preflight = request.form.get("tks") if request.form.get("tks") else 0
            preflight_rec.anti_ice_type = request.form.get("anti_ice_type")
            preflight_rec.temperature = request.form.get("temperature") if request.form.get("temperature") else None
            preflight_rec.anti_ice_mix = request.form.get("anti_ice_mix")
            preflight_rec.anti_ice_time = request.form.get("anti_ice_time") if request.form.get("anti_ice_time")\
                else None
            preflight_rec.holdover_time = request.form.get("holdover_time") if request.form.get("holdover_time")\
                else None

            db.session.commit()

            return redirect(url_for("views.records"))

    # ----------------  In case the aircraft does NOT already have a preflight performed  ------------
    else:
        srp_next = int(srp_current) + 1
        callsign = ac_rec.callsign
        location = ac_rec.location
        fuel_bfwd = ac_rec.fuel
        oil_dep_l = ac_rec.oil_l
        oil_dep_r = ac_rec.oil_r
        tks = ac_rec.tks
        pic_name = userdata.name_last if userdata else srp_user.query.filter_by(username=current_user.username). \
            first().username
        dof = datetime.now()

        if request.method == "GET":

            return render_template('preflight.html',
                                   page="preflight",
                                   user=current_user,
                                   ac=ac,
                                   srp=srp_next,
                                   callsign=callsign,
                                   location=location,
                                   pic_name=pic_name,
                                   current_srp_user_name=current_srp_user_name,
                                   # today=dof,
                                   fuel_bfwd=fuel_bfwd,
                                   pilot_name=pilot_name,
                                   crew_list=crew_list,
                                   oil_dep_l=oil_dep_l,
                                   oil_dep_r=oil_dep_r,
                                   tks=tks,
                                   current_srp_user_initial=current_srp_user_initial,
                                   current_srp_user_callsign=current_srp_user_callsign,
                                   dof=dof,
                                   username=username,
                                   ac_list=ac_list,
                                   )
        else:
            pax = request.form.get("pax")
            new_pax = passenger(name_first=pax, name_last=pax)
            db.session.add(new_pax)

            callsign = request.form.get("callsign") if request.form.get("callsign") else "-"
            task = request.form.get("task")
            task_desc = request.form.get("task_desc")
            date = request.form.get("date")
            airport_dep = request.form.get("airport_dep").upper()
            airport_des = request.form.get("airport_des").upper()
            pic_name = request.form.get("p1")
            p1 = pilot.query.join(employee, pilot.employee_id == employee.employee_id) \
                .filter_by(name_last=pic_name).first().pilot_id
            pm = request.form.get("p2")
            p2 = pilot.query.join(employee, pilot.employee_id == employee.employee_id) \
                .filter_by(name_last=pm).first().pilot_id if pm else 0
            crew_name = request.form.get("crew")
            crew_id = crew.query.join(employee, crew.employee_id == employee.employee_id) \
                .filter_by(name_last=crew_name).first().crew_id if crew_name else None
            takeoff_mass = request.form.get("tom")
            fuel_bfwd = request.form.get("fuel_bfwd") if request.form.get("fuel_bfwd") else 0
            depfuel_total = request.form.get("fuel_dep")
            depfuel_uplift_exp = request.form.get("uplift_exp") if request.form.get("uplift_exp") else 0
            depfuel_uplift_act = request.form.get("uplift_act") if request.form.get("uplift_act") else 0
            oil_dep_l = request.form.get("dep_oil_l")
            oil_dep_r = request.form.get("dep_oil_r")
            oil_uplift_l = request.form.get("oil_up_l") if request.form.get("oil_up_l") else 0
            oil_uplift_r = request.form.get("oil_up_l") if request.form.get("oil_up_l") else 0
            tks_preflight = request.form.get("tks") if request.form.get("tks") else 0
            anti_ice_type = request.form.get("anti_ice_type")
            temperature = request.form.get("temperature") if request.form.get("temperature") else None
            anti_ice_mix = request.form.get("anti_ice_mix")
            anti_ice_time = request.form.get("anti_ice_time") if request.form.get("anti_ice_time") else None
            holdover_time = request.form.get("holdover_time") if request.form.get("holdover_time") else None

            # -------------------  enter sector preflight data  ---------------------------------
            preflight_data = flight(srp=srp_next,
                                    ac=ac_id,
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
                                    oil_uplift_l=oil_uplift_l,
                                    oil_uplift_r=oil_uplift_r,
                                    oil_dep_l=oil_dep_l,
                                    oil_dep_r=oil_dep_r,
                                    tks_preflight=tks_preflight,
                                    deantiice_type=anti_ice_type,
                                    deantiice_temp=temperature,
                                    deantiice_mix=anti_ice_mix,
                                    deantiice_time=anti_ice_time,
                                    holdovertime=holdover_time,
                                    preflight_signature=current_srp_user_name,
                                    preflight_callsign=current_srp_user_callsign
                                    )
            db.session.add(preflight_data)

            # -------------------  update aircraft  ---------------------------------
            ac_rec.location = airport_des
            ac_rec.fuel = depfuel_total
            ac_rec.oil_l = oil_dep_l
            ac_rec.oil_r = oil_dep_r
            ac_rec.tks = tks_preflight
            ac_rec.callsign = callsign
            ac_rec.srp = srp_next
            print(ac_rec.srp)

            db.session.commit()

            return redirect(url_for('views.records',
                                    # ac=ac,
                                    user=current_user
                                    ))


@views.route("/postflight/<ac>", methods=["GET", "POST"])
@login_required
def postflight(ac):
    ac_record = aircraft.query.filter_by(registration=ac).first()
    ac_id = aircraft.query.filter_by(registration=ac).first().aircraft_id
    srp = ac_record.srp
    print(ac, srp)
    sector_record = flight.query.filter_by(ac=ac_id, srp=srp).first()
    ac_hrs_bfwd = ac_record.hours
    ac_hrs_bfwd_hrs = '%02d' % int((ac_hrs_bfwd.total_seconds() / 60) // 60)
    ac_hrs_bfwd_min = '%02d' % int((ac_hrs_bfwd.total_seconds() / 60) % 60)
    total_cycles = ac_record.cycles
    total_day_ldg = ac_record.landing_day_total
    total_night_ldg = ac_record.landing_night_total
    tks = ac_record.tks
    servicetime = ac_record.servicetime
    service_hrs = int((servicetime.total_seconds() / 60) // 60)
    service_min = int((servicetime.total_seconds() / 60) % 60)
    rem_hrs = int(((servicetime - ac_hrs_bfwd).total_seconds() / 60) // 60)
    rem_min = int(((servicetime - ac_hrs_bfwd).total_seconds() / 60) % 60)

    # -----------------  Postflight submission  ----------------------
    date = sector_record.date
    srp_user_name = employee.query.join(srp_user, srp_user.email == employee.email).filter_by(
        email=current_user.email).first().name_last
    srp_user_initial = employee.query.join(srp_user, srp_user.email == employee.email).filter_by(
        email=current_user.email).first().name_first[0]
    srp_user_callsign = pilot.query.filter_by(
        employee_id=(employee.query.join(srp_user, employee.email == srp_user.email).filter_by(
            email=current_user.email).first().employee_id)).first().call_sign

    if request.method == "GET":
        return render_template('postflight.html',
                               user=current_user,
                               srp=srp,
                               ac=ac,
                               ac_hrs_bfwd_hrs=ac_hrs_bfwd_hrs,
                               ac_hrs_bfwd_min=ac_hrs_bfwd_min,
                               total_cycles=total_cycles,
                               total_day_ldg=total_day_ldg,
                               total_night_ldg=total_night_ldg,
                               tks=tks,
                               service_hrs=service_hrs,
                               service_min=service_min,
                               rem_hrs=rem_hrs,
                               rem_min=rem_min,
                               date=date,
                               srp_user_name=srp_user_name,
                               srp_user_initial=srp_user_initial,
                               srp_user_callsign=srp_user_callsign
                               )
    else:
        # -----------  update sector record  ---------------------------------
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
        landfuel_main_l = request.form.get("main_l") if request.form.get("main_l") else 0
        landfuel_main_r = request.form.get("main_r") if request.form.get("main_r") else 0
        landfuel_aux_l = request.form.get("aux_l") if request.form.get("aux_l") else 0
        landfuel_aux_r = request.form.get("aux_r") if request.form.get("aux_r") else 0
        landfuel_other_l = request.form.get("other_l") if request.form.get("other_l") else 0
        landfuel_other_r = request.form.get("other_r") if request.form.get("other_r") else 0
        tks_postflight = request.form.get("tks") if request.form.get("tks") else 0
        landing_day = int(request.form.get("landings_day")) if request.form.get("landings_day") else 0
        landing_night = int(request.form.get("landings_night")) if request.form.get("landings_night") else 0
        cycles = int(request.form.get("cycles")) if request.form.get("cycles") else 0

        sector_record.blockoff = blockoff
        sector_record.takeoff = takeoff
        sector_record.landing = landing
        sector_record.blockon = blockon
        sector_record.landfuel_main_l = landfuel_main_l
        sector_record.landfuel_main_r = landfuel_main_r
        sector_record.landfuel_aux_l = landfuel_aux_l
        sector_record.landfuel_aux_r = landfuel_aux_r
        sector_record.landfuel_other_l = landfuel_other_l
        sector_record.landfuel_other_r = landfuel_other_r
        sector_record.tks_postflight = tks_postflight
        sector_record.landing_day = landing_day
        sector_record.landing_night = landing_night
        sector_record.postflight_signature = srp_user_name
        sector_record.postflight_callsign = srp_user_callsign

        # -------------  update aircraft  ----------------------------------
        ac_hrs = int('%02d' % int(request.form.get("ac_hrs_new")))
        ac_min = int('%02d' % int(request.form.get("ac_min_new")))
        ac_time = f"{ac_hrs}:{ac_min}"

        ac_record.hours = ac_time
        ac_record.fuel = int(request.form.get("landing_fuel"))
        ac_record.cycles = total_cycles + cycles
        ac_record.landing_day_total = total_day_ldg + landing_day
        ac_record.landing_night_total = total_night_ldg + landing_night
        ac_record.tks = request.form.get("tks")
        ac_record.defect = request.form.get("defect")

        db.session.commit()

        return redirect(url_for("views.records", user=current_user))


@views.route("/postflight", methods=["GET", "POST"])
@login_required
def get_preflight():
    if request.method == "GET":
        username = current_user.username
        user_employee = employee.query.filter_by(email=current_user.email).first()
        user_name_last = user_employee.name_last
        active_preflights = flight.query.filter_by(postflight_signature=None).all()
        signed_ac = {}
        for pf in active_preflights:
            signed_ac.update({pf.preflight_signature: pf.ac})
        prefl_ac = aircraft.query.filter(aircraft.aircraft_id.in_(signed_ac.values())).all()
        if user_name_last in signed_ac:
            ac = aircraft.query.filter_by(aircraft_id=signed_ac[user_name_last]).first().registration
            return redirect(url_for("views.postflight", user=current_user, ac=ac))
        else:
            return render_template('postflight-ac.html',
                                   user=current_user,
                                   active_preflights=active_preflights,
                                   username=username,
                                   prefl_ac=prefl_ac
                                   )
    else:
        ac = request.form.get("preflight_ac")
        if ac:
            return redirect(url_for("views.postflight",
                                    user=current_user,
                                    ac=ac
                                    ))
        else:
            return render_template("home.html",
                                   user=current_user)


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
    query = flight.query.join(aircraft, aircraft.aircraft_id == flight.ac)

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            cast(flight.flight_id, String).like(f"%{search}%"),
            aircraft.registration.like(f"%{search}%"),
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
