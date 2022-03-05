from kafka import KafkaConsumer, KafkaProducer

import cv2
import numpy as np
import base64
import threading
import json

from utils import predict, grpc_call

class ConsumerThread:
    def __init__(
        self, 
        bootstrap_servers, 
        inference_type="grpc"
    ):
        if inference_type == "local":
            self.client = self.local
        elif inference_type == "grpc":
            self.client = self.grpc
        elif inference_type == "rest":
            self.client = self.rest
        else:
            raise ValueError("잘못된 inference type입니다.")

        self.consumer = KafkaConsumer("VideoStream", bootstrap_servers=bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def _byte_2_img(self, byte_arr):
        np_arr = np.frombuffer(byte_arr, dtype=np.uint8)
        img_arr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        return img_arr

    def _send_results(self, results):
        encoded_results = json.dumps(results).encode('utf-8')
        self.producer.send("ResultStream", encoded_results)


    def rest(self):
        pass

    def grpc(self):
        for msg_idx, message in enumerate(self.consumer):
            img_arr = self._byte_2_img(message.value)
            results = grpc_call(img_arr)
            self._send_results(results)
            print(results)

    def local(self):
        for msg_idx, message in enumerate(self.consumer):
            img_arr = self._byte_2_img(message.value)
            results = predict(img_arr)
            self._send_results(results)

    def run(self, num_threads):
        for _ in range(num_threads):
            t = threading.Thread(target=self.client)
            t.start()

        self.producer.flush()

if __name__ == "__main__":
    consumer_thread = ConsumerThread(
        bootstrap_servers=["34.125.104.58:9091", "34.125.104.58:9092", "34.125.104.58:9093"]
    )

    consumer_thread.run(1)