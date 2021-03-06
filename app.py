import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify
import numpy as np

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

#Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def Welcome():
    return(
        f"Welcome to the Hawaii Climate API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>" 
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Convert the query results to a dictionary using date as the key and prcp as the value.
    session = Session(engine)
    results = session.query(measurement).all()
    
    #close session
    session.close()

    prcp = []
    for result in results:
        prcp_dict={}
        prcp_dict["date"] = result.date
        prcp_dict["prcp"] = result.prcp
        prcp.append(prcp_dict)

    #Return the JSON representation of your dictionary.

    return jsonify(prcp)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    stations = session.query(station.station, station.name).all()
    
    session.close()
    
    station_names = list(np.ravel(stations))

    return jsonify(station_names)


#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    date_query = session.query(measurement.date).\
        filter(measurement.station == "USC00519281").\
        order_by(measurement.date.desc()).first()[0]
    print(date_query)
    year_ago = dt.date(2017, 8, 18) - dt.timedelta(days=365)
    #year_ago = dt.date(date_query) - dt.timedelta(days=365)

    temp = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date > year_ago).all()

    tobs = []
    for result in temp:
        tobs_dict={}
        tobs_dict["date"] = result.date
        tobs_dict["tobs"] = result.tobs
        tobs.append(tobs_dict)
    # Convert list of tuples into normal list
    #temp_list = list(np.ravel(temp))

    return jsonify(tobs)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
#for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
def start_date(start):
    #start_date = dt.datetime.strftime(start,"%y-%m-%d")
    
    session = Session(engine)
    temp_summary = session.query(func.max(measurement.tobs), func.min(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date > start).all()
    
    session.close()

    start_temp = []
    date_dict={}
    date_dict["TMAX"] = temp_summary[0][0]
    date_dict["TMIN"] = temp_summary[0][1]
    date_dict["TAVG"] = temp_summary[0][2]
    start_temp.append(date_dict)

    #summary = list(np.ravel(temp_summary))

    return jsonify(start_temp)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    session = Session(engine)
    temp_summary = session.query(func.max(measurement.tobs), func.min(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date > start).filter(measurement.date < end).all()
    
    session.close()

    start_temp = []
    date_dict={}
    date_dict["TMAX"] = temp_summary[0][0]
    date_dict["TMIN"] = temp_summary[0][1]
    date_dict["TAVG"] = temp_summary[0][2]
    start_temp.append(date_dict)

#Return the JSON representation of your dictionary.
    return jsonify(start_temp)

    

if __name__ == '__main__':
    app.run(debug=True)