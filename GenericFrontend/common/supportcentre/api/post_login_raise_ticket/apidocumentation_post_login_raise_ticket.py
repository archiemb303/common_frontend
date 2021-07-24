#API logic
"""
1. Check API authentication
2. Check Session Authentication
3. Check validations
4. Insert a record into postlogintickets table
        4.1 If ticket_question_id is 0 then insert null against the respective field names else, use the user's profile_id

"""

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
                "profile_id":186,
                "session_id":566,
                "session_key":"5vWiTkopRkJPcvg45ud3D3JE3E78jDRp"
            }
        "APIParams":
            {
                "ticket_type_id": 1,
                "ticket_question_id": 2,
                "subject": "I want to check this out",
                "query": "Wow, you guys are so awesome"
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
    "Payload": {
        "Status": "Success",
        "Message": "Congratulations, you areregistered successfully with genericfrontend",
        "Payload": {
            [
                {
                    ticket_type_id:1, 
                    ticket_type_text:"How to use", 
                    common_questions: 
                    [
                        {question_id: 1, question_text:"How to I sign in"},
                        {question_id: 2, question_text:"How to I sign out"}
                    ]
                },
                {
                    ticket_type_id:1, 
                    ticket_type_text:"Profile related", 
                    common_questions: 
                    [
                        {question_id: 4, question_text:"How do I update my name"},
                        {question_id: 5, question_text:"How to I update my email"}
                    ]
                }
            ]

        }
    }
}
"""
