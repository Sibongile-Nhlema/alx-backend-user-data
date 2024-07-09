#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if 'AUTH_TYPE' in os.environ:
    auth_type = os.environ['AUTH_TYPE']
    if auth_type == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()


# Define before_request handler
@app.before_request
def before_request_handler():
    if auth is None:
        return

    # Paths that do not require any authentication
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/', '/api/v1/forbidden/']

    # Check if request path is excluded
    if request.path in excluded_paths:
        return

    # Check if authentication is required
    if auth.require_auth(request.path, excluded_paths):

        auth_header = auth.authorization_header(request)
        if auth_header is None:
            abort(401)

        current_user = auth.current_user(request)
        if current_user is None:
            abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


# Task 1 - Error handler: Unauthorized
@app.errorhandler(401)
def not_found(error: Exception) -> tuple:
    """ Not Authorised request
    """
    return jsonify({"error": "Unauthorized"}), 401


# Task 2 - Error handler: Forbidden
@app.errorhandler(403)
def forbidden(error: Exception) -> tuple:
    """ Forbidden request for the 403 status code
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
