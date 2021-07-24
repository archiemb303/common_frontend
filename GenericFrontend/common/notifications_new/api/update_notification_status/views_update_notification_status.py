"""This API will update notification status for a notification"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.notifications_new.api.update_notification_status.validations_update_notification_status \
    import validation_update_notification_status
from common.notifications_new.specificlib.views_lib import update_notifications_status

# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class UpdateNotificationStatusAPI(APIView):
    """This API will update notification status for a notification"""
    @common_post_login_authentications
    @validation_update_notification_status
    def post(self, request):
        """Post function to update notification status for a notification"""
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        try:
            json_params = input_json['APIParams']
            json_params['profile_id'] = input_json['SessionDetails']['Payload']['profile_id']
            output_json['Payload'] = self.update_notification_status_json(json_params)
            return Response(output_json)
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f'Exception Encountered.Something went wrong {ex}', None]))
            return Response(output_json)

    def update_notification_status_json(self, request):
        """
        This API will update notification status for a notification
        :param request: {
                           'individual_notification_id':1,
                           'notification_status':3
                        }
        :return
        """
        input_json = request
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Notification are updated successfully', dict()]))
        try:
            # update status of notifications
            update_status_var = update_notifications_status(input_json)
            match = re.findall(r"'Status': 'Failure'", str(update_status_var))
            if match:
                return update_status_var
            output_json['Payload'] = update_status_var
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f'Exception Encountered.Something went wrong {ex}', None]))
            return output_json
