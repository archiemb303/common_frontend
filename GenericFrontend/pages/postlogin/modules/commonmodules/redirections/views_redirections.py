import logging
import re
import requests
from rest_framework.views import APIView, Response
from django.shortcuts import render, get_object_or_404, redirect
from genericfrontend.settings import *


class RedirectionsAPI(APIView):
    def get(self,request):
        redirection_url = request.session['redirection_url']
        return redirect(f"/{redirection_url}")

