# url: http://localhost:8000/check_if_staff/

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
            "session_key": "Lmoem5qNVw5oO6TPl2t4sNHlFkXoZysD"
        }
    },
    "Payload": {
        "Status": "Success",
        "Message": "User is a staff",
        "Payload": {
            "staff_id": 3,
            "staff_registration_date": "2020-09-07T00:00:00Z",
            "staff_removal_date": "2025-09-07T00:00:00Z",
            "added_date": "2020-09-07T00:00:00Z",
            "last_modified_date": "2020-09-07T00:00:00Z",
            "added_by_id": 277,
            "last_modified_by_id": 277,
            "staff_profile_id_id": 277,
            "staff_status_id": 1
        }
    }
}
"""
