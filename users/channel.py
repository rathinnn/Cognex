import grpc
from .recommendations_pb2_grpc import *
from .recommendations_pb2 import *
channel = grpc.insecure_channel("localhost:50051")
recommend_client = RecommendationsStub(channel)
put_client = PutServiceStub(channel)