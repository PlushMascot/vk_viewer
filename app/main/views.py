from datetime import datetime
from flask import render_template, session, redirect, url_for, request
from .. import db
from ..models import User
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/signup', methods=['GET'])
def signup():
    code = request.args.get('code')
    print(code)
    return redirect(url_for('.home'), code=302)


@main.route('/home', methods=['GET'])
def home():
    return render_template('home.html')
