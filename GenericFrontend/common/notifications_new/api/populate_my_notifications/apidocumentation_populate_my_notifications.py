# url: http://localhost:8000/populate_my_notifications/

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
            "session_key": "KHjzxcpS9dzfTaNieqlPd5DM0PGudYgM"
        }
    },
    "Payload": {
        "Status": "Success",
        "Message": "Notifications are populated successfully",
        "Payload": {}
    }
}
"""
