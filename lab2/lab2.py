import hazelcast
import time
import threading

def task_three(hz_handler):
    test_map = hz_handler.get_map("my_map").blocking()

    print(" --- started writing to the map --- ")

    for i in range(1000):
        test_map.put(i, i)

    print(" --- finished writing to the map --- ")


def publish_m(topic_handler):
    for i in range(100):
        topic_handler.publish(str(i))
        time.sleep(1)


def func_test(event):
    print("Got message:", event.message)
    print("Publish time:", event.publish_time)


def sub_m(topic_handler):
    topic_handler.add_listener(func_test)


def sub_m_with_pause(topic_handler):
   
    print("pausing this subscriber for 10 seconds!")
    time.sleep(10)
    print("renewing this subscriber!")
    topic_handler.add_listener(func_test)


def task_four(hz_handler):
    hz_handler.get_topic("my_topic").destroy()
    topic_handler = hz_handler.get_topic("my_topic").blocking()
    #topic_handler.add_listener(func_test)
    thread_pool = []

    thread_sub1 = threading.Thread(target=sub_m, args=(topic_handler, ))
    thread_pool.append(thread_sub1)
    thread_sub1.start()

    thread_sub2 = threading.Thread(target=sub_m_with_pause, args=(topic_handler,))
    thread_pool.append(thread_sub2)
    thread_sub2.start()

    thread_pub = threading.Thread(target=publish_m, args=(topic_handler,))
    thread_pool.append(thread_pub)
    thread_pub.start()

    
    for thread in thread_pool:
        thread.join()


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


my_queue = hazelcast_client.get_queue("my_queue").blocking()


def produce_in_queue():
    for i in range(100):
        if my_queue.offer("ID:" + str(i)):
            print("[+] offered value: ", str(i))
        else:
            print("[-] value was not added to queue!")
        time.sleep(1)



if __name__ == "__main__":
    

    produce_in_queue()

    hazelcast_client.shutdown()
