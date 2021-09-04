import vk_api
from flask import render_template, session, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user

from .. import db
from ..models import User
from . import main
from .extract_transform import wall_linear_search
from .credentials import APP_ID, CLIENT_SECRET, REDIRECT_URI


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('.home'))

    return render_template('index.html', redirect_uri=REDIRECT_URI)


@main.route('/signup', methods=['GET'])
def signup():

    code = request.args.get('code')
    vk_session = vk_api.VkApi(app_id=APP_ID, client_secret=CLIENT_SECRET)
    vk_session.code_auth(code, REDIRECT_URI)
    vk_id = str(vk_session.token['user_id'])  # returns int otherwise
    vk_token = vk_session.token['access_token']

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

    groups = vk.groups.get(extended=1)
    items = groups['items']
    groups_info_list = []
    for item in items:
        if item['is_closed'] == 0:
            groups_info_list.append({key: item[key] for key in ['id', 'name', 'screen_name', 'photo_50']})

    return render_template('home.html', groups_info=groups_info_list)


@main.route('/<screen_name>', methods=['GET', 'POST'])
def group_posts(screen_name):
    query = dict(request.args)
    query['screen_name'] = screen_name
    vk_session = vk_api.VkApi(token=current_user.social_token)
    vk = vk_session.get_api()

    try:
        posts = wall_linear_search(vk, query)
    except vk_api.exceptions.ApiError:
        return render_template('vk_api.error.html')

    return render_template('group_posts.html', posts=posts)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".index"))
