from confluent_kafka import Consumer
from ..crud.wallet import create_wallet
from uuid import UUID
import json

# consumer configuration
conf: dict = {
  'bootstrap.servers': 'localhost:9092',
  'group.id': 'wallet-service-group',
  'auto.offset.reset': 'earliest'
}

consumer: Consumer = Consumer(conf)

consumer.subscribe(["user-events"])

def consume_events():
  while True:
    # wait 1 sec max to receive a new message/event
    message: str = consumer.poll(1.0)

    if message is None:
      continue

    if message.error():
      print(f"Kafka error: {message.error()}")
      continue

    # convert raw byte string -> json -> dict
    event = json.loads(message.value().decode("utf-8"))

    if event["event"] == "user.created":
      user_id: UUID = UUID(event["user_id"])

      create_wallet(user_id)

      consumer.commit(message)