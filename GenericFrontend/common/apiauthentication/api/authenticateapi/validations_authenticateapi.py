"""Module to validate authentication parameters for api access."""
import logging
from rest_framework.views import APIView

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class ValidationsAuthenticateApiJson(APIView):
    """This covers the API for validating authentication parameters for api access."""
    def validations_authenticate_api_json_function(self, request):
        """Perform validation of authentication parameters for api access"""
        input_json, output_json = request, {}
        output_json['Status'] = "Success"
        output_json['Message'] = "API params fine to process"
        try:
            if input_json['token_type'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_type cannot be empty string."
                return output_json
            if input_json['token_type'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_type cannot be empty json."
                return output_json
            if input_json['token_type'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_type cannot be null."
                return output_json
            if not isinstance(input_json['token_type'], int):
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_type must be an integer."
                return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"token_type missing. Exception encountered: {ex}"
            return output_json
        try:
            if input_json['token_vendor_id'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_vendor_id cannot be Empty string"
                return output_json
            if input_json['token_vendor_id'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_vendor_id cannot be empty json"
                return output_json

            if input_json['token_vendor_id'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_vendor_id cannot be null."
                return output_json
            if not isinstance(input_json['token_vendor_id'], int):
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_vendor_id must be an integer."
                return output_json

        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"token_vendor_id missing. Exception encountered: {ex}"
            return output_json

        try:
            if input_json['token_string'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_string cannot be empty string."
                return output_json

            if input_json['token_string'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_string cannot be empty json."
                return output_json

            if input_json['token_string'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_string cannot be null."
                return output_json

            if not isinstance(input_json['token_string'], str):
                output_json['Status'] = "Failure"
                output_json['Message'] = "token_string must be a string."
                return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"token_string missing. Exception encountered: {ex}"
            return output_json
        try:
            if input_json['dev_key'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "dev_key cannot be empty string."
                return output_json

            if input_json['dev_key'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "dev_key cannot be empty json."
                return output_json

            if input_json['dev_key'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "dev_key cannot be null."
                return output_json

            if not isinstance(input_json['dev_key'], str):
                output_json['Status'] = "Failure"
                output_json['Message'] = "dev_key must be a string."
                return output_json
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"dev_key is  missing. Exception encountered: {ex} "
            return output_json
        return output_json
