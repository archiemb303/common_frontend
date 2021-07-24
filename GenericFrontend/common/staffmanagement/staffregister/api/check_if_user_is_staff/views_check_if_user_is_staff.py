"""This API checks if the given user is a staff"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.supportcentre.specificlib.views_lib import fetch_all_ticket_for_user_sql, format_all_ticket_for_user
from common.staffmanagement.staffregister.specificlib.views_lib import check_if_staff_sql
# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class CheckIfUserIsStaffAPI(APIView):
    """This covers the API for checking if the given user is a staff"""
    @common_post_login_authentications
    def post(self, request):
        """Post Function to fetching common questions based on ticket type."""
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        json_params = dict(zip(['profile_id'],
                               [input_json['SessionDetails']['Payload']['profile_id']]))
        output_json['Payload'] = self.check_if_user_is_staff_json(json_params)
        return Response(output_json)

    def check_if_user_is_staff_json(self, request):
        """
        This function checks if the given user is a staff
        :param request: {
                            'profile_id': 1,
                        }
        :return:
        """
        input_json = request
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'User is a staff', dict()]))
        try:
            check_if_staff_var = check_if_staff_sql(input_json)
            match = re.findall(r"'Status': 'Failure'", str(check_if_staff_var))
            if match:
                return check_if_staff_var
            if not check_if_staff_var:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ['Failure', 'User is not a staff', None]))
                return output_json
            output_json['Payload'] = check_if_staff_var[0]
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f'Exception Encountered.Something went wrong {ex}', None]))
            return output_json


