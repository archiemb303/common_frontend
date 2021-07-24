"""Module to initiate the signup through email id for unverified user."""
import random
import logging
import re
import uuid
from collections import defaultdict
from rest_framework.views import APIView, Response
from django.utils.crypto import get_random_string
from common.commondecorators.preloginauthentications import common_pre_login_authentications
from common.registration.serializers import UuidToProfileIdMapSerializer, EmailVerificationOtpSerializer
from common.utilities.lib import serializer_save, sql_exec, sql_fetch_cursor
from common.registration.serializers import UuidSerializer, UserProfileSerializer, AddBioSerializer
from common.emailengine.specificlib.views_lib import UserRegistrationEmailOtpVerification as emailviews
from common.registration.models import EmailVerificationOtp
from common.registration.specificlib.userprofile_lib import fetch_profile_from_emailotp, \
    fetch_profile_emailorphone_sql, fetch_emailverificationotp_sql
from .validations_signup_emailotp_initiate import validations_signupemailotpinitiate
# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class SignUpInitiationEmailOtpAPI(APIView):
    """This covers the API for sending otp to new as well as existing user for registration."""
    @common_pre_login_authentications
    @validations_signupemailotpinitiate
    def post(self, request):
        """Post Function to authenticate and send email to new as well as existing user for registration ."""
        input_json, output_json, vendor_id, payload = request.data['APIParams'], {}, \
                                             request.data['APIDetails']['token_vendor_id'], {'Payload': None}
        input_json['vendor_id'] = vendor_id
        input_json['email_id'] = input_json['email_id'].lower()
        input_json['namestring'] = input_json['email_id']
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'Payload'],
                               [request.data['AvailabilityDetails'], request.data['AuthenticationDetails'], None]))
        try:
            fetch_profilefromemail = fetch_profile_emailorphone_sql(input_json)
            match = re.findall(r"'Status': 'Failure'", str(fetch_profilefromemail))
            if match:
                # Fetch profile row from mobile verification table for input email id.
                fetch_profilefromemailotp = fetch_profile_from_emailotp(input_json)
                match = re.findall(r"'Status': 'Failure'", str(fetch_profilefromemailotp))
                if match:
                    # check whether mobile verification table is having a record for input email id.
                    existing_user_check_var = self.check_existing_user(input_json)
                    match = re.findall(r"'Status': 'Failure'", str(existing_user_check_var))
                    if match:
                        output_json['Payload'] = existing_user_check_var
                        return Response(output_json)
                    if existing_user_check_var['Payload'] == 0:
                        # Insert record into uuid table for input email id.
                        uuid_var = self.insert_uuid(input_json)
                        match = re.findall(r"'Status': 'Failure'", str(uuid_var))
                        if match:
                            output_json['Payload'] = uuid_var
                            return Response(output_json)
                        input_json.update(uuid_var)
                        # Insert record into MobileVerification table for input email id.
                        emailverificationotp_params = self.insert_emailverificationotp(input_json)
                        match = re.findall(r"'Status': 'Failure'", str(emailverificationotp_params))
                        if match:
                            output_json['Payload'] = emailverificationotp_params
                            return Response(output_json)
                        input_json.update(emailverificationotp_params)
                        # Verify profile details for a given email id.
                        verified_profile = self.verify_profile(input_json)
                        match = re.findall(r"'Status': 'Failure'", str(verified_profile))
                        if match:
                            output_json['Payload'] = verified_profile
                            return Response(output_json)
                        output_json['Payload'] = verified_profile
                        return Response(output_json)
                    # Update records in MobileVerification table for input email id.
                    updated_emailverificationotp_data = self.update_emailverificationotp(input_json)
                    match = re.findall(r"'Status': 'Failure'", str(updated_emailverificationotp_data))
                    if match:
                        output_json['Payload'] = updated_emailverificationotp_data
                        return Response(output_json)
                    input_json.update(updated_emailverificationotp_data)
                    # Verify profile details for a given email id.
                    verify_existinguserprofile = self.verify_profile(input_json)
                    match = re.findall(r"'Status': 'Failure'", str(verify_existinguserprofile))
                    if match:
                        output_json['Payload'] = verify_existinguserprofile
                        return Response(output_json)
                    output_json['Payload'] = verify_existinguserprofile
                    return Response(output_json)
                input_json.update(fetch_profilefromemailotp)
                profile_id, payload['Payload'] = fetch_profilefromemailotp['profile_id'], fetch_profilefromemailotp
                # Fetch uuid from UserProfiles table  for a profile_id.
                uuid_details = self.fetch_uuidfromprofileid(input_json)
                match = re.findall(r"'Status': 'Failure'", str(uuid_details))
                if match:
                    output_json['Payload'] = uuid_details
                    return Response(uuid_details)
                input_json.update(uuid_details)
                # Update record in MobileVerification table for a given email id.
                emailverificationotp_params = self.update_emailverificationotp(input_json)
                match = re.findall(r"'Status': 'Failure'", str(emailverificationotp_params))
                if match:
                    output_json['Payload'] = emailverificationotp_params
                    return Response(output_json)

                # Send otp through sms for a given email id
                otp_email = self.send_otp_email(input_json)
                match = re.findall(r"'Status': 'Failure'", str(otp_email))
                if match:
                    output_json['Payload'] = otp_email
                    return Response(output_json)
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Success', 'Otp sent successfully',
                                                                                     None]))
                return Response(output_json)
            input_json.update(fetch_profilefromemail)
            profile_id, payload['Payload'] = fetch_profilefromemail['profile_id'], fetch_profilefromemail
            # Fetch uuid from UserProfiles table  for a profile_id.
            uuid_details = self.fetch_uuidfromprofileid(input_json)
            match = re.findall(r"'Status': 'Failure'", str(uuid_details))
            if match:
                output_json['Payload'] = uuid_details
                return Response(uuid_details)
            input_json.update(uuid_details)
            emailverificationotp_records = fetch_emailverificationotp_sql(input_json)
            match = re.findall(r"'Status': 'Failure'", str(emailverificationotp_records))
            if match:
                emailverificationotp_params = self.insert_emailverificationotp(input_json)
                match = re.findall(r"'Status': 'Failure'", str(emailverificationotp_params))
                if match:
                    output_json['Payload'] = emailverificationotp_params
                    return Response(output_json)
                    # Update record in MobileVerification table for a given email id.
                # emailverificationotp_params = self.update_emailverificationotp(input_json)
                # match = re.findall(r"'Status': 'Failure'", str(emailverificationotp_params))
                # if match:
                #     output_json['Payload'] = emailverificationotp_params
                #     return Response(output_json)

                input_json.update(emailverificationotp_params)
                # Send otp through sms for a given email id
                otp_email = self.send_otp_email(input_json)
                match = re.findall(r"'Status': 'Failure'", str(otp_email))
                if match:
                    output_json['Payload'] = otp_email
                    return Response(output_json)
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Success', 'Otp sent successfully',
                                                                                     None]))
                return Response(output_json)
            # input_json.update(emailverificationotp_records)
            emailverificationotp_params = self.update_emailverificationotp(input_json)
            match = re.findall(r"'Status': 'Failure'", str(emailverificationotp_params))
            if match:
                output_json['Payload'] = emailverificationotp_params
                return Response(output_json)
            input_json.update(emailverificationotp_params)
            # Send otp through sms for a given email id
            otp_email = self.send_otp_email(input_json)
            match = re.findall(r"'Status': 'Failure'", str(otp_email))
            if match:
                output_json['Payload'] = otp_email
                return Response(output_json)
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Success', 'Otp sent successfully',
                                                                                 None]))
            return Response(output_json)


        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Success',
                                                                                 f"We are facing errors with your email"
                                                                                 f" id.Seems like your email id"
                                                                                 f" is missing during the registration"
                                                                                 f" Process. Please try again."
                                                                                 f" Exception encountered.: {ex}",
                                                                                 payload['Payload']]))
            # logger.error('Something went wrong!')
            return Response(output_json)

    def check_existing_user(self, request):
        """Function for checking whether user is existing or new for the provided email id."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            credential_id_var = EmailVerificationOtp.objects.filter(email_id=input_json['email_id']). \
                values('emailverificationotp_id')
            numberofentries = credential_id_var.count()
            payload['Payload'] = numberofentries
            options = defaultdict(lambda: dict(zip(['Status', 'Message', 'Payload'],
                                                   ["Failure", "DB has more than one entry for the same email id",
                                                    payload['Payload']])),
                                  {1: dict(zip(['Status', 'Message', 'Payload'],
                                               ["Success", "DB has exactly one entry for the same email id",
                                                payload['Payload']])), 0: dict(zip(['Status', 'Message', 'Payload'],
                                                                                   ["Success",
                                                                                    "Start email registration process"
                                                                                    " for the given email id",
                                                                                    payload['Payload']]))})
            existing_user_status = options[numberofentries]
            return existing_user_status
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f"Exception encountered while checking for exisitng user email"
                                               f" id during Registration process :{ex}", payload['Payload']]))
            return output_json

    def insert_uuid(self, request):
        """Function for inserting uuid for a given email id."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            source_uuid, source_id, vendor = str(uuid.uuid4()), 1, input_json['vendor_id']
            added_by = last_modified_by = str(input_json['email_id'])
            uuid_var = dict(zip(['source_uuid', 'source', 'added_by', 'last_modified_by', 'vendor'],
                                [source_uuid, source_id, added_by, last_modified_by, vendor]))
            serialized_uuid = serializer_save(UuidSerializer, uuid_var)
            return serialized_uuid.data
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Error encountered during Registration process."
                                                                      f"Encountered Exception: {ex}.",
                                                                      payload['Payload']]))
            return output_json

    def fetch_mapuuidtoprofile(self, request):
        """Function for fetching row from mapuuidtoprofielid table."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            sql = sql_exec("fetch_mapuuidtoprofileid", [input_json['uuid_id_id']])[0]
            return sql
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f"Error while fetching details from mapuuidtoprofielid table : {ex}",
                                    payload['Payload']]))
            return output_json

    def fetch_profiledetails(self, request):
        """Function for fetching row from profile table."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            sql = sql_exec("fetch_profile", [input_json['profile_id_id']])[0]
            return sql
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f"Error while fetching details from profile table : {ex}", payload['Payload']]))
            return output_json

    def create_userprofile(self, request):
        """Function for creating user profile for a given email id."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            profile_params = self.get_profile_params(input_json)
            match = re.findall(r"'Status': 'Failure'", str(profile_params))
            if match:
                return profile_params
            profile_details = self.create_profile(profile_params)
            match = re.findall(r"'Status': 'Failure'", str(profile_details))
            if match:
                return profile_details
            input_json.update(profile_details)
            bio_params = self.get_bio_params(input_json)
            match = re.findall(r"'Status': 'Failure'", str(bio_params))
            if match:
                return bio_params
            bio_details = self.add_bio(bio_params)
            match = re.findall(r"'Status': 'Failure'", str(bio_details))
            if match:
                return bio_details
            mapuuidtoprofileid_params = self.get_mapuuidtoprofileid_params(input_json)
            match = re.findall(r"'Status': 'Failure'", str(mapuuidtoprofileid_params))
            if match:
                return mapuuidtoprofileid_params
            input_json.update(mapuuidtoprofileid_params)
            mapuuidtoprofileid_details = self.create_mapuuidtoprofileid(input_json)
            match = re.findall(r"'Status': 'Failure'", str(mapuuidtoprofileid_details))
            if match:
                return mapuuidtoprofileid_details
            return profile_details
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Error occured during Registration process."
                                                                      f"Encountered Exception: {ex}.", payload['Payload']]))
            return output_json

    def insert_emailverificationotp(self, request):
        """Function for inserting a row in mobileverification table."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        if 'uuid_id_id' in input_json and 'uuid_id' not in input_json:
            input_json['uuid_id'] = input_json['uuid_id_id']
        if 'uuid_id' in input_json and 'uuid_id_id' not in input_json:
            input_json['uuid_id'] = input_json['uuid_id']
        try:
            params = dict(zip(['email_id', 'otp', 'uuid', 'emailverificationotp_status',
                               'added_by', 'last_modified_by'],
                              [input_json['email_id'], random.randint(100000, 999999),
                               input_json['uuid_id'], 1, input_json['added_by'], input_json['last_modified_by']]))

            serialized = serializer_save(EmailVerificationOtpSerializer, params)
            return serialized.data
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message'], ['Failure',
                                                           f"Error occured during insertion in emailverificationotp"
                                                           f"table. Encountered Exception: {ex}.", payload['Payload']]))
            return output_json

    def update_emailverificationotp(self, request):
        """Function for updating fields in mobileverification table."""
        input_json, output_json, update_params, payload = request, {}, {}, {'Payload': None}
        try:
            sql = sql_fetch_cursor("fetch_emailverificationotp", 'email_ref', ['email_ref', input_json['email_id']])[0]
            update_params = dict(zip(['otp', 'uuid_id', 'emailverificationotp_status'],
                                     [random.randint(100000, 999999), sql['uuid_id'],
                                      sql['emailverificationotp_status_id']]))
            # update_query(EmailVerificationOtp, sql['emailverificationotp_id'], otp=update_params['otp'],
            #              emailverificationotp_status=update_params['emailverificationotp_status'],
            #              uuid_id=update_params['uuid_id'])
            EmailVerificationOtp.objects.filter(pk=sql['emailverificationotp_id']).\
                update(otp=update_params['otp'],
                       emailverificationotp_status=update_params['emailverificationotp_status'],
                       uuid_id=update_params['uuid_id'])
            qs = EmailVerificationOtp.objects.filter(pk=sql['emailverificationotp_id']).all()
            return qs.values()[0]
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message'], ['Failure',
                                                           f"Error occured during updation in mobile verification"
                                                           f"table. Encountered Exception: {ex}.", payload['Payload']]))
            return output_json

    def send_otp_email(self, request):
        """Function for sending otp through sms."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            check_verification_mail = emailviews.user_registration_email_otp_verification(input_json,
                                                                                          email_id=input_json['email_id'],
                                                                                          otp=input_json[
                                                                                              'otp'])
            return check_verification_mail
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Exception encountered "
                                                                      f"while sending email: {ex}",
                                                                      payload['Payload']]))
            return output_json

    def get_profile_params(self, request):
        """Function for setting parameters for creating user profile for a given email id."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            profilelist = ['default', 'default', 'default', None, 'default', None, 1, 1, 2]
            profile_params = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth', 'orientation', 'city_id',
                                       'profile_status', 'dp_flag', 'profile_completion_status'],
                                      [i for i in profilelist]))
            profile_params.update(dict.fromkeys(['web_profile_key', 'android_app_profile_key',
                                                 'ios_app_profile_key', 'global_profile_key'],
                                                get_random_string(length=32)))
            profile_params.update(dict.fromkeys(['added_by', 'last_modified_by'], "EV__" + str(input_json["email_id"])))

            return profile_params
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"Exception Encountered while getting profile parameters: {ex}"
            output_json['Payload'] = payload['Payload']
            return output_json

    def create_profile(self, request):
        """Function for inserting a row with generated profile id in profile table for given email id."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            serializer_var = serializer_save(UserProfileSerializer, input_json)
            return serializer_var.data
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"Exception Encountered while creating profile id: {ex}"
            output_json['Payload'] = payload['Payload']
            return output_json

    def get_bio_params(self, request):
        """Function for setting bio parameters in order to create bio for a given profile."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            add_bio_var = dict(zip(['short_description', 'added_by', 'last_modified_by', 'profile_id'],
                                   [" ", input_json['added_by'], input_json['last_modified_by'],
                                    input_json['profile_id']]))
            return add_bio_var
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"Unable to add default bio: {ex}"
            output_json['Payload'] = payload['Payload']
            return output_json

    def add_bio(self, request):
        """Function for inserting a row in bio table for a given profile."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            serialized = serializer_save(AddBioSerializer, input_json)
            return serialized.data
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"Unable to add default bio: {ex}"
            output_json['Payload'] = payload['Payload']
            return output_json

    def get_mapuuidtoprofileid_params(self, request):
        """Function for setting uuidtoprofileidmap parameters for inserting row in uuidtoprofileidmap table."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        if 'uuid_id_id' in input_json and 'uuid_id' not in input_json:
            input_json['uuid_id_id'] = input_json['uuid_id_id']
        if 'uuid_id' in input_json and 'uuid_id_id' not in input_json:
            input_json['uuid_id_id'] = input_json['uuid_id']
        try:
            map_list = [input_json['uuid_id_id'], input_json['profile_id'], 1, input_json['added_by'],
                        input_json['last_modified_by']]
            map_uuidtoprofileid_var = dict(zip(['uuid_id_id', 'profile_id', 'status', 'added_by', 'last_modified_by',
                                                'profile_id'], [i for i in map_list]))
            return map_uuidtoprofileid_var
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Error while fetching mapuuidtoprofileid "
                                                                      f"parameters.Encountered Exception:"
                                                                      f" {ex}", payload['Payload']]))
            return output_json

    def create_mapuuidtoprofileid(self, request):
        """Function for inserting a row in uuidtoprofileidmap table."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        if 'uuid_id_id' in input_json and 'uuid_id' not in input_json:
            input_json['uuid_id_id'] = input_json['uuid_id_id']
        if 'uuid_id' in input_json and 'uuid_id_id' not in input_json:
            input_json['uuid_id_id'] = input_json['uuid_id']
        try:
            params = dict(zip(['uuid_id', 'profile_id', 'status', 'added_by', 'last_modified_by'],
                              [input_json['uuid_id_id'], input_json['profile_id'], input_json['profile_status'],
                               input_json['added_by'], input_json['last_modified_by']]))
            serializer_var = serializer_save(UuidToProfileIdMapSerializer, params)
            return serializer_var.data
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"Some exception in mapping uuid to profile .Encounter Exception + {ex}"
            output_json['Payload'] = payload['Payload']
            return output_json

    def verify_profile(self, request):
        """Function for verifying profile details for a given email id."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            otp_email = self.send_otp_email(input_json)
            match = re.findall(r"'Status': 'Failure'", str(otp_email))
            if match:
                return otp_email
            mapuuidtoprofiledetails = self.fetch_mapuuidtoprofile(input_json)
            match = re.findall(r"'Status': 'Failure'", str(mapuuidtoprofiledetails))
            if match:
                user_profile = self.create_userprofile(input_json)
                match = re.findall(r"'Status': 'Failure'", str(user_profile))
                if match:
                    return user_profile
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ['Success', 'Otp sent successfully', None]))
                return output_json
            profile_data = self.fetch_profiledetails(mapuuidtoprofiledetails)
            match = re.findall(r"'Status': 'Failure'", str(profile_data))
            if match:
                return profile_data
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Success', 'Otp sent successfully', None]))
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Error"
                                                                                 f" while verifying profile details for"
                                                                                 f" user.Encountered Exception:"
                                                                                 f" {ex}", payload['Payload']]))
            return output_json

    def fetch_uuidfromprofileid(self, request):
        """Function for fetching uuid from profile_id."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            sql = sql_fetch_cursor("fetch_uuidfromprofile", 'uuid_ref',
                                   ['uuid_ref', input_json['profile_id']])[0]
            return sql
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Encountered exception while fetching uuid"
                                                                      f" from profileid.: {ex}", payload['Payload']]))
            return output_json
