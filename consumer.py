from kafka import KafkaConsumer, KafkaProducer

import cv2
import numpy as np
import json

from utils import predict

bootstrap_servers = ["34.125.104.58:9091", "34.125.104.58:9092", "34.125.104.58:9093"]
consumer = KafkaConsumer("VideoStream", bootstrap_servers=bootstrap_servers)
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

for msg_idx, message in enumerate(consumer):
    np_arr = np.frombuffer(message.value, dtype=np.uint8)
    img_arr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = predict(img_arr)
    encoded_results = json.dumps(results).encode('utf-8')

    producer.send("ResultStream", encoded_results)

producer.flush()
