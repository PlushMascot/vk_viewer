from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        pass
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())

@main.route("/<group_name>")
def display_group(group_name):
    group_name = "etherealgrooves"
    return render_template('home_page.html',
                                 group_name=group_name)


@main.route("/<group_name>/")
def display_query_result(group_name):
    group_name = "etherealgrooves"
    query_params = {}

    url_for(group_name, **query_params)
    return render_template('home_page.html',
                                 group_name=group_name)

