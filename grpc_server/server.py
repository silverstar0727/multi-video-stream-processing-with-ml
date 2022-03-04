import numpy as np 
import base64

from concurrent import futures
import logging

import grpc
import yolox_pb2, yolox_pb2_grpc

def predict(b64img, w, h):
    b64decoded = base64.b64decode(b64img)

    imgarr = np.frombuffer(b64decoded, dtype=np.uint8).reshape(w, h, -1)

    return imgarr.shape[2], np.mean(imgarr)


class Greeter(yolox_pb2_grpc.YoloxServicer):

    def Inference(self, request, context):

        return yolox_pb2.Prediction(bbox_arr='Hello, %s!' % request.b64image) # 결과 반환


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    yolox_pb2_grpc.add_YoloxServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()