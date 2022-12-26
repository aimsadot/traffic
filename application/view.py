from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import login_required, current_user
from .dal import *

view = Blueprint('view', __name__)


@view.route('/')
@login_required
def home():
    return render_template("home.html", current_user=current_user)


@view.route('/settings', methods=['GET'])
@login_required
def settings():
    flash('Email already exists', category='error')
    areas = [
        {
            "id":1,
            "name": "Area - 1"
        },
        {
            "id": 2,
            "name": "Area - 2"
        },
        {
            "id": 3,
            "name": "Area - 3"
        }
    ]
    return render_template("settings.html", tab=1, areas=areas)


@view.route('/settings-create-rtsp-link', methods=['POST'])
@login_required
def settings_create_rtsp_link():
    if request.method == 'POST':
        rtsp_link = request.form['link'].strip()
        rtsp_link_name = request.form['name'].strip()
        area_id = int(request.form['area_id'].strip())
        error = False
        if not rtsp_link.lower().startswith("rtsp://"):
            flash("Invalid RTSP Link!", category='error')
            error = True
        if len(rtsp_link_name) == 0:
            flash("Empty RTSP name!", category='error')
            error = True

        if not error:
            if not add_media(rtsp_link_name, rtsp_link, StreamType.rtsp, area_id):
                flash("Cannot add rtsp link, already exists or area not found!", category='error')
            else:
                flash("RTSP Link added successfully!", category='success')

    return redirect(url_for('view.settings'))


@view.route('/analytics', methods=['GET'])
@login_required
def analytics():
    return render_template("video.html", page_type="Analytics", media_name="Dummy Video", area_name="Dhaka")


@view.route('/clips', methods=['GET'])
@login_required
def clips():
    return render_template("video.html", page_type="Recorded Clips", media_name="Dummy Clip", area_name="Dhaka")


@view.route('/live', methods=['GET'])
@login_required
def video():
    return render_template("video.html", page_type="Live", media_name="Dummy Live", area_name="Dhaka")
