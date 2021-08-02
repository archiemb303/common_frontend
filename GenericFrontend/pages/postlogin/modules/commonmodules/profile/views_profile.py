"""Module to verify API for login of verified user with session details."""
import logging
import re
from rest_framework.views import APIView, Response
from django.shortcuts import render, get_object_or_404, redirect

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class PostLoginProfileAPI(APIView):
    """This covers the API for login of verified user with session details."""
    def get(self, request):
        # import pdb;pdb.set_trace()
        payload = {"key1": "one", "key2": "two"}
        return render(request, 'user-profile.html', payload)

