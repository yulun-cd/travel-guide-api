from flask_restful import Resource
import requests
import re

from cache import cache
from helper import country_code_helper
    
    
class WeatherService(Resource):
    
    @cache.cached(timeout=86400)
    def get(self, country, city, date):
        # validate date in the format of YYYY-MM-DD
        if not re.match("^\d{4}\-\d{2}\-\d{2}$", date):
            return {'message': 'Date not valid!'}, 400

        country = country_code_helper(country)
        if not country:
            return {'message': 'Invalid country name or code!'}, 400
            
        # convert city name to coordinate through Geocoding API
        api_key = "9460f45feadc388db6fba14e4bd6af35"
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={api_key}"
        response = requests.get(url)
        result = response.json()
        if not result:
            return {'message': 'No such city found!'}, 400
        
        lat, lon = result[0]['lat'], result[0]['lon']
        
        # use coordinates and date to get weather data from weahter API
        api_key = "26bdae686ce84ace9c465903222508"
        url = f"http://api.weatherapi.com/v1/future.json?key={api_key}&q={lat},{lon}&dt={date}"
        response = requests.get(url)
        result = response.json()
        return result, response.status_code