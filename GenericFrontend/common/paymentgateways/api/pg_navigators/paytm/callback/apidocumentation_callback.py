# API Logic:
"""
This API reads the response from the payment gateway and then does appropriate processes
Step 1: For returned order_id update response object in paymentgatewaytransactions table
Step 2: For this order_id find the session id, profile_id of the user, and associated_bank_account_id by
 calling function named get_all_details_for_transaction_id
Step 3: make an entry in general ledger table even if the transaction is failed.
Step 4: check if transaction status is failed. If success then goto step 5 else goto step return
Step 5: make an entry in the respective financial_account ledger
Step 6: update balance in the respective financial account. Achieve step 5 and 6 by calling AddAccountTransactionAPI
Step 7: make an entry in userwalletsledger table
Step 8: update balance in userwallet where wallet type is cash. Achieve step 5 and 6 by calling AddWalletTransactionAPI
Step 9: insert record into invoices table. Achieve step 5 and 6 by calling AddInvoiceAPI
Step 10: return output with new wallet balance in the message
"""

# API input:
"""
{
	'ORDERID': ['86d9d1fb-729f-48ce-8f09-08648e2338e1'], 
	'MID': ['MNsMBb00175452515101'], 
	'TXNID': ['20200910111212800110168265901887654'], 
	'TXNAMOUNT': ['8.99'], 
	'PAYMENTMODE': ['CC'], 
	'CURRENCY': ['INR'], 
	'TXNDATE': ['2020-09-10 14:43:29.0'], 
	'STATUS': ['TXN_SUCCESS'], 
	'RESPCODE': ['01'], 
	'RESPMSG': ['Txn Success'], 
	'GATEWAYNAME': ['HDFC'], 
	'BANKTXNID': ['777001816915511'], 
	'BANKNAME': ['ICICI Bank'], 
	'CHECKSUMHASH': ['vMH5E1XQUHn+6C/yGJHrUra5MDgpBqQKaFU3iCsMLhRQvceKIJkU6yzd8NvhSnqgKZzj1/E3Wix3pls8IauOe4BxezQ44cK8Y9mtKtNxdXY=']
}

"""