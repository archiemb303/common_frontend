# Step 1: In your app create a file name views_populate_master_tables at the same level where models.py resides
# Step 2: create a function named populate_<<app_name>>_master_tables 
# and import populate_master_data from common.utilities.populate_all_master_tables.populate_master_tables_lib
#    Eg: if your app name is myapp, then this function name should be populate_myapp_master_tables

# Step 3: for every master table in the app create a function named populate_<<master_table_name>>
#    Eg: if you have defined two master tables named sample_master_table_one and sample_master_table_two
#    then create two functions named populate_sample_master_table_one and populate_sample_master_table_two

# Step 4: copy paste the below body into each of the tables as defined in step 3 and follow the comments in the code
#    """
#    This function populates the master table named TimelineSampleStatus in the app named timeline
#    :return:
#    """
#    try:
#       # defining all the master table rows. This is the final data that should be there in the master table.
#        # Hence write all information that you want to populate including the ones that are existing.
#        # Remember to use the exact field names in this definition as it is defined in the respective model definitions.
#        # Do not forget to keep the primary keys values in this list of dictionaries.
#        # Also keep the same order in you want to populate the tables.
#        # You may ignore to add values of fields that are auto populated,
#        # or assigned default values in the db definition.
#        # Do not define datetime values for such respective keys

#        final_model_data = [
#            {'status_id': 1, 'status_name': "Active"},
#            {'status_id': 3, 'status_name': "Inactive"},
#            {'status_id': 2, 'status_name': "Fuzzy"},
#        ]
        
#        # define the below mentioned parameters for this model
#        primary_key_var = "status_id"
#        model_name = "TimelineSampleStatus"
#        model_instance = TimelineSampleStatus
#        model_serializer_instance = TimelineSampleStatusSerializer
        
#        # do not change the piece of code below. Keep it as such
#        populate_master_data_params = dict(zip(['primary_key_var', 'model_name', 'model_instance',
#                                                'model_serializer_instance', 'final_model_data'],
#                                               [primary_key_var, model_name, model_instance,
#                                                model_serializer_instance, final_model_data]))
#        output_json = populate_master_data(populate_master_data_params, table_population_output_list)
#        return output_json
#
#    except Exception as ex:
#        output_json = dict(zip(['Status', 'Message', 'Payload'],
#                               ["Failure", f"Exception encountered while calling function "
#                                           f"to populate master table data: {ex}", None]))
#        return output_json
        
# Step 5: Copy paste the below code in the function defined in step 2 and follow the comments within the code
#    """
#    This function populates all the master table data of the app named timeline
#    This function will insert additional records. In case you want to update then it will update them as well
#    :return:
#    """
#    try:
#        # copy paste the below line for every master model that you want to populate for this app
#        # Note the naming convention of the function below.
#        # There has to be separate functions for each model, all written one below the other in this file.
#        table_population_output_list = populate_timeline_sample_status(table_population_output_list)
#        table_population_output_list = populate_timeline_sample_status_two(table_population_output_list)

#        return table_population_output_list

#    except Exception as ex:
#        output_json = dict(zip(['Status', 'Message', 'Payload'],
#                               ["Failure", f"One or more master tables of timeline app could not be populated."
#                                           "Exception encountered: {ex}", table_population_output_list]))
#        return output_json
        
# Step 6: import the function defined in step 2 in the file common/utilities/populate_all_master_tables.py
# Step 7: write the below line of code inside the function named populate_all_master_tables 
# just before the line where output_json is defined. You will find where to write this by following the comments in that function
#        table_population_output_list = populate_<<app_name>>_master_tables(table_population_output_list)
