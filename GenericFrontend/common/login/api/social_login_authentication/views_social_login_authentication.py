"""Module to verify API for social login of verified user with session details."""
import logging
import re
import facebook
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.views import APIView, Response

from common.commondecorators.preloginauthentications import common_pre_login_authentications
from common.utilities.lib import sql_fetch_cursor
from common.registration.specificlib.userprofile_lib import verify_profile, \
    fetch_uuid_guid, fetch_profile_uuid, insert_uuid, check_profile_session_updated, fetch_sources, \
    fetch_profile_from_emailotp, fetch_uuid_email, create_mapuuidtoprofileid, insert_emailverificationotp
from .validations_social_login_authenticate import validation_social_login_auth

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class SocialLoginAuthenticationAPI(APIView):
    """This covers the API for login of verified user with session details."""
    @common_pre_login_authentications
    @validation_social_login_auth
    def post(self, request):
        """Function to perform login of verified user with session details."""
        input_json, output_json, vendor_id, json_social_login = request.data["APIParams"], {}, \
                                                                request.data['APIDetails']['token_vendor_id'], \
                                                                {}
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'Payload'],
                               [request.data['AvailabilityDetails'], request.data['AuthenticationDetails'], None]))
        input_json['vendor_id'] = vendor_id
        try:
            # Fetch records from Sources table for input source id.
            json_social_login = self.social_login_auth_json(input_json)
            match = re.findall(r"'Status': 'Failure'", str(json_social_login))
            if match:
                output_json['Payload'] = json_social_login
                return Response(output_json)
            output_json['SessionDetails'] = json_social_login['SessionDetails']
            output_json['Payload'] = json_social_login['Payload']
            return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ["Failure",
                                                                                 f"Session not created due to failure"
                                                                                 f" at fetching payload: {ex}.",
                                                                                 json_social_login['Payload']]))
            return Response(output_json)

    def social_login_auth_json(self, request):
        """Function to perform login of verified user with session details."""
        input_json, output_json, user_details  = request, {}, {}
        try:
            # Fetch records from Sources table for input source id.
            sources = fetch_sources(input_json)
            match = re.findall(r"'Status': 'Failure'", str(sources))
            if match:
                return sources
            if sources['source_id'] < 3 or sources['source_id'] > 4:
                output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure', 'Not a Verified Source', None]))
                return output_json
            if sources['source_id'] == 3:
                user_info = self.fetch_userinfo_facebook(input_json)
                match = re.findall(r"'Status': 'Failure'", str(user_info))
                if match:
                    return user_info
                user_profile = self.get_user_profile(input_json, user_info)
                match = re.findall(r"'Status': 'Failure'", str(user_profile))
                if match:
                    return user_profile
                return user_profile
            if sources['source_id'] == 4:
                user_info = self.fetch_userinfo_google(input_json)
                match = re.findall(r"'Status': 'Failure'", str(user_info))
                if match:
                    return user_info
                user_details['id'] = user_info['sub']
                user_details['email'] = user_info['email']
                user_details['first_name'] = user_info['given_name']
                user_details['last_name'] = user_info['family_name']
                user_profile = self.get_user_profile(input_json, user_details)
                match = re.findall(r"'Status': 'Failure'", str(user_profile))
                if match:
                    return user_profile
                return user_profile
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ["Failure",
                                                                      f"Session not created due to failure at fetching "
                                                                      f"payload: {ex}.", None]))
            return output_json

    def social_login_profile_json(self, request):
        """Function to perform login of verified user with session details."""
        input_json, output_json = request, {}
        try:
            profile_email = fetch_profile_from_emailotp(input_json)
            match = re.findall(r"'Status': 'Failure'", str(profile_email))
            if match:
                input_json['source_guid'] = input_json['source_uuid']
                input_json['source_value'] = input_json['source']
                input_json.pop('source_uuid')
                input_json.pop('source')
                uuid_from_email = fetch_uuid_email(input_json)
                match1 = re.findall(r"'Status': 'Failure'", str(uuid_from_email))
                if match1:
                    new_uuid = insert_uuid(input_json)
                    match2 = re.findall(r"'Status': 'Failure'", str(new_uuid))
                    if match2:
                        output_json['Payload'] = new_uuid
                        return output_json
                    input_json.update(new_uuid)
                if not match1:
                    input_json.update(uuid_from_email)
                insert_emailrecord = insert_emailverificationotp(request)
                match3 = re.findall(r"'Status': 'Failure'", str(insert_emailrecord))
                if match3:
                    output_json['Payload'] = insert_emailrecord
                    return output_json
                input_json.update(insert_emailrecord)
                input_json['uuid_email'] = input_json['uuid_id']
                input_json.pop('uuid_id')
                input_json.pop('uuid')
            if not match:
                input_json.update(profile_email)

            if match:
                input_json['source_uuid'] = input_json['source_guid']
                input_json['source'] = input_json['source_value']
            uuid_from_guid = fetch_uuid_guid(input_json)
            match = re.findall(r"'Status': 'Failure'", str(uuid_from_guid))
            if match:
                # Insert a record into uuid table if input uuid details not present in database.
                new_uuid = insert_uuid(input_json)
                match1 = re.findall(r"'Status': 'Failure'", str(new_uuid))
                if match1:
                    output_json['Payload'] = new_uuid
                    return output_json
                input_json.update(new_uuid)
            if not match:
                input_json.update(uuid_from_guid)
            input_json['uuid_guid'] = input_json['uuid_id']
            profile_guid = fetch_profile_uuid(input_json)
            match = re.findall(r"'Status': 'Failure'", str(profile_guid))
            if match and re.findall(r"'Status': 'Failure'", str(profile_email)):
                input_json['uuid_id'] = input_json['uuid_email']
                input_json.pop('source')
                input_json.pop('source_uuid')
                profile_from_email = verify_profile(input_json)
                match1 = re.findall(r"'Status': 'Failure'", str(profile_from_email))
                if match1:
                    output_json['Payload'] = profile_from_email
                    return output_json
                input_json.pop('uuid_id_id')
                input_json['profile_id'] = profile_from_email['Payload']['profile_id']
                input_json['uuid_id'] = input_json['uuid_guid']
                input_json['source_uuid'] = input_json['source_guid']
                input_json['source'] = input_json['source_value']

                map_uuid_profile = create_mapuuidtoprofileid(input_json)
                match2 = re.findall(r"'Status': 'Failure'", str(map_uuid_profile))
                if match2:
                    return map_uuid_profile
                input_json['source'] = 1
                profile_check = check_profile_session_updated(input_json)
                match3 = re.findall(r"'Status': 'Failure'", str(profile_check))
                if match3:
                    return profile_check

                output_json['SessionDetails'] = profile_check['SessionDetails']
                output_json['Payload'] = profile_check['Payload']
                return output_json
            if match and not re.findall(r"'Status': 'Failure'", str(profile_email)):
                input_json['profile_id'] = profile_email['profile_id']
                map_uuid_profile = create_mapuuidtoprofileid(input_json)
                match1 = re.findall(r"'Status': 'Failure'", str(map_uuid_profile))
                if match1:
                    return map_uuid_profile
                profile_check = check_profile_session_updated(input_json)
                match2 = re.findall(r"'Status': 'Failure'", str(profile_check))
                if match2:
                    return profile_check
                output_json['SessionDetails'] = profile_check['SessionDetails']
                output_json['Payload'] = profile_check['Payload']
                return output_json




            if not match:
                input_json.update(profile_guid)

            if not re.findall(r"'Status': 'Failure'", str(profile_guid)) and re.findall(r"'Status': 'Failure'", str(profile_email)):
                input_json['profile_id'] = profile_guid['profile_id']
                input_json['uuid_id'] = input_json['uuid_email']
                input_json.pop('source')
                input_json.pop('source_uuid')
                map_uuid_profile = create_mapuuidtoprofileid(input_json)
                match = re.findall(r"'Status': 'Failure'", str(map_uuid_profile))
                if match:
                    return map_uuid_profile
                input_json['source'] = 1
                profile_check = check_profile_session_updated(input_json)
                match = re.findall(r"'Status': 'Failure'", str(profile_check))
                if match:
                    return profile_check
                output_json['SessionDetails'] = profile_check['SessionDetails']
                output_json['Payload'] = profile_check['Payload']
                return output_json

            if not re.findall(r"'Status': 'Failure'", str(profile_email)) and not re.findall(r"'Status': 'Failure'", str(profile_guid)):
                if profile_email['profile_id'] != profile_guid['profile_id']:
                    output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                       ["Failure", "Multiple profiles, looks suspicious", None]))
                profile_check = check_profile_session_updated(input_json)
                match = re.findall(r"'Status': 'Failure'", str(profile_check))
                if match:
                    return profile_check
                output_json['SessionDetails'] = profile_check['SessionDetails']
                output_json['Payload'] = profile_check['Payload']
                return output_json

        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ["Failure",
                                                                      f"Session not created due to failure"
                                                                      f" at fetching payload: {ex}.",
                                                                      None]))
            return output_json

    def fetch_sociallogin_secretkey(self, request):
        """Function to fetch uuid from registration_uuid table for input source_uuid."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            sql = sql_fetch_cursor("sp_get_social_login_secret_key", 'secretkey_ref',
                                   ['secretkey_ref', input_json['source']])[0]
            return sql
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f"Issues happened while fetching social login secret key. "
                                               f"Encountered Exception: {ex} ", payload['Payload']]))
            return output_json

    def fetch_userinfo_google(self, request):
        """Fetch profile details from userprofile table for existing uuid.."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            client_id_object_var = self.fetch_sociallogin_secretkey(input_json)
            client_id = client_id_object_var['socialloginsecret_key']
            id_token_var = str(input_json['id_token'])
            id_info_var = id_token.verify_oauth2_token(id_token_var, requests.Request(), client_id)
            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')
            if id_info_var['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ['Failure', "Wrong Issuer of the request", None]))
                return output_json
            return id_info_var
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Issues happened while fetching from google"
                                                                      f" Encountered Exception"
                                                                      f": {ex}", payload['Payload']]))
            return output_json

    def fetch_userinfo_facebook(self, request):
        """Fetch profile details from userprofile table for existing uuid.."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            access_token_var = input_json['access_token']
            graph = facebook.GraphAPI(access_token=access_token_var)
            user_info = graph.get_object(
                id='me',
                fields='first_name, middle_name, last_name, id, currency, hometown, location, locale, email, gender,'
                       ' interested_in, picture.type(large), birthday, cover')

            return user_info
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Issues happened while fetching userinfo "
                                                                      f"from facebook."
                                                                      f" Encountered Exception"
                                                                      f": {ex}", payload['Payload']]))
            return output_json

    def get_user_profile(self, request, user_info):
        """Fetch profile details from userprofile table for existing uuid.."""
        input_json, output_json, payload = request, {}, {'Payload': None}
        try:
            user_info_keylist = ['first_name', 'last_name', 'email']
            keylist = [key for key in user_info_keylist if key not in user_info.keys()]
            if keylist:
                user_info.update(dict.fromkeys(keylist, 'default'))
                user_info['profile_completion_status'] = 2
                input_json.update(dict(zip(['first_name', 'last_name', 'sex', 'orientation',
                                            'profile_completion_status',
                                            'source_uuid'], [user_info['first_name'],
                                                             user_info['last_name'], 'default',
                                                             'default', user_info['profile_completion_status'],
                                                             user_info['id']])))
                input_json['city_id'], input_json['date_of_birth'], input_json['dp_flag'] = 1, '0001-01-01', 1
                input_json['added_by'] = input_json['last_modified_by'] = "EV__" + str(user_info['email'])
                input_json['email_id'] = user_info['email']
                input_json['email_id'] = input_json['email_id'].lower()
                userprofile = self.social_login_profile_json(input_json)
                match = re.findall(r"'Status': 'Failure'", str(userprofile))
                if match:
                    return userprofile
                return userprofile
            user_info['profile_completion_status'] = 2
            input_json.update(dict(zip(['first_name', 'last_name', 'sex', 'orientation', 'profile_completion_status',
                                        'source_uuid'], [user_info['first_name'], user_info['last_name'], 'default',
                                                         'default', user_info['profile_completion_status'],
                                                         user_info['id']])))
            input_json['city_id'], input_json['date_of_birth'], input_json['dp_flag'] = 1, '0001-01-01', 1
            input_json['added_by'] = input_json['last_modified_by'] = "EV__" + str(user_info['email'])
            input_json['email_id'] = user_info['email']
            input_json['email_id'] = input_json['email_id'].lower()
            userprofile = self.social_login_profile_json(input_json)
            match = re.findall(r"'Status': 'Failure'", str(userprofile))
            if match:
                return userprofile
            return userprofile
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Issues happened while fetching user profile."
                                                                      f" Encountered Exception"
                                                                      f": {ex}", payload['Payload']]))
            return output_json
