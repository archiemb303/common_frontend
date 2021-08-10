import logging
import re
import requests
from rest_framework.views import APIView, Response
from django.shortcuts import render, get_object_or_404, redirect
from genericfrontend.settings import *

from utilities.apicallers.apicallers import makebackendapicall_json


class VerifyEmailLoginOTPAPI(APIView):
    def get(self,request):
        return render(request, 'verify_otp.html')

    def post(self, request):
        try:
            input_json = request.data
            backend_call_params = dict(zip(['api_type', 'api_name', 'request_type', 'api_params'],
                                           ['prelogin', 'signup_emailotp_verify', 'post', dict()]))
            backend_call_params['api_params']['email_id'] = request.session['email_id']
            backend_call_params['api_params']['otp'] = int(input_json)
            backend_call_output = makebackendapicall_json(request, backend_call_params)
            if backend_call_output['Payload']['Payload']['Status'] == "Success" and \
                     backend_call_output['Payload']['Payload']['Message'] in \
                    ["OTP verified successfully", "User logged in, Profile Details Updated Successfully"]:
                request.session['login_flag'] = 1
                if backend_call_output['Payload']['Payload']['Message'] == "OTP verified successfully":
                    request.session['redirection_url'] = "user/profile/"
                else:
                    if 'redirection_url' not in request.session or request.session['redirection_url'] is None:
                        request.session['redirection_url'] = "user/home/"

            output_json = dict(
                zip(["Status", "Message", "Payload"], ["Success", "Backend API called successfully", backend_call_output]))
            return Response(output_json)

        except Exception as ex:
            output_json = dict(zip(["Status", "Message", "Payload"],
                                   ["Failure", f"Exception encountered while making Backed API call: {ex}"]))
        return Response(output_json)
