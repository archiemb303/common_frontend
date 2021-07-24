"""
This API initiates a new transaction by inserting a record into PaymentGatewayTransactions table
"""
import logging
import re
import requests
from rest_framework.views import APIView, Response
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.sessionmanagement.api.sessioncontrol.views_sessioncontrol import session_control
from common.paymentgateways.api.initiate_payment_gateway_transaction.validations_initiate_payment_gateway_transaction import validation_initiate_payment_gateway_transaction
from common.location.api.get_user_geos.views_get_user_geos import GetUserGeosAPI
from common.location.specificlib.views_lib import get_currency_id_from_text_sql
from common.paymentgateways.specificlib.views_lib import initiate_new_payment_gateway_transaction_sql

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class InitiatePaymentGatewayTransactionAPI(APIView):
    """This API will will initiate the purchase process by creating a new transaction_id which is yet to be fulfilled"""
    @api_authenticate
    @session_control
    @validation_initiate_payment_gateway_transaction
    def post(self, request):
        """Post function to initiate the purchase process by creating a new transaction_id
        which is yet to be fulfilled"""
        input_json, output_json = request.data, {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        output_json['SessionDetails'] = request.data['SessionDetails']
        # local initialization of user's ip based on if the information is passed in the request body or not
        if 'APIParams' not in input_json or 'user_ip' not in input_json['APIParams']:
            # uncomment this part for local and comment it for staging/production
            user_ip_var = None
            # uncomment this part for local and comment it for staging/production

            # uncomment this part for staging/production and comment it for local
            # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            # user_ip_var = x_forwarded_for.split(',')[0]
            # uncomment this part for staging/production and comment it for local
        else:
            user_ip_var = input_json['APIParams']['user_ip']
        json_params = dict(zip(['profile_id', 'amount', 'currency', 'payment_gateway_id', 'user_ip'],
                               [input_json['SessionDetails']['Payload']['profile_id'],
                                input_json['APIParams']['amount'], input_json['APIParams']['currency'],
                                input_json['APIParams']['payment_gateway_id'], user_ip_var]))
        output_json['Payload'] = self.initiate_payment_gateway_transaction_json(json_params)
        return Response(output_json)

    def initiate_payment_gateway_transaction_json(self, request):
        """
        This fucntion first identifies the user's country and then coverts amount to INR if needed and then
        initiates a new transaction by inserting a record into the appropriate table
        :param request: {'profile_id':186, 'amount':'100', 'currency': "USD", 'payment_gateway_id': 1,
        'user_ip': "10.1.1.2"}
        :return:
        """
        try:
            input_json = request
            # getting user's country id
            geo_params = dict(zip(['profile_id', 'user_ip'], [input_json['profile_id'], input_json['user_ip']]))
            user_geo_details = GetUserGeosAPI.get_user_geos_json(request, geo_params)
            match = re.findall(r"'Status': 'Failure'", str(user_geo_details))
            if match:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ["Failure", "Unable to initiate transaction", user_geo_details['Payload']]))
                return output_json

            # getting currency_id from currency text as passed in the input
            currency_details_params = dict(zip(['currency_text'], [input_json['currency']]))
            currency_details = get_currency_id_from_text_sql(currency_details_params)
            match = re.findall(r"'Status': 'Failure'", str(currency_details))
            if match or len(currency_details) == 0:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ["Failure", "Provided currency is not accepted", currency_details['Payload']]))
                return output_json
            currency_id = currency_details[0]['currency_id']
            final_amount = input_json['amount']
            # checking if payment_gateway is 1, then converting the amount and currency to INR
            if input_json['payment_gateway_id'] == 1:
                currency_id, currency_conversion_rate = 2, 1
                if input_json['currency'] == 'AED':
                    currency_conversion_rate = 25
                if input_json['currency'] != 'INR' and input_json['currency'] != 'AED':
                    conversion_rates = requests.get('https://api.exchangeratesapi.io/latest').json()['rates']
                    currency_var = input_json['currency']
                    if currency_var != 'EUR':
                        currency_conversion_rate = conversion_rates['INR'] / conversion_rates[currency_var]
                    else:
                        currency_conversion_rate = conversion_rates['INR']
                final_amount = round(input_json['amount'] * currency_conversion_rate, 2)

            # inserting record into payment gateway transaction table to initiate the payment
            initiation_params = dict(zip(['profile_id', 'session_id', 'amount', 'currency', 'actual_transaction_amount',
                                          'actual_transaction_currency', 'pg_id', 'country_id'],
                                         [input_json['profile_id'], input_json['session_id'], input_json['amount'],
                                          currency_details[0]['currency_id'], final_amount,
                                          currency_id, input_json['payment_gateway_id'],
                                          user_geo_details['Payload']['country_id']]))
            transaction_initiation_var = initiate_new_payment_gateway_transaction_sql(initiation_params)
            match = re.findall(r"'Status': 'Failure'", str(transaction_initiation_var))
            if match:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ["Failure", "Unable to initiate transaction", transaction_initiation_var['Payload']]))
                return output_json
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Success", "Transaction successfully initiated",
                                    transaction_initiation_var['Payload']]))
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Failure", f"Unable to initiate transaction. Exception encountered: {ex}", None]))
            return output_json
