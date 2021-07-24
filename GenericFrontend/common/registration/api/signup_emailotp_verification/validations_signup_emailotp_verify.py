"""Module to validate APIParams for signup completion."""
import logging
import re
from functools import wraps
from rest_framework.views import Response

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def validation_signupemailotpverify(func):
    """Function to validate signup completion apiparams."""
    @wraps(func)
    def validation_signupemailotpverify_json(self, request):
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
            if input_json['otp'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "OTP can't be an empty String"
                return Response(output_json)

            if input_json['otp'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "OTP can't be 0"
                return Response(output_json)

            if input_json['otp'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "OTP can't be an empty JSON"
                return Response(output_json)

            if input_json['otp'] is None:
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], ['Failure', "Otp cannot "
                                                                                                "be Null.", None]))
                return Response(output_json)

            if not isinstance(input_json['otp'], int):
                output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                                  ['Failure', "otp must be an integer", None]))
                return Response(output_json)

            if len(str(input_json['otp'])) < 6:
                output_json['Status'] = "Failure"
                output_json['Message'] = "The Input OTP is less than 6 digits"
                return Response(output_json)

            if len(str(input_json['otp'])) > 6:
                output_json['Status'] = "Failure"
                output_json['Message'] = "The Input OTP is more than 6 digits"
                return Response(output_json)

        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "Exception occured" + str(ex)
            return Response(output_json)
        return func(self, request)
    return validation_signupemailotpverify_json
