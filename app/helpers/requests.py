import requests

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
        uri = f"https://www.futbin.org/futbin/api/23/fetchPlayerInformationAndroid?ID={android_id}&platform={device}"
        r = requests.get(uri, headers=self.headers)

        if r.status_code == 304 or r.status_code == 200:
            return r.json()

        return None

    def update_player_database(self, id):
        uri = f"https://www.futbin.org/futbin/api/23/fetchPlayerInformationAndroid?ID={id}"
        r = requests.get(uri, headers=self.headers)

        if r.status_code == 304 or r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            return False

        raise Exception(f"Unable to add new player to database. fut_android_id = {id}")
