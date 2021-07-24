"""
#################     Sample API Body       ######################
{  "APIDetails":{
                  "dev_key":"sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234",
                  "token_type":1,
                  "token_vendor_id":1,
                  "token_string":"dguegkhdfjkghdljkfghdjfhvkjdnvj"},
 },

    "APIParams" :{
        "state_name": "LA",
        "added_by": "sxzusdnil",
        "last_modified_by": "ssausansail",
        "country_id":2
        }
 }
########################    Input   ################################
        "state_name": "LA",
        "added_by": "sxzusdnil",
        "last_modified_by": "ssausansail",
        "country_id":2
########################   Sample Output  ################################
"AuthenticationPayload": {
        "Status": "Success",
        "Message": "API call is authentic"
    },

    "Payload": {
        "Status": "Success",
        "Message": "State data  was  successfully added to Database"
    }
}
# #######################    Algorithm  ############################
Algorithm
    1.Excute Validations for APIParams
    2.Serialize the Data
    3.Add the data into WdStates table
    4.End
    """