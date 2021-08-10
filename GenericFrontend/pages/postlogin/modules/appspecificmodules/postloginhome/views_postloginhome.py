"""Module to verify API for login of verified user with session details."""
import logging
import re
from rest_framework.views import APIView, Response
from django.shortcuts import render, get_object_or_404, redirect

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class PostLoginHomeAPI(APIView):
    """This covers the API for login of verified user with session details."""
    def get(self, request):
        # Handling case when user is not logged in but has directly hit the particular url
        if 'login_flag' not in request.session or request.session['login_flag'] != 1:
            request.session['redirection_url'] = "user/home/"
            return redirect('/prelogin/')

        output_json = dict(
            zip(["Status", "Message", "active_item", "Payload"],
                ["Success", "Backend API called successfully", "user/home", None]))
        return render(request, 'index.html', output_json)

