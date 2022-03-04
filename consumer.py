from kafka import KafkaConsumer

import cv2
import numpy as np
import base64

from utils import predict, grpc_call

bootstrap_servers = ["34.125.104.58:9091", "34.125.104.58:9092", "34.125.104.58:9093"]
consumer = KafkaConsumer("VideoStream", bootstrap_servers=bootstrap_servers)

for msg_idx, message in enumerate(consumer):
    results = predict(message.value)
