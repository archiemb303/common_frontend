"""Module to validate APIParams for Social Login."""
import logging
from functools import wraps
from rest_framework.views import Response

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def validation_social_login_auth(func):
    """Function to validate signup completion apiparams."""
    @wraps(func)
    def validation_social_login_auth_json(self, request):
        input_json, output_json = request.data['APIParams'], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        try:
            if input_json['device'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device can't"
                                                                                                " be an empty String.",
                                                                                     None]))
                return Response(output_json)

            if input_json['device'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device can't"
                                                                                                " be an empty json.",
                                                                                     None]))
                return Response(output_json)

            if input_json['device'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device can't"
                                                                                                " be NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['device'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device must"
                                                                                                " be string.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        # try:
        #     if input_json['access_token'] == "":
        #         output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Access Token can't"
        #                                                                                         " be an empty String.",
        #                                                                              None]))
        #         return Response(output_json)
        #
        #     if input_json['access_token'] == {}:
        #         output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device can't"
        #                                                                                         " be an empty json.",
        #                                                                              None]))
        #         return Response(output_json)
        #
        #     if input_json['access_token'] is None:
        #         output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Access Token can't"
        #                                                                                         " be NULL.",
        #                                                                              None]))
        #         return Response(output_json)
        #
        #     if not isinstance(input_json['access_token'], str):
        #         output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
        #                                                                              "Access Token must be string.",
        #                                                                              None]))
        #         return Response(output_json)
        #
        # except Exception as ex:
        #     output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
        #                                                                                     f"{ex}", None]))
        #     return Response(output_json)

        try:
            if input_json['device'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device can't be "
                                                                                                "an empty string.",
                                                                                     None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "device cannot be Empty string"
                return Response(output_json)
            if input_json['device'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device can't be "
                                                                                                "an empty json.",
                                                                                     None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "device cannot be empty json"
                return Response(output_json)
            if input_json['device'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device can't be "
                                                                                                "NULL", None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "device cannot be null"
                return Response(output_json)
            if not isinstance(input_json['device'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device must "
                                                                                                "be a string", None]))
                return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)
        try:
            if input_json['source'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Source can't be "
                                                                                                "an empty string.",
                                                                                     None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "source cannot be Empty string"
                return Response(output_json)
            if input_json['source'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Source can't be "
                                                                                                "an empty json.",
                                                                                     None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "source cannot be empty json"
                return Response(output_json)
            if input_json['source'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Source  can't be "
                                                                                                "NULL.", None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "source cannot be null"
                return Response(output_json)
            if not isinstance(input_json['source'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Source must be "
                                                                                                "an integer", None]))
                return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        return func(self, request)
    return validation_social_login_auth_json
