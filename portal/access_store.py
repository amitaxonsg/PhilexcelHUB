"""Private AI overrides and audit, separate from NAS/SharePoint provisioning."""
import json, sqlite3
from datetime import datetime, timezone

class AccessStore:
 def __init__(self, path):
  self.path=path
  with self.connect() as db:
   db.execute('CREATE TABLE IF NOT EXISTS ai_access (oid TEXT PRIMARY KEY, settings TEXT NOT NULL)')
   db.execute('CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, at TEXT, actor TEXT, target TEXT, before_value TEXT, after_value TEXT)')
 def connect(self): return sqlite3.connect(self.path, timeout=15)
 def get(self, oid):
  with self.connect() as db:
   row=db.execute('SELECT settings FROM ai_access WHERE oid=?',(oid,)).fetchone()
  return json.loads(row[0]) if row else {}
 def set(self, actor, oid, value):
  serialized=json.dumps(value,sort_keys=True)
  with self.connect() as db:
   row=db.execute('SELECT settings FROM ai_access WHERE oid=?',(oid,)).fetchone()
   db.execute('INSERT INTO ai_access VALUES (?,?) ON CONFLICT(oid) DO UPDATE SET settings=excluded.settings',(oid,serialized))
   db.execute('INSERT INTO audit (at,actor,target,before_value,after_value) VALUES (?,?,?,?,?)',
    (datetime.now(timezone.utc).isoformat(),actor,oid,row[0] if row else '{}',serialized))
