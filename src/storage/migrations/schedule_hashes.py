from storage.migration_runner import Migration, migration


@migration
class ScheduleHashesMigration(Migration):
    create_table = '''
        CREATE TABLE public.schedule_hashes (
            id serial PRIMARY KEY,
            starts_at date NOT NULL,
            hash int NOT NULL
        )
    '''
