from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

begin = '2016-08-23'
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Calculate the date 1 year ago from the last data point in the database
    latest_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    one_bld = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precip = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_bld)

    #Convert the query results to a dictionary using date as the key and prcp as the value.
    precip_dict = []
    for date, prcp in precip:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        precip_dict.append(prcp_dict)

    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Return a JSON list of stations from the dataset
    stations = session.query(measurement.station).group_by(measurement.station).all()
    
    station_info = list(np.ravel(stations))

    return jsonify(station_info)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query the dates and temperature observations of the most active station for the last year of data.
    one_bld = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).\
    filter(measurement.date >= one_bld).filter(measurement.station == 'USC00519281').all()
    # Return a JSON list of temperature observations (TOBS) for the previous year.
    tobs_list = list(np.ravel(results))
    return jsonify(tobs_list)



@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    day_temp_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= date).all()
    return jsonify(day_temp_results)



@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    session = Session(engine)
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    multi_day_temp_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    return jsonify(multi_day_temp_results)


if __name__ == "__main__":
    app.run(debug=True)
