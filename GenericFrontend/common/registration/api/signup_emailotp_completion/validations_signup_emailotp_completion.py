"""Module to validate APIParams for signup completion."""
import logging
from functools import wraps
from rest_framework.views import Response

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def validation_signupemailotpcomplete(func):
    """Function to validate signup completion apiparams."""
    @wraps(func)
    def validation_signupemailotpcomplete_json(self, request):
        input_json, output_json = request.data['APIParams'], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']

        try:
            if input_json['first_name'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "First Name can't"
                                                                                                " be an empty String.",
                                                                                     None]))
                return Response(output_json)

            if input_json['first_name'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "First Name can't"
                                                                                                " be an empty json.",
                                                                                     None]))
                return Response(output_json)

            if input_json['first_name'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "First Name can't"
                                                                                                " be NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['first_name'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "First Name must"
                                                                                                " be string.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if input_json['last_name'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Last Name can't"
                                                                                                " be an empty String.",
                                                                                     None]))
                return Response(output_json)

            if input_json['last_name'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "First Name can't"
                                                                                                " be an empty json.",
                                                                                     None]))
                return Response(output_json)

            if input_json['last_name'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Last Name can't"
                                                                                                " be NULL.",
                                                                                     None]))
                return Response(output_json)

            if not isinstance(input_json['last_name'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                     "Last Name must be string.",
                                                                                     None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if input_json['sex'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Sex can't "
                                                                                                " be an empty string.",
                                                                                     None]))
                return Response(output_json)

            if input_json['sex'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Sex can't "
                                                                                                " be an empty string.",
                                                                                     None]))
                return Response(output_json)

            if input_json['sex'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Sex can't be NULL. ",
                                                                                     None]))
                return Response(output_json)

            if not isinstance(input_json['sex'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Sex must be a string.",
                                                                                     None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)
        try:
            if input_json['orientation'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Orientation can't be"
                                                                                                "an empty string.",
                                                                                     None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "Orientation can't be an empty String"
                return Response(output_json)

            if input_json['orientation'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Orientation can't be"
                                                                                                "an empty json.",
                                                                                     None]))
                return Response(output_json)

            if input_json['orientation'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Orientation can't be "
                                                                                                "NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['orientation'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Sex must be a string.",
                                                                                     None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if input_json['date_of_birth'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Date of birth can't be"
                                                                                                "an empty string.",
                                                                                     None]))
                return Response(output_json)

            if input_json['date_of_birth'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Date of birth can't be"
                                                                                                "an empty json.",
                                                                                     None]))
                return Response(output_json)

            if input_json['date_of_birth'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Date of birth can't be"
                                                                                                "NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['date_of_birth'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Date of birth must be"
                                                                                                "a string.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if input_json['city_id'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "City ID can't be an "
                                                                                                "empty string.", None]))
                return Response(output_json)

            if input_json['city_id'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "City ID can't be an "
                                                                                                "empty json.", None]))
                return Response(output_json)

            if input_json['city_id'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "City ID can't be "
                                                                                                "NULL.", None]))
                return Response(output_json)

            if not isinstance(input_json['city_id'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "City ID must be an "
                                                                                                "integer.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if input_json['dp_id'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Dp ID can't be an "
                                                                                                "empty string.", None]))
                return Response(output_json)

            if input_json['dp_id'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Dp ID can't be an "
                                                                                                "empty json.", None]))
                return Response(output_json)

            if input_json['dp_id'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Dp ID can't be NULL. ",
                                                                                     None]))
                return Response(output_json)

            if not isinstance(input_json['dp_id'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Dp ID must be an "
                                                                                                "integer.", None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)
        return func(self, request)
    return validation_signupemailotpcomplete_json
