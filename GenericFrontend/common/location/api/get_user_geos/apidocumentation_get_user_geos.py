"""
This is a post login API and hence would have APIDetails and SessionDetails in the request object
-------------------------------------------------------------------------------------------------
Step 1: find if user's ip address is provided in the request object, if yes then got to step 2 else goto step 4
Step 2: call third party api to find the country of the IP address and its ISO2 and ISO3 codes
Step 3: using the ISO2 and/or ISO3 codes get the user's geo and associated currency. Return output
Step 4: from UserProfiles table get city_id and using this get the user's geo and associated currency. Return output
"""

"""
INPUT:
{
        "APIDetails":{
            	"token_type":1,
            	"token_vendor_id":1,
            	"token_string":"sdxfcgvbhjnmklasdfghjk",
            	"dev_key":"sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"
            },
        "SessionDetails":{
            "profile_id":159,
            "session_id":787,
            "session_key":"xxbJt0nUwyMbsDdOfVFYISRjoD1DC0jO"
        },
        "APIParams":{
            "user_ip" : "192.168.0.1"
        }
}
"""

"""
OUTPUT:
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
            "session_id": 787,
            "session_key": "LcTyf2Ypx6YRQOz3AYOyaE2uedblWnZB"
        }
    },
    "Payload": {
        "Status": "Success",
        "Message": "ticket types and respective questions Fetched successfully",
        "Payload": {
            "geo_id": 2,
            "geo_name": "Indian Subcontinent",
            "geo_currency": "INR"
        }
    }
}
"""