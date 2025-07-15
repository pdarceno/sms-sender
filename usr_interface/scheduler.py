import sqlite3
from datetime import datetime

DB_PATH = 'scheduled_sms.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scheduled_sms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination TEXT NOT NULL,
        message TEXT NOT NULL,
        scheduled_time TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def schedule_sms(destination, message, scheduled_time):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO scheduled_sms (destination, message, scheduled_time, status) VALUES (?, ?, ?, 'pending')''',
              (destination, message, scheduled_time))
    conn.commit()
    conn.close()

def get_due_sms():
    now = datetime.now().isoformat(timespec='minutes')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT id, destination, message FROM scheduled_sms WHERE status='pending' AND scheduled_time<=?''', (now,))
    rows = c.fetchall()
    conn.close()
    return rows

def mark_sms_sent(sms_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''UPDATE scheduled_sms SET status='sent' WHERE id=?''', (sms_id,))
    conn.commit()
    conn.close()

def get_all_scheduled_sms():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT id, destination, message, scheduled_time, status, created_at FROM scheduled_sms ORDER BY scheduled_time''')
    rows = c.fetchall()
    conn.close()
    return rows

def delete_scheduled_sms(sms_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''DELETE FROM scheduled_sms WHERE id=?''', (sms_id,))
    conn.commit()
    conn.close()

init_db()
