#!/usr/bin/env python3

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

import pytest
from app import app
from models import db

@pytest.fixture(scope='function', autouse=True)
def app_context():
    """Create a new database table for each test."""
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

