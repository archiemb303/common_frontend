"""Module to validate the APIParams for login."""
import re
from functools import wraps
from rest_framework.views import Response


def validation_login(func):
    """Funtion to validate logout field."""
    @wraps(func)
    def validations_user_login_json(self, request):
        input_json, output_json = request.data['APIParams'], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
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

            match = re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", input_json['email_id'])
            try:
                if not match.group():
                    output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Not a valid email"
                                                                                                    " id format.",
                                                                                         None]))
                    return Response(output_json)
            except Exception as ex:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Not a valid email"
                                                                                                f" id format.: {ex}",
                                                                                     None]))

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
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', f"Not a valid  password format, password should contain "
                                                              f" at least 1 special character, 1 Capital case letter,"
                                                              f" 1 small case letter, 1 number and minimum of 8 "
                                                              f"characters all put together.: {ex}", None]))
                return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)

        try:
            if input_json['login_type'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Login type can't be "
                                                                                                "an empty string.",
                                                                                     None]))
                return Response(output_json)
            if input_json['login_type'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Login type can't be "
                                                                                                "an empty json.",
                                                                                     None]))
                return Response(output_json)
            if input_json['login_type'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Login type can't be "
                                                                                                "NULL.", None]))
                return Response(output_json)
            if input_json['login_type'] not in ['Native', 'native']:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Invalid Login type.",
                                                                                     None]))
                return Response(output_json)
            if not isinstance(input_json['login_type'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Login type must be a "
                                                                                                "string.", None]))
                return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)
        try:
            if input_json['device'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device can't be "
                                                                                                "an empty string.",
                                                                                     None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "device cannot be Empty string"
                return Response(output_json)
            if input_json['device'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device can't be "
                                                                                                "an empty json.",
                                                                                     None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "device cannot be empty json"
                return Response(output_json)
            if input_json['device'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device can't be "
                                                                                                "NULL", None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "device cannot be null"
                return Response(output_json)
            if not isinstance(input_json['device'], str):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Device must "
                                                                                                "be a string", None]))
                return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)
        try:
            if input_json['guid'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "guid can't be "
                                                                                                "an empty string.",
                                                                                     None]))
                return Response(output_json)
            if input_json['guid'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "guid can't be "
                                                                                                "an empty string.",
                                                                                     None]))
                return Response(output_json)
            if input_json['guid'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "guid can't be "
                                                                                                "NUll.", None]))
                return Response(output_json)
            if not isinstance(input_json['guid'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "guid must be "
                                                                                                "an integer.", None]))
                return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)
        try:
            if input_json['source_id'] == "":
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Source Id can't be "
                                                                                                "an empty string.",
                                                                                     None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "source_id cannot be Empty string"
                return Response(output_json)
            if input_json['source_id'] == {}:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Source Id can't be "
                                                                                                "an empty json.",
                                                                                     None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "source_id cannot be empty json"
                return Response(output_json)
            if input_json['source_id'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Source Id can't be "
                                                                                                "NULL.", None]))
                output_json['Status'] = "Failure"
                output_json['Message'] = "source_id cannot be null"
                return Response(output_json)
            if not isinstance(input_json['source_id'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Source Id must be "
                                                                                                "an integer", None]))
                return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', f"Exception encountered: "
                                                                                            f"{ex}", None]))
            return Response(output_json)
        return func(self, request)
    return validations_user_login_json
