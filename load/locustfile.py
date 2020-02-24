""" Load test code."""
import datetime
import random
import uuid

from locust import HttpLocust, TaskSet, task

import grpc
from google.type.date_pb2 import Date

from promotion.grpc.v1alpha1.promotion_api_pb2_grpc import PromotionAPIStub
from promotion.grpc.v1alpha1.promotion_api_pb2 import CreateUserRequestResponse

users = [
    "e837c97f-7efa-4b23-84f5-1ce99d80ad79",
    "b0941757-e568-40a1-9a6f-f957dfc0d394",
    "34168233-4bfe-424d-b73e-1818f21016e6",
    "71238906-1d72-4569-8a2a-ca9bf4d53e55",
    "e5af6099-fb70-4284-9178-b7a793f7f32b",
    "6dfb8f79-759d-4658-a122-48b97c75253a",
    "b013785c-9604-4308-969b-5c3b3a971c6f",
    "49fef5ab-90ee-4d2e-a469-97d65a414c51",
    "18de450f-8036-4775-bf6b-aa201ff42891",
    "34140804-8fe9-4a17-ac6e-6b93e111d96e",
]


class Product(TaskSet):
    def list_products(self):
        user_id = random.choice(users)
        self.client.get("/v1beta1/cataloging/products")

    def create_product(self):
        product = {
            "title": "",
            "description": "",
            "price_in_cents": random.choice(range(0, 1000)),
        }
        self.client.post("/v1beta1/cataloging/products")

    """
    def create_user(self):
        with grpc.insecure_channel("promotion:50051") as channel:
            user_id = random.choice(users)
            stub = PromotionAPIStub(channel)
            date = datetime.date.today()
            birthday = Date(year=date.year, month=date.month, day=date.day)
            request = CreateUserRequestResponse(
                user_id=str(user_id).encode(), date_of_birth=birthday
            )
            response = stub.CreateUser(request)
    """

    tasks = {list_products: 1, create_product: 1}


class Cataloging(HttpLocust):
    task_set = Product
    min_wait = 1000
    max_wait = 10000
