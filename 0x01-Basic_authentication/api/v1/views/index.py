#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


# Task 1 - Error handler: Unauthorized
@app_views.route('/unauthorized/', methods=['GET'], strict_slashes=False)
def unauthorized() -> tuple:
    """ GET /api/v1/unathorised
    Return:
      - the number of each objects
    """
    abort(401)


# Task 2 - Error handler: Forbidden
@app_views.route('/forbidden/', methods=['GET'], strict_slashes=False)
def forbidden() -> tuple:
    """ GET /api/v1/forbidden
    Return:
      - the number of each objects
    """
    abort(403)
