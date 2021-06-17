## Dependencies

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

## Import Flask

from flask import Flask, jsonify

## Setup Engine

engine = create_engine("sqlite:\\\Resources\hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

## Enter Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
        f"Temperature stat from the start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature stat from start to end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route('/api/v1.0/<start>')
def get_temp_start(start):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    session.close()

    tobs = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs.append(tobs_dict)

    return jsonify(tobs)

@app.route('/api/v1.0/<start>/<stop>')
def get_temp_start_stop(start,stop):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= stop).all()
    session.close()

    tobs = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs.append(tobs_dict)

    return jsonify(tobs)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    latestdatestring = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    latestdate = dt.datetime.strptime(latestdatestring, '%Y-%m-%d')
    querydate = dt.date(latestdate.year -1, latestdate.month, latestdate.day)
    results = session.query(measurement.date,measurement.tobs).filter(measurement.date >= querydate).all()
    session.close()

    tobs= []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs.append(tobs_dict)

    return jsonify(tobs)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    results = session.query(station.station,station.name,station.latitude,station.longitude,station.elevation).all()
    session.close()

    stations = []
    for station,name,lat,lon,el in queryresults:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = lat
        station_dict["Longitude"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date,measurement.prcp).all()
    session.close()

    prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        prcp.append(prcp_dict)

    return jsonify(prcp)

if __name__ == '__main__':
    app.run(debug=True)