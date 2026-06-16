import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / 'db.sqlite3'
if not DB.exists():
    print('DB not found:', DB)
    raise SystemExit(1)

conn = sqlite3.connect(str(DB))
c = conn.cursor()
print('Existing messaging tables before drop:')
for name in ['messaging_notification','messaging_message']:
    try:
        rows = c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'").fetchall()
        print(name, 'exists' if rows else 'missing')
        if rows:
            c.execute(f"DROP TABLE IF EXISTS {name}")
            print('Dropped', name)
    except Exception as e:
        print('Error checking/dropping', name, e)

conn.commit()
conn.close()
print('Done')
