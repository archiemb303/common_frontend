from migrate_sql.config import SQLItem

sql_items = [
    SQLItem(
        'sp_find_user_notifications',  # name of the item
        """
        CREATE OR REPLACE FUNCTION public.sp_find_user_notifications(
        notification_ref refcursor,
        profile_id integer )
        RETURNS refcursor
        LANGUAGE 'plpgsql'

        COST 100
        VOLATILE
        AS $BODY$
        BEGIN
        OPEN notification_ref FOR
        select 
            * 
        from 
            public.notifications_new_supernotifications
        where 
            (distribution_type_id_id = 3
        or 
            (distribution_type_id_id = 1 and notified_profile_id_id = profile_id))
        and 
            notification_id not in 
            (select 
                super_notification_id_id 
            from 
                public.notifications_new_individualnotifications
            );
        RETURN notification_ref;
        END;
        $BODY$;
        """,
        # sql for removal
        reverse_sql='drop function sp_find_user_notifications(refcursor,integer);',
    ),
    SQLItem(
        'sp_fetch_my_notifications',  # name of the item
        """
        CREATE OR REPLACE FUNCTION public.sp_fetch_my_notifications(
        notification_ref refcursor,
        pid integer )
        RETURNS refcursor
        LANGUAGE 'plpgsql'
        COST 100
        VOLATILE
        AS $BODY$
        BEGIN
        OPEN notification_ref FOR
        select 
            a.individual_notification_id,a.notification_status_id,a.super_notification_id_id,a.profile_id_id,
            b.notification_text,b.redirection_url,b.comments,b.notifier_profile_id_id,b.added_date,
            b.notified_profile_id_id,b.distribution_type_id_id,b.type_id_id,
            c.first_name as notifier_first_name,c.last_name as notifier_last_name,e.status_name,
            (case when b.type_id_id = 1 then '../../../../assets/icons/app_logo_1x1.png' 
             else (case when d.media_image_url is not null then d.media_image_url else 
             (case when lower(c.sex) = 'male' 
              then 'https://akstagefe.com/assets/images/male-avatar.png' 
              when lower(c.sex) = 'female' 
              then 'https://akstagefe.com/assets/images/female-avatar.png'  
              else
              'https://akstagefe.com/assets/images/unisex-avatar.jpg'
              end)
             end) end) as media_image_url
        from 
            public.notifications_new_individualnotifications a
        left outer join 
            public.notifications_new_supernotifications b
        on a.super_notification_id_id = b.notification_id
        left outer join 
            public.registration_userprofile c
        on b.notifier_profile_id_id = c.profile_id
        left outer join
                (
                    select 
                        a.*,
                        b.file_content, b.media_static_path,
                        concat(b.media_static_path, b.file_content) as media_image_url
                    from 
                        public.media_dp a
                        left outer join
                        public.media_medialibrary b
                        on a.media_id_id = b.media_id
                    where status_id_id =1
                    ) d
                    on b.notifier_profile_id_id = d.profile_id_id
            left outer join
             public.notifications_new_individualnotificationstatus e
        on e.status_id = a.notification_status_id
        where 
            a.profile_id_id = pid
        order by b.added_date desc;
        RETURN notification_ref;
        END;
        $BODY$;
        """,
        # sql for removal
        reverse_sql='drop function sp_fetch_my_notifications(refcursor,integer);',
    )
]
