"""Module to validate APIParams for session management."""
import logging
from rest_framework.views import APIView

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class ValidationsSessionCheckJson(APIView):
    """This covers the API for verification of session details for verified users."""
    def validations_session_check_json_function(self, request):
        """Function to validate session details for verified users."""
        input_json = request
        output_json = {}
        output_json['Status'] = "Success"
        output_json['Message'] = "Session params fine to process"
        try:
            if input_json['profile_id'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "profile_id cannot be 0"
                return output_json

            if input_json['profile_id'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "profile_id cannot be Empty string"
                return output_json

            if input_json['profile_id'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "profile_id cannot be empty json"
                return output_json

            if input_json['profile_id'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "profile_id cannot be null"
                return output_json

            if not isinstance(input_json['profile_id'], int):
                output_json['Status'] = "Failure"
                output_json['Message'] = "profile_id should be an integer"
                return output_json

        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "profile_id missing. Exception encountered: " + str(ex)
            return output_json
        try:
            if input_json['session_id'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "session_id cannot be 0"
                return output_json

            if input_json['session_id'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "session_id cannot be Empty string"
                return output_json

            if input_json['session_id'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "session_id cannot be empty json"
                return output_json

            if input_json['session_id'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "session_id cannot be null"
                return output_json

            if not isinstance(input_json['session_id'], int):
                output_json['Status'] = "Failure"
                output_json['Message'] = "Session_id should be an integer"
                return output_json

        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "session_id missing. Exception encountered: " + str(ex)
            return output_json

        try:
            if input_json['session_key'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "session_key cannot be 0"
                return output_json
            if input_json['session_key'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "session_key cannot be Empty string"
                return output_json

            if input_json['session_key'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "session_key cannot be empty json"
                return output_json

            if input_json['session_key'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "session_key cannot be null"
                return output_json

            if not isinstance(input_json['session_key'], str):
                output_json['Status'] = "Failure"
                output_json['Message'] = "Session_key should be a string"
                return output_json

        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "session_key missing. Exception encountered: " + str(ex)
            return output_json
        return output_json
