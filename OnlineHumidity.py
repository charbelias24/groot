import requests, sys
from bs4 import BeautifulSoup

def getHumidity(plant):
    plant_encoded = plant.replace(' ','+')  #tranform into url encoding

    search_page = 'https://garden.org/plants/search/text/?q=' + plant_encoded
                                            #the url of the kinds of plants found
    page1 = requests.get(search_page)
    soup1 = BeautifulSoup(page1.text, 'html.parser')
    plant_page = soup1.select('td > a')     #get the <a> that exists directly after <td>
    
    if(len(plant_page) == 0):               #if the plant is not found
        print ('This plant does not exist in our database')
        return -1
    else:                                   #if the plant is found
        plant_link = 'https://garden.org' + plant_page[0]['href']
                                            #get the url of the most relevant plant
        page2 = requests.get(plant_link)
        soup2 = BeautifulSoup(page2.text, 'html.parser')
        plant_humidity = soup2.find('span' , attrs = {'class' : 'db_tooltip'})
                                            #gets the soil moisture data if available
        if(plant_humidity):
            print ('Soil Moisture: '+plant_humidity.text)
        else:
            print ('There are no available details about moisture levels')

    return plant_humidity.text

def getScientific(plant):
    pass
