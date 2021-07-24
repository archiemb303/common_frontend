"""Module to validate APIParams for send chat messages."""
import logging
from functools import wraps
from rest_framework.views import Response

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def validation_post_login_update_ticket_status(func):
    """Function to validate send chat messages apiparams."""
    @wraps(func)
    def validation_post_login_update_ticket_status_json(self, request):
        input_json, output_json = request.data['APIParams'], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        try:
            if input_json['ticket_id'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Ticket Id can't be an "
                                                              "empty string.", None]))
                return Response(output_json)

            if input_json['ticket_id'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Ticket Id can't be an "
                                                              "empty json.", None]))
                return Response(output_json)

            if input_json['ticket_id'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Ticket Id can't be "
                                                              "NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['ticket_id'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Ticket Id must be an "
                                                              "integer.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if input_json['current_ticket_status'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Current Ticket Status can't be an "
                                                              "empty string.", None]))
                return Response(output_json)

            if input_json['current_ticket_status'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Current Ticket Status can't be an "
                                                              "empty json.", None]))
                return Response(output_json)

            if input_json['current_ticket_status'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Current Ticket Status can't be "
                                                              "NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['current_ticket_status'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Current Ticket Status must be an "
                                                              "integer.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if input_json['closing_flag'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Closing Flag can't be an "
                                                              "empty string.", None]))
                return Response(output_json)

            if input_json['closing_flag'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Closing Flag can't be an "
                                                              "empty json.", None]))
                return Response(output_json)

            if input_json['closing_flag'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Closing Flag can't be "
                                                              "NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['closing_flag'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "Closing Flag must be an "
                                                              "integer.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)
        return func(self, request)
    return validation_post_login_update_ticket_status_json
