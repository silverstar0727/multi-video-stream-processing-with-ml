from kafka import KafkaProducer
import cv2
from concurrent import futures
import glob
import os
import time

from utils import serializeImg

class ProducerThread:
    def __init__(self, bootstrap_servers=["34.125.104.58:9091", "34.125.104.58:9092", "34.125.104.58:9093"]):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def publish_frame(self, video_path):
        video = cv2.VideoCapture(video_path)
        video_name = os.path.basename(video_path).split(".")[0]
        frame_no = 0

        while video.isOpened():
            _, frame = video.read()

            if frame_no % 3 == 0:
                frame_bytes = serializeImg(frame)
                self.producer.send("VideoStream", frame_bytes)

            time.sleep(0.1)
            frame_no += 1

        video.release()

        self.producer.flush()
        return

    def start(self, vid_paths):
        with futures.ThreadPoolExecutor() as executor:
            executor.map(self.publish_frame, vid_paths)

        self.producer.flush()
        print("finished")

if __name__ == "__main__":
    video_dir = "/home/dojm.ex5/multi-video-stream/videos/"
    video_paths = glob.glob(video_dir + "*.mp4")
    print(video_paths)

    producer_thread = ProducerThread()
    producer_thread.start(video_paths)
    # producer_thread.publish_frame(video_paths)