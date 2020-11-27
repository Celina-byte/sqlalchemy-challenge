import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# Data base setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
# Flask setup
app = Flask(__name__)
# Routes
@app.route("/")
def home():
    return f"""
        <p>Available routes:</p>
        <p>/api/v1.0/precipitation</p>
        <p>/api/v1.0/stations</p>
        <p>/api/v1.0/tobs</p>
        <p>/api/v1.0/<start> </p>
        <p>/api/v1.0/<start>/<end></p>
    """


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    precipitationfinal=[]
    for date,prcp in results:
        precipitationfinal.append({
            "date":date,
            "precipitation":prcp
        })

    return jsonify(precipitationfinal)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    results = list(np.ravel(results))
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    py=dt.date(2017,8,23)-dt.timedelta(days=365)
    tobs_results = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date>=py).\
        filter(Measurement.station=="USC00519281").\
            group_by(Measurement.date).all()
    tobs_list = list(np.ravel(tobs_results))
    session.close()
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_day(start):
    session = Session(engine)
    start = dt.date(2017,8,23)
    results1 = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    first= list(np.ravel(results1))
    session.close()
    return jsonify(first)

@app.route("/api/v1.0/<start>/<end>")
def start2(start,end):
    session = Session(engine)
    end = dt.date(2017,8,12)
    start = dt.date(2016,5,23)
    results2 = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    second= list(np.ravel(results2))
    session.close()
    return jsonify(second)


if __name__ == "__main__":
    app.run(debug=True)