from kafka import KafkaConsumer
import cv2
import numpy as np


bootstrap_servers = ["34.125.104.58:9091", "34.125.104.58:9092", "34.125.104.58:9093"]
consumer = KafkaConsumer("VideoStream", bootstrap_servers=bootstrap_servers)

for message in consumer:
    # print(message.value)
    # print(dir(message))
    # message.decode("utf-8")
    nparr = np.frombuffer(message.value, dtype=np.uint8)

    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))

    print(img.shape)