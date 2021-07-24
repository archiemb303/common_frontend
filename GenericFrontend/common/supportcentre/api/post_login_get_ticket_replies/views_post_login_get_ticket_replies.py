"""This API returns all the values that should be bound to the raise support center ticket form"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.supportcentre.specificlib.views_lib import get_ticket_replies_sql, get_ticket_replies_format, \
    check_if_ticket_owner_sql
from common.supportcentre.api.post_login_get_ticket_replies.validations_post_login_get_ticket_replies import \
    validation_post_login_get_ticket_replies
from common.staffmanagement.staffregister.specificlib.views_lib import check_if_staff_sql

# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class PostLoginGetTicketRepliesAPI(APIView):
    """This covers the API for fetching all support centre tickets raised by the user"""
    @common_post_login_authentications
    @validation_post_login_get_ticket_replies
    def post(self, request):
        """Post Function to fetching common questions based on ticket type."""
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        json_params = dict(zip(['profile_id', 'ticket_id'],
                               [input_json['SessionDetails']['Payload']['profile_id'], input_json['APIParams']['ticket_id']]))
        output_json['Payload'] = self.post_login_get_ticket_replies_json(json_params)
        return Response(output_json)

    def post_login_get_ticket_replies_json(self, request):
        """
        This function fetches all the support centre tickets raised by logged in user
        :param request: {
                            'profile_id': 1, 'ticket_id' = 1
                        }
        :return:
        """
        input_json = request
        try:
            # check if the user is the ticket owner
            check_if_ticket_owner_var = check_if_ticket_owner_sql(input_json)
            match = re.findall(r"'Status': 'Failure'", str(check_if_ticket_owner_var))
            if match:
                return check_if_ticket_owner_var
            # check if the user is a staff
            check_if_staff_var = check_if_staff_sql(input_json)
            match = re.findall(r"'Status': 'Failure'", str(check_if_staff_var))
            if match:
                return check_if_staff_var
            # raise error if the user is neither the ticket owner nor the staff
            if not check_if_staff_var and not check_if_ticket_owner_var:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ['Failure', 'User is neither a staff nor a ticket owner', None]))
                return output_json
            # getting ticket details and its reply in the sql funciton
            ticket_replies_var = get_ticket_replies_sql(input_json)
            match = re.findall(r"'Status': 'Failure'", str(ticket_replies_var))
            # checking if any ticket exists for given ticket_id and whether this ticket_id belongs to the logged in user also
            if match:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ["Failure", "Ticket details could not be fetched. ", ticket_replies_var]))
                return output_json
            # formatting the output as required by frontend
            formatted_ticket_details = get_ticket_replies_format(ticket_replies_var)
            match = re.findall(r"'Status': 'Failure'", str(formatted_ticket_details))
            if match:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ["Failure",
                                        "Ticket details fetched but could not be formatted",
                                        formatted_ticket_details]))
                return output_json
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Success", "users tickets fetched successfully",
                                    formatted_ticket_details['Payload']]))
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Failure", f"Exception encountered while fetching ticket_details: {ex}",
                                    None]))
            return output_json

