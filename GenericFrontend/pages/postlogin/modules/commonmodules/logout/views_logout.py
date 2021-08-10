"""Module to verify API for login of verified user with session details."""
import logging
import re
import requests
from rest_framework.views import APIView, Response
from django.shortcuts import render, get_object_or_404, redirect
from genericfrontend.settings import *

from utilities.apicallers.apicallers import makebackendapicall_json
# from .validations_preloginhome import validation_login

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class PostLoginLogoutAPI(APIView):
    """This covers the API for login of verified user with session details."""
    def get(self, request):
        try:
            # Handling case when user is not logged in but has directly hit the particular url
            if 'login_flag' not in request.session or request.session['login_flag'] != 1:
                request.session['redirection_url'] = "user/logout/"
                return redirect('/prelogin/')

            output_json = dict(
                zip(["Status", "Message", "active_item", "Payload"],
                    ["Success", "logout page loaded successfully", "user/logout", None]))
            return render(request, 'logout_confirm.html', output_json)
        except Exception as ex:
            output_json = dict(
                zip(["Status", "Message", "active_item", "Payload"],
                    ["Success", f"Exception encountered: {ex}", "user/profile", None]))
            return render(request, 'user-profile.html', output_json)

