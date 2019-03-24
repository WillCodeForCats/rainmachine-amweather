# Ambient Weather Parser
# Author: Seth Mattinen <sethm@rollernet.us>
#
# Tested with weather stations:
#   * WS-2000 with Osprey sensor array
#
# 20190324:
#   - initial version using data from WS-2000
#

from RMParserFramework.rmParser import RMParser
from RMUtilsFramework.rmLogging import log
from RMUtilsFramework.rmUtils import convertFahrenheitToCelsius,convertInchesToMM,convertRadiationFromWattsToMegaJoules
import json


class AmWeatherParser(RMParser):
    parserName = "Ambient Weather Network Parser"
    parserDescription = "Live personal weather station data from www.ambientweather.net"
    parserForecast = False
    parserHistorical = True
    parserEnabled = False
    parserDebug = False
    parserInterval = 60 * 60 # hourly

    params = {"apiKey": None
        , "applicationKey": None
        , "macAddress": None}

    def perform(self):
        # https://api.ambientweather.net/v1/devices/macAddress?apiKey=&applicationKey=&endDate=&limit=288
        url = 'https://api.ambientweather.net/v1/devices/' + str(self.params["macAddress"])
        parameterList = [("apiKey", str(self.params["apiKey"]))
            , ("applicationKey", str(self.params["applicationKey"]))
            , ("limit", "1")]

        log.info('Getting data from {0}'.format(str(url)))
        data = self.openURL(url, parameterList)

        if data is None:
            self.lastKnownError = "Error: No data received from server"
            log.error(self.lastKnownError)
            return

        staData = json.loads(data.read())
        for staValues in staData:
            dateutc = staValues["dateutc"] / 1000 # from milliseconds
            pressure = staValues["baromabsin"] * 3.38639 # to kPa
            temp = convertFahrenheitToCelsius(staValues["tempf"])
            dewpoint = convertFahrenheitToCelsius(staValues["dewPoint"])
            windspeed = staValues["windspeedmph"] * 0.44704 # to meters/sec
            rain = convertInchesToMM(staValues["hourlyrainin"])
            solarrad = convertRadiationFromWattsToMegaJoules(staValues["solarradiation"])
            self.addValue(RMParser.dataType.TEMPERATURE, dateutc, temp)
            self.addValue(RMParser.dataType.RH, dateutc, staValues["humidity"])
            self.addValue(RMParser.dataType.WIND, dateutc, windspeed)
            self.addValue(RMParser.dataType.SOLARRADIATION, dateutc, solarrad)
            self.addValue(RMParser.dataType.RAIN, dateutc, rain)
            self.addValue(RMParser.dataType.PRESSURE, dateutc, pressure)
            self.addValue(RMParser.dataType.DEWPOINT, dateutc, dewpoint)
            return True


if __name__ == "__main__":
    p = AmWeatherParser()
    p.perform()
