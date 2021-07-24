from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from common.sessionmanagement.serializers import *


class CreateNewSession(APIView):
    @classmethod
    def create_new_session_function(self, request):
        input_json, session_details_params_var, output_json = request, {}, {}
        session_details_params_var['profile_id'] = input_json['profile_id']
        session_details_params_var['login_time'] = datetime.now()
        session_details_params_var['logout_time'] = datetime.now()
        session_details_params_var['session_key'] = get_random_string(length=32)
        session_details_params_var['login_source'] = input_json['device']
        session_details_params_var['login_type'] = input_json['login_type']
        session_details_params_var['logout_type'] = 'blank'
        session_details_params_var['last_activity_time'] = datetime.now()
        session_details_params_var['status_id'] = 1
        session_details_params_var['vendor_id'] = input_json['vendor_id']
        session_details_params_var['added_by'] = "UP_" + str(input_json['profile_id'])
        session_details_params_var['last_modified_by'] = "UP_" + str(input_json['profile_id'])
        try:
            session_serializer_var = UserSessionsSerializer(data=session_details_params_var)
            if session_serializer_var.is_valid(raise_exception=True):
                session_serializer_var.save()
                output_json['Status'] = "Success"
                output_json['Message'] = "new session created successfully"
                output_json['SessionDetails'] = session_serializer_var.data
                return output_json
            output_json['Status'] = "Failure"
            output_json['Message'] = "session not created successfully"
            return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"while creating sessiondetails error occur-- .Encounter Exception : {ex}"
            return output_json
