import os
import six
import sys
import random
import json
import time

from datetime import datetime
from typing import List
from pytz import timezone

# @TODO: Error with that lib using python 3.12
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

import pandas as pd
from faker import Faker
from kafka import KafkaProducer



class OrderProducer:
    def __init__(
            self, 
            language: str = 'pt_BR', 
            timezone_name: str = 'America/Sao_Paulo',
            bootstrap_server: str = 'localhost:9092',
            topic: str = 'orders'
        ):

        self.language = language
        self.timezone_name = timezone_name

        self.faker = Faker(language)
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

        self.selected_timezone = timezone(timezone_name)
        self.products = self.import_products()
        self.clients = self.generate_clients()

    
    def import_products(self) -> List[dict]:
        filepath = os.path.join('data', 'products.json')
        products_df = pd.read_json(filepath)
        products = products_df.to_dict(orient='records')
        return products

    def generate_clients(self) -> List[dict]:
        clients = [
            {
                'name': self.faker.name(),
                'document': self.faker.cpf()
            }
            for _ in range(len(self.products))
        ]
        return clients

    def generate_orders(self) -> List[dict]:
        previous_indexes = set()
        order_quantity = self.faker.random_int(min=0, max=len(self.clients))

        orders = []
        for _ in range(order_quantity):
            item_quantity = self.faker.random_int(min=1, max=len(self.products))
            items = random.sample(self.products.copy(), item_quantity)

            for item in items:
                item['quantity'] = self.faker.random_digit_not_null()

            client_index = self.faker.random_int(min=0, max=len(self.clients) - 1)
            if client_index in previous_indexes:
                continue

            previous_indexes.add(client_index)
            order = {
                'id': self.faker.uuid4(),
                'date': datetime.now(tz=self.selected_timezone).strftime('%Y-%m-%d %H:%M:%s'),
                'client': self.clients[client_index],
                'items': items,
                'total': round(sum([item['quantity'] * item['price'] for item in items]), 2)
            }

            orders.append(order)
        
        return orders
        
    def main(self) -> None:
        print("\033[92m" + "\n-----------------  GERANDO PEDIDOS -----------------\n" + "\033[0m")
        orders = self.generate_orders()
        for order in orders:
            self.producer.send(self.topic, value=order)
            print("\033[94m" + f"\nPedido enviado: {order}\n" + "\033[0m")
            time.sleep(1) 


order_producer = OrderProducer()
attempts = 0
while True:
    try:
        assert attempts <= 5, 'Muitas tentativas inválidas'

        order_producer.main()
        attempts = 0

        time.sleep(5)
    except KeyboardInterrupt:
        print("\033[93m" + "\n-----------------  FINALIZANDO PRODUTOR -----------------\n" + "\033[0m")
        order_producer.producer.close()
        break
    except Exception as error:
        print("\033[91m" + f"\n----------------- ERRO -----------------\n{error}\n" + "\033[0m")
        attempts += 1

        if attempts > 5:
            order_producer.producer.close()
            break
