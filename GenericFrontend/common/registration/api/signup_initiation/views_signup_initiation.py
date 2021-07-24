"""Module to initiate signup through email."""
import logging
import re
from rest_framework.views import APIView, Response
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from common.utilities.lib import serializer_save
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.registration.serializers import EmailVerificationSerializer, UuidSerializer
from common.registration.specificlib.utils import get_activation_status_message
from common.registration.specificlib.views_lib import CheckEmailForRegistration
from common.emailengine.specificlib.views_lib import UserRegistrationEmailVerification as emailviews
from common.emailengine.specificlib.views_lib import UserRegistrationEmailVerificationViaInvite as emailviews2
from common.emailengine.specificlib.views_lib import UserRegistrationEmailVerificationViaInvitePartner as emailviews3
from common.utilities.lib import sql_exec
from .validations_signupinitiate import validation_signupinitiate

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class SignUpInitiationAPI(APIView):
    """This covers the API for sending email to new as well as existing user for registration."""
    @api_authenticate
    @validation_signupinitiate
    def post(self, request):
        """Post Function to authenticate and send email to new as well as existing user for registration ."""
        input_json, output_json, vendor_id, payload = request.data['APIParams'], {}, \
                                                      request.data['APIDetails']['token_vendor_id'], {'Payload': None}
        input_json['vendor_id'] = vendor_id
        input_json['activation_key'] = get_random_string(length=32)
        input_json['activation_status'] = 1
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        # Check for email id presence in EmailVerification table.
        existing_user_check_var = CheckEmailForRegistration.check_email_for_registration_function(
            input_json['email_id'])
        if existing_user_check_var['Status'] == "Failure":
            # Add input parameters from new user request to dictionary for adding record in EmailVerification table .
            new_user = self.add_new_user(input_json)
            match = re.findall(r"'Status': 'Failure'", str(new_user))
            if match:
                output_json['Payload'] = new_user
                return Response(new_user)
            # Send email verification mail to new user for registration.
            invite_output = self.get_invite_via_email(input_json, new_user)
            match = re.findall(r"'Status': 'Failure'", str(invite_output))
            if match:
                output_json['Payload'] = invite_output
                return Response(invite_output)
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Success', 'Thank you for '
                                                                                            'registering! Please check'
                                                                                            ' your inbox  and verify'
                                                                                            ' your email address',
                                                                                 payload['Payload']]))
            return Response(output_json)
        try:
            if str(existing_user_check_var['email_presence']) == str("True"):
                if existing_user_check_var['activation_status'] == 1:
                    # Update activation key and activation status in EmailVerification table for existing
                    # email id presence in email verification table .
                    activation_key_var = self.set_activation_key(input_json)
                    match = re.findall(r"'Status': 'Failure'", str(activation_key_var))
                    if match:
                        output_json['Payload'] = activation_key_var
                        return Response(output_json)
                    # Send email verification mail to user for registration.
                    check_reg_email = self.check_registration_email(input_json, existing_user_check_var)
                    match = re.findall(r"'Status': 'Failure'", str(check_reg_email))
                    if match:
                        output_json['Payload'] = check_reg_email
                        return Response(output_json)
                activation_status_val = existing_user_check_var['activation_status']
                # Fetch activation status along with message for unregistered user.
                activation_status_output = get_activation_status_message(activation_status_val)
                match = re.findall(r"'Status': 'Failure'", str(activation_status_output))
                if match:
                    output_json['Payload'] = activation_status_output
                    return Response(output_json)
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Success',
                                                                                     'Thank you for registering! Please'
                                                                                     ' check your inbox and '
                                                                                     'verify your email address',
                                                                                     activation_status_output]))
                return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                              ['Success', f"We are facing errors with your email_id.Seems like your "
                                                          f"email id is missing. during the Registration Process. "
                                                          f"Please try again. Exception encountered. {ex}",
                                               payload['Payload']]))
            logger.error('Something went wrong!')
            return Response(output_json)

    def add_new_user(self, request):
        """Function  to add new user for registration"""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            reg_input = dict(zip(
                ['first_name', 'last_name', 'email_id', 'activation_key', 'activation_status', 'source_uuid', 'source',
                 'vendor_id'], [input_json['first_name'], input_json['last_name'], input_json['email_id'],
                                input_json['activation_key'], input_json['activation_status'],
                                input_json['source_uuid'], input_json['source_id'], input_json['vendor_id']]))
            reg_input['added_by'] = str(reg_input['email_id'])
            reg_input['last_modified_by'] = str(reg_input['email_id'])
            return reg_input
        except Exception as ex:
            output_json['Status'] = 'Failure'
            output_json[
                'Message'] = f"Error occured during Registration process.Please try again after a moment." \
                             f"Encountered Exception: {ex}."
            output_json = payload['Payload']
            return output_json

    def check_registration_email(self, request, existing_user_check_var):
        """Check for registration email for existing user."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            check_verification_mail = emailviews.user_registration_email_verification(existing_user_check_var,
                                                                                      firstName=input_json['first_name'],
                                                                                      lastName=input_json['last_name'],
                                                                                      email_id=input_json['email_id'],
                                                                                      activation_key=input_json[
                                                                                          'activation_key'])
            return check_verification_mail
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Exception encountered "
                                                                      f"while sending email: {ex}",
                                                                      payload['Payload']]))
            return output_json

    def set_activation_key(self, request):
        """Function  to set activation key for existing user."""
        input_json, output_json = request, {}
        try:
            activation_key_var = dict(zip(['activation_key', 'activation_status'],
                                          [input_json['activation_key'], 1]))
            sql = sql_exec("update_row", [input_json['email_id'], activation_key_var['activation_key'],
                                          activation_key_var['activation_status']])[0]
            logger.info(f"update emailverification table: {sql}")
            return activation_key_var
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"Activation key could not be updated: {ex}"
            return output_json

    def insert_uuid(self, reg_input):
        """Function  to insert a record into uuid table."""
        output_json, payload = {}, {'Payload': None}
        try:
            uuid_var = dict(zip(['source_uuid', 'source', 'added_by', 'last_modified_by'],
                                [reg_input['source_uuid'], reg_input['source'],
                                 reg_input['added_by'], reg_input['last_modified_by']]))
            serialized_uuid = serializer_save(UuidSerializer, uuid_var)
            return serialized_uuid.data
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message'], ['Failure',
                                                           f"Error occured during inserting  uuid into uuid table."
                                                           f"Encountered Exception: {ex}.", payload['Payload']]))
            return output_json

    def get_invite_via_email(self, request, reg_input):
        """Function  to receive invitation via mail from web app or from existing user."""
        input_json, output_json = request, {}
        try:
            uuid_var = dict(zip(['source_uuid', 'source', 'added_by', 'last_modified_by', 'vendor_id'],
                                [reg_input['source_uuid'], reg_input['source'],
                                 reg_input['added_by'], reg_input['last_modified_by'], reg_input['vendor_id']]))
            serialized_uuid = serializer_save(UuidSerializer, uuid_var)
            reg_input['uuid'] = serialized_uuid.data['uuid_id']
            serializer_var = serializer_save(EmailVerificationSerializer, reg_input)
            invite_flag, firstName, lastName, email_id, activation_key, requester_fname, requester_lname = \
                input_json['invite_flag'], input_json['first_name'], input_json['last_name'], \
                input_json['email_id'], input_json['activation_key'], input_json['requester_fname'], input_json[
                    'requester_lname']
            invite_list = [firstName, lastName, email_id, activation_key,
                           requester_fname, requester_lname, invite_flag]
            if invite_flag == 0:
                emailviews.user_registration_email_verification(serializer_var.data, firstName=invite_list[0],
                                                                lastName=invite_list[1], email_id=invite_list[2],
                                                                activation_key=invite_list[3])
            elif invite_flag == 1:
                emailviews2.user_registration_email_verification_via_invite(
                    serializer_var.data, firstName=invite_list[0], lastName=invite_list[1], email_id=invite_list[2],
                    activation_key=invite_list[3], requester_fname=invite_list[4], requester_lname=invite_list[5],
                    invite_flag=invite_list[6])
            elif invite_flag == 2:
                emailviews3.user_registration_email_verification_via_invite_partner(
                    serializer_var.data, firstName=invite_list[0], lastName=invite_list[1],
                    email_id=invite_list[2], activation_key=invite_list[3],
                    requester_fname=invite_list[4], requester_lname=invite_list[5],
                    invite_flag=invite_list[6])
            else:
                output_json = dict(zip(['Status', 'Message'], ["Failure",
                                                               "Something went wrong while receiving invitation."]))
            output_json['Status'] = 'Success'
            output_json['Message'] = "Thank you for registering! Please check your inbox and verify your email address"
            return output_json
        except Exception as ex:
            output_json['Status'] = 'Failure'
            output_json['Message'] = f"Exception encountered while sending invitation and " \
                                     f"Error occured during Insertion of User's data into Database." \
                                     f"Please try again, sorry for the inconvenience: {ex}"
            return output_json


def trigger_error():
    """Function  to test for logging."""
    try:
        division_by_zero = 1 / 0
        return division_by_zero
    except Exception as ex:
        logger.error(f"exception encountered: {ex}", exc_info=1)
    return HttpResponse("function executed")
