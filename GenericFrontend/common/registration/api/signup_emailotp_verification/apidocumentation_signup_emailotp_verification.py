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
#         "email_id":"raj378@mailinator.com",
#         "otp":681606
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
#         "Status": "Success",
#         "Message": "Session created successfully",
#         "Payload": {
#             "profile_id": 242,
#             "session_id": 304,
#             "session_key": "EebH2qky7Pn10Kc5xWMecx1pjqDkxAbM"
#         }
#     },
#     "Payload": {
#         "Profile_id": 242,
#         "profile_completion_status": 2
#     }
# }

# Sample Failed Output
# {
#     "AuthenticationDetails": {
#         "Status": "Success",
#         "Message": "ApiDetails fine to process"
#     },
#     "Payload": {
#         "Status": "Failure",
#         "Message": "otp doesn't match, Please re-enter otp",
#         "Payload": null
#     }
# }
