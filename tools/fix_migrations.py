import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / 'db.sqlite3'
if not DB.exists():
    print('DB not found:', DB)
    raise SystemExit(1)

conn = sqlite3.connect(str(DB))
c = conn.cursor()
print('Before:', c.execute("SELECT app, name FROM django_migrations WHERE app='messaging'").fetchall())
# Delete the messaging migration record
c.execute("DELETE FROM django_migrations WHERE app='messaging' AND name='0001_initial'")
conn.commit()
print('Deleted messaging migration record')
print('After:', c.execute("SELECT app, name FROM django_migrations WHERE app='messaging'").fetchall())
conn.close()
