# API Logic
"""
This API will receive all commercial details price and currency and payment gateway_id
get user's country_id from ip
if payment gateway id = 1, ie. paytm payment receiving page then it will do the following operations
as PayTM takes payments only in INR
    If currency is INR then it will set conversion rate as 1
    If currency is in AED then it will set conversion rate as 21
    If currency is anything else then it will call api https://api.exchangeratesapi.io/latest and calculate the latest conversion rate for INR
    Calculate price in INR as price*conversion rate
insert a new record into the table
"""

# API Input:
"""
{
    "APIDetails": {
        "token_type": 1,
        "token_vendor_id": 1,
        "token_string": "sdxfcgvbhjnmklasdfghjk",
        "dev_key": "sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"
    },
    "SessionDetails": {
        "profile_id": 159,
        "session_id": 944,
        "session_key": "mOMNfNtQzzBbNTwG6m10EAUD26er31cv"
    },

    "APIParams": {
        "amount": 2,
        "currency": "INR",
        "payment_gateway_id": 1
    }

}
"""