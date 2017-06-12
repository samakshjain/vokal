# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_optional, get_jwt_identity

from jwt_geo.public.forms import LoginForm
from jwt_geo.user.forms import RegisterForm
from jwt_geo.user.models import User
from jwt_geo.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/', methods=['GET', 'POST'])
@jwt_optional
def home():
    """Home page."""
    current_user = get_jwt_identity()
    form = LoginForm(request.form)
    return render_template('public/home.html', form=form, current_user=current_user)


@blueprint.route('/login/', methods=['POST'])
def login():
    """Login and get JWT token"""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        access_token = create_access_token(identity=form.username.data)
        resp = jsonify({'access_token': access_token})
        set_access_cookies(resp, access_token)
        return resp, 200
    else:
        return jsonify({"error": "Bad username or password"}), 401


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)
