import paho.mqtt.client as paho
import time

broker="broker.hivemq.com"
i = 0
j = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Received message: ", str(msg.payload.decode("utf-8")))

# create the client
client = paho.Client("client - 001")
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to Broker")
client.connect(broker)


start = time.perf_counter()

while i <= 100:
    print("subscribing ")
    client.subscribe("heartbeat")
    i += 1

while j <= 100:
    print("publishing ")
    client.publish("heartbeat","heartbeat : 70")
    j += 1

print("Subscriber Thread count : " + str(i))
print("Publisher Thread count : " + str(j))


if (i == j):
    print("100 % Reliability")
elif (i > j):
    print("subscribing lost in middle")
else:
    print("Publisher lost in middle")


end = time.perf_counter() - start
print('{:.6f}s for the calculation'.format(end))

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.disconnect()
client.loop_forever()
