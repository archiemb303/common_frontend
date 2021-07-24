"""Module to validate APIParams for create notifications."""
import logging
from functools import wraps
from rest_framework.views import Response

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def validation_update_notification_status(func):
    """Function to validate send chat messages apiparams."""
    @wraps(func)
    def validation_update_notification_status_json(self, request):
        input_json, output_json = request.data['APIParams'], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        output_json['SessionDetails'] = request.data['SessionDetails']
        try:
            if input_json['individual_notification_id'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Notification Id can't be an "
                                                              "empty string.", None]))
                return Response(output_json)

            if input_json['individual_notification_id'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Notification Id can't be an "
                                                              "empty json.", None]))
                return Response(output_json)

            if input_json['individual_notification_id'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Notification Id can't be "
                                                              "NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['individual_notification_id'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Notification Id must be an "
                                                              "integer.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if input_json['notification_status'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Notification Status Id can't be an "
                                                              "empty string.", None]))
                return Response(output_json)

            if input_json['notification_status'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Notification Status Id can't be an "
                                                              "empty json.", None]))
                return Response(output_json)

            if input_json['notification_status'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Notification Status Id can't be "
                                                              "NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['notification_status'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Notification Status Id must be an "
                                                              "integer.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)
        return func(self, request)
    return validation_update_notification_status_json
