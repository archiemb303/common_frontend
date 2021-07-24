"""This API filters all tickets generated in the system based on search query"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.supportcentre.specificlib.views_lib import filter_all_tickets_sql, format_all_ticket_for_user

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class PostLoginFilterAllTicketsAPI(APIView):
    """This covers the API for fetching all tickets generated in the system based on search query"""
    @common_post_login_authentications
    def post(self, request):
        """Post Function to filter all tickets generated in the system """
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        json_params = input_json['APIParams']
        json_params['profile_id'] = input_json['SessionDetails']['Payload']['profile_id']
        output_json['Payload'] = self.post_login_filter_all_tickets_json(json_params)
        return Response(output_json)

    def post_login_filter_all_tickets_json(self, request):
        """
        This function filtering all tickets generated in the system
        :param request: {
                            'search_query':'test query'
                        }
        :return:
        """
        input_json = request
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'All Tickets are fetched and filtered successfully', dict()]))
        try:
            if not input_json['search_query']:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ["Failure", "Search input can't be an empty string", None]))
                return output_json
            filter_tickets_var = filter_all_tickets_sql(input_json)
            match = re.findall(r"'Status': 'Failure'", str(filter_tickets_var))
            if match or not filter_tickets_var:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ["Failure", "No entries found with given search input",
                                        None]))
                return output_json
            formatted_user_ticket_var = format_all_ticket_for_user(filter_tickets_var)
            match = re.findall(r"'Status': 'Failure'", str(formatted_user_ticket_var))
            if match:
                return formatted_user_ticket_var
            output_json['Payload']['tickets_list'] = formatted_user_ticket_var['Payload']
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f'Exception Encountered.Something went wrong {ex}', None]))
            return output_json
