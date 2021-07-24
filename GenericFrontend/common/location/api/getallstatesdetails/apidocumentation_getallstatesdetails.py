"""
#################     Sample API Body       ######################
{
    "APIDetails": {
        "token_type": 1,
        "token_vendor_id": 1,
        "token_string": "sdxfcgvbhjnmklasdfghjk",
        "dev_key": "sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"
    },
    "APIParams":
        {
        }
}
########################    Output  ################################
{
    "Payload": {
        "Status": "Success",
        "Message": "Successfully retrieved States.",
        "States": [
            {
                "state_id": 1,
                "state_name": "karnataka",
                "added_by": "vandana",
                "added_date": "2020-04-26T18:30:00Z",
                "last_modified_by": "vandana",
                "last_modified_date": "2020-04-26T18:30:00Z",
                "country_id": 1
            },
            {
                "state_id": 2,
                "state_name": "karnataka",
                "added_by": "dev",
                "added_date": "2020-04-28T02:07:24.861028Z",
                "last_modified_by": "dev",
                "last_modified_date": "2020-04-28T02:07:24.861028Z",
                "country_id": 1
            },
            {
                "state_id": 3,
                "state_name": "karnataka",
                "added_by": "dev",
                "added_date": "2020-04-28T02:09:23.505593Z",
                "last_modified_by": "dev",
                "last_modified_date": "2020-04-28T02:09:23.505593Z",
                "country_id": 1
            }
        ]
    }
}
# ####################### Algorithm  ############################
Alogorithm

         Step 1.Check for API authentication
         Step 2.Retreive all States object from WdStates table
         Step 3.Serialize States object from step 2.If error, report->Internal DB error message
         Step 4.Return Serialized States object
"""