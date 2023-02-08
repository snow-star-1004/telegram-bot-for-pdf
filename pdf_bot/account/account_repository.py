from google.cloud.datastore import Client, Entity

from pdf_bot.consts import LANGUAGE, USER


class AccountRepository:
    def __init__(self, datastore_client: Client) -> None:
        self.datastore_client = datastore_client

    def get_user(self, user_id: int) -> Entity | None:
        key = self.datastore_client.key(USER, user_id)
        entity: Entity | None = self.datastore_client.get(key)

        return entity

    def upsert_user(self, user_id: int, language_code: str) -> None:
        with self.datastore_client.transaction():
            key = self.datastore_client.key(USER, user_id)
            db_user = self.datastore_client.get(key)

            if db_user is None:
                db_user = Entity(key)
            if LANGUAGE not in db_user:
                db_user[LANGUAGE] = language_code

            self.datastore_client.put(db_user)
