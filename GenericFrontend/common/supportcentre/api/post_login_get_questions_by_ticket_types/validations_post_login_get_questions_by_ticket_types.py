"""Module to validate the APIParams for UpdateSkills."""
from functools import wraps

from rest_framework.views import Response


def validation_post_login_get_questions_by_ticket_type(func):
    """Function to validate Update Skills field."""

    @wraps(func)
    def validation_post_login_get_questions_by_ticket_type_json(self, request):
        """Function to validate update dp fields."""
        input_json, output_json = request.data['APIParams'], {}
        output_json['Status'] = "Success"
        output_json['Message'] = "API params fine to process"
        try:
            if not input_json['ticket_type_id']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "ticket_type_id is missing."
                return Response(output_json)
            if input_json['ticket_type_id'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "ticket_type_id cannot be zero."
                return Response(output_json)
            if input_json['ticket_type_id'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "ticket_type_id cannot be Empty string."
                return Response(output_json)
            if input_json['ticket_type_id'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "ticket_type_id cannot be empty json."
                return Response(output_json)
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"ticket_type_id is missing.{ex}"
            return Response(output_json)
        return func(self, request)
    return validation_post_login_get_questions_by_ticket_type_json
