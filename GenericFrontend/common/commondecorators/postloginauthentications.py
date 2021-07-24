""" module for common postlogin authentications"""
from functools import wraps
from rest_framework.views import APIView, Response

from common.website_management.api.get_website_availability.views_get_website_availability import website_control
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate, api_formdata_authenticate
from common.sessionmanagement.api.sessioncontrol.views_sessioncontrol import session_control, session_form_control, \
    session_control_search


def common_post_login_authentications(func):
    """Closure Function to run all common post-login authentication functions."""

    @wraps(func)
    @website_control
    @api_authenticate
    @session_control
    def common_post_login_authentications_json(self, request):
        """Function to run all post login authentication decorators"""
        try:
            return func(self, request)
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure',
                                    f"Exception encountered while doing common post login authentications: {ex}", None]))
            return Response(output_json)
    return common_post_login_authentications_json


def common_formdata_post_login_authentications(func):
    """Closure Function to run all common post-login authentication functions."""

    @wraps(func)
    @website_control
    @api_formdata_authenticate
    @session_form_control
    def common_formdata_post_login_authentications_json(self, request):
        """Function to run all post login authentication decorators"""
        try:
            return func(self, request)
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure',
                                    f"Exception encountered while doing common post login authentications: {ex}", None]))
            return Response(output_json)
    return common_formdata_post_login_authentications_json


def common_user_search_post_login_authentications(func):
    """Closure Function to run all common post-login authentication functions."""

    @wraps(func)
    @website_control
    @api_authenticate
    @session_control_search
    def common_user_search_post_login_authentications_json(self, request):
        """Function to run all post login authentication decorators"""
        try:
            return func(self, request)
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure',
                                    f"Exception encountered while doing common post login authentications: {ex}", None]))
            return Response(output_json)
    return common_user_search_post_login_authentications_json

