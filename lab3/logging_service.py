from flask import Flask, request
import sys
import hazelcast

app = Flask(__name__)



hazelcastInstance = hazelcast.HazelcastClient()
test_map = hazelcastInstance.get_map("my_map").blocking()

@app.route('/logging-service', methods= ['POST', 'GET'])
def handler_function():
    
    if request.method == 'POST':
        key_data = request.args 

        for k in key_data.keys():
            test_map.put(k, key_data[k])
            print(f"[+] Got this message: {key_data[k]}")
            
        return key_data
    
    else:
        msg_list = []
        for v in test_map.values():
            msg_list.append(v)
        return msg_list


if __name__ == "__main__":
    app.run(port=sys.argv[1])
