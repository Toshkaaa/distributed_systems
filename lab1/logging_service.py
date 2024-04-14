from flask import Flask, request

app = Flask(__name__)

dict_hashmap = {}

@app.route('/logging-service', methods= ['POST', 'GET'])
def handler_function():

    if request.method == 'POST':
        key_data = request.args 

        for k in key_data.keys():
            dict_hashmap[k] = key_data[k]
            print(f"[+] Got this message: {key_data[k]}")
            
        return key_data
    
    else:
        msg_list = []
        for k in dict_hashmap.keys():
            msg_list.append(dict_hashmap[k])
        return msg_list


if __name__ == "__main__":
    app.run(port=5001)