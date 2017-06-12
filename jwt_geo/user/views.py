# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify, flash, redirect, url_for, request
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies

from .models import User, Location
from .forms import LocationForm

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/')
@jwt_required
def members():
    """List members."""
    current_user = get_jwt_identity()
    return render_template('users/members.html', current_user=current_user)


# Endpoint for revoking the current users access token
@blueprint.route('/logout/', methods=['POST'])
@jwt_required
def logout():
    resp = redirect(url_for('public.home'))
    flash('You are logged out.', 'info')
    unset_jwt_cookies(resp)
    return resp, 200


@blueprint.route('/locations/', methods=['GET', 'POST'])
@jwt_required
def locations():
    """Return user name"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    form = LocationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            location = Location(user_id=user.id)
            form.populate_obj(location)
            location.save()
            return jsonify({"msg": "OK"}), 200
        else:
            return jsonify({"err": "Invalid Data"}), 400

    locations = user.locations.all()
    return jsonify(
        {'locations': [
            {
                'name': l.name or '',
                'street': l.street or '',
                'state': l.state or '',
                'country': l.country or '',
                'pin': l.pin or '',
                'latlng': l.latlng or ''
            } for l in locations
        ]}
    ), 200
