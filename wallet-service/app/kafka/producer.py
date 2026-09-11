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

def publish_wallet_recharge_successful(user_id: UUID, amount: Decimal) -> None:
  event: dict = {
    "event": "wallet.recharge.successful",
    "user_id": str(user_id),
    "amount": str(amount)
  }

  producer.produce(
    "wallet-events",
    key=str(user_id),
    value=json.dumps(event)
  )

  producer.flush()

def publish_wallet_recharge_failed(user_id: UUID, amount: Decimal) -> None:

  event: dict = {
    "event": "wallet.recharge.failed",
    "user_id": str(user_id),
    "amount": str(amount)
  }

  producer.produce(
    "wallet-events",
    key=str(user_id),
    value=json.dumps(event)
  )

  producer.flush()

def publish_wallet_withdraw_successful(user_id: UUID, amount: Decimal) -> None:
  event: dict = {
    "event": "wallet.withdraw.successful",
    "user_id": str(user_id),
    "amount": str(amount)
  }

  producer.produce(
    "wallet-events",
    key=str(user_id),
    value=json.dumps(event)
  )

  producer.flush()

def publish_wallet_withdraw_failed(user_id: UUID, amount: Decimal) -> None:

  event: dict = {
    "event": "wallet.withdraw.failed",
    "user_id": str(user_id),
    "amount": str(amount)
  }

  producer.produce(
    "wallet-events",
    key=str(user_id),
    value=json.dumps(event)
  )

  producer.flush()