"""This API returns all the values that should be bound to the raise support center ticket form"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.supportcentre.specificlib.views_lib import fetch_all_ticket_for_user_sql, format_all_ticket_for_user

# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class PostLoginFetchMyTicketsAPI(APIView):
    """This covers the API for fetching all support centre tickets raised by the user"""
    @common_post_login_authentications
    def post(self, request):
        """Post Function to fetching common questions based on ticket type."""
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        json_params = dict(zip(['profile_id'],
                               [input_json['SessionDetails']['Payload']['profile_id']]))
        output_json['Payload'] = self.post_login_fetch_my_tickets_json(json_params)
        return Response(output_json)

    def post_login_fetch_my_tickets_json(self, request):
        """
        This function fetches all the support centre tickets raised by logged in user
        :param request: {
                            'profile_id': 1,
                        }
        :return:
        """
        input_json = request
        user_tickets_var = fetch_all_ticket_for_user_sql(input_json)
        match = re.findall(r"'Status': 'Failure'", str(user_tickets_var))
        if match:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', 'user tickets could not be fetched', user_tickets_var]))
            return output_json
        formatted_user_ticket_var = format_all_ticket_for_user(user_tickets_var)
        match = re.findall(r"'Status': 'Failure'", str(formatted_user_ticket_var))
        if match:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', 'user tickets fetched but could not be formatted',
                                    str(formatted_user_ticket_var['Payload'])]))
            return output_json
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'users tickets fetched successfully',
                                dict(zip(['tickets_list'], [formatted_user_ticket_var['Payload']]))]))

        return output_json

