""" This contains the lib files for populating master tables"""
import re


def compare_items_to_populate(request):
    """
    This function compares the new set of items that need to be populated in the master table
    against the current items that are there in the table.
    It then returns the output of what all rows need to be updated, inserted,
    and the rows that are there in the existing set but not in new set and hence need to be removed

    :param request:
        {
            'model_fields': ['status_id', 'status_name']
            'new_list' : [{}, {}],
            'existing_list': [{}, {}],
            'primary_key': 'status_id'
        }
    :return:
        {
            'items_to_update': [{}, {}],
            'items_to_insert': [{}, {}]
            'items_to_ignore': [{}, {}]
            'items_to_remove': [{}, {}]
        }
    """

    input_json = request
    output_json = dict(zip(['action', 'observations', 'items_to_update', 'items_to_insert',
                            'items_to_ignore', 'items_to_remove'],
                           ["proceed", "All data fine to process", [], [], [], []]))
    try:
        new_list_keys, existing_list_keys = [], []

        # Checking if keys in new list are there in the existing models. If not then the process is aborted
        for key in input_json['new_list'][0].keys():
            new_list_keys.append(key)
        if len(input_json['existing_list']) == 0:
            for item in input_json['model_fields']:
                existing_list_keys.append(item.name)
        else:
            for key in input_json['existing_list'][0].keys():
                existing_list_keys.append(key)

        key_comparison = set(new_list_keys).issubset(set(existing_list_keys))
        if not key_comparison:
            output_json['action'] = "abort"
            output_json['observations'] = "Keys mismatch between new_list and existing_list"
            return output_json
        #####################################################################################
        # if current db is empty then insert all records from new_list
        if len(input_json['existing_list']) == 0:
            output_json['items_to_insert'] = input_json['new_list']
            return output_json
        #####################################################################################

        # find items that need to be updated, ignored, and inserted
        for existing_list_item in input_json['existing_list']:
            # finding items that are currently in the db but not in new list
            if existing_list_item[input_json['primary_key']] \
                    not in [x[input_json['primary_key']] for x in input_json['new_list']]:
                output_json['items_to_remove'].append(existing_list_item)
                continue
            # finding items to ignore, update
            for new_list_item in input_json['new_list']:
                if existing_list_item[input_json['primary_key']] == new_list_item[input_json['primary_key']]:
                    operation_var = "ignore"
                    for key in new_list_keys:
                        if existing_list_item[key] != new_list_item[key]:
                            operation_var = "update"
                            output_json['items_to_update'].append(new_list_item)
                            break
                    if operation_var == "ignore":
                        output_json['items_to_ignore'].append(new_list_item)
                    break
        # finding items to insert
        output_json['items_to_insert'] = [x for x in input_json['new_list'] if x[input_json['primary_key']] not in
                                          [y[input_json['primary_key']] for y in input_json['existing_list']]]
        #####################################################################################

        if len(output_json['items_to_remove']) > 0:
            output_json['action'] = "abort"
            output_json['observations'] = "Existing table in db has data that are not defined in new list"
        return output_json
    except Exception as ex:
        output_json['action'] = "abort"
        output_json['observations'] = f"Exception encountered: {ex}"
        return output_json


def populate_master_data(request, table_population_output_list):
    """

    :param request:
        {
            "model_name":,
            "model_instance":,
            "model_serializer_instance":,
            "primary_key_var":,
            "final_model_data"
        }
    :return:
    """
    try:
        input_json = request
        table_population_output_var = dict(zip(['table_name', 'result', 'observations', 'actions'],
                                               [None, None, None, None]))
        ########################################################

        # initializing output
        table_population_output_var['table_name'] = input_json['model_name']
        ########################################################

        # getting current values of the master table
        current_model_data = input_json['model_serializer_instance'](input_json['model_instance'].objects.all(), many=True).data
        ########################################################

        # comparing information in master table with the ones defined above.
        db_actions_params = dict(zip(['model_fields', 'new_list', 'existing_list', 'primary_key'],
                                     [input_json['model_instance']._meta.get_fields(), input_json['final_model_data'],
                                      current_model_data, input_json['primary_key_var']]))
        db_actions_var = compare_items_to_populate(db_actions_params)
        ########################################################

        # Initiating function output
        table_population_output_var['table_name'] = input_json['model_name']
        table_population_output_var['result'] = db_actions_var['action']
        table_population_output_var['observations'] = db_actions_var['observations']
        table_population_output_var['actions'] = dict(zip(['items_to_ignore', 'items_to_update',
                                                           'items_to_insert', 'items_to_remove'],
                                                          [db_actions_var['items_to_ignore'],
                                                           db_actions_var['items_to_update'],
                                                           db_actions_var['items_to_insert'],
                                                           db_actions_var['items_to_remove']]))
        if db_actions_var['action'] == "abort":
            table_population_output_var['result'] = "aborted"
            table_population_output_var['observations'] = db_actions_var['observations']
            table_population_output_list.append(table_population_output_var)
            return table_population_output_list
        ########################################################

        # checking the order of the operations. If not in proper order then abort.
        # Eg. if a row needs to be inserted between existing rows, then abort
        db_actions_params = dict(zip(['primary_key', 'actions'],
                                     [input_json['primary_key_var'],
                                      table_population_output_var['actions']]))
        order_check_var = check_action_order(db_actions_params)
        match = re.findall(r"'Status': 'Failure'", str(order_check_var))
        if match or not order_check_var['Payload']:
            table_population_output_var['result'] = "aborted"
            table_population_output_var['observations'] = "model rows not defined in correct order"
            table_population_output_list.append(table_population_output_var)
            return table_population_output_list
        ########################################################

        # Performing db actions
        db_actions_params['model_instance'] = input_json['model_instance']
        db_actions_params['model_serializer_instance'] = input_json['model_serializer_instance']
        dp_operations_var = perform_action_on_master_tables(db_actions_params)
        match = re.findall(r"'Status': 'Failure'", str(dp_operations_var))
        if match or not order_check_var['Payload']:
            table_population_output_var['result'] = "action interrupted"
            table_population_output_var['observations'] = f"Issues happened while performing db actions on the tables+ {dp_operations_var}"
            table_population_output_list.append(table_population_output_var)
            return table_population_output_list

        table_population_output_var['result'] = "Data populated"
        table_population_output_var['observations'] = "Master table has been updated successfully"
        table_population_output_list.append(table_population_output_var)
        return table_population_output_list

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"One or more master tables of timeline app could not be populated."
                                           f"Exception encountered: {ex}", None]))
        return output_json


def check_action_order(request):
    """
    This function checks if the actions that need to be taken on master tables are in the correct order or not.
    If not then the action should be aborted
    :param request:
            {
                'primary_key': "status_id",
                'actions':
                {
                    'items_to_update': [],
                    'items_to_insert':
                        [
                            {'status_id': 1, 'status_name': 'Active'},
                            {'status_id': 2, 'status_name': 'Inactive'}
                        ],
                }
            }
    :return:
    """
    try:
        input_json, primary_key_list, verdict_var = request, [], False
        for item in input_json['actions']['items_to_update']:
            primary_key_list.append(item[input_json['primary_key']])
        for item in input_json['actions']['items_to_insert']:
            primary_key_list.append(item[input_json['primary_key']])
        if sorted(primary_key_list) == primary_key_list:
            verdict_var = True
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", "Operation order verified", verdict_var]))
        return output_json

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to verify item operation order. "
                                           f"Exception encountered: {ex}", None]))
        return output_json


def perform_action_on_master_tables(request):
    """
    This function first updates the existing records if needed followed by inserting new rows of data.
    :param request:
            {
                "model_instance":,
                "model_serializer_instance":,
                'primary_key': "status_id",
                'actions':
                {
                    'items_to_update': [],
                    'items_to_insert':
                        [
                            {'status_id': 1, 'status_name': 'Active'},
                            {'status_id': 2, 'status_name': 'Inactive'}
                        ],
                }
            }

    :return:
    """
    try:
        input_json = request
        # updating rows in the master table one by one
        for item in input_json['actions']['items_to_update']:
            update_params = dict()
            for item_key in item.keys():
                if item_key != input_json['primary_key']:
                    update_params[item_key] = item[item_key]
            row_qs = input_json['model_instance'](pk=item[input_json['primary_key']])
            serialized_update_var = input_json['model_serializer_instance'](row_qs, data=update_params)
            if serialized_update_var.is_valid(raise_exception=True):
                serialized_update_var.save()

        # inserting rows into the master table
        serialized_insertion_params = input_json['model_serializer_instance']\
            (data=input_json['actions']['items_to_insert'], many=True)
        if serialized_insertion_params.is_valid(raise_exception=True):
            serialized_insertion_params.save()

        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", f"DB operations performed successfully", None]))
        return output_json

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Issues encountered while updating master table. "
                                           f"Please update the table manually. Exception encountered: {ex}", None]))
        return output_json
