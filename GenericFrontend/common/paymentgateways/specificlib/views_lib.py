import re
import datetime
from common.utilities.lib import sql_fetch_cursor, serializer_save, serializer_update
from django.utils.crypto import get_random_string
from common.paymentgateways.serializers import PaymentGatewayTransactionsSerializer
from common.paymentgateways.models import PaymentGatewayTransactions

def get_get_all_payment_gateways_sql():
    """
    This function returns the sql output listing all the the payment gateways that we have.
    :param request:
    :return:
    """
    try:
        sql = sql_fetch_cursor("sp_fetch_all_payment_gateways", 'profile_ref',
                               ['profile_ref'])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch payment gateways "
                                           f"Exception encountered: {ex}", None]))
        return output_json


def get_get_all_payment_gateways_format(request):
    """
    this function formats the output as received from get_get_all_payment_gateways_sql
    :param request: list of dictionaries
    :return:
    """
    input_json, payment_gateways_list = request, []

    try:
        for item in input_json:
            each_payment_gateways_details = dict(zip(['payment_gateways_id', 'payment_gateways_name', 'pg_provider'],
                                       [item['pg_id'], item['pg_name'], item['pg_provider_id']]))
            payment_gateways_list.append(each_payment_gateways_details)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", f"payment gateways information successfully.", payment_gateways_list]))
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to format payment gateways information from sql. "
                                           f"Exception encountered{ex}", None]))
        return output_json



def get_payment_gateway_details_sql(request):
    """
    This function returns the sql output listing details of the given payment gateway.
    :param request: {'payment_gateway_id': 2}
    :return:
    """
    input_json, output_json = request, dict()
    try:
        sql = sql_fetch_cursor("sp_payment_gateways_details", 'profile_ref',
                               ['profile_ref', input_json['payment_gateway_id']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch payment gateways "
                                           f"Exception encountered: {ex}", None]))
        return output_json


def initiate_new_payment_gateway_transaction_sql(request):
    """
    This function inserts a record into PaymentGatewayTRansactions table thereby initiating a new transaction
    :param request:
                    {
                        'pg_id': 1,
                        'amount': 100,
                        'currency': 2,
                        'customer_country_id': 186,
                        'caller_session_id': 944,
                        'actual_transaction_amount': 500,
                        'actual_transaction_currency': 4
                    }
    :return:
    """
    input_json = request
    try:
        payment_gateway_trans_param = dict(zip(['pg_transaction_id', 'pg_id', 'amount', 'currency',
                                                'customer_country_id', 'caller_session_id',
                                                'transaction_status', 'actual_transaction_amount',
                                                'actual_transaction_currency'],
                                               [get_random_string(length=10), input_json['pg_id'], input_json['amount'],
                                                input_json['currency'], input_json['country_id'],
                                                input_json['session_id'], 1, input_json['actual_transaction_amount'],
                                                input_json['actual_transaction_currency']]))
        serializer_var = serializer_save(PaymentGatewayTransactionsSerializer, payment_gateway_trans_param)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'New payment gateway transaction initiated successfully', serializer_var.data]))
        return output_json
    except Exception as ex:
        output_json = dict(
            zip(['Status', 'Message', 'Payload'], ['Failure', f'Unable to initiate new payment gateway transaction: {ex}', None]))
        return output_json


def update_pg_trans_request_params(request):
    """
    function to store the request_object that is to be sent to the payment gateway
    :param request:
    :return:
    """
    input_json = request
    try:
        update_params = PaymentGatewayTransactions.objects.filter(pg_transaction_id=input_json['transaction_id']) \
            .update(request_object=input_json['request_object_details'])
        output_json = dict(
            zip(['Status', 'Message', 'Payload'],
                ['Success', 'Updated request object for the transaction', None]))
        return output_json

    except Exception as ex:
        output_json = dict(
            zip(['Status', 'Message', 'Payload'],
                ['Failure', f'Unable to update request object for the transaction: {ex}', None]))
        return output_json


def update_pg_trans_response_params(request):
    """
    This function updates the response received from the Payment Gateway after user has attempted to pay
    :param request:
                    {
                        'transaction_id':"asdf-sdfsd-sadf-werte',
                        'response_object_details': {'sdfg':'dsfgs', 'dsfgsdfg':'fsdgdsgf'},
                        'transaction_status': 3
                    }
    :return:
    """
    input_json = request
    try:
        update_params = PaymentGatewayTransactions.objects.filter(pg_transaction_id=input_json['transaction_id']) \
            .update(response_object=input_json['response_object_details'],
                    transaction_status=input_json['transaction_status'])
        output_json = dict(
            zip(['Status', 'Message', 'Payload'],
                ['Success', 'Updated request object for the transaction', None]))
        return output_json

    except Exception as ex:
        output_json = dict(
            zip(['Status', 'Message', 'Payload'],
                ['Failure', f'Unable to update request object for the transaction: {ex}', None]))
        return output_json


def get_all_details_of_pg_transaction_sql(request):
    """ function to get all details related to a particular payment_gateway_transaction_id"""
    input_json = request
    try:
        sql = sql_fetch_cursor("sp_fetch_pg_trans_all_details", 'profile_ref',
                               ['profile_ref', input_json['pg_trans_id']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch payment gateways "
                                           f"Exception encountered: {ex}", None]))
        return output_json
