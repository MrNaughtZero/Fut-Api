import requests
import base64

class ExternalRequests():
    def __init__(self):
        self.headers = {
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding" : "gzip, deflate, br",
            "DNT" : "1",
            "Host" : "futbin.org",
            "TE" : "trailers",
            "Upgrade-Insecure-Requests" : "1",
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0"
        }

    def update_prices(self, android_id, device):
        try:
            uri = f"https://www.futbin.org/futbin/api/23/fetchPlayerInformationAndroid?ID={android_id}&platform={device}"
            r = requests.get(uri, headers=self.headers)

            if r.status_code == 304 or r.status_code == 200:
                return r.json()

            return None
        except Exception as e:
            raise Exception(e)

    def update_player_database(self, id):
        try:
            uri = f"https://www.futbin.org/futbin/api/23/fetchPlayerInformationAndroid?ID={id}"
            r = requests.get(uri, headers=self.headers)

            if r.status_code == 304 or r.status_code == 200:
                return r.json()
            elif r.status_code == 404:
                return False

            raise Exception(f"Unable to add new player to database. fut_android_id = {id}")
        except Exception as e:
            raise Exception(e)

    def get_nation_image(self, nation_id):
        try:
            url = f"https://cdn.futbin.com/content/fifa23/img/nation/{nation_id}.png"
            return base64.b64encode(requests.get(url).content).decode("utf-8")
        except Exception as e:
            raise Exception(e)

    def get_league_image(self, league_id):
        try:
            url = f"https://cdn.futbin.com/content/fifa23/img/league/{league_id}.png"
            return base64.b64encode(requests.get(url).content).decode("utf-8")
        except Exception as e:
            raise Exception(e)

    def get_club_image(self, club_id):
        try:
            url = f"https://cdn.futbin.com/content/fifa23/img/clubs/{club_id}.png"
            return base64.b64encode(requests.get(url).content).decode("utf-8")
        except Exception as e:
            raise Exception(e)

    def get_player_image(self, fut_resource_id):
        try:
            url = f"https://cdn.futbin.com/content/fifa23/img/players/{fut_player_id}.png"
            return base64.b64encode(requests.get(url).content).decode("utf-8")
        except Exception as e:
            try:
                url = f"https://cdn.futbin.com/content/fifa23/img/players/p{fut_player_id}.png"
                return base64.b64encode(requests.get(url).content).decode("utf-8") 
            except Exception as e:
                raise Exception(e)