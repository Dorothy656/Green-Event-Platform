# init_sample_data.py
import os
from datetime import date
from blogapp import app, db
from blogapp.models import User, Event, Participation, Feedback
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    print("✅ New database created!")

    # === Create sample user ===
    alice = User(username="Alice", email="alice@example.com",
                 password_hash=generate_password_hash("123456"), role="Volunteer")
    bob = User(username="Bob", email="bob@example.com",
               password_hash=generate_password_hash("123456"), role="Organizer")
    admin = User(username="Admin", email="admin@example.com",
                 password_hash=generate_password_hash("admin123"), role="Admin")

    db.session.add_all([alice, bob, admin])
    db.session.commit()
    print("✅ Added sample users")

    # ===  Create sample event ===
    event1 = Event(title="Community Tree Planting",
                   description="Join us to plant trees in the local park.",
                   date=date(2025, 12, 1),
                   location="Central Park",
                   organizer=bob)

    event2 = Event(title="Beach Cleanup Drive",
                   description="Help clean the beach and preserve marine life.",
                   date=date(2025, 12, 5),
                   location="Sunny Beach",
                   organizer=bob)

    db.session.add_all([event1, event2])
    db.session.commit()
    print("✅ Added sample events")

    # === 5️⃣ Participation（参与记录） ===
    p1 = Participation(user_id=alice.id, event_id=event1.id, hours=5, participation_date=date(2025, 12, 1))
    p2 = Participation(user_id=alice.id, event_id=event2.id, hours=3, participation_date=date(2025, 12, 5))
    db.session.add_all([p1, p2])
    db.session.commit()
    print("✅ Added sample participation records")

    # === 6️⃣ Feedback（反馈） ===
    f1 = Feedback(user_id=alice.id, event_id=event1.id, rating=5,
                  comment="It was an amazing experience! Learned a lot about environmental care.")
    f2 = Feedback(user_id=alice.id, event_id=event2.id, rating=4,
                  comment="Great teamwork! The beach looks much cleaner now.")
    db.session.add_all([f1, f2])
    db.session.commit()
    print("✅ Added sample feedback records")

    print("\n🎉 Sample data initialization completed successfully!")
