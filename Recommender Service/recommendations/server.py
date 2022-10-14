from concurrent import futures
import random

import grpc

from recommendations_pb2 import *
import recommendations_pb2_grpc

class RecommendationService(
    recommendations_pb2_grpc.RecommendationsServicer
):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(
            books_for_category, num_results
        )

        return RecommendationResponse(recommendations=books_to_recommend)
from concurrent import futures
import random

import grpc

from recommendations_pb2 import *
import recommendations_pb2_grpc
import pymongo

client = pymongo.MongoClient()
rest_api = client['rest_api']
users = rest_api['users']
class RecommendationService(
    recommendations_pb2_grpc.RecommendationsServicer
):
    def Recommend(self, request, context):
        selected = []
        for user in users.find({"skills": request.skill}, limit = request.max_results):
            print(user)
            selected.append(UserRecommendation(id =  int(user['id'])))
            
        return RecommendationResponse(recommendations=selected)

class PutService(
    recommendations_pb2_grpc.PutServiceServicer
):
    def Put(self, request, context):
        user = {"id": request.id,
        "skills": list(request.skills)}
        users.insert_one(user)
        return PutResponse(status = 200)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    recommendations_pb2_grpc.add_PutServiceServicer_to_server(
        PutService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print('Started')
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
