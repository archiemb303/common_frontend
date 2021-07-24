"""Module to verify API for login of verified user with session details."""
import logging
import re
import random
import uuid
from django.utils.crypto import get_random_string
from common.registration.serializers import UserProfileSerializer, UuidToProfileIdMapSerializer, \
    AddBioSerializer, UuidSerializer, EmailVerificationOtpSerializer
from common.sessionmanagement.serializers import UserSessionsSerializer
from common.utilities.lib import sql_fetch_cursor, \
    serializer_save, sql_exec
from common.registration.models import UserProfile

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def fetch_profile_from_emailotp(request):
    """Function for fetching profile_id for a given email id."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    try:
        sql = sql_fetch_cursor("fetch_profile_emailverificationotp", 'profile_ref',
                               ['profile_ref', input_json['email_id']])[0]
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Issues happened while fetching profile_id."
                                                                  f" Encountered Exception"
                                                                  f": {ex}", payload['Payload']]))
        return output_json


def fetch_profilefromphonenumber(request):
    """Function for fetching profile_id for a given phone number."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    try:
        sql = sql_fetch_cursor("fetch_profile_mobileverification", 'profile_ref',
                               ['profile_ref', input_json['phone_number']])[0]
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Issues happened while fetching profile_id."
                                                                  f" Encountered Exception"
                                                                  f": {ex}", payload['Payload']]))
        return output_json


def fetch_profile_uuid(request):
    """Fetch profile details from userprofile table for existing uuid.."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    try:
        sql = sql_fetch_cursor("fetch_profilefromuuid", 'profile_ref',
                               ['profile_ref', input_json['uuid_id']])[0]
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Issues happened while fetching profile from uuid."
                                                                  f" Encountered Exception"
                                                                  f": {ex}", payload['Payload']]))
        return output_json


def fetch_profile(request):
    """Fetch profile details from userprofile table for existing uuid."""
    input_json = request
    try:
        keyparam = [key for key in input_json.keys() if key in ('email_id', 'uuid_id', 'phone_number')][0]
        if keyparam == 'email_id':
            return fetch_profile_from_emailotp(input_json)
        elif keyparam == 'uuid_id':
            return fetch_profile_uuid(input_json)
        elif keyparam == 'phone_number':
            return fetch_profilefromphonenumber(input_json)
        output_json = dict(zip(['Status', 'Message', 'Payload'], ["Failure", "Invalid Parameter Passed", None]))
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure', f"Exception encountered while checking for existing user mobile"
                                           f" number during Registration process :{ex}", None]))
        return output_json


def fetch_sources(request):
    """Function to fetch records from Sources table for a given source id"""
    input_json, output_json, payload = request, {}, {'Payload': None}
    try:
        sql = sql_fetch_cursor("fetch_source", 'source_ref',
                               ['source_ref', input_json['source']])[0]
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Issues happened while fetching source_id."
                                                                  f" Encountered Exception"
                                                                  f": {ex}", payload['Payload']]))
        return output_json


def fetch_uuid_guid(request):
    """Function to fetch uuid from registration_uuid table for input source_uuid."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    try:
        sql = sql_fetch_cursor("fetch_uuidforguid", 'uuid_ref',
                               ['uuid_ref', input_json['source_uuid']])[0]
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Issues happened while fetching uuid "
                                                                             f"from guid. Encountered Exception: {ex}",
                                                                  payload['Payload']]))
        return output_json


def fetch_uuid_email(request):
    """Function for setting uuidtoprofileidmap parameters for inserting row in uuidtoprofileidmap table."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    if 'uuid_id_id' in input_json and 'uuid_id' not in input_json:
        input_json['uuid_id_id'] = input_json['uuid_id_id']
    if 'uuid_id' in input_json and 'uuid_id_id' not in input_json:
        input_json['uuid_id_id'] = input_json['uuid_id']
    try:
        sql = sql_fetch_cursor("sp_fetch_uuid_from_email", 'uuid_ref',
                               ['uuid_ref', input_json['email_id']])[0]
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Issues happened while fetching uuid "
                                                                             f"from guid. Encountered Exception: {ex}",
                                                                  payload['Payload']]))
        return output_json


def get_profile_params(request):
    """Function for setting parameters for creating user profile for a given input."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    try:
        profilelist = [input_json['first_name'], input_json['last_name'], input_json['sex'],
                       input_json['date_of_birth'], input_json['orientation'], input_json['city_id'],
                       1, 1, input_json['profile_completion_status']]
        profile_params = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth', 'orientation', 'city_id',
                                   'profile_status', 'dp_flag', 'profile_completion_status'],
                                  [i for i in profilelist]))
        profile_params.update(dict.fromkeys(['web_profile_key', 'android_app_profile_key', 'ios_app_profile_key',
                                             'global_profile_key'], get_random_string(length=32)))
        input_json['added_by'] = "EV__" + input_json['added_by']
        profile_params.update(dict.fromkeys(
            ['added_by', 'last_modified_by'], input_json['added_by']))
        input_json.update(profile_params)
        return input_json
    except Exception as ex:
        output_json['Status'] = "Failure"
        output_json[
            'Message'] = f"Exception Encountered while getting profile parameters: {ex}"
        output_json['Payload'] = payload['Payload']
        return output_json


def get_bio_params(request):
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


def get_mapuuidtoprofileid_params(request):
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


def fetch_mapuuidtoprofile(request):
    """Function for fetching row from mapuuidtoprofielid table."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    if 'uuid_id_id' in input_json and 'uuid_id' not in input_json:
        input_json['uuid_id_id'] = input_json['uuid_id_id']
    if 'uuid_id' in input_json and 'uuid_id_id' not in input_json:
        input_json['uuid_id_id'] = input_json['uuid_id']
    try:
        sql = sql_exec("fetch_mapuuidtoprofileid", [
            input_json['uuid_id_id']])[0]
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure', f"Error while fetching details from mapuuidtoprofielid table : {ex}",
                                payload['Payload']]))
        return output_json


def fetch_profiledetails(request):
    """Function for fetching row from profile table."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    if 'profile_id_id' in input_json and 'profile_id' not in input_json:
        input_json['profile_id_id'] = input_json['profile_id_id']
    if 'profile_id' in input_json and 'profile_id_id' not in input_json:
        input_json['profile_id_id'] = input_json['profile_id']
    try:
        sql = sql_exec("fetch_profile", [input_json['profile_id_id']])[0]
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure', f"Error while fetching details from profile table : {ex}",
                                payload['Payload']]))
        return output_json


def fetch_profile_records(request):
    """Function for fetching records from user profile table."""
    input_json, output_json = request, {}
    try:
        sql = sql_fetch_cursor("fetch_profile_records", 'profile_ref',
                               ['profile_ref', input_json['profile_id']])[0]
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message'], ['Failure',
                                                       f"Error occured during checking for profile fields"
                                                       f"table. Encountered Exception: {ex}."]))
        return output_json


def fetch_profile_emailorphone_sql(request):
    """Function for fetching records from user profile table."""
    input_json, output_json = request, {}
    try:
        sql = sql_fetch_cursor("sp_fetch_profile_email_phone", 'profile_ref',
                               ['profile_ref', f"%{input_json['namestring']}%"])[0]
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message'], ['Failure',
                                                       f"Error occured during checking for profile fields"
                                                       f"table. Encountered Exception: {ex}."]))
        return output_json


def fetch_emailverificationotp_sql(request):
    """Function for fetching records from user profile table."""
    input_json, output_json = request, {}
    try:
        input_json['email_id'] = input_json['email_id'].lower()
        sql = sql_fetch_cursor("fetch_emailverificationotp", 'email_ref',
                               ['email_ref', input_json['email_id']])[0]
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message'], ['Failure',
                                                       f"Error occured during checking for profile fields"
                                                       f"table. Encountered Exception: {ex}."]))
        return output_json


def insert_emailverificationotp(request):
    """Function for inserting a row in mobileverification table."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    if 'uuid_id_id' in input_json and 'uuid_id' not in input_json:
        input_json['uuid_id'] = input_json['uuid_id_id']
    if 'uuid_id' in input_json and 'uuid_id_id' not in input_json:
        input_json['uuid_id'] = input_json['uuid_id']
    try:
        input_json['email_id'] = input_json['email_id'].lower()
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

def create_profile(request):
    """Function for inserting a row with generated profile id in profile table for given input."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    try:
        serializer_var = serializer_save(UserProfileSerializer, input_json)
        return serializer_var.data
    except Exception as ex:
        output_json['Status'] = "Failure"
        output_json['Message'] = f"Exception Encountered while creating profile id: {ex}"
        output_json['Payload'] = payload['Payload']
        return output_json


def add_bio(request):
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


def create_mapuuidtoprofileid(request):
    """Function for inserting a row in uuidtoprofileidmap table."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    if 'uuid_id_id' in input_json and 'uuid_id' not in input_json:
        input_json['uuid_id_id'] = input_json['uuid_id_id']
    if 'uuid_id' in input_json and 'uuid_id_id' not in input_json:
        input_json['uuid_id_id'] = input_json['uuid_id']
    if 'profile_status_id' in input_json and 'profile_status' not in input_json:
        input_json['profile_status'] = input_json['profile_status_id']
    if 'profile_status' in input_json and 'profile_status_id' not in input_json:
        input_json['profile_status'] = input_json['profile_status']
    if 'profile_id_id' in input_json and 'profile_id' not in input_json:
        input_json['profile_id_id'] = input_json['profile_id_id']
    if 'profile_id' in input_json and 'profile_id_id' not in input_json:
        input_json['profile_id_id'] = input_json['profile_id']
    try:
        params = dict(zip(['uuid_id', 'profile_id', 'status', 'added_by', 'last_modified_by'],
                          [input_json['uuid_id_id'], input_json['profile_id'], input_json['profile_status'],
                           input_json['added_by'], input_json['last_modified_by']]))
        serializer_var = serializer_save(UuidToProfileIdMapSerializer, params)
        return serializer_var.data
    except Exception as ex:
        output_json['Status'] = "Failure"
        output_json[
            'Message'] = f"Some exception in mapping uuid to profile .Encounter Exception + {ex}"
        output_json['Payload'] = payload['Payload']
        return output_json


def create_userprofile(request):
    """Function for creating user profile for a given input."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    try:
        profile_params = get_profile_params(input_json)
        match = re.findall(r"'Status': 'Failure'", str(profile_params))
        if match:
            return profile_params
        profile_details = create_profile(profile_params)
        match = re.findall(r"'Status': 'Failure'", str(profile_details))
        if match:
            return profile_details
        input_json.update(profile_details)
        bio_params = get_bio_params(profile_details)
        match = re.findall(r"'Status': 'Failure'", str(bio_params))
        if match:
            return bio_params
        bio_details = add_bio(bio_params)
        match = re.findall(r"'Status': 'Failure'", str(bio_details))
        if match:
            return bio_details
        mapuuidtoprofileid_params = get_mapuuidtoprofileid_params(input_json)
        match = re.findall(r"'Status': 'Failure'",
                           str(mapuuidtoprofileid_params))
        if match:
            new_uuid = insert_uuid(input_json)
            match1 = re.findall(r"'Status': 'Failure'", str(new_uuid))
            if match1:
                return new_uuid
            input_json.update(new_uuid)
            mapuuidtoprofileid_details = create_mapuuidtoprofileid(input_json)
            match2 = re.findall(r"'Status': 'Failure'",
                                str(mapuuidtoprofileid_details))
            if match2:
                return mapuuidtoprofileid_details
            return profile_details
        input_json.update(mapuuidtoprofileid_params)
        mapuuidtoprofileid_details = create_mapuuidtoprofileid(input_json)
        match = re.findall(r"'Status': 'Failure'",
                           str(mapuuidtoprofileid_details))
        if match:
            return mapuuidtoprofileid_details
        return profile_details
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Error occured during Registration process. "
                                                                  f"Encountered Exception: {ex}.", payload['Payload']]))
        return output_json


def verify_profile(request):
    """Function for verifying profile details for user verification."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    try:
        mapuuidtoprofiledetails = fetch_mapuuidtoprofile(input_json)
        match = re.findall(r"'Status': 'Failure'",
                           str(mapuuidtoprofiledetails))
        if match:
            user_profile = create_userprofile(input_json)
            match1 = re.findall(r"'Status': 'Failure'", str(user_profile))
            if match1:
                return user_profile
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Success', f"Profile is verified", user_profile]))
            return output_json
        profile_data = fetch_profiledetails(mapuuidtoprofiledetails)
        match2 = re.findall(r"'Status': 'Failure'", str(profile_data))
        if match2:
            profile_data.update(payload)
            return profile_data
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', "profile verified", profile_data]))
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Error"
                                                                             f" while verifying profile details for"
                                                                             f" user.Encountered Exception:"
                                                                             f" {ex}", payload['Payload']]))
        return output_json


def check_profile_fields(request):
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
                                                                   input_json['city_id'],
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


def update_userprofile(request):
    """Function for updating record in user profile table."""
    input_json, output_json, update_params, payload = request, {}, {}, {'Payload': None}
    if 'profile_completion_status' in input_json and 'profile_completion_status_id' not in input_json:
        input_json['profile_completion_status'] = input_json['profile_completion_status']
    if 'profile_completion_status_id' in input_json and 'profile_completion_status' not in input_json:
        input_json['profile_completion_status'] = input_json['profile_completion_status_id']
    try:
        if input_json['profile_completion_status'] == 2:
            update_params = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth', 'orientation', 'city_id',
                                      'dp_flag_id', 'profile_completion_status_id'], [input_json['first_name'],
                                                                                      input_json['last_name'],
                                                                                      input_json['sex'],
                                                                                      input_json['date_of_birth'],
                                                                                      input_json['orientation'],
                                                                                      input_json['city_id'],
                                                                                      input_json['dp_flag'], 1]))
        if input_json['profile_completion_status'] == 1:
            update_params = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth', 'orientation', 'city_id',
                                      'dp_flag_id', 'profile_completion_status_id'],
                                     [input_json['first_name'], input_json['last_name'], input_json['sex'],
                                      input_json['date_of_birth'], input_json['orientation'], input_json['city_id'],
                                      input_json['dp_flag'], 2]))
        UserProfile.objects.filter(pk=input_json['profile_id']).update(first_name=update_params['first_name'],
                                                                       last_name=update_params['last_name'],
                                                                       sex=update_params['sex'],
                                                                       date_of_birth=update_params['date_of_birth'],
                                                                       orientation=update_params['orientation'],
                                                                       city_id=update_params['city_id'],
                                                                       dp_flag_id=update_params['dp_flag_id'],
                                                                       profile_completion_status=update_params
                                                                       ['profile_completion_status_id'])
        qs = UserProfile.objects.filter(pk=input_json['profile_id']).all()
        return qs.values()[0]
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message','Payload'], ['Failure',
                                                       f"Error encountered during updation in user profilemobile "
                                                       f"table. Encountered Exception: {ex}.", None]))
        return output_json


def insert_usersessions(request):
    """Function for inserting a row in session management table ."""
    input_json, output_json = request, {}
    try:
        if input_json['source'] > 2:
            input_json['login_type'] = 'social'
        else:
            input_json['login_type'] = 'native'
        session_var = dict(zip(['profile_id', 'session_key', 'login_source', 'login_type', 'added_by',
                                'added_date', 'last_modified_date', 'last_modified_by', 'status_id', 'vendor_id'],
                               [input_json['profile_id'], get_random_string(length=32), input_json['source'], input_json['login_type'],
                                input_json['added_by'], input_json['added_date'], input_json['last_modified_date'],
                                input_json['last_modified_by'], 1, input_json['vendor_id']]))
        serialized = serializer_save(UserSessionsSerializer, session_var)
        return serialized.data


    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                       f"Error occured during insertion in session"
                                                       f"table. Encountered Exception: {ex}.", None]))
        return output_json


# def check_profilecompletion_createsession(request):
#     input_json, output_json, payload = request, {}, {'Payload': None}
#     if 'profile_completion_status' in input_json and 'profile_completion_status_id' not in input_json:
#         input_json['profile_completion_status'] = input_json['profile_completion_status']
#     if 'profile_completion_status_id' in input_json and 'profile_completion_status' not in input_json:
#         input_json['profile_completion_status'] = input_json['profile_completion_status_id']
#     try:
#         profile_completion = input_json['profile_completion_status']
#         # check if profile_completion=2, stating incomplete profile.
#         if profile_completion == 2:
#             # Update record in user profile table for a given input.
#             user_profile = update_userprofile(input_json)
#             match = re.findall(r"'Status': 'Failure'", str(user_profile))
#             if match:
#                 output_json['Payload'] = user_profile
#                 return output_json
#             # Check whether any field in profile table table is default or none, if yes update profile.
#             profiledetails = check_profile_fields(user_profile)
#             match = re.findall(r"'Status': 'Failure'", str(profiledetails))
#             if match:
#                 input_json['profile_completion_status'] = 1
#                 update_profile_completion = update_userprofile(input_json)
#                 match1 = re.findall(r"'Status': 'Failure'",
#                                     str(update_profile_completion))
#                 if match1:
#                     output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
#                                                       ["Failure", "Issues in updating profile completion status.",
#                                                        update_profile_completion]))
#                     return output_json
#                 output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ["Failure", "User has "
#                                                                                                 "not completed his "
#                                                                                                 "profile",
#                                                                                      update_profile_completion]))
#                 return output_json
#             input_json.update(profiledetails)
#             # Create session for updated user profile.
#             session = insert_usersessions(input_json)
#             match2 = re.findall(r"'Status': 'Failure'", str(session))
#             if match2:
#                 output_json['Payload'] = session
#                 return output_json
#             new_session = dict(zip(["profile_id", "session_id", "session_key"],
#                                    [session["profile_id"], session["session_id"], session["session_key"]]))
#             session_details = dict(zip(['Status', 'Message', 'Payload'],
#                                        ['Success', 'Session created successfully', new_session]))
#             output_json['SessionDetails'] = session_details
#             output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ["Success", "User logged in, "
#                                                                                             "Profile Details "
#                                                                                             "Updated Successfully",
#                                                                                  profiledetails]))
#             return output_json
#         # For profile_completion=1, stating complete profile.
#         if profile_completion == 1:
#             # Create session for user profile with complete profile details.
#             session = insert_usersessions(input_json)
#             match = re.findall(r"'Status': 'Failure'", str(session))
#             if match:
#                 output_json['Payload'] = session
#                 return output_json
#             new_session = dict(zip(["profile_id", "session_id", "session_key"],
#                                    [session["profile_id"], session["session_id"], session["session_key"]]))
#             session_details = dict(zip(['Status', 'Message', 'Payload'],
#                                        ['Success', 'Session created successfully', new_session]))
#             output_json['SessionDetails'] = session_details
#             # Fetch profile record from user profile table for profile_id.
#             profile_data = fetch_profile_records(input_json)
#             match = re.findall(r"'Status': 'Failure'", str(profile_data))
#             if match:
#                 output_json['Payload'] = profile_data
#                 return output_json
#             output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ["Success", "User logged in, "
#                                                                                             "Profile Details "
#                                                                                             "Updated Successfully",
#                                                                                  profile_data]))
#             return output_json
#         output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', 'Issues in fetching'
#                                                                                         ' profile details for'
#                                                                                         ' user',
#                                                                              payload['Payload']]))
#         return output_json
#     except Exception as ex:
#         output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Some issues happened. "
#                                                                                         f"Encountered Exception: "
#                                                                                         f"{ex}",
#                                                                              payload['Payload']]))
#         return output_json


def check_profile_session_updated(request):
    """Function for fetching records from user profile table."""
    input_json, output_json, payload = request, {}, None
    input_json['email_id'] = input_json['email_id'].lower()
    profile_data = fetch_profile(input_json)
    match = re.findall(r"'Status': 'Failure'", str(profile_data))
    if match:
        output_json['Payload'] = profile_data
        return output_json
    profile_completion = profile_data['profile_completion_status_id']
    input_json.update(profile_data)

    # check if profile_completion=2, stating incomplete profile.
    if profile_completion == 2:
        session = insert_usersessions(input_json)
        match = re.findall(r"'Status': 'Failure'", str(session))
        if match:
            output_json['Payload'] = session
            return output_json
        input_json.update(session)
        new_session = dict(zip(["profile_id", "session_id", "session_key"],
                               [session["profile_id"], session["session_id"], session["session_key"]]))
        session_details = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Success', 'Session created successfully', new_session]))
        output_json['SessionDetails'] = session_details
        output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                          ['Success', 'User profile created, please complete your profile',
                                           {'profile_completion_status': profile_completion,
                                            'first_name': input_json['first_name'],
                                            'last_name': input_json['last_name'], 'email_id': input_json['email_id']}]))
        return output_json
    # For profile_completion=1, stating complete profile.
    if profile_completion == 1:
        input_json.update(profile_data)
        # Create session for user profile with complete profile details.
        session = insert_usersessions(input_json)
        match = re.findall(r"'Status': 'Failure'", str(session))
        if match:
            session.update(payload)
            output_json['Payload'] = session
            return output_json
        input_json.update(session)
        new_session = dict(zip(["profile_id", "session_id", "session_key"],
                               [session["profile_id"], session["session_id"], session["session_key"]]))
        session_details = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Success', 'Session created successfully', new_session]))
        output_json['SessionDetails'] = session_details
        # profiledisplay = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth',
        #                            'city_id', 'dp_flag', 'profile_completion_status'],
        #                           [profile_data['first_name'], profile_data['last_name'],
        #                            profile_data['sex'], profile_data['date_of_birth'],
        #                            profile_data['city_id_id'], profile_data['dp_flag_id'],
        #                            profile_data['profile_completion_status_id']]))
        profiledisplay = dict(zip(['profile_completion_status', 'first_name', 'last_name', 'email_id'],
                                  [profile_data['profile_completion_status_id'], profile_data['first_name'],
                                   profile_data['last_name'], input_json['email_id']]))
        # payload_app = get_app_profiledetails(input_json)
        # app_payload = {'payload_app': payload_app}
        # profiledisplay.update(app_payload['payload_app'])
        output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ["Success", "User logged in, "
                                                                                        "Profile Details "
                                                                                        "Updated Successfully",
                                                                             profiledisplay]))
        return output_json
    output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', 'Issues in fetching'
                                                                                    ' profile details for'
                                                                                    ' user',
                                                                         payload['Payload']]))
    return output_json


def insert_uuid(request):
    """Function for inserting uuid for a given email id."""
    input_json, output_json = request, {}
    try:
        if 'source' not in input_json.keys():
            keyparam = [key for key in input_json.keys() if key in ('email_id', 'phone_number')][0]
            if keyparam == 'email_id':
                input_json['source'] = 1
                input_json['email_id'] = input_json['email_id'].lower()
                new_uuid = insert_uuid_params(input_json, str(input_json['email_id']))
                match = re.findall(r"'Status': 'Failure'", str(new_uuid))
                if match:
                    return new_uuid
                return new_uuid
            elif keyparam == 'phone_number':
                input_json['source'] = 2
                new_uuid = insert_uuid_params(input_json, input_json['phone_number'])
                match = re.findall(r"'Status': 'Failure'", str(new_uuid))
                if match:
                    return new_uuid
                return new_uuid
        new_uuid = insert_uuid_params(input_json, input_json['email_id'])
        match = re.findall(r"'Status': 'Failure'", str(new_uuid))
        if match:
            return new_uuid
        return new_uuid
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Error occured while inserting uuid in uuid table."
                                                                  f"Encountered Exception: {ex}.",
                                                                  None]))
        return output_json


def insert_uuid_params(request, arg):
    """Function for inserting uuid for a given email id."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    try:
        if 'source_uuid' not in input_json.keys():
            source_uuid = str(uuid.uuid4())
            vendor = input_json['vendor_id']
            added_by = last_modified_by = arg
            uuid_var = dict(zip(['source_uuid', 'source', 'added_by', 'last_modified_by', 'vendor'],
                                [source_uuid, input_json['source'], added_by, last_modified_by, vendor]))
            serialized_uuid = serializer_save(UuidSerializer, uuid_var)
            return serialized_uuid.data
        elif 'source_uuid' in input_json.keys():
            source_uuid = input_json['source_uuid']
            vendor = input_json['vendor_id']
            added_by = last_modified_by = arg
            uuid_var = dict(zip(['source_uuid', 'source', 'added_by', 'last_modified_by', 'vendor'],
                                [source_uuid, input_json['source'], added_by, last_modified_by, vendor]))
            serialized_uuid = serializer_save(UuidSerializer, uuid_var)
            return serialized_uuid.data

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Error encountered during Registration process."
                                                                  f"Encountered Exception: {ex}.",
                                                                  payload['Payload']]))
        return output_json





def get_app_profiledetails(request):
    input_json, output_json = request, {}
    return output_json

