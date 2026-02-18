import sys
print("Script started...", flush=True)

try:
    from db import engine, Base
    print("DB connection loaded.", flush=True)
except Exception as e:
    print(f"ERROR loading db: {e}", flush=True)
    sys.exit(1)

try:
    import models
    print("Models loaded.", flush=True)
except Exception as e:
    print(f"ERROR loading models: {e}", flush=True)
    sys.exit(1)

try:
    Base.metadata.create_all(bind=engine)
    print("Users table created successfully!", flush=True)
except Exception as e:
    print(f"ERROR creating tables: {e}", flush=True)
    sys.exit(1)
