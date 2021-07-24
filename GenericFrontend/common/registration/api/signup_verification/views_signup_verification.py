"""Module to validate the API for verification of link sent on user's email for unverified user."""
import re
import logging
from rest_framework.views import APIView, Response
from common.registration.specificlib.utils import get_activation_status_message
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.registration.specificlib.views_lib import CheckEmailForRegistration
from .validations_signupverify import validation_signupverify

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class SignUpVerificationAPI(APIView):
    """This covers the API for verification of link sent on user's email for unverified user."""
    @api_authenticate
    @validation_signupverify
    def post(self, request):
        """Post Function to verify the link sent on user's email for unverified user."""
        input_json, output_json, payload = request.data['APIParams'], {}, {'Payload': None}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        # Check for email id presence in EmailVerification table.
        existing_user_check_var = CheckEmailForRegistration.check_email_for_registration_function(
            input_json['email_id'])
        match = re.findall(r"'Status': 'Failure'", str(existing_user_check_var))
        if match:
            existing_user_check_var.update(payload)
            output_json['Payload'] = existing_user_check_var
            return Response(existing_user_check_var)
        try:
            if existing_user_check_var['activation_status'] == 1:
                # Check for validation of activation key from EmailVerification table.
                activation_key_check = self.check_for_activation_key(input_json, existing_user_check_var)
                match = re.findall(r"'Status': 'Failure'", str(activation_key_check))
                if match:
                    activation_key_check.update(payload)
                    output_json['Payload'] = activation_key_check
                    return Response(output_json)
                output_json['Payload'] = activation_key_check
                return Response(output_json)
            activation_status_val = existing_user_check_var['activation_status']
            # Fetch activation status along with message for unregistered user.
            activation_status_output = get_activation_status_message(activation_status_val)
            match = re.findall(r"'Status': 'Failure'", str(activation_status_output))
            if match:
                activation_status_output.update(payload)
                output_json['Payload'] = activation_status_output
                return Response(output_json)
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Success', "Welcome back! Please "
                                                                                            "check your inbox and "
                                                                                            "verify your email address",
                                                                                 activation_status_output]))
            return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"User has not completed "
                                                                                            f"Registration Phase-1."
                                                                                            f"Please complete your "
                                                                                            f"registration phase 1 "
                                                                                            f"first. Exception "
                                                                                            f"encountered: {ex}",
                                                                                 payload['Payload']]))
            return Response(output_json)

    def check_for_activation_key(self, request, existing_user_check_var):
        """Function to check for activation key status."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            if existing_user_check_var['activation_key'] == input_json['activation_key']:
                output_json['Status'] = "Success"
                output_json['Message'] = "Allow registration step 2"
                output_json['Payload'] = payload['Payload']
                return output_json
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Activation key is not valid",
                                                                      payload['Payload']]))
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f"Exception encountered while checking for activation key: {ex}",
                                    payload['Payload']]))
            return output_json
