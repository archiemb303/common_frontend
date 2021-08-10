import logging
import re
import requests
from rest_framework.views import APIView, Response
from django.shortcuts import render, get_object_or_404, redirect
from genericfrontend.settings import *

from utilities.apicallers.apicallers import makebackendapicall_json


class GenerateEmailLoginOTPAPI(APIView):
    def post(self, request):
        try:
            input_json = request.data
            request.session['email_id'] = input_json
            backend_call_params = dict(zip(['api_type', 'api_name', 'request_type', 'api_params'],
                                           ['prelogin', 'signup_email_otp_initiate', 'post', dict()]))
            backend_call_params['api_params']['email_id'] = input_json
            backend_call_output = makebackendapicall_json(request, backend_call_params)
            output_json = dict(zip(["Status", "Message", "Payload"], ["Success", "Backend API called successfully", backend_call_output]))
            return Response(output_json)
        except Exception as ex:
            output_json = dict(zip(["Status", "Message", "Payload"],
                                   ["Failure", f"Exception encountered while making Backed API call: {ex}"]))
            return Response(output_json)
