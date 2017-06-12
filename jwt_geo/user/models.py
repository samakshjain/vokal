# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from jwt_geo.database import Column, Model, SurrogatePK, db, reference_col, relationship
from jwt_geo.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    locations = db.relationship('Location', backref='user', lazy='dynamic')

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


class Location(SurrogatePK, Model):
    """A location searched by a user"""

    __tablename__ = 'user_locations'
    name = Column(db.String(256), nullable=True)
    street = Column(db.String(64), nullable=True)
    state = Column(db.String(64), nullable=True)
    country = Column(db.String(64), nullable=True)
    pin = Column(db.String(64), nullable=True)
    latlng = Column(db.String(64), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    user_id = Column(db.Integer, db.ForeignKey('users.id'))