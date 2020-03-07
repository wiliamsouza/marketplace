"""Load test code."""
import datetime
import random
import time
from copy import copy

import grpc
import grpc.experimental.gevent
from faker import Faker
from google.type.date_pb2 import Date
from locust import HttpLocust, Locust, TaskSet, between, events, task
from prettyconf import config

from promotion.grpc.v1alpha1.promotion_api_pb2 import CreateUserRequestResponse
from promotion.grpc.v1alpha1.promotion_api_pb2_grpc import PromotionAPIStub

grpc.experimental.gevent.init_gevent()

USERS = [
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
USERS_TO_BE_CREATED = copy(USERS)


class GRPCLocust(Locust):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        channel = grpc.insecure_channel(self.endpoint)
        self.client = PromotionAPIStub(channel)


class User(TaskSet):
    def create_user(self):
        start_time = time.time()
        try:
            user_id = USERS_TO_BE_CREATED.pop()
        except IndexError:
            return

        date = datetime.date.today()
        birthday = Date(year=date.year, month=date.month, day=date.day)
        request = CreateUserRequestResponse(
            user_id=str(user_id).encode(), date_of_birth=birthday
        )
        try:
            response = self.client.CreateUser(request)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="gRPC",
                name="create_user",
                response_time=total_time,
                exception=e,
                response_length=0,
            )

    tasks = {create_user: 1}


class Promotion(GRPCLocust):
    endpoint = config("PROMOTION_GRPC_ENDPOINT", cast=str)
    task_set = User
    wait_time = between(5, 15)


class Product(TaskSet):
    def list_products(self):
        user_id = random.choice(USERS)
        headers = {"X-USER-ID": user_id}
        self.client.get("/v1beta1/cataloging/products", headers=headers)

    def create_product(self):
        fake = Faker()
        product = {
            "title": fake.catch_phrase(),
            "description": fake.text(),
            "price_in_cents": random.choice(range(0, 1000)),
        }
        self.client.post("/v1beta1/cataloging/products")

    tasks = {list_products: 2, create_product: 1}


class Cataloging(HttpLocust):
    task_set = Product
    wait_time = between(5, 15)
