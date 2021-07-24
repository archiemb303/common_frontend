"""Module to validate APIParams for create notifications."""
import logging
from functools import wraps
from rest_framework.views import Response

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def validation_create_notification(func):
    """Function to validate send chat messages apiparams."""
    @wraps(func)
    def validation_create_notification_json(self, request):
        input_json, output_json = request.data['APIParams'], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        output_json['SessionDetails'] = request.data['SessionDetails']
        try:
            if input_json['type_id'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Type Id can't be an "
                                                              "empty string.", None]))
                return Response(output_json)

            if input_json['type_id'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Type Id can't be an "
                                                              "empty json.", None]))
                return Response(output_json)

            if input_json['type_id'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Type Id can't be "
                                                              "NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['type_id'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Type Id must be an "
                                                              "integer.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if input_json['distribution_type_id'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Distribution Type Id can't be an "
                                                              "empty string.", None]))
                return Response(output_json)

            if input_json['distribution_type_id'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Distribution Type Id can't be an "
                                                              "empty json.", None]))
                return Response(output_json)

            if input_json['distribution_type_id'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Distribution Type Id can't be "
                                                              "NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['distribution_type_id'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Distribution Type Id must be an "
                                                              "integer.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)
        return func(self, request)
    return validation_create_notification_json
