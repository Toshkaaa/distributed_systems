from flask import request
import requests
import uuid
import random


MESSAGES_SERVICE = "http://localhost:5001/messages-service"

class FacadeService:
    def __init__(self):
        self.WebClients = [
            "http://localhost:5002/logging-service",
            "http://localhost:5003/logging-service",
            "http://localhost:5004/logging-service"
        ]

    def post_req(self):
        message_uuid = uuid.uuid4()
        message_data = request.form.get("message")
        requests.post(self.WebClients[random.randint(0,2)] + "?" + str(message_uuid) + "=" + str(message_data))
        return "[+] Data has been send to LOGGING SERVICE: " + str(message_data) + " = " + str(message_uuid) + "\n"

    def get_req(self):
        log_serv_req = requests.get(self.WebClients[random.randint(0,2)])
        mess_serv_req = requests.get(MESSAGES_SERVICE)
        if log_serv_req.status_code == 200 and mess_serv_req.status_code == 200:
          
            return "\n --- LOGGING_SERVICE response --- \n" + "[+] status code: " + str(log_serv_req.status_code) + "\n" + "[+] response data: " + log_serv_req.text + "\n\n" \
            +  " --- MESSAGES_SERVICE response --- \n" + "[+] status code: " + str(mess_serv_req.status_code) + "\n" + "[+] response data: " + mess_serv_req.text  + "\n\n"
        else:

            return "Error in sending GET request!"

