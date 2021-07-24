"""This API returns all the values that should be bound to the raise support center ticket form"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.supportcentre.specificlib.views_lib import fetch_all_ticket_type_and_questions_sql, \
    fetch_all_ticket_type_and_questions_format

# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class PostLoginGetTicketTypesAPI(APIView):
    """This covers the API for get all ticket types."""

    @common_post_login_authentications
    def post(self, request):
        """Post Function for getting ticket types."""
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        output_json['Payload'] = self.post_login_get_ticket_types_json()
        return Response(output_json)

    def post_login_get_ticket_types_json(self):
        """
        This function fetches all the query types and respective common questions
        :param request: {'profile_id': 186, 'skill_ids': [2,3,4]}
        :return:
        """
        all_tickets = fetch_all_ticket_type_and_questions_sql(self)
        match = re.findall(r"'Status': 'Failure'", str(all_tickets))
        if match:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', 'ticket types and respective questions could not be fetched', None]))
            return output_json

        formatted_sql = fetch_all_ticket_type_and_questions_format(all_tickets)
        match = re.findall(r"'Status': 'Failure'", str(formatted_sql))
        if match:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', 'ticket types and respective questions could not be formatted', None]))
            return output_json
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'ticket types and respective questions Fetched successfully',
                                dict(zip(['ticket_type_list'], [formatted_sql['Payload']]))]))
        return output_json
