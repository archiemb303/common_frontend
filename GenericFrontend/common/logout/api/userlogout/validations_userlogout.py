"""Module to test logout functionality for current session and all sessions for verified user."""
import logging
from functools import wraps
from rest_framework.views import Response

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def validation_logout(func):
    """Function to validate logout field."""
    @wraps(func)
    def validations_user_logout_json(self, request):
        """Function to validate logout field for current and all sessions."""
        input_json, output_json = request.data['APIParams'], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        try:
            if input_json['logout_type'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Logout type can't be "
                                                                                                "an empty string.",
                                                                                     None]))
                return Response(output_json)
            if input_json['logout_type'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Logout type can't be "
                                                                                                "an empty json.",
                                                                                     None]))
                return Response(output_json)
            if input_json['logout_type'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Logout type can't be "
                                                                                                "NULL.", None]))
                return Response(output_json)
            if input_json['logout_type'] not in ['current_session', 'all_sessions']:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Invalid Logout type.",
                                                                                     None]))
                return Response(output_json)
            if not isinstance(input_json['logout_type'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Logout type must be a "
                                                                                                "string.", None]))
                return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                 f"Exception encountered: {ex}", None]))
            return Response(output_json)
        return func(self, request)
    return validations_user_logout_json
