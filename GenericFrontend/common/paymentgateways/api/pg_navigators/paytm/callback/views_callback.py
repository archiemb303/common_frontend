""" This API receives the output from PayTM once user is navigating back to our website after making a payment"""
from datetime import datetime
from django.shortcuts import redirect
from rest_framework.views import APIView
from common.paymentgateways.specificlib.views_lib import update_pg_trans_response_params, \
    get_all_details_of_pg_transaction_sql
from common.finance.ownaccountsandledger.specificlib.views_lib import make_general_ledger_entry
from common.finance.ownaccountsandledger.api.add_account_transaction.views_add_account_transaction \
    import AddAccountTransactionAPI
from common.finance.userwalletsandpackages.api.add_wallet_transaction.views_add_wallet_transaction \
    import AddWalletTransactionAPI
from common.finance.invoice.api.create_invoice.views_create_invoice import CreateInvoiceAPI
import logging

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class CallBackPayTMAPI(APIView):
    """ This API reads the response from the payment gateway and then does appropriate processes"""
    def post(self, request):
        """ Post function that reads the response from the payment gateway and then does appropriate processes"""
        input_json = request.data
        output_json = self.call_back_paytm_json(input_json)
        # uncomment this part for local and comment it for staging/production
        return redirect(f"http://localhost:4200/post/getPGTransOutput/{output_json['Payload']['pg_transaction_id']}")
        # uncomment this part for local and comment it for staging/production

        # uncomment this part for staging/production and comment it for local
        # return redirect(f"https://akstagefe.com/post/getPGTransOutput/{output_json['Payload']['pg_transaction_id']}")
        # uncomment this part for staging/production and comment it for local

    def call_back_paytm_json(self, request):
        """ JSON function that reads the response from the payment gateway and then does appropriate processes"""
        # initializing default transaction_status to "failed"
        input_json, transaction_status_var, output_json = request, 2, dict(zip(['transaction_ref'], [request['ORDERID']]))
        try:
            # For returned order_id update response object in paymentgatewaytransactions table
            if input_json['STATUS'] == "TXN_SUCCESS":
                # initialize transaction status to success
                transaction_status_var = 3
            update_response_params = dict(zip(['transaction_id', 'response_object_details', 'transaction_status'],
                                              [input_json['ORDERID'], input_json, transaction_status_var]))
            updated_transaction_var = update_pg_trans_response_params(update_response_params)

            # For this order_id find the associated_bank_account_id by calling function named
            # get_all_details_for_transaction_id
            fetch_trans_details_params = dict(zip(['pg_trans_id'], [input_json['ORDERID']]))
            trans_details_var = get_all_details_of_pg_transaction_sql(fetch_trans_details_params)[0]

            # make an entry in general ledger table even if the transaction is failed.
            # creating a description for the entry in general ledger table
            gl_transaction_description = f"purchase of {trans_details_var['no_of_credits']} wallet points. " \
                                         f"package_price: {trans_details_var['package_price']}, package_currency: " \
                                         f"{trans_details_var['package_currency_name']}, trans_price: " \
                                         f"{trans_details_var['actual_transaction_amount']}, " \
                                         f"trans_currency: {trans_details_var['transaction_currency_name']}"
            general_ledger_entry_params = dict(zip(['entry_type_id', 'entry_description', 'transaction_value',
                                                    'reference_pg_transaction_id', 'added_by', 'last_modified_by'],
                                                   [1, gl_transaction_description,
                                                    trans_details_var['actual_transaction_amount'], input_json['ORDERID'],
                                                    trans_details_var['user_profile_id_id'], trans_details_var['user_profile_id_id']]))
            general_ledger_entry_vars = make_general_ledger_entry(general_ledger_entry_params)

            # if transaction status is not successful then return from here
            if transaction_status_var != 3:
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ["Success", "Transaction failed at Payment gateway level.",
                                        trans_details_var]))
                return output_json

            # Step 5: add a transaction to the respective self financial account
            # creating a description for the entry to record in financial account transaction
            fl_transaction_description = f"adding money to financial account. Amount: " \
                                         f"{trans_details_var['actual_transaction_amount']}. " \
                                         f"Currency: {trans_details_var['transaction_currency_name']}"
            fin_account_posting_params = dict(zip(['profile_id', 'general_ledger_entry_id', 'account_id',
                                                   'transaction_type', 'amount',
                                                   'currency_id', 'transaction_comments'],
                                                  [trans_details_var['user_profile_id_id'],
                                                   general_ledger_entry_vars['Payload']['ledger_entry_id'],
                                                   trans_details_var['associated_self_financial_accounts_id'],
                                                   1, trans_details_var['actual_transaction_amount'],
                                                   trans_details_var['actual_transaction_currency_id'],
                                                   fl_transaction_description]))
            financial_account_entry_var = AddAccountTransactionAPI.\
                add_account_transaction_json(request, fin_account_posting_params)

            # Step 7: add a transaction to respective wallet
            # creating a description for the entry to record in wallet transaction
            wl_transaction_description = f"adding {trans_details_var['no_of_credits']} credits to wallet."
            wallet_entry_params = dict(zip(['entry_details', 'wallet_id', 'general_ledger_entry_id',
                                            'transaction_type', 'no_of_points', 'expiry_status', 'expiry_date',
                                            'ref_wallet_ledger_entry_id', 'profile_id'],
                                           [wl_transaction_description, trans_details_var['wallet_id'],
                                            general_ledger_entry_vars['Payload']['ledger_entry_id'], 1,
                                            trans_details_var['no_of_credits'], None, None, None,
                                            trans_details_var['user_profile_id_id']]))
            wallet_entry_var = AddWalletTransactionAPI.add_wallet_transaction_json(request, wallet_entry_params)

            # Step 9: generate invoice and get invoice id
            invoice_entry_params = dict(zip(['profile_id', 'invoice_details', 'customer_details', 'items_details'],
                                            [trans_details_var['user_profile_id_id'], dict(), dict(), []]))
            invoice_entry_params['invoice_details'] = \
                dict(zip(['total_price_before_discounts', 'discount_percentage', 'discount_value',
                          'price_after_discount_before_tax', 'total_taxes', 'price_after_tax', 'currency',
                          'general_ledger_id', 'invoice_type'],
                         [trans_details_var['actual_transaction_amount'], 0, 0,
                          trans_details_var['actual_transaction_amount'],
                          trans_details_var['actual_transaction_amount'] * trans_details_var['tax_percentage']/100,
                          trans_details_var['actual_transaction_amount'] * (1 + trans_details_var['tax_percentage']/100),
                          trans_details_var['transaction_currency_name'],
                          general_ledger_entry_vars['Payload']['ledger_entry_id'], 2]))
            invoice_entry_params['customer_details'] = \
                dict(zip(['customer_name', 'customer_id'],
                         [trans_details_var['customer_name'], trans_details_var['user_profile_id_id']]))
            item_description_var = f"{trans_details_var['package_name']} package " \
                                   f"- {trans_details_var['no_of_credits']} wallet points for " \
                                   f"{trans_details_var['package_currency_name']} {trans_details_var['package_price']}"
            invoice_entry_params['items_details'].append(
                dict(zip(['item_id', 'item_name', 'item_description', 'quantity', 'currency', 'unit_price', 'total_amount'],
                         [trans_details_var['wallet_package_id_id'], trans_details_var['package_name'],
                          item_description_var, 1, trans_details_var['transaction_currency_name'],
                          trans_details_var['actual_transaction_amount'], trans_details_var['actual_transaction_amount']])))
            invoice_entry_var = CreateInvoiceAPI.create_invoice_json(request, invoice_entry_params)


            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Success", "Payment gateway output processed successfully", trans_details_var]))
            return output_json

        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Failure", f"Payment gateway output could not be processed. "
                                               f"Exception encountered: {ex}", None]))
            return output_json
