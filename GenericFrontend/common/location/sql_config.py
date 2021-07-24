from migrate_sql.config import SQLItem

sql_items = [
    SQLItem(
        'sp_fetch_cities_by_stateid',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.sp_fetch_cities_by_stateid(
            stateid integer)
            RETURNS TABLE(city_id integer, city_name character varying, added_by character varying, added_date timestamp with time zone, last_modified_by character varying, last_modified_date timestamp with time zone, state_id integer) 
            LANGUAGE 'plpgsql'
        
            COST 100
            VOLATILE 
            ROWS 1000
        AS $BODY$
        BEGIN
        RETURN QUERY
        select * from public.location_cities a
        where a.state_id_id = stateid  ORDER BY city_name ASC ;
        END;
        $BODY$;
        
    '''
    ),
    SQLItem(
        'sp_fetch_states_by_countryid',  # name of the item
        '''
 
    CREATE OR REPLACE FUNCTION public.sp_fetch_states_by_countryid(
         countryid integer)
         RETURNS TABLE(state_id integer, state_name character varying, added_by character varying, added_date timestamp with time zone, last_modified_by character varying, last_modified_date timestamp with time zone, country_id integer) 
         LANGUAGE 'plpgsql'
     
         COST 100
         VOLATILE 
         ROWS 1000
     AS $BODY$
     BEGIN
     RETURN QUERY
     select * from public.location_states a
     where a.country_id_id = countryid  ORDER BY state_name ASC ;
     END;
     $BODY$;
    '''
     
     ),

    SQLItem(
            'sp_fetch_city',  # name of the item
            '''
    
    CREATE OR REPLACE FUNCTION public.sp_fetch_city(
        city_ref refcursor,
        cityid integer)
        RETURNS refcursor
        LANGUAGE 'plpgsql'
    
        COST 100
        VOLATILE 
    AS $BODY$
    
    DECLARE cid integer;
    BEGIN
    cid:=(select a.state_id_id from location_cities a where city_id=cityid);
    OPEN city_ref FOR select * from location_states where state_id=cid;
    RETURN city_ref;
    END;
    $BODY$;
    '''
    ),


    SQLItem(
            'sp_fetch_city',  # name of the item
            '''

        CREATE OR REPLACE FUNCTION public.fetch_city(
            city_ref refcursor,
            cityid integer)
            RETURNS refcursor
            LANGUAGE 'plpgsql'
        
            COST 100
            VOLATILE 
        AS $BODY$
        
        DECLARE cid integer;
        BEGIN
        cid:=(select a.state_id_id from location_cities a where city_id=cityid);
        OPEN city_ref FOR select * from location_states where state_id=cid;
        RETURN city_ref;
        END;
        $BODY$;
    '''
    ),

    SQLItem(
        'fetch_user_location_by_profile_id',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.fetch_user_location_by_profile_id(
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
                     b.city_id, b.city_name, 
                     c.state_id, c.state_name, 
                     d.country_id, d.country_name, 
                     e.geo_id, e.geo_name, e.tax_percentage,
                     f.currency_id, f.currency_name
                from 
                    public.registration_userprofile a
                    left outer join
                    public.location_cities b
                    on a.city_id_id = b.city_id
                    
                    left outer join
                    public.location_states c
                    on b.state_id_id = c.state_id
                    
                    left outer join
                    public.location_countries d
                    on c.country_id_id = d.country_id
                    
                    left outer join
                    public.location_geos e
                    on d.geo_id_id = e.geo_id
                    
                    left outer join
                    public.location_currencies f
                    on e.geo_currency_id = f.currency_id
                where 
                    a.profile_id = pid
                ;

            RETURN profile_ref;
            END;
            $BODY$;

        ''',

        reverse_sql='drop function fetch_user_location_by_profile_id(refcursor, integer);',  # sql for removal
    ),

    SQLItem(
        'fetch_user_location_by_iso_country_name',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.fetch_user_location_by_iso_country_name(
            profile_ref refcursor,
            iso3 character varying,
            iso2 character varying,
            cntry_name character varying)
            RETURNS refcursor
            LANGUAGE 'plpgsql'

            COST 100
            VOLATILE 
            AS $BODY$
            BEGIN
            OPEN profile_ref FOR
                select 
                    d.country_id, d.country_name, 
                    e.geo_id, e.geo_name, e.tax_percentage,
                    f.currency_id, f.currency_name
                from
                    (
                        select country_id, country_name, geo_id_id, 1 as output_rank from public.location_countries
                        where 
                            lower(country_code_iso3) = lower(iso3)
                    union
                        select country_id, country_name, geo_id_id, 2 as output_rank from public.location_countries
                        where 
                            lower(country_code_iso2) = lower(iso2)
                    union
                        select country_id, country_name, geo_id_id,  3 as output_rank from public.location_countries
                        where 
                            lower(country_name) = lower(cntry_name)
                    order by output_rank
                    ) d
                    
                    left outer join
                    public.location_geos e
                    on d.geo_id_id = e.geo_id
                    
                    left outer join
                    public.location_currencies f
                    on e.geo_currency_id = f.currency_id
                ;

            RETURN profile_ref;
            END;
            $BODY$;

        ''',

        reverse_sql='drop function fetch_user_location_by_iso_country_name(refcursor, character varying, character varying, character varying);',  # sql for removal
    ),

    SQLItem(
        'sp_fetch_currency_id_from_text',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.sp_fetch_currency_id_from_text(
            profile_ref refcursor,
            currency_text character varying
            )
            RETURNS refcursor
            LANGUAGE 'plpgsql'

            COST 100
            VOLATILE 
            AS $BODY$
            BEGIN
            OPEN profile_ref FOR
                select * from public.location_currencies where currency_name = currency_text
                ;

            RETURN profile_ref;
            END;
            $BODY$;

        ''',

        reverse_sql='drop function sp_fetch_currency_id_from_text(refcursor, character varying);',  # sql for removal
    ),

    SQLItem(
        'sp_fetch_all_currencies',  # name of the item
        '''
        CREATE OR REPLACE FUNCTION public.sp_fetch_all_currencies(
            profile_ref refcursor
            )
            RETURNS refcursor
            LANGUAGE 'plpgsql'

            COST 100
            VOLATILE 
            AS $BODY$
            BEGIN
            OPEN profile_ref FOR
                select * from public.location_currencies
                ;

            RETURN profile_ref;
            END;
            $BODY$;

        ''',

        reverse_sql='drop function sp_fetch_all_currencies(refcursor);',  # sql for removal
    ),


    ]
