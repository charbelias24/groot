import Motors as mo     # used to contorl the valves, pump and fans

import Database         # used to acces the database (create, add, delete)

from OnlineHumidity import getHumidity
                        # returns the humidity of the plant passed as a parameter
                        # note that the values are taken from garden.org
                        
from MCP import getADC  # returns the analog value of the sensor located on the
                        # pin number passed as a parameter
                        
from PiTemperature import getCPUTemperature
                        # returns the temperature of the CPU of the Raspberry Pi 

from Ultrasonic import measureUltra
                        # returns the distance to the surface of water of the
                        # water tank using the Ultrasonic sensor
from time import sleep
                        # used to pause the program for specific number of seconds
                        # passed as parameters
                        
from datetime import datetime
                        # used to get the date using datetime.now()


plant1_name = 'daisy'   # used for demonstration purposes
plant2_name = 'rose'

try:

    #gets the humidity group the specific plant from garden.org
    humidity_group1 = getHumidity(plant1_name)
    humidity_group2 = getHumidity(plant2_name)


    plant1_threshold = 50 #default threshold if the plant was not found online
    plant2_threshold = 50

    #assigns the threshold values of the humidity of each plant
    #according to their humidity group
    if humidity_group1 == 'dry mesic' : 
        plant1_threshold = 40

    elif humidity_group1 == 'mesic' :
        plant1_threshold = 60
    
    if humidity_group2 == 'dry mesic' :
        plant2_threshold = 40

    elif humidity_group2 == 'mesic':
        plant2_threshold = 60

    gardener_no = Database.cursor.lastrowid
    
    #creating 2 plants in the database
    plant1_data = (gardener_no, plant1_name)
    plant2_data = (gardener_no, plant2_name)
    Database.cursor.execute(Database.add_plant, plant1_data)
    Database.cursor.execute(Database.add_plant, plant2_data)
    Database.cnx.commit()
    
    
    while True:
        
        plant1_humidityValue = getADC(0)     #get the value of the soil humidity sensor for 
        plant2_humidityValue = getADC(1)     #plants 1 and 2
        print('Sensor 1: '+str(plant1_humidityValue))
        print('Sensor 2: '+str(plant2_humidityValue))

        CPU_temp = getCPUTemperature()

        #gets the current date and time
        measure_date = datetime.now()

        
        #adding the sensor values to the database
        plant1_humidityData = (1, measure_date, plant1_humidityValue)
        plant2_humidityData = (2, measure_date, plant2_humidityValue)
        Database.cursor.execute(Database.add_humidity, plant1_humidityData)
        Database.cursor.execute(Database.add_humidity, plant2_humidityData)
        #Database.cnx.commit()


        # gets the soil humidity of each plant and compares it
        # to the threshold value
        if plant1_humidityValue < plant1_threshold:

            mo.valve1_on()
            mo.pump_on()
            pumpOn = True
        else:
            mo.valve1_off()
            
        if plant2_humidityValue < plant2_threshold:
            mo.valve2_on()
            mo.pump_on()
            pumpOn = True
        else:
            mo.valve2_off()
            
        if plant1_humidityValue > plant1_threshold and plant2_humidityValue > plant2_threshold:
            mo.pump_off()
            pumpOn = False

        if CPU_temp > 60.0 or pumpOn:
            mo.fan1_on()
            mo.fan2_on()

            
        Database.cnx.commit()    
        sleep(10)


        # in case of a keyboard interrupt all the motors stop and the database as well
except KeyboardInterrupt:
    mo.fan1_off()
    mo.fan2_off()
    mo.valve1_off()
    mo.valve2_off()
    mo.pump_off()
    Database.cursor.close()
    Database.cnx.close()

