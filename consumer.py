from kafka import KafkaConsumer

import cv2
import numpy as np

from utils import predict

bootstrap_servers = ["34.125.104.58:9091", "34.125.104.58:9092", "34.125.104.58:9093"]
consumer = KafkaConsumer("VideoStream", bootstrap_servers=bootstrap_servers)

inference_type = "local"

if inference_type == "local":
    for msg_idx, message in enumerate(consumer):
        np_arr = np.frombuffer(message.value, dtype=np.uint8)
        cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        results = predict(cv2_img)

if inference_type == "grpc":
    pass

if inference_type == "rest":
    pass