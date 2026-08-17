from confluent_kafka import Producer
from uuid import UUID
import json
import socket

# producer configuration
conf: dict = {
  'bootstrap.servers': 'localhost:9092',
  'client.id': socket.gethostname()
}

producer: Producer = Producer(conf)

def publish_user_created_event(user_id: UUID) -> None:
  event: dict = {
    "event": "user.created",
    "user_id": str(user_id)
  }

  producer.produce(
    "user-events",
    key=str(user_id),
    value=json.dumps(event)
  )

  producer.flush()