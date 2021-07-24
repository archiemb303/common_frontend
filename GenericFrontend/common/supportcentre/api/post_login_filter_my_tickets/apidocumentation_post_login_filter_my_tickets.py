# url: http://localhost:8000/post_login_filter_my_tickets/

# Sample Input:

"""
    {
        "APIDetails":
            {
                "token_type":1,
                "token_vendor_id":1,
                "token_string":"sdxfcgvbhjnmklasdfghjk",
                "dev_key":"sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"
            },
        "SessionDetails":
            {
                "profile_id":277,
                "session_id":3040,
                "session_key":"5vWiTkopRkJPcvg45ud3D3JE3E78jDRp"
            }
        "APIParams":
            {
                    "search_query":"media query"
            }
    }
"""

# Sample Output:
"""
{
    "AvailabilityDetails": {
        "Status": "Success",
        "Message": "Website Availability status fetched successfully",
        "Payload": {
            "live_flag": 1,
            "state_flag": 1
        }
    },
    "AuthenticationDetails": {
        "Status": "Success",
        "Message": "ApiDetails fine to process"
    },
    "SessionDetails": {
        "Status": "Success",
        "Message": "session is active. session details updated",
        "Payload": {
            "profile_id": 277,
            "session_id": 3440,
            "session_key": "5DRZDrKrwdQhzoBUepanfn3K36ZcIHDQ"
        }
    },
    "Payload": {
        "Status": "Success",
        "Message": "users tickets fetched successfully",
        "Payload": {
            "tickets_list": [
                {
                    "ticket_id": 41,
                    "ticket_subject": "media query demo",
                    "ticket_query": "media query demo query",
                    "ticket_status_id": 3,
                    "ticket_type_id": 3,
                    "ticket_question_id": 7,
                    "ticket_owner_name": "Aryan Kumar",
                    "added_date": "2020-09-10T16:20:16.152287Z",
                    "last_modified_date": "2020-09-10T16:20:16.152287Z",
                    "status_name": "Open-Answered",
                    "type_name": "Media related",
                    "common_question_text": "question text is31",
                    "last_action_date": "2020-10-29T20:53:50.636860Z",
                    "ticket_replies": [
                        {
                            "reply_id": 99,
                            "ticket_reply": "tested reply field",
                            "reply_date": "2020-10-29T19:42:34.597944Z",
                            "replied_by": "User"
                        },
                        {
                            "reply_id": 100,
                            "ticket_reply": "reply field is working",
                            "reply_date": "2020-10-29T19:44:24.489474Z",
                            "replied_by": "User"
                        },
                        {
                            "reply_id": 101,
                            "ticket_reply": "yaa reply field is working",
                            "reply_date": "2020-10-29T20:53:50.636860Z",
                            "replied_by": "Staff"
                        }
                    ]
                }
            ]
        }
    }
}
"""
