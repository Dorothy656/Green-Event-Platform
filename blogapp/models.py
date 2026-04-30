from datetime import datetime, date
from blogapp import db


# 1. User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    role = db.Column(db.String(20), default="Volunteer", server_default="Volunteer")

    # Profile related
    avatar = db.Column(db.String(256), default="images/default_avatar.png")
    cv_file = db.Column(db.String(256), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    # admin
    is_disabled = db.Column(db.Boolean, default=False)
    disabled_until = db.Column(db.DateTime, nullable=True)
    disabled_reason = db.Column(db.String(255), nullable=True)

    # relationship
    events = db.relationship('Event', backref='organizer', lazy='dynamic')
    participations = db.relationship('Participation', backref='user', lazy='dynamic')
    feedbacks = db.relationship('Feedback', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.username}, Role={self.role}>"

    @property
    def is_currently_banned(self):
        """
        Determine if the user is currently under an active ban.
        Logic: Marked as disabled AND (permanent ban OR ban period not expired)
        """
        if not self.is_disabled:
            return False

        # Permanent ban (is_disabled=True but no end time)
        if self.disabled_until is None:
            return True

        # Temporary ban: Check if current time is still within the ban period
        return datetime.now() < self.disabled_until

    @property
    def ban_remaining_time(self):
        """
        Calculate and return the text description of the remaining ban time.
        """
        if not self.is_disabled:
            return None

        if self.disabled_until is None:
            return "Permanent Ban"

        now = datetime.now()

        # If the ban has expired
        if now > self.disabled_until:
            return "Expired (Awaiting Unban)"

        # Calculate remaining time
        diff = self.disabled_until - now
        days = diff.days
        seconds = diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if days > 0:
            return f"{days} days {hours} hrs"
        elif hours > 0:
            return f"{hours} hrs {minutes} mins"
        else:
            return f"{minutes} mins"

    def unban(self):
        """Perform unban operation"""
        self.is_disabled = False
        self.disabled_until = None
        self.disabled_reason = None


# 2. Event Table
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String(120))

    # Foreign key → organizer
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # relationships
    participants = db.relationship('Participation', backref='event', lazy='dynamic')
    feedbacks = db.relationship('Feedback', backref='event', lazy='dynamic')
    result_summary = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Event {self.title}>"

# 3. Participation Table
class Participation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    hours = db.Column(db.Float, nullable=False)
    participation_date = db.Column(db.Date, default=date.today)

    def __repr__(self):
        return f"<Participation user={self.user_id}, event={self.event_id}, hours={self.hours}>"


# 4. Feedback Table

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    rating = db.Column(db.Integer)  # 1–5 stars
    comment = db.Column(db.Text)

    def __repr__(self):
        return f"<Feedback User={self.user_id}, Event={self.event_id}, Rating={self.rating}>"
