import requests

class LastFM:
    USER_AGENT = 'AIMS'
    API_KEY = '8e047dd8d6b487dec2bc5e98e5f67f21'
    URL = 'https://ws.audioscrobbler.com/2.0/'
    HEADERS = {'user-agent' : USER_AGENT}
    
    def __init__(self, artist_in, album_in):
        url = self.URL
        
        payload = {
        'method'    : 'album.getinfo',
        'api_key'   : self.API_KEY,
        'artist'    : artist_in,
        'album'     : album_in,
        'format'    : 'json'
        }
        
        response = requests.get(url, headers=self.HEADERS, params=payload)
        self.status_code = response.status_code
        self.album_json = response.json()
        
    
    def get_track_list (self):
        
        track_tags_list = self.album_json['album']['tracks']['track']
        track_list = []
        for track in track_tags_list:
            track_list.append(track['name'])

        return track_list
    
    def get_image_url (self):
        img_url = self.album_json['album']['image'][4]['#text']
        return img_url
    
    def get_genre_list (self):
        genre_tags_list = self.album_json['album']['tags']['tag']
        genre_list = []
        for tag in genre_tags_list:
            genre_list.append(tag['name'])
            
        return genre_list