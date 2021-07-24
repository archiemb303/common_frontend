"""Module to validate the APIParams for get_payment_gateway_credentials."""
from functools import wraps
from rest_framework.views import Response


def validation_get_payment_gateway_credentials(func):
    """Function to validate get_payment_gateway_credentials fields."""
    @wraps(func)
    def validation_get_payment_gateway_credentials_json(self, request):
        """Function to validate get_payment_gateway_credentials fields."""
        input_json, output_json = request.data['APIParams'], dict(zip(['Status', 'Message', 'Payload'],
                                                                      ['Success', 'API params fine to process', None]))
        try:
            # validating for payment_gateway_id
            if not input_json['payment_gateway_id']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "payment_gateway_id is missing."
                return Response(output_json)
            if input_json['payment_gateway_id'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "payment_gateway_id cannot be zero."
                return Response(output_json)
            if input_json['payment_gateway_id'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "payment_gateway_id cannot be Empty string."
                return Response(output_json)
            if input_json['payment_gateway_id'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "payment_gateway_id cannot be empty json."
                return Response(output_json)

        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = f"package_id is missing.{ex}"
            return Response(output_json)
        return func(self, request)
    return validation_get_payment_gateway_credentials_json
