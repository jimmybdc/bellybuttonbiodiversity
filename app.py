# import necessary libraries
from sqlalchemy import func, inspect
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
import sqlalchemy as sq
from sqlalchemy.ext.automap import automap_base

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///belly_button_biodiversity.sqlite"

db = SQLAlchemy(app)

engine = sq.create_engine("sqlite:///belly_button_biodiversity.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Samples = Base.classes.samples

class SampleMetaData(db.Model):
    __tablename__ = 'samples_metadata'

    SAMPLEID = db.Column(db.Integer, primary_key=True)
    AGE = db.Column(db.Integer)
    BBTYPE = db.Column(db.String)
    ETHNICITY = db.Column(db.String)
    GENDER = db.Column(db.String)
    LOCATION = db.Column(db.String)
    WFREQ = db.Column(db.Integer)

class Otu(db.Model):
    __tablename__ = 'otu'
    otu_id = db.Column(db.Integer, primary_key=True)
    lowest_taxonomic_unit_found = db.Column(db.String)

# Create database classes
@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()


#################################################
# Flask Routes
#################################################

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/names")
def sample_names():
    results =  db.session.query(SampleMetaData).all()
    samp_names = []
    for row in results:
        samp_names.append("BB_"+str(row.SAMPLEID))
    return jsonify(samp_names)
@app.route('/otu')
def descriptions():
    results = db.session.query(Otu).all()
    des = []
    for row in results:
        des.append(row.lowest_taxonomic_unit_found)
    return jsonify(des)
@app.route('/metadata/<sample>')
def metasamp(sample):
    results = db.session.query(SampleMetaData).all()
    des = {}
    for row in results:
        if row.SAMPLEID==int(sample[3:]):
            des["AGE"] = row.AGE
            des["BBTYPE"] = row.BBTYPE
            des["ETHNICITY"] = row.ETHNICITY
            des["GENDER"] = row.GENDER
            des["LOCATION"] = row.LOCATION
            des["SAMPLEID"] = row.SAMPLEID
            break
    return jsonify(des)

@app.route('/wfreq/<sample>')
def sampwfreq(sample):
    results = db.session.query(SampleMetaData).all()
    for row in results:
        if row.SAMPLEID==int(sample[3:]):
            return row.WFREQ

@app.route('/samples/<sample>')
def sampVal(sample):
    results = db.session.query(Samples).options(load_only(sample)).order_by(getattr(Samples,sample).desc()).all()
    samples_val = [{"otu_ids":[],"sample_values":[]}]
    for row in results:
        samples_val[0]["otu_ids"].append(row.__dict__["otu_id"])
        samples_val[0]["sample_values"].append(row.__dict__[sample])

    return jsonify(samples_val)

if __name__ == "__main__":
    app.run(debug=True)
