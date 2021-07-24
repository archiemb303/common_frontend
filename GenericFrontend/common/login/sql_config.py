from migrate_sql.config import SQLItem

sql_items = [
    SQLItem(
        "sp_get_social_login_secret_key", """
        CREATE OR REPLACE FUNCTION public.sp_get_social_login_secret_key(
	secretkey_ref refcursor, sourceid integer
	)
    RETURNS refcursor
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE

AS $BODY$

BEGIN

OPEN secretkey_ref FOR select socialloginsecret_key from registration_wdsocialloginsecretkey where
source_id=sourceid and status_id=1;

RETURN secretkey_ref;
END;
$BODY$;
""",
        reverse_sql= 'drop function sp_get_social_login_secret_key(refcursor, integer);'

    ),
    SQLItem(
        "sp_fetch_profile_from_email", """
        CREATE OR REPLACE FUNCTION public.sp_fetch_profile_from_email(
	profile_ref refcursor,
	emailid character varying)
    RETURNS refcursor
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE

AS $BODY$
BEGIN

OPEN profile_ref FOR select * from registration_userprofile where added_by=emailid; 
RETURN profile_ref;
END;
$BODY$;
""",
        reverse_sql= 'drop function sp_fetch_profile_from_email(refcursor, character varying);'

    ),
]