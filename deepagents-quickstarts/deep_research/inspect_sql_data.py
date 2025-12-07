import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

def inspect_sql():
    print("--- 🔍 SQL Database Audit ---")
    conn_str = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_str:
        print("❌ POSTGRES_CONNECTION_STRING missing.")
        return

    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()

        # 1. Get Table Names
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = [r[0] for r in cur.fetchall()]
        print(f"📊 Tables found: {tables}")

        for table in tables:
            print(f"\n📋 Table: {table}")
            
            # 2. Get Columns
            cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}';")
            columns = [r[0] for r in cur.fetchall()]
            print(f"   📍 Columns: {columns}")

            # 3. Get Distinct Tickers (if 'ticker' column exists)
            if 'ticker' in columns:
                cur.execute(f"SELECT DISTINCT ticker FROM {table} ORDER BY ticker;")
                tickers = [r[0] for r in cur.fetchall()]
                print(f"   🏢 Tickers Available: {tickers}")
            elif 'companhia_ticker' in columns:
                 cur.execute(f"SELECT DISTINCT companhia_ticker FROM {table} ORDER BY companhia_ticker;")
                 tickers = [r[0] for r in cur.fetchall()]
                 print(f"   🏢 Tickers Available: {tickers}")

        conn.close()

    except Exception as e:
        print(f"❌ SQL Error: {e}")

if __name__ == "__main__":
    inspect_sql()
