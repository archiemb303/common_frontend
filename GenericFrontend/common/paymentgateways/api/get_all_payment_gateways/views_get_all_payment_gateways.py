"""API returns details of all available payment gateways"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.paymentgateways.specificlib.views_lib import get_get_all_payment_gateways_sql, get_get_all_payment_gateways_format

# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class GetAllPaymentGatewaysAPI(APIView):
    """API returns details of all available payment gateways"""
    @common_post_login_authentications
    def post(self, request):
        """Post Function to fetch details of all available payment gateways."""
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'SessionDetails', 'Payload'],
                               [input_json['AvailabilityDetails'], input_json['AuthenticationDetails'],
                                input_json['SessionDetails'], None]))
        json_params = dict(zip(['profile_id'],
                               [input_json['SessionDetails']['Payload']['profile_id']]))
        output_json['Payload'] = self.get_all_payment_gateways_json(json_params)
        return Response(output_json)

    def get_all_payment_gateways_json(self, request):
        """
        This function fetches details of all available payment gateways
        :param request:
        :return:
        """
        try:
            payment_gateways_var = get_get_all_payment_gateways_sql()
            match = re.findall(r"'Status': 'Failure'", str(payment_gateways_var))
            if match:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ['Failure', 'payment gateways could not be fetched', payment_gateways_var]))
                return output_json
            formatted_payment_gateway_var = get_get_all_payment_gateways_format(payment_gateways_var)
            match = re.findall(r"'Status': 'Failure'", str(formatted_payment_gateway_var))
            if match:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ['Failure', 'payment gateways fetched but could not be formatted',
                                        str(formatted_payment_gateway_var['Payload'])]))
                return output_json
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Success', 'payment gateways fetched successfully',
                                    dict(zip(['payment_gateways_list'], [formatted_payment_gateway_var['Payload']]))]))

            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Failure", f"Unable to get pg_list. Exception encountered: {ex}", None]))
            return output_json
