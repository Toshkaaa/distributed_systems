from flask import Flask
import sys
import hazelcast
import threading


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


if __name__ == "__main__":

    thread_handle = threading.Thread(target=consume_data)
    thread_handle.start()
    #thread_handle.join()
    port_to_run = sys.argv[1]
    app.run(port=port_to_run)


