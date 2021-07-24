"""
################     Sample API Body       ######################
{  "APIDetails":{
                  "DevKey":"sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234",
                  "token_type":1,
                  "token_vendor_id":1,
                  "token_string":"dguegkhdfjkghdljkfghdjfhvkjdnvj"},
 },
    "APIParams" :{
        "country_name": "India",
        "added_by": "vandana",
        "last_modified_by": "vandana",
          "phone_code":91,
        "country_abbreviation":"aszexdcfvgbh",
         "country_code_iso3" :"mmm" ,
         "country_code_iso2" :" bnn",
         "currency":"nnn"
    }
########################   Sample Output  ################################
{"AuthenticationPayload": {
        "Status": "Success",
        "Message": "API call is authentic"
    },

    "Payload": {
        "Status": "Success",
        "Message": "Country data  was  successfully added to Database "
    }
}

#######################    Algorithm  ############################
Algorithm
    # 1.Excute Validations for APIParams
    # 2.Serialize the Data
    # 3.Add the data into WdCountries table
    # 4.End
    """
