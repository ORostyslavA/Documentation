from .interfaces import IOutputStrategy
import json

class ConsoleOutputStrategy(IOutputStrategy):
    def output_message(self, message: str) -> None:
        print(message)

class KafkaOutputStrategy(IOutputStrategy):
    def __init__(self, bootstrap_servers: str, topic: str):
        try:
            from kafka import KafkaProducer
        except ImportError:
            raise ImportError("kafka-python is required for Kafka output strategy")
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def output_message(self, message: str) -> None:
        self.producer.send(self.topic, {'message': message})
        self.producer.flush()