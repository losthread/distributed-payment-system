from confluent_kafka import Consumer
from ..crud.notification import create_notification
import socket
import json

# consumer configuration
consumer_conf: dict = {
  'bootstrap.servers': 'kafka:9092',
  'group.id': 'notification-service-group',
  'auto.offset.reset': 'earliest',
  'client.id': socket.gethostname()
}

consumer: Consumer = Consumer(consumer_conf)

consumer.subscribe(["user-events", "wallet-events", "payment-events", "transaction-events"])

def consumer_events():
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

    if event["event"] in [
      "payment.successful",
      "payment.pending",
      "payment.failed",
      "refund.completed",
      "refund.successful",
      "refund.failed",
      "wallet.recharge.successful",
      "wallet.recharge.failed",
      "wallet.withdraw.successful",
      "wallet.withdraw.failed",
      "user.created",
      "user.logged.in",
    ]:
      create_notification(event)

    consumer.commit(message)