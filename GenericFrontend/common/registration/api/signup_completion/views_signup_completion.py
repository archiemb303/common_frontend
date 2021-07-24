"""Module to complete the registration process and creation of profile id  for verified user."""
import logging
import re
from django.utils.crypto import get_random_string
from rest_framework.views import APIView, Response
from common.utilities.lib import sql_exec, sql_fetch_cursor
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.registration.specificlib.views_lib import CheckEmailForRegistration, CompleteUserRegistration
from common.location.specificlib.views_lib import ValidateCity
from common.registration.models import EmailVerification
from .validations_signupcomplete import validation_signupcomplete

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class SignUpCompletionAPI(APIView):
    """This covers the API for completion of registration process and creation of profile id  for verified user."""
    @api_authenticate
    @validation_signupcomplete
    def post(self, request):
        """Post Function to complete the registration process and create  profile id  for verified user."""
        input_json, output_json, payload = request.data['APIParams'], {}, {'Payload': None}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        try:
            # Validate the city code input by user.
            city_status = self.check_city_code(input_json)
            match = re.findall(r"'Status': 'Failure'", str(city_status))
            if match:
                output_json['Payload'] = city_status
                return Response(output_json)
            # Check for email id presence in EmailVerification table.
            existing_user_check_var = CheckEmailForRegistration.check_email_for_registration_function(
                input_json['email_id'])
            match = re.findall(r"'Status': 'Failure'", str(existing_user_check_var))
            if match:
                output_json['Payload'] = existing_user_check_var
                return Response(output_json)
            # Fetch activation key from email_id for user registration.
            activation_key = self.fetch_activation_key(input_json)
            match = re.findall(r"'Status': 'Failure'", str(activation_key))
            if match:
                output_json['Payload'] = activation_key
                return Response(output_json)
            if input_json['activation_key'] == activation_key:
                # Update activation key  and activation status for unverified user.
                updated_activation_key = self.update_activation_key(input_json)
                match = re.findall(r"'Status': 'Failure'", str(updated_activation_key))
                if match:
                    output_json['Payload'] = updated_activation_key
                    return Response(output_json)
                # Fetch profile details for a given email id input by user.
                fetch_profilefromemail = self.fetch_profilefromemail(input_json)
                match = re.findall(r"'Status': 'Failure'", str(fetch_profilefromemail))
                if match:
                    input_json['id_user_cred_id'] = existing_user_check_var['email_id']
                    input_json['id_source'] = "genericfrontend"  # code change required
                    # Perform complete registration process for a given email id input by user.
                    signup_completion = CompleteUserRegistration.complete_user_registration_function(input_json)
                    match = re.findall(r"'Status': 'Failure'", str(signup_completion))
                    if match:
                        output_json['Payload'] = signup_completion
                        return Response(output_json)
                    sql = sql_fetch_cursor("fetch_profile_emailverification", 'profile_ref',
                                           ['profile_ref', input_json['email_id']])[0]
                    output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ["Success", "Congratulations,"
                                                                                                    " you are"
                                                                                                    "registered "
                                                                                                    "successfully "
                                                                                                    "with genericfrontend", sql]))
                    return Response(output_json)
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Profile-id with this "
                                                                                                "email-id already "
                                                                                                "exists in database",
                                                                                     payload['Payload']]))
                return Response(output_json)
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "invalid activation key",
                                                                                 payload['Payload']]))
            return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Error encountered in "
                                                                                            f"registration completion"
                                                                                            f" initiation: {ex}",
                                                                                 payload['Payload']]))
            return Response(output_json)

    def check_city_code(self, request):
        """Function to validate the city code input by user."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            city_code_validity_var = ValidateCity.validate_city_function(self, input_json['city_id'])
            return city_code_validity_var
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Issues happened while fetching city_code. "
                                                                      f"Encountered Exception"
                                                                      f": {ex}", payload['Payload']]))
            return output_json

    def check_existing_user(self, existing_user_check_var):
        """Function to check whether user is existing or new."""
        output_json, payload = {}, {'Payload': None}
        try:
            if existing_user_check_var["Status"] == "Failure":
                output_json = existing_user_check_var
                return output_json
            return
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Issues happened while checking whether user"
                                                                      f" already exists. Encountered Exception"
                                                                      f": {ex}", payload['Payload']]))
            return output_json

    def fetch_activation_key(self, request):
        """Function to fetch activation key from email_id"""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            sql = sql_exec("fetch_row", [input_json['email_id']])[0]
            return sql['activation_key']
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Issues happened while fetching activation_key."
                                                                      f" Encountered Exception"
                                                                      f": {ex}", payload['Payload']]))
        return output_json

    def fetch_profilefromemail(self, request):
        """Function to fetch profile_id from email_id"""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            sql = sql_fetch_cursor("fetch_profile_emailverification", 'profile_ref',
                                   ['profile_ref', input_json['email_id']])[0]
            return sql
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Issues happened while fetching profile_id."
                                                                      f" Encountered Exception"
                                                                      f": {ex}", payload['Payload']]))
            return output_json

    def update_activation_key(self, request):
        """Function te update activation key for unverified user."""
        input_json, output_json, activation_key_var, payload = request, {}, {}, {'Payload': None}
        try:
            sql = sql_exec("fetch_row", [input_json['email_id']])[0]
            activation_key_var['activation_key'] = get_random_string(length=32)
            activation_key_var['activation_status'] = 1
            activation_key_var['uuid'] = sql['uuid_id']
            EmailVerification.objects.filter(pk=sql['emailverification_id']).update(activation_key=activation_key_var['activation_key'],
                                                                                    activation_status_id=1, uuid_id=activation_key_var['uuid'])

            qs = EmailVerification.objects.filter(pk=sql['emailverification_id']).all()
            return qs.values()[0]
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"Activation key could not be updated: {ex}"
            output_json['Payload'] = payload['Payload']
            return output_json
