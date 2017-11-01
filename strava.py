from stravalib.client import Client

class StravaData:
    RUNNER_ID = None
    ACCESS_TOKEN = None
    client = None
    def __init__(runner_id, access_token):
        RUNNER_ID = runner_id
        ACCESS_TOKEN = access_token
        client = Client()
        client.access_token = access_token

    def getAthlete():
        athlete = client.get_athlete()
        return athlete

    def getActivites():
        activities = client.get_activities()
        return activities
