#Import dependencies including Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Import db and tables
Base = automap_base()
Base.prepare(engine, reflect=True)

measurements = Base.classes.measurement
stations = Base.classes.station

# Create app
app = Flask(__name__)

# Home page: list all routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>TOBS</a><br/>"
        f"<a href='/api/v1.0/<start>'>Start</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>Start/End</a><br/>"
    )

#Precipitations route: convert query to dictionary using date as key/precipitation as value
@app.route("/api/v1.0/precipitation")
def Precipitation():
    # Create session - Python to DB
    session = Session(engine)

    # Query for precipitation
    results = session.query(measurements.date, measurements.prcp).filter(measurements.date >= '2016-08-23').all()
    
    session.close()

    # Create dictionary from row data append
    items_dict = []
    for item in results:
        items = {}
        items["date"] = item[0]
        items["prcp"] = item[1]
        items_dict.append(items)

    # Return JSON
    return jsonify(items_dict)

#Stations route
@app.route("/api/v1.0/stations")
def Stations():
    session = Session(engine)

    # Query stations
    stations_results = session.query(stations.station).all()

    session.close()

    all_stations = list(np.ravel(stations_results))

# Return a JSON list of stations from the dataset.
    return jsonify(all_stations)

#TOBS route: query dates and temp observations of most active station for the last year
@app.route("/api/v1.0/tobs")
def TOBS():
    session = Session(engine)
# 
    tobs_query = session.query(measurements.date,measurements.tobs).filter(measurements.date >= '2016-08-23').filter(measurements.station == 'USC00519281').all()
    session.close()

    tobs_results = list(np.ravel(tobs_query))
# Return list of (TOBS) for the previous year in JSON form
    return jsonify(tobs_results)

#Start route: given only start, calculate TMIN, TAVG, and TMAX for dates past start date
@app.route("/api/v1.0/<start>")
def temperature_start(start):
    session = Session(engine)
# Query dates and temp observations    
    start_results = session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).filter(measurements.date >= '2016-08-23').all()
    
    temp_start = list(np.ravel(start_results))
# Return JSON list of temp observations
    return jsonify(temp_start)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def temperature_start_end(start, end):
    session = Session(engine)
# Query the dates and temperature observations    
    start_end_results = session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).filter(measurements.date >= '2016-08-23').filter(measurements.date <= '2016-08-30').all()
    
    temp_start_end = list(np.ravel(start_end_results))
# Return a JSON list of temperature observations (TOBS).
    return jsonify(temp_start_end)
if __name__ == "__main__":
    app.run(debug=True)