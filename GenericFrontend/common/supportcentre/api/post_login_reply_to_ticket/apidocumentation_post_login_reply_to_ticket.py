# url: http://localhost:8000/post_login_reply_to_ticket/

# Sample Input:
"""
    {
      "APIDetails": {
        "token_type": 1,
        "token_vendor_id": 1,
        "token_string": "sdxfcgvbhjnmklasdfghjk",
        "dev_key": "sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"
      },
      "SessionDetails": {
        "profile_id": 277,
        "session_id": 1068,
        "session_key": "d3XOwq0nUCu04IOy1QSeFJOLIYlCKwMi"
      },
      "APIParams": {
        "ticket_id":36,
        "reply_body":"demo reply"
      }
}
"""

# Sample Output:
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
            "profile_id": 277,
            "session_id": 1068,
            "session_key": "Vj1MtUwFHiUcKxtUKMMUvE5mhHH3tKdF"
        }
    },
    "Payload": {
        "Status": "Success",
        "Message": "The given ticket is replied successfully",
        "Payload": {
            "reply_id": 86,
            "ticket_reply": "demo reply",
            "added_date": "2020-09-30T15:26:55.200579Z",
            "last_modified_date": "2020-09-30T15:26:55.200579Z",
            "ticket_id": 36,
            "added_by": 277,
            "last_modified_by": 277
        }
    }
}
"""
