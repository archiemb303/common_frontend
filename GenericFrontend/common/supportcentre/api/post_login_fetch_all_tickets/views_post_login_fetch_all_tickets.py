"""This API fetches all tickets generated in the system """
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.supportcentre.specificlib.views_lib import fetch_all_tickets_sql, format_all_ticket_for_user

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class PostLoginFetchAllTicketsAPI(APIView):
    """This covers the API for fetching all tickets generated in the system """
    @common_post_login_authentications
    def post(self, request):
        """Post Function to fetch all tickets generated in the system """
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        json_params = dict(zip(['profile_id'],
                               [input_json['SessionDetails']['Payload']['profile_id']]))
        output_json['Payload'] = self.post_login_fetch_all_tickets_json(json_params)
        return Response(output_json)

    def post_login_fetch_all_tickets_json(self, request):
        """
        This function fetches all tickets generated in the system
        :param request: { }
        :return:
        """
        input_json = request
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'All Tickets are fetched successfully', dict()]))
        fetch_tickets_var = fetch_all_tickets_sql(input_json)
        match = re.findall(r"'Status': 'Failure'", str(fetch_tickets_var))
        if match:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', 'Tickets could not be fetched', fetch_tickets_var]))
            return output_json
        formatted_user_ticket_var = format_all_ticket_for_user(fetch_tickets_var)
        match = re.findall(r"'Status': 'Failure'", str(formatted_user_ticket_var))
        if match:
            return formatted_user_ticket_var
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'users tickets fetched successfully',
                                dict(zip(['tickets_list'], [formatted_user_ticket_var['Payload']]))]))
        return output_json

