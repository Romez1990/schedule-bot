from src.migrations.migration import Migration


class SubscriptionMigration(Migration):
    create_table = '''
        CREATE TABLE IF NOT EXISTS public.subscriptions (
            id serial PRIMARY KEY,
            user_id integer NOT NULL,
            "group" character varying(40) NOT NULL
        )
    '''

    create_relationships = '''
        ALTER TABLE ONLY public.subscriptions
            ADD CONSTRAINT subscriptions_users_id_fk FOREIGN KEY (user_id) REFERENCES public.users(id)
                ON DELETE CASCADE
    '''
