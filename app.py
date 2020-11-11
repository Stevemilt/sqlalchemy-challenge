import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

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
        f"Welcome to the Hawaii Climate API"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>" and "/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Convert the query results to a dictionary using date as the key and prcp as the value.
    results = Session.query(measurement).all()
    
    #close sessiont
    session.close()

    prcp = []
    for result in results:
        prcp_dict={}
        prcp_date["date"] = result.date
        prcp_date["prcp"] = result.prcp
        prcp.append(prcp_dict)

    #Return the JSON representation of your dictionary.

    return jsonify(prcp)

#@app.route("/api/v1.0/stations")






    #Return the JSON representation of your dictionary.
