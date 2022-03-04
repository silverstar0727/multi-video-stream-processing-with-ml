from kafka import KafkaConsumer

import cv2
import numpy as np
import base64

from utils import predict, grpc_call

bootstrap_servers = ["34.125.104.58:9091", "34.125.104.58:9092", "34.125.104.58:9093"]
consumer = KafkaConsumer("VideoStream", bootstrap_servers=bootstrap_servers)

inference_type = "grpc"

if inference_type == "local":
    for msg_idx, message in enumerate(consumer):
        np_arr = np.frombuffer(message.value, dtype=np.uint8)
        img_arr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        results = predict(img_arr)

if inference_type == "grpc":
    for msg_idx, message in enumerate(consumer):
        np_arr = np.frombuffer(message.value, dtype=np.uint8)
        img_arr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        results = grpc_call(img_arr)
        print(results)

if inference_type == "rest":
    pass
