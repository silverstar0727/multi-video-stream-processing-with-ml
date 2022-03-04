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
        results = predict(message.value)

if inference_type == "grpc":
    for msg_idx, message in enumerate(consumer):
        np_arr = np.frombuffer(message.value, dtype=np.uint8)
        cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        byte_arr = base64.b64encode(cv2_img)

        results = grpc_call(byte_arr)

        if msg_idx == 0:
            break

if inference_type == "rest":
    pass
