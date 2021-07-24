"""This API will will fetch all notifications for a user"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.notifications_new.specificlib.views_lib import fetch_my_notifications_sql,update_notifications_as_seen
from common.notifications_new.api.populate_my_notifications.views_populate_my_notifications \
    import PopulateMyNotificationsAPI

# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class FetchMyNotificationsAPI(APIView):
    """This API will fetch all notifications for a user"""
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
            output_json['Payload'] = self.fetch_my_notifications_json(json_params)
            return Response(output_json)
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f'Exception Encountered.Something went wrong {ex}', None]))
            return Response(output_json)

    def fetch_my_notifications_json(self, request):
        """
        This API will fetch all notifications for a user.
        :param request: {
                           'profile_id':277
                        }
        :return
        """
        input_json = request
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Notification are fetched successfully', dict()]))
        try:
            # populate new notifications for the user
            populate_notifications_var = PopulateMyNotificationsAPI.populate_my_notifications_json(self, input_json)
            match = re.findall(r"'Status': 'Failure'", str(populate_notifications_var))
            if match:
                return populate_notifications_var
            # fetch all notifications for the user from IndividualNotifications
            fetch_my_notifications_var = fetch_my_notifications_sql(input_json)
            match = re.findall(r"'Status': 'Failure'", str(fetch_my_notifications_var))
            if match:
                return fetch_my_notifications_var
            # update status of all unread notifications for this user as seen
            update_status_var = update_notifications_as_seen()
            match = re.findall(r"'Status': 'Failure'", str(update_status_var))
            if match:
                return update_status_var
            output_json['Payload']['notifications'] = fetch_my_notifications_var
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f'Exception Encountered.Something went wrong {ex}', None]))
            return output_json
