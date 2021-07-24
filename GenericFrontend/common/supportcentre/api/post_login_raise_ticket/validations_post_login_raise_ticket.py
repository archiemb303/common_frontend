"""Module to validate the APIParams for UpdateSkills."""
from functools import wraps

from rest_framework.views import Response


def validation_post_login_raise_ticket_type(func):
    """Function to validate Update Skills field."""

    @wraps(func)
    def validation_post_login_raise_ticket_json(self, request):
        """Function to validate update dp fields."""
        input_json, output_json = request.data['APIParams'], {}
        output_json['Status'] = "Success"
        output_json['Message'] = "API params fine to process"
        try:
            # validating entry for ticket_type_id
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

            # validating entry for ticket_question_id
            if not input_json['ticket_question_id']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "ticket_question_id is missing."
                return Response(output_json)
            if input_json['ticket_question_id'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "ticket_question_id cannot be Empty string."
                return Response(output_json)
            if input_json['ticket_question_id'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "ticket_question_id cannot be empty json."
                return Response(output_json)

            # validating entry for subject
            if not input_json['subject']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "subject is missing."
                return Response(output_json)
            if input_json['subject'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "subject cannot be Empty string."
                return Response(output_json)
            if input_json['subject'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "subject cannot be empty json."
                return Response(output_json)

            # validating entry for query
            if not input_json['query']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "query is missing."
                return Response(output_json)
            if input_json['ticket_question_id'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "query cannot be Empty string."
                return Response(output_json)
            if input_json['ticket_question_id'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "query cannot be empty json."
                return Response(output_json)

        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"One or more input parameters is missing.{ex}"
            return Response(output_json)
        return func(self, request)
    return validation_post_login_raise_ticket_json
