import vk_api
from datetime import datetime
from flask import render_template, session, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user

from .. import db
from ..models import User
from . import main
from .credentials import APP_ID, CLIENT_SECRET


redirect_uri = "http://127.0.0.1:5000/signup"


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('.home'))

    return render_template('index.html', redirect_uri=redirect_uri)


@main.route('/signup', methods=['GET'])
def signup():

    code = request.args.get('code')
    vk_session = vk_api.VkApi(app_id=APP_ID, client_secret=CLIENT_SECRET)
    vk_session.code_auth(code, redirect_uri)
    vk = vk_session.get_api()
    vk_id = vk_session.token['user_id']
    vk_token = vk_session.token['access_token']
    session['vk_token'] = vk_token

    user = User.query.filter_by(social_id=vk_id).first()
    if user is None:
        user = User(social_id=vk_id, social_token=vk_token)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('.home'), code=302)


@main.route('/home', methods=['GET', 'POST'])
def home():
    vk_session = vk_api.VkApi(token=current_user.social_token)
    vk = vk_session.get_api()

    groups = vk.groups.get()
    if groups.get('count', 0) > 0:
        groups_ids = groups['items']
    else:
        groups_ids = []

    groups_info_list = vk.groups.getById(group_ids=groups_ids)

    return render_template('home.html', groups_info=groups_info_list)


@main.route('/listing', methods=['GET', 'POST'])
def group_posts():
    breakpoint()
    vk_session = vk_api.VkApi(token=current_user.social_token)
    vk = vk_session.get_api()

    posts = vk.wall.get(owner_id=f"-{2}", count=2)
    if posts.get('count', 0) > 0:
        posts = posts['items']
    else:
        posts = []

    return render_template('group_posts.html', posts=posts)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".index"))
