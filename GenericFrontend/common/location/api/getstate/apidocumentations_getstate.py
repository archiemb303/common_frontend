""""#################     Sample API Body       ######################
{
    "APIDetails": {
        "token_type": 1,
        "token_vendor_id": 1,
        "token_string": "sdxfcgvbhjnmklasdfghjk",
        "dev_key": "sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"
    },
    "APIParams":
        {

            "state_id": 1
        }
}
#   
#           *   state_id
#
#
########################   Sample Output  ################################
{
    "Payload": {
        "Status": "Success",
        "Message": "Successfully retrieved State.",
        "States": {
            "state_id": 1,
            "state_name": "karnataka",
            "added_by": "vandana",
            "added_date": "2020-04-26T18:30:00Z",
            "last_modified_by": "vandana",
            "last_modified_date": "2020-04-26T18:30:00Z",
            "country_id": {
                "country_id": 1,
                "country_name": "india",
                "added_by": "vandana",
                "added_date": "2020-04-26T18:30:00Z",
                "last_modified_by": "vandana",
                "last_modified_date": "2020-04-26T18:30:00Z"
            }
        }
    }
}
# 
# #######################    Algorithm  ############################    
#Alogorithm
#          
#          Step 1.Check for API authentication
#          Step 2.Validate state_id parameter
#          Step 3.Retreive state object from WdStates table and perform join on WdCountry
table,,if error report->Join operation error message
#          Step 4.Serialize state object from step 3              
#          Step 5.Return Serialized state object with countries
information,if error report ->Internal Database error.End
"""
