import numpy as np 
import base64

from concurrent import futures
import logging

import grpc
import yolox_pb2, yolox_pb2_grpc

from utils import predict

import base64


class Greeter(yolox_pb2_grpc.YoloxServicer):

    def Inference(self, request, context):
        data = base64.b64decode(request.b64image)
        img_arr = np.frombuffer(data, dtype=np.uint8)
        img_arr = img_arr.reshape(request.width, request.height, -1)

        results = predict(img_arr)
        return yolox_pb2.Prediction(bbox_arr=b"abcdefghijklmnop")

        # encoded_results = base64.b64encode(results)

        # return yolox_pb2.Prediction(bbox_arr=results) # 결과 반환

def serve():
    options = [
        # ('grpc.max_send_message_length', 1024 * 1024 * 1024), 
        ('grpc.max_receive_message_length', 1024 * 1024 * 1024 )
    ]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=options
    )

    yolox_pb2_grpc.add_YoloxServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')

    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()