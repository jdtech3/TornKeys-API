from pony.orm import *

# --- Schema and Init ---

db = Database()


class Member(db.Entity):
    id = PrimaryKey(int, auto=True)
    api_key = Required(str, unique=True)
    discord_id = Optional(int, size=64, unique=True)
    torn_id = Required(int, unique=True)


db.bind(provider='sqlite', filename='db.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


# --- Wrapper functions (CRUD) ---

@db_session
def create_member(api_key: str, discord_id: int, torn_id: int):
    Member(api_key=api_key, discord_id=discord_id, torn_id=torn_id)


@db_session
def get_member(value: int, by: str):
    if by in ['discord_id', 'torn_id']:
        member = Member.get(**{by: value})

        if member is not None:
            return {
                'id': member.id,
                'api_key': member.api_key,
                'discord_id': member.discord_id,
                'torn_id': member.torn_id
            }
        else:
            return None

    else:
        raise ValueError('Invalid \'by\' type, supported types are: \'discord_id\' and \'torn_id\'')
