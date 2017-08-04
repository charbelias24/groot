# creates random graphs and adds them to the database
# only used for demonstration purposes

from datetime import datetime, timedelta
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import random
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/WateringSystem'
                    ###################### IMPORTANT ######################
                    # CHANGE THE USERNAME AND PASSWORD INTO VALID ONES
                    # FOR THE PROGRAM TO WORK CORRECTLY

db = SQLAlchemy(app)


class Humidity(db.Model):
    __tablename__='soil_humidity'
    humidity_no = db.Column('humidity_no', db.Integer, primary_key = True)
    plant_no = db.Column('plant_no', db.Integer)
    measurement_date = db.Column('measurement_date', db.Date)
    humidity_value = db.Column('humidity_value', db.Integer)

    def __init__(self,plant_no, measurement_date, humidity_value):
        self.plant_no=plant_no
        self.measurement_date=measurement_date
        self.humidity_value=humidity_value


value=50

average = []


def getRand(value):
    value += random.randint(-1,1)
    while value < 30 or value > 70:
        value += random.randint(-3,3)
    return value


for i in range(1,3):
    date = datetime.now()-timedelta(minutes=1000)
    current_avg = 0
    for j in range(1000):
            date += timedelta(minutes=1)
            value = getRand(value)
            current_avg += value
            h = Humidity(i, date, value)
            db.session.add(h)
            db.session.commit()
            print j
    average.append(current_avg/1000.0)
for a in average:
    print "average = {}".format(a)
