from datetime import date

from flask import render_template, flash, redirect, url_for, session, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import re
from blogapp import app, db
from blogapp.forms import LoginForm, SignupForm, ProfileForm, EventForm, FeedbackForm, ResultForm, JoinForm, AdminRoleForm
from blogapp.models import User, Event, Participation, Feedback
from functools import wraps
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import or_
import os


def login_required(role=None, allow_visitor=False):
    """Decorator to restrict access to logged-in users, optionally allowing visitors."""
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            user_role = session.get('ROLE')

            # Check if user is logged in at all
            if 'USERNAME' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))

            # Block visitor if not allowed for this route
            if user_role == 'Visitor' and not allow_visitor:
                flash('This action requires login. Please log in to continue.', 'warning')
                return redirect(url_for('login'))

            # If a specific role is required
            if role and user_role != role:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@app.route('/')
@app.route('/welcome')
def welcome():
    """Public welcome page, no login required."""
    # If already logged in, redirect to their own homepage
    if session.get('ROLE') in ['Volunteer', 'Organizer', 'Admin']:
        return redirect(url_for('index'))

    # Otherwise, show the public welcome page
    return render_template('welcome.html', title='Welcome')

@app.route('/visitor')
def visitor_entry():
    """Visitor-only entry page."""
    session.clear()
    session['ROLE'] = 'Visitor'
    session['USERNAME'] = 'Visitor'

    # Visitors can only view public event list
    events = Event.query.order_by(Event.date.asc()).all()
    flash('You are browsing as a visitor. Log in to join or create events.')
    return render_template('visitor_index.html', title='Visitor Mode', events=events)
@app.route('/index')
@login_required()
def index():
    username = session['USERNAME']
    role = session['ROLE']
    user_id = session['USER_ID']

    search_query = request.args.get('search', '').strip()
    query = Event.query

    if search_query:
        query = query.filter(
            sa.or_(
                Event.title.ilike(f"%{search_query}%"),
                Event.location.ilike(f"%{search_query}%")
            )
        )

    events = query.order_by(Event.date.asc()).all()

    total_events = Event.query.count()
    total_hours = db.session.query(db.func.sum(Participation.hours)).scalar() or 0
    volunteer_count = User.query.filter_by(role='Volunteer').count()

    leaderboard = (
        db.session.query(User.username, db.func.sum(Participation.hours).label('total_hours'))
        .join(Participation)
        .group_by(User.id)
        .order_by(db.func.sum(Participation.hours).desc())
        .limit(5)
        .all()
    )

    joined_event_ids = [
        p.event_id for p in Participation.query.filter_by(user_id=user_id).all()
    ]

    return render_template(
        'index.html',
        title='Home',
        user={'username': username},
        role=role,
        events=events,
        total_events=total_events,
        total_hours=total_hours,
        volunteer_count=volunteer_count,
        leaderboard=leaderboard,
        joined_event_ids=joined_event_ids,
        search_query=search_query
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page.
    Special handling:
    - If current session is in Visitor mode, clear the session first so that
      visitor users can reach the real login form instead of being redirected
      back and forth between /login and /index.
    """
    # If currently in Visitor mode, treat as not logged in
    if session.get('ROLE') == 'Visitor':
        session.clear()

    # If a real user is already logged in, redirect to homepage directly
    if 'USERNAME' in session and session.get('ROLE') in ['Volunteer', 'Organizer', 'Admin']:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # 1. User does not exist
        if not user:
            app.logger.warning(f"Failed login attempt: Username '{form.username.data}' not found")
            flash(f"No account found for username '{form.username.data}'. Please sign up first.", "error")
            return redirect(url_for('login'))

        # 2. Incorrect password
        if not check_password_hash(user.password_hash, form.password.data):
            app.logger.warning(f"Failed login attempt for user '{user.username}': Incorrect password")
            flash("Incorrect password. Please try again.", "error")
            return redirect(url_for('login'))

        # ==========================================
        # 3. New: Check ban status (Ban Check)
        # ==========================================

        # Scenario A: User is currently banned
        if user.is_currently_banned:
            reason = user.disabled_reason or "Violation of community guidelines"
            remaining = user.ban_remaining_time

            app.logger.warning(f"Banned user '{user.username}' tried to login.")

            # Show ban details
            flash(f"Your account has been banned. Reason: {reason}. Remaining time: {remaining}.", "error")
            return redirect(url_for('login'))

        # Scenario B: User is marked as disabled, but ban period has expired (Auto-unban logic)
        if user.is_disabled and not user.is_currently_banned:
            user.is_disabled = False
            user.disabled_until = None
            user.disabled_reason = None
            db.session.commit()
            app.logger.info(f"User '{user.username}' ban expired. Auto-unbanned during login.")
            # Do not block, proceed to login process below...

        # ==========================================
        # 4. Allow login (Session Setup)
        # ==========================================
        session['USERNAME'] = user.username
        session['USER_ID'] = user.id
        session['ROLE'] = user.role

        app.logger.info(f"User '{user.username}' logged in successfully as {user.role}")
        flash(f"Welcome back, {user.username}! You are logged in as {user.role}.", "success")

        if user.role == 'Admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('index'))

    return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        # 1. Validate password consistency
        if form.password.data != form.password2.data:
            form.password2.errors.append("Passwords do not match.")
            return render_template('signup.html', title='Sign Up', form=form)

        # 2. Validate email format
        email_pattern = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
        if not email_pattern.match(form.email.data.strip()):
            form.email.errors.append("Invalid email format.")
            return render_template('signup.html', title='Sign Up', form=form)

        # 3. Check for existing username
        if User.query.filter_by(username=form.username.data.strip()).first():
            form.username.errors.append("This username is already taken.")
            return render_template('signup.html', title='Sign Up', form=form)

        # 4. Check for existing email
        if User.query.filter_by(email=form.email.data.strip()).first():
            form.email.errors.append("This email is already registered.")
            return render_template('signup.html', title='Sign Up', form=form)

        # 5. Create new user if all checks pass
        passw_hash = generate_password_hash(form.password.data.strip())
        new_user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip(),
            password_hash=passw_hash,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. Please log in to continue.", "success")
        return redirect(url_for('login'))

    # Initial load or validation errors
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/check_username', methods=['POST'])
def check_username():
    """AJAX endpoint: check if a username already exists."""
    data = request.get_json()
    username = data.get('username', '').strip()
    exists = User.query.filter_by(username=username).first() is not None
    return jsonify({'exists': exists})


@app.route('/check_email', methods=['POST'])
def check_email():
    """AJAX endpoint: check if an email already exists."""
    data = request.get_json()
    email = data.get('email', '').strip()
    exists = User.query.filter_by(email=email).first() is not None
    return jsonify({'exists': exists})

@app.route('/profile')
@login_required()
def profile():
    # Get current user
    username = session.get("USERNAME")
    user = User.query.filter_by(username=username).first()

    # Calculate joined or created events
    joined_events = []
    created_events = []
    total_hours = 0

    if user.role == 'Volunteer':
        participations = Participation.query.filter_by(user_id=user.id).all()
        joined_events = [p.event for p in participations]
        total_hours = sum(p.hours for p in participations)
    elif user.role == 'Organizer':
        created_events = Event.query.filter_by(organizer_id=user.id).all()

    return render_template(
        'profile.html',
        title='Profile',
        user=user,
        joined_events=joined_events,
        created_events=created_events,
        total_hours=total_hours
    )
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required()
def edit_profile():
    """Allow users to update all profile information except their role"""

    # Retrieve current logged-in user
    username = session.get("USERNAME")
    user = User.query.filter_by(username=username).first()
    form = ProfileForm(obj=user)

    # Pre-fill form fields
    if request.method == 'GET':
        form.dob.data = user.dob
        form.gender.data = user.gender

    # Prepare upload directories
    avatar_dir = os.path.join(app.root_path, 'static', 'uploads', 'avatars')
    cv_dir = os.path.join(app.root_path, 'static', 'uploads', 'cv')
    os.makedirs(avatar_dir, exist_ok=True)
    os.makedirs(cv_dir, exist_ok=True)

    # Define allowed file extensions
    allowed_image_ext = {'jpg', 'jpeg', 'png'}
    allowed_cv_ext = {'pdf'}

    if form.validate_on_submit():
        new_username = request.form.get('username').strip() if request.form.get('username') else None
        new_email = request.form.get('email').strip() if request.form.get('email') else None
        new_password = request.form.get('password')

        # Check for duplicate username/email
        if new_username and new_username != user.username:
            if User.query.filter_by(username=new_username).first():
                flash('Username already exists. Please choose another one.', 'danger')
                return redirect(url_for('edit_profile'))
            user.username = new_username
            session['USERNAME'] = new_username  # Keep session in sync

        if new_email and new_email != user.email:
            if User.query.filter_by(email=new_email).first():
                flash('Email already registered. Please use a different one.', 'danger')
                return redirect(url_for('edit_profile'))
            user.email = new_email

        # Update password if provided
        if new_password:
            user.password_hash = generate_password_hash(new_password)

        # Save gender and date of birth
        user.gender = form.gender.data
        user.dob = form.dob.data

        # Handle avatar upload
        if form.avatar.data:
            filename = secure_filename(form.avatar.data.filename)
            if filename:
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in allowed_image_ext:
                    avatar_filename = f"{user.username}_avatar.{ext}"
                    avatar_path = os.path.join(avatar_dir, avatar_filename)
                    form.avatar.data.save(avatar_path)
                    user.avatar = f"uploads/avatars/{avatar_filename}"
                else:
                    flash('Invalid avatar type. Only JPG, JPEG, PNG are allowed.', 'danger')
                    return redirect(url_for('edit_profile'))

        # Handle CV upload
        if form.cv.data:
            filename = secure_filename(form.cv.data.filename)
            if filename:
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in allowed_cv_ext:
                    cv_filename = f"{user.username}_CV.{ext}"
                    cv_path = os.path.join(cv_dir, cv_filename)
                    form.cv.data.save(cv_path)
                    user.cv_file = f"uploads/cv/{cv_filename}"
                else:
                    flash('Invalid CV file type. Only PDF is allowed.', 'danger')
                    return redirect(url_for('edit_profile'))

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', title='Edit Profile', form=form, user=user)

@app.route('/delete_account', methods=['POST'])
@login_required()
def delete_account():
    """Delete the current user account and all related data."""
    username = session.get("USERNAME")
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    # Delete related data
    if user.role == 'Volunteer':
        # Delete all participations and feedbacks related to this volunteer
        Participation.query.filter_by(user_id=user.id).delete()
        Feedback.query.filter_by(user_id=user.id).delete()

    elif user.role == 'Organizer':
        # For each event organized by this user, delete related participations and feedbacks
        events = Event.query.filter_by(organizer_id=user.id).all()
        for event in events:
            Participation.query.filter_by(event_id=event.id).delete()
            Feedback.query.filter_by(event_id=event.id).delete()
            db.session.delete(event)

    # Finally delete the user
    db.session.delete(user)
    db.session.commit()

    # Clear session and redirect
    session.clear()
    flash('Your account and all related data have been permanently deleted.', 'danger')
    return redirect(url_for('login'))

@app.route('/choice')
@login_required()
def choice():
    user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
    return render_template('choice.html', user=user_in_db)

@app.route('/join_event/<int:event_id>', methods=['POST'])
@login_required()
def join_event(event_id):
    """Allow volunteers to join an event, then refresh the homepage."""
    user_id = session['USER_ID']
    event = Event.query.get_or_404(event_id)

    # Prevent duplicate participation
    existing = Participation.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing:
        flash('You have already joined this event.', 'info')
        return redirect(url_for('event_detail', event_id=event_id))

    # Add new participation record
    participation = Participation(
        user_id=user_id,
        event_id=event_id,
        hours=0,
        participation_date=date.today()
    )
    db.session.add(participation)
    db.session.commit()

    flash(f'Successfully joined "{event.title}"!', 'success')
    return redirect(url_for('index'))

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
@login_required(allow_visitor=True)
def event_detail(event_id):
    """Show event details.
    - Volunteers: can join & give feedback
    - Organizers/Admins: can manage
    - Visitors: read-only
    """
    event = Event.query.get_or_404(event_id)
    user_role = session.get('ROLE')
    user_id = session.get('USER_ID')
    form = JoinForm()

    already_joined = False
    if user_role not in ['Visitor', None]:
        already_joined = Participation.query.filter_by(
            user_id=user_id, event_id=event_id
        ).first() is not None

    if (
        form.validate_on_submit()
        and user_role == 'Volunteer'
        and not already_joined
    ):
        participation = Participation(
            user_id=user_id,
            event_id=event_id,
            hours=0,
            participation_date=date.today(),
        )
        db.session.add(participation)
        db.session.commit()
        flash(f'You have successfully joined "{event.title}".', 'success')
        return redirect(url_for('event_detail', event_id=event_id))

    participants = event.participants.all()
    feedbacks = Feedback.query.filter_by(event_id=event_id).all()

    return render_template(
        'event_detail.html',
        event=event,
        participants=participants,
        feedbacks=feedbacks,
        already_joined=already_joined,
        form=form,
        user_role=user_role,
    )

@app.route('/feedback/<int:event_id>', methods=['GET', 'POST'])
@login_required()
def feedback(event_id):
    form = FeedbackForm()
    if form.validate_on_submit():
        new_feedback = Feedback(user_id=session['USER_ID'], event_id=event_id,
                                rating=form.rating.data, comment=form.comment.data)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Thank you for your feedback!')
        return redirect(url_for('index'))
    return render_template('volunteer/feedback.html', title='Leave Feedback', form=form)

@app.route('/leaderboard')
@login_required(allow_visitor=True)
def leaderboard():
    """
    Display the volunteer leaderboard.
    Ranks volunteers based on their total participation hours.
    """
    from sqlalchemy import func
    try:
        # Calculate total volunteer hours per user
        results = (
            db.session.query(
                User.username,
                func.coalesce(func.sum(Participation.hours), 0).label('total_hours')
            )
            .join(Participation, User.id == Participation.user_id)
            .filter(User.role == 'Volunteer')
            .group_by(User.id)
            .order_by(func.sum(Participation.hours).desc())
            .all()
        )
        # Convert to a list of dicts for easy rendering
        leaderboard_data = [
            {'username': r[0], 'total_hours': r[1] or 0} for r in results
        ]
    except Exception as e:
        app.logger.error(f"Error loading leaderboard: {e}")
        flash("Unable to load leaderboard data at this time.", "danger")
        leaderboard_data = []
    # Render leaderboard template (Visitor sees read-only)
    return render_template(
        'leaderboard.html',
        title='Leaderboard',
        leaderboard=leaderboard_data
    )

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if session.get('ROLE') != 'Organizer':
        flash("Only organizers can create events.", "danger")
        return redirect(url_for('index'))

    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            date=datetime.combine(form.date.data, datetime.min.time()),
            location=form.location.data,
            organizer_id=session['USER_ID']
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for('organizer_events'))
    return render_template('organizer/create_event.html', title='Create Event', form=form)


@app.route('/organizer/events')
def organizer_events():
    if session.get('ROLE') != 'Organizer':
        flash("Only organizers can access this page.", "danger")
        return redirect(url_for('index'))

    search_query = request.args.get('search', '').strip()

    query = Event.query.filter_by(organizer_id=session['USER_ID'])

    if search_query:
        query = query.filter(
            sa.or_(
                Event.title.ilike(f"%{search_query}%"),
                Event.location.ilike(f"%{search_query}%")
            )
        )

    events = query.order_by(Event.date.asc()).all()

    return render_template(
        'organizer/organizer_events.html',
        title='My Events',
        events=events,
        search_query=search_query
    )

@app.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if session.get('ROLE') != 'Organizer' or event.organizer_id != session['USER_ID']:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('index'))

    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = datetime.combine(form.date.data, datetime.min.time())
        event.location = form.location.data
        db.session.commit()
        flash("Event updated successfully!", "success")
        return redirect(url_for('organizer_events'))
    return render_template('organizer/edit_event.html', form=form, event=event)


@app.route('/event/<int:event_id>/delete')
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if session.get('ROLE') != 'Organizer' or event.organizer_id != session['USER_ID']:
        flash("Unauthorized deletion attempt.", "danger")
        return redirect(url_for('index'))

    db.session.delete(event)
    db.session.commit()
    flash("Event deleted.", "info")
    return redirect(url_for('organizer_events'))

@app.route('/event/<int:event_id>/manage', methods=['GET', 'POST'])
def manage_event(event_id):
    event = Event.query.get_or_404(event_id)
    if session.get('ROLE') != 'Organizer' or event.organizer_id != session['USER_ID']:
        flash("Unauthorized.", "danger")
        return redirect(url_for('index'))

    participants = Participation.query.filter_by(event_id=event.id).all()
    feedbacks = Feedback.query.filter_by(event_id=event.id).all()

    # --- Get volunteers who are NOT in this event ---
    current_participant_ids = [p.user_id for p in participants]
    available_volunteers = (
        User.query
        .filter(User.role == 'Volunteer', ~User.id.in_(current_participant_ids))
        .order_by(User.username.asc())
        .all()
    )

    # ---- Add participant ----
    if request.method == 'POST':
        if 'add_userid' in request.form:
            user_id = int(request.form.get('add_userid'))
            user = User.query.filter_by(id=user_id, role='Volunteer').first()
            if not user:
                flash('User not found or not a Volunteer.', 'danger')
            elif Participation.query.filter_by(user_id=user.id, event_id=event.id).first():
                flash('User already in event.', 'warning')
            else:
                db.session.add(Participation(user_id=user.id, event_id=event.id, hours=0))
                db.session.commit()
                flash(f'Added {user.username} to participants.', 'success')
            return redirect(url_for('manage_event', event_id=event.id))

        # ---- Delete participant ----
        if 'delete_userid' in request.form:
            user_id = int(request.form.get('delete_userid'))
            Participation.query.filter_by(user_id=user_id, event_id=event.id).delete()
            db.session.commit()
            flash(f'Removed participant ID {user_id}.', 'info')
            return redirect(url_for('manage_event', event_id=event.id))

    return render_template(
        'organizer/manage_event.html',
        event=event,
        participants=participants,
        feedbacks=feedbacks,
        available_volunteers=available_volunteers
    )

@app.route('/event/<int:event_id>/participants')
def view_participants(event_id):
    event = Event.query.get_or_404(event_id)
    search_query = request.args.get('search', '').strip()

    participants_query = Participation.query.filter_by(event_id=event.id).join(User)

    if search_query:
        participants_query = participants_query.filter(User.username.ilike(f"%{search_query}%"))

    participants = participants_query.all()

    return render_template(
        'organizer/view_participants.html',
        event=event,
        participants=participants,
        search_query=search_query
    )

@app.route('/event/<int:event_id>/feedback')
def view_feedback(event_id):
    event = Event.query.get_or_404(event_id)
    search_query = request.args.get('search', '').strip()

    feedback_query = Feedback.query.filter_by(event_id=event.id).join(User)

    if search_query:
        feedback_query = feedback_query.filter(
            sa.or_(
                User.username.ilike(f"%{search_query}%"),
                Feedback.comment.ilike(f"%{search_query}%")
            )
        )

    feedbacks = feedback_query.all()

    return render_template(
        'organizer/view_feedback.html',
        event=event,
        feedbacks=feedbacks,
        search_query=search_query
    )

@app.route('/event/<int:event_id>/results', methods=['GET', 'POST'])
def update_results(event_id):
    event = Event.query.get_or_404(event_id)
    if session.get('ROLE') != 'Organizer' or event.organizer_id != session['USER_ID']:
        flash("Unauthorized.", "danger")
        return redirect(url_for('index'))

    form = ResultForm(obj=event)
    participants = Participation.query.filter_by(event_id=event.id).join(User).all()

    if request.method == 'POST' and 'update_hours_userid' in request.form:
        user_id = int(request.form.get('update_hours_userid'))
        new_hours = float(request.form.get('new_hours', 0))
        participation = Participation.query.filter_by(event_id=event.id, user_id=user_id).first()
        if participation:
            participation.hours = new_hours
            db.session.commit()
            flash(f"Updated hours for user ID {user_id} to {new_hours} hrs.", "success")
        return redirect(url_for('update_results', event_id=event.id))

    if form.validate_on_submit():
        event.result_summary = form.result_summary.data
        db.session.commit()
        flash("Event results updated successfully!", "success")
        return redirect(url_for('manage_event', event_id=event.id))

    return render_template(
        'organizer/update_results.html',
        event=event,
        form=form,
        participants=participants
    )


@app.route('/admin_dashboard')
@login_required(role='Admin')
def admin_dashboard():
    """Admin dashboard showing system overview statistics."""
    total_users = User.query.count()
    total_events = Event.query.count()
    total_feedbacks = Feedback.query.count()
    total_volunteers = User.query.filter_by(role='Volunteer').count()
    total_organizers = User.query.filter_by(role='Organizer').count()

    return render_template(
        'admin/admin_dashboard.html',
        title='Admin Dashboard',
        total_users=total_users,
        total_events=total_events,
        total_feedbacks=total_feedbacks,
        total_volunteers=total_volunteers,
        total_organizers=total_organizers
    )


@app.route('/admin_users')
@login_required(role='Admin')
def admin_users():
    """Display all registered users with search and management options."""
    search_query = request.args.get('search', '').strip()
    query = User.query

    if search_query:
        if search_query.isdigit():
            query = query.filter(
                or_(
                    User.id == int(search_query),
                    User.username.ilike(f"%{search_query}%"),
                    User.role.ilike(f"%{search_query}%")
                )
            )
        else:
            query = query.filter(
                or_(
                    User.username.ilike(f"%{search_query}%"),
                    User.role.ilike(f"%{search_query}%")
                )
            )

    users = query.order_by(User.role.asc()).all()

    return render_template(
        'admin/admin_users.html',
        title='Manage Users',
        users=users,
        search_query=search_query
    )

@app.route('/admin_update_role/<int:user_id>', methods=['GET', 'POST'])
@login_required(role='Admin')
def admin_update_role(user_id):
    """Allow admin to change the role of any user"""
    user = User.query.get_or_404(user_id)

    # Default is current role
    form = AdminRoleForm(role=user.role)

    if form.validate_on_submit():
        new_role = form.role.data
        if new_role == 'Admin':
            flash("You cannot assign Admin role.", "danger")
            return redirect(url_for('admin_users'))

        user.role = new_role
        db.session.commit()
        flash(f"Updated role for {user.username} to {user.role}.", "success")
        return redirect(url_for('admin_users'))

    return render_template(
        'admin/admin_update_role.html',
        title='Update User Role',
        form=form,
        user=user
    )
@app.route('/admin_delete_user/<int:user_id>')
@login_required(role='Admin')
def admin_delete_user(user_id):
    """Delete a user and related records."""
    user = User.query.get_or_404(user_id)

    # Avoid deleting other admins
    if user.role == 'Admin':
        flash("Cannot delete another Admin account.", "warning")
        return redirect(url_for('admin_users'))

    # Cascade delete related participations, feedbacks, events
    Participation.query.filter_by(user_id=user.id).delete()
    Feedback.query.filter_by(user_id=user.id).delete()
    Event.query.filter_by(organizer_id=user.id).delete()

    db.session.delete(user)
    db.session.commit()
    flash(f"User '{user.username}' and related records deleted successfully.", "info")
    return redirect(url_for('admin_users'))


@app.route('/admin_events')
@login_required(role='Admin')
def admin_events():
    """Display all events for admin management with flexible search (by ID, title, or organizer username)."""
    search_query = request.args.get('search', '').strip()
    query = Event.query.join(User, Event.organizer_id == User.id, isouter=True)

    if search_query:
        if search_query.isdigit():
            query = query.filter(
                or_(
                    Event.id == int(search_query),
                    Event.title.ilike(f"%{search_query}%"),
                    User.username.ilike(f"%{search_query}%")
                )
            )
        else:
            query = query.filter(
                or_(
                    Event.title.ilike(f"%{search_query}%"),
                    User.username.ilike(f"%{search_query}%")
                )
            )

    events = query.order_by(Event.date.desc()).all()

    return render_template(
        'admin/admin_events.html',
        title='Manage Events',
        events=events,
        search_query=search_query
    )
@app.route('/admin_event/<int:event_id>', methods=['GET', 'POST'])
@login_required(role='Admin')
def admin_edit_event(event_id):
    """Allow admin to manage event details except ID, title, date, and location."""
    event = Event.query.get_or_404(event_id)

    organizer_candidates = User.query.filter_by(role='Organizer').all()

    all_users = User.query.all()

    if request.method == 'POST':
        # ---- Update organizer ----
        organizer_username = request.form.get('organizer', '').strip()
        organizer = User.query.filter_by(username=organizer_username, role='Organizer').first()
        if not organizer:
            flash('Organizer username does not exist or is not an Organizer.', 'danger')
            return redirect(url_for('admin_edit_event', event_id=event.id))
        event.organizer_id = organizer.id

        # ---- Update participants ----
        participants_input = request.form.get('participants', '').strip()
        participants_usernames = [u.strip() for u in participants_input.split(',') if u.strip()]

        Participation.query.filter_by(event_id=event.id).delete()

        for uname in participants_usernames:
            user = User.query.filter_by(username=uname).first()
            if not user:
                flash(f'Participant "{uname}" does not exist.', 'danger')
                return redirect(url_for('admin_edit_event', event_id=event.id))
            new_participation = Participation(user_id=user.id, event_id=event.id, hours=0)
            db.session.add(new_participation)

        db.session.commit()
        flash('Event updated successfully.', 'success')
        return redirect(url_for('admin_events'))

    # ---- For GET ----
    current_participants = ', '.join([p.user.username for p in event.participants if p.user])

    return render_template(
        'admin/admin_event_edit.html',
        title=f'Manage Event #{event.id}',
        event=event,
        organizer_candidates=organizer_candidates,
        all_users=all_users,
        current_participants=current_participants
    )

@app.route('/admin_delete_event/<int:event_id>')
@login_required(role='Admin')
def admin_delete_event(event_id):
    """Allow admin to delete any event and related participations/feedbacks."""
    event = Event.query.get_or_404(event_id)

    Participation.query.filter_by(event_id=event.id).delete()
    Feedback.query.filter_by(event_id=event.id).delete()
    db.session.delete(event)
    db.session.commit()

    flash(f"Event '{event.title}' deleted successfully.", "info")
    return redirect(url_for('admin_events'))


@app.route('/admin_feedback')
@login_required(role='Admin')
def admin_feedback():
    """View all feedback records in the system with flexible search."""
    search_query = request.args.get('search', '').strip()
    query = Feedback.query.join(User, Feedback.user_id == User.id).join(Event, Feedback.event_id == Event.id)

    if search_query:
        if search_query.isdigit():
            query = query.filter(
                or_(
                    Feedback.id == int(search_query),
                    Feedback.rating == int(search_query),
                    User.username.ilike(f"%{search_query}%"),
                    Event.title.ilike(f"%{search_query}%")
                )
            )
        else:
            query = query.filter(
                or_(
                    User.username.ilike(f"%{search_query}%"),
                    Event.title.ilike(f"%{search_query}%"),
                    Feedback.comment.ilike(f"%{search_query}%")
                )
            )

    feedbacks = query.order_by(Feedback.id.desc()).all()
    return render_template('admin/admin_feedback.html',
                           title='All Feedback',
                           feedbacks=feedbacks,
                           search_query=search_query)

@app.route('/admin_feedback/<int:feedback_id>', methods=['GET', 'POST'])
@login_required(role='Admin')
def admin_edit_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if request.method == 'POST':
        feedback.comment = request.form.get('comment')
        feedback.rating = request.form.get('rating', type=int)
        db.session.commit()
        flash(f"Feedback #{feedback.id} updated successfully.", "success")
        return redirect(url_for('admin_feedback'))

    return render_template('admin/admin_feedback_edit.html',
                           title=f"Edit Feedback #{feedback.id}",
                           feedback=feedback)

@app.route('/admin_feedback/delete/<int:feedback_id>', methods=['POST'])
@login_required(role='Admin')
def admin_delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    flash(f"Feedback #{feedback.id} has been deleted.", "warning")
    return redirect(url_for('admin_feedback'))

@app.route('/admin_logs')
@login_required(role='Admin')
def admin_logs():
    """View system logs with filtering by level and keyword search."""
    # Get query parameters
    log_level = request.args.get('level', 'all')
    search_query = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 50  # Display 50 logs per page

    # Log file path
    log_file_path = os.path.join(app.root_path, 'logs', 'app.log')

    logs = []

    try:
        with open(log_file_path, 'r') as f:
            # Read all log lines
            all_logs = f.readlines()

            # Reverse logs to show latest first
            all_logs = all_logs[::-1]

            # Filter logs
            filtered_logs = []
            for log in all_logs:
                # Filter by log level
                if log_level != 'all' and log_level.upper() not in log:
                    continue

                # Filter by keyword search
                if search_query and search_query.lower() not in log.lower():
                    continue

                filtered_logs.append(log)

            # Pagination handling
            total_logs = len(filtered_logs)
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            paginated_logs = filtered_logs[start_idx:end_idx]

            # Format logs: extract time, level, message, etc.
            for log in paginated_logs:
                # Try to parse log format: YYYY-MM-DD HH:MM:SS,mmm - NAME - LEVEL - MESSAGE
                try:
                    # Split log line
                    parts = log.split(' - ', 3)
                    if len(parts) >= 4:
                        log_time_str = parts[0]
                        log_name = parts[1]
                        log_level_str = parts[2]
                        log_message = parts[3].strip()

                        # Parse time
                        log_time = datetime.strptime(log_time_str, '%Y-%m-%d %H:%M:%S,%f')

                        logs.append({
                            'time': log_time,
                            'name': log_name,
                            'level': log_level_str,
                            'message': log_message,
                            'raw': log.strip()
                        })
                    else:
                        # Unparsable log, add directly
                        logs.append({
                            'time': None,
                            'name': 'UNKNOWN',
                            'level': 'UNKNOWN',
                            'message': log.strip(),
                            'raw': log.strip()
                        })
                except Exception as e:
                    # Parsing error, add raw log with error info
                    logs.append({
                        'time': None,
                        'name': 'ERROR',
                        'level': 'ERROR',
                        'message': f"Failed to parse log: {log.strip()}",
                        'raw': log.strip()
                    })

            # Calculate total pages
            total_pages = (total_logs + per_page - 1) // per_page

    except FileNotFoundError:
        logs = []
        total_logs = 0
        total_pages = 0
    except Exception as e:
        logs = [{
            'time': datetime.now(),
            'name': 'ERROR',
            'level': 'ERROR',
            'message': f"Failed to read logs: {str(e)}",
            'raw': f"Failed to read logs: {str(e)}"
        }]
        total_logs = 1
        total_pages = 1

    return render_template(
        'admin/admin_logs.html',
        title='System Logs',
        logs=logs,
        log_level=log_level,
        search_query=search_query,
        page=page,
        per_page=per_page,
        total_logs=total_logs,
        total_pages=total_pages
    )

@app.route('/test_log')
def test_log():
    app.logger.info('This is a test info log')
    app.logger.warning('This is a test warning log')
    app.logger.error('This is a test error log')
    return 'Log test completed'

@app.route('/logout')
@login_required()
def logout():
    session.pop("USERNAME", None)
    session.pop("USER_ID", None)
    session.pop("ROLE", None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/admin/disable_user/<int:user_id>', methods=['POST'])
@login_required(role='Admin')
def disable_user(user_id):
    user = User.query.get_or_404(user_id)

    # 1. Get form data (Using request.form directly is more convenient for Modal handling)
    reason = request.form.get('reason')
    until_str = request.form.get('until')  # Format is usually "2023-12-31T12:00" from datetime-local input

    if not reason:
        flash("Ban reason is required.", "danger")
        return redirect(url_for('admin_users'))

    # 2. Update user status
    user.is_disabled = True
    user.disabled_reason = reason

    # 3. Handle ban until time
    if until_str:
        try:
            # Convert datetime-local string to datetime object
            user.disabled_until = datetime.strptime(until_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash("Invalid time format.", "danger")
            return redirect(url_for('admin_users'))
    else:
        # If no time is provided, it's a permanent ban
        user.disabled_until = None

    db.session.commit()
    flash(f"User {user.username} has been banned.", "warning")
    return redirect(url_for('admin_users'))

# Route: Restore banned user
@app.route('/admin/restore_user/<int:user_id>', methods=['POST'])
@login_required(role='Admin')
def restore_user(user_id):
    user = User.query.get_or_404(user_id)
    user.unban()  # Call the method in the User model
    db.session.commit()
    flash(f"User {user.username} has been restored to normal.", "success")
    return redirect(url_for('admin_users'))