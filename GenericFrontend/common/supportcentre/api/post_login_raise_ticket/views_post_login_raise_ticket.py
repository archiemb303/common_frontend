"""This API returns all the values that should be bound to the raise support center ticket form"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.supportcentre.api.post_login_raise_ticket.validations_post_login_raise_ticket import validation_post_login_raise_ticket_type
from common.supportcentre.specificlib.views_lib import raise_ticket_for_logged_in_user


# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class PostLoginRaiseTicketAPI(APIView):
    """This covers the API for raising a support center ticket by a logged in user."""

    @common_post_login_authentications
    @validation_post_login_raise_ticket_type
    def post(self, request):
        """Post Function to fetching common questions based on ticket type."""
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        json_params = dict(zip(['profile_id', 'ticket_details', 'raised_by'],
                               [input_json['SessionDetails']['Payload']['profile_id'], input_json['APIParams'],
                                input_json['SessionDetails']['Payload']['profile_id']]))
        output_json['Payload'] = self.post_post_login_raise_ticket_json(json_params)
        return Response(output_json)

    def post_post_login_raise_ticket_json(self, request):
        """
        This function fetches raises a support centre ticket for the logged in user
        :param request: {
                            'profile_id': 1,
                            'raised_by': 1,
                            'ticket_details':{
                                        "ticket_type_id": 1,
                                        "ticket_question_id": 2,
                                        "subject": "I want to check this out",
                                        "query": "Wow, you guys are so awesome"
                                }
                        }
        :return:
        """
        input_json = request
        raised_ticket_var = raise_ticket_for_logged_in_user(input_json)

        match = re.findall(r"'Status': 'Failure'", str(raised_ticket_var))
        if match:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', 'Ticket could not be raised successfully', None]))
            return output_json
        raised_ticket_details = raised_ticket_var['Payload']
        output_load = dict(zip(['ticket_id', 'subject', 'query', 'ticket_date'],
                               [raised_ticket_details['ticket_id'],
                                raised_ticket_details['ticket_subject'],
                                raised_ticket_details['ticket_query'],
                                raised_ticket_details['added_date']]))
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Support ticket successfully raised', output_load]))
        return output_json
