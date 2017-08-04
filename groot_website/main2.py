#this is the main python file for the server to become online

from flask import Flask, render_template
                    # flask is a web micro-framework for creating web applications
from flask_sqlalchemy import SQLAlchemy
                    # used to access the database where the information of
                    # the plants are available
import json
                    # used to convert python into a language that javascript understands

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/WateringSystem'
                    ###################### IMPORTANT ######################
                    # CHANGE THE USERNAME AND PASSWORD INTO VALID ONES
                    # FOR THE PROGRAM TO WORK CORRECTLY
                    
db = SQLAlchemy(app)

                    # creates a class for every table in the database
class Plant(db.Model):      
    __tablename__='plants'
    plant_no = db.Column('plant_no', db.Integer, primary_key = True)
    plant_cname = db.Column('plant_cname', db.Unicode)

    ''' def __init__(self,plant_no,plant_cname):
        self.plant_no = plant_no
        self.plant_cname = plant_cname'''
                    # ^^^ this is used to add plants into the database

        
class Humidity(db.Model):
    __tablename__='soil_humidity'
    humidity_no = db.Column('humidity_no', db.Integer, primary_key = True)
    plant_no = db.Column('plant_no', db.Integer)
    measurement_date = db.Column('measurement_date', db.Date)
    humidity_value = db.Column('humidity_value', db.Integer)
    

plant1_humidityGraph = []
                    # used later to contain the values of the soil 
plant2_humidityGraph = []
                    # moisture of both plants
                    
humid1 = Humidity.query.filter(Humidity.plant_no == 1).all()
                    # filters the values of the soil moisture by plant number 1
for h1 in humid1:
    plant1_humidityGraph.append({"date" : str(h1.measurement_date),
                                         "humidity1" : h1.humidity_value})
                    # adds the values of soil moisture with their corresponding
                    # date to plant1_humidityGraph
                    
humid2 = Humidity.query.filter(Humidity.plant_no == 2).all()
                    # filters the values of the soil moisture by plant number 2
for h2 in humid2:
    plant2_humidityGraph.append({"humidity2" : h2.humidity_value})
                    # adds the values of soil moisture with their corresponding
                    # date to plant2_humidityGraph


@app.route('/')     # ipaddress:5000/
@app.route('/login')# ipaddress:5000/login
def index():
    return render_template('/login.html')
                    # redirect to login.html located in the templates folder


@app.route('/statistics')
                    # ipaddress:5000/statistics
def statistics():
        return render_template('/statistics.html',
                               plant1_humidityGraph_JSON=map(json.dumps, plant1_humidityGraph),
                               plant2_humidityGraph_JSON=map(json.dumps, plant2_humidityGraph),
                               len1 = len(plant1_humidityGraph))
                    # passing the arguments to javascipt
                    # and redirecting to statistics.html
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
                    # running the application
