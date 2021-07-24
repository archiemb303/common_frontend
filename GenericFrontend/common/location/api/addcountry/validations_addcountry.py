"""this api validate the country input param"""
from functools import wraps
from rest_framework.views import Response


def validation_addcountry(func):
    """Funtion to validate country  field."""
    @wraps(func)
    def validation_addcountry_json(self, request):
        input_json = request.data['APIParams']
        output_json = {}
        output_json['Status'] = "Success"
        output_json['Message'] = "API params fine to process"
        try:
            if input_json['country_name'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "country_name cannot be 0"
                return Response(output_json)
            if input_json['country_name'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "country_name cannot be Empty string"
                return Response(output_json)

            if input_json['country_name'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "country_name cannot be empty json"
                return Response(output_json)

            if input_json['country_name'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "country_name cannot be null"
                return Response(output_json)
            if not isinstance(input_json['country_name'], str):
                output_json['Status'] = "Failure"
                output_json['Message'] = "country_name cannot a Integer"
                return Response(output_json)
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"country_name missing. Exception encountered: {ex} "
            return Response(output_json)

        try:
            if input_json['added_by'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "added_by cannot be 0"
                return Response(output_json)
            if input_json['added_by'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "added_by cannot be Empty string"
                return Response(output_json)

            if input_json['added_by'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "added_by cannot be empty json"
                return Response(output_json)

            if input_json['added_by'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "added_by cannot be null"
                return Response(output_json)
            if not isinstance(input_json['added_by'], str):
                output_json['Status'] = "Failure"
                output_json['Message'] = "added_by cannot a Integer"
                return Response(output_json)
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"added_by missing. Exception encountered: {ex}"
            return Response(output_json)

        try:
            if input_json['last_modified_by'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "last_modified_by cannot be 0"
                return Response(output_json)
            if input_json['last_modified_by'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "last_modified_by cannot be Empty string"
                return Response(output_json)

            if input_json['last_modified_by'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "last_modified_by cannot be empty json"
                return Response(output_json)

            if input_json['last_modified_by'] is None:
                output_json['Status'] = "Failure"
                output_json['Message'] = "last_modified_by cannot be null"
                return Response(output_json)
            if not isinstance(input_json['last_modified_by'], str):
                output_json['Status'] = "Failure"
                output_json['Message'] = "last_modified_by cannot a Integer"
                return Response(output_json)
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"last_modified_by missing. Exception encountered: {ex} "
            return Response(output_json)
        return func(self, request)

    return validation_addcountry_json
