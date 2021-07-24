# Sample Input:

# {
#
#     "APIDetails":{
#         "token_type":1,
#         "token_vendor_id":1,
#         "token_string":"sdxfcgvbhjnmklasdfghjk",
#         "dev_key":"sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"
#     },
#     "APIParams":
#         {
#             "first_name":"raj",
#             "last_name":"raj",
#             "email_id":"raj111@mailinator.com",
#             "activation_key": "d36Ej82HhRWjqIUi9baKOm4MA3gy0KLb"
#
#         }
# }

# Sample Output:

# {
#     "AuthenticationDetails": {
#         "Status": "Success",
#         "Message": "ApiDetails fine to process"
#     },
#     "Payload": {
#         "Status": "Success",
#         "Message": "Allow registration step 2",
#         "Payload": null
#     }
# }

#Sample Failed Output
# {
#     "AuthenticationDetails": {
#         "Status": "Success",
#         "Message": "ApiDetails fine to process"
#     },
#     "Payload": {
#         "Status": "Failure",
#         "Message": "Activation key is not valid",
#         "Payload": null
#     }
# }