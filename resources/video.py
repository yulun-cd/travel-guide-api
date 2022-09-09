from flask_restful import Resource
import requests

from cache import cache


class VideoService(Resource):
    
    @cache.cached(timeout=86400)
    def get(self, city):
        api_key = "AIzaSyAxtdmmGs30_2VlCTGFfYLmm99H85RpSdU"
        city = city.replace(" ", "+")
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&key={api_key}&type=video&q={city}+travel"
        
        response = requests.get(url)
        if response.status_code != 200:
            return {'message': 'Internal error. Invalid url'}, 500
        
        result = response.json()
        return {'videos': [f"http://www.youtube.com/embed/{item['id']['videoId']}" for item in result['items']]}, 200