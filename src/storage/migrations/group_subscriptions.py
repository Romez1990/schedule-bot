from storage.migration_runner import Migration, migration


@migration
class GroupSubscriptionsMigration(Migration):
    create_table = '''
        CREATE TABLE group_subscriptions (
            id serial PRIMARY KEY,
            chat_id int NOT NULL,
            group_name character varying(40) NOT NULL
        )
    '''

    create_relationships = '''
        ALTER TABLE group_subscriptions
            ADD CONSTRAINT group_subscriptions_chats_id_fk
                FOREIGN KEY (chat_id) REFERENCES chats
                    ON UPDATE  CASCADE ON DELETE  CASCADE
    '''
