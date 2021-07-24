# url: http://localhost:8000/update_notification_status/

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
             "individual_notification_id":1,
             "notification_status":3
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
            "session_key": "cpXslKAxCyaLI4pJKm7zwQEalVu0V1Cj"
        }
    },
    "Payload": {
        "Status": "Success",
        "Message": "Notification are updated successfully",
        "Payload": {
            "individual_notification_id": 1,
            "super_notification_id_id": 1,
            "notification_status_id": 3,
            "profile_id_id": 277,
            "added_date": "2020-09-19T15:57:12.156137Z",
            "added_by_id": 277,
            "last_modified_date": "2020-09-19T15:57:12.156137Z",
            "last_modified_by_id": 277
        }
    }
}
"""
