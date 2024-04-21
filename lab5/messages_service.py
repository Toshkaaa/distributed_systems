from flask import Flask
import sys
import hazelcast
import threading
import consul


consul_client = consul.Consul(
    host='localhost',
    port=8500,
)

hazelcast_client = hazelcast.HazelcastClient()
my_queue = hazelcast_client.get_queue("my_queue").blocking()
app = Flask(__name__)

memory_list = []
port_to_run = None

def consume_data():
    while True:
        data_from_queue = my_queue.take()
        print("Consuming {}".format(data_from_queue))
        memory_list.append(data_from_queue)


@app.route('/messages-service', methods= ['GET'])
def handler_function():
    data = " data from client runninng on port " + port_to_run + "\n"
    for i in memory_list:
        data +=  i + " "
    return data


def register_service_in_consul(port_to_run):
    consul_client.agent.service.register(service_id=f"message_service:{port_to_run}", name='messages_service', 
        address='127.0.0.1', port=int(port_to_run),
        check={'service_id': f"message_service:{port_to_run}", 'name': 'messages_service',
            'tcp': f'127.0.0.1:{port_to_run}',
            'Interval': '5s', 'timeout': '2s'})


if __name__ == "__main__":
    port_to_run = sys.argv[1]
    register_service_in_consul(port_to_run)

    thread_handle = threading.Thread(target=consume_data)
    thread_handle.start()
    
    app.run(port=port_to_run)


