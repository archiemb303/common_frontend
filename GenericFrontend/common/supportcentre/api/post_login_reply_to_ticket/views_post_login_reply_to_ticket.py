"""This API adds reply to given ticket"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.supportcentre.api.post_login_reply_to_ticket.validations_post_login_reply_to_ticket \
    import validation_post_login_reply_to_ticket
from common.supportcentre.specificlib.views_lib import check_if_ticket_owner_sql, reply_to_ticket, fetch_ticket_details
from common.staffmanagement.staffregister.specificlib.views_lib import check_if_staff_sql
from common.notifications_new.specificlib.views_lib import create_notification

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class PostLoginReplyToTicketAPI(APIView):
    """This covers the API for adding reply to given ticket"""

    @common_post_login_authentications
    @validation_post_login_reply_to_ticket
    def post(self, request):
        """Post Function to fetching common questions based on ticket type."""
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        input_json['APIParams']['profile_id'] = input_json['SessionDetails']['Payload']['profile_id']
        json_params = input_json['APIParams']
        output_json['Payload'] = self.post_login_reply_to_ticket_json(json_params)
        return Response(output_json)

    def post_login_reply_to_ticket_json(self, request):
        """
        This function adds reply to given ticket
        :param request: {
                            'profile_id': 1,
                            'ticket_id':12,
                            'reply_body':"Resolved"
                        }
        :return:
        """
        input_json = request
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'The given ticket is replied successfully', dict()]))
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
            reply_to_ticket_var = reply_to_ticket(input_json)
            match = re.findall(r"'Status': 'Failure'", str(reply_to_ticket_var))
            if match:
                return reply_to_ticket_var
            if check_if_staff_var:
                ticket_details_var = fetch_ticket_details(input_json)
                match = re.findall(r"'Status': 'Failure'", str(ticket_details_var))
                if match:
                    return ticket_details_var

                # defining notification parameters
                type_id, distribution_type_id, algorithm_id = 1, 1, None
                notified_profile_id, notifier_profile_id, desc_var = ticket_details_var['ticket_owner_id'], None, []
                redirection_url = '/post/postloginViewTicketReplies/' + str(input_json['ticket_id'])

                # defining notification description
                desc_text_line1 = "Your ticket was replied by the team."
                desc_text_line2 = f"The ticket id: {input_json['ticket_id']}"
                desc_text_line3 = f"The reply text: {input_json['reply_body']}"
                desc_var.append(desc_text_line1)
                desc_var.append(desc_text_line2)
                desc_var.append(desc_text_line3)
                comments = "Support centre staff has replied to a ticket"
                
                # raising notification
                create_notification_params = dict(
                    zip(['profile_id', 'type_id', 'distribution_type_id', 'notification_text', 'notifier_profile_id',
                         'notified_profile_id', 'redirection_url', 'comments', 'algorithm_id'],
                        [input_json['profile_id'], type_id, distribution_type_id, desc_var, notifier_profile_id,
                         notified_profile_id, redirection_url, comments,
                         algorithm_id]))
                create_notification_var = create_notification(create_notification_params)
                match = re.findall(r"'Status': 'Failure'", str(create_notification_var))
                if match:
                    return create_notification_var
            output_json['Payload'] = reply_to_ticket_var['Payload']
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f"Exception Encountered.Something went wrong {ex}", None]))
            return output_json
