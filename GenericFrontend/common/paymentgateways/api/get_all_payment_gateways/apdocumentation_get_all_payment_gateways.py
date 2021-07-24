# API Logic:
"""
This API does not need any additional parameters in APIParams section
Step 1: get all payment gateways from PaymentGateways table where status = active

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
        "session_key": "ncteAuLloVDM9FhA2ELRu8PV5nfxHOXb"
    }
}
"""

# API output
"""
{
    "AuthenticationDetails": {
        "Status": "Success",
        "Message": "ApiDetails fine to process"
    },
    "SessionDetails": {
        "Status": "Success",
        "Message": "session is active. session details updated",
        "Payload": {
            "profile_id": 159,
            "session_id": 944,
            "session_key": "qoVfuvs5n9irrJNmipZzOAbhMDmOf5fV"
        }
    },
    "Payload": {
        "Status": "Success",
        "Message": "Wallet current package formatted successfully.",
        "Payload":{
            pg_list:[
                    {'pg_id': 1, 'pg_name':"PayTM"},
                    {'pg_id': 2, 'pg_name':"CCAvenue"}
                ]
            }
        }
}
"""
