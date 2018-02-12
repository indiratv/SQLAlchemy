# Climate App
# Design a Flask api based on the climate analysis queries
# Use FLASK to create different routes

#Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_

from flask import Flask, jsonify
import datetime as dt
from dateutil.relativedelta import relativedelta
from sqlalchemy import and_


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Save references to the tables
Measurementr  = Base.classes.Measurement 
Stationr = Base.classes.Station

#################################################
# Flask Routes
#################################################
#Welcome Route: List all available api routes.
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Enter a start date in the format yyyy-mm-dd in the url<br/>"
        f"/api/v1.0/<start><br/>"
        f"Enter start and end dates in the format yyyy-mm-dd/yyyy-mm-dd in the url<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#precip Route: Display jsonified response of precipitation data 
#in the last one year
@app.route("/api/v1.0/precipitation")
def precip():
    today = dt.date.today()
    today = dt.date(day=today.day, month=today.month, year=today.year)
    today1yrback = today - relativedelta(days=365)
    results = session.query(Measurementr.date, Measurementr.prcp).filter(and_(Measurementr.date>=today1yrback,Measurementr.date<=today)).all()
    # Convert list of tuples into normal list using np.ravel
    prcp = []
    for result in results:
        prcp_dict = {}
        prcp_dict["date"] = result[0]
        prcp_dict["prcp"] = float(result[1])
        prcp.append(prcp_dict)
    return jsonify(prcp)

#stations Route: Return a json list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    sresults = session.query(Stationr.station,Stationr.name).all()
    station_results = list(np.ravel(sresults))
    return jsonify(station_results)

#tobs Route: Return a json list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    today = dt.date.today()
    today = dt.date(day=today.day, month=today.month, year=today.year)
    today1yrback = today - relativedelta(days=365)
    tresults = session.query(Measurementr.date, Measurementr.tobs).filter(and_(Measurementr.date>=today1yrback,Measurementr.date<=today)).all()
    # Convert list of tuples into normal list using np.ravel
    tobs_results = list(np.ravel(tresults))
    return jsonify(tobs_results)

#tstart route: Return a json list of min,max and avg of tobs data 
#for data collected after a given date(start date)
@app.route("/api/v1.0/<start>")
def tstart(start):
    start_date = start
    import datetime as dt
    sd = dt.datetime.strptime(start_date, '%Y-%m-%d')
    tsresults = session.query(func.min(Measurementr.tobs).label("mintemp"),func.max(Measurementr.tobs).label("maxtemp"),func.avg(Measurementr.tobs).label("avgtemp")).\
    filter(and_(Measurementr.date>sd)).all()
    mintemp = tsresults[0][0]
    maxtemp = tsresults[0][1]
    avgtemp = tsresults[0][2]
    tstart_results = list(np.ravel(tsresults))
    return jsonify(tstart_results)

#tstartend route: Return a json list of min,max and avg of tobs data 
#for data collected between a given range of dates
@app.route("/api/v1.0/<start>/<end>")
def tstartend(start,end):
    sd = dt.datetime.strptime(start, '%Y-%m-%d')
    ed = dt.datetime.strptime(end, '%Y-%m-%d')
    tseresults = session.query(func.min(Measurementr.tobs).label("mintemp"),func.max(Measurementr.tobs).label("maxtemp"),func.avg(Measurementr.tobs).label("avgtemp")).\
    filter(and_(Measurementr.date>=sd,Measurementr.date<=ed)).all()
    mintemp = tseresults[0][0]
    maxtemp = tseresults[0][1]
    avgtemp = tseresults[0][2]
    tstartend_results = list(np.ravel(tseresults))
    return jsonify(tstartend_results)

if __name__ == '__main__':
    app.run(debug=True)