from migrate_sql.config import SQLItem

sql_items = [
    SQLItem(
        'sp_fetch_emailverificationotp',  # name of the item
    '''
    CREATE OR REPLACE FUNCTION public.sp_fetch_emailverificationotp(
        email_ref refcursor,
        emailid character varying)
        RETURNS refcursor
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
    AS $BODY$
    BEGIN
    
    OPEN email_ref FOR select * from registration_emailverificationotp where email_id=emailid;
    RETURN email_ref;
    END;
     $BODY$;
'''
),
SQLItem(
        'sp_fetch_mapuuidtoprofileid',  # name of the item
    ''' 

    CREATE OR REPLACE FUNCTION public.sp_fetch_mapuuidtoprofileid(
        uuid_id character varying)
        RETURNS TABLE(map_id integer, added_date timestamp with time zone, added_by character varying, last_modified_date timestamp with time zone, last_modified_by character varying, profile_id_id integer, status_id integer, uuid_id_id character varying) 
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
        ROWS 1000
    AS $BODY$
    
    BEGIN
    RETURN QUERY
    SELECT * FROM public.registration_uuidtoprofileidmap a
    where a.uuid_id_id = uuid_id;
    END;
    $BODY$;
    '''
),
SQLItem(
        'sp_fetch_mapuuidtoprofileid',  # name of the item
    '''
    CREATE OR REPLACE FUNCTION public.sp_fetch_mobileverification_row(
        phonenumber bigint)
        RETURNS TABLE(mobileverification_id integer, phone_number bigint, otp integer, login_count integer, added_date timestamp with time zone, added_by character varying, last_modified_date timestamp with time zone, last_modified_by character varying, country_id_id integer, mobilverification_status_id integer, uuid_id character varying) 
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
        ROWS 1000
    AS $BODY$
    
    BEGIN
    RETURN QUERY
    SELECT * FROM public.registration_mobileverification a
    where a.phone_number = phonenumber;
    END;
    $BODY$;
    '''
),
SQLItem(
        'sp_fetch_profile',  # name of the item

    '''
    CREATE OR REPLACE FUNCTION public.sp_fetch_profile(
        profile_ref refcursor,
        profileid integer)
        RETURNS refcursor
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
    AS $BODY$
    --  DECLARE uid character varying ;
    -- DECLARE pid integer;
    BEGIN
    -- uid:=(select a.uuid_id from registration_emailverification a where email_id=emailid);
    -- pid:= (select profile_id_id from public.registration_uuidtoprofileidmap b
    --  where b.uuid_id_id =uid);
    OPEN profile_ref FOR select * from registration_userprofile where profile_id=profileid;
    RETURN profile_ref;
    END;
     $BODY$;
    '''
    ),
    SQLItem(
        'sp_fetch_profile',  # name of the item

        '''
     
    CREATE OR REPLACE FUNCTION public.fetch_profile_details(
        pid integer)
        RETURNS TABLE(email character varying, firstname character varying, lastname character varying, gender character varying, dateofbirth date, location character varying) 
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
        ROWS 1000
    AS $BODY$
    #variable_conflict use_column
    DECLARE em_id character varying := 0;
    DECLARE city_name character varying := Null;
    BEGIN
    em_id:=
    (select email_id from public.registration_emailverificationotp
    where uuid_id=
    (select uuid_id_id from public.registration_uuidtoprofileidmap where profile_id_id=pid));--em_id:=(select email_id from public.registration_usercredentials
    --where account_verification_id_id=
    --(select emailverification_id from public.registration_emailverification where uuid_id=
    --(select uuid_id_id from public.registration_uuidtoprofileidmap where profile_id_id=pid)));
    city_name:=(SELECT city_name FROM public.location_cities WHERE city_id =(SELECT city_id_id  FROM public.registration_userprofile  WHERE profile_id =pid));
    
    RETURN QUERY
    SELECT em_id ,first_name AS firstname,last_name AS lastname,sex AS gender,date_of_birth AS dateofbirth,city_name as locatin FROM public.registration_userprofile  a
    WHERE a.profile_id = pid AND a.profile_status_id=1;
    
    END;
    $BODY$;

'''
),


SQLItem(
        'sp_fetch_profile_emailverification ',  # name of the item
    '''
    CREATE OR REPLACE FUNCTION public.sp_fetch_profile_emailverification(
        profile_ref refcursor,
        emailid character varying)
        RETURNS refcursor
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
    AS $BODY$
     DECLARE uid character varying ;
    DECLARE pid integer;
    BEGIN
    uid:=(select a.uuid_id from registration_emailverification a where email_id=emailid);
    pid:= (select profile_id_id from public.registration_uuidtoprofileidmap b
     where b.uuid_id_id =uid);
    OPEN profile_ref FOR select * from registration_userprofile where profile_id=pid;
    RETURN profile_ref;
    END;
     $BODY$;

    '''
),
SQLItem(
        'sp_fetch_profile_emailverificationotp ',  # name of the item
    '''
    
    CREATE OR REPLACE FUNCTION public.sp_fetch_profile_emailverificationotp(
        profile_ref refcursor,
        emailid character varying)
        RETURNS refcursor
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
    AS $BODY$
     DECLARE uid character varying ;
    DECLARE pid integer;
    BEGIN
    uid:=(select a.uuid_id from registration_emailverificationotp a where email_id =emailid);
    pid:= (select profile_id_id from public.registration_uuidtoprofileidmap b
     where b.uuid_id_id =uid);
    OPEN profile_ref FOR select * from registration_userprofile where profile_id=pid;
    RETURN profile_ref;
    END;
     $BODY$;

    '''
),
SQLItem(
        'sp_fetch_profile_mobileverificationotp ',  # name of the item
    '''

    CREATE OR REPLACE FUNCTION public.sp_fetch_profile_mobileverification(
        profile_ref refcursor,
        phonenumber bigint)
        RETURNS refcursor
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
    AS $BODY$
     DECLARE uid character varying ;
    DECLARE pid integer;
    BEGIN
    uid:=(select a.uuid_id_id from registration_mobileverification a where phone_number=phonenumber);
    pid:= (select profile_id_id from public.registration_uuidtoprofileidmap b
     where b.uuid_id_id =uid);
    OPEN profile_ref FOR select * from registration_userprofile where profile_id=pid;
    RETURN profile_ref;
    END;
     $BODY$;
    '''
),
SQLItem(
        'sp_fetch_profile_records ',  # name of the item
    '''
    CREATE OR REPLACE FUNCTION public.sp_fetch_profile_records(
        profile_ref refcursor,
        profileid integer)
        RETURNS refcursor
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
    AS $BODY$
    --  DECLARE uid character varying ;
    -- DECLARE pid integer;
    BEGIN
    -- uid:=(select a.uuid_id from registration_emailverification a where email_id=emailid);
    -- pid:= (select profile_id_id from public.registration_uuidtoprofileidmap b
    --  where b.uuid_id_id =uid);
    OPEN profile_ref FOR select * from registration_userprofile where profile_id=profileid;
    RETURN profile_ref;
    END;
     $BODY$;

    '''
),
SQLItem(
        'sp_fetch_profilefromuuid ',  # name of the item
    '''
    CREATE OR REPLACE FUNCTION public.sp_fetch_profilefromuuid(
        profile_ref refcursor,
        uuidid character varying)
        RETURNS refcursor
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
    AS $BODY$
    --  DECLARE uid character varying ;
    DECLARE pid integer;
    BEGIN
    pid:=(select a.profile_id from registration_uuidtoprofileidmap a where uuid_id_id=uuidid);
    -- pid:= (select uuid_id_id from public.registration_uuidtoprofileidmap b
    --  where b.uuid_id_id =uid);
    OPEN profile_ref FOR select * from registration_userprofile where profile_id_id=pid;
    RETURN profile_ref;
    END;
     $BODY$;
    '''
),
SQLItem(
        'sp_fetch_row ',  # name of the item
    '''
    CREATE OR REPLACE FUNCTION public.sp_fetch_row(
        emailvalue character varying)
        RETURNS TABLE(emailverification_id integer, first_name character varying, last_name character varying, email_id character varying, activation_key character varying, added_date timestamp with time zone, added_by character varying, last_modified_date timestamp with time zone, last_modified_by character varying, history character varying, activation_status_id integer, uuid_id character varying) 
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
        ROWS 1000
    AS $BODY$
    
    BEGIN
    RETURN QUERY
    SELECT * FROM public.registration_emailverification a
    where a.email_id = emailvalue;
    END;
    $BODY$;


    '''
),
    SQLItem(
        "sp_fetch_uuid_from_email",  # name of the item
        """
        CREATE OR REPLACE FUNCTION public.sp_fetch_uuid_from_email(
        uuid_ref refcursor,
        emailid character varying)
        RETURNS refcursor
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
    AS $BODY$
    
    BEGIN
    OPEN uuid_ref FOR select * from registration_emailverificationotp where email_id= emailid;
    RETURN uuid_ref;
    END;
     $BODY$;
        """,
        reverse_sql='drop function sp_fetch_uuid_from_email(refcursor, character varying);'
    ),
    SQLItem(
        'sp_fetch_profile_email_phone',  # name of the item
        """
        CREATE OR REPLACE FUNCTION public.sp_fetch_profile_email_phone(
            profile_ref refcursor,
            emailphone character varying)
            RETURNS refcursor
            LANGUAGE 'plpgsql'
        
            COST 100
            VOLATILE 
        AS $BODY$
        BEGIN
        
        OPEN profile_ref FOR select * from registration_userprofile where added_by like emailphone;
        RETURN profile_ref;
        END;
         $BODY$;
    """,
        reverse_sql='drop function sp_fetch_profile_email_phone(refcursor, character varying);'
    ),

 ]