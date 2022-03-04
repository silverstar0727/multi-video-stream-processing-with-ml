import grpc 
import yolox_pb2, yolox_pb2_grpc

import cv2
import base64

options = [
    ('grpc.max_send_message_length', 1024 * 1024 * 1024), 
    # ('grpc.max_receive_message_length', 1024 * 1024 * 1024 )
]
channel = grpc.insecure_channel("localhost:50051", options)
stub = yolox_pb2_grpc.YoloxStub(channel)

img_arr = cv2.imread("/home/dojm.ex5/multi-video-stream/videos/KOR_DaeguSmartcity_BisanNegeori-E_20211129T075944+0900_00001.jpg", cv2.IMREAD_COLOR)
data = base64.b64encode(img_arr)

request_data = yolox_pb2.B64Image(
    b64image=data, 
    width=img_arr.shape[0], 
    height=img_arr.shape[1]
)
response = stub.Inference(request_data)

print(response.bbox_arr)
