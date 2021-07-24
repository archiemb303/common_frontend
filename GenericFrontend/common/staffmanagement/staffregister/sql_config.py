from migrate_sql.config import SQLItem

sql_items = [
    SQLItem(
        'sp_check_if_staff',  # name of the item
        """
        CREATE OR REPLACE FUNCTION public.sp_check_if_staff(
        staff_ref refcursor,
        profile_id integer )
        RETURNS refcursor
        LANGUAGE 'plpgsql'

        COST 100
        VOLATILE
        AS $BODY$
        BEGIN
        OPEN staff_ref FOR
        select * from public.staffregister_staffs where staff_profile_id_id = profile_id and staff_status_id = 1;
        RETURN staff_ref;
        END;
        $BODY$;
        """,
        # sql for removal
        reverse_sql='drop function sp_check_if_staff(refcursor,integer);',
    ),
]
