sp_var_fetch_profile_from_mobileverification = """  
    CREATE OR REPLACE FUNCTION public.sp_fetch_profile_from_mobileverification(
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

sp_var_fetch_profile_records = """
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
"""

sp_var_fetch_profile_from_uuid = """
CREATE OR REPLACE FUNCTION public.sp_fetch_profile_from_uuid(
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

sp_var_fetch_uuid_for_guid = """
CREATE OR REPLACE FUNCTION public.sp_fetch_uuid_for_guid(
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

sp_var_fetch_profile_from_uuid11 = """
CREATE OR REPLACE FUNCTION public.sp_fetch_profile_from_uuid11(
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

sp_var_fetch_profile_from_uuid12 = """
CREATE OR REPLACE FUNCTION public.sp_fetch_profile_from_uuid12(
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

sp_var_fetch_profile_from_uuid15 = """
CREATE OR REPLACE FUNCTION public.sp_fetch_profile_from_uuid15(
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

sp_var_fetch_profile_from_uuid16 = """
CREATE OR REPLACE FUNCTION public.sp_fetch_profile_from_uuid16(
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

sp_var_fetch_profile_from_uuid17 = """
CREATE OR REPLACE FUNCTION public.sp_fetch_profile_from_uuid17(
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



