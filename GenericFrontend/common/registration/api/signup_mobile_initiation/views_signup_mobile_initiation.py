"""Module to initiate the signup through phone number for unverified user."""
import random
import logging
import re
import uuid
from collections import defaultdict
from rest_framework.views import APIView, Response
from django.utils.crypto import get_random_string
from common.commondecorators.preloginauthentications import common_pre_login_authentications
from common.registration.models import MobileVerification
from common.registration.serializers import UuidToProfileIdMapSerializer
from common.smsengine.specificlib.sendsms import send_sms
from common.utilities.lib import serializer_save, sql_exec, sql_fetch_cursor
from common.registration.serializers import UuidSerializer, UserProfileSerializer, \
    AddBioSerializer, MobileVerificationSerializer
from common.registration.specificlib.userprofile_lib import fetch_profilefromphonenumber
from .validations_signup_mobile_initiate import validations_signupmobileinitiate

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class SignUpInitiationMobileAPI(APIView):
    """This covers the API for sending otp to new as well as existing user for registration."""
    @common_pre_login_authentications
    @validations_signupmobileinitiate
    def post(self, request):
        """Post Function to authenticate and send email to new as well as existing user for registration ."""
        input_json, output_json, vendor_id, payload = request.data['APIParams'], {}, \
            request.data['APIDetails']['token_vendor_id'], {'Payload': None}
        input_json['vendor_id'] = vendor_id
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'Payload'],
                               [request.data['AvailabilityDetails'], request.data['AuthenticationDetails'], None]))
        try:
            # Fetch profile row from mobile verification table for input phone number.
            fetch_profilefromphone = fetch_profilefromphonenumber(input_json)
            match = re.findall(r"'Status': 'Failure'",
                               str(fetch_profilefromphone))
            if match:
                # check whether mobile verification table is having a record for input phone number.
                existing_user_check_var = self.check_existing_user(input_json)
                match = re.findall(r"'Status': 'Failure'",
                                   str(existing_user_check_var))
                if match:
                    output_json['Payload'] = existing_user_check_var
                    return Response(output_json)
                if existing_user_check_var['Payload'] == 0:
                    # Insert record into uuid table for input phone number.
                    uuid_var = self.insert_uuid(input_json)
                    match = re.findall(r"'Status': 'Failure'", str(uuid_var))
                    if match:
                        output_json['Payload'] = uuid_var
                        return Response(output_json)
                    input_json.update(uuid_var)
                    # Insert record into MobileVerification table for input phone number.
                    mobileverificationparams = self.insert_mobileverification(
                        input_json)
                    match = re.findall(r"'Status': 'Failure'",
                                       str(mobileverificationparams))
                    if match:
                        output_json['Payload'] = mobileverificationparams
                        return Response(output_json)
                    input_json.update(mobileverificationparams)
                    # Verify profile details for a given phone number.
                    verified_profile = self.verify_profile(input_json)
                    match = re.findall(r"'Status': 'Failure'",
                                       str(verified_profile))
                    if match:
                        output_json['Payload'] = verified_profile
                        return Response(output_json)
                    output_json['Payload'] = verified_profile
                    return Response(output_json)
                # Update records in MobileVerification table for input phone number.
                updated_mobileverification_data = self.update_mobileverification(
                    input_json)
                match = re.findall(r"'Status': 'Failure'", str(
                    updated_mobileverification_data))
                if match:
                    output_json['Payload'] = updated_mobileverification_data
                    return Response(output_json)
                input_json.update(updated_mobileverification_data)
                # Verify profile details for a given phone number.
                verify_existinguserprofile = self.verify_profile(input_json)
                match = re.findall(r"'Status': 'Failure'",
                                   str(verify_existinguserprofile))
                if match:
                    output_json['Payload'] = verify_existinguserprofile
                    return Response(output_json)
                output_json['Payload'] = verify_existinguserprofile
                return Response(output_json)
            input_json.update(fetch_profilefromphone)
            profile_id, payload['Payload'] = fetch_profilefromphone['profile_id'], fetch_profilefromphone
            # Fetch uuid from UserProfiles table  for a profile_id.
            uuid_details = self.fetch_uuidfromprofileid(input_json)
            match = re.findall(r"'Status': 'Failure'", str(uuid_details))
            if match:
                output_json['Payload'] = uuid_details
                return Response(uuid_details)
            input_json.update(uuid_details)
            # Update record in MobileVerification table for a given phone number.
            mobileverificationparams = self.update_mobileverification(
                input_json)
            match = re.findall(r"'Status': 'Failure'",
                               str(mobileverificationparams))
            if match:
                output_json['Payload'] = mobileverificationparams
                return Response(output_json)
            input_json.update(mobileverificationparams)
            # Send otp through sms for a given phone number
            sms = self.send_sms(input_json)
            match = re.findall(r"'Status': 'Failure'", str(sms))
            if match:
                output_json['Payload'] = sms
                return Response(output_json)
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Success',
                                                                                 'Otp sent successfully', None]))
            return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Success',
                                                                                 f"We are facing errors with your phone"
                                                                                 f" number.Seems like your phone number"
                                                                                 f" is missing during the registration"
                                                                                 f" Process. Please try again."
                                                                                 f" Exception encountered.: {ex}",
                                                                                 payload['Payload']]))
            # logger.error('Something went wrong!')
            return Response(output_json)

    def check_existing_user(self, request):
        """Function for checking whether user is existing or new for the provided phone number."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            credential_id_var = MobileVerification.objects.filter(phone_number=input_json['phone_number']). \
                values('mobileverification_id')
            numberofentries = credential_id_var.count()
            payload['Payload'] = numberofentries
            options = defaultdict(lambda: dict(zip(['Status', 'Message', 'Payload'],
                                                   ["Failure", "DB has more than one entry for the same phone number",
                                                    payload['Payload']])),
                                  {1: dict(zip(['Status', 'Message', 'Payload'],
                                               ["Success", "DB has exactly one entry for the same phone number",
                                                payload['Payload']])), 0: dict(zip(['Status', 'Message', 'Payload'],
                                                                                   ["Success",
                                                                                    "Start mobile registration process"
                                                                                    " for the given phone number",
                                                                                    payload['Payload']]))})
            existing_user_status = options[numberofentries]
            return existing_user_status
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f"Exception encountered while checking for exisitng user mobile"
                                               f" number during Registration process :{ex}", payload['Payload']]))
            return output_json

    def insert_uuid(self, request):
        """Function for inserting uuid for a given phone number."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            source_uuid, source_id, vendor = str(
                uuid.uuid4()), 2, input_json['vendor_id']
            added_by = last_modified_by = str(input_json['phone_number'])
            uuid_var = dict(zip(['source_uuid', 'source', 'added_by', 'last_modified_by', 'vendor'],
                                [source_uuid, source_id, added_by, last_modified_by, vendor]))
            serialized_uuid = serializer_save(UuidSerializer, uuid_var)
            return serialized_uuid.data
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Error occured during Registration process."
                                                                      f"Encountered Exception: {ex}.",
                                                                      payload['Payload']]))
            return output_json

    def fetch_mapuuidtoprofile(self, request):
        """Function for fetching row from mapuuidtoprofielid table."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            sql = sql_exec("fetch_mapuuidtoprofileid", [
                           input_json['uuid_id_id']])[0]
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
        """Function for creating user profile for a given phone number."""
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
            mapuuidtoprofileid_params = self.get_mapuuidtoprofileid_params(
                input_json)
            match = re.findall(r"'Status': 'Failure'",
                               str(mapuuidtoprofileid_params))
            if match:
                return mapuuidtoprofileid_params
            input_json.update(mapuuidtoprofileid_params)
            mapuuidtoprofileid_details = self.create_mapuuidtoprofileid(
                input_json)
            match = re.findall(r"'Status': 'Failure'",
                               str(mapuuidtoprofileid_details))
            if match:
                return mapuuidtoprofileid_details
            return profile_details
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Error occured during Registration process."
                                                                      f"Encountered Exception: {ex}.", payload['Payload']]))
            return output_json

    def insert_mobileverification(self, request):
        """Function for inserting a row in mobileverification table."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        if 'uuid_id_id' in input_json and 'uuid_id' not in input_json:
            input_json['uuid_id'] = input_json['uuid_id_id']
        if 'uuid_id' in input_json and 'uuid_id_id' not in input_json:
            input_json['uuid_id'] = input_json['uuid_id']
        try:
            params = dict(zip(['phone_number', 'country_code', 'otp', 'uuid_id', 'mobileverification_status',
                               'added_by', 'last_modified_by'], [input_json['phone_number'], input_json['country_code'],
                                                                 random.randint(
                                                                     100000, 999999), input_json['uuid_id'],
                                                                 1, input_json['added_by'],
                                                                 input_json['last_modified_by']]))
            serialized = serializer_save(MobileVerificationSerializer, params)
            return serialized.data
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message'], ['Failure',
                                                           f"Error occured during insertion in mobile verification"
                                                           f"table. Encountered Exception: {ex}.", payload['Payload']]))
            return output_json

    def update_mobileverification(self, request):
        """Function for updating fields in mobileverification table."""
        input_json, output_json, update_params, payload = request, {}, {}, {'Payload': None}
        try:
            sql = sql_exec("fetch_mobileverification_row",
                           [input_json['phone_number']])[0]
            update_params = dict(zip(['otp', 'uuid_id', 'mobileverification_status_id'], [random.randint(100000, 999999),
                                                                                       sql['uuid_id'],
                                                                                       sql['mobilverification_status_id']]))
            MobileVerification.objects.filter(pk=sql['mobileverification_id']).update(otp=update_params['otp'],
                                                                                      mobileverification_status_id=
                                                                                      update_params
                                                                                      ['mobileverification_status_id'],
                                                                                      uuid_id=update_params['uuid_id'])
            qs = MobileVerification.objects.filter(
                pk=sql['mobileverification_id']).all()
            return qs.values()[0]
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message'], ['Failure',
                                                           f"Error occured during updation in mobile verification"
                                                           f"table. Encountered Exception: {ex}.", payload['Payload']]))
            return output_json

    def send_sms(self, request):
        """Function for sending otp through sms."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            output_json['frm'] = 34567
            output_json['phone_number'] = str(input_json["phone_number"])
            output_json['country_code'] = str(input_json["country_code"])
            output_json['text'] = f"Welcome to genericfrontend. Please use {input_json['otp']} as your OTP to login"
            output_json['sms_type'] = "transactional"
            sms = send_sms(output_json)
            return sms
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message'], ['Failure', f"Error while sending otp though sms."
                                                                      f"Encountered Exception: {ex}",
                                                           payload['Payload']]))
            return output_json

    def get_profile_params(self, request):
        """Function for setting parameters for creating user profile for a given phone number."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            profilelist = ['default', 'default',
                           'default', None, 'default', '', 1, 1, 2]
            profile_params = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth', 'orientation', 'city_id',
                                       'profile_status', 'dp_flag', 'profile_completion_status'],
                                      [i for i in profilelist]))
            profile_params.update(dict.fromkeys(['web_profile_key', 'android_app_profile_key',
                                                 'ios_app_profile_key', 'global_profile_key'],
                                                get_random_string(length=32)))
            profile_params.update(dict.fromkeys(['added_by', 'last_modified_by'], str(input_json["phone_number"])))
            return profile_params
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json[
                'Message'] = f"Exception Encountered while getting profile parameters: {ex}"
            output_json['Payload'] = payload['Payload']
            return output_json

    def create_profile(self, request):
        """Function for inserting a row with generated profile id in profile table for given phone number."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            serializer_var = serializer_save(UserProfileSerializer, input_json)
            return serializer_var.data
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json[
                'Message'] = f"Exception Encountered while creating profile id: {ex}"
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
            serializer_var = serializer_save(
                UuidToProfileIdMapSerializer, params)
            return serializer_var.data
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json[
                'Message'] = f"Some exception in mapping uuid to profile .Encounter Exception + {ex}"
            output_json['Payload'] = payload['Payload']
            return output_json

    def verify_profile(self, request):
        """Function for verifying profile details for a given phone number."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            sms = self.send_sms(input_json)
            match = re.findall(r"'Status': 'Failure'", str(sms))
            if match:
                return sms
            mapuuidtoprofiledetails = self.fetch_mapuuidtoprofile(input_json)
            match = re.findall(r"'Status': 'Failure'",
                               str(mapuuidtoprofiledetails))
            if match:
                user_profile = self.create_userprofile(input_json)
                match1 = re.findall(r"'Status': 'Failure'", str(user_profile))
                if match1:
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
