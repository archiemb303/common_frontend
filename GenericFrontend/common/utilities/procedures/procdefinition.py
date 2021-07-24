fetch_profile_from_mobileverification11 = """
    CREATE OR REPLACE FUNCTION public.fetch_profile_mobileverification11(
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
        """

fetch_profile_records6 = """
CREATE OR REPLACE FUNCTION public.fetch_profile_records6(
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
"""

fetch_profile_from_uuid8 = """
CREATE OR REPLACE FUNCTION public.fetch_profilefromuuid8(
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
pid:=(select a.profile_id_id from registration_uuidtoprofileidmap a where uuid_id_id=uuidid);
-- pid:= (select uuid_id_id from public.registration_uuidtoprofileidmap b
--  where b.uuid_id_id =uid);
OPEN profile_ref FOR select * from registration_userprofile where profile_id=pid;
RETURN profile_ref;
END;
$BODY$;
"""
fetch_uuid_for_guid8 = """
CREATE OR REPLACE FUNCTION public.fetch_profile_records6(
	uuid_ref refcursor,
	guid character varying)
    RETURNS refcursor
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE

AS $BODY$
--  DECLARE uid character varying ;
-- DECLARE pid integer;
BEGIN
-- pid:=(select a.profile_id from registration_uuidtoprofileidmap a where uuid_id_id=uuidid);
-- pid:= (select uuid_id_id from public.registration_uuidtoprofileidmap b
--  where b.uuid_id_id =uid);
OPEN uuid_ref FOR select * from registration_uuid where source_uuid=guid;
RETURN uuid_ref;
END;
 $BODY$;
"""
fetch_profile_from_uuid9 = """
CREATE OR REPLACE FUNCTION public.fetch_profilefromuuid8(
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
pid:=(select a.profile_id_id from registration_uuidtoprofileidmap a where uuid_id_id=uuidid);
-- pid:= (select uuid_id_id from public.registration_uuidtoprofileidmap b
--  where b.uuid_id_id =uid);
-- checking
OPEN profile_ref FOR select * from registration_userprofile where profile_id=pid;
RETURN profile_ref;
END;
$BODY$;
"""

fetch_profile_from_mobileverification12 = """
    CREATE OR REPLACE FUNCTION public.fetch_profile_mobileverification11(
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
        """