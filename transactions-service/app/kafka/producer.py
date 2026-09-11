from confluent_kafka import Producer
from uuid import UUID
from decimal import Decimal
import socket
import json

# producer configuration
producer_conf: dict = {
  'bootstrap.servers': 'kafka:9092',
  'client.id': socket.gethostname()
}

producer: Producer = Producer(producer_conf)

def publish_refund_event(transaction_id: UUID, sender_id: UUID, amount: Decimal) -> None:
  event: dict = {
    "event": "refund.requested",
    "transaction_id": str(transaction_id),
    "sender_id": str(sender_id),
    "amount": str(amount)
  }

  producer.produce(
    "refund-events",
    key = str(transaction_id),
    value = json.dumps(event),
    retry = 1,
  )

  producer.flush()

def publish_transaction_successful(transaction_id: UUID, sender_id: UUID, receiver_id: UUID, amount: Decimal):
  event: dict = {
    "event": "payment.successful",
    "transaction_id": str(transaction_id),
    "sender_id": str(sender_id),
    "receiver_id": str(receiver_id),
    "amount": str(amount)
  }

  producer.produce(
    "payment-events",
    key = str(transaction_id),
    value = json.dumps(event)
  )

  producer.flush()

def publish_transaction_pending(transaction_id: UUID, sender_id: UUID, receiver_id: UUID, amount: Decimal):
  event: dict = {
    "event": "payment.pending",
    "transaction_id": str(transaction_id),
    "sender_id": str(sender_id),
    "receiver_id": str(receiver_id),
    "amount": str(amount)
  }

  producer.produce(
    "payment-events",
    key = str(transaction_id),
    value = json.dumps(event)
  )

  producer.flush()

def publish_transaction_failed(transaction_id: UUID, sender_id: UUID, receiver_id: UUID, amount: Decimal):
  event: dict = {
    "event": "payment.failed",
    "transaction_id": str(transaction_id),
    "sender_id": str(sender_id),
    "receiver_id": str(receiver_id),
    "amount": str(amount)
  }

  producer.produce(
    "payment-events",
    key = str(transaction_id),
    value = json.dumps(event)
  )

  producer.flush()

def publish_refund_successful(transaction_id: UUID, sender_id: UUID, amount: Decimal):
  event: dict = {
    "event": "refund.completed",
    "transaction_id": str(transaction_id),
    "sender_id": str(sender_id),
    "amount": str(amount)
  }

  producer.produce(
    "payment-events",
    key = str(transaction_id),
    value = json.dumps(event)
  )

  producer.flush()

  # **refund failed event is already published by wallet service**