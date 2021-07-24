"""Perform  authentication of api"""
import logging
import re
from functools import wraps
from rest_framework.response import Response
from common.utilities.lib import sql_exec
from .validations_authenticateapi import ValidationsAuthenticateApiJson


# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def api_authenticate(func):
    """Perform authentication of api with input parameters."""
    @wraps(func)
    def authenticate_api_json(self, request):
        """Perform authentication of api"""

        # input_json, output_json = request.data['APIDetails'], \
        #                           dict(zip(['AvailabilityDetails', 'AuthenticationDetails'],
        #                                    [request.data['AvailabilityDetails'], dict()]))
        input_json, output_json = request.data['APIDetails'], \
                                  dict(zip([ 'AuthenticationDetails'],
                                           [ dict()]))
        try:
            # Validate input json APIDetails parameters.
            validation_check_var = ValidationsAuthenticateApiJson. \
                validations_authenticate_api_json_function(self, input_json)
            if validation_check_var['Status'] == "Failure":
                output_json['AuthenticationDetails'] = validation_check_var
                return Response(output_json)
            if input_json['dev_key'] != "sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234":
                output_json['AuthenticationDetails'] = dict(zip(['Status', 'Message'],
                                       ["Failure", "DevKey not matching"]))
                return Response(output_json)
            token_vendor_id, token_string, token_type = input_json['token_vendor_id'], \
                                                        input_json['token_string'], input_json['token_type']
            sql = sql_exec("validate_apitoken", [token_vendor_id, token_string, token_type])[0]
            output_json['AuthenticationDetails'] = dict(zip(['Status', 'Message'], [sql['status'], sql['message_out']]))
            match = re.findall(r"'Status': 'Failure'", str(output_json))
            if match:
                return Response(output_json)
            output_json['AuthenticationDetails'] = dict(zip(['Status', 'Message'], ['Success',
                                                                                    'ApiDetails fine to process']))
            request.data.update(output_json)
            return func(self, request)
        except Exception as ex:
            output_json['AuthenticationDetails'] = dict(zip(['Status', 'Message'],
                                   ['Failure', f"Invalid Entry for Api Authentication: {ex}"]))
            return Response(output_json)
    return authenticate_api_json


def api_formdata_authenticate(func):
    """Perform authentication of api with formadata input parameters."""
    @wraps(func)
    def authenticate_api_formdata_json(self, request):
        """Perform authentication of api with formdata input parameters"""
        input_json = request.data.dict()
        input_json['token_type'], input_json['token_vendor_id'] = int(input_json['token_type']), \
                                                                  int(input_json['token_vendor_id'])
        try:
            # Validate input json APIDetails parameters.
            validation_check_var = ValidationsAuthenticateApiJson. \
                validations_authenticate_api_json_function(self, input_json)
            if validation_check_var['Status'] == "Failure":
                output_json = validation_check_var
                return Response(output_json)
            if input_json['dev_key'] != "sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234":
                output_json = dict(zip(['Status', 'Message'],
                                       ["Failure", "DevKey not matching"]))
                return Response(output_json)
            token_vendor_id, token_string, token_type = input_json['token_vendor_id'], \
                                                        input_json['token_string'], input_json['token_type']
            sql = sql_exec("validate_apitoken", [token_vendor_id, token_string, token_type])[0]
            output_json = dict(zip(['Status', 'Message'], [sql['status'], sql['message_out']]))
            match = re.findall(r"'Status': 'Failure'", str(output_json))
            if match:
                return Response(output_json)
            output_json['AuthenticationDetails'] = dict(zip(['Status', 'Message'], ['Success',
                                                                                    'ApiDetails fine to process']))
            request.data['APIDetails'] = output_json
            request.data.dict().update(output_json)
            return func(self, request)
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message'],
                                   ['Failure', f"Invalid Entry for Api Authentication: {ex}"]))
            return Response(output_json)
    return authenticate_api_formdata_json
