import numpy as np 
import base64

from concurrent import futures
import logging

import grpc
import yolox_pb2, yolox_pb2_grpc

from utils import predict


class Greeter(yolox_pb2_grpc.YoloxServicer):

    def Inference(self, request, context):
        results = predict(request.b64image)
        encoded_results = base64.b64encode(results)

        return yolox_pb2.Prediction(bbox_arr=b"abc") # 결과 반환

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    yolox_pb2_grpc.add_YoloxServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()