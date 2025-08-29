import json
import urllib.parse
from kafka import KafkaConsumer
import psycopg2

# --- CHANGE THESE TO MATCH YOUR POSTGRES ---
DB_USER = "postgres"
DB_PASSWORD = "pavan"      # <- put your real password
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "eventsdb"       # we'll create this below
# ------------------------------------------

TOPIC = "orders"

def pg_conn():
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )

# ensure DB/table exist (run once at startup)
def setup_db():
    # connect to default "postgres" DB to create eventsdb if needed
    conn = psycopg2.connect(
        dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s;", (DB_NAME,))
    if cur.fetchone() is None:
        cur.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"🆕 created database {DB_NAME}")
    cur.close(); conn.close()

    # create table in eventsdb
    conn = pg_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
      order_id    VARCHAR(40) PRIMARY KEY,
      customer_id VARCHAR(40),
      amount      NUMERIC(10,2),
      ts          TIMESTAMPTZ
    );
    """)
    conn.commit()
    cur.close(); conn.close()
    print("✅ table ready")

def main():
    setup_db()

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers="localhost:9092",
        group_id="orders_group_1",
        auto_offset_reset="earliest",
        value_deserializer=lambda b: json.loads(b.decode("utf-8")),
        key_deserializer=lambda b: b.decode("utf-8") if b else None,
        enable_auto_commit=True,
    )

    conn = pg_conn()
    cur = conn.cursor()
    print("👂 listening… (Ctrl+C to stop)")
    for msg in consumer:
        data = msg.value
        cur.execute("""
            INSERT INTO orders (order_id, customer_id, amount, ts)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING;
        """, (data["order_id"], data["customer_id"], data["amount"], data["ts"]))
        conn.commit()
        print(f"← saved to Postgres | {data}")

if __name__ == "__main__":
    main()