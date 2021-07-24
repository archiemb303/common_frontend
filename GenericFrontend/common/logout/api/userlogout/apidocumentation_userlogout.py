# Sample Input:

# {
#     "APIDetails":
#         {
#
#             "token_type":1,
#             "token_vendor_id":1,
#             "token_string":"sdxfcgvbhjnmklasdfghjk",
#             "dev_key":"sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"
#         },
#     "SessionDetails": {
#         "profile_id": 141,
#         "session_id": 165,
#         "session_key": "l11MfqAD3oD9wQDpbFJNt5wtLfkOZhFd"
#
#     },
#     "APIParams":
#         {
#             "logout_type":"current_session"
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
#         "Message": "User has been logged out from current_session",
#         "Payload": null
#     }
# }
# Sample Failed Output
# {
#     "AuthenticationDetails": {
#         "Status": "Success",
#         "Message": "ApiDetails fine to process"
#     },
#     "SessionDetails": {
#         "Status": "Failure",
#         "Message": "Looks like the user is already logged out."
#     }
# }

######## ALGORITHM #######
# Step 1 : API Authentiucation is done and sessions are created for the current user.
# Step 2 : Validations are done for the current inputs
# Step 3 : If input is 'current users' then go to Step 4, else goto Step 5
# Step 4 : if profile ID of the current session matech the profile ID of the fected session, update status to 2, else goto 6
# Step 5 : If the profile ID of any session ID matches the profile ID of the inputed sessions, update all the status to 2, else goto step 6
# Step 6 : Throw an error message
# Step 7 : Return the final output as the Response.
