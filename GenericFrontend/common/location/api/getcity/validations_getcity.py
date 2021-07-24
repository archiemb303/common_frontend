"""Funtion to validate getcity field"""
from functools import wraps
from rest_framework.views import Response


def validation_getcity(func):
    """Funtion to validate getcity field."""
    @wraps(func)
    def validation_getcity_json(self, request):
        input_json = request.data['APIParams']
        output_json = {}
        output_json['Status'] = "Success"
        output_json['Message'] = "API params fine to process"
        try:
            if input_json['city_id'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "city_id cannot be 0"
                return Response(output_json)
            if input_json['city_id'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "city_id cannot be Empty string"
                return Response(output_json)

            if input_json['city_id'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "city_id cannot be empty json"
                return Response(output_json)

            if input_json['city_id'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "city_id cannot be null"
                return Response(output_json)
            if isinstance(input_json['city_id'], str):
                output_json['Status'] = "Failure"
                output_json['Message'] = "city_id cannot a String"
                return Response(output_json)
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"city_id missing. Exception encountered: {ex} "
            return Response(output_json)
        return func(self, request)

    return validation_getcity_json
