from .migration import Migration


class UserMigration(Migration):
    create_table = '''
        CREATE TABLE IF NOT EXISTS public.users (
            id serial PRIMARY KEY,
            platform character varying(40) NOT NULL,
            platform_id character varying(40) NOT NULL
        )
    '''
