# API Logic
"""
Every payment gateway would collect payments in their own as well as respective bank pages (for security reasons).
Once the transaction is passed (successfully or unsuccessfully) the user has to return to our website.
During this return process, we have to capture the payment gateway transaction output and do all
appropriate calculations and updates in our database, before showing the user the respective output page.
Since each payment gateway takes in an returns data in different formats, we need to have dedicated functions for
each payment gateway provider. As a result, the user navigates through a dedicated route of pages.
Hence this function helps us decide the necessary naigation.

Step 1: check for API and Session authentication (Since we are not creating any API for this at the moment,
we will just have the _json function, and hence will not create any validation functions for this)
Step 2: get pg provider from input_json
Step 3: based on pg_provider_id call the respective get_pg_navigators function
"""

# API Input:
"""
{
    
    "payment_gateway_details": {
        "pg_id": 1,
        "pg_name": "PayTM",
        "pg_cred": {
                    "PAYTM_WEBSITE": "WEBSTAGING",
                    "PAYTM_CHANNEL_ID": "WEB",
                    "PAYTM_SECRET_KEY": "1e6ohbxKcalNi1Lq",
                    "PAYTM_MERCHANT_ID": "MNsMBb00175452515101",
                    "PAYTM_INDUSTRY_TYPE_ID": "Retail"
                    },
        "added_date": "2020-09-07T00:00:00Z",
        "added_by": "186",
        "last_modified_date": "2020-09-07T00:00:00Z",
        "last_modified_by": "186",
        "associated_self_financial_accounts_id": 1,
        "pg_status_id": 1,
        "pg_provider_id": 4
    },
    "user_id": 159,
    "transaction_details": {
            "pg_transaction_id": "f9e4fb58-c63a-4785-8ac9-6f3f9d69ebfa",
            "transaction_date": "2020-09-09T12:21:37.021070Z",
            "amount": 664.47,
            "request_object": null,
            "response_object": null,
            "pg_id": 1,
            "currency": 2,
            "customer_country_id": 14,
            "transaction_status": 1
    }
}

"""