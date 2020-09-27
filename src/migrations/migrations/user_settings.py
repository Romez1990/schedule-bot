from src.migrations.migration import Migration


class UserSettingsMigration(Migration):
    create_table = '''
        CREATE TABLE IF NOT EXISTS user_settings(
            user_id serial PRIMARY KEY,
            theme character varying(40)
        )
    '''

    create_relationships = '''
        ALTER TABLE ONLY public.user_settings
            ADD CONSTRAINT user_settings_users_id_fk FOREIGN KEY (user_id) REFERENCES public.users(id)
                ON DELETE CASCADE
    '''
