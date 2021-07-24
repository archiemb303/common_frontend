"""This module covers the logout functionality of current and all sessions for verified user."""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.sessionmanagement.models import UserSessions
from .validations_userlogout import validation_logout

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class UserLogoutAPI(APIView):
    """This covers the API for logout of verified user from current_session or all sessions."""
    @common_post_login_authentications
    @validation_logout
    def post(self, request):
        """Function to perform logout of verified user from current_session or all sessions."""
        input_json, output_json = request.data, {}
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        payload =  {'Payload': None}
        output_json['Payload'] = {}
        try:
            logout = self.logout_session(input_json)
            match = re.findall(r"'Status': 'Failure'", str(logout))
            if match:
                output_json['SessionDetails'] = request.data['SessionDetails']
                output_json.update(logout)
                return Response(output_json)
            output_json['Payload'] = logout
            return Response(output_json)
        except Exception as ex:
            output_json['SessionDetails'] = request.data['SessionDetails']
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                 f"Exception encountered while "
                                                                                 f"logging out from current session "
                                                                                 f"or all sessions: {ex}",
                                                                                 payload['Payload']]))
            return Response(output_json)

    def logout_session(self, request):
        """Function to validate logout type input by user from logout type present in UserSessions table."""
        input_json, output_json, payload, logout_type = request, {}, {'Payload': None}, \
                                                        request['APIParams']['logout_type']
        try:
            if logout_type in ('current_session', 'all_sessions'):
                UserSessions.objects.filter(profile_id__exact=input_json["SessionDetails"]["Payload"]['profile_id'],
                                            status_id=1).update(status_id=2, logout_type=logout_type)
                payload['Payload'] = None
                output_json = dict(zip(['Status', 'Message', 'Payload'], ["Success", f"User has been logged out from "
                                                                                     f"{logout_type}",
                                                                          payload['Payload']]))
                return output_json
            output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                      f"Invalid logout type: {logout_type}",
                                                                      payload['Payload']]))
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f"Exception encountered while logging out from session: {ex}",
                                    payload['Payload']]))
            return output_json
