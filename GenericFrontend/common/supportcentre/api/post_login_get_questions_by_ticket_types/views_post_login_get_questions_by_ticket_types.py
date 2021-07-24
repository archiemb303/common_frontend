"""This API returns all the values that should be bound to the raise support center ticket form"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.supportcentre.api.post_login_get_questions_by_ticket_types.validations_post_login_get_questions_by_ticket_types import validation_post_login_get_questions_by_ticket_type
from common.supportcentre.specificlib.views_lib import fetch_questions_by_ticket_type_sql

# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class PostLoginGetQuestionsByTicketTypesAPI(APIView):
    """This covers the API for fetching common questions based on ticket type."""

    @common_post_login_authentications
    @validation_post_login_get_questions_by_ticket_type
    def post(self, request):
        """Post Function to fetching common questions based on ticket type."""
        input_json, output_json = request.data, dict()
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        json_params = dict(zip(['ticket_type_id'], [input_json['APIParams']['ticket_type_id']]))
        output_json['Payload'] = self.post_login_get_questions_by_ticket_types_json(json_params)
        return Response(output_json)

    def post_login_get_questions_by_ticket_types_json(self, request):
        """
        This function fetches all the common questions for the user's chosen ticekt_type
        :param request: {'ticket_type_id': 1}
        :return:
        """
        input_json = request
        common_questions = fetch_questions_by_ticket_type_sql(input_json)
        match = re.findall(r"'Status': 'Failure'", str(common_questions))
        if match:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', 'Questions for given ticket_type could not be fetched', None]))
            return output_json
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Questions for given ticket_type fetched successfully',
                                dict(zip(['common_questions_list'], [common_questions]))]))
        return output_json
