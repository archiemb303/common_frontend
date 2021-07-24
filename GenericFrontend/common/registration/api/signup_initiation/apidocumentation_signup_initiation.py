# Sample Input:

# {
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
#             "source_uuid":1,
#             "source_id":1,
#             "invite_flag":0,
#             "requester_fname":"raj",
#             "requester_lname":"raj"
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
#         "Message": "Thank you for registering! Please check your inbox  and verify your email address",
#         "Payload": null
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
#         "Message": "Activation key could not be updated: structure of query does not match function result type\nDETAIL:  Returned type timestamp with time zone does not match expected type character varying in column 5.\nCONTEXT:  PL/pgSQL function update_row(character varying,character varying,integer) line 3 at RETURN QUERY\n",
#         "Payload": null
#     }
# }