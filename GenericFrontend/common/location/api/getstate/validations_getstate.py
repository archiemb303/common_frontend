"""Funtion to validate getstate field."""
from functools import wraps
from rest_framework.views import Response


def validation_getstate(func):
    """Funtion to validate getstate field."""
    @wraps(func)
    def validation_getstate_json(self, request):
        input_json = request.data['APIParams']
        output_json = {}
        output_json['Status'] = "Success"
        output_json['Message'] = "API params fine to process"
        try:
            if input_json['state_id'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "state_id cannot be 0"
                return Response(output_json)
            if input_json['state_id'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "state_id cannot be Empty string"
                return Response(output_json)
            if input_json['state_id'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "state_id cannot be empty json"
                return Response(output_json)
            if input_json['state_id'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "state_id cannot be null"
                return Response(output_json)
            if isinstance(input_json['state_id'], str):
                output_json['Status'] = "Failure"
                output_json['Message'] = "state_id cannot a String"
                return Response(output_json)
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"state_id missing. Exception encountered: {ex} "
            return output_json
        return func(self, request)

    return validation_getstate_json
