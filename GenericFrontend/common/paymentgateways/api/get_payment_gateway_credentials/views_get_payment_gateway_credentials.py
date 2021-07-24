""" This API will return the credentials of the provided payment_gateway_id """
import logging
import re
from rest_framework.views import APIView, Response
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.sessionmanagement.api.sessioncontrol.views_sessioncontrol import session_control
from common.paymentgateways.api.get_payment_gateway_credentials.validations_get_payment_gateway_credentials \
    import validation_get_payment_gateway_credentials
from common.paymentgateways.specificlib.views_lib import get_payment_gateway_details_sql
# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class GetPaymentGatewayCredentialsAPI(APIView):
    """This API will return the credentials of the provided payment_gateway_id"""
    @api_authenticate
    @session_control
    @validation_get_payment_gateway_credentials
    def post(self, request):
        """Post function to return the credentials of the provided payment_gateway_id"""
        input_json, output_json = request.data, {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        output_json['SessionDetails'] = request.data['SessionDetails']
        json_params = dict(zip(['payment_gateway_id'],
                               [input_json['APIParams']['payment_gateway_id']]))
        output_json['Payload'] = self.get_payment_gateway_credentials_json(json_params)
        return Response(output_json)

    def get_payment_gateway_credentials_json(self, request):
        """
        This function will will return the credentials of the provided payment_gateway_id.
        :param request: {'payment_gateway_id': 1}
        :return:output_json['Payload'] =
        """
        input_json = request
        try:
            payment_gateway_details_var = get_payment_gateway_details_sql(input_json)
            match = re.findall(r"'Status': 'Failure'", str(payment_gateway_details_var))
            if match:
                output_json = payment_gateway_details_var
                return output_json
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Success', 'Payment Gateway details fetched successfully',
                                    dict(zip(['payment_gateway_details'], [payment_gateway_details_var[0]]))]))
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Failure", f"Unable to fetch Payment Gateway details. "
                                               f"Exception encountered: {ex}", None]))
            return output_json
