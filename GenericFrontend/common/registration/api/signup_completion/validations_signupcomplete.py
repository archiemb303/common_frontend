"""Module to validate APIParams for signup completion."""
import logging
import re
from functools import wraps
from rest_framework.views import Response

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def validation_signupcomplete(func):
    """Funtion to validate logout field."""
    @wraps(func)
    def validation_signupcomplete_json(self, request):
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
            if not isinstance(input_json['email_id'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Email Id must be a "
                                                                                                "string.", None]))
                return Response(output_json)
            if input_json['email_id'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Email Id can't be "
                                                                                                "NULL.", None]))

                return Response(output_json)

            if input_json['email_id'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Email Id must be a "
                                                                                                "string.", None]))
                return Response(output_json)
            if input_json['email_id'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Email Id can't be an "
                                                                                                "empty json.", None]))
                return Response(output_json)
            try:
                match = re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", input_json['email_id'])
                if not match:
                    output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Not a valid email"
                                                                                                    " id format.",
                                                                                         None]))
                    return Response(output_json)
            except Exception as ex:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Not a valid email"
                                                                                                f" id format.: {ex}",
                                                                                     None]))
                return Response(output_json)

        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if input_json['password'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Password can't be an "
                                                                                                "empty json.", None]))
                return Response(output_json)

            if input_json['password'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Password can't be an "
                                                                                                "empty string.", None]))
                return Response(output_json)

            if not isinstance(input_json['password'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Password must be "
                                                                                                "string.", None]))

                return Response(output_json)

            try:
                match = re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~\"])"
                                  r"[A-Za-z\d!#$%&'()*+,-./:;<=>?@[\]^_`{|}~\"]{8,}$", input_json['password'])
                if not match.group():
                    output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Not a valid "
                                                                                                    "password format.",
                                                                                         None]))
            except Exception as ex:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Not a valid  password"
                                                                                               f" format, password "
                                                                                               f"should contain "
                                                                                               f" at least 1 special "
                                                                                               f"character, 1 Capital"
                                                                                               f"case letter, 1 small"
                                                                                               f" case letter, 1 number"
                                                                                               f" and minimum of 8 "
                                                                                               f"characters all put "
                                                                                               f"together.: {ex}",
                                                                                    None]))
                return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if not isinstance(input_json['activation_key'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Activation Key must "
                                                                                                "be a string. ", None]))
                return Response(output_json)

            if input_json['activation_key'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Activation Key can't "
                                                                                                "be an empty string.",
                                                                                     None]))
                return Response(output_json)
            if input_json['activation_key'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Activation Key can't "
                                                                                                "be an empty json.",
                                                                                     None]))
                return Response(output_json)
            if input_json['activation_key'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Email Id must be a "
                                                                                                "string.", None]))
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
        return func(self, request)
    return validation_signupcomplete_json
