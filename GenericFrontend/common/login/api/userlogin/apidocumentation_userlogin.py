# Sample Input:

# {
#     "APIDetails":{
#         "token_type":1,
#         "token_vendor_id":1,
#         "token_string":"sdxfcgvbhjnmklasdfghjk",
#         "dev_key":"sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"
#     },
#
#     "APIParams":{
#         "email_id":"raj111@mailinator.com",
#         "password":"Sac$2045",
#         "login_type":"Native",
#         "device":"laptop",
#         "guid":1,
#         "source_id":1
#
#
#     }
# }
# Sample Output:

# {
#     "AuthenticationDetails": {
#         "Status": "Success",
#         "Message": "ApiDetails fine to process"
#     },
#     "SessionDetails": {
#         "profile_id": 145,
#         "session_id": 167,
#         "session_key": "VJgz0SYcmCPWFRNahureL6KDW7bMZ7pO",
#         "Status": "Success",
#         "Message": "new session created successfully"
#     },
#     "Payload": {
#         "Status": "Success",
#         "Message": "User successfully logged in, Profile Details Updated Successfully.",
#         "Payload": {
#             "email_id": "raj111@mailinator.com",
#             "login_count": 1,
#             "activation_status": 1
#         }
#     }
# }
#Failed Response:
# {
#     "AuthenticationDetails": {
#         "Status": "Success",
#         "Message": "ApiDetails fine to process"
#     },
#     "Payload": {
#         "Status": "Failure",
#         "Message": "No user registered with provided email address",
#         "Payload": null
#     }
# }