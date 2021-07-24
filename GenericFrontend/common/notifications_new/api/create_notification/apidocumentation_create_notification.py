# url: http://localhost:8000/create_notification/

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
           "notification_text":["Your ticket was replied by the team."],
            "type_id":1,
            "distribution_type_id": 1,
            "notifier_profile_id": 277,
            "notified_profile_id":279,
            "algorithm_id":null,
            "redirection_url":"/post/postloginViewTicketReplies/36",
            "comments":"Support centre staff has replied to a ticket"
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
            "session_key": "rxddihuhoZdei7a90Yj3MKVVbFrUlmK8"
        }
    },
    "Payload": {
        "Status": "Success",
        "Message": "Notification is created successfully",
        "Payload": {
            "notification_id": 18,
            "notification_text": [
                "Your ticket was replied by the team."
            ],
            "redirection_url": "/post/postloginViewTicketReplies/36",
            "comments": "Support centre staff has replied to a ticket",
            "added_date": "2020-09-30T15:13:52.541754Z",
            "last_modified_date": "2020-09-30T15:13:52.541754Z",
            "type_id": 1,
            "distribution_type_id": 1,
            "notification_status": 1,
            "notifier_profile_id": 277,
            "notified_profile_id": 279,
            "algorithm_id": null,
            "added_by": 277,
            "last_modified_by": 277
        }
    }
}
"""
