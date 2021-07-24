# url: http://localhost:8000/fetch_my_notifications/

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
            "session_key": "XrXmAjdoeXFzmCOFTMsSkzZr8uruuQyX"
        }
    },
    "Payload": {
        "Status": "Success",
        "Message": "Notification are fetched successfully",
        "Payload": {
            "notifications": [
                {
                    "individual_notification_id": 4,
                    "notification_status_id": 3,
                    "super_notification_id_id": 5,
                    "profile_id_id": 277,
                    "notification_text": null,
                    "redirection_url": "http://localhost:4200",
                    "comments": "important comment",
                    "notifier_profile_id_id": 279,
                    "added_date": "2020-09-19T12:26:51.883646Z",
                    "notified_profile_id_id": null,
                    "distribution_type_id_id": 3,
                    "type_id_id": 2,
                    "notifier_first_name": "Aryan",
                    "notifier_last_name": "Kumar",
                    "status_name": "Read",
                    "media_image_url": "https://akstagefe.com/assets/images/male-avatar.png"
                },
                {
                    "individual_notification_id": 3,
                    "notification_status_id": 3,
                    "super_notification_id_id": 3,
                    "profile_id_id": 277,
                    "notification_text": null,
                    "redirection_url": "http://localhost:4200",
                    "comments": "important comment",
                    "notifier_profile_id_id": 279,
                    "added_date": "2020-09-19T12:23:46.224433Z",
                    "notified_profile_id_id": 277,
                    "distribution_type_id_id": 1,
                    "type_id_id": 2,
                    "notifier_first_name": "Aryan",
                    "notifier_last_name": "Kumar",
                    "status_name": "Read",
                    "media_image_url": "https://akstagefe.com/assets/images/male-avatar.png"
                },
                {
                    "individual_notification_id": 2,
                    "notification_status_id": 2,
                    "super_notification_id_id": 2,
                    "profile_id_id": 277,
                    "notification_text": null,
                    "redirection_url": "/post/postLoginSupportCentre",
                    "comments": "important comment",
                    "notifier_profile_id_id": null,
                    "added_date": "2020-09-19T12:21:20.633937Z",
                    "notified_profile_id_id": null,
                    "distribution_type_id_id": 3,
                    "type_id_id": 1,
                    "notifier_first_name": null,
                    "notifier_last_name": null,
                    "status_name": "Seen",
                    "media_image_url": "../../../../assets/icons/app_logo.png"
                },
                {
                    "individual_notification_id": 1,
                    "notification_status_id": 3,
                    "super_notification_id_id": 1,
                    "profile_id_id": 277,
                    "notification_text": null,
                    "redirection_url": "http://localhost:4200",
                    "comments": "important comment",
                    "notifier_profile_id_id": null,
                    "added_date": "2020-09-19T12:18:27.065651Z",
                    "notified_profile_id_id": 277,
                    "distribution_type_id_id": 1,
                    "type_id_id": 1,
                    "notifier_first_name": null,
                    "notifier_last_name": null,
                    "status_name": "Read",
                    "media_image_url": "../../../../assets/icons/app_logo.png"
                }
            ]
        }
    }
}
"""
