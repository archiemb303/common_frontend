"""
#----------------------------------------------- APIinput ---------------------------------
{
        "APIDetails":{
                        "token_type":1,
                        "token_vendor_id":1,
                        "token_string":"sdxfcgvbhjnmklasdfghjk",
                        "dev_key":"sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"
                        },
              "APIParams":{}
}
 #------------------------------------------------ API OUTPUT ----------------------------------
 {
    "Payload": {
        "Status": "Success",
        "Message": "Successfully retrieved countries.",
        "countries": [
            {
                "country_id": 1,
                "country_name": "india",
                "added_by": "vandana",
                "added_date": "2020-04-26T18:30:00Z",
                "last_modified_by": "vandana",
                "last_modified_date": "2020-04-26T18:30:00Z"
            },
            {
                "country_id": 2,
                "country_name": "nepal",
                "added_by": "dev",
                "added_date": "2020-04-27T20:18:30.968084Z",
                "last_modified_by": "dev",
                "last_modified_date": "2020-04-27T20:18:30.968084Z"
            }
        ]
    }
}

# ####################### Algorithm  ############################
Alogorithm

         Step 1.Check for API authentication
         Step 2.Retreive all countries object from WdCountries table.If error,
         report->Internal DB error message
         Step 3.Serialize countries object from step 2
         Step 4.Return Serialized countries object
"""