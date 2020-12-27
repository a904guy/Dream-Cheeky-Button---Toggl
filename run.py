from windows.control import Dream_Cheeky_Button
from pprint import pprint
import json

with open('credentials.json', 'r') as file:
    config = json.loads(file.read())

class CallBacks:
    id = None
    toggl = None
    endpoints = None
    def __init__(self):
        from toggl.TogglPy import Toggl, Endpoints
        self.toggl = Toggl()
        self.toggl.setAPIKey(config['togglAPIkey'])
        self.endpoints = Endpoints
    
    def open_lid(self):
        data = { 
        "time_entry":
            {
                "description":"Untitled",
                "tags":[],
                "pid": config['togglProjectPID'],
                "created_with":"Dooms Day Button"
            }
        }

        response = json.loads(self.toggl.postRequest("https://api.track.toggl.com/api/v8/time_entries/start", parameters=data))
        self.id = response['data']['id']

    def close_lid(self):

        if self.id:
            response = json.loads(self.toggl.postRequest(self.endpoints.STOP_TIME(self.id)))


DCB = Dream_Cheeky_Button();
callbacks = CallBacks()
DCB.callbacks['LID_OPEN'].append(callbacks.open_lid);
DCB.callbacks['LID_CLOSED'].append(callbacks.close_lid);
DCB.run();