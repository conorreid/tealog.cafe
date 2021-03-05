"""Logged-in page routes."""
from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user

from .forms import TeaAddForm, TeaLogForm
from .models import Tea, TeaLog, User, db

# Blueprint Configuration
main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)


@main_bp.route("/", methods=["GET"])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    user = User.query.filter_by(id=current_user.get_id()).first()
    tea_log_unsorted = [(log.tea.name, log.date.date()) for log in user.tea_log]
    tea_log = sorted(tea_log_unsorted, key=lambda x: x[1], reverse=True)
    return render_template(
        "dashboard.jinja2",
        title="Tea Log",
        template="dashboard-template",
        current_user=current_user,
        tea_log=tea_log,
    )


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for("auth_bp.login"))


@main_bp.route("/create_tea", methods=["GET", "POST"])
@login_required
def create_tea():
    """
    Log-in page for registered users.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in

    form = TeaAddForm()
    # Validate login attempt
    if form.validate_on_submit():
        tea = Tea(
            name=form.name.data,
            price_per_gram=form.price_per_gram.data,
        )
        db.session.add(tea)
        db.session.commit()  # Create new tea
        return redirect(url_for("main_bp.dashboard"))
    return render_template(
        "add_tea.jinja2",
        title="Add a Tea",
        form=form,
        template="add_tea-page",
        body="Add a Tea",
    )


@main_bp.route("/log_tea", methods=["GET", "POST"])
@login_required
def log_tea():
    """
    Log-in page for registered users.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in

    form = TeaLogForm()
    form.tea.choices = [(tea.id, tea.name) for tea in Tea.query.all()]
    # Validate login attempt
    if form.validate_on_submit():
        tea_log = TeaLog(
            tea_id=form.tea.data, date=form.date.data, user_id=current_user.get_id()
        )
        db.session.add(tea_log)
        db.session.commit()  # Create new tea log
        return redirect(url_for("main_bp.dashboard"))
    return render_template(
        "log_tea.jinja2",
        title="Log a Tea",
        form=form,
        template="log_tea-page",
        body="Log a Tea",
    )
