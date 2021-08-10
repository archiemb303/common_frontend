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


class PreLoginHomeAPI(APIView):
    """This covers the API for login of verified user with session details."""
    def get(self, request):
        output_json = dict(zip(['login_flag', "Payload"], [2, None]))
        if 'login_flag' in request.session and request.session['login_flag'] == 1:
            output_json['login_flag'] = 1
        if 'redirection_url' in request.session:
            output_json['redirection_url'] = request.session['redirection_url']

        backend_call_params = dict(zip(['api_type', 'api_name', 'request_type', 'api_params'],
                                       ['prelogin', 'get_website_availability', 'post', dict()]))
        backend_call_output = makebackendapicall_json(request, backend_call_params)

        if backend_call_output['Payload']['AvailabilityDetails']['Payload']['live_flag'] == 1 and \
                backend_call_output['Payload']['AvailabilityDetails']['Payload']['state_flag'] == 1:
            output_json['Payload'] = backend_call_output
            return render(request, 'prelogin-home.html', output_json)
        return render(request, 'page-404.html', output_json)

    def post(self, request):

        """Function to perform login of verified user with session details."""
        input_json, output_json, vendor_id, payload, session_dict = request.data["APIParams"], {}, \
                                                      request.data['APIDetails']['token_vendor_id'], \
                                                                    {'Payload': None}, {}
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'Payload'],
                               [request.data['AvailabilityDetails'], request.data['AuthenticationDetails'], None]))
        input_json['vendor_id'] = vendor_id
        try:
            # Fetch user credential details from UserCredentials table for a given email id.
            user = self.fetch_user(input_json)
            match = re.findall(r"'Status': 'Failure'", str(user))
            if match:
                output_json['Payload'] = user
                return Response(output_json)
            # Check for password match between password present in UserCredentials table with password input by user.
            user_cred_check = self.check_user_cred(user)
            match = re.findall(r"'Status': 'Failure'", str(user_cred_check))
            if match:
                output_json['Payload'] = user_cred_check
                return Response(output_json)
            # Fetch records from Sources table for a given source id.
            sources = self.fetch_sources(input_json)
            match = re.findall(r"'Status': 'Failure'", str(sources))
            if match:
                output_json['Payload'] = sources
                return Response(output_json)
            if sources['source_id'] != 1:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', 'Not a Verified Source', payload['Payload']]))
                return Response(output_json)
            # check for  user profile presence for a given email id input by user.
            user_profile = self.check_user_profile(input_json)
            match = re.findall(r"'Status': 'Failure'", str(user_profile))
            if match:
                output_json['Payload'] = user_profile
                return Response(output_json)
            session_dict['device'] = input_json['device']
            session_dict['profile_id'] = user_profile['User_Details']['profile_id']
            session_dict['login_type'] = input_json['login_type']
            session_dict['vendor_id'] = input_json['vendor_id']
            # Create new session for registered user.
            new_session = self.create_session(session_dict)
            match = re.findall(r"'Status': 'Failure'", str(new_session))
            if match:
                output_json['SessionDetails'] = new_session
                return Response(output_json)
            session_obj = new_session['SessionDetails']
            new_user_session = dict(zip(['profile_id', 'session_id', 'session_key', 'Status', 'Message'],
                                        [session_obj['profile_id'], session_obj['session_id'],
                                         session_obj['session_key'], new_session['Status'], new_session['Message']]))
            # insert the number of login attempts of user into db
            login_count_save = self.insert_login_count(input_json)
            match = re.findall(r"'Status': 'Failure'", str(login_count_save))
            if match:
                output_json['Payload'] = login_count_save
                return Response(output_json)
            # Insert number of login attempts by user to UserCredentials Table.
            login_count = self.get_login_count(input_json)
            if match:
                output_json['Payload'] = login_count
                return Response(output_json)
            # Fetch record from EmailVerification Table for a given email id.
            email_verification_record = CheckEmailForRegistration.\
                check_email_for_registration_function(input_json['email_id'])

            match = re.findall(r"'Status': 'Failure'", str(email_verification_record))
            if match:
                output_json['Payload'] = email_verification_record
                return Response(output_json)
            payload_details = {'email_id': input_json['email_id'], 'login_count': login_count['login_count'],
                               'activation_status': email_verification_record['activation_status']}
            output_json['SessionDetails'] = new_user_session
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Success', "User successfully logged"
                                                                                            " in, Profile Details "
                                                                                            "Updated Successfully.",
                                                                                 payload_details]))
            return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ["Failure",
                                                                                 f"Session not created due to failure"
                                                                                 f" at fetching payload: {ex}.",
                                                                                 payload['payload']]))
            return Response(output_json)

    def fetch_user(self, request):
        """Function to fetch user credential."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            user_cred = CheckUserCredentials.check_user_credentials_function(input_json)
            user_cred['Payload'] = None
            return user_cred
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered while"
                                                                                 f" fetching user credentials: {ex}",
                                                                      payload['Payload']]))
            return output_json

    def check_user_cred(self, user):
        """Function to check for username and password."""
        output_json, payload = {}, {'Payload': None}
        try:
            if user['user_credential_output']['password_match'] is False:
                output_json['Status'] = "Failure"
                output_json['Message'] = "Username and Password don't match"
                return output_json
            return
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered while"
                                                                                 f" checking for username and password:"
                                                                                 f" {ex}", payload['Payload']]))
            return output_json

    def fetch_sources(self, request):
        """Function to fetch records from Sources table for a given source id"""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            sql = sql_fetch_cursor("fetch_source", 'source_ref',
                                   ['source_ref', input_json['source_id']])[0]
            return sql
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Issues happened while fetching source_id."
                                                                      f" Encountered Exception"
                                                                      f": {ex}", payload['Payload']]))
            return output_json

    def check_user_profile(self, request):
        """Function to check for user profile presence."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            user_profile = GetEmailCredNProfileIdsFromEmailId.get_email_cred_n_profile_ids_from_email_id_function(
                self, input_json)
            return user_profile
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered while"
                                                                                 f" checking for user profile"
                                                                                 f" {ex}", payload['Payload']]))
            return output_json

    def create_session(self, session):
        """Function to create session for registered user."""
        output_json, payload = {}, {'Payload': None}
        try:
            new_user_session = CreateNewSession.create_new_session_function(session)
            return new_user_session
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered while"
                                                                                 f"creating new session for user"
                                                                                 f" {ex}", payload['Payload']]))
            return output_json

    def insert_login_count(self, request):
        """Function to insert number of login attempts by user to UserCredentials Table."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            login_count_object_var = UserCredentials.objects.get(email_id__exact=input_json['email_id'])
            login_count_object_var.login_count = (login_count_object_var.login_count + 1)
            login_count_object_var.save()
            return
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"Exception encountered while inserting login counts for user: {ex}"
            output_json['Payload'] = payload['Payload']
            return Response(output_json)

    def get_login_count(self, request):
        """Function to count the number of login attempts by user."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            login_count = self.get_login_info(input_json)
            return login_count
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered while"
                                                                                 f" fetching login counts"
                                                                                 f" {ex}", payload['Payload']]))
            return output_json

    def get_login_info(self, request):
        """Function to check the user credentials in UserCredentials table."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            usercredentials_model_var = UserCredentials.objects.get(email_id__exact=input_json['email_id'])
            serialized_usercredentials_model_var = UserCredentialsSerializer(usercredentials_model_var)
            return serialized_usercredentials_model_var.data
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"Exception encountered while fetching login info for user: {ex}"
            output_json['Payload'] = payload['Payload']
            return output_json
