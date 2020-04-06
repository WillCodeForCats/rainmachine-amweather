# Ambient Weather Network parser for RainMachine smart sprinkler controller
#
# Feed your personal weather station data from ambientweather.net into your RainMachine
# Requires an API and application key, and the MAC address of your weather station.
#
# Author: Seth Mattinen <seth@mattinen.org>
# 
# 20200405:
#   - Ambient Weather changed backend and started using Cloudflare, which broke stuff
#       * Cloudflare blocks default urllib user-agent
#       * Use http since rainmachine ssl lib doesn't work with cloudflare https
#         (error:14077410:SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure)
#   - Use urllib2 directly so we can have better error logging
#   - Added debug logging to show station data in log (system settings->log level->debug)
#
# 20190324:
#   - first version using data from a WS-2000 with Osprey sensor array
#
# LICENSE: GNU General Public License v3.0
# GitHub: https://github.com/WillCodeForCats/rainmachine-amweather
#

from RMParserFramework.rmParser import RMParser
from RMUtilsFramework.rmLogging import log
from RMUtilsFramework.rmUtils import convertFahrenheitToCelsius,convertInchesToMM,convertRadiationFromWattsToMegaJoules
import json
import urllib, urllib2, ssl



class AmbientWeatherParser(RMParser):
    parserName = "Ambient Weather Network Parser"
    parserDescription = "Live personal weather station data from www.ambientweather.net"
    parserForecast = False
    parserHistorical = True
    parserEnabled = False
    parserDebug = False
    parserInterval = 60 * 60  # hourly

    params = {"apiKey": None
        , "applicationKey": None
        , "macAddress": None}
        
    req_headers = {"User-Agent": "ambientweather-parser/1.0 (https://github.com/WillCodeForCats/rainmachine-amweather)"}
    
    def perform(self):
        
        url = 'http://api.ambientweather.net/v1/devices/' + str(self.params["macAddress"])
        parameterList = [("apiKey", str(self.params["apiKey"]))
            , ("applicationKey", str(self.params["applicationKey"]))
            , ("limit", "1")]

        log.info('Getting data from {0}'.format(str(url)))

        query_string = urllib.urlencode(parameterList)
        url_query = "?" . join([url, query_string])

        try:
            req = urllib2.Request(url=url_query, headers=self.req_headers)
            data = urllib2.urlopen(url=req, timeout=60)
            log.debug("Connected to %s" % (url_query))
        except Exception, e:
            log.error("Error while connecting to %s, error: %s" % (url, e.reason))
            return

        station = json.loads(data.read())
        for entry in station:
            dateutc = entry["dateutc"] / 1000  # from milliseconds

            if 'tempf' in entry:
                temp = convertFahrenheitToCelsius(entry["tempf"])
                self.addValue(RMParser.dataType.TEMPERATURE, dateutc, temp, False)
                log.debug("TEMPERATURE = %s" % (temp))
            
            if 'humidity' in entry:
                self.addValue(RMParser.dataType.RH, dateutc, entry["humidity"], False)
                log.debug("RH = %s" % (entry["humidity"]))
            
            if 'windspeedmph' in entry:
                windspeed = entry["windspeedmph"] * 0.44704  # to meters/sec
                self.addValue(RMParser.dataType.WIND, dateutc, windspeed, False)
                log.debug("WIND = %s" % (windspeed))
            
            if 'solarradiation' in entry:
                solarrad = convertRadiationFromWattsToMegaJoules(entry["solarradiation"])
                self.addValue(RMParser.dataType.SOLARRADIATION, dateutc, solarrad, False)
                log.debug("SOLARRADIATION = %s" % (solarrad))
            
            if 'dailyrainin' in entry:
                rain = convertInchesToMM(entry["dailyrainin"])
                self.addValue(RMParser.dataType.RAIN, dateutc, rain, False)
                log.debug("RAIN = %s" % (rain))
            
            if 'baromrelin' in entry:
                pressure = entry["baromrelin"] * 3.38639  # to kPa
                self.addValue(RMParser.dataType.PRESSURE, dateutc, pressure, False)
                log.debug("PRESSURE = %s" % (pressure))
            
            if 'dewPoint' in entry:
                dewpoint = convertFahrenheitToCelsius(entry["dewPoint"])
                self.addValue(RMParser.dataType.DEWPOINT, dateutc, dewpoint, False)
                log.debug("DEWPOINT = %s" % (dewpoint))
            
        log.info('Successful update from station {0}'.format(str(self.params["macAddress"])))
        return True
