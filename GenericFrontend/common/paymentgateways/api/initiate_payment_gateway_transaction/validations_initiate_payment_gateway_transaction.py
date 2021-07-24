"""Module to validate the APIParams for get_package_details."""
from functools import wraps
from rest_framework.views import Response


def validation_initiate_payment_gateway_transaction(func):
    """Function to validate get_package_details field."""
    @wraps(func)
    def validation_initiate_payment_gateway_transaction_json(self, request):
        """Function to validate get_package_details fields."""
        input_json, output_json = request.data['APIParams'], dict(zip(['Status', 'Message', 'Payload'],
                                                                      ['Success', 'API params fine to process', None]))
        try:
            # validating for currency
            if not input_json['currency']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "currency is missing."
                return Response(output_json)
            if input_json['currency'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "currency cannot be zero."
                return Response(output_json)
            if input_json['currency'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "currency cannot be Empty string."
                return Response(output_json)
            if input_json['currency'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "currency cannot be empty json."
                return Response(output_json)

            # validating for amount
            if not input_json['amount']:
                output_json['Status'] = "Failure"
                output_json['Message'] = "amount is missing."
                return Response(output_json)
            if input_json['amount'] == 0:
                output_json['Status'] = "Failure"
                output_json['Message'] = "amount cannot be zero."
                return Response(output_json)
            if input_json['amount'] == "":
                output_json['Status'] = "Failure"
                output_json['Message'] = "amount cannot be Empty string."
                return Response(output_json)
            if input_json['amount'] == {}:
                output_json['Status'] = "Failure"
                output_json['Message'] = "amount cannot be empty json."
                return Response(output_json)

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
            output_json['Message'] = f"input parameter missing: {ex}"
            return Response(output_json)
        return func(self, request)
    return validation_initiate_payment_gateway_transaction_json
