import sys
import os

# add backend path to sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db import SessionLocal
from app.services.booking_service import create_booking
from datetime import datetime

db = SessionLocal()

print("Existing appointments:")
from app.models.appointment import Appointment
appointments = db.query(Appointment).all()
for a in appointments:
    print(f"Appt {a.id}: provider {a.provider_id}, time {a.appointment_time}, status {a.status}")

try:
    # Let's see what happens if we book at 9 AM for tomorrow
    dt = datetime(2026, 3, 29, 9, 0)
    print(f"Trying to book {dt} (duration 60 mins)")
    b = create_booking(db, user_id=1, provider_id=1, service_id=1, appointment_time=dt, duration_minutes=60)
    print("Success:", b.id)
except Exception as e:
    print("Error:", e)

# Test the 00:00 booking
try:
    dt = datetime(2026, 3, 30, 0, 0)
    print(f"Trying to book {dt} (duration 60 mins)")
    b = create_booking(db, user_id=1, provider_id=1, service_id=1, appointment_time=dt, duration_minutes=60)
    print("Success:", b.id)
except Exception as e:
    print("Error:", e)

try:
    dt = datetime(2026, 3, 29, 10, 0)
    print(f"Trying to book {dt} (duration 60 mins)")
    b = create_booking(db, user_id=1, provider_id=1, service_id=1, appointment_time=dt, duration_minutes=60)
    print("Success:", b.id)
except Exception as e:
    print("Error:", e)
