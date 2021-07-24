from common.utilities.lib import sql_fetch_cursor, serializer_save


def check_if_staff_sql(request):
    """
    This function checks existing chatroom for given participants
    :param request: {
                        'profile_id': 186,
                    }
    """
    input_json, output_json = request, {}
    try:
        sql = sql_fetch_cursor("sp_check_if_staff", 'staff_ref',
                               ['staff_ref', input_json['profile_id']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ["Failure",
                                                                  f"Exception Encountered while "
                                                                  f"fetching details: {ex} ", None]))
        return output_json
