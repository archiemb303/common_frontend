""" This API returns the navigation params necessary for PayTM to process a payment"""
from common.paymentgateways.api.pg_navigators.paytm.get_pg_navigators_paytm.views_paytm_checksum_hashers import generate_checksum


def get_pg_navigators_paytm(request):
    """
    function to find the navigators for users who want to pay using PayTM payment gateway
    :param request: see apidocumentation_get_pg_navigators_paytm.py
    :return:
    """
    try:
        input_json, trans_details, callback_url = request, request['transaction_details'],\
                                                  "http://127.0.0.1:8000/callback_paytm/"
        pg_credentials, navigation_params = request['gateway_details']['pg_cred'],\
                                            dict(zip(['initiation_page', 'call_params'],
                                                     ['collectPaymentPayTM', 'paytm_params']))
        paytm_params, merchant_key = dict(zip(['MID', 'ORDER_ID', 'CUST_ID', 'TXN_AMOUNT', 'CHANNEL_ID',
                                               'WEBSITE', 'INDUSTRY_TYPE_ID', 'CALLBACK_URL'],
                                              [pg_credentials['PAYTM_MERCHANT_ID'], trans_details['pg_transaction_id'],
                                               str(input_json['user_id']), str(trans_details['actual_transaction_amount']),
                                               pg_credentials['PAYTM_CHANNEL_ID'], pg_credentials['PAYTM_WEBSITE'],
                                               pg_credentials['PAYTM_INDUSTRY_TYPE_ID'], callback_url])),\
                                     pg_credentials['PAYTM_SECRET_KEY']

        paytm_params['CHECKSUMHASH'] = generate_checksum(paytm_params, merchant_key)
        navigation_params['call_params'] = paytm_params
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", "PayTM navigators fetched successfully",
                                navigation_params]))
        return output_json

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch PayTM navigation variables. Exception encountered: {ex}",
                                None]))
        return output_json
