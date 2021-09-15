from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from SRP.models import aircraft, airport, crew, flight, passenger, pilot, srp_user
from SRP import db

views = Blueprint("views", __name__)


@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    return render_template('home.html', page="home", user=current_user)


@views.route("/preflight", methods=["GET", "POST"])
@login_required
def preflight():
    ac = aircraft.query.all()
    today = datetime.now()
    ac_reg = aircraft.query.filter_by(registration="G-WKTO").first()  # get latest fuel from database
    fuel_bfwd = ac_reg.fuel
    uplift_act = 0  # default value
    fuel_dep = fuel_bfwd + uplift_act
    crew_name = crew.query.all()
    pilot_rec = pilot.query.all()
    if request.method == "GET":
        return render_template("preflight.html",
                               page="preflight",
                               user=current_user,
                               aircraft=ac,
                               today=today,
                               fuel_bfwd=fuel_bfwd,
                               fuel_dep=fuel_dep,
                               pilot_name=pilot_rec,
                               crew_name=crew_name)
    else:
        pax = request.form.get("pax")
        print(pax)
        new_pax = passenger(name_first=pax, name_last=pax)
        db.session.add(new_pax)
        db.session.commit()
        return redirect(url_for('views.preflight'))


@views.route("/postflight", methods=["GET", "POST"])
@login_required
def postflight():
    return render_template("postflight.html", page="postflight", user=current_user)


@views.route("/records", methods=["GET", "POST"])
@login_required
def records():
    airports = airport.query.first()
    crew_name = crew.query.filter_by(name_last='Barlow').first()
    crew_data = crew.query.all()
    return render_template("records.html",
                           page="records",
                           user=current_user,
                           airports=airports,
                           crew_name=crew_name,
                           crew_data=crew_data)
