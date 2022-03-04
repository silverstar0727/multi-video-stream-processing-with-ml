from kafka import KafkaConsumer

import cv2
import numpy as np

from utils import predict, grpc_call

bootstrap_servers = ["34.125.104.58:9091", "34.125.104.58:9092", "34.125.104.58:9093"]
consumer = KafkaConsumer("VideoStream", bootstrap_servers=bootstrap_servers)

inference_type = "grpc"

if inference_type == "local":
    for msg_idx, message in enumerate(consumer):
        results = predict(message.value)

if inference_type == "grpc":
    for msg_idx, message in enumerate(consumer):
        results = grpc_call(message.value)

if inference_type == "rest":
    pass
