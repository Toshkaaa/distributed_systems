import hazelcast
import time
import threading


hazelcast_client = hazelcast.HazelcastClient(
    #cluster_name = "dev1",
    cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703",
    ],
    lifecycle_listeners = [
        lambda state: print( "listener status", state)
    ]
)


my_queue = hazelcast_client.get_queue("my_queue")


def consume():

    consumed_count = 0
    while consumed_count < 100: 
        head = my_queue.take().result()
        print("Consuming {}".format(head))
        consumed_count += 1


if __name__ == "__main__":
    
    consume()
    hazelcast_client.shutdown()