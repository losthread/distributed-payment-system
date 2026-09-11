from ..crud.transactions import update_transaction_status
from confluent_kafka import Consumer
from uuid import UUID
import socket
import json

# consumer configuration
consumer_conf: dict = {
  'bootstrap.servers': 'kafka:9092',
  'group.id': 'transactions-service-group',
  'auto.offset.reset': 'earliest',
  'client.id': socket.gethostname()
}

consumer: Consumer = Consumer(consumer_conf)

consumer.subscribe(["transaction-events"])

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

    if event["event"] == "refund.completed":
      # update transaction status from 'pending' -> 'failed'
      transaction_id = UUID(event.get("transaction_id"))
      update_transaction_status(transaction_id, "failed")
      consumer.commit(message)

    elif event["event"] == "refund.failed":
      # wallet service already published the refund.failed event;
      # transaction service just records the failure status
      transaction_id = UUID(event.get("transaction_id"))
      update_transaction_status(transaction_id, "refund_failed")
      consumer.commit(message)