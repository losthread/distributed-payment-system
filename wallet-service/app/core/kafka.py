from confluent_kafka import Consumer, Producer
from ..crud.wallet import create_wallet
from ..crud.internal_wallet import wallet_credit_money
from uuid import UUID
from decimal import Decimal
import socket
import json

# consumer configuration
consumer_conf: dict = {
  'bootstrap.servers': 'localhost:9092',
  'group.id': 'wallets-service-group',
  'auto.offset.reset': 'earliest',
  'client.id': socket.gethostname()
}

# producer configuration
producer_conf: dict = {
  'bootstrap.servers': 'localhost:9092',
  'client.id': socket.gethostname()
}

consumer: Consumer = Consumer(consumer_conf)
producer: Producer = Producer(producer_conf)

consumer.subscribe(["user-events", "refund-events"])

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
      user_id: UUID = UUID(event.get("user_id"))

      create_wallet(user_id)

      consumer.commit(message)

    elif event["event"] == "refund.requested":
      transaction_id = UUID(event.get("transaction_id"))
      sender_id = UUID(event.get("sender_id"))
      amount = Decimal(event.get("amount"))
      retry_count = event.get("retry_count", 1)

      try:
        wallet_credit_money(sender_id, amount)
        # refund successful -> notify transaction service to update status
        producer.produce(
          "transaction-events",
          key=str(transaction_id),
          value=json.dumps({
            "event": "refund.completed",
            "transaction_id": str(transaction_id)
          })
        )

        producer.flush()
        consumer.commit(message)

      except Exception as e:
        print(f"Refund failed: {e}")

        # retry refund if maximum attempts have not been reached
        if retry_count < 3:
          producer.produce(
            "refund-events",
            key=str(transaction_id),
            value=json.dumps({
              "event": "refund.requested",
              "transaction_id": str(transaction_id),
              "sender_id": str(sender_id),
              "amount": str(amount),
              "retry_count": retry_count + 1
            })
          )

        # max attempts reached but still refund fails -> notify transaction service
        else:
          producer.produce(
            "transaction-events",
            key=str(transaction_id),
            value=json.dumps({
              "event": "refund.failed",
              "transaction_id": str(transaction_id)
            })
          )

        producer.flush()
        consumer.commit(message)