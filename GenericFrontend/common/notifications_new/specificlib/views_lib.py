from common.notifications_new.serializers import SuperNotificationsSerializer, IndividualNotificationsSerializer
from common.notifications_new.models import IndividualNotifications
from common.utilities.lib import sql_fetch_cursor, serializer_save, update_record


def find_user_notifications_sql(request):
    """
    This function finds all notifications for a user from SuperNotifications.
    :param request: {'profile_id': 186
                     }
    """
    input_json, output_json = request, {}
    try:
        sql = sql_fetch_cursor("sp_find_user_notifications  ", 'invoice_ref',
                               ['invoice_ref', input_json['profile_id']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Error while fetching details: {ex}", None]))
        return output_json


def populate_notifications_sql(request):
    """
        This function is used to populate notifications in IndividualNotifications
        :param request: {
                            'profile_id':277,
                            'notification_id_list':[1,2,3]
                         }
        """
    input_json, output_json = request, {}
    try:
        for i in input_json['notification_id_list']:
            populate_notification_params = dict(zip(['super_notification_id', 'notification_status',
                                                     'profile_id', 'added_by', 'last_modified_by'],
                                                    [i, 1, input_json['profile_id'],
                                                     input_json['profile_id'], input_json['profile_id']]))
            serializer_var = serializer_save(IndividualNotificationsSerializer, populate_notification_params)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Notifications was populated successfully', None]))
        return output_json
    except Exception as ex:
        output_json = dict(
            zip(['Status', 'Message', 'Payload'], ['Failure', f'Unable to create Notification.{ex}', None]))
        return output_json


def fetch_my_notifications_sql(request):
    """
    This function fetches all notifications for a user from IndividualNotifications
    :param request: {'profile_id': 186}
    """
    input_json, output_json = request, {}
    try:
        sql = sql_fetch_cursor("sp_fetch_my_notifications", 'invoice_ref',
                               ['invoice_ref', input_json['profile_id']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Error while fetching details: {ex}", None]))
        return output_json


def create_notification(request):
    """
        This function is used to create notification
        :param request: {
                            'notification_text':'new ticket is raised',
                            'type_id':1,
                            'distribution_type_id': 1,
                            'notifier_profile_id': 32/null,
                            'notified_profile_id':55/null,
                            'algorithm_id':10/null,
                            'redirection_url':'url_for_redirection',
                            'comments':'important comment'
                         }
        """
    input_json = request
    try:
        create_notification_params = dict(zip(['type_id', 'distribution_type_id',
                                               'notification_text', 'redirection_url', 'notification_status',
                                               'notifier_profile_id', 'notified_profile_id', 'algorithm_id', 'comments',
                                               'added_by', 'last_modified_by'],
                                              [input_json['type_id'], input_json['distribution_type_id'],
                                               input_json['notification_text'], input_json['redirection_url'],
                                               1, input_json['notifier_profile_id'], input_json['notified_profile_id'],
                                               input_json['algorithm_id'], input_json['comments'],
                                               input_json['profile_id'], input_json['profile_id']]))
        serializer_var = serializer_save(SuperNotificationsSerializer, create_notification_params)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Notification was created successfully', serializer_var.data]))
        return output_json
    except Exception as ex:
        output_json = dict(
            zip(['Status', 'Message', 'Payload'], ['Failure', f'Unable to create Notification.{ex}', None]))
        return output_json


def update_notifications_as_seen():
    """
        This function is used to update all unseen notifications to seen.
        :param request: { }
        """
    try:
        update_var = IndividualNotifications.objects.filter(notification_status=1).update(notification_status=2)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Notification was updated successfully', None]))
        return output_json
    except Exception as ex:
        output_json = dict(
            zip(['Status', 'Message', 'Payload'], ['Failure', f'Unable to update Notification Status.{ex}', None]))
        return output_json


def update_notifications_status(request):
    """
        This function is used to update notification for a notification.
        :param request: {
                            'individual_notification_id':5,
                            'notification_status':3
                        }
        """
    input_json = request
    try:
        update_record_var = update_record(IndividualNotifications, input_json['individual_notification_id'],
                                          notification_status=input_json['notification_status'])
        return update_record_var
    except Exception as ex:
        output_json = dict(
            zip(['Status', 'Message', 'Payload'], ['Failure', f'Unable to update Notification Status.{ex}', None]))
        return output_json
