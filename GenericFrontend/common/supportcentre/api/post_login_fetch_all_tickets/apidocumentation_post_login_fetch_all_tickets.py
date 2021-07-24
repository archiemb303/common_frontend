# url: http://localhost:8000/post_login_fetch_all_tickets/

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
        "session_key": "DKrSogXOIDAoo4ZQlxFAeVMQtt11CTyV"
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
            "session_key": "9TpgORCU09QEuWsgbMxefdtBcuJIcet1"
        }
    },
    "Payload": {
        "Status": "Success",
        "Message": "users tickets fetched successfully",
        "Payload": {
            "tickets_list": [
                {
                    "ticket_id": 1,
                    "ticket_subject": "Test Subject",
                    "ticket_query": "Just testing the waters",
                    "ticket_status_id": 1,
                    "ticket_type_id": 1,
                    "ticket_question_id": 2,
                    "added_date": "2020-08-14T15:30:17.826072Z",
                    "last_modified_date": "2020-08-14T15:30:17.826072Z",
                    "status_name": "Fresh",
                    "type_name": "How to use",
                    "common_question_text": "question text is12",
                    "last_action_date": "2020-08-14T15:30:17.826072Z",
                    "ticket_replies": []
                },
                {
                    "ticket_id": 3,
                    "ticket_subject": "Token of appreciation",
                    "ticket_query": "You are really awesome",
                    "ticket_status_id": 1,
                    "ticket_type_id": 1,
                    "ticket_question_id": 2,
                    "added_date": "2020-08-14T15:36:35.280917Z",
                    "last_modified_date": "2020-08-14T15:36:35.281914Z",
                    "status_name": "Fresh",
                    "type_name": "How to use",
                    "common_question_text": "question text is12",
                    "last_action_date": "2020-08-14T15:36:35.280917Z",
                    "ticket_replies": []
                },
                {
                    "ticket_id": 18,
                    "ticket_subject": "Some Text subject",
                    "ticket_query": "Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body Some text body",
                    "ticket_status_id": 1,
                    "ticket_type_id": 3,
                    "ticket_question_id": 9,
                    "added_date": "2020-09-01T15:31:56.309205Z",
                    "last_modified_date": "2020-09-01T15:31:56.309228Z",
                    "status_name": "Fresh",
                    "type_name": "Media related",
                    "common_question_text": "question text is33",
                    "last_action_date": "2020-09-02T17:57:50.199361Z",
                    "ticket_replies": [
                        {
                            "reply_id": 4,
                            "ticket_reply": "reply 18-3",
                            "reply_date": "2020-09-02T15:57:50.199361Z",
                            "replied_by": "User"
                        },
                        {
                            "reply_id": 5,
                            "ticket_reply": "reply 18-4",
                            "reply_date": "2020-09-02T16:57:50.199361Z",
                            "replied_by": "User"
                        },
                        {
                            "reply_id": 6,
                            "ticket_reply": "reply 18-5",
                            "reply_date": "2020-09-02T17:57:50.199361Z",
                            "replied_by": "Staff"
                        }
                    ]
                },
                {
                    "ticket_id": 36,
                    "ticket_subject": "demo query 1",
                    "ticket_query": "demo query body",
                    "ticket_status_id": 3,
                    "ticket_type_id": 1,
                    "ticket_question_id": 1,
                    "added_date": "2020-09-07T12:17:25.389623Z",
                    "last_modified_date": "2020-09-07T12:17:25.389646Z",
                    "status_name": "Open-Answered",
                    "type_name": "How to use",
                    "common_question_text": "question text is11",
                    "last_action_date": "2020-09-30T15:26:55.200579Z",
                    "ticket_replies": [
                        {
                            "reply_id": 84,
                            "ticket_reply": "try again",
                            "reply_date": "2020-09-30T14:53:37.188465Z",
                            "replied_by": "Staff"
                        },
                        {
                            "reply_id": 85,
                            "ticket_reply": "try agian",
                            "reply_date": "2020-09-30T14:58:56.124175Z",
                            "replied_by": "Staff"
                        },
                        {
                            "reply_id": 86,
                            "ticket_reply": "demo reply",
                            "reply_date": "2020-09-30T15:26:55.200579Z",
                            "replied_by": "Staff"
                        }
                    ]
                }
            ]
        }
    }
}
"""
