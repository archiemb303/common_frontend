# Sample Input:

# {
#     "APIDetails":{
#         "token_type":1,
#         "token_vendor_id":1,
#         "token_string":"sdxfcgvbhjnmklasdfghjk",
#         "dev_key":"sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"
#     },
#     "APIParams": {
#         "first_name":"raj",
#         "last_name":"raj",
#         "email_id":"raj111@mailinator.com",
#         "activation_key": "d36Ej82HhRWjqIUi9baKOm4MA3gy0KLb",
#         "password": "Sac$2045",
#         "sex": "male",
#         "date_of_birth": "1985-07-04",
#         "orientation": "straight",
#         "city_id":1
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
#     "Payload": {
#         "Status": "Success",
#         "Message": "Congratulations, you areregistered successfully with genericfrontend",
#         "Payload": {
#             "profile_id": 145,
#             "first_name": "raj",
#             "last_name": "raj",
#             "sex": "male",
#             "date_of_birth": "1985-07-04",
#             "orientation": "straight",
#             "web_profile_key": "6DX5SFX9mFpkRBpkSBAPPux3C4UmF2rp",
#             "android_app_profile_key": "6DX5SFX9mFpkRBpkSBAPPux3C4UmF2rp",
#             "ios_app_profile_key": "6DX5SFX9mFpkRBpkSBAPPux3C4UmF2rp",
#             "global_profile_key": "6DX5SFX9mFpkRBpkSBAPPux3C4UmF2rp",
#             "added_date": "2020-05-30T19:09:42.607003Z",
#             "added_by": "EV_raj111@mailinator.com",
#             "last_modified_date": "2020-05-30T19:09:42.607003Z",
#             "last_modified_by": "EV_raj111@mailinator.com",
#             "city_id_id": 1,
#             "dp_flag_id": 1,
#             "profile_status_id": 1,
#             "profile_completion_status_id": 1
#         }
#     }
# }

#Sample Failed Output:
# {
#     "AuthenticationDetails": {
#         "Status": "Success",
#         "Message": "ApiDetails fine to process"
#     },
#     "Payload": {
#         "Status": "Failure",
#         "Message": "invalid activation key",
#         "Payload": null
#     }
# }
