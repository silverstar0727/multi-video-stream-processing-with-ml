from kafka import KafkaConsumer
import cv2
import numpy as np
import io
from PIL import Image
import base64
from utils import predict
import onnxruntime

bootstrap_servers = ["34.125.104.58:9091", "34.125.104.58:9092", "34.125.104.58:9093"]
consumer = KafkaConsumer("VideoStream", bootstrap_servers=bootstrap_servers)

for msg_idx, message in enumerate(consumer):
    np_arr = np.frombuffer(message.value, dtype=np.uint8)
    cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = predict(cv2_img)
    print(results)

    if msg_idx == 1:
        break