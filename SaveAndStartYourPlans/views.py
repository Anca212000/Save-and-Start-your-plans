from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import auth
# from .models import Tasks, PeriodTasks, DateTasks
# from . import db

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return redirect(url_for('auth.login'))
    # return render_template("login.html", user=current_user)
