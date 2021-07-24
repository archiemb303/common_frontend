""" module for common postlogin authentications"""
from functools import wraps
from rest_framework.views import APIView, Response

from common.website_management.api.get_website_availability.views_get_website_availability import website_control
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate


def common_pre_login_authentications(func):
    """Closure Function to run all common pre-login authentication functions."""

    @wraps(func)
    @website_control
    @api_authenticate
    def common_pre_login_authentications_json(self, request):
        """Function to run all pre login authentication decorators"""
        try:
            print("came here again")
            return func(self, request)
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure',
                                    f"Exception encountered while doing common pre login authentications: {ex}", None]))
            return Response(output_json)
    return common_pre_login_authentications_json

