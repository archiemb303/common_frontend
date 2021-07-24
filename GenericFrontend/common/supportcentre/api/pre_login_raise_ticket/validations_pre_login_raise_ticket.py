"""Module to validate the APIParams for UpdateSkills."""
from functools import wraps

from rest_framework.views import Response


def validation_pre_login_raise_ticket(func):
    """Function to validate Update Skills field."""

    @wraps(func)
    def validation_pre_login_raise_ticket_json(self, request):
        """Function to validate update dp fields."""
        input_json, output_json = request.data['APIParams'], {}
        output_json['Status'] = "Success"
        output_json['Message'] = "API params fine to process"
        try:
            if not input_json['first_name']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "first_name is missing."
                return Response(output_json)
            if input_json['first_name'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "first_name cannot be zero."
                return Response(output_json)
            if input_json['first_name'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "first_name cannot be Empty string."
                return Response(output_json)
            if input_json['first_name'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "first_name cannot be empty json."
                return Response(output_json)

            if not input_json['last_name']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "last_name is missing."
                return Response(output_json)
            if input_json['last_name'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "last_name cannot be zero."
                return Response(output_json)
            if input_json['last_name'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "last_name cannot be Empty string."
                return Response(output_json)
            if input_json['last_name'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "last_name cannot be empty json."
                return Response(output_json)

            if not input_json['email']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "email is missing."
                return Response(output_json)
            if input_json['email'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "email cannot be zero."
                return Response(output_json)
            if input_json['email'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "email cannot be Empty string."
                return Response(output_json)
            if input_json['email'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "email cannot be empty json."
                return Response(output_json)

            if not input_json['code']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "code is missing."
                return Response(output_json)
            if input_json['code'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "code cannot be zero."
                return Response(output_json)
            if input_json['code'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "code cannot be Empty string."
                return Response(output_json)
            if input_json['code'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "code cannot be empty json."
                return Response(output_json)

            if not input_json['mobile']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "mobile is missing."
                return Response(output_json)
            if input_json['mobile'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "mobile cannot be zero."
                return Response(output_json)
            if input_json['mobile'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "mobile cannot be Empty string."
                return Response(output_json)
            if input_json['mobile'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "mobile cannot be empty json."
                return Response(output_json)

            if not input_json['query']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "query is missing."
                return Response(output_json)
            if input_json['query'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "query cannot be zero."
                return Response(output_json)
            if input_json['query'] == "":
                output_json['Status'] = "Failure"
                output_json['query'] = "query cannot be Empty string."
                return Response(output_json)
            if input_json['query'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "query cannot be empty json."
                return Response(output_json)
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"variable missing.{ex}"
            return Response(output_json)
        return func(self, request)
    return validation_pre_login_raise_ticket_json
