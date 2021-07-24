from migrate_sql.config import SQLItem

sql_items = [
    SQLItem(
        'sp_fetch_website_maintenance_flags',  # name of the item
        """
        CREATE OR REPLACE FUNCTION public.sp_fetch_website_maintenance_flags(
        invoice_ref refcursor )
        RETURNS refcursor
        LANGUAGE 'plpgsql'

        COST 100
        VOLATILE
        AS $BODY$
        BEGIN
        OPEN invoice_ref FOR
        
        select a.launch_flag, b.state_flag
        from
            (select 
                (case when now()>=launch_date then 1 else 0 end) as launch_flag
             from public.website_management_websitelaunchinfo
             where launch_info_status_id = 1
            ) a,
            (select 
                (case when count(downtime_info_id)>0 then 0 else 1 end) as state_flag
             from public.website_management_websitedowntime
             where downtime_start_datetime<= now() and downtime_end_datetime>= now()
             and downtime_info_status_id = 1
            ) b
        
        ;
        RETURN invoice_ref;
        END;
        $BODY$;
        """,
        # sql for removal
        reverse_sql='drop function sp_fetch_website_maintenance_flags(refcursor);',
    ),
]
