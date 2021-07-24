"""This API updates ticket status for the ticket according to user type and current status"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.supportcentre.api.post_login_update_ticket_status.validations_post_login_update_ticket_status \
    import validation_post_login_update_ticket_status
from common.supportcentre.specificlib.views_lib import get_new_ticket_status,update_ticket_status

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class PostLoginUpdateTicketStatusAPI(APIView):
    """This covers the API updating ticket status for the ticket """

    @common_post_login_authentications
    @validation_post_login_update_ticket_status
    def post(self, request):
        """Post Function to update ticket status for the ticket """
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        input_json['APIParams']['profile_id'] = input_json['SessionDetails']['Payload']['profile_id']
        json_params = input_json['APIParams']
        output_json['Payload'] = self.post_login_update_ticket_status_json(json_params)
        return Response(output_json)

    def post_login_update_ticket_status_json(self, request):
        """
        This function updates ticket status for the ticket
        :param request: {
                            'profile_id': 1,
                            'ticket_id':24,
                            'current_ticket_status':1,
                            'closing_flag':0/1
                            'user_type':'staff'/'ticket-owner'
                        }
        :return:
        """
        input_json = request
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'The ticket status is updated successfully', dict()]))
        try:
            # decide new ticket status according to current ticket status and user type
            get_new_status_var = get_new_ticket_status(input_json)
            match = re.findall(r"'Status': 'Failure'", str(get_new_status_var))
            if match:
                return get_new_status_var
            input_json['new_ticket_status'] = get_new_status_var['Payload']
            # update new ticket status for the ticket
            update_ticket_status_var = update_ticket_status(input_json)
            match = re.findall(r"'Status': 'Failure'", str(update_ticket_status_var))
            if match:
                return update_ticket_status_var
            output_json['Payload'] = update_ticket_status_var
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f"Exception Encountered.Something went wrong {ex}", None]))
            return output_json
