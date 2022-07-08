from storage.migration_runner import Migration, migration


@migration
class ChatsMigration(Migration):
    create_table = '''
        CREATE TABLE chats (
            id serial PRIMARY KEY,
            messenger character varying(40) NOT NULL,
            messenger_id character varying(40) NOT NULL
        )
    '''
