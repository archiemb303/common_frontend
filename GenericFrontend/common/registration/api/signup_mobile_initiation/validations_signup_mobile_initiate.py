"""Module to validate APIParams for signup initiation through phone number."""
import logging
from functools import wraps
from rest_framework.views import Response


# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def validations_signupmobileinitiate(func):
    """Function to validate apiparams for signup initiation though phone number."""
    @wraps(func)
    def validations_signupmobileinitiate_json(self, request):
        input_json, output_json = request.data['APIParams'], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        try:
            if input_json['phone_number'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Phone Number can't"
                                                                                                " be an empty String.",
                                                                                     None]))
                return Response(output_json)

            if input_json['phone_number'] == 0:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                     "Phone Number can't be 0.", None]))
                return Response(output_json)

            if input_json['phone_number'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Phone Number can't"
                                                                                                " be an empty JSON.",
                                                                                     None]))
                return Response(output_json)

            if input_json['phone_number'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Phone Number cannot "
                                                                                                "be Null.", None]))
                return Response(output_json)

            if not isinstance(input_json['phone_number'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Phone Number "
                                                                                                "must be an integer",
                                                                                     None]))
                return Response(output_json)

            if len(str(input_json['phone_number'])) < 10:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                     "Phone Number cannot be less "
                                                                                     "than 10 digits.", None]))
                return Response(output_json)

            if len(str(input_json['phone_number'])) > 10:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                     "Phone Number cannot be more "
                                                                                     "than 10 digits.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                 f"Exception encountered: {ex}", None]))
            return Response(output_json)

        try:
            if input_json['country_code'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                     "Country Code can't be an empty "
                                                                                     "string.", None]))
                return Response(output_json)

            if input_json['country_code'] == 0:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                     "Country Code cannot be 0.", None]))
                return Response(output_json)

            if input_json['country_code'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                     "Country Code cannot be an empty "
                                                                                     "json.", None]))
                return Response(output_json)

            if input_json['country_code'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                     "Country Code cannot be NULL.",
                                                                                     None]))
                return Response(output_json)

            if not isinstance(input_json['country_code'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                     "Country Code must be an integer",
                                                                                     None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                 f"Exception encountered: {ex}", None]))
            return Response(output_json)
        return func(self, request)
    return validations_signupmobileinitiate_json
