"""This API will create a notification"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.notifications_new.specificlib.views_lib import find_user_notifications_sql, populate_notifications_sql

# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class PopulateMyNotificationsAPI(APIView):
    """This API will create a notification"""
    @common_post_login_authentications
    def post(self, request):
        """Post function to crete a notification"""
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        try:
            json_params = input_json['APIParams']
            json_params['profile_id'] = input_json['SessionDetails']['Payload']['profile_id']
            output_json['Payload'] = self.populate_my_notifications_json(json_params)
            return Response(output_json)
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f'Exception Encountered.Something went wrong {ex}', None]))
            return output_json

    def populate_my_notifications_json(self, request):
        """
        This API will create a notification
        :param request: {
                           'profile_id':277
                        }
        :return
        """
        input_json = request
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Notifications are populated successfully', dict()]))
        try:
            # find notifications to be populated for a user
            find_user_notifications_var = find_user_notifications_sql(input_json)
            match = re.findall(r"'Status': 'Failure'", str(find_user_notifications_var))
            if match:
                return find_user_notifications_var
            if find_user_notifications_var:
                notification_id_list = [x['notification_id'] for x in find_user_notifications_var]
                input_json['notification_id_list'] = notification_id_list
                # populate the notifications in IndividualNotifications.
                populate_notifications_var = populate_notifications_sql(input_json)
                match = re.findall(r"'Status': 'Failure'", str(populate_notifications_var))
                if match:
                    return populate_notifications_var
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f'Exception Encountered.Something went wrong {ex}', None]))
            return output_json
