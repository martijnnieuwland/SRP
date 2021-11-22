# cd ~/SectorRecords
# . venv/bin/activate
# export FLASK_APP=srp.py
# export FLASK_ENV=development
# flask run


from flask import Flask, request, render_template
from datetime import datetime
psycopg2

db = psycopg2.connect("dbname=learning")
cr = db.cursor()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/preflight/")
def preflight():
    return render_template("preflight.html")


@app.route("/input/", methods=["POST", "GET"])
def input():
    if request.method == "POST":
        if request.form["submit_flight"] == "Submit Preflight":
            return render_template("/preflight")
        elif request.form["submit_flight"] == "Submit Postflight":
            return render_template("/postflight.html")
    elif request.method == "GET":
        return render_template("input.html")


@app.route("/postflight/")
def postflight():
    return render_template("postflight.html")


# @app.route('/input/<int:srp_id>')
# def show_srp(srp_id):
#     cr.execute("SELECT * FROM flights")
#     db.commit()
#     srp_id = cr.fetchall()
#     return render_template('records.html', srp=srp_id)


@app.route("/output/")
def output():
    offblocktime = request.args.get("offblocktime")
    takeofftime = datetime.now()  # request.args.get('takeofftime')
    landingtime = datetime.now()  # request.args.get('landingtime')
    onblocktime = request.args.get("onblocktime")
    blocktime = datetime.strptime(onblocktime, "%H:%M") - datetime.strptime(
        offblocktime, "%H:%M"
    )
    flighttime = (
        datetime.now()
    )  # datetime.strptime(landingtime, '%H:%M') - datetime.strptime(takeofftime, '%H:%M')
    cr.execute(
        "INSERT INTO flights (offblock, takeoff, landing, onblock) "
        "VALUES (%(offblock)s, %(takeoff)s, %(landing)s, %(onblock)s)",
        {
            "offblock": offblocktime,
            "takeoff": takeofftime,
            "landing": landingtime,
            "onblock": onblocktime,
        },
    )

    ac = request.args.get("ac")
    date = request.args.get("date")
    p1 = request.args.get("p1")
    p2 = request.args.get("p2")
    callsign = request.args.get("callsign")
    crew = request.args.get("crew")
    pax = request.args.get("pax")

    cr.execute(
        "INSERT INTO srp (ac, date, p1, p2, callsign, crew, pax) "
        "VALUES (%(ac)s, %(date)s, %(p1)s, %(p2)s, %(callsign)s, %(crew)s, %(pax)s)",
        {
            "ac": ac,
            "date": date,
            "p1": p1,
            "p2": p2,
            "callsign": callsign,
            "crew": crew,
            "pax": pax,
        },
    )
    cr.execute("SELECT id FROM flights ORDER BY id DESC LIMIT 1")
    srp_id = cr.fetchall()
    db.commit()
    return render_template(
        "records.html",
        srp=str(srp_id[0]).strip("(),"),
        offblocktime=offblocktime,
        takeofftime=takeofftime,
        landingtime=landingtime,
        onblocktime=onblocktime,
        blocktime=blocktime,
        flighttime=flighttime,
    )


@app.route("/records")
def listofnumbers():
    return "wtf"
    # cr.execute("SELECT id FROM flights")
    # flight = cr.fetchall()
    # cr.execute("SELECT * FROM srp")
    # results = cr.fetchall()
    # db.commit()
    # cr.execute("SELECT id FROM srp ORDER BY id DESC LIMIT 1")
    # srp_id = str(cr.fetchall()[0]).strip('(),')
    #
    # cr.execute(f"SELECT ac FROM srp WHERE id = {srp_id}")
    # ac = str(cr.fetchall()[0]).strip('\'(),')
    # date = request.args.get('date')
    # p1 = request.args.get('p1')
    # p2 = request.args.get('p2')
    # callsign = request.args.get('callsign')
    # crew = request.args.get('crew')
    # pax = request.args.get('pax')
    # offblocktime = request.args.get('offblocktime')
    # takeofftime = datetime.now()  # request.args.get('takeofftime')
    # landingtime = datetime.now()  # request.args.get('landingtime')
    # onblocktime = datetime.now()  # request.args.get('onblocktime')
    # # cr.execute(f"SELECT onblock FROM flights WHERE id = {srp_id}")
    # # blocktime = cr.fetchall()[0][0]
    # db.commit()
    #
    # blocktime = datetime.now()  # datetime.strptime(onblocktime, '%H:%M') - datetime.strptime(offblocktime, '%H:%M')
    # flighttime = datetime.now()  # datetime.strptime(landingtime, '%H:%M') - datetime.strptime(takeofftime, '%H:%M')
    #
    # return render_template('preflight.html', srp=srp_id, ac=ac, date=date, p1=p1, p2=p2,
    #                        callsign=callsign, crew=crew, pax=pax, offblocktime=offblocktime, takeofftime=takeofftime,
    #                        landingtime=landingtime, onblocktime=onblocktime, blocktime=blocktime, flighttime=flighttime)
