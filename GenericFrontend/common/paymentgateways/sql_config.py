from migrate_sql.config import SQLItem

sql_items = [
    SQLItem(
        'sp_fetch_all_payment_gateways',  # name of the item
        """
        CREATE OR REPLACE FUNCTION public.sp_fetch_all_payment_gateways(
        wallet_ref refcursor)
        RETURNS refcursor
        LANGUAGE 'plpgsql'

        COST 100
        VOLATILE
        AS $BODY$
        BEGIN
        OPEN wallet_ref FOR
        select * from public.paymentgateways_paymentgateways where pg_status_id = 1
        order by pg_id
        ;
        RETURN wallet_ref;
        END;
        $BODY$;
        """,
        # sql for removal
        reverse_sql='drop function sp_fetch_all_payment_gateways(refcursor);',
    ),

    SQLItem(
            'sp_payment_gateways_details',  # name of the item
            """
            CREATE OR REPLACE FUNCTION public.sp_payment_gateways_details(
            wallet_ref refcursor,
            pgid integer )
            RETURNS refcursor
            LANGUAGE 'plpgsql'
    
            COST 100
            VOLATILE
            AS $BODY$
            BEGIN
            OPEN wallet_ref FOR
            select * from public.paymentgateways_paymentgateways where pg_id = pgid
            ;
            RETURN wallet_ref;
            END;
            $BODY$;
            """,
            # sql for removal
            reverse_sql='drop function sp_payment_gateways_details(refcursor, integer);',
        ),

    SQLItem(
            'sp_fetch_pg_trans_all_details',  # name of the item
            """
            CREATE OR REPLACE FUNCTION public.sp_fetch_pg_trans_all_details(
            wallet_ref refcursor,
            pg_trans_id character varying )
            RETURNS refcursor
            LANGUAGE 'plpgsql'
    
            COST 100
            VOLATILE
            AS $BODY$
            BEGIN
            OPEN wallet_ref FOR
            	
            select 
                a.*, b.interest_id_id, c.user_profile_id_id, c.wallet_package_id_id,
                d.package_name, d.no_of_credits, d.package_price,
                e.geo_currency_id as package_currency_id, e.tax_percentage,
                f.currency_name as package_currency_name,
                g.currency_name as transaction_currency_name,
                h.pg_name, h.associated_self_financial_accounts_id,
                i.wallet_id, i.wallet_balance,
                j.account_id, j.account_type_id, j.currency_id as account_currency,
				concat(k.first_name, ' ', k.last_name) as customer_name
                
            from 
                public.paymentgateways_paymentgatewaytransactions a
                left outer join
                public.userwalletsandpackages_userpackageinteresttopgtranmap b
                on a.pg_transaction_id = b.pg_tran_id_id
                left outer join
                public.userwalletsandpackages_userpackageinterest c
                on b.interest_id_id = c.user_interest_id
                left outer join
                public.userwalletsandpackages_userwalletpackages d
                on c.wallet_package_id_id = d.package_id
                left outer join
                public.location_geos e
                on d.package_geo_id = e.geo_id
                left outer join
                public.location_currencies f
                on e.geo_currency_id = f.currency_id
                left outer join
                public.location_currencies g
                on a.actual_transaction_currency_id = g.currency_id
                left outer join
                public.paymentgateways_paymentgateways h
                on a.pg_id_id = h.pg_id
                left outer join 
                (select * from public.userwalletsandpackages_userwallets where wallet_type_id=1 and wallet_status_id=1) i
                on c.user_profile_id_id=i.profile_id_id
                left outer join
                public.ownaccountsandledger_selfaccounts j
                on h.associated_self_financial_accounts_id = j.account_id
				left outer join public.registration_userprofile k
				on c.user_profile_id_id = k.profile_id
            where 
                pg_transaction_id = pg_trans_id

            ;
            RETURN wallet_ref;
            END;
            $BODY$;
            """,
            # sql for removal
            reverse_sql='drop function sp_fetch_pg_trans_all_details(refcursor, character varying);',
        ),

    ]