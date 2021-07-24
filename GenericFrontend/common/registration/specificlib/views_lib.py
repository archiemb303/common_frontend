from common.utilities.lib import sql_exec
from collections import defaultdict
from common.registration.serializers import *
from common.registration.models import *
from common.registration.api.signup_mobile_completion.views_signup_mobile_completion import SignUpCompletionMobileAPI
# from common.registration.api.signup_initiation.views_signup_initiation import SignUpInitiationAPI
from datetime import datetime
from rest_framework.views import APIView, Response
from django.utils.crypto import get_random_string
import re

class CheckEmailForRegistration(APIView):
    @classmethod
    def check_email_for_registration_function(self, request):
        input_json_var, output_json, payload = request, {}, {'Payload': None}
        try:
            sql = sql_exec("fetch_row", [input_json_var])[0]
            output_json = dict(zip(['email_presence', 'first_name', 'last_name', 'email_id', 'activation_key',
                                    'activation_status', 'Status', 'Message'],
                                   ["True", sql["first_name"], sql["last_name"], sql["email_id"],
                                    sql["activation_key"], sql['activation_status_id'], "Success",
                                    "email id present in database"]))
            return output_json

        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'email_presence', 'Payload'],
                                   ["Failure",  f"Email id not present in database .Encountered Exception.:{ex}", 'False', payload['Payload']]))
            return output_json

class CompleteUserRegistration(APIView):
    @classmethod
    def complete_user_registration_function(self, request):
        input_json = request
        output_json = wd_uuid_params_var = wd_uuid_params_var = update_fields_var = wd_profile_params_var = \
        wd_uuid_profile_map_params_var = {}
        user_cred_id_var = input_json['id_user_cred_id']
        source = input_json['id_source']
        try:
            if source == "genericfrontend":
                # update_fields_var = dict(zip(['activation_status', 'activation_key', 'mobile_otp'],
                #                              [5, get_random_string(length=32), random.randint(100000, 999999) ]))
                update_fields_var = dict(zip(['activation_status', 'activation_key'],
                                             [5, get_random_string(length=32)]))
                updated_data_var = UpdateActivationStatus.update_activation_status_function(update_fields_var,
                                                                                            user_cred_id_var)
                if updated_data_var['Status'] == "Failure":
                    output_json = updated_data_var
                    return output_json
                try:
                    account_verification_id_object = EmailVerification.objects.get(email_id=user_cred_id_var)
                except Exception as ex:
                    output_json['Status'] = "Failure"
                    output_json['Message'] = "Some Internal DB issues"
                    return output_json
                input_json['email_id'] = input_json['email_id'].lower()
                account_verification_id_var = account_verification_id_object.pk
                current_time = datetime.now()
                email_id_for_added_var = input_json['email_id']
                credlist = [input_json['email_id'], input_json['password'], get_random_string(length=32),
                            str(current_time), account_verification_id_var, 0]
                post_wd_user_credentials_params_var = dict(zip(['email_id', 'password', 'forgot_pwd_key',
                                                                'forgot_pwd_time', 'account_verification_id',
                                                                'login_count'],
                                                               [i for i in credlist]))
                post_wd_user_credentials_params_var.update(dict.fromkeys(['added_by', 'last_modified_by'],
                                                                         str(post_wd_user_credentials_params_var['email_id'])))



                post_wd_user_credentials_details_var = InsertIntoUserCredentials.insert_into_user_credentials_function(
                    self, post_wd_user_credentials_params_var)
                if post_wd_user_credentials_details_var['Status'] == "Failure":
                    output_json = post_wd_user_credentials_details_var
                    return output_json
                cred_id = post_wd_user_credentials_details_var["serializer_data"]['cred_id']  #code change required

            if source != "genericfrontend":
                output_json['Status'] = "Failure"
                output_json['Message'] = "Source does not belong to our website genericfrontend"
                return output_json
            input_json['email_id'] = input_json['email_id'].lower()
            query = EmailVerification.objects.get(email_id=input_json['email_id'])
            serialized = EmailVerificationSerializer(query)
            uuid_var = {}
            uuid_var['uuid'] = serialized.data['uuid']
            newquery = Uuid.objects.get(uuid_id=uuid_var['uuid'])
            wd_uuid_details_var = UuidSerializer(newquery)

            profilelist = [input_json['first_name'], input_json['last_name'], input_json['sex'],
                           input_json['date_of_birth'], input_json['orientation'], input_json['city_id'], 1, 1, 1]
            
            
            # wd_profile_params_var = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth', 'orientation',
            #                                   'profile_status', 'city_id', 'dp_flag'], [i for i in profilelist]))
            wd_profile_params_var = dict(zip(['first_name', 'last_name', 'sex', 'date_of_birth', 'orientation',
                                              'city_id', 'profile_status', 'dp_flag', 'profile_completion_status'], [i for i in profilelist]))
            wd_profile_params_var.update(dict.fromkeys(['web_profile_key', 'android_app_profile_key',
                                                        'ios_app_profile_key', 'global_profile_key'],
                                                       get_random_string(length=32)))
            wd_profile_params_var.update(dict.fromkeys(['added_by', 'last_modified_by'], str(email_id_for_added_var)))
            #Add condition for  default or null , also set profile_completion_status
            wd_profile_details_var = CreateUserProfile.create_user_profile_function(self, wd_profile_params_var)
            if wd_profile_details_var['Status'] == "Failure":
                output_json = wd_profile_details_var
                return output_json
            # return (wd_profile_details_var)
            profiledetails = SignUpCompletionMobileAPI.check_profile_fields(self, wd_profile_details_var['serializer_data'])
            match = re.findall(r"'Status': 'Failure'", str(profiledetails))
            if match:
                return profiledetails
            try:
                add_bio_var = {}
                add_bio_var['short_description'] = " "
                add_bio_var['added_by'] = str(email_id_for_added_var)
                add_bio_var['last_modified_by'] = str(email_id_for_added_var)
                add_bio_var['profile_id'] = wd_profile_details_var['serializer_data']['profile_id']
                serializer_var = AddBioSerializer(data=add_bio_var)   #code change required
                if serializer_var.is_valid(raise_exception=True):
                    serializer_var.save()
                    # bio_id_var = serializer_var.data['bio_id']
            except Exception as ex:
                output_json['Status'] = "Failure"
                output_json['Message'] = "error in adding bio"
                return output_json
            # wd_profile_params_var['add_bio'] = bio_id_var

            wd_uuid_profile_map_params_var['uuid_id'] = wd_uuid_details_var.data['uuid_id']
            wd_uuid_profile_map_params_var['profile_id'] = wd_profile_details_var['serializer_data']['profile_id']
            wd_uuid_profile_map_params_var['status'] = 1
            wd_uuid_profile_map_params_var['added_by'] = str(wd_uuid_profile_map_params_var['profile_id'])
            wd_uuid_profile_map_params_var['last_modified_by'] = str(wd_uuid_profile_map_params_var['profile_id'])
            wd_uuid_profile_map_details_var = MapUuidToProfileId.map_uuid_to_profile_id_function(self,
                                                                                                 wd_uuid_profile_map_params_var)
            if wd_uuid_profile_map_details_var['Status'] == "Failure":
                output_json = wd_uuid_profile_map_details_var
                return output_json

            update_fields_var['activation_status'] = 1
            update_fields_var['activation_key'] = get_random_string(length=32)
            update_fields_var['added_by'] = str(email_id_for_added_var)
            update_fields_var['last_modified_by'] = str(email_id_for_added_var)

            updated_data_var = UpdateActivationStatus.update_activation_status_function(update_fields_var,
                                                                                        user_cred_id_var)
            if updated_data_var['Status'] == "Failure":
                output_json = updated_data_var
                return output_json
            if updated_data_var['Status'] == "Success":
                output_json['Status'] = "Success"
                output_json['Message'] = "User Registered Succesfully. Please login."
                return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"Internal issue in Registration.Encounter Exception: {ex}"
            return output_json


class UpdateActivationStatus(APIView):
    @classmethod
    def update_activation_status_function(self, request, pk):
        output_json = {}
        input_json = request
        try:
            verifiation_object_var = EmailVerification.objects.get(email_id=pk)
            serializer_var = EmailVerificationSerializer(verifiation_object_var, data=input_json, partial=True)

            if serializer_var.is_valid(raise_exception=True):
                serializer_var.save()
                output_json['Status'] = "Success"
                output_json['Message'] = "Status updated Successfully"
                return output_json
            output_json['Status'] = "Failure"
            output_json['Message'] = "Please check if all Fields are valid and is not missing for insertion"
            return output_json

        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "Some internal error occured,Activation Status Updation failed.Encounter Exception"
            return output_json


class InsertIntoUserCredentials(APIView):
    def insert_into_user_credentials_function(self, request):
        output_json = {}
        try:


            serializer_var = UserCredentialsSerializer(data=request)
            if serializer_var.is_valid(raise_exception=True):
                serializer_var.save()
                output_json['Status'] = "Success"
                output_json['Message'] = "Insertion of user Credentials successfull"
                output_json['serializer_data'] = serializer_var.data
                return output_json
            output_json['Status'] = "Failure"
            output_json['Message'] = "Error during saving data in insertcredential table"
            output_json['errors'] = serializer_var.errors
            return output_json

        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "some internal error in inserting data in table.Encounter Excpetion"
            return output_json


class CreateOwnUuid(APIView):
    def create_own_uuid_function(self, request):
        input_json = request
        output_json = {}
        try:
            serializer_var = UuidSerializer(data=input_json)
            if serializer_var.is_valid(raise_exception=True):
                serializer_var.save()
                output_json['Status'] = "Success"
                output_json['Message'] = "Successfully created uuid"
                output_json['serializer_data'] = serializer_var.data
                return output_json
            output_json['Status'] = "Failure"
            output_json['Message'] = "Error in saving the data  into databses"
            output_json['errors'] = serializer_var.errors
            return output_json

        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json[
                'Message'] = "Some internal error in inserting data into createownuuid table.Encounter Exception"
            return output_json


class CreateUserProfile(APIView):
    def create_user_profile_function(self, request):
        output_json = {}                
        try:
            serializer_var = UserProfileSerializer(data=request)  #code change required
            if serializer_var.is_valid(raise_exception=True):
                serializer_var.save()
                output_json['Status'] = "Success"
                output_json['Message'] = "Created profile successfully"
                output_json['serializer_data'] = serializer_var.data
                return output_json

            output_json['Status'] = "Failure"
            output_json['Message'] = "Error in creating profile "
            output_json['errors'] = serializer_var.errors
            return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "Some internal issue while creating profile  --.Encounter Exception"
            return output_json


class MapUuidToProfileId(APIView):
    def map_uuid_to_profile_id_function(self, request):
        output_json = {}
        try:
            serializer_var = UuidToProfileIdMapSerializer(data=request, partial=True)  #code change required
            if serializer_var.is_valid(raise_exception=True):
                serializer_var.save()
                output_json['Status'] = "Success"
                output_json['Message'] = "Map uuid to profile successfully"
                output_json['serializer_data'] = serializer_var.data
                return output_json

            output_json['Status'] = "Failure"
            output_json['Message'] = "Error in mapping uuid to profile"
            output_json['errors'] = serializer_var.errors
            return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"Some exception in mapping .Encounter Exception + {ex}"
            return output_json

class CheckUserCredentials(APIView):
    @classmethod
    def check_user_credentials_function(self, request):
        input_json = request
        output_json = {}
        user_credential_check_var = {}
        user_credential_check_var['activation_status'] = ""
        user_credential_check_var['password_match'] = False
        user_registration_check_var = CheckEmailForRegistration.check_email_for_registration_function(
            input_json['email_id'])
        if user_registration_check_var['email_presence'] == "False":
            output_json['Status'] = "Failure"
            output_json['Message'] = "No user registered with provided email address"
            return output_json

        user_credential_check_var['activation_status'] = user_registration_check_var['activation_status']
        if user_credential_check_var['activation_status'] == 2:
            output_json['Status'] = "Failure"
            output_json['Message'] = "Please complete user registration step 2 to continue further"
            return output_json

        if user_credential_check_var['activation_status'] == 5:
            output_json['Status'] = "Failure"
            output_json['Message'] = "Something went wrong, we are fixin it. Ask user to try again later"
            return output_json

        if user_credential_check_var['activation_status'] == 4:
            output_json['Status'] = "Failure"
            output_json['Message'] = "Inform user that his account has been blocked"
            return output_json

        try:
            usercredentialobject_var = UserCredentials.objects.get(email_id__exact=input_json['email_id'])
            usercredentialserializer = UserCredentialsSerializer(usercredentialobject_var)
            if input_json['password'] == usercredentialserializer.data['password']:
                user_credential_check_var['password_match'] = True
                output_json['Status'] = "Success"
                output_json['Message'] = "password match process is successfully completed"
                output_json['user_credential_output'] = user_credential_check_var
                return output_json
            output_json['Status'] = "Failure"
            output_json['Message'] = "Password does not match please check"
            return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json[
                'Message'] = f"Some major technical issue. Seems like user has completed registration step 2," \
                             f"but his records have not been updated in the db appropriately.Encountered Exception: " \
                             f"{ex}"
            return output_json


class CheckGuidPresence(APIView):
    @classmethod
    def check_guid_presence_function(self, request):

        input_json = request
        output_json = {}
        try:
            wd_uuid_details_var = Uuid.objects.get(source_uuid=input_json['guid'])
            if wd_uuid_details_var.source_name == input_json['source']:
                output_json['Status'] = "Success"
                output_json['Message'] = "wd_uuid present in Database"
                output_json['wd_uuid'] = wd_uuid_details_var
                return output_json
            else:
                output_json['Status'] = "Failure"
                output_json['Message'] = "uuid and source do not match"
                output_json['Exception'] = ''
                return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "wd_uuid is not present in Database"
            output_json['wduid'] = {None}
            output_json['Exception'] = ex
            return output_json


class GetProfileIdsFromGuid(APIView):
    @classmethod
    def get_profile_ids_from_guid_function(self, request):
        try:
            output_json = {}
            input_json = request
            requestparam2_var = Uuid.objects.get(uuid_id=input_json)
            serlizer = UuidSerializer(requestparam2_var)
            wd_uuid_sourceuuid_var = requestparam2_var.uuid_id
            requestparam3_var = UuidToProfileIdMap.objects.get(uuid_id=wd_uuid_sourceuuid_var)
            requestparam3_serializer_var = UuidToProfileIdMapSerializer(requestparam3_var)

            profile_id = requestparam3_serializer_var.data['profile_id']

            output_json['Status'] = "Success"
            output_json['Message'] = "profile id Successfully returned"
            output_json['profile_id'] = profile_id
            return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "Unable to retrieve profile_id"
            output_json['Exception'] = ex
            output_json['profile_id'] = {None}
            return output_json


class GetEmailCredNProfileIdsFromEmailId(APIView):
    def get_email_cred_n_profile_ids_from_email_id_function(self, request, format='json'):
        input_json = request
        output_json = {}
        User_Details_var = {}
        User_Details_var['email_id'] = input_json['email_id']
        User_Details_var['email_verification_id'] = ""
        User_Details_var['profile_id'] = ""
        User_Details_var['added_by'] = str(User_Details_var['profile_id'])
        User_Details_var['last_modified_by'] = str(User_Details_var['profile_id'])
        try:
            email_verification_details_var = EmailVerification.objects.get(email_id__iexact=input_json['email_id'])
            wd_email_verification_details_var = EmailVerificationSerializer(email_verification_details_var)

            User_Details_var['email_verification_id'] = wd_email_verification_details_var.data['emailverification_id']
            if int(wd_email_verification_details_var.data['activation_status']) == 2:
                output_json['Status'] = "Success"
                output_json[
                    'Message'] = "User already tried registering or has registered with us before but has not competed step 2"
                output_json['User_Details'] = User_Details_var
                return (output_json)

            if int(wd_email_verification_details_var.data['activation_status']) == 5:
                output_json['Status'] = "Success"
                output_json['Message'] = "User already tried registering but faced issues in step 2"
                output_json['User_Details'] = User_Details_var
                return (output_json)
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "User has never tried with genericfrontend"
            output_json['Exception'] = ex
            output_json['User_Details'] = User_Details_var
            return (output_json)
        try:
            uuid_obj = wd_email_verification_details_var.data['uuid']
            user_profile_details_var = GetProfileIdsFromGuid.get_profile_ids_from_guid_function(uuid_obj)
            if user_profile_details_var['Status'] == "Success":
                output_json['Status'] = "Success"
                output_json['Message'] = "user details fetched successfully"
                User_Details_var['profile_id'] = user_profile_details_var['profile_id']
            else:
                output_json['Status'] = "Failure"
                output_json['Message'] = " unable to get profile_id"
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Exception'] = ex
            output_json[
                'Message'] = "User has done only registration step 1 and not step 2. Seems like some manual entry in database. Need deep diving"
        output_json['User_Details'] = User_Details_var
        return (output_json)


class ValidatePasswordString(APIView):
    def validate_password_string_function(self, request, format='json'):
        input_json = request
        output_json = {}
        try:
            match = re.search(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~\"])[A-Za-z\d!#$%&'()*+,-./:;<=>?@[\]^_`{|}~\"]{8,}$",
                input_json)
            if match.group():
                pass
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json[
                'Message'] = "Not a valid  password format ,password should atleast 1 special character,1 Capital case letter,1 small case letter,1 number and minimum of 8 character all put together"
            return output_json

        output_json['Status'] = "Success"
        output_json['Message'] = "Password is of valid format"
        return output_json


class GetEmailCredNProfileIdsFromEmailIdForNativeUuid(APIView):
    def get_email_cred_n_profile_ids_from_email_id_for_native_uuid_function(self, request, format='json'):
        input_json = request

        output_json = {}
        User_Details_var = {}
        User_Details_var['email_id'] = input_json['email_id']
        User_Details_var['email_verification_id'] = ""
        User_Details_var['profile_id'] = ""
        User_Details_var['added_by'] = str(User_Details_var['profile_id'])
        User_Details_var['last_modified_by'] = str(User_Details_var['profile_id'])
        try:
            email_verification_details_var = EmailVerification.objects.get(email_id__iexact=input_json['email_id'])
            wd_email_verification_details_var = EmailVerificationSerializer(email_verification_details_var)
            email_verification_id_var = email_verification_details_var.emailverification_id

            User_Details_var['email_verification_id'] = wd_email_verification_details_var.data['emailverification_id']
            if int(wd_email_verification_details_var.data['activation_status']) == 1:
                pass

            User_Details_var['email_serilaized_data'] = wd_email_verification_details_var

            if int(wd_email_verification_details_var.data['activation_status']) == 5:
                output_json['Status'] = "Failure"
                output_json[
                    'Message'] = "Something went wrong. We are fixing it. In the meanwhile you may try registering with another email address"
                output_json['Exception'] = ''
                return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "User has never tried with genericfrontend"
            output_json['Exception'] = ex
            return output_json
        try:
            requestparam1_var = UserCredentials.objects.get(account_verification_id=email_verification_id_var)
            uuid_details_var = {}
            uuid_details_var["email_verification_id"] = email_verification_id_var
            uuid_details_var['guid'] = requestparam1_var.cred_id
            uuid_details_var['source'] = "genericfrontend"
            User_Details_var['cred_id'] = uuid_details_var['guid']
            user_profile_details_var = GetProfileIdsFromGuid.get_profile_ids_from_guid_function(uuid_details_var)
            if user_profile_details_var['Status'] == "Success":
                output_json['Status'] = "Success"
                output_json['Message'] = "user details fetched successfully"
                User_Details_var['profile_id'] = user_profile_details_var['profile_id']
            else:
                output_json['Status'] = "Failure"
                output_json['Message'] = "Unable to get profile_id"
                output_json['Exception'] = user_profile_details_var['Exception']
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Exception'] = ex
            output_json[
                'Message'] = "User has done only registration step 1 and not step 2. Seems like some manual entry in database. Need deep diving"
            output_json['User_Details'] = User_Details_var
            return output_json

        output_json['User_Details'] = User_Details_var
        return output_json


class CheckUuidNProfileId(APIView):
    def check_uuid_n_profile_id_function(self, request, format='json'):
        input_json = request
        output_json = {}
        try:
            guid_primary_key_object = CheckGuidPresence.check_guid_presence_function(input_json)
            if guid_primary_key_object['Status'] == "Failure":
                output_json['Status'] = "Failure"
                output_json['Message'] = "Some Internal issue"
                output_json['Exception'] = guid_primary_key_object['Exception']
                return output_json

            requestparam1_var = UserCredentials.objects.get(email_id__exact=input_json['email_id'])
            uuid_details_var = {}
            uuid_details_var['guid'] = requestparam1_var.cred_id
            uuid_details_var['source'] = "genericfrontend"
            user_profile_details_var = GetProfileIdsFromGuid.get_profile_ids_from_guid_function(uuid_details_var)
            if user_profile_details_var['Status'] == "Failure":
                output_json['Status'] = "Failure"
                output_json['Message'] = "No Profile for given Guid exists" + user_profile_details_var['Message']
                output_json['Exception'] = ''
                return output_json

            guid_primary_key_var = guid_primary_key_object['wd_uuid'].wd_uuid
            try:
                check_profile_with_guid_var = UuidToProfileIdMap.objects.get(wd_uuid__exact=guid_primary_key_var,
                                                                               wd_profile_id__exact=
                                                                               user_profile_details_var['profile_id'])
            except Exception as ex:
                output_json['Status'] = "Failure"
                output_json['Message'] = "Some Internal issue"
                output_json['Exception'] = ex
                return output_json

            output_json['Status'] = "Success"
            output_json['Message'] = "Guid and Email match the same profile"
            output_json['wd_uuid'] = check_profile_with_guid_var
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "guid does not match the given email_id"
            output_json['Exception'] = ex
            return output_json
        return output_json


class CheckProfileIdFromEmailIdWithInputProfileId(APIView):
    def check_profile_from_email_id_with_input_profile_id_function(self, request, format='json'):
        input_json = request
        output_json = {}
        try:
            requestparam1_var = UserCredentials.objects.get(email_id__exact=input_json['email_id'])
            uuid_details_var = {}
            uuid_details_var['guid'] = requestparam1_var.cred_id
            uuid_details_var['source'] = "genericfrontend"
            user_profile_details_var = GetProfileIdsFromGuid.get_profile_ids_from_guid_function(uuid_details_var)
            if user_profile_details_var['Status'] == "Failure":
                output_json['Status'] = "Failure"
                output_json['Message'] = user_profile_details_var['Message']
                return output_json
            db_profile_var = user_profile_details_var['profile_id']

            if db_profile_var == input_json['profile_id']:
                output_json['Status'] = "success"
                output_json['Message'] = "Profile_id from database matches with input profile_id for the input email_id"
                return output_json

            output_json['Status'] = "Failure"
            output_json['Message'] = "Profile_id not matching in database for the  provided email_id's profile_id"
            return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "Some Internal Error"
            return output_json
        return output_json


def check_existing_user_by_email(request):
    """Function for checking whether user is existing or new for the provided email id."""
    input_json, output_json, payload = request, {}, {'Payload': None}
    try:
        credential_id_var = EmailVerificationOtp.objects.filter(email_id=input_json['email_id']). \
            values('emailverificationotp_id')
        number_of_entries_var = credential_id_var.count()
        payload['Payload'] = number_of_entries_var
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
        existing_user_status = options[number_of_entries_var]
        return existing_user_status
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure', f"Exception encountered while checking for exisitng user email"
                                           f" id during Registration process :{ex}", payload['Payload']]))
        return output_json
