from migrate_sql.config import SQLItem

sql_items = [
    SQLItem(
        'sp_fetch_all_ticket_types_and_questions',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.sp_fetch_all_ticket_types_and_questions(
            profile_ref refcursor)
            RETURNS refcursor
            LANGUAGE 'plpgsql'

            COST 100
            VOLATILE 
            AS $BODY$
            BEGIN
            OPEN profile_ref FOR
                select lefttable.type_id, lefttable.type_name, righttable.common_question_id, righttable.common_question_text
                from 
                        public.supportcentre_postlogintickettypes lefttable
                    left outer join
                        public.supportcentre_postlogincommonquestionsbytickettypes righttable
                    on
                        lefttable.type_id = righttable.ticket_type_id_id
                order by lefttable.type_id, righttable.common_question_id;

            RETURN profile_ref;
            END;
            $BODY$;

        ''',

        reverse_sql='drop function sp_fetch_all_ticket_types_and_questions(refcursor);',  # sql for removal
    ),

    SQLItem(
        'sp_fetch_questions_by_ticket_type',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.sp_fetch_questions_by_ticket_type(
            profile_ref refcursor,
            ticket_type_id integer)
            RETURNS refcursor
            LANGUAGE 'plpgsql'

            COST 100
            VOLATILE 
            AS $BODY$
            BEGIN
            OPEN profile_ref FOR
                select 
                    common_question_id, common_question_text 
                from 
                    public.supportcentre_postlogincommonquestionsbytickettypes 
                where 
                    ticket_type_id_id =ticket_type_id
                order by common_question_id 
                    ;

            RETURN profile_ref;
            END;
            $BODY$;

        ''',

        reverse_sql='drop function sp_fetch_questions_by_ticket_type(refcursor, integer);',  # sql for removal
    ),

    SQLItem(
        'fetch_all_ticket_for_user',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.fetch_all_ticket_for_user(
            profile_ref refcursor,
            pid integer)
            RETURNS refcursor
            LANGUAGE 'plpgsql'

            COST 100
            VOLATILE 
            AS $BODY$
            BEGIN
            OPEN profile_ref FOR
                select 
                    a.ticket_id, a.ticket_subject, a.ticket_query,
                    a.ticket_status_id, a.ticket_type_id, a.ticket_question_id,
                    a.added_date, a.last_modified_date, a.ticket_owner_id,
                    b.status_name,
                    c.type_name,
                    d.common_question_text,
                    e.reply_id, e.ticket_reply,  e.added_by_id as replied_by,
                    (case when e.added_date is null then a.added_date else e.added_date end) as reply_date,
                    concat(g.first_name,' ',g.last_name) as ticket_owner_name
                from 
                    public.supportcentre_postlogintickets a
                    left outer join
                    public.supportcentre_postloginticketstatus b
                    on a.ticket_status_id = b.status_id
                    left outer join
                    public.supportcentre_postlogintickettypes c
                    on a.ticket_type_id = c.type_id
                    left outer join
                    public.supportcentre_postlogincommonquestionsbytickettypes d
                    on a.ticket_question_id = d.common_question_id
					left outer join
					(
					    SELECT rs.reply_id,rs.ticket_reply, rs.added_by_id, rs.added_date, rs.ticket_id_id
                        FROM (
                            SELECT reply_id,ticket_reply, added_by_id,added_date , ticket_id_id, ROW_NUMBER() 
                              OVER (Partition BY ticket_id_id
                                    ORDER BY added_date DESC ) AS Rank
                            FROM public.supportcentre_postloginticketsreplies
                            ) rs WHERE Rank <= 3
					) e
					on a.ticket_id = e.ticket_id_id
                    left outer join 
					public.registration_userprofile g
					on a.ticket_owner_id = g.profile_id
                where 
                    ticket_owner_id = pid
                order by 
					reply_date desc    
                ;

            RETURN profile_ref;
            END;
            $BODY$;

        ''',

        reverse_sql='drop function fetch_all_ticket_for_user(refcursor, integer);',  # sql for removal
    ),

    SQLItem(
        'sp_fetch_all_tickets',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.sp_fetch_all_tickets(
            ticket_ref refcursor)
            RETURNS refcursor
            LANGUAGE 'plpgsql'

            COST 100
            VOLATILE 
            AS $BODY$
            BEGIN
            OPEN ticket_ref FOR
                select 
                    a.ticket_id, a.ticket_subject, a.ticket_query,
                    a.ticket_status_id, a.ticket_type_id, a.ticket_question_id,
                    a.added_date, a.last_modified_date, a.ticket_owner_id,
                    b.status_name,
                    c.type_name,
                    d.common_question_text,
                    e.reply_id, e.ticket_reply,  e.added_by_id as replied_by,
                    (case when e.added_date is null then a.added_date else e.added_date end) as reply_date,
                    concat(g.first_name,' ',g.last_name) as ticket_owner_name
                from 
                    public.supportcentre_postlogintickets a
                    left outer join
                    public.supportcentre_postloginticketstatus b
                    on a.ticket_status_id = b.status_id
                    left outer join
                    public.supportcentre_postlogintickettypes c
                    on a.ticket_type_id = c.type_id
                    left outer join
                    public.supportcentre_postlogincommonquestionsbytickettypes d
                    on a.ticket_question_id = d.common_question_id
                    left outer join
                    (
                        SELECT rs.reply_id,rs.ticket_reply, rs.added_by_id, rs.added_date, rs.ticket_id_id
                        FROM (
                            SELECT reply_id,ticket_reply, added_by_id,added_date , ticket_id_id, ROW_NUMBER() 
                              OVER (Partition BY ticket_id_id
                                    ORDER BY added_date DESC ) AS Rank
                            FROM public.supportcentre_postloginticketsreplies
                            ) rs WHERE Rank <= 3
                        ) e
                    on a.ticket_id = e.ticket_id_id
                    left outer join 
                    public.registration_userprofile g
                    on a.ticket_owner_id = g.profile_id
                order by 
                    reply_date desc    
                ;

            RETURN ticket_ref;
            END;
            $BODY$;

        ''',

        reverse_sql='drop function sp_fetch_all_tickets(refcursor);',  # sql for removal
    ),

    SQLItem(
        'fetch_ticket_replies',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.fetch_ticket_replies(
            profile_ref refcursor,
            tid integer)
            RETURNS refcursor
            LANGUAGE 'plpgsql'

            COST 100
            VOLATILE 
            AS $BODY$
            BEGIN
            OPEN profile_ref FOR
                select 
                    a.ticket_id, a.ticket_subject, a.ticket_query,
                    a.ticket_status_id, a.ticket_type_id, a.ticket_question_id,
                    a.added_date, a.last_modified_date, a.ticket_owner_id,
                    b.status_name,
                    c.type_name,
                    d.common_question_text,
                    e.reply_id, e.ticket_reply,  e.added_by_id as replied_by,
                    (case when e.added_date is null then a.added_date else e.added_date end) as reply_date,
                    concat(g.first_name,' ',g.last_name) as ticket_owner_name
                from 
                    public.supportcentre_postlogintickets a
                    left outer join
                    public.supportcentre_postloginticketstatus b
                    on a.ticket_status_id = b.status_id
                    left outer join
                    public.supportcentre_postlogintickettypes c
                    on a.ticket_type_id = c.type_id
                    left outer join
                    public.supportcentre_postlogincommonquestionsbytickettypes d
                    on a.ticket_question_id = d.common_question_id
                    left outer join
                    public.supportcentre_postloginticketsreplies e
                    on a.ticket_id = e.ticket_id_id
                    left outer join 
                    public.registration_userprofile g
                    on a.ticket_owner_id = g.profile_id
                where 
                    a.ticket_id = tid
                order by 
                    reply_date
                ;

            RETURN profile_ref;
            END;
            $BODY$;

        ''',

        reverse_sql='drop function fetch_ticket_replies(refcursor, integer);',  # sql for removal
    ),

    SQLItem(
        'sp_check_if_ticket_owner',  # name of the item
        """
        CREATE OR REPLACE FUNCTION public.sp_check_if_ticket_owner(
        ticket_ref refcursor,
        owner_id integer,
        ticketid integer
        )
        RETURNS refcursor
        LANGUAGE 'plpgsql'

        COST 100
        VOLATILE
        AS $BODY$
        BEGIN
        OPEN ticket_ref FOR
        select * 
        from
            public.supportcentre_postlogintickets 
        where 
            ticket_id = ticketid and ticket_owner_id = owner_id;
        RETURN ticket_ref;
        END;
        $BODY$;
        """,
        # sql for removal
        reverse_sql='drop function sp_check_if_ticket_owner(refcursor,integer,integer);',
    ),
    SQLItem(
        'sp_fetch_ticket_details',  # name of the item
        """
        CREATE OR REPLACE FUNCTION public.sp_fetch_ticket_details(
        ticket_ref refcursor,
        ticketid integer
        )
        RETURNS refcursor
        LANGUAGE 'plpgsql'

        COST 100
        VOLATILE
        AS $BODY$
        BEGIN
        OPEN ticket_ref FOR
        select * 
        from
            public.supportcentre_postlogintickets 
        where 
            ticket_id = ticketid;
        RETURN ticket_ref;
        END;
        $BODY$;
        """,
        # sql for removal
        reverse_sql='drop function sp_fetch_ticket_details(refcursor,integer);',
    ),

    SQLItem(
        'filter_all_ticket_for_user',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.filter_all_ticket_for_user(
            profile_ref refcursor,
            pid integer,
            query varchar)
            RETURNS refcursor
            LANGUAGE 'plpgsql'

            COST 100
            VOLATILE 
            AS $BODY$
            BEGIN
            OPEN profile_ref FOR
                select 
                    a.ticket_id, a.ticket_subject, a.ticket_query,
                    a.ticket_status_id, a.ticket_type_id, a.ticket_question_id,
                    a.added_date, a.last_modified_date, a.ticket_owner_id,
                    b.status_name,
                    c.type_name,
                    d.common_question_text,
                    e.reply_id, e.ticket_reply,  e.added_by_id as replied_by,
                    (case when e.added_date is null then a.added_date else e.added_date end) as reply_date,
                    concat(g.first_name,' ',g.last_name) as ticket_owner_name
                from 
                    public.supportcentre_postlogintickets a
                    left outer join
                    public.supportcentre_postloginticketstatus b
                    on a.ticket_status_id = b.status_id
                    left outer join
                    public.supportcentre_postlogintickettypes c
                    on a.ticket_type_id = c.type_id
                    left outer join
                    public.supportcentre_postlogincommonquestionsbytickettypes d
                    on a.ticket_question_id = d.common_question_id
					left outer join
					(
					    SELECT rs.reply_id,rs.ticket_reply, rs.added_by_id, rs.added_date, rs.ticket_id_id
                        FROM (
                            SELECT reply_id,ticket_reply, added_by_id,added_date , ticket_id_id, ROW_NUMBER() 
                              OVER (Partition BY ticket_id_id
                                    ORDER BY added_date DESC ) AS Rank
                            FROM public.supportcentre_postloginticketsreplies
                            ) rs WHERE Rank <= 3
					) e
					on a.ticket_id = e.ticket_id_id
                    left outer join 
					public.registration_userprofile g
					on a.ticket_owner_id = g.profile_id
                where 
                    ticket_owner_id = pid
                and
                (
                    lower(a.ticket_query) like lower(query)
                    or
                    lower(a.ticket_subject) like lower(query)
                )
                order by 
					reply_date desc    
                ;

            RETURN profile_ref;
            END;
            $BODY$;

        ''',

        reverse_sql='drop function filter_all_ticket_for_user(refcursor, integer, varchar);',  # sql for removal
    ),

    SQLItem(
        'sp_filter_all_tickets',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.sp_filter_all_tickets(
            ticket_ref refcursor,
            query varchar)
            RETURNS refcursor
            LANGUAGE 'plpgsql'

            COST 100
            VOLATILE 
            AS $BODY$
            BEGIN
            OPEN ticket_ref FOR
                select 
                    a.ticket_id, a.ticket_subject, a.ticket_query,
                    a.ticket_status_id, a.ticket_type_id, a.ticket_question_id,
                    a.added_date, a.last_modified_date, a.ticket_owner_id,
                    b.status_name,
                    c.type_name,
                    d.common_question_text,
                    e.reply_id, e.ticket_reply,  e.added_by_id as replied_by,
                    (case when e.added_date is null then a.added_date else e.added_date end) as reply_date,
                    concat(g.first_name,' ',g.last_name) as ticket_owner_name
                from 
                    public.supportcentre_postlogintickets a
                    left outer join
                    public.supportcentre_postloginticketstatus b
                    on a.ticket_status_id = b.status_id
                    left outer join
                    public.supportcentre_postlogintickettypes c
                    on a.ticket_type_id = c.type_id
                    left outer join
                    public.supportcentre_postlogincommonquestionsbytickettypes d
                    on a.ticket_question_id = d.common_question_id
                    left outer join
                    (
                        SELECT rs.reply_id,rs.ticket_reply, rs.added_by_id, rs.added_date, rs.ticket_id_id
                        FROM (
                            SELECT reply_id,ticket_reply, added_by_id,added_date , ticket_id_id, ROW_NUMBER() 
                              OVER (Partition BY ticket_id_id
                                    ORDER BY added_date DESC ) AS Rank
                            FROM public.supportcentre_postloginticketsreplies
                            ) rs WHERE Rank <= 3
                        ) e
                    on a.ticket_id = e.ticket_id_id
                    left outer join 
                    public.registration_userprofile g
                    on a.ticket_owner_id = g.profile_id
                where 
                    lower(a.ticket_query) like lower(query)
                    or
                    lower(a.ticket_subject) like lower(query)
                order by 
                    reply_date desc    
                ;

            RETURN ticket_ref;
            END;
            $BODY$;

        ''',

        reverse_sql='drop function sp_filter_all_tickets(refcursor, varchar);',  # sql for removal
    ),

]

