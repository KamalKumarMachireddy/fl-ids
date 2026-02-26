# send_test_attack.py
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')

# Test with real CICIDS2018 label formats
test_cases = [
    {"Dst Port": 80, "Protocol": 6, "Label": "Bot"},
    {"Dst Port": 443, "Protocol": 6, "Label": "DDOS attack HOIC"},
    {"Dst Port": 22, "Protocol": 6, "Label": "Brute Force -Web"}
]

for msg in test_cases:
    producer.send('network_traffic', json.dumps(msg).encode('utf-8'))

producer.flush()
print("Test attack messages sent!")