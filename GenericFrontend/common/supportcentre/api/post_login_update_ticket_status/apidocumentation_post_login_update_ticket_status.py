# url: http://localhost:8000/post_login_update_ticket_status/

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
                    "ticket_id":24,
                    "current_ticket_status":1,
                    "closing_flag":0,                                       # 0/1
                    "user_type":"staff"                                     # "staff"/"ticket-owner"
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
            "profile_id": 279,
            "session_id": 1080,
            "session_key": "Ut9VyENyX1jZMpyKZ5LXYsqH7KB9GpNH"
        }
    },
    "Payload": {
        "Status": "Success",
        "Message": "The ticket status is updated successfully",
        "Payload": {
            "ticket_id": 24,
            "ticket_type_id": 4,
            "ticket_question_id": 12,
            "ticket_subject": "Demo Ticket Subject",
            "ticket_query": "Demo Ticket Query",
            "ticket_owner_id": 159,
            "ticket_status_id": 3,
            "added_date": "2020-09-04T11:11:43.589885Z",
            "added_by_id": 159,
            "last_modified_date": "2020-09-04T11:11:43.589885Z",
            "last_modified_by_id": 159
        }
    }
}
"""
