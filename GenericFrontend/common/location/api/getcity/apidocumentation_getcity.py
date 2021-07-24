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
            "city_id": 1
        }
}
########################     Sample Output  ################################
{
    "Payload": {
        "Status": "Success",
        "Message": "Successfully retrieved city.",
        "States": {
            "city_id": 1,
            "city_name": "bangalore",
            "added_by": "vandana",
            "added_date": "2020-04-26T18:30:00Z",
            "last_modified_by": "vandana",
            "last_modified_date": "2020-04-26T18:30:00Z",
            "state_id": {
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
}
# #######################    Algorithm  ############################    
Alogorithm

         Step 1.Check for API authentication
         Step 2.Validate city_id parameter
         Step 3.Retreive city object from WdCities table and perform join on WdStates
          and WdCountries.If error, report->Join operation error message
         Step 4.Serialize city object from step 3
         Step 5.Return Serialized city object along with State and Country objects.End

"""