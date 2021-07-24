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
#         "phone_number":9972695796,
#         "country_code" : 91,
#         "otp": 785437
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
#             "profile_id": 244,
#             "session_id": 309,
#             "session_key": "g25KVLx7KPS34auLk0t3eAjO7MxtiUIB"
#         }
#     },
#     "Payload": {
#         "Status": "Success",
#         "Message": "Otp verified successfully",
#         "Payload": {
#             "profile_completion_status": 2
#         }
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
