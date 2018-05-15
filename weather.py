import requests, json, datetime, sys, random
import matplotlib.pyplot as plt

# key
with open("APIKEY.txt", "r") as f:
    key = f.read()

class weather:
    def __init__(self, state = "CA", city = "Davis", reportHours = 12):
        url = "http://api.wunderground.com/api/" + key + "/hourly/q/" + state + "/" + city + ".json"
        
        wunderground = json.loads(requests.get(url).text)

        self.hourlyForecast = wunderground["hourly_forecast"]
        self.city = city
        self.state = state
        self.reportHours = reportHours
        self.cleanWeatherInfo() # to clean the data

    def cleanWeatherInfo(self):

        hours = self.hourlyForecast

        # Instantiate.
        times = []
        temps = []
        pops = []
        windSpeeds = []

        # Puts each set of values into array.
        for hour in range(self.reportHours):
            time = str(int(hours[hour]["FCTTIME"]["hour"])%12) + (" PM" if int(hours[hour]["FCTTIME"]["hour"]) > 11 else " AM")
            if time == "0 AM":
                time = "12 AM"
            if time == "0 PM":
                time = "12 PM"

            temp = hours[hour]["temp"]["english"]
            pop = hours[hour]["pop"]
            windSpeed = hours[hour]["wspd"]["english"]

            windSpeeds.append(int(windSpeed))
            pops.append(int(pop))
            times.append(time)
            temps.append(int(temp))

        # Make available to rest of class.
        self.times = times
        self.windSpeeds = windSpeeds
        self.pops = pops
        self.temps = temps

    def createGraph(self):

        times = self.times
        windSpeeds = self.windSpeeds
        pops = self.pops
        temps = self.temps

        # Create the subplot variables.

        fig = plt.figure(figsize=(self.reportHours,4))
        temp = fig.add_subplot(111) # 111 since they're right on each other.
        rain = temp.twinx()

        # Creates the plot.
        rainPlot = rain.bar(times, pops, label = "Rain", color = "blue")
        tempPlot = temp.scatter(times,temps, label = "Temperature", marker = ".",  s= [(windSpeed * 500 ) for windSpeed in windSpeeds])

        # Annotate
        for i, txt in enumerate(windSpeeds):
            temp.annotate(str(txt), (times[i],temps[i]), va="center", ha="center", color = "white", zorder= 500)

        # Labeling.
        temp.set_ylabel('Temperature (F)')
        rain.set_ylabel('Percentage Rain (%)')
        temp.set_xlabel('Time of Day')
        temp.legend([tempPlot, rainPlot], ['Temperature', 'Rain'], bbox_to_anchor=(1, 1),
                   bbox_transform=plt.gcf().transFigure)

        date = datetime.datetime.now().strftime("%A, %B %d")
        plt.title(str(self.reportHours) + "-Hour Report: " + self.city + ", " + self.state + "\n " + date)
        temp.set_zorder(rain.get_zorder()+1)
        plt.ylim((0,100)) # makes sure scale of rain is 0-100
        temp.patch.set_visible(False) # hide the 'canvas'

        filename = 'graphs/' + self.city + '_' + '_'.join(date.split(" ")) + '-' + str(random.randint(1,1000)) + '.png'
        fig.savefig(filename)
        print("sent file name")
        return (filename)
        # plt.show()

def main():
    if len(sys.argv) < 3:
        city = "Los Angeles"
        state = "CA"
        reportHours = 12
    else:
        city = sys.argv[1]
        state = sys.argv[2]
        reportHours = int(sys.argv[3])

    w = weather(state = state, city = city, reportHours = reportHours, key = key)
    w.createGraph()

# main()
