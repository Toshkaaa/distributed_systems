from flask import Flask, request
import sys
import hazelcast
import consul

app = Flask(__name__)


consul_client = consul.Consul(
    host='localhost',
    port=8500,
)

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


def register_service_in_consul(port_to_run):

    consul_client.agent.service.register(service_id=f"logging_service:{port_to_run}", name='logging_service', 
        address='127.0.0.1', port=int(port_to_run),
        check={'service_id': f"logging_service:{port_to_run}", 'name': 'logging_service',
            'tcp': f'127.0.0.1:{port_to_run}',
            'Interval': '5s', 'timeout': '2s'})



if __name__ == "__main__":

    port_to_run = sys.argv[1]

    register_service_in_consul(port_to_run)

    app.run(port=port_to_run)

