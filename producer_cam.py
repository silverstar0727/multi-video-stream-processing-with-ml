import time
import sys
import cv2

from kafka import KafkaProducer
from kafka.errors import KafkaError

def emit_video(path_to_video, producer, topic_name="VideoStream"):
    print('start')

    video = cv2.VideoCapture(path_to_video)

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break

        # png might be too large to emit
        data = cv2.imencode('.jpeg', frame)[1].tobytes()

        future = producer.send(topic, data)
        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)
            break

if __nam__ == "__main__":
    bootstrap_servers=["34.125.104.58:9091", "34.125.104.58:9092", "34.125.104.58:9093"]
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    emit_video(0, producer)