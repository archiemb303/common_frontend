import itertools
from django.db import connection, transaction
from collections import defaultdict
from common.utilities.libfiles import dictfetchall
from common.registration.serializers import MobileVerificationSerializer


def sql_exec(procname, *args):
    """Call Procedure to perform db operation"""
    with connection.cursor() as cursor:
        cursor.callproc(procname, *args)
        qs = dictfetchall(cursor)
        return qs


def sql_fetch_cursor(procname, arg1, *args):
    """Call Procedure to perform db operation"""
    with transaction.atomic(), connection.cursor() as cursor:
        cursor.callproc(procname, *args)
        cursor.execute(f"FETCH ALL FROM {arg1}")
        qs = dictfetchall(cursor)
        return qs


def sql_execute_query(query):
    """Call Procedure to perform db operation"""
    with transaction.atomic(), connection.cursor() as cursor:
        cursor.execute(query)
        return


def get_all_procs_query(query):
    """Call Procedure to perform db operation"""
    with transaction.atomic(), connection.cursor() as cursor:
        cursor.execute(query)
        row = dictfetchall(cursor)
        proc_list = [row[i]['function_name'] for i in range(len(row))]
        return proc_list


def verification_func(func):
    def inner(*args, **kwargs):
        returned_value = func(*args, **kwargs)
        return returned_value
    return inner


@verification_func
def serializer_save(model_serializer, input_json):

    serializer_var = model_serializer(data=input_json)
    if serializer_var.is_valid(raise_exception=True):
        serializer_var.save()
    return serializer_var


@verification_func
def serializer_save_multiple(model_serializer, input_json):

    serializer_var = model_serializer(data=input_json, many=True)
    if serializer_var.is_valid(raise_exception=True):
        serializer_var.save()
    return serializer_var


@verification_func
def serializer_partial_save(model_serializer, input_json):
    serializer_var = model_serializer(data=input_json, partial=True)
    if serializer_var.is_valid(raise_exception=True):
        serializer_var.save()
    return serializer_var

# @verification_func


def serializer_update(model_serializer, queryobj, input_json):
    serializer_var = model_serializer(queryobj, data=input_json)
    if serializer_var.is_valid(raise_exception=True):
        serializer_var.save()
    return serializer_var


def update_query1(arg1, **kwargs):
    first_index = dict(list(kwargs.items())[0: 1])
    arg1.objects.filter(**first_index).update(kwargs)
    qs = arg1.objects.filter(**first_index).all()
    return qs.values()[0]


def update_query(arg1, arg2, **kwargs):
    # dict1 = dict(itertools.islice(kwargs.items(), 1))
    # # temp = dict1.keys()
    # # value = dict1['temp']
    # list1, list2=[], []
    # for key,val in dict1.items():
    #     list1.append(key), list2.append(val)
    # # print(list1, list2)
    # # value=dict2[temp]
    # temp, val=list1[0], list2[0]
    # dict3={}
    # dict3[temp]= val
    arg1.objects.filter(pk=arg2).update(kwargs)
    qs = arg1.objects.filter(pk=arg2).all()
    return qs.values()[0]


def sel_flag(arg1, arg2, arg3):
    """select flag out of given options, below mentioned sample code."""
    # options = defaultdict(lambda: dict(zip(['Status', 'Message'],
    #                                        ["Failure",
    #                                         "Something went wrong while receiving invitation."])),
    #                       {0: 'raj', 1:'shyam', 2:'rohit'})
    options = defaultdict(arg1, arg2)
    return options[arg3]


def update_record(model, index, **kwargs):
    """This function is used to update records within a table identified by its Primary Key """
    modelobj = model.objects.filter(pk=index)
    modelobj.update(**kwargs)
    qs = model.objects.filter(pk=index).all()
    return qs.values()[0]


def update_record_multiple(model, index_list, **kwargs):
    """This function is used to update multiple records within a table identified by their Primary Key """
    modelobj = model.objects.filter(pk__in=index_list)
    modelobj.update(**kwargs)
    qs = model.objects.filter(pk__in=index_list).all()
    return qs.values()[0]