from confluent_kafka import Producer
from uuid import UUID
from decimal import Decimal
import socket
import json

# producer configuration
producer_conf: dict = {
  'bootstrap.servers': 'localhost:9092',
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