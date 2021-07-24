"""Module to complete the signup through phone number for verified user."""
import logging
import re
from rest_framework.views import APIView, Response
from django.utils.crypto import get_random_string
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.registration.models import UserProfile
from common.sessionmanagement.serializers import UserSessionsSerializer
from common.registration.api.signup_emailotp_completion.validations_signup_emailotp_completion import \
    validation_signupemailotpcomplete
from common.registration.specificlib.userprofile_lib import fetch_profile_records
from common.utilities.lib import serializer_save, sql_fetch_cursor
from common.registration.specificlib.userprofile_lib import get_app_profiledetails

# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class SignUpCompletionEmailOtpAPI(APIView):
    """This covers the API for sending email to new as well as existing user for registration."""
    @common_post_login_authentications
    @validation_signupemailotpcomplete
    def post(self, request):
        """Post Function to authenticate and send email to new as well as existing user for registration ."""
        input_json, output_json, vendor_id, payload = request.data['APIParams'], {}, \
                                             request.data['APIDetails']['token_vendor_id'], {'Payload': None}
        input_json['vendor_id'] = vendor_id
        output_json['AvailabilityDetails'] = request.data['AvailabilityDetails']
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        output_json['AvailabilityDetails'] = request.data['AvailabilityDetails']
        try:
            input_json['profile_id'] = request.data['SessionDetails']['Payload']['profile_id']
            # Fetch a record from user profile table.
            profile_data = fetch_profile_records(input_json)
            match = re.findall(r"'Status': 'Failure'", str(profile_data))
            if match:
                output_json['Payload'] = profile_data
                return Response(output_json)
            profile_completion = profile_data['profile_completion_status_id']
            # check if profile_completion=2, stating incomplete profile.
            if profile_completion == 2:
                # Update record in user profile table for input phone number.
                user_profile = self.update_userprofile(input_json, profile_data)
                match = re.findall(r"'Status': 'Failure'", str(user_profile))
                if match:
                    output_json['Payload'] = user_profile
                    return Response(output_json)
                input_json.update(user_profile)
                # Check whether any field in profile table table is default or none, if yes update profile.
                profiledetails = self.check_profile_fields(input_json)
                match = re.findall(r"'Status': 'Failure'", str(profiledetails))
                if match:
                    input_json['profile_completion_status'] = 1
                    update_profile_completion = self.update_userprofile(input_json, profiledetails)
                    match1 = re.findall(r"'Status': 'Failure'", str(update_profile_completion))
                    if match1:
                        # output_json['Payload'] = update_profile_completion
                        output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                          ["Failure", "Issues in updating profile completion status",
                                                           update_profile_completion]))
                    output_json['Payload'] = profiledetails
                    return Response(output_json)
                # Create session for updated user profile.
                session = self.insert_usersessions(input_json)
                match = re.findall(r"'Status': 'Failure'", str(session))
                if match:
                    session.update(payload)
                    output_json['Payload'] = session
                    return Response(output_json)
                input_json.update(session)
                new_session = dict(zip(["profile_id", "session_id", "session_key"],
                                       [session["profile_id"], session["session_id"], session["session_key"]]))
                session_details = dict(zip(['Status', 'Message', 'Payload'],
                                           ['Success', 'Session created successfully', new_session]))
                output_json['SessionDetails'] = session_details
                profiledisplay = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth', 'city_id',
                                           'dp_flag', 'profile_completion_status'], [profiledetails['first_name'],
                                                                                     profiledetails['last_name'],
                                                                                     profiledetails['sex'],
                                                                                     profiledetails['date_of_birth'],
                                                                                     profiledetails['city_id_id'],
                                                                                     profiledetails['dp_flag_id'],
                                                                                     profiledetails['profile_completion'
                                                                                                    '_status_id']]))
                payload_app = get_app_profiledetails(input_json)
                app_payload = {'payload_app': payload_app}
                profiledisplay.update(app_payload['payload_app'])
                output_json['SessionDetails'] = session_details
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ["Success", "User logged in, "
                                                                                                "Profile Details "
                                                                                                "Updated Successfully",
                                                                                     profiledisplay]))
                return Response(output_json)
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', 
                                                                                            ' profile completion status is already complete. Hence function did not  excute',
                                                                                            
                                                                                 payload['Payload']]))
            return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Otp doesn't match or "
                                                                                            f"emailid doesn't exist. "
                                                                                            f"Encountered Exception: "
                                                                                            f"{ex}",
                                                                                 payload['Payload']]))
            return Response(output_json)

    def insert_usersessions(self, request):
        """Function for inserting a row in session management table ."""
        input_json, output_json = request, {}
        try:
            session_var = dict(zip(['profile_id', 'session_key', 'login_source', 'login_type', 'added_by',
                                    'added_date', 'last_modified_date', 'last_modified_by', 'status_id', 'vendor_id'],
                                   [input_json['profile_id'], get_random_string(length=32), 'email', 'native',
                                    input_json['added_by'], input_json['added_date'], input_json['last_modified_date'],
                                    input_json['last_modified_by'], 1, input_json['vendor_id']]))
            serialized = serializer_save(UserSessionsSerializer, session_var)
            return serialized.data
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message'], ['Failure',
                                                           f"Error occured during insertion in session"
                                                           f"table. Encountered Exception: {ex}."]))
            return output_json

    def check_profile_fields(self, request):
        """Function for fetching/setting input parameters for user profile."""
        input_json, output_json, update_profile_params = request, {}, []
        try:
            sql = sql_fetch_cursor("fetch_profile", 'profile_ref',
                                   ['profile_ref', input_json['profile_id']])[0]
            profile_params = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth', 'orientation', 'city_id',
                                       'dp_flag'], [sql['first_name'], sql['last_name'],
                                                    sql['sex'], sql['date_of_birth'],
                                                    sql['orientation'],
                                                    sql['city_id_id'], sql['dp_flag_id']]))
            for key, value in profile_params.items():
                if value is None or value == 'default':
                    update_profile_params.append(key)
            if len(update_profile_params) == 0:
                return sql
            updated_profile_params = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth', 'orientation',
                                               'city_id', 'dp_flag'], [input_json['first_name'],
                                                                       input_json['last_name'], input_json['sex'],
                                                                       input_json['date_of_birth'],
                                                                       input_json['orientation'],
                                                                       input_json['city_id_id'],
                                                                       input_json['dp_flag_id']]))
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Please update your {update_profile_params}",
                                                                      updated_profile_params]))
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message'], ['Failure',
                                                           f"Error occured during checking for profile fields"
                                                           f"table. Encountered Exception: {ex}."]))
            return output_json

    def update_userprofile(self, request, profile):
        """Function for updating record in user profile table."""
        input_json, output_json, update_params, payload = request, {}, {}, {'Payload': None}
        if 'profile_completion_status' in profile and 'profile_completion_status_id' not in profile:
            profile['profile_completion_status'] = profile['profile_completion_status']
        if 'profile_completion_status_id' in profile and 'profile_completion_status' not in profile:
            profile['profile_completion_status'] = profile['profile_completion_status_id']
        try:
            update_params = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth', 'orientation', 'city_id',
                                      'dp_flag_id', 'profile_completion_status'], [input_json['first_name'],
                                                                                   input_json['last_name'],
                                                                                   input_json['sex'],
                                                                                   input_json['date_of_birth'],
                                                                                   input_json['orientation'],
                                                                                   input_json['city_id'],
                                                                                   input_json['dp_id'], 1]))
            UserProfile.objects.filter(pk=profile['profile_id']).update(first_name=update_params['first_name'],
                                                                        last_name=update_params['last_name'],
                                                                        sex=update_params['sex'],
                                                                        date_of_birth=update_params['date_of_birth'],
                                                                        orientation=update_params['orientation'],
                                                                        city_id=update_params['city_id'],
                                                                        dp_flag_id=update_params['dp_flag_id'],
                                                                        profile_completion_status=update_params
                                                                        ['profile_completion_status'])
            qs = UserProfile.objects.filter(pk=profile['profile_id']).all()
            return qs.values()[0]
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message'], ['Failure',
                                                           f"Error encountered during updation in user profile "
                                                           f"table. Encountered Exception: {ex}.", payload['Payload']]))
            return output_json
