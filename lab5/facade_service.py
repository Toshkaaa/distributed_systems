from flask import request
import requests
import uuid
import random
import hazelcast
import consul

hazelcast_client = hazelcast.HazelcastClient()
my_queue = hazelcast_client.get_queue("my_queue").blocking()


consul_client = consul.Consul(
    host='localhost',
    port=8500,
)


class FacadeService:
    def __init__(self):

        self.WebClients = str((consul_client.kv.get('logging_service_addresses')[1]["Value"]).decode()).split()
        
        self.MessageClients = str((consul_client.kv.get('message_service_addresses')[1]["Value"]).decode()).split()


    def post_req(self):
        message_uuid = uuid.uuid4()
        message_data = request.form.get("message")
        requests.post(self.WebClients[random.randint(0,2)] + "?" + str(message_uuid) + "=" + str(message_data))
        
        my_queue.offer("Message[ " + message_data + " ]")
        print("Message[ " + message_data + " ] was added to Queue!\n")
        
        return "[+] Data has been send to LOGGING SERVICE: " + str(message_data) + " = " + str(message_uuid) + "\n"

    def get_req(self):
        log_serv_req = requests.get(self.WebClients[random.randint(0,2)])
        mess_serv_req = requests.get(self.MessageClients[random.randint(0,1)])

        if log_serv_req.status_code == 200 and mess_serv_req.status_code == 200:
          
            return "\n --- LOGGING_SERVICE response --- \n" + "[+] status code: " + str(log_serv_req.status_code) + "\n" + "[+] response data: " + log_serv_req.text + "\n\n" \
            +  " --- MESSAGES_SERVICE response --- \n" + "[+] status code: " + str(mess_serv_req.status_code) + "\n" + "[+] response data: " + mess_serv_req.text  + "\n\n"
        else:

            return "Error in sending GET request!"

