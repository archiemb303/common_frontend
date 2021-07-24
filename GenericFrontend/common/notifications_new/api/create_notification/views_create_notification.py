"""This API will create a notification"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.notifications_new.api.create_notification.validations_create_notification \
    import validation_create_notification
from common.notifications_new.specificlib.views_lib import create_notification

# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class CreateNotificationAPI(APIView):
    """This API will create a notification"""
    @common_post_login_authentications
    @validation_create_notification
    def post(self, request):
        """Post function to crete a notification"""
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        try:
            json_params = input_json['APIParams']
            json_params['profile_id'] = input_json['SessionDetails']['Payload']['profile_id']
            output_json['Payload'] = self.create_notification_json(json_params)
            return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f'Exception Encountered.Something went wrong {ex}', None]))
            return Response(output_json)

    def create_notification_json(self, request):
        """
        This API will create a notification
        :param request: {
                            'notification_text':'new ticket is raised',
                            'type_id':1,
                            'distribution_type_id': 1,
                            'notifier_profile_id': 32/null,
                            'notified_profile_id':55/null,
                            'algorithm_id':10/null,
                            'redirection_url':'url_for_redirection',
                            'comments':'important comment'
                        }
        :return
        """
        input_json = request
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Notification is created successfully', dict()]))
        try:
            # create notification
            create_invoice_var = create_notification(input_json)
            match = re.findall(r"'Status': 'Failure'", str(create_invoice_var))
            if match:
                return create_invoice_var
            output_json['Payload'] = create_invoice_var['Payload']
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', f'Exception Encountered.Something went wrong {ex}', None]))
            return output_json
