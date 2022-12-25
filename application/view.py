from flask import Blueprint, render_template
from flask_login import login_user, login_required, logout_user, current_user

view = Blueprint('view', __name__)


@view.route('/')
@login_required
def home():
    return render_template("home.html", current_user=current_user)
