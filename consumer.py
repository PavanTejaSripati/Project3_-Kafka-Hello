import json, time, random, string
from datetime import datetime
from kafka import KafkaProducer

TOPIC = "orders"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    key_serializer=lambda k: k.encode("utf-8"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def rid(prefix, n=6):
    import secrets
    alphabet = string.ascii_uppercase + string.digits
    return prefix + "-" + "".join(secrets.choice(alphabet) for _ in range(n))

for _ in range(20):
    order = {
        "order_id": rid("ORD"),
        "customer_id": rid("CUST", 4),
        "amount": round(random.uniform(10, 500), 2),
        "ts": datetime.utcnow().isoformat() + "Z",
    }
    producer.send(TOPIC, key=order["customer_id"], value=order)
    print("→ produced:", order)
    time.sleep(0.2)

producer.flush()
print("✅ done producing")
