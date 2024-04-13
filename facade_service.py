from flask import Flask, request
import requests
import uuid


LOGGING_SERVICE = "http://localhost:5001/logging-service"
MESSAGES_SERVICE = "http://localhost:5002/messages-service"


app = Flask(__name__)

@app.route('/facade-service', methods= ['POST', 'GET'])
def handler_function():

    if request.method == 'POST':
        message_uuid = uuid.uuid4()
        message_data = request.form.get("message")
        requests.post(LOGGING_SERVICE + "?" + str(message_uuid) + "=" + str(message_data))
        return "[+] Data has been send to LOGGING SERVICE: " + str(message_data) + " = " + str(message_uuid)
    
    else:
        log_serv_req = requests.get(LOGGING_SERVICE)
        mess_serv_req = requests.get(MESSAGES_SERVICE)
        if log_serv_req.status_code == 200 and mess_serv_req.status_code == 200:
            return "\n --- LOGGING_SERVICE response --- \n" + "[+] status code: " + str(log_serv_req.status_code) + "\n" + "[+] response data: " + log_serv_req.text + "\n\n" \
            +  " --- MESSAGES_SERVICE response --- \n" + "[+] status code: " + str(mess_serv_req.status_code) + "\n" + "[+] response data: " + mess_serv_req.text  + "\n\n"
        else:
            return "Error in sending GET request!"


if __name__ == "__main__":
    app.run()