"""################     Sample API Body       ######################
{  "APIDetails":{
                  "DevKey":"sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234",
                  "token_type":1,
                  "token_vendor_id":1,
                  "token_string":"dguegkhdfjkghdljkfghdjfhvkjdnvj"},
 },

    "APIParams" :{
               "city_name": "Silicon_Valley",
               "added_by": "sewweunediwedwel",
               "last_modified_by": "sunwwdiedwewl",
               "state_id":2
               }
}
#######################    Input   ################################
               "city_name": "Silicon_Valley",
               "added_by": "sewweunediwedwel",
               "last_modified_by": "sunwwdiedwewl",
               "state_id":2

#######################  Sample Output  ################################
    "AuthenticationPayload": {
        "Status": "Success",
        "Message": "API call is authentic"
    },

    "Payload": {
        "Status": "Success",
        "Message": "City data  was  successfully added to Database  "
    }
}

#######################    Algorithm  ############################
Alogorithm
   1.Excute Validations  for APIParams
   2.Serialize the Data
   3.Add the Serialized data into WdCities Table
   4.End
   """
